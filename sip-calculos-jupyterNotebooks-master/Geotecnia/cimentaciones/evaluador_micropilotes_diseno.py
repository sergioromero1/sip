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
from .util import γ_agua, generar_serie, tan_g
from .evaluador_micropilotes import EvaluadorMicropilotes

DBFila = Dict[str, Any]

class EvaluadorMicropilotesDiseno():

    def __init__(self, evaluador: EvaluadorMicropilotes):
        self.evaluador = evaluador

    def evaluar(self, grupo, parametros: DBFila, torre: Torre, perfil: Perfil, info_cargas: Cargas, usar_tabla_α_exp: bool = True, α_exp: float = None, pausar_en_error: bool = True, usar_geom_grupo:bool=False, lista_HG=None) -> Dict[Tuple[float,float], Dict[str, Tuple[float,float,bool]]]:

        #
        # Información de Parámetros
        #
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
        info_barras = parametros["lista_barras"]              # lista_barras {List[Barra]} -- Lista de barras
        H_min = parametros["h_min"]                           # H_min {float} -- Altura mínima de la zapata [m]
        H_max = parametros["h_max"]                           # H_max {float} -- Altura máxima de la zapata [m]
        H_paso = parametros["h_paso"]                         # H_paso {float} -- Incremento en la altura de la zapata [m]
        D_d_min = parametros["d_d_min"]                       # D_d_min {float} -- Altura dentellón mínima de la zapata [m]
        D_d_max = parametros["d_d_max"]                       # D_d_max {float} -- Altura dentellón máxima de la zapata [m]
        D_d_paso = parametros["d_d_paso"]                     # H_paso {float} -- Incremento en la altura del dentellón de la zapata [m]
        H_relleno_min = parametros["h_relleno_min"]           # H_relleno_min {float} -- Altura mínima permitida para el relleno [m]
        FSCD = parametros['fsc_d']                            # FSCD {float} -- Factor de seguridad mínimo para compresión del dado
        FSC = parametros['fsc']                               # FSC {float} -- Factor de seguridad mínimo para cargas a compresión
        FSL = parametros['fsl']                               # FSL {float} -- Factor de seguridad mínimo para cargas laterales
        FST = parametros['fst']                               # FST {float} -- Factor de seguridad mínimo para cargas a tensión
        k = parametros['k']                                   # k {int} -- Número de segmentos para análisis de asentamiento
        t = parametros['t']                                   # t {int} Número de años para corrección 'Creep'
        S_max_adm_g = parametros['s_max_adm_g']               # S_max_adm {float} -- Asentamiento máximo permitido para suelos granulares [m]
        S_max_adm_c = parametros['s_max_adm_c']               # S_max_adm {float} -- Asentamiento máximo permitido para suelos cohesivos [m]
        S_max_adm_r = parametros['s_max_adm_r']               # S_max_adm {float} -- Asentamiento máximo permitido para roca [m]
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

        hs_grupo = None
        tps_grupo = None
        anc_grupo = None

        if usar_geom_grupo:
            hs_grupo = (grupo["hs_grupos"])
            tps_grupo = (grupo["tps_grupos"])
            anc_grupo = (grupo["anc_grupos"])
        else:
            # TP: Ancho mínimo del pedestal [m], calculado a partir de los parámetros geométricos del pedestal
            B_a = info_cargas.get_ancho_aleta_conector_cortante(torre)  # B_a: Ancho de la aleta del conector de cortante del stub [m]
            TP = 2 * (1.5 * B_a + d_agg + d_b_long + d_b_trans + rec)
            TP = math.ceil(TP * 10) / 10 # Aproximación a la décima por arriba

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

        proc_iny = grupo["proc_iny"]

        if f_carga_mp == None:
            mensaje_error = "No se encontró solución"
            return [{"D_f": None, "D_d": None, "E_d": None, "HG": None, "B": None, "H": None, "TP": TP, "θ": θ, "f_carga_mp": None, "proc_iny": proc_iny, 
                    "N_m": None, "L_b": None, "D_p": None, "S_m": None, "barra": None, "α": α, "ω":ω, "error": True, "mensaje_error": mensaje_error, "evaluacion": {}}]

        D_f = float(grupo["d_f"])
            
        # Se satura todo el perfil si
        # el nivel freático esta por encima de
        # la profundidad de desplante
        if NF is not None and NF < D_f:
            perfil_ajustado = perfil.clonar_saturado()
            ajuste_saturacion_perfil = True
        else:
            perfil_ajustado = perfil
            ajuste_saturacion_perfil = False

        N_m = int(grupo["n_m"])
        L_b = float(grupo["l_b"])      

        # α_exp: Factor de expansión [-]
        if usar_tabla_α_exp:
            tipos_mat = perfil.calcular_tipo_mat_distintos(D_f, D_f + L_b)        
            α_exp = max([tabla_α_exp[(tipo_mat, proc_iny)] for tipo_mat in tipos_mat])

        suelo_micropilote = perfil.calcular_suelo_micropilotes(D_f, D_f + L_b)
        D_p = float(grupo["d_p"])
        nombre_barra = grupo["nombre_barra"]
        barra = next(b for b in lista_barras if b.nombre == nombre_barra)
        

        resultados_por_hg = []
        for HG in lista_HG:
            # anclaje
            anclaje_segun_barra = next(iter([geom["anclaje"] for geom in barra.geoms if geom["hg"]==HG]))

            # Recupera la longitud nominal
            L_b = float(grupo["l_b"]) + anclaje_segun_barra
            
            if usar_geom_grupo:
                H = hs_grupo[str(HG)]
                H_min = H
                H_max = H
                TP = tps_grupo[str(HG)]
                anclaje = anc_grupo[str(HG)]
            else:
                H = H_min
                anclaje = anclaje_segun_barra

            B = float(grupo["b"])
            S_m = float(grupo["s_m"])

            resultado = {"D_f": D_f, "D_d": 0.0, "E_d": 0.0, "HG": HG, "H": H, "TP": TP, "θ": θ, "f_carga_mp": f_carga_mp, "proc_iny": proc_iny, 
            "N_m": N_m, "L_b": L_b - anclaje, "D_p": D_p, "D_s": None, "S_m": S_m, "barra": vars(barra), "α": α, "ω":ω, "error": False, "mensaje_error": None, "evaluacion": {}}         
            try:
                micropilotes = Micropilotes(D_f, 0.0, HG, H, TP, θ, γ_c, N_m, S_m, L_b - anclaje, barra, D_p, η, proc_iny, f_pc, f_py, A_camisa, d_b_long, perfil_ajustado, α, ω, f_carga_mp, α_exp, γ_l)
                # Se pone H_max = H para que el evaluador no modifique el H suministrado en la evaluación
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
        resultados = []
        self.clasificar_resultado(resultados, self.integrar_resultados(resultados_por_hg, H_min), 1, costo_excavacion, costo_relleno, costo_micropilote, costo_concreto, costo_camisa)
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
        resultado_grupo["L_b"] = resultados_por_hg[0]["L_b"]
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

    def clasificar_resultado(self, resultados: List, resultado: List, n_soluciones: int, costo_excavacion: float, costo_relleno: float, costo_micropilote:float, costo_concreto: float, costo_camisa: float):
        mala_calificacion = (999999, 999999)

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
            else:
                sum_desviaciones_fs =  math.sqrt(sum([evaluacion[key]["desviacion"]**2 for key in evaluacion if not evaluacion[key]["cumple"]]))
                resultado["calificacion"] = (incumplimientos, sum_desviaciones_fs)
        
        if len(resultados) < n_soluciones:
            resultados.append(resultado)
            resultados.sort(key = lambda r: r["calificacion"])
        elif resultado["calificacion"] <  resultados[-1]["calificacion"]:
            resultados[-1] = resultado
            resultados.sort(key = lambda r: r["calificacion"])