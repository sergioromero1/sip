import json
import copy
import sys, traceback
import math
from typing import List, Dict, Tuple, Any
from .pila import Pila
from .perfil import Perfil
from .torre import Torre
from .cargas import Cargas
from .util import γ_agua, tan_g, generar_serie
from .evaluador_pilas import EvaluadorPila

DBFila = Dict[str, Any]

class OptimizadorPilasPorTorre():

    def __init__(self, evaluador: EvaluadorPila):
        self.evaluador = evaluador

    def optimizar(self, parametros: DBFila, torre: Torre, perfil: Perfil, info_cargas: Cargas, hg_por_pata: bool, n_soluciones:int, pausar_en_error: bool = True) -> Dict[Tuple[float,float], Dict[str, Tuple[float,float,bool]]]:
        """
        Evalua pilas para la torre:'torre', en el espacio D_p, H (diametro, espesor).
        El resultado de esta evaluación es un arreglo con información de las 'n_soluciones'
        mejores soluciones en la forma de un diccionario. Cada diccionario de
        evaluación tiene información de la pila y las verificaciones relizadas en ella.
        
        Arguments:
            parametros {DBFila} -- Diccionario con los parámetros de diseño
            torre {DBFila} -- Diccionario con los datos de la torre
            perfil {Perfil} -- Perfil estratigráfico asociado a la torre 
            info_cargas {Cargas} -- Información de cargas
            hg_por_pata {bool} -- Indica si se debe tener en cuenta los pedestales de las torres además de la lista estándar 'lista_hg'
            n_soluciones {int} -- Número de mejores soluciones para almacenar en la corrida
            pausar_en_error {bool} -- Indica si se debe pausar la ejecución si se presenta un error inesper
        Returns:
            {} -- 
        """
        if perfil.calcular_NF():
            raise Exception("No puede optimizar pila en zona saturada")

        # Límites para el espacio de evaluación D_p (diametro), H (espesor), HGs(pedestales)
        
        D_p_min = parametros['D_p_min']                         # D_p_min {float} -- Valor mínimo para las iteraciones de diametro de la pila D_p [m]
        D_p_max = parametros['D_p_max']                         # D_p_max {float} -- Valor máximo para las iteraciones de diametro de la pila D_p [m]
        D_p_paso = parametros['D_p_paso']                       # D_p_paso {float} -- Incremento para las iteraciones de diametro de la pila D_p [m]
        H_min = parametros['H_min']                             # H_min {float} -- Valor mínimo para las iteraciones del espesor de la pila H [m]
        H_max = parametros['H_max']                             # H_max {float} -- Valor máximo para las iteraciones del espesor de la pila H [m]
        H_paso = parametros['H_paso']                           # H_paso {float} -- Incremento para las iteraciones del espesor de la pila H [m]
        h_i_min = parametros['h_i_min']                         # h_i_min {float} -- Valor mínimo para las iteraciones de la profundidad de inicio de la pila [m]
        h_i_max = parametros['h_i_max']                         # h_i_max {float} -- Valor máximo para las iteraciones de la profundidad de inicio de la pila [m]
        h_i_paso = parametros['h_i_paso']                        # h_i_paso {float} -- Incremento para las iteraciones de la profundidad de inicio de la pila [m]
        # h_is = parametros['h_is']                               # h_is {float} -- Listado de profundidad inicial de la pila [m]
        rec = parametros['rec']                                 # rec {float} -- Espesor del recubrimiento [m]
        rec_fondo_stub = parametros['rec_fondo_stub']           # rec_fondo_stub {float} --Recubrimiento vertical en el fondo de la pila para el stub [m]
        h_c = parametros['h_c']                                 # h_c {float} -- altura de campana [m]
        h_con = parametros['h_con']                             # h_con {float} -- Altura de la sección conica de la campana[m]
        θ_c = parametros['θ_c']                                 #θ_c {float} --  Ángulo de la campana [°]

        campana = parametros['campana']                         #campana{bool} -- Boleano que define condicion de la pila con o sin campana
        γ_c = parametros['gamma_c']          # Peso unitario de la cimentación [kN/m³]
        θ = info_cargas.get_angulo_inclinacion(torre) # Ángulo del pedestal con respecto a la vertical [°]
        E_p = parametros["E_p"]                                 # Modulo de elasticidad del material de la pila [kPa]
        
        # Factores de seguridad y restricciones
        FSC = parametros['fsc']              # FSC {float} -- Factore de seguridad a compresión
        FST = parametros['fst']              # FST {float} -- Factor de seguridad a tensión suelo granular
        FSV = parametros['fsv']              # FSV {float} -- Factor de seguridad para volcamiento
        FSLl = parametros['fsll']            # FSLl {float} -- Factor de seguridad mínimo para cargas laterales
        FSLc = parametros['fslc']            # FSLc {float} -- Factor de seguridad mínimo para cargas laterales

        # Asentamientos máximos 
        s_max_adm_g = parametros['s_max_adm_g']                 # s_max_adm_g {float} -- Asentamiento máximo permitido suelos granulares [m]
        s_max_adm_c = parametros['s_max_adm_c']                 # s_max_adm_c {float} -- Asentamiento máximo permitido suelos cohesivos [m]
        s_max_adm_r = parametros['s_max_adm_r']                 # s_max_adm_r {float} -- Asentamiento máximo permitido roca [m]

        # Lado correspondiente a la sección transversal del pedestal [m]    
        usar_TP = parametros['usar_tp'] # 
        if usar_TP:
            dict_TP = parametros['dict_tp']
            TP = dict_TP[torre.tipo]
        else:
            d_agg = parametros['d_agg']          # d_agg {float} -- Tamaño máximo nominal del agregado grueso [m]
            d_b_long = parametros['d_b_long']    # d_b_long {float} -- Diámetro de barras de refuerzo longitudinal [m]
            d_b_trans = parametros['d_b_trans']  # d_b_trans {float} -- Diámetro de barras de refuerzo transversal [m]
            rec = parametros['rec']              # rec {float} -- Longitud del recubrimiento [m]
            ancho_aleta = info_cargas.get_ancho_aleta_conector_cortante(torre)
            TP = 2 * (1.5 * ancho_aleta + d_agg + d_b_long + d_b_trans + rec)
            TP = math.ceil(TP * 10) / 10 # Aproximación a la décima por arriba

        # Proyección vertical del stub
        pvs = info_cargas.get_proyeccion_vertical_stub(torre)
                
        # lista_HG {List[float]} -- Lista de altura de pedestales a evaluar [m]
        # se incluyen los pedestales de la lista estándar que se define en los parámetros
        # y si el parámetro 'hg_por_pata' = True, entonces incluye además cualquier
        # pedestal no estándar que aparezca en la torre.
        lista_HG = copy.copy(parametros["lista_hg"])
        if hg_por_pata:
            if torre.ped_pata_a is not None and not torre.ped_pata_a in lista_HG:
                lista_HG.append(torre.ped_pata_a) 
            if torre.ped_pata_b is not None and not torre.ped_pata_b in lista_HG:
                lista_HG.append(torre.ped_pata_b) 
            if torre.ped_pata_c is not None and not torre.ped_pata_c in lista_HG:
                lista_HG.append(torre.ped_pata_c) 
            if torre.ped_pata_d is not None and not torre.ped_pata_d in lista_HG:
                lista_HG.append(torre.ped_pata_d) 
        lista_HG.sort()

        # Inclinación del terreno
        ω = torre.inclinacion_terreno or 0

        resultados = []
        for h_i  in generar_serie(h_i_min, h_i_max, h_i_paso):
            for D_p in generar_serie(D_p_min, D_p_max, D_p_paso, 2):
                for H in generar_serie(H_min, H_max, H_paso, 2):
                    resultados_por_hg = []               
                    for HG in lista_HG:
                        resultado = {"D_p": D_p, "H": H, "HG": HG, "TP": TP, "θ": θ, "h_i": h_i, "ω": ω, "campana": campana, "error": False, "mensaje_error": None, "evaluacion": {}}                
                        try:
                            D_p_req_por_pedestal = TP * 2**0.5 + 4 * rec
                            D_p_req_por_stub = tan_g(θ) * (pvs - HG - h_i) + 2 * rec + d_b_long + d_b_trans + ancho_aleta

                            if D_p < D_p_req_por_pedestal:
                                resultado["error"] = True
                                resultado["mensaje_error"] = "Falla por ancho de pedestal"
                            elif D_p < D_p_req_por_stub:
                                resultado["error"] = True
                                resultado["mensaje_error"] = "Falla por stub a lo ancho, HG: {}".format(HG)
                            elif h_i + HG < pvs + rec_fondo_stub - H :
                                resultado["error"] = True
                                resultado["mensaje_error"] = "Falla por stub a lo alto, HG: {}".format(HG)
                            else:
                                pila = Pila(D_p, h_i, H, HG, h_c, h_con, θ_c, TP, θ, γ_c, E_p, perfil, campana, ω)
                                resultado["evaluacion"]  = self.evaluador.evaluar(pila, torre, perfil, info_cargas, FSC, FST, FSV, FSLl, FSLc, s_max_adm_c, s_max_adm_g, s_max_adm_r)
                                resultado["modulos_balasto"] = pila.calculo_modulos_de_reaccion_horizontal()
                                resultado["volumen_pila"] = pila.volumen()
                                resultado["volumen_relleno"] = pila.volumen_relleno()
                                resultado["volumen_ponderado"] = (pila.volumen() * 4 + pila.volumen_relleno())/5
                                resultado["esbeltez"] = pila.D / pila.D_p
                                resultado["relleno"] = perfil.calcular_material_relleno(pila.D - pila.H)

                        except Exception as e:
                            resultado["error"] = True
                            resultado["mensaje_error"] = str(e)
                            print("Error inesperado procesando: Torre:{}, D_p:{}, H:{}, HG:{}, h_i: {}, Error:", torre.nombre, D_p, H, HG, h_i, str(e))
                            traceback.print_exc(file=sys.stdout)
                            if pausar_en_error:
                                input("...")

                        finally:
                            resultados_por_hg.append(resultado)

                    # El optimizador encuentra la pilástra óptima que funcione para todos
                    # los pedestales. Requiere entonces sintetizar todos los resultados por pedestal
                    # en uno solo, que sirva para comparar en la selección del óptimo
                    resultado_grupo = self.integrar_resultados(resultados_por_hg)

                    # Clasificación del resultado en busca de las mejores soluciones
                    self.clasificar_resultado(resultados, resultado_grupo, n_soluciones)

        return resultados

    def integrar_resultados(self, resultados_por_hg):
        resultado_grupo = {}        
        resultado_grupo["D_p"] = resultados_por_hg[0]["D_p"]
        resultado_grupo["H"] = resultados_por_hg[0]["H"]
        resultado_grupo["HG"] = [r["HG"] for r in resultados_por_hg]
        resultado_grupo["TP"] = resultados_por_hg[0]["TP"]
        resultado_grupo["θ"] = resultados_por_hg[0]["θ"]
        resultado_grupo["h_i"] = resultados_por_hg[0]["h_i"]      
        resultado_grupo["ω"] = resultados_por_hg[0]["ω"]
        resultado_grupo["campana"] = resultados_por_hg[0]["campana"]
        resultado_grupo["error"] = any([r["error"] for r in resultados_por_hg])
        if resultado_grupo["error"]:
            resultado_grupo["mensaje_error"] = ". ".join(set([r["mensaje_error"] for r in resultados_por_hg if r["error"]]))
            resultado_grupo["evaluacion"] = {}
            resultado_grupo["modulos_balasto"] = None
            resultado_grupo["volumen_pila"] = None
            resultado_grupo["volumen_relleno"] = None
            resultado_grupo["volumen_ponderado"] = None
            resultado_grupo["esbeltez"] = None
            resultado_grupo["relleno"] = None
        else:
            resultado_grupo["mensaje_error"] = None
            resultado_grupo["evaluacion"] = {}
            keys_verif = resultados_por_hg[0]["evaluacion"].keys()
            for key in keys_verif:
                resultado_grupo["evaluacion"][key] = max([r["evaluacion"][key] for r in resultados_por_hg], key = lambda x : x["desviacion"])
            resultado_grupo["modulos_balasto"] = resultados_por_hg[0]["modulos_balasto"]
            resultado_grupo["volumen_pila"] = max([r["volumen_pila"] for r in resultados_por_hg])
            resultado_grupo["volumen_relleno"] = resultados_por_hg[0]["volumen_relleno"]
            resultado_grupo["volumen_ponderado"] = max([r["volumen_ponderado"] for r in resultados_por_hg])
            resultado_grupo["esbeltez"] = resultados_por_hg[0]["esbeltez"]
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
                resultado["calificacion"] = (incumplimientos, resultado["volumen_pila"])
            else:
                sum_desviaciones_fs =  math.sqrt(sum([evaluacion[key]["desviacion"]**2 for key in evaluacion if not evaluacion[key]["cumple"]]))
                resultado["calificacion"] = (incumplimientos, sum_desviaciones_fs)

        if len(resultados) < n_soluciones:
            resultados.append(resultado)
            resultados.sort(key = lambda r: r["calificacion"])
        elif resultado["calificacion"] <  resultados[-1]["calificacion"]:
            resultados[-1] = resultado
            resultados.sort(key = lambda r: r["calificacion"])
