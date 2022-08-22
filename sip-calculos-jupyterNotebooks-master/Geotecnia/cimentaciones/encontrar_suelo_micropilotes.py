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
from .util import γ_agua, generar_serie
from .evaluador_micropilotes2 import EvaluadorMicropilotes2

DBFila = Dict[str, Any]

class EncontrarSuelo():

    def __init__(self, evaluador: EvaluadorMicropilotes2):
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
        η = parametros["eta"]                                 # η {float} -- Eficiencia del grupo de micropilotes [-]
        f_pc = parametros["f_pc"]                             # f_pc {float} -- Resistencia a la compresión del concreto [kPa]
        f_py = parametros["f_py"]                             # f_py {float} -- Esfuerzo de fluencia de la barra de refuerzo [kPa]
        A_camisa = parametros["a_camisa"]                     # A_camisa {float} -- Área de la sección de la camisa [m²]
        lista_N_m = parametros["lista_N_m"]                   # lista_N_m {List[float]} -- Lista de valores posibles para el número de micropilotes
        lista_L_b = parametros["lista_L_b"]                   # lista_L_b {List[float]} -- Lista de valores de longitudes de micropilotes a evaluar [m]
        P_anc = parametros["P_anc"]                           # P_anc {float} -- Profundidad de anclaje del micropilote al dado [m]
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
        D_f_min = math.ceil((pvs + 0.15 - HG_min) *10) /10
        
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
            
            # Verifica si con el desplante 'D_f' y la altura de zapata 'H_min' se pueda lograr la altura mínima de relleno 'H_relleno_min' 
            if D_f - H_min < H_relleno_min:
                mensaje_error = f"No se puede lograr altura de relleno mínimo. D_f: {D_f}, H: {H_min}, H_relleno_min: {H_relleno_min}"
                resultado = {"D_f": D_f, "D_d": None, "E_d": None, "HG": None, "B": None, "H": None, "TP": TP, "θ": θ, "f_carga_mp": f_carga_mp, "proc_iny": proc_iny, 
                            "N_m": None, "L_b": None, "D_p": None, "S_m": None, "barra": None, "α": α, "ω":ω, "error": True, "mensaje_error": mensaje_error, "evaluacion": {}}
                continue 
            
            # Se satura todo el perfil si
            # el nivel freático esta por encima de
            # la profundidad de desplante
            if NF and NF < D_f:
                perfil_ajustado = perfil.clonar_saturado()
                γ_c_ajustado = γ_c - γ_agua
                ajuste_saturacion_perfil = True
            else:
                perfil_ajustado = perfil
                γ_c_ajustado = γ_c
                ajuste_saturacion_perfil = False
                                    
            for N_m in lista_N_m:
                for L_b in lista_L_b:
                    # α_exp: Factor de expansión [-]
                    if usar_tabla_α_exp:
                        tipos_mat = perfil.calcular_tipo_mat_distintos(D_f, D_f + L_b)        
                        α_exp = max([tabla_α_exp[(tipo_mat, proc_iny)] for tipo_mat in tipos_mat])                                

                    suelo_micropilote = perfil.calcular_suelo_micropilotes(D_f, D_f + L_b)
                    resultados.append({"D_f":D_f, "N_m":N_m, "L_b":L_b, "suelo_micropilote":suelo_micropilote})
                    
        return resultados

