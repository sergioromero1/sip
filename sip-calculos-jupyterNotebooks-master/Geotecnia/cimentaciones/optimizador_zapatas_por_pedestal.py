import math
import json
import copy
import sys, traceback
from typing import List, Dict, Tuple, Any
from .zapata import Zapata
from .perfil import Perfil
from .cargas import Cargas
from .util import γ_agua, generar_serie
from .evaluador_zapatas import EvaluadorZapatas

DBFila = Dict[str, Any]

class OptimizadorZapatasPorPedestal():

    def __init__(self, evaluador: EvaluadorZapatas):
        self.evaluador = evaluador

    def optimizar(self, parametros: DBFila, torre: Torre, perfil: Perfil, info_cargas: Cargas, hg_por_pata: bool, n_soluciones:int, optimo_por_profundidad: bool = True, pausar_en_error: bool = True, usar_prof_min_desp_por_torre: bool = True) -> Dict[Tuple[float,float], Dict[str, Tuple[float,float,bool]]]:
        """
        Encuentra las zapatas óptimas para la torre:'torre', en el espacio B, D (ancho, profundidad),
        para cada uno de los pedestal de interés. El resultado de esta optimización es una lista con las
        'n_soluciones' soluciones ordenadas de mejor a peor respecto al volumen ponderado de la zapata.
        Cada solución consiste de un diccionario con la información geométrica de la zapata y 
        sub-diccionarios con la evaluación de los diferentes aspectos de su estabilidad geotécnica. Es
        posible que una mejor solución no cumpla con todos los requerimientos de estabilidad, en cuyo caso
        la zapata se ordena de acuerdo a la 'distancia' en que está la zapata de cumplir todos los requisitos.
        
        Arguments:
            parametros {DBFila} -- Diccionario con los parámetros de diseño
            torre {DBFila} -- Diccionario con los datos de la torre
            perfil {Perfil} -- Perfil estratigráfico asociado a la torre. Se corrige más adelante por saturación.
            info_cargas {Cargas} -- Información de cargas
            hg_por_pata {bool} -- Indica si se deben usar los HG (pedestales) de las patas de la 'torre' o la lista que viene en 'parametros'
            n_soluciones {int} -- Número de mejores soluciones para almacenar en la corrida
        
        Returns:
            {Lis[Dict]} -- Lista con la infomación de las zapatas óptimas
        """
        # Límites para el espacio de búsqueda B (ancho), D (profundidad)
        
        B_min = parametros["b_min"]        # B_min {float} -- Valor mínimo para las iteraciones de ancho de la zapata B [m]
        B_max = parametros["b_max"]        # B_max {float} -- Valor máximo para las iteraciones de ancho de la zapata B [m]
        B_paso = parametros["b_paso"]      # B_paso {float} -- Incremento para las iteraciones de ancho de la zapata B [m]
        D_min = parametros["d_min"]        # D_min {float} -- Valor mínimo para las iteraciones de la profundidad de la zapata D [m]
        D_max = parametros["d_max"]        # D_max {float} -- Valor máximo para las iteraciones de la profundidad de la zapata D [m]
        D_paso = parametros["d_paso"]      # D_paso {float} -- Incremento para las iteraciones de la profundidad de la zapata D [m]
                
        γ_c = parametros["gamma_c"]                   # Peso unitario de la cimentación. Se corrige más adelante por saturación. [kN/m³]
        θ = info_cargas.get_angulo_inclinacion(torre) # Ángulo del pedestal con respecto a la vertical [°]

        perf_roca_min = parametros["perf_roca_min"]                    # perf_roca_min {float} -- Perforación mínima de la zapata a la roca [m]
        perf_roca_max = parametros["perf_roca_max"]                    # perf_roca_max {float} -- Perforación máxima de la zapata a la roca [m]
        dist_atraccion_roca = parametros["dist_atraccion_roca"]        # dist_atraccion_roca {float} -- Distancia a la roca, a partir de la cual debe penetrar la zapata [m]

        # Factores de seguridad y restricciones
        FSC = parametros['fsc']
        FST_g = parametros['fst_g']
        FST_c = parametros['fst_c']
        FSV = parametros['fsv']
        FSL = parametros['fsl']        
        k = parametros['k']
        t = parametros['t']
        S_max_adm_c = parametros['s_max_adm_c']
        S_max_adm_g = parametros['s_max_adm_g']


        # TP: Lado correspondiente a la sección transversal del pedestal [m]    
        usar_TP = parametros["usar_tp"] # 
        if usar_TP:
            dict_TP = parametros["dict_tp"]
            TP = dict_TP[torre["tipo"]]
        else:
            d_agg = parametros["d_agg"]          # Tamaño máximo nominal del agregado grueso [m]
            d_b_long = parametros["d_b_long"]    # Diámetro de barras de refuerzo longitudinal [m]
            d_b_trans = parametros["d_b_trans"]  # Diámetro de barras de refuerzo transversal [m]
            rec = parametros["rec"]              # Longitud del recubrimiento del dado [m]
            ancho_aleta = info_cargas.get_ancho_aleta_conector_cortante(torre)
            TP = 2 * (1.5 * ancho_aleta + d_agg + d_b_long + d_b_trans + rec)
            TP = math.ceil(TP * 10) / 10 # Aproximación a la décima por arriba

        rec_fondo_stub = parametros['rec_fondo_stub']  # rec_fondo_stub {float} --Recubrimiento vertical en el fondo de la zapata para el stub [m]

        # Espesor del dado [m]
        H = parametros['h']
        usar_H = parametros['usar_h']
        if not usar_H:
            H = max(H, TP / 2)
        
        # Proyección vertical del stub
        pvs = info_cargas.get_proyeccion_vertical_stub(torre)

        # Revisión del D_min con la limitación del sitio de torre
        if usar_prof_min_desp_por_torre and torre.prof_min_desplante:
            D_min = max(D_min, torre.prof_min_desplante)

        # Aproxima D_min y D_max al decímetro
        D_min, D_max =  math.ceil(D_min * 10) / 10, math.ceil(D_max * 10) / 10            

        profundidad_roca = perfil.calcular_profundidad_hasta_roca()            

        # lista_HG {List[float]} -- Lista de altura de pedestales a evaluar [m] 
        lista_HG = copy.copy(parametros["lista_hg"])
        if hg_por_pata:
            if torre["ped_pata_a"] and not torre["ped_pata_a"] in lista_HG:
                lista_HG.append(torre["ped_pata_a"]) 
            if torre["ped_pata_b"] and not torre["ped_pata_b"] in lista_HG:
                lista_HG.append(torre["ped_pata_b"]) 
            if torre["ped_pata_c"] and not torre["ped_pata_c"] in lista_HG:
                lista_HG.append(torre["ped_pata_c"]) 
            if torre["ped_pata_d"] and not torre["ped_pata_d"] in lista_HG:
                lista_HG.append(torre["ped_pata_d"]) 
        lista_HG.sort()

        # Nivel freático incluyendo inundabilidad
        NF = perfil.calcular_NF()

        # Inclinación del terreno
        ω = torre.inclinacion_terreno or 0        
        
        # Inclinación de la base de la zapata
        α = torre.inclinacion_base_zapata or 0           

        # Se revisa si se puede calcular zapatas dadas las restricciones de profundidad mínima
        # de desplante y profundad máxima o profundidad de la roca
        if D_min > D_max:
            mensaje_error = f"Error: D_min > D_max. Prof. mínima desplante: {D_min}, Prof. máxima desplante: {D_max}"
            print(f"Error inesperado procesando: {mensaje_error}")
            if pausar_en_error:
                input("...")
            return [{"B": None, "D": None, "HG": None, "TP": None, "θ": None, "α": None, "ω": None, "error": True, "mensaje_error": mensaje_error, "evaluacion": {}}]  

        resultados = []
        for HG in lista_HG:
            resultados_por_hg = []
            # for B in generar_serie(B_min, B_max, B_paso, 2):
            B = B_min
            hay_solucion = False
            while True:
                entro_a_roca = False                
                for D in generar_serie(D_min, D_max, D_paso, 2):
                    perfil_ajustado = perfil
                    
                    # Valida si está cerca de roca (dist_atraccion_roca) para
                    # modificar el caso, cambiando la profundidad D
                    # a la que corresponda a 'perf_roca_min' dentro de  la roca
                    # si es necesario. Además, se valida que si está
                    # perforando la roca, no sobrepase perf_roca_max. Si esto
                    # sucede genera un error y sale.
                    # Estos distancia dentro de la roca se modelan como
                    # suelo para todos los cálculos de estabilidad,
                    # salvo la capacidad portante, que se asume un
                    # valor fijo de 493 kPa.
                    if profundidad_roca:
                        perf_roca = round(D - profundidad_roca, 2)
                        if perf_roca > perf_roca_max:
                            mensaje_error = f"Zapata sobrepasa la perforación máxima en roca. D: {D}. profundidad roca: {profundidad_roca}, perforación máxima permitida: {perf_roca_max}"
                            resultado = {"B": B, "D": D, "HG": None, "TP": TP, "θ": θ, "α": α, "ω": ω, "error": True, "mensaje_error": mensaje_error, "evaluacion": {}} 
                            self.clasificar_resultado(resultados, resultado, n_soluciones)
                            break
                        elif perf_roca >= -dist_atraccion_roca:
                            if perf_roca < perf_roca_min:
                                perf_roca = perf_roca_min
                                D = profundidad_roca + perf_roca_min
                            perfil_ajustado = copy.deepcopy(perfil)
                            perfil_ajustado.extender_suelo_a_roca(perf_roca)
                            entro_a_roca = True

                    # Se satura todo el perfil si
                    # el nivel freático esta por encima de
                    # la profundidad de desplante
                    if NF is not None and NF < D:
                        perfil_ajustado = perfil_ajustado.clonar_saturado()
                        ajuste_saturacion_perfil = True
                    else:
                        ajuste_saturacion_perfil = False
                    
                    # Zapata
                    C = D + HG - H
                    
                    if C < pvs + rec_fondo_stub - H:
                        resultado["error"] = True
                        resultado["mensaje_error"] = "Falla por stub"
                    else:
                        zapata = Zapata(B, B, D, H, C, TP, θ, γ_c, perfil_ajustado, 0, ω)
                        resultado = self.evaluador.evaluar(zapata, parametros, torre, perfil_ajustado, info_cargas, FSC, FST_g, FST_c, k, t, S_max_adm_c, S_max_adm_g, FSV, FSL)
                    
                    if (self.clasificar_resultado(resultados_por_hg, resultado, n_soluciones, optimo_por_profundidad)):
                        hay_solucion = True


            resultados.extend(resultados_por_hg)
        return resultados

    def clasificar_resultado(self, resultados: List, resultado: List, n_soluciones: int, optimo_por_profundidad: bool):
        mala_calificacion = (999999, 999999)

        if resultado["error"]:
            resultado["cumple"] = False
            resultado["calificacion"] = mala_calificacion
        else:
            evaluacion = resultado["evaluacion"]
            resultado["cumple"] = all([evaluacion[key]["cumple"] for key in evaluacion])
            incumplimientos = sum([1  for key in evaluacion if not evaluacion[key]["cumple"]])
            if incumplimientos == 0:
                resultado["calificacion"] = (incumplimientos, resultado["volumen_ponderado"])
            else:
                sum_desviaciones_fs =  math.sqrt(sum([evaluacion[key]["desviacion"]**2 for key in evaluacion if not evaluacion[key]["cumple"]]))
                resultado["calificacion"] = (incumplimientos, sum_desviaciones_fs)
        
        if optimo_por_profundidad:
            resultado_previo = next(iter([r for r in resultados if r["D"] == resultado["D"]]), None)
            if resultado_previo:
                if resultado_previo["calificacion"] > resultado["calificacion"]:
                    resultados.remove(resultado_previo)
                    resultados.append(resultado)
                    resultados.sort(key = lambda r: r["calificacion"])
            else:
                resultados.append(resultado)
                resultados.sort(key = lambda r: r["calificacion"])
        else:
            if len(resultados) < n_soluciones:
                resultados.append(resultado)
                resultados.sort(key = lambda r: r["calificacion"])
            elif resultado["calificacion"] <  resultados[-1]["calificacion"]:
                resultados[-1] = resultado
                resultados.sort(key = lambda r: r["calificacion"])
                
        return resultado["cumple"] 