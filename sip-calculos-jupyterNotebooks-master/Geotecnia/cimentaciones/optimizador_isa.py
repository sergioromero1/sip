import math
import json
import copy
import sys, traceback
from typing import List, Dict, Tuple, Any
from .zapata import Zapata
from .perfil import Perfil
from .torre import Torre
from .cargas import Cargas
from .util import γ_agua, generar_serie
from .evaluador_zapatas import EvaluadorZapatas

DBFila = Dict[str, Any]

class OptimizadorZapatasPorTorre():

    def __init__(self, evaluador: EvaluadorZapatas):
        self.evaluador = evaluador

    def optimizar(self, parametros: DBFila, torre: Torre, perfil: Perfil, info_cargas: Cargas, hg_por_pata: bool, n_soluciones:int, optimo_por_profundidad: bool = True, pausar_en_error: bool = True, usar_prof_min_desp_por_torre: bool = True, H: float = None ) -> Dict[Tuple[float,float], Dict[str, Tuple[float,float,bool]]]:
        """
        Encuentra las zapatas óptimas para la torre:'torre', en el espacio B, D (ancho, profundidad),
        que sirva para todos los pedestal de interés. El resultado de esta optimización es una lista con las
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
            hg_por_pata {bool} -- Indica si se debe tener en cuenta los pedestales de las torres además de la lista estándar 'lista_hg'
            n_soluciones {int} -- Número de mejores soluciones para almacenar en la corrida
            optimo_por_profundidad {bool} -- Indica si se deben reportar las mejores soluciones por profundidad (solo una solución por profundidad)
            pausar_en_error {bool} -- Indica si se debe pausar la ejecución si se presenta un error inesperado
        Returns:
            {Dict[Tuple[float,float], Dict[str, Tuple[float,float,bool]]]} -- Diccionario con la evaluación de zapata para cada tupla (B, D)
        """
        # Límites para el espacio de búsqueda B (ancho), D (profundidad)
        
        B_min = parametros["b_min"]        # B_min {float} -- Valor mínimo para las iteraciones de ancho de la zapata B [m]
        B_max = parametros["b_max"]        # B_max {float} -- Valor máximo para las iteraciones de ancho de la zapata B [m]
        B_extra = parametros['b_extra'] or parametros["b_max"]  # B_extra {float} -- Valor extra de búsqueda para el ancho de la zapata B si no encuentra solución con B_max [m]
        B_paso = parametros["b_paso"]      # B_paso {float} -- Incremento para las iteraciones de ancho de la zapata B [m]
        D_min = parametros["d_min"]        # D_min {float} -- Valor mínimo para las iteraciones de la profundidad de la zapata D [m]
        D_max = parametros["d_max"]        # D_max {float} -- Valor máximo para las iteraciones de la profundidad de la zapata D [m]
        D_paso = parametros["d_paso"]      # D_paso {float} -- Incremento para las iteraciones de la profundidad de la zapata D [m]
        
        γ_c = parametros["gamma_c"]                   # Peso unitario de la cimentación seco[kN/m³]
        θ = info_cargas.get_angulo_inclinacion(torre) # Ángulo del pedestal con respecto a la vertical [°]

        perf_roca_min = parametros["perf_roca_min"]                    # perf_roca_min {float} -- Perforación mínima de la zapata a la roca [m]
        perf_roca_max = parametros["perf_roca_max"]                    # perf_roca_max {float} -- Perforación máxima de la zapata a la roca [m]
        dist_atraccion_roca = parametros["dist_atraccion_roca"]        # dist_atraccion_roca {float} -- Distancia a la roca, a partir de la cual debe penetrar la zapata [m]

        # Factores de seguridad y restricciones
        FSC = parametros['fsc']                  # FSC {float} -- Factore de seguridad a compresión
        FST_g = parametros['fst_g']              # FST_g {float} -- Factor de seguridad a tensión suelo granular
        FST_c = parametros['fst_c']              # FST_c {float} -- Factor de seguridad a tensión suelo cohesivo
        FSV = parametros['fsv']                  # FSV {float} -- Factor de seguridad para volcamiento
        FSL = parametros['fsl']                  # FSL {float} -- Factor de seguridad para cargas laterales
        k = parametros['k']                      # k {int} -- Número de segmentos para análisis de asentamiento  
        t = parametros['t']                      # t {int} -- Número de años para corrección 'Creep'
        S_max_adm_c = parametros['s_max_adm_c']  # S_max_adm_c {float} -- Asentamiento máximo permitido suelos granulares [m]
        S_max_adm_g = parametros['s_max_adm_g']  # S_max_adm_g {float} -- Asentamiento máximo permitido suelos cohesivos [m]

        # TP: Lado correspondiente a la sección transversal del pedestal [m]    
        usar_TP = parametros["usar_tp"] 
        if usar_TP:
            dict_TP = parametros["dict_tp"]
            TP = dict_TP[torre.tipo]
        else:
            d_agg = parametros["d_agg"]          # d_agg {float} -- Tamaño máximo nominal del agregado grueso [m]
            d_b_long = parametros["d_b_long"]    # d_b_long {float} -- Diámetro de barras de refuerzo longitudinal [m]
            d_b_trans = parametros["d_b_trans"]  # d_b_trans {float} -- Diámetro de barras de refuerzo transversal [m]
            rec = parametros["rec"]              # rec {float} -- Longitud del recubrimiento del dado [m]
            ancho_aleta = info_cargas.get_ancho_aleta_conector_cortante(torre)
            TP = 2 * (1.5 * ancho_aleta + d_agg + d_b_long + d_b_trans + rec)
            TP = math.ceil(TP * 10) / 10         # Aproximación a la décima por arriba
        
        rec_fondo_stub = parametros['rec_fondo_stub']  # rec_fondo_stub {float} --Recubrimiento vertical en el fondo de la zapata para el stub [m]

        # Espesor del dado [m]
        if H is None:
            usar_H = parametros['usar_h']
            H = parametros['h']
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
            if torre.ped_pata_a and not torre.ped_pata_a in lista_HG:
                lista_HG.append(torre.ped_pata_a) 
            if torre.ped_pata_b and not torre.ped_pata_b in lista_HG:
                lista_HG.append(torre.ped_pata_b) 
            if torre.ped_pata_c and not torre.ped_pata_c in lista_HG:
                lista_HG.append(torre.ped_pata_c) 
            if torre.ped_pata_d and not torre.ped_pata_d in lista_HG:
                lista_HG.append(torre.ped_pata_d) 
        lista_HG.sort()

        # Nivel freático de campo
        NFC = perfil.nivel_freatico_exploracion

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
        #for B in generar_serie(B_min, B_max, B_paso, 2):
        B = B_min
        hay_solucion = False
        while True:
            entro_a_roca = False
            for D in generar_serie(D_min, D_max, D_paso, 2): """ aquí puede ingresar la entrada del D (mejor que pruebe 4 D's 0.5, 1, 2, 3) """
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
                        self.clasificar_resultado(resultados, resultado, n_soluciones, optimo_por_profundidad)
                        print(f"Rompe D porque rompe la roca más que {perf_roca_max}. B:{B}, D:{D}, profundidad_roca:{profundidad_roca}")
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
                
                # DA: Profundidad de la cimentación bajo el nivel freático de campo
                if NFC is not None and NFC < D:
                    DA = D - NFC
                else:
                    DA = 0

                # derrumbabilidad:
                derrumbabilidad = perfil_ajustado.calcular_derrumbabilidad(D)

                resultados_por_hg = []
                for HG in lista_HG:""" aqui va a haber un solo pedestal promedio"""
                    
                    resultado = {"B": B, "D": D, "HG": HG, "TP": TP, "θ": θ, "α": α, "ω": ω, "γ_c": γ_c, "error": False, "mensaje_error": None, "evaluacion": {}}  
                    try:
                        C = D + HG - H
                        
                        if C < pvs + rec_fondo_stub - H:
                            resultado["error"] = True
                            resultado["mensaje_error"] = "Falla por stub"
                        else:
                            zapata = Zapata(B, B, D, H, C, TP, θ, γ_c, perfil_ajustado, α, ω)
                            resultado["evaluacion"] = self.evaluador.evaluar(zapata, torre, perfil_ajustado, info_cargas, FSC, FST_g, FST_c, k, t, S_max_adm_c, S_max_adm_g, FSV, FSL)
                            resultado["H"] = zapata.H
                            resultado["ajuste_saturacion_perfil"] = ajuste_saturacion_perfil
                            resultado["da"] = DA
                            resultado["derrumbabilidad"] = derrumbabilidad
                            resultado["volumen_zapata"] = zapata.volumen()
                            resultado["volumen_relleno"] = zapata.volumen_relleno()
                            resultado["volumen_ponderado"] = (zapata.volumen() * 4 + zapata.volumen_relleno())/5
                            resultado["esbeltez"] = zapata.D / zapata.B
                            resultado["relleno"] = perfil.calcular_material_relleno(zapata.D - zapata.H)
                            resultado["parametros_suelo"] = self.calcular_parametros_generales_suelo(resultado["evaluacion"])
                            resultado["γ_c"] = zapata.γ_c

                    except Exception  as e:
                        resultado["error"] = True
                        resultado["mensaje_error"] = str(e)
                        print(f"Error inesperado procesando: Torre:{torre.nombre}, B:{B}, D:{D}, HG:{HG}, Error:{str(e)}")
                        traceback.print_exc(file=sys.stdout)
                        if pausar_en_error:
                            input("...")
                    except:
                        print(f"Error no interceptado en B:{B}, D:{D}")

                    finally:
                        resultados_por_hg.append(resultado)               

                # El optimizador encuentra la zapata óptima que funcione para todos
                # los pedestales. Requiere entonces sintetizar todos los resultados por pedestal
                # en uno solo, que sirva para comparar en la selección del óptimo
                resultado_grupo = self.integrar_resultados(resultados_por_hg)

                # Clasificación del resultado en busca de las mejores soluciones
                if (self.clasificar_resultado(resultados, resultado_grupo, n_soluciones, optimo_por_profundidad)):
                    hay_solucion = True

                if entro_a_roca:
                    print(f"Rompe D porque entró a roca. B:{B}, D:{D}")
                    break

            B = round(B + B_paso,2)
            if (B > B_max and hay_solucion) or B > B_extra:
                break

        return resultados

    def integrar_resultados(self, resultados_por_hg):
        resultado_grupo = {}
        resultado_grupo["B"] = resultados_por_hg[0]["B"]
        resultado_grupo["D"] = resultados_por_hg[0]["D"]
        resultado_grupo["HG"] = [r["HG"] for r in resultados_por_hg]
        resultado_grupo["TP"] = resultados_por_hg[0]["TP"]
        resultado_grupo["θ"] = resultados_por_hg[0]["θ"]
        resultado_grupo["α"] = resultados_por_hg[0]["α"]
        resultado_grupo["ω"] = resultados_por_hg[0]["ω"]
        resultado_grupo["γ_c"] = resultados_por_hg[0]["γ_c"]
        resultado_grupo["error"] = any([r["error"] for r in resultados_por_hg])
        if resultado_grupo["error"]:
            resultado_grupo["mensaje_error"] = ". ".join(set([r["mensaje_error"] for r in resultados_por_hg if r["error"]]))
            resultado_grupo["evaluacion"] = {}
            resultado_grupo["H"] = None
            resultado_grupo["ajuste_saturacion_perfil"] = None
            resultado_grupo["da"] = None
            resultado_grupo["derrumbabilidad"] = None
            resultado_grupo["volumen_zapata"] = None
            resultado_grupo["volumen_relleno"] = None
            resultado_grupo["volumen_ponderado"] = None
            resultado_grupo["esbeltez"] = None
            resultado_grupo["relleno"] = None
            resultado_grupo["parametros_suelo"] = None
        else:
            resultado_grupo["mensaje_error"] = None
            resultado_grupo["evaluacion"] = {}
            keys_verif = resultados_por_hg[0]["evaluacion"].keys()
            for key in keys_verif:
                resultado_grupo["evaluacion"][key] = max([r["evaluacion"][key] for r in resultados_por_hg], key = lambda x : x["desviacion"] if x["cumple"] else 9999999999 + x["desviacion"])
            resultado_grupo["H"] = max([r["H"] for r in resultados_por_hg])
            resultado_grupo["ajuste_saturacion_perfil"] = resultados_por_hg[0]["ajuste_saturacion_perfil"]
            resultado_grupo["da"] = resultados_por_hg[0]["da"]
            resultado_grupo["derrumbabilidad"] = resultados_por_hg[0]["derrumbabilidad"]
            resultado_grupo["volumen_zapata"] = max([r["volumen_zapata"] for r in resultados_por_hg])
            resultado_grupo["volumen_relleno"] = resultados_por_hg[0]["volumen_relleno"]
            resultado_grupo["volumen_ponderado"] = max([r["volumen_ponderado"] for r in resultados_por_hg])
            resultado_grupo["esbeltez"] = resultados_por_hg[0]["esbeltez"]
            resultado_grupo["relleno"] = resultados_por_hg[0]["relleno"]
            resultado_grupo["parametros_suelo"] = resultados_por_hg[0]["parametros_suelo"]

        return resultado_grupo

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

    def calcular_parametros_generales_suelo(self, evaluacion):
        tipo_mat = evaluacion["cap_port-comp_max"]["memoria_q_ult"]["tipo_mat"]
        γ = evaluacion["cap_port-comp_max"]["memoria_q_ult"]["γ"]
        φ = 0.0
        c_u = 0.0
        if tipo_mat == "c":
            c_u = evaluacion["cap_port-comp_max"]["memoria_q_ult"]["c_u"]
        elif tipo_mat == "g":
            φ = evaluacion["cap_port-comp_max"]["memoria_q_ult"]["φ"]
        elif tipo_mat == "r":
            φ = evaluacion["cap_port-comp_max"]["memoria_q_ult"]["φ"]
        return {"tipo_mat": tipo_mat, "γ": γ, "φ": φ, "c_u": c_u}
            