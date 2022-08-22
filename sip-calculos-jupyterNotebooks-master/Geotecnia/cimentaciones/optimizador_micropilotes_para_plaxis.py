import math
import json
import sys, traceback
from typing import List, Dict, Tuple, Any
from .micropilotes import Micropilotes
from .perfil import Perfil
from .barra import Barra
from .cargas import Cargas
from .util import γ_agua, generar_serie
from .evaluador_micropilotes import EvaluadorMicropilotes

DBFila = Dict[str, Any]

class OptimizadorMicropilotesParaPlaxis():

    def __init__(self, evaluador: EvaluadorMicropilotes):
        self.evaluador = evaluador

    def optimizar(self, parametros: DBFila, torre: DBFila, f_carga_mp: float, perfil: Perfil, info_cargas: Cargas, HG, usar_tabla_α_exp: bool = True, α_exp: float = None, pausar_en_error: bool = True) -> Dict[Tuple[float,float], Dict[str, Tuple[float,float,bool]]]:
        #
        # Información de Parámetros
        #
        n_soluciones = parametros['n_soluciones']             # n_soluciones {int} -- Número de soluciones a conservar para reportes
        b_max = parametros['b_max']                           # b_max {float} -- Distancia máxima del lado de zapata [m]
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
        D_f_max = parametros['d_f_max']                       # D_f_max {float} -- Profundida de desplante máxima [m]
        D_f_paso = parametros['d_f_paso']                     # D_f_paso {float} -- Profundida de desplante máxima [m]
        if usar_tabla_α_exp:
            tabla_α_exp = parametros['tabla_alfa_exp']        # tabla_α_exp {Dict} -- Diccionario para la evaluación de α_exp : Factor de expansión, con key: (tipo material, procedimiento de inyección)

        # Crea lista de barras
        lista_barras = [Barra(b["nombre"], b["D"], b["D_int"], b["area"], b["f_y"], b["precio"], b["geoms"]) for b in info_barras]

        #
        # Información de estructura y cargas
        #
        B_a = info_cargas.get_ancho_aleta_conector_cortante(torre)  # B_a: Ancho de la aleta del conector de cortante del stub [m]
        θ = info_cargas.get_angulo_inclinacion(torre) # Ángulo del pedestal con respecto a la vertical [°]
        
        # TP_stub: Ancho mínimo del pedestal [m]
        TP = 2 * (1.5 * B_a + d_agg + d_b_long + d_b_trans + rec)
        TP = math.ceil(TP * 10) / 10 # Aproximación a la décima por arriba

        pvs = info_cargas.get_proyeccion_vertical_stub(torre)                                    
        resultados = []
        print("\tHG: {}".format(HG), flush=True)
        
        D_f_min = math.ceil((pvs + 0.15 - HG) *10) /10

        if D_f_min <= D_f_max:

            for D_f in generar_serie(D_f_min, D_f_max, D_f_paso, 2):
                
                NF = perfil.calcular_NF()
                if NF is not None and NF < D_f:
                    perfil_ajustado = perfil.clonar_saturado()
                else:
                    perfil_ajustado = perfil
                for N_m in lista_N_m:
                    for L_b in lista_L_b:
                        # α_exp: Factor de expansión [-]
                        if usar_tabla_α_exp:
                            tipos_mat = perfil.calcular_tipo_mat_distintos(D_f, D_f + L_b)        
                            α_exp = max([tabla_α_exp[(tipo_mat, proc_iny)] for tipo_mat in tipos_mat])

                        suelo_micropilote = perfil.calcular_suelo_micropilotes(D_f, D_f + L_b)
                        if suelo_micropilote == "Desconocido":
                            resultado = {"D_f": D_f, "HG": HG, "f_carga_mp": f_carga_mp, "TP": TP, "proc_iny": proc_iny}
                            mensaje_error = f"Suelo desconocido para barras de micropilotes. D_f: {D_f}, L_b: {L_b}"
                            resultado["error"] = True
                            resultado["mensaje_error"] = mensaje_error
                            self.clasificar_resultado(resultados, resultado, n_soluciones)
                            continue

                        lista_D_p = [sdb["D_p"] for sdb in suelo_diametro_barra if sdb["suelo"] == suelo_micropilote and sdb["proc_iny"] == proc_iny]
                        for D_p in lista_D_p:
                            nombres_barras_a_probar = next(filter(lambda x: x["suelo"] == suelo_micropilote and x["D_p"] == D_p and x["proc_iny"] == proc_iny, suelo_diametro_barra))["barras"]
                            for nombre_barra in nombres_barras_a_probar:
                                barra = next(b for b in lista_barras if b.nombre == nombre_barra)

                                # H_min
                                H_min_barra = next(iter([geom["h_min"] for geom in barra.geoms if geom["hg"]==HG]))
                                H_min = max(parametros["h_min"], H_min_barra)

                                # anclaje
                                anclaje = next(iter([geom["anclaje"] for geom in barra.geoms if geom["hg"]==HG]))

                                # Verifica si con el desplante 'D_f' y la altura de zapata 'H_min' se pueda lograr la altura mínima de relleno 'H_relleno_min' 
                                if D_f - H_min < H_relleno_min:
                                    continue 
                                S_m = math.ceil(max(3 * α_max * D_p, (TP + 0.3)/(N_m / 4 ), S_m_min) * 10 ) / 10            
                                while True: # Loop para probar todos los S_m que cumplan con B <= b_max
                                    resultado = {"D_f": D_f, "D_d": 0.0, "E_d": 0.0, "HG": HG, "H": H_min, "TP": TP, "θ": θ, "f_carga_mp": f_carga_mp, "proc_iny": proc_iny, 
                                    "N_m": N_m, "L_b": L_b, "D_p": D_p, "D_s": None, "S_m": S_m, "barra": vars(barra), "α": 0, "ω":0, "error": False, "mensaje_error": None, "evaluacion": {}}                                      
                                    try:
                                        micropilotes = Micropilotes(D_f, 0.0, HG, H_min, TP, θ, γ_c, N_m, S_m, L_b - anclaje, barra, D_p, η, proc_iny, f_pc, f_py, A_camisa, d_b_long, perfil_ajustado, 0, 0, f_carga_mp, α_exp, γ_l)
                                        if round(micropilotes.B,2) > b_max:
                                            break
                                        resultado["evaluacion"] = self.evaluador.evaluar(micropilotes, torre, perfil, info_cargas, H_min, H_max, H_paso, D_d_min, D_d_max, D_d_paso, H_relleno_min, FSC, FSCD, FST, k, t, S_max_adm_c, S_max_adm_g, S_max_adm_r, rec, FSL)
                                        resultado["B"] = micropilotes.B
                                        resultado["H"] = micropilotes.H
                                        resultado["D_d"] = micropilotes.D_d
                                        resultado["E_d"] = micropilotes.E_d 
                                        resultado["D_s"] = micropilotes.D_s 
                                        resultado["dist_bor"] = micropilotes.dist_bor
                                        resultado["volumen_concreto"] = micropilotes.volumen_dado
                                        resultado["relleno"] = perfil.calcular_material_relleno(micropilotes.D_f - micropilotes.H)
                                        resultado["anclaje"] = anclaje
                                        self.clasificar_resultado(resultados, resultado, n_soluciones)
                                    except Exception  as e:
                                        resultado["B"] = micropilotes.B
                                        resultado["H"] = micropilotes.H
                                        resultado["error"] = True
                                        resultado["mensaje_error"] = str(e)
                                        #print(f"Error inesperado procesando: Torre:{torre.nombre}, Error:{str(e)}")
                                        self.clasificar_resultado(resultados, resultado, n_soluciones)
                                        #traceback.print_exc(file=sys.stdout)
                                        if pausar_en_error:
                                            input("...")
                                    S_m += S_m_paso
        else:
            resultado = {"HG": HG, "f_carga_mp": f_carga_mp, "TP": TP, "proc_iny": proc_iny}
            resultado["error"] = True
            resultado["mensaje_error"] = "No cumple dimensiones para el stub: D_f_min ({}) > D_f_max ({})".format(D_f_min, D_f_max)
            resultados.append(resultado)
            print("\t\tNo encontró soluciones para el pedestal", flush=True)
            print("\t\t\tNo cumple dimensiones para el stub")
        return resultados

    # def clasificar_resultado(self, resultados: List, resultado: Dict, n_soluciones: int):

    #     verificaciones = ["deslizamiento-long_max", 
    #                     "deslizamiento-tran_max",
    #                     "mp-adh-mp-suelo-comp_max_m",
    #                     "mp-adh-mp-suelo-lat_max_m",
    #                     "mp-adh-mp-suelo-tens_max_m",
    #                     "mp-tension-tens_max_m_d",
    #                     "mp-compresion-comp_max_m_d",
    #                     "mp-compresion-lat_max_m_d",
    #                     "mp-adh-barra-grouting-comp_max_m",
    #                     "mp-adh-barra-grouting-lat_max_m",
    #                     "mp-adh-barra-grouting-tens_max_m",        
    #                     "compresion_dado-comp_max_m",
    #                     "compresion_micropilotes-comp_max_m",
    #                     "asentamientos-comp_max",
    #                     "arrancamiento-tens_max_m"]
    #     resultado["cumple"] = all([resultado[verificacion]["cumple"] for verificacion in verificaciones])
    #     incumplimientos = sum([1  for verificacion in verificaciones if not resultado[verificacion]["cumple"]])
    #     if incumplimientos == 0:
    #         N_m = resultado["N_m"]
    #         L_b = resultado["L_b"]
    #         precio = resultado["barra"]["precio"]
    #         D_f = resultado["D_f"]
    #         volumen_concreto = resultado["volumen_concreto"]
    #         calificacion = (incumplimientos, N_m * L_b * precio, volumen_concreto, D_f )
    #     else:
    #         sum_desviaciones_fs =  math.sqrt(sum([resultado[verificacion]["desviacion"]**2 for verificacion in verificaciones if not resultado[verificacion]["cumple"]]))
    #         calificacion = (incumplimientos, sum_desviaciones_fs)

    #     resultado["calificacion"] = calificacion

    #     if len(resultados) < n_soluciones:
    #         resultados.append(resultado)
    #         resultados.sort(key = lambda r: r["calificacion"])
    #     elif resultado["calificacion"] <  resultados[-1]["calificacion"]:
    #         resultados[-1] = resultado
    #         resultados.sort(key = lambda r: r["calificacion"])

    def clasificar_resultado(self, resultados: List, resultado: List, n_soluciones: int):
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
                D_f = resultado["D_f"]
                volumen_concreto = resultado["volumen_concreto"]                
                resultado["calificacion"] = (incumplimientos, N_m * (L_b + anclaje) * precio, volumen_concreto, D_f, precio )
            else:
                sum_desviaciones_fs =  math.sqrt(sum([evaluacion[key]["desviacion"]**2 for key in evaluacion if not evaluacion[key]["cumple"]]))
                resultado["calificacion"] = (incumplimientos, sum_desviaciones_fs)
        
        if len(resultados) < n_soluciones:
            resultados.append(resultado)
            resultados.sort(key = lambda r: r["calificacion"])
        elif resultado["calificacion"] <  resultados[-1]["calificacion"]:
            resultados[-1] = resultado
            resultados.sort(key = lambda r: r["calificacion"])            

