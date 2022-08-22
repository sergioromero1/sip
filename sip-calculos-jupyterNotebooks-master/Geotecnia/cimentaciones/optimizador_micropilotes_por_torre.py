import math
import json
import logging
import sys, traceback
from typing import List, Dict, Tuple, Any
from .micropilotes import Micropilotes
from .perfil import Perfil
from .torre import Torre
from .barra import Barra
from .cargas import Cargas
from .util import γ_agua, generar_serie,tan_g
from .evaluador_micropilotes import EvaluadorMicropilotes

DBFila = Dict[str, Any]

class OptimizadorMicropilotesPorTorre():

    def __init__(self, evaluador: EvaluadorMicropilotes):
        self.evaluador = evaluador

    def optimizar(self, parametros: DBFila, torre: Torre, perfil: Perfil, info_cargas: Cargas, usar_tabla_α_exp: bool = True, α_exp: float = None, pausar_en_error: bool = True) -> Dict[Tuple[float,float], Dict[str, Tuple[float,float,bool]]]:

        #
        # Información de Parámetros
        #
        b_max = parametros['b_max']                           # b_max {float} -- Distancia máxima del lado de zapata [m]
        n_soluciones = parametros['n_soluciones']             # n_soluciones {int} -- Número de soluciones para almacenar
        f_carga_por_torre = parametros['f_carga_por_torre']   # f_carga_por_torre {bool} -- Indica si la fracción de carga que toma el mp se toma por cada torre
        f_carga_mp_fijo = parametros['f_carga_mp_fijo']       # f_carga_mp_fijo {float} -- Si 'f_carga_por_torre' == False, fracción de carga fija que toma el mp de todas las torres [0.0 - 1.0]
        d_agg = parametros['d_agg']                           # d_agg {float} -- Tamaño máximo nominal del agregado grueso [m]
        d_b_long = parametros['d_b_long']                     # d_b_long {float} -- Diámetro de barras de refuerzo longitudinal [m]
        d_b_trans = parametros['d_b_trans']                   # d_b_trans {float} -- Diámetro de barras de refuerzo transversal [m]
        rec = parametros['rec']                               # rec {float} -- Espesor del recubrimiento [m]
        γ_c = parametros['gamma_c']                           # γ_c {float} -- Peso unitario de la cimentación [kN/m³]
        γ_l = parametros['gamma_l']                           # γ_l {float} -- Peso unitario de la lechada del micropilote [kN/m³]
        η = parametros["eta"]                                 # η {float} -- Eficiencia del grupo de micropilotes [-]
        f_pc = parametros["f_pc"]                             # f_pc {float} -- Resistencia a la compresión del concreto [kPa]
        f_py = parametros["f_py"]                             # f_py {float} -- Esfuerzo de fluencia de la barra de refuerzo [kPa]
        A_camisa = parametros["a_camisa"]                     # A_camisa {float} -- Área de la sección de la camisa [m²]
        lista_N_m = parametros["lista_N_m"]                   # lista_N_m {List[float]} -- Lista de valores posibles para el número de micropilotes
        lista_L_b = parametros["lista_L_b"]                   # lista_L_b {List[float]} -- Lista de valores de longitudes de micropilotes a evaluar [m]
        proc_iny = parametros["proc_iny"]                     # proc_iny {str} -- Proceso de inyección, puede uno de "IGU" o "IRS"
        info_barras = parametros["lista_barras"]              # lista_barras {List[Barra]} -- Lista de barras
        suelo_diametro_barra = parametros["suelo_diametro_barra"] # suelo_diametro_barra {List[Dict]} -- Tabla de utilización de barras de acuerdo al proceso de inyección, suelo y diámetro de perforación
        S_m_min = parametros["S_m_min"]
        S_m_paso = parametros["S_m_paso"]
        H_min = parametros["h_min"]                           # H_min {float} -- Altura mínima de la zapata [m]
        H_max = parametros["h_max"]                           # H_max {float} -- Altura máxima de la zapata [m]
        H_paso = parametros["h_paso"]                         # H_paso {float} -- Incremento en la altura de la zapata [m]
        D_d_min = parametros["d_d_min"]                       # D_d_min {float} -- Altura dentellón mínima de la zapata [m]
        D_d_max = parametros["d_d_max"]                       # D_d_max {float} -- Altura dentellón máxima de la zapata [m]
        D_d_paso = parametros["d_d_paso"]                     # H_paso {float} -- Incremento en la altura del dentellón de la zapata [m]
        H_relleno_min = parametros["h_relleno_min"]           # H_relleno_min {float} -- Altura mínima permitida para el relleno [m]
        α_max = parametros["alfa_max"]                        # α_max {float} -- Factor de expansión máximo
        FSCD = parametros['fsc_d']                            # FSCD {float} -- Factor de seguridad mínimo para compresión del dado
        FSC = parametros['fsc']                               # FSC {float} -- Factor de seguridad mínimo para cargas a compresión
        FSL = parametros['fsl']                               # FSL {float} -- Factor de seguridad mínimo para cargas laterales
        FST = parametros['fst']                               # FST {float} -- Factor de seguridad mínimo para cargas a tensión
        k = parametros['k']                                   # k {int} -- Número de segmentos para análisis de asentamiento
        t = parametros['t']                                   # t {int} Número de años para corrección 'Creep'
        S_max_adm_g = parametros['s_max_adm_g']               # S_max_adm {float} -- Asentamiento máximo permitido para suelos granulares [m]
        S_max_adm_c = parametros['s_max_adm_c']               # S_max_adm {float} -- Asentamiento máximo permitido para suelos cohesivos [m]
        S_max_adm_r = parametros['s_max_adm_r']               # S_max_adm {float} -- Asentamiento máximo permitido para roca [m]
        lista_HG = parametros['lista_hg']                     # lista_HGs {List[float]]} -- Lista de alturas de pedestales a evaluar por tipo de torre [m]
        D_f_max = parametros['d_f_max']                       # D_f_max {float} -- Profundida de desplante máxima [m]
        D_f_paso = parametros['d_f_paso']                     # D_f_paso {float} -- Incremento para las iteraciones de la profundidad de desplante [m]
        if usar_tabla_α_exp:
            tabla_α_exp = parametros['tabla_alfa_exp']        # tabla_α_exp {Dict} -- Diccionario para la evaluación de α_exp : Factor de expansión, con key: (tipo material, procedimiento de inyección)

        costo_excavacion = parametros['costo_excavacion']     # costo_excavacion [$/m³] -- Costo de excavación para optimización 
        costo_relleno = parametros['costo_relleno']           # costo_relleno [$/m³] -- Costo de excavación para optimización 
        costo_micropilote = parametros['costo_micropilote']   # costo_micropilote [$/m] -- Costo de micropilote para optimización 
        costo_concreto = parametros['costo_concreto']         # costo_concreto [$/m³] -- Costo de concreto del dado para optimización 
        costo_camisa = parametros["costo_camisa"]             # costo_concreto [$/m] -- Costo de la camisa para optimización

        # Crea lista de barras
        lista_barras = [Barra(b["nombre"], b["D"], b["D_int"], b["area"], b["f_y"], b["precio"], b["geoms"]) for b in info_barras]

        # θ: Ángulo del pedestal con respecto a la vertical [°]
        θ = info_cargas.get_angulo_inclinacion(torre) 
        
        # TP: Ancho mínimo del pedestal [m], calculado a partir de los parámetros geométricos del pedestal
        B_a = info_cargas.get_ancho_aleta_conector_cortante(torre)  # B_a: Ancho de la aleta del conector de cortante del stub [m]
        TP = 2 * (1.5 * B_a + d_agg + d_b_long + d_b_trans + rec)
        TP = math.ceil(TP * 10) / 10 # Aproximación a la décima por arriba

        # D_f_min: Profundidad mínima de desplante [m], calculada a partir de la proyección vertical del stub
        pvs = info_cargas.get_proyeccion_vertical_stub(torre)  # Proyección vertical del stub                               
        HG_min = min(iter(lista_HG))
        D_f_min = max(math.ceil((pvs + 0.15 - HG_min) *10) /10 , H_relleno_min)
        
        # Se revisa si se puede calcular micropilotes dadas las restricciones de profundidad mínima
        # y máxima de desplante 
        if D_f_min > D_f_max:
            mensaje_error = f"Error: D_f_min > D_f_max. Prof. mínima desplante por stub: {D_f_min}, Prof. máxima desplante: {D_f_max}."
            print(f"Error inesperado procesando: {mensaje_error}")
            if pausar_en_error:
                input("...")
            return [{"D_f": None, "D_d": None, "HG": None, "B": None, "H": None, "TP": None, "θ": None, "error": True, "mensaje_error": mensaje_error, "evaluacion": {}}]  

        # Nivel freático incluyendo inundabilidad
        NF = perfil.calcular_NF()

        # Inclinación del terreno
        ω = torre.inclinacion_terreno or 0        
        
        # Inclinación de la base de la zapata
        α = torre.inclinacion_base_zapata or 0        

        # f_carga_mp: Fracción de carga que toman los micropilotes [0..1]
        if f_carga_por_torre:
            f_carga_mp = torre.f_carga_mp
        else:
            f_carga_mp = f_carga_mp_fijo

        if f_carga_mp == None:
            mensaje_error = "No se encontró solución"
            return [{"D_f": None, "D_d": None, "E_d": None, "HG": None, "B": None, "H": None, "TP": TP, "θ": θ, "f_carga_mp": None, "proc_iny": proc_iny, 
                    "N_m": None, "L_b": None, "D_p": None, "S_m": None, "barra": None, "α": α, "ω":ω, "error": True, "mensaje_error": mensaje_error, "evaluacion": {}}]

        resultados = []
        for D_f in generar_serie(D_f_min, D_f_max, D_f_paso, 2):
            
            # Se satura todo el perfil si
            # el nivel freático esta por encima de
            # la profundidad de desplante
            if NF is not None and NF < D_f:
                perfil_ajustado = perfil.clonar_saturado()
                ajuste_saturacion_perfil = True
            else:
                perfil_ajustado = perfil
                ajuste_saturacion_perfil = False
                                    
            for N_m in lista_N_m:
                for L_b in lista_L_b:
                    if usar_tabla_α_exp:
                        tipos_mat = perfil.calcular_tipo_mat_distintos(D_f, D_f + L_b)        
                        α_exp = max([tabla_α_exp[(tipo_mat, proc_iny)] for tipo_mat in tipos_mat])                                

                    suelo_micropilote = perfil.calcular_suelo_micropilotes(D_f, D_f + L_b)
                    if suelo_micropilote == "Desconocido":
                        mensaje_error = f"Suelo desconocido para barras de micropilotes. D_f: {D_f}, L_b: {L_b}"
                        resultado = {"D_f": D_f, "D_d": None, "E_d": None, "HG": None, "B": None, "H": None, "TP": TP, "θ": θ, "f_carga_mp": f_carga_mp, "proc_iny": proc_iny, 
                                    "N_m": N_m, "L_b": None, "D_p": None, "S_m": None, "barra": None, "α": α, "ω":ω, "anclaje": None, "error": True, "mensaje_error": mensaje_error, "evaluacion": {}}
                        resultado["mensaje_error"] = mensaje_error
                        self.clasificar_resultado(resultados, resultado, n_soluciones, costo_excavacion, costo_relleno, costo_micropilote, costo_concreto, costo_camisa)
                        continue
                    
                    lista_D_p = [sdb["D_p"] for sdb in suelo_diametro_barra if sdb["suelo"] == suelo_micropilote and sdb["proc_iny"] == proc_iny]
                    for D_p in lista_D_p:
                        nombres_barras_a_probar = next(filter(lambda x: x["suelo"] == suelo_micropilote and x["D_p"] == D_p and x["proc_iny"] == proc_iny, suelo_diametro_barra))["barras"]
                        for nombre_barra in nombres_barras_a_probar:
                            barra = next(b for b in lista_barras if b.nombre == nombre_barra)

                            S_m = math.ceil(max(3 * α_max * D_p, (TP + 0.3)/(N_m / 4 ), S_m_min) * 10 ) / 10
                            B_en_rango = True
                            while B_en_rango:
                                resultados_por_hg = []
                                for HG in lista_HG:

                                    # H_min
                                    H_min_barra = next(iter([geom["h_min"] for geom in barra.geoms if geom["hg"]==HG]))
                                    H_min = max(parametros["h_min"], H_min_barra)

                                    # anclaje
                                    anclaje = next(iter([geom["anclaje"] for geom in barra.geoms if geom["hg"]==HG]))

                                    # Verifica si con el desplante 'D_f' y la altura de zapata 'H_min' se pueda lograr la altura mínima de relleno 'H_relleno_min' 
                                    if D_f - H_min < H_relleno_min:
                                        mensaje_error = f"No se puede lograr altura de relleno mínimo. D_f: {D_f}, H: {H_min}, H_relleno_min: {H_relleno_min}"
                                        resultado = {"D_f": D_f, "D_d": None, "E_d": None, "HG": HG, "B": None, "H": H_min, "TP": TP, "θ": θ, "f_carga_mp": f_carga_mp, "proc_iny": proc_iny, 
                                                    "N_m": N_m, "L_b": None, "D_p": D_p, "S_m": None, "barra": None, "α": α, "ω":ω, "anclaje": anclaje, "error": True, "mensaje_error": mensaje_error, "evaluacion": {}}
                                        resultados_por_hg.append(resultado)
                                        D_s = D_p * α_exp
                                        dist_bor =  max(1.5 * D_s, 0.25)
                                        N_mL = N_m / 4 + 1
                                        B = 2 * dist_bor + (N_mL - 1) * S_m * math.sqrt(1 + tan_g(θ)**2) + 2 * anclaje * tan_g(θ)
                                        if B > b_max:
                                            B_en_rango = False
                                            break
                                        continue            

                                    resultado = {"D_f": D_f, "D_d": 0.0, "E_d": 0.0, "HG": HG, "H": H_min, "TP": TP, "θ": θ, "f_carga_mp": f_carga_mp, "proc_iny": proc_iny, 
                                    "N_m": N_m, "L_b": L_b - anclaje, "D_p": D_p, "D_s": None, "S_m": S_m, "barra": vars(barra), "α": α, "ω":ω, "error": False, "mensaje_error": None, "evaluacion": {}}         
                                    try:
                                        micropilotes = Micropilotes(D_f, 0.0, HG, H_min, TP, θ, γ_c, N_m, S_m, L_b - anclaje, barra, D_p, η, proc_iny, f_pc, f_py, A_camisa, d_b_long, perfil_ajustado, α, ω, f_carga_mp, α_exp, γ_l)
                                        if micropilotes.B > b_max:
                                            B_en_rango = False
                                            break
                                        resultado["evaluacion"] = self.evaluador.evaluar(micropilotes, torre, perfil, info_cargas, H_min, H_max, H_paso, D_d_min, D_d_max, D_d_paso, H_relleno_min, FSC, FSCD, FST, k, t, S_max_adm_c, S_max_adm_g, S_max_adm_r, rec, FSL)
                                        resultado["B"] = micropilotes.B
                                        resultado["E_d"] = micropilotes.E_d 
                                        resultado["D_s"] = micropilotes.D_s 
                                        resultado["x"] = micropilotes.x 
                                        resultado["dist_bor"] = micropilotes.dist_bor
                                        resultado["volumen_concreto"] = micropilotes.volumen_dado
                                        resultado["volumen_relleno"] = micropilotes.volumen_relleno()
                                        resultado["peso_dado"] = micropilotes.peso_dado()
                                        resultado["peso_micropilotes"] = micropilotes.peso_micropilotes()
                                        resultado["relleno"] = perfil.calcular_material_relleno(micropilotes.D_f - micropilotes.H)
                                        resultado["H"] = micropilotes.H
                                        resultado["D_d"] = micropilotes.D_d
                                        resultado["ajuste_saturacion_perfil"] = ajuste_saturacion_perfil
                                        resultado["suelo_micropilote"] = suelo_micropilote
                                        resultado["anclaje"] = anclaje
                                        resultado["L_c"] = micropilotes.L_c
                                        resultados_por_hg.append(resultado)    

                                    except Exception  as e:
                                        resultado["error"] = True
                                        resultado["mensaje_error"] = str(e)
                                        resultados_por_hg.append(resultado)    
                                        if pausar_en_error:
                                            print(f"Error inesperado procesando: Torre:{torre.nombre}, D_f: {D_f}, Error: {str(e)}")
                                            traceback.print_exc(file=sys.stdout)
                                            input("...")

                                if B_en_rango:
                                    # El optimizador encuentra los micropilotes óptimos que funcione para todos
                                    # los pedestales. Requiere entonces sintetizar todos los resultados por pedestal
                                    # en uno solo, que sirva para comparar en la selección del óptimo
                                    resultado_grupo = self.integrar_resultados(resultados_por_hg, H_min)

                                    # Clasificación del resultado en busca de las mejores soluciones
                                    self.clasificar_resultado(resultados, resultado_grupo, n_soluciones, costo_excavacion, costo_relleno, costo_micropilote, costo_concreto, costo_camisa)                                                                                                                 

                                S_m += S_m_paso

        return resultados

    def integrar_resultados(self, resultados_por_hg, H_min):
        resultado_grupo = {}
        resultado_grupo["D_f"] = resultados_por_hg[0]["D_f"]
        resultado_grupo["HG"] = [r["HG"] for r in resultados_por_hg]
        resultado_grupo["TP"] = resultados_por_hg[0]["TP"]
        resultado_grupo["θ"] = resultados_por_hg[0]["θ"]
        resultado_grupo["f_carga_mp"] = resultados_por_hg[0]["f_carga_mp"]
        resultado_grupo["proc_iny"] = resultados_por_hg[0]["proc_iny"]
        resultado_grupo["N_m"] = resultados_por_hg[0]["N_m"]
        resultado_grupo["L_b"] = min([r["L_b"] or 0 for r in resultados_por_hg])
        resultado_grupo["D_p"] = resultados_por_hg[0]["D_p"]
        resultado_grupo["S_m"] = resultados_por_hg[0]["S_m"]
        resultado_grupo["barra"] = resultados_por_hg[0]["barra"]
        resultado_grupo["α"] = resultados_por_hg[0]["α"]
        resultado_grupo["ω"] = resultados_por_hg[0]["ω"]        
        resultado_grupo["error"] = any([r["error"] for r in resultados_por_hg])
        if resultado_grupo["error"]:
            resultado_grupo["mensaje_error"] = ". ".join(set([r["mensaje_error"] for r in resultados_por_hg if r["error"]]))
            resultado_grupo["evaluacion"] = {}
            resultado_grupo["D_d"] = None
            resultado_grupo["E_d"] = None
            resultado_grupo["D_s"] = None
            resultado_grupo["x"] = None
            resultado_grupo["B"] = None
            resultado_grupo["H"] = None
            resultado_grupo["dist_bor"] = None
            resultado_grupo["L_c"] = None
            resultado_grupo["ajuste_saturacion_perfil"] = None
            resultado_grupo["volumen_concreto"] = None
            resultado_grupo["volumen_relleno"] = None
            resultado_grupo["relleno"] = None
        else:
            resultado_grupo["mensaje_error"] = None
            resultado_grupo["evaluacion"] = {}
            keys_verif = resultados_por_hg[0]["evaluacion"].keys()
            for key in keys_verif:
                resultado_grupo["evaluacion"][key] = max([r["evaluacion"][key] for r in resultados_por_hg], key = lambda x : x["desviacion"] if x["desviacion"] else float("-inf"))
            resultado_grupo["E_d"] = resultados_por_hg[0]["E_d"]
            resultado_grupo["D_s"] = resultados_por_hg[0]["D_s"]
            resultado_grupo["x"] = resultados_por_hg[0]["x"]
            resultado_grupo["B"] = resultados_por_hg[0]["B"]
            resultado_grupo["D_d"] = max([r["D_d"] for r in resultados_por_hg])
            if resultado_grupo["D_d"] > 0:
                resultado_grupo["H"] = H_min
            else:
                resultado_grupo["H"] = max([r["H"] for r in resultados_por_hg])
            resultado_grupo["dist_bor"] = resultados_por_hg[0]["dist_bor"]
            resultado_grupo["L_c"] = max([r["L_c"] for r in resultados_por_hg])
            resultado_grupo["ajuste_saturacion_perfil"] = resultados_por_hg[0]["ajuste_saturacion_perfil"]
            resultado_grupo["suelo_micropilote"] = resultados_por_hg[0]["suelo_micropilote"]
            resultado_grupo["volumen_concreto"] =  max([r["volumen_concreto"] for r in resultados_por_hg])
            resultado_grupo["peso_dado"] = max([r["peso_dado"] for r in resultados_por_hg])
            resultado_grupo["peso_micropilotes"] = resultados_por_hg[0]["peso_micropilotes"]
            resultado_grupo["volumen_relleno"] = resultados_por_hg[0]["volumen_relleno"]
            resultado_grupo["relleno"] = resultados_por_hg[0]["relleno"]
            resultado_grupo["anclaje"] = max([r["anclaje"] for r in resultados_por_hg])

        return resultado_grupo

    # def clasificar_resultado(self, resultados: List, resultado: List, n_soluciones: int):
    #     mala_calificacion = (999999, 999999)

    #     if resultado["error"]:
    #         resultado["cumple"] = False
    #         resultado["calificacion"] = mala_calificacion
    #     else:
    #         evaluacion = resultado["evaluacion"]
    #         resultado["cumple"] = all([evaluacion[key]["cumple"] for key in evaluacion])
    #         incumplimientos = sum([1  for key in evaluacion if not evaluacion[key]["cumple"]])
    #         if incumplimientos == 0:
    #             N_m = resultado["N_m"]
    #             L_b = resultado["L_b"]
    #             anclaje = resultado["anclaje"]
    #             precio = resultado["barra"]["precio"]
    #             D_f = resultado["D_f"]
    #             D_p = resultado["D_p"]
    #             volumen_concreto = resultado["volumen_concreto"]
    #             resultado["calificacion"] = (incumplimientos, N_m * (L_b + anclaje) * precio, volumen_concreto, D_f, precio, D_p )
    #         else:
    #             sum_desviaciones_fs =  math.sqrt(sum([evaluacion[key]["desviacion"]**2 for key in evaluacion if not evaluacion[key]["cumple"]]))
    #             resultado["calificacion"] = (incumplimientos, sum_desviaciones_fs)
        
    #     if len(resultados) < n_soluciones:
    #         resultados.append(resultado)
    #         resultados.sort(key = lambda r: r["calificacion"])
    #     elif resultado["calificacion"] <  resultados[-1]["calificacion"]:
    #         resultados[-1] = resultado
    #         resultados.sort(key = lambda r: r["calificacion"])

    def clasificar_resultado(self, resultados: List, resultado: List, n_soluciones: int, costo_excavacion: float, costo_relleno: float, costo_micropilote:float, costo_concreto: float, costo_camisa: float):
        mala_calificacion = (99999999999, 99999999999)

        if resultado["error"]:
            resultado["cumple"] = False
            resultado["calificacion"] = mala_calificacion
        else:
            evaluacion = resultado["evaluacion"]
            resultado["cumple"] = all([evaluacion[key]["cumple"] for key in evaluacion])
            incumplimientos = sum([1  for key in evaluacion if not evaluacion[key]["cumple"]])
            if incumplimientos == 0:
                N_m = resultado["N_m"]
                L_b = resultado["L_b"]
                anclaje = resultado["anclaje"]
                precio = resultado["barra"]["precio"]
                volumen_concreto = resultado["volumen_concreto"]
                B = resultado["B"]
                D_f = resultado["D_f"]
                D_p = resultado["D_p"]
                volumen_concreto = resultado["volumen_concreto"]
                volumen_relleno = resultado["volumen_relleno"]
                L_c = resultado["L_c"]
                resultado["calificacion"] = (incumplimientos, 
                    B, 
                    (B * B * D_f) * costo_excavacion + 
                    volumen_relleno * costo_relleno +
                    volumen_concreto * costo_concreto + 
                    N_m * (L_b + anclaje) * costo_micropilote +
                    N_m * L_c * costo_camisa,
                    D_f, 
                    D_p )
                # resultado["calificacion"] = (incumplimientos, 
                #                             (B * B * D_f) * costo_excavacion + 
                #                             volumen_relleno * costo_relleno +
                #                             volumen_concreto * costo_concreto + 
                #                             N_m * (L_b + anclaje) * costo_micropilote,
                #                             volumen_concreto, D_f, precio, D_p )
            else:
                sum_desviaciones_fs =  math.sqrt(sum([evaluacion[key]["desviacion"]**2 for key in evaluacion if not evaluacion[key]["cumple"]]))
                resultado["calificacion"] = (incumplimientos, sum_desviaciones_fs)        
        if len(resultados) < n_soluciones:
            resultados.append(resultado)
            resultados.sort(key = lambda r: r["calificacion"])
        elif resultado["calificacion"] <  resultados[-1]["calificacion"]:
            resultados[-1] = resultado
            resultados.sort(key = lambda r: r["calificacion"])    