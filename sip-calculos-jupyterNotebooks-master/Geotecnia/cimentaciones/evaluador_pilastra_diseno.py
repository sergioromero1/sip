import json
import copy
import sys, traceback
import math
from typing import List, Dict, Tuple, Any
from .pilastra import Pilastra
from .perfil import Perfil
from .torre import Torre
from .cargas import Cargas
from .util import γ_agua, tan_g, generar_serie
from .evaluador_pilastras import EvaluadorPilastras

DBFila = Dict[str, Any]

class EvaluadorPilastraDiseno():

    def __init__(self, evaluador: EvaluadorPilastras):
        self.evaluador = evaluador

    def evaluar(self, grupo, parametros: DBFila, torre: Torre, perfil: Perfil, info_cargas: Cargas, pausar_en_error: bool = True, constructorPilastra = Pilastra) -> Dict[Tuple[float,float], Dict[str, Tuple[float,float,bool]]]:
        """
        Evalua pilastras para la torre:'torre', en el espacio D_p, H (diametro, espesor).
        El resultado de esta evaluación es un arreglo con información de las 'n_soluciones'
        mejores soluciones en la forma de un diccionario. Cada diccionario de
        evaluación tiene información de la pilastra y las verificaciones relizadas en ella.
        
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
            raise Exception("No puede optimizar pilastra en zona saturada")

        # Límites para el espacio de evaluación D_p (diametro), H (espesor), HGs(pedestales)
        
        rec_fondo_stub = parametros['rec_fondo_stub']  # rec_fondo_stub {float} --Recubrimiento vertical en el fondo de la pilastra para el stub [m]
        
        γ_c = parametros['gamma_c']          # Peso unitario de la cimentación [kN/m³]
        θ = info_cargas.get_angulo_inclinacion(torre) # Ángulo del pedestal con respecto a la vertical [°]
        
        # Factores de seguridad y restricciones
        FSC = parametros['fsc']              # FSC {float} -- Factore de seguridad a compresión
        FST = parametros['fst']              # FST {float} -- Factor de seguridad a tensión suelo granular
        FSV = parametros['fsv']              # FSV {float} -- Factor de seguridad para volcamiento
        FSL = parametros['fsl']              # FSL {float} -- Factor de seguridad para cargas laterales

        # Información del grupo de diseño
        D_p = grupo["d_p"]
        H = grupo["h_p"]
        h_i = grupo["h_i"]
        lista_HG = grupo["hgs"]                  # lista_HG {List[float]} -- Lista de altura de pedestales [m] 


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
        
        # Profundidad de la roca
        profundidad_roca = perfil.calcular_profundidad_hasta_roca()

        # Inclinación del terreno
        ω = torre.inclinacion_terreno or 0

        resultados = []
        resultados_por_hg = []               
        for HG in lista_HG:
            
            resultado = {"D_p": D_p, "H": H, "HG": HG, "TP": TP, "θ": θ, "h_i": h_i, "ω": ω, "profundidad_roca": profundidad_roca, "error": False, "mensaje_error": None, "evaluacion": {}}                
            try:
                D_p_req_por_pedestal = TP * 2**0.5 + 4 * rec
                D_p_req_por_stub = tan_g(θ) * (pvs - HG - profundidad_roca) + 2 * rec + d_b_long + d_b_trans + ancho_aleta

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
                    pilastra = constructorPilastra(h_i, D_p, H, HG, TP, θ, γ_c, perfil, ω)
                    resultado["evaluacion"]  = self.evaluador.evaluar(pilastra, torre, perfil, info_cargas, FSC, FST, FSV, FSL)
                    resultado["volumen_pilastra"] = pilastra.volumen()
                    resultado["volumen_relleno"] = pilastra.volumen_relleno()
                    resultado["volumen_ponderado"] = (pilastra.volumen() * 4 + pilastra.volumen_relleno())/5
                    resultado["esbeltez"] = pilastra.D / pilastra.D_p
                    resultado["relleno"] = perfil.calcular_material_relleno(pilastra.D - pilastra.H)

            except Exception as e:
                resultado["error"] = True
                resultado["mensaje_error"] = str(e)
                print("Error inesperado procesando: Torre:{}, D_p:{}, H:{}, HG:{}, Error:", torre.nombre, D_p, H, HG, str(e))
                traceback.print_exc(file=sys.stdout)
                if pausar_en_error:
                    input("...")

            finally:
                resultados_por_hg.append(resultado)

        # Se integran los resultados del grupo de pedestales
        resultado_grupo = self.integrar_resultados(resultados_por_hg)

        # Clasificación del resultado en busca de las mejores soluciones
        self.clasificar_resultado(resultados, resultado_grupo)

        return resultados

    def integrar_resultados(self, resultados_por_hg):
        resultado_grupo = {}        
        resultado_grupo["D_p"] = resultados_por_hg[0]["D_p"]
        resultado_grupo["H"] = resultados_por_hg[0]["H"]
        resultado_grupo["HG"] = [r["HG"] for r in resultados_por_hg]
        resultado_grupo["TP"] = resultados_por_hg[0]["TP"]
        resultado_grupo["θ"] = resultados_por_hg[0]["θ"]
        resultado_grupo["ω"] = resultados_por_hg[0]["ω"]
        resultado_grupo["h_i"] = resultados_por_hg[0]["h_i"]
        resultado_grupo["profundidad_roca"] = resultados_por_hg[0]["profundidad_roca"]        
        resultado_grupo["error"] = any([r["error"] for r in resultados_por_hg])
        if resultado_grupo["error"]:
            resultado_grupo["mensaje_error"] = ". ".join(set([r["mensaje_error"] for r in resultados_por_hg if r["error"]]))
            resultado_grupo["evaluacion"] = {}
            resultado_grupo["volumen_pilastra"] = None
            resultado_grupo["volumen_relleno"] = None
            resultado_grupo["volumen_ponderado"] = None
            resultado_grupo["esbeltez"] = None
            resultado_grupo["relleno"] = None
        else:
            resultado_grupo["mensaje_error"] = None
            resultado_grupo["evaluacion"] = {}
            keys_verif = resultados_por_hg[0]["evaluacion"].keys()
            for key in keys_verif:
                resultado_grupo["evaluacion"][key] = max([r["evaluacion"][key] for r in resultados_por_hg], key = lambda x : x["desviacion"] if x["desviacion"] else float("-inf"))
            resultado_grupo["volumen_pilastra"] = max([r["volumen_pilastra"] for r in resultados_por_hg])
            resultado_grupo["volumen_relleno"] = resultados_por_hg[0]["volumen_relleno"]
            resultado_grupo["volumen_ponderado"] = max([r["volumen_ponderado"] for r in resultados_por_hg])
            resultado_grupo["esbeltez"] = resultados_por_hg[0]["esbeltez"]
            resultado_grupo["relleno"] = resultados_por_hg[0]["relleno"]

        return resultado_grupo

    def clasificar_resultado(self, resultados: List, resultado: List):
        mala_calificacion = (999999, 999999)

        if resultado["error"]:
            resultado["cumple"] = False
            resultado["calificacion"] = mala_calificacion
        else:
            evaluacion = resultado["evaluacion"]
            resultado["cumple"] = all([evaluacion[key]["cumple"] for key in evaluacion])
            incumplimientos = sum([1  for key in evaluacion if not evaluacion[key]["cumple"]])
            if incumplimientos == 0:
                resultado["calificacion"] = (incumplimientos, resultado["volumen_pilastra"])
            else:
                sum_desviaciones_fs =  math.sqrt(sum([evaluacion[key]["desviacion"]**2 for key in evaluacion if not evaluacion[key]["cumple"]]))
                resultado["calificacion"] = (incumplimientos, sum_desviaciones_fs)

        resultados.append(resultado)
        resultados.sort(key = lambda r: r["calificacion"])

        return resultado["cumple"]
