import math
import json
import copy
import sys, traceback
from typing import List, Dict, Tuple, Any
from .pilastra import Pilastra
from .perfil import Perfil
from .torre import Torre
from .cargas import Cargas
from .util import γ_agua

DBFila = Dict[str, Any]

class EvaluadorPilastras():

    def evaluar(self, pilastra: Pilastra, torre: Torre, perfil: Perfil, info_cargas: Cargas, FSC:float, FST:float, FSV:float, FSL:float):
        """Realiza todas las evaluaciones de estabilidad y demás restrcciones en la pilastra
                
        Arguments:
            pilastra {Pilastra} -- Pilastra a evaluar
            torre {Torre} -- Torre donde se evalúa la pilastra
            perfil {Perfil} -- Perfil estratigráfico asociado a la torre 
            info_cargas {Cargas} -- Información de cargas
            FSC {float} -- Factor de seguridad a compresión
            FST {float} -- Factor de seguridad a tensión
            FSV {float} -- Factor de seguridad a vuelco
            FSL {float} -- Factor de seguridad a carga lateral
        
        Returns:
            {Dict[]} -- Diccionario con la evaluación de pilastra 
        """
        evaluacion = {}

        # Compresión- máxima compresión
        cargas = info_cargas.obtener_cargas_trabajo_maxima_compresion_cartesiano(torre)
        evaluacion["comp-comp_max"] = self.evaluar_compresion(pilastra, cargas, FSC)
        # Compresión - máxima longitudinal
        cargas = info_cargas.obtener_cargas_trabajo_maxima_longitudinal_cartesiano(torre)
        evaluacion["comp-long_max"] = self.evaluar_compresion(pilastra, cargas, FSC)
        # Compresión - máxima transversal
        cargas = info_cargas.obtener_cargas_trabajo_maxima_transversal_cartesiano(torre)
        evaluacion["comp-tran_max"] = self.evaluar_compresion(pilastra, cargas, FSC)

        # Arrancamiento - máxima tensión
        cargas = info_cargas.obtener_cargas_trabajo_maxima_tesion_cartesiano(torre)
        evaluacion["arrancamiento-tens_max"] = self.evaluar_arrancamiento(pilastra, cargas, FST)
        
        # Volcamiento - máxima tensión
        cargas = info_cargas.obtener_cargas_trabajo_maxima_tesion_cartesiano(torre)
        evaluacion["volcamiento-tens_max"] = self.evaluar_volcamiento(pilastra, cargas, FSV)
        # Volcamiento - máxima longitudinal
        cargas = info_cargas.obtener_cargas_trabajo_maxima_longitudinal_cartesiano(torre)
        evaluacion["volcamiento-long_max"] = self.evaluar_volcamiento(pilastra, cargas, FSV)
        # Volcamiento - máxima transversal
        cargas = info_cargas.obtener_cargas_trabajo_maxima_transversal_cartesiano(torre)
        evaluacion["volcamiento-tran_max"] = self.evaluar_volcamiento(pilastra, cargas, FSV)

        # Deslizamiento - máxima longitudinal
        F_zc, F_xc, F_yc = info_cargas.obtener_cargas_trabajo_maxima_longitudinal_cartesiano(torre)
        evaluacion["deslizamiento-long_max"] = self.evaluar_deslizamiento(pilastra, (F_zc, F_xc, F_yc), FSL)
        # Deslizamiento - máxima transversal
        F_zc, F_xc, F_yc = info_cargas.obtener_cargas_trabajo_maxima_transversal_cartesiano(torre)
        evaluacion["deslizamiento-tran_max"] = self.evaluar_deslizamiento(pilastra, (F_zc, F_yc, F_xc), FSL)

        return evaluacion

    def evaluar_compresion(self, pilastra: Pilastra, cargas: List[float], FSC: float):
        """
        Evalua la pilastra respecto a la compresión
        
        Arguments:
            pilastra {Pilatra} -- Pilastra a evaluar
            cargas {Cargas} -- Información de cargas
            FSC {float} -- Factor de seguridad a compresión
        
        Returns:
            Dict[float,float,float,bool,dict[], float] -- Diccionario con los resultados: (P_act, P_adm, fs, cumple, memoria, desviacion)
        """    
        
        # Cargas
        F_zc, _, _ = cargas

        # Solicitud, capacidad y memoria 
        P_adm, P_act, memoria = pilastra.calculo_compresion(F_zc)

        # factor de seguridad respecto a Q_max
        fs = round(P_adm / P_act, 2)

        # Cumplimiento respecto a Q_max
        cumple = fs >= FSC 

        # Desviación
        desviacion = (FSC - fs) / FSC

        return {"P_act":P_act, 
                "P_adm":P_adm,
                "fs":fs, 
                "cumple": cumple,
                "memoria":memoria, 
                "desviacion":desviacion} 

    def evaluar_arrancamiento(self, pilastra: Pilastra, cargas: List[float], FST:float):
        """
        Evalua la pilastra respecto a la tensión (arrancamiento)
        
        Arguments:
            pilastra {Pilastra} -- Pilastra a evaluar
            cargas {Cargas} -- Información de cargas
            FST {float} -- Factor de seguridad a tensión
        
        Returns:
            Dict[float,float,float,bool,dict[], float] -- Diccionario con los resultados: (T_adm, fs, cumple, memoria, desviacion)
        """     
        
            
        # Cargas
        F_zc, _, _ = cargas

        # Capacidad
        T_adm, memoria = pilastra.calculo_tension()
    
        # Factor de seguridad
        fs = round(T_adm / F_zc, 2)
        
        # cumple
        cumple = fs >= FST

        #Desviación
        desviacion = (FST - fs) / FST

        return {"T_adm":T_adm,
                "fs":fs,
                "cumple":cumple,
                "memoria":memoria,
                "desviacion": desviacion}

    def evaluar_volcamiento(self, pilastra: Pilastra, cargas: List[float], FSV:float):
        """
        Evalua la Pilastra respecto al volcamiento
        
        Arguments:
            pilastra {Pilastra} -- Pilastra a evaluar
            cargas {Cargas} -- Información de cargas
            FSV {float} -- Factor de seguridad a vuelco
        
        Returns:
            Dict[float,float,float,bool,dict[], float] -- Diccionario con los resultados: (Mv, Me, fs, cumple, memoria, desviacion)
        """      

        # Cargas
        F_zc, F_xc, F_yc = cargas

        # Solicitud y Capacidad
        F = math.sqrt(F_xc**2 + F_yc**2)
        Mv, Me, memoria = pilastra.calculo_volcamiento(F_zc, F)

        # Factor de seguridad
        fs = round(Me / Mv, 2)
        
        # Cumple
        cumple = fs >= FSV

        # Desviación
        desviacion = (FSV - fs) / FSV    

        return {"Mv":Mv,
                "Me":Me,
                "fs":fs,
                "cumple":cumple,
                "memoria":memoria,
                "desviacion":desviacion}

    def evaluar_deslizamiento(self, pilastra: Pilastra, cargas: List[float], FSL:float):
        """
        Evalua la pilastra respecto a la carga lateral
        
        Arguments:
            pilastra {Pilastra} -- pilastra a evaluar
            cargas {List[float]} -- Conjunto de cargas (Vertical y lateral)
            FSL {float} -- Factor de seguridad a carga lateral
        
        Returns:
            Dict[float,float,float,bool,dict[], float] -- Diccionario con los resultados: (F, Q_L, fs, cumple, memoria, desviacion)
        """   

        # Cargas
        #F_zc, F = cargas

        F_zc, F_xc, F_yc = cargas

        F = math.sqrt(F_xc**2 + F_yc**2)
        
        # Capacidad
        Q_L, memoria = pilastra.calculo_carga_lateral(F_zc)
        
        # Factor de seguridad
        fs = round(Q_L / F, 2)
        
        # Cumple
        cumple = fs >= FSL

        # Desviación
        desviacion = (FSL - fs) / FSL    

        return {"F":F,
                "Q_L":Q_L,
                "fs":fs,
                "cumple":cumple,
                "memoria":memoria,
                "desviacion":desviacion}