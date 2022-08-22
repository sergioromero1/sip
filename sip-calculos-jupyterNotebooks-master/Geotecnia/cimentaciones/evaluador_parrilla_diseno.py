import math
import json
import copy
import sys, traceback
from typing import List, Dict, Tuple, Any
from .parrilla import Parrilla
from .perfil import Perfil
from .torre import Torre
from .cargas import Cargas
from .util import γ_agua, generar_serie
from .evaluador_parrillas import EvaluadorParrillas

DBFila = Dict[str, Any]

class EvaluadorParrillasDiseno():

    def __init__(self, evaluador: EvaluadorParrillas):
        self.evaluador = evaluador

    def evaluar(self, datos_parrilla, parametros: DBFila, torre: Torre, perfil: Perfil, info_cargas: Cargas, pausar_en_error: bool = True ) -> Dict[Tuple[float,float], Dict[str, Tuple[float,float,bool]]]:
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
        B = datos_parrilla["b"]
        D = datos_parrilla["d"]
        peso = datos_parrilla["peso"]
        tipo_parrilla = datos_parrilla["tipo_parrilla"]
        esf_act_ingedisa  = datos_parrilla["esf_act_ingedisa"]
        H =  datos_parrilla["h"]
        TP =  datos_parrilla["tp"]
        mv_ingedisa  = datos_parrilla["mv_ingedisa"]

        # Inclinación del terreno
        ω = torre.inclinacion_terreno or 0        
        
        # Inclinación de la base de la zapata
        α = torre.inclinacion_base_zapata or 0 

        perfil_ajustado = perfil

        resultados = []
            
        resultado = {"B": B, "D": D, "H": H, "TP": TP, "θ": θ, "α": α, "ω": ω, "error": False, "mensaje_error": None, "evaluacion": {}}  
        try:
            parrilla = Parrilla(B, B, D, H, D, TP, θ, peso, esf_act_ingedisa, mv_ingedisa, perfil_ajustado, α, ω)
            resultado["evaluacion"] = self.evaluador.evaluar(parrilla, torre, perfil_ajustado, info_cargas, FSC, FST_g, FST_c, k, t, S_max_adm_c, S_max_adm_g, FSV, FSL)
            resultado["volumen_relleno"] = parrilla.volumen_relleno()
            resultado["relleno"] = perfil.calcular_material_relleno(parrilla.D)
            resultado["parametros_suelo"] = self.calcular_parametros_generales_suelo(resultado["evaluacion"])
            resultado["peso_parrilla"] = peso
            resultado["tipo_parrilla"] = tipo_parrilla
            resultado["mv_ingedisa"] = mv_ingedisa
            resultado["esf_act_ingedisa"] = esf_act_ingedisa

        except Exception  as e:
            resultado["error"] = True
            resultado["mensaje_error"] = str(e)
            print(f"Error inesperado procesando: Torre:{torre.nombre}, B:{B}, D:{D}, Error:{str(e)}")
            traceback.print_exc(file=sys.stdout)
            if pausar_en_error:
                input("...")
        except:
            print(f"Error no interceptado en B:{B}, D:{D}")

        finally:
            # Clasificación del resultado
            self.clasificar_resultado(resultados, resultado)

        return resultados

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
                resultado["calificacion"] = (incumplimientos)
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
