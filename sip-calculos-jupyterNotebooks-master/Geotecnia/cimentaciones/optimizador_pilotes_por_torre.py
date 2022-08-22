import math
import json
import logging
import sys, traceback
from typing import List, Dict, Tuple, Any
from .pilotes import Pilotes
from .perfil import Perfil
from .torre import Torre
from .cargas import Cargas
from .util import γ_agua, generar_serie, tan_g
from .evaluador_pilotes import EvaluadorPilotes

DBFila = Dict[str, Any]

class OptimizadorPilotesPorTorre():

    def __init__(self, evaluador: EvaluadorPilotes):
        self.evaluador = evaluador

    def optimizar(self, parametros: DBFila, torre:Torre, perfil: Perfil, info_cargas:Cargas, pausar_en_error:bool = True):

        #
        # Información de Parámetros
        #

        D_f_max = parametros['d_f_max']                         # b_max {float} -- Profundida de desplante máxima [m]
        D_f_paso = parametros['d_f_paso']                       # d_f_paso {float} -- Incremento para las iteraciones de profundidad de desplante [m]
        # b_max = parametros['b_max']                             # b_max {float} -- Distancia máxima del lado de zapata [m]
        n_soluciones = parametros['n_soluciones']               # n_soluciones {int} -- Número de soluciones a conservar para reportes
        d_agg = parametros['d_agg']                             # d_agg {float} -- Tamaño máximo nominal del agregado grueso [m]
        d_b_long = parametros['d_b_long']                       # d_b_long {float} -- Diámetro de barras de refuerzo longitudinal [m]
        d_b_trans = parametros['d_b_trans']                     # d_b_trans {float} -- Diámetro de barras de refuerzo transversal [m]
        rec = parametros['rec']                                 # rec {float} -- Espesor del recubrimiento [m]
        γ_c = parametros['gamma_c']                             # γ_c {float} -- Peso unitario de la cimentación [kN/m³]
        lista_n = parametros["lista_n"]                         # lista_n {List[float]} -- Lista de valores posibles para el número de pilotes
        lista_H = parametros["lista_H"]                         # lista_H {List[float]} -- Lista de valores de longitudes de pilotes a evaluar [m]
        factor_S_p = parametros["factor_s_p"]                   # factor_S_p {float} -- Factor de separación de los pilotes respecto a su diámetro [-]
        h_c = parametros['h_c']                                 # h_c {float} -- altura de campana [m]
        h_con = parametros['h_con']                             # h_con {float} -- Altura de la sección conica de la campana[m]
        θ_c = parametros['θ_c']                                 #θ_c {float} --  Ángulo de la campana [°]
        d_bor = parametros['d_bor']                             #d_bor {float -- Distancia del pilote al borde del dado [m]
        f_carga_por_torre =parametros['f_carga_por_torre']      # f_carga_por_torre {bool} -- Indica si la fracción de carga que toma el mp se toma por cada torre
        f_carga_p_fijo = parametros['f_carga_p_fijo']                #f_carga_p_fijo {float} -- Fracción de carga que toman los pilotes [-]
        hincado = parametros['hincado']                         #hincado {bool} -- Boleano que define condicion del pilote hincado o preexcavado
        campana = parametros['campana']                         #campana{bool} -- Boleano que define condicion del pilote con o sin campana
        k = parametros['k']                                     # k {int} -- Número de segmentos para análisis de asentamiento       
        t = parametros['t']                                     # t {int} --  Número de años para corrección 'Creep'
        s_max_adm_g = parametros['s_max_adm_g']                 # s_max_adm_g {float} -- Asentamiento máximo permitido suelos granulares [m]
        s_max_adm_c = parametros['s_max_adm_c']                 # s_max_adm_c {float} -- Asentamiento máximo permitido suelos cohesivos [m]
        s_max_adm_r = parametros['s_max_adm_r']                 # s_max_adm_r {float} -- Asentamiento máximo permitido roca [m]
        lista_HG = parametros['lista_hg']                       # lista_HG {List[float]} -- Lista de altura de pedestales a evaluar [m]
        #hg_por_pata = parametros['hg_por_pata']                 # Indica si aparte de la lista de hgs a evaluar, se debe incluir el hg de cada pata
        # D_p_min = parametros['D_p_min']                         # D_p_min {float} -- Valor mínimo para las iteraciones de diametro de los pilotes D_p [m]
        # D_p_max =  parametros['D_p_max']                        # D_p_max {float} -- Valor máximo para las iteraciones de diametro de los pilotes D_p [m]
        # D_p_paso = parametros['D_p_paso']                       # D_p_paso {float} -- Incremento para las iteraciones de diametro de los pilotes D_p [m]
        rec_fondo_stub = parametros['rec_fondo_stub']           # rec_fondo_stub {float} -- Recubrimiento vertical en el fondo de los pilotes para el stub [m]    
        usar_TP = parametros['usar_tp']                         # Indica si los cálculos deben usar el tp indicado o calcular el TP mínimo
        dict_TP = parametros['dict_tp']                         # Diccionario con Lados correspondiente a la sección transversal del pedestal [m] de ser requerido
        H_relleno_min = parametros["h_relleno_min"]             # h_relleno_min {float} -- Altura mínima del relleno [m]
        lista_D_p = parametros['lista_D_p']                     # lista_D_p {list} -- Lista de diámetros del pilote [m]
        lista_H_z_min = parametros['lista_H_z_min']             # lista_H_z_min {list} -- Lista de alturas de zapata mínimas correspondiente a cada diámetro del pilote [m]
        E_p = parametros["E_p"]                                 # Modulo de elasticidad del material de los pilotes [kPa]
        FSC = parametros['fsc']                                 # FSC {float} -- Factor de seguridad mínimo para cargas a compresión
        FSLl = parametros['fsll']                               # FSL {float} -- Factor de seguridad mínimo para cargas laterales pila larga
        FSLc = parametros['fslc']                               # FSL {float} -- Factor de seguridad mínimo para cargas laterales pila corta
        FST = parametros['fst']                                 # FST {float} -- Factor de seguridad mínimo para cargas a tensión
        FSCp = parametros['fsc_p']                              # FSCp {float} -- Factor de seguridad mínimo para cargas a compresión para un pilote

        # θ: Ángulo del pedestal con respecto a la vertical [°]
        θ = info_cargas.get_angulo_inclinacion(torre)

        # TP: Ancho mínimo del pedestal [m], calculado a partir de los parámetros geométricos del pedestal
        usar_TP = parametros['usar_tp'] # 
        if usar_TP:
            dict_TP = parametros['dict_tp']
            TP = dict_TP[torre.tipo]
        else:
            B_a = info_cargas.get_ancho_aleta_conector_cortante(torre)  # B_a: Ancho de la aleta del conector de cortante del stub [m]
            TP = 2 * (1.5 * B_a + d_agg + d_b_long + d_b_trans + rec)
            TP = math.ceil(TP * 10) / 10 # Aproximación a la décima por arriba

        # D_f_min: Profundidad mínima de desplante [m], calculada a partir de la proyección vertical del stub
        pvs = info_cargas.get_proyeccion_vertical_stub(torre)  # Proyección vertical del stub                               
        HG_min = min(iter(lista_HG))
        D_f_min = math.ceil((pvs + rec_fondo_stub - HG_min) *10) /10

        # Se revisa si se puede calcular pilotes dadas las restricciones de profundidad mínima
        # y máxima de desplante 
        if D_f_min > D_f_max:
            mensaje_error = f"Error: D_f_min > D_f_max. Prof. mínima desplante: {D_f_min}, Prof. máxima desplante: {D_f_max}."
            print(f"Error inesperado procesando: {mensaje_error}")
            if pausar_en_error:
                input("...")
            return [{"D_f": None, "D_d": None, "HG": None, "H": None, "TP": None, "θ": None, "B": None, "H_z": None, "d_bor":d_bor, "error": True, "mensaje_error": mensaje_error, "evaluacion": {}}]

        # Nivel freático incluyendo inundabilidad
        NF = perfil.calcular_NF()

        # Inclinación del terreno
        ω = torre.inclinacion_terreno or 0

        # f_carga_p: Fracción de carga que toman los pilotes [0..1]
        if f_carga_por_torre:
            f_carga_p = torre.f_carga_p
        else:
            f_carga_p = f_carga_p_fijo

        #
        profundidad_perfil = perfil.calcular_profundidad_total()

        resultados = []
        for D_f in generar_serie(D_f_min, D_f_max, D_f_paso, 2):
            
            lista_H_posible = [h for h in lista_H if D_f + h <= profundidad_perfil]

            # Se satura todo el perfil si
            # el nivel freático esta por encima de
            # la profundidad de desplante
            if NF is not None and NF < D_f:
                perfil_ajustado = perfil.clonar_saturado()
                γ_c_ajustado = γ_c - γ_agua
                ajuste_saturacion_perfil = True
            else:
                perfil_ajustado = perfil
                γ_c_ajustado = γ_c
                ajuste_saturacion_perfil = False

            for index, D_p in enumerate(lista_D_p):
                S_p = factor_S_p * D_p  
                H_z = max(S_p * math.sqrt(2) / 4, tan_g(25) * S_p * math.sqrt(2) / 2 + rec, lista_H_z_min[index])
                H_z = math.ceil(H_z * 10) / 10
                # Verifica si con el desplante 'D_f' y la altura de zapata 'H_z_min' se pueda lograr la altura mínima de relleno 'H_relleno_min' 
                if D_f - H_z < H_relleno_min:
                    mensaje_error = f"No se puede lograr altura de relleno mínimo. D_f: {D_f}, H_z: {H_z}, H_relleno_min: {H_relleno_min}"
                    resultado = {"D_f": D_f, "HG": None, "B": None, "H_z": H_z, "TP": TP, "θ": θ, "d_bor": d_bor, "f_carga_p": f_carga_p, "n": None, "H": None, "D_p": D_p,
                                "S_p": None, "ω":ω, "error": True, "mensaje_error": mensaje_error, "evaluacion": {}}
                    self.clasificar_resultado(resultados, resultado, n_soluciones)
                    break                
                for n in lista_n:
                    for H in lista_H_posible:
                        resultados_por_hg = []
                        for HG in lista_HG:
                            resultado = {"D_f": D_f, "HG": HG, "B": None, "H_z": H_z, "TP": TP, "θ": θ, "d_bor": d_bor, "f_carga_p": f_carga_p, 
                            "n": n, "H": H, "D_p": D_p, "S_p": S_p, "ω":ω, "error": False, "mensaje_error": None, "evaluacion": {}}
                            try:
                                pilotes = Pilotes(D_f, H_z, n, S_p, D_p, H, HG, h_c, θ_c, h_con, TP, θ, γ_c_ajustado, E_p, d_bor, f_carga_p, perfil_ajustado, hincado, campana, ω)
                                resultado["B"] = pilotes.B
                                resultado["evaluacion"]  = self.evaluador.evaluar(pilotes, torre, perfil, info_cargas, FSC, FST, FSLl, FSLc, FSCp, s_max_adm_c, s_max_adm_g, s_max_adm_r, k ,t)
                                resultado["modulos_balasto"] = pilotes.calculo_modulos_de_reaccion_horizontal()
                                resultado["volumen_pilotes"] = pilotes.volumen_cimentacion()
                                resultado["volumen_relleno"] = pilotes.volumen_relleno()
                                resultado["volumen_ponderado"] = (pilotes.volumen_cimentacion() * 4 + pilotes.volumen_relleno())/5
                                resultado["ajuste_saturacion_perfil"] = ajuste_saturacion_perfil
                                resultado["relleno"] = perfil.calcular_material_relleno(pilotes.D_f - pilotes.H_z)


                            except Exception  as e:
                                resultado["error"] = True
                                resultado["mensaje_error"] = str(e)
                                print("Error inesperado procesando: Torre:{torre.nombre}, D_f: {D_f}, Error: {str(e)}")
                                traceback.print_exc(file=sys.stdout)
                                if pausar_en_error:
                                    input("...")

                            except:
                                print(f"Error no interceptado en n:{n}, H:{H}, D_p{D_p}")

                            finally:
                                resultados_por_hg.append(resultado)

                        # El optimizador encuentra los pilotes óptimos que funcione para todos
                        # los pedestales. Requiere entonces sintetizar todos los resultados por pedestal
                        # en uno solo, que sirva para comparar en la selección del óptimo
                        resultado_grupo = self.integrar_resultados(resultados_por_hg)

                        # Clasificación del resultado en busca de las mejores soluciones
                        self.clasificar_resultado(resultados, resultado_grupo, n_soluciones)
                                    
        return resultados

    def integrar_resultados(self, resultados_por_hg):
        resultado_grupo = {}        
        resultado_grupo["D_f"] = resultados_por_hg[0]["D_f"]
        resultado_grupo["B"] = resultados_por_hg[0]["B"]
        resultado_grupo["H_z"] = resultados_por_hg[0]["H_z"]
        resultado_grupo["HG"] = [r["HG"] for r in resultados_por_hg]
        resultado_grupo["TP"] = resultados_por_hg[0]["TP"]
        resultado_grupo["θ"] = resultados_por_hg[0]["θ"]
        resultado_grupo["d_bor"] = resultados_por_hg[0]["d_bor"]
        resultado_grupo["f_carga_p"] = resultados_por_hg[0]["f_carga_p"]
        resultado_grupo["n"] = resultados_por_hg[0]["n"]
        resultado_grupo["H"] = resultados_por_hg[0]["H"]
        resultado_grupo["D_p"] = resultados_por_hg[0]["D_p"]
        resultado_grupo["S_p"] = resultados_por_hg[0]["S_p"]
        resultado_grupo["ω"] = resultados_por_hg[0]["ω"]       
        resultado_grupo["error"] = any([r["error"] for r in resultados_por_hg])
        if resultado_grupo["error"]:
            resultado_grupo["mensaje_error"] = ". ".join(set([r["mensaje_error"] for r in resultados_por_hg if r["error"]]))
            resultado_grupo["evaluacion"] = {}
            resultado_grupo["modulos_balasto"] = None
            resultado_grupo["volumen_pilotes"] = None
            resultado_grupo["volumen_relleno"] = None
            resultado_grupo["volumen_ponderado"] = None
            resultado_grupo["ajuste_saturacion_perfil"] = None
            resultado_grupo["relleno"] = None
        else:
            resultado_grupo["mensaje_error"] = None
            resultado_grupo["evaluacion"] = {}
            keys_verif = resultados_por_hg[0]["evaluacion"].keys()
            for key in keys_verif:
                resultado_grupo["evaluacion"][key] = max([r["evaluacion"][key] for r in resultados_por_hg], key = lambda x : x["desviacion"] if x["desviacion"] else float("-inf") )
            resultado_grupo["modulos_balasto"] = resultados_por_hg[0]["modulos_balasto"]
            resultado_grupo["volumen_pilotes"] = max([r["volumen_pilotes"] for r in resultados_por_hg])
            resultado_grupo["volumen_relleno"] = resultados_por_hg[0]["volumen_relleno"]
            resultado_grupo["volumen_ponderado"] = max([r["volumen_ponderado"] for r in resultados_por_hg])
            resultado_grupo["ajuste_saturacion_perfil"] = resultados_por_hg[0]["ajuste_saturacion_perfil"]
            resultado_grupo["relleno"] = resultados_por_hg[0]["relleno"]

        return resultado_grupo

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
                resultado["calificacion"] = (incumplimientos, resultado["volumen_pilotes"])
            else:
                sum_desviaciones_fs =  math.sqrt(sum([evaluacion[key]["desviacion"]**2 for key in evaluacion if not evaluacion[key]["cumple"]]))
                resultado["calificacion"] = (incumplimientos, sum_desviaciones_fs)
        
        if len(resultados) < n_soluciones:
            resultados.append(resultado)
            resultados.sort(key = lambda r: r["calificacion"])
        elif resultado["calificacion"] <  resultados[-1]["calificacion"]:
            resultados[-1] = resultado
            resultados.sort(key = lambda r: r["calificacion"])
