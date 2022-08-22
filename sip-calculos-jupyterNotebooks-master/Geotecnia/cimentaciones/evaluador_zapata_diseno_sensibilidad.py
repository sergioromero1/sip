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

class EvaluadorZapataDisenoSensibilidad():

    def __init__(self, evaluador: EvaluadorZapatas):
        self.evaluador = evaluador

    def evaluar(self, grupo, delta_z, parametros: DBFila, torre: Torre, perfil: Perfil, info_cargas: Cargas, pausar_en_error: bool = True, usar_geom_grupo:bool = True ) -> Dict[Tuple[float,float], Dict[str, Tuple[float,float,bool]]]:
        """
        TODO
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
        γ_c = parametros["gamma_c"]                   # Peso unitario de la cimentación. Se corrige más adelante por saturación. [kN/m³]
        θ = info_cargas.get_angulo_inclinacion(torre) # Ángulo del pedestal con respecto a la vertical [°]

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

        # Información del grupo de diseño
        B = grupo["b"]
        D = grupo["d"]
        # H_grupo = grupo["h_grupo"]
        # TP_grupo = grupo["tp_grupo"]
        lista_HG = grupo["hgs"]                  # lista_HG {List[float]} -- Lista de altura de pedestales [m]
        Hs = grupo["hs_grupo"]
        TPs = grupo["tps_grupo"]

        rec_fondo_stub = parametros['rec_fondo_stub']  # rec_fondo_stub {float} --Recubrimiento vertical en el fondo de la zapata para el stub [m]

        
        # Proyección vertical del stub
        pvs = info_cargas.get_proyeccion_vertical_stub(torre)

        # Nivel freático de campo
        NFC = perfil.nivel_freatico_exploracion

        # Nivel freático incluyendo inundabilidad
        NF = perfil.calcular_NF()

        # Inclinación del terreno
        ω = torre.inclinacion_terreno or 0        
        
        # Inclinación de la base de la zapata
        α = torre.inclinacion_base_zapata or 0 

        perfil_ajustado = perfil
        
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

        resultados = []
        resultados_por_hg = []
        for HG in lista_HG:

            # TP: Lado correspondiente a la sección transversal del pedestal [m]
            if usar_geom_grupo:
                TP = TPs[str(HG)]
            else:
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

            # H: Espesor del dado [m]
            if usar_geom_grupo:
                H = Hs[str(HG)]
            else:
                usar_H = parametros['usar_h']
                H = parametros['h']
                if not usar_H:
                    H = max(H, TP / 2)
            
            resultado = {"B": B, "D": D - delta_z, "HG": HG + delta_z, "TP": TP, "θ": θ, "α": α, "ω": ω, "error": False, "mensaje_error": None, "evaluacion": {}}  
            try:
                C = D + HG - H
                
                if C < pvs + rec_fondo_stub - H:
                    resultado["error"] = True
                    resultado["mensaje_error"] = "Falla por stub"
                else:
                    zapata = Zapata(B, B, D - delta_z, H, C, TP, θ, γ_c, perfil_ajustado, α, ω)
                    resultado["H"] = zapata.H
                    resultado["evaluacion"] = self.evaluador.evaluar(zapata, torre, perfil_ajustado, info_cargas, FSC, FST_g, FST_c, k, t, S_max_adm_c, S_max_adm_g, FSV, FSL)
                    resultado["ajuste_saturacion_perfil"] = ajuste_saturacion_perfil
                    resultado["da"] = DA
                    resultado["derrumbabilidad"] = derrumbabilidad
                    resultado["volumen_zapata"] = zapata.volumen()
                    resultado["volumen_relleno"] = zapata.volumen_relleno()
                    resultado["volumen_ponderado"] = (zapata.volumen() * 4 + zapata.volumen_relleno())/5
                    resultado["esbeltez"] = zapata.D / zapata.B
                    resultado["relleno"] = perfil.calcular_material_relleno(zapata.D - zapata.H)
                    resultado["parametros_suelo"] = self.calcular_parametros_generales_suelo(resultado["evaluacion"])

            except Exception  as e:
                resultado["error"] = True
                resultado["mensaje_error"] = str(e)
                print(f"Error inesperado procesando: Torre:{torre.nombre}, B:{B}, D:{D - delta_z}, HG:{HG + delta_z}, Error:{str(e)}")
                traceback.print_exc(file=sys.stdout)
                if pausar_en_error:
                    input("...")
            except:
                print(f"Error no interceptado en B:{B}, D:{D - delta_z}")

            finally:
                resultados_por_hg.append(resultado)               

        # Se integran los resultados del grupo de pedestales
        resultado_grupo = self.integrar_resultados(resultados_por_hg)

        # Clasificación del resultado
        self.clasificar_resultado(resultados, resultado_grupo)

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
                resultado_grupo["evaluacion"][key] = max([r["evaluacion"][key] for r in resultados_por_hg], key = lambda x : x["desviacion"])
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
                resultado["calificacion"] = (incumplimientos, resultado["volumen_ponderado"])
            else:
                sum_desviaciones_fs =  math.sqrt(sum([evaluacion[key]["desviacion"]**2 for key in evaluacion if not evaluacion[key]["cumple"]]))
                resultado["calificacion"] = (incumplimientos, sum_desviaciones_fs)
        
        resultados.append(resultado)
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
            