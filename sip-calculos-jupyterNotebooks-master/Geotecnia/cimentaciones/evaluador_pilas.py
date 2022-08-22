import math
import json
import copy
import sys, traceback
from typing import List, Dict, Tuple, Any
from .pila import Pila
from .perfil import Perfil
from .torre import Torre
from .cargas import Cargas
from .util import γ_agua

DBFila = Dict[str, Any]

class EvaluadorPila():

    def evaluar(self, pila:Pila, torre: Torre, perfil: Perfil, info_cargas: Cargas, FSC:float, FST:float, FSV:float, FSLl:float, FSLc:float, S_max_adm_c: {float}, S_max_adm_g: {float}, S_max_adm_r: float):
        """Realiza todas las evaluaciones de estabilidad y demás restrcciones en la pila
                
        Arguments:
            pila {Pila} -- Pila a evaluar
            torre {Torre} -- Torre donde se evalúan los pila
            perfil {Perfil} -- Perfil estratigráfico asociado a la torre 
            info_cargas {Cargas} -- Información de cargas
            FSC {float} -- Factor de seguridad a compresión
            FST {float} -- Factor de seguridad a tensión
            FSV {float} -- Factor de seguridad a volcamiento
            FSL {float} -- Factor de seguridad a carga lateral
            S_max_adm_c {float} -- Asentamiento máximo suelo cohesivo
            S_max_adm_g {float} -- Asentamiento máximo suelo granular
            ex {float} -- excentricidad para carga lateral
        
        Returns:
            {Dict[]} -- Diccionario con la evaluación de la pila
        """

        evaluacion = {}

        # Capacidad portante de la pila - máxima compresión
        cargas = info_cargas.obtener_cargas_trabajo_maxima_compresion_cartesiano(torre)
        evaluacion["cap_port-comp_max"] = self.evaluar_capacidad_portante_pila(pila, cargas, FSC)
        # Capacidad portante de la pila  - máxima longitudinal
        cargas = info_cargas.obtener_cargas_trabajo_maxima_longitudinal_cartesiano(torre)
        evaluacion["cap_port-long_max"] = self.evaluar_capacidad_portante_pila(pila, cargas, FSC)
        # Capacidad portante de la pila - máxima transversal
        cargas = info_cargas.obtener_cargas_trabajo_maxima_transversal_cartesiano(torre)
        evaluacion["cap_port-tran_max"] = self.evaluar_capacidad_portante_pila(pila, cargas, FSC)

        # Arrancamiento pila - máxima tensión
        cargas = info_cargas.obtener_cargas_trabajo_maxima_tesion_cartesiano(torre)
        evaluacion["arrancamiento-tens_max"] = self.evaluar_arrancamiento_pila(pila, cargas, FST)

        # Asentamiento - máxima compresión
        cargas = info_cargas.obtener_cargas_trabajo_maxima_compresion_cartesiano(torre)
        cargas_eds = info_cargas.obtener_cargas_trabajo_maxima_compresion_eds_cartesiano(torre)
        evaluacion["asentamiento-comp_max"] = self.evaluar_asentamiento_pila(pila, cargas_eds, S_max_adm_c, S_max_adm_g, S_max_adm_r)

        # Volcamiento - máxima tensión
        cargas = info_cargas.obtener_cargas_trabajo_maxima_tesion_cartesiano(torre)
        evaluacion["volcamiento-tens_max"] = self.evaluar_volcamiento_pila(pila, cargas, FSV)
        # Volcamiento - máxima longitudinal
        cargas = info_cargas.obtener_cargas_trabajo_maxima_longitudinal_cartesiano(torre)
        evaluacion["volcamiento-long_max"] = self.evaluar_volcamiento_pila(pila, cargas, FSV)
        # Volcamiento - máxima transversal
        cargas = info_cargas.obtener_cargas_trabajo_maxima_transversal_cartesiano(torre)
        evaluacion["volcamiento-tran_max"] = self.evaluar_volcamiento_pila(pila, cargas, FSV)

        # Deslizamiento pila - máxima longitudinal
        cargas = info_cargas.obtener_cargas_trabajo_maxima_longitudinal_cartesiano(torre)
        evaluacion["deslizamiento-long_max"] = self.evaluar_deslizamiento_pila(pila, cargas, FSLl, FSLc)
        # Deslizamiento pila - máxima transversal
        cargas = info_cargas.obtener_cargas_trabajo_maxima_transversal_cartesiano(torre)
        evaluacion["deslizamiento-tran_max"] = self.evaluar_deslizamiento_pila(pila, cargas, FSLl, FSLc)

        return evaluacion

    def evaluar_capacidad_portante_pila(self, pila:Pila, cargas: List[float], FSC:float):
        """
        Evalua la pila respecto a la compresión
        
        Arguments:
            pila {Pila} -- Pila a evaluar
            cargas {Cargas} -- Información de cargas
            FSC {float} -- Factor de seguridad a compresión
        
        Returns:
            Dict[float,float,float,bool,dict[], float] -- Diccionario con los resultados: (P_act, P_adm, fs, cumple, memoria, desviacion)
        """

        # Cargas
        P_act, _, _ = cargas

        # Solicitud, capacidad y memoria 
        q_ult, _, _, memoria_p, memoria_s = pila.calculo_capacidad_portante()

        # factor de seguridad respecto a Q_max
        fs = round(q_ult / P_act, 2)

        # Cumplimiento respecto a Q_max
        cumple = fs >= FSC 

        # Desviación
        desviacion = (FSC - fs) / FSC

        return {"P_act":P_act, 
                "q_ult":q_ult,
                "fs":fs, 
                "cumple": cumple,
                "memoria_p":memoria_p, 
                "memoria_s":memoria_s, 
                "desviacion":desviacion} 

    def evaluar_arrancamiento_pila(self, pila:Pila, cargas: List[float], FST:float):
        """
        Evalua los pila respecto a la tensión (arrancamiento)
        
        Arguments:
            pila {Pila} -- Pila a evaluar
            cargas {Cargas} -- Información de cargas
            FST {float} -- Factor de seguridad a tensión
        
        Returns:
            Dict[float,float,float,bool,dict[], float] -- Diccionario con los resultados: (T_adm, fs, cumple, memoria, desviacion)
        """
        # Cargas
        P_act, _, _ = cargas

        # Capacidad
        P_t, memoria = pila.calculo_tension()
    
        # Factor de seguridad
        fs = round(P_t / P_act, 2)
        
        # cumple
        cumple = fs >= FST

        #Desviación
        desviacion = (FST - fs) / FST

        return {"P_t":P_t,
                "fs":fs,
                "cumple":cumple,
                "memoria":memoria,
                "desviacion": desviacion}

    def evaluar_asentamiento_pila(self, pila:Pila, cargas_eds: List[float], S_max_adm_c: float, S_max_adm_g:float, S_max_adm_r: float):
        """
        Evalua la pila  respecto a la tensión (arrancamiento)
        
        Arguments:
            pila {Pila} -- Pila a evaluar
            cargas {Cargas} -- Información de cargas
            cargas_eds {Cargas} -- Información de cargas EDS
            k {int} -- Número de segmentos para análisis de asentamiento
            t {int} -- Número de años para corrección 'Creep'
            S_max_adm_c {float} -- Asentamiento máximo permitido para suelos cohesivos [m]
            S_max_adm_g {float} -- Asentamiento máximo permitido para suelos granulares [m]
        
        Returns:
            Tuple[float,float,bool] -- Tupla con los resultados: (asentamiento, holgura, cumple)
        """
        # Asentamiento máximo permitido [m] 

        
        tipos_mat_porcen = pila.perfil.calcular_porcentaje_tipo_mat(pila.D, pila.D + 2 * pila.D_c)

        
        if tipos_mat_porcen["c"] > 0 or tipos_mat_porcen["g"] > 0:
            if round(tipos_mat_porcen["c"] / (tipos_mat_porcen["c"] + tipos_mat_porcen["g"]), 2) >= 0.3:
                S_max_adm = S_max_adm_c
            else:
                S_max_adm = S_max_adm_g  
        else:
            S_max_adm = S_max_adm_r

        # Cargas
        # F_zc, _, _ = cargas
        F_zc_eds, _, _ = cargas_eds

        # Capacidad
        S_e, S_c, memoria_e, memoria_c = pila.calculo_asentamiento(F_zc_eds)
        S_e = round(S_e, 100)
        S_c = round(S_c, 100)
        S = round(S_e + S_c, 100)

        # Holgura
        holgura = round(S_max_adm - S, 6)
        
        # Cumple
        cumple = holgura >= 0

        # Desviación
        desviacion = 0.0 if cumple else (S - S_max_adm)/ S_max_adm

        memoria_e["S_max_adm"] = S_max_adm

        return {"S_e":S_e,
                "S_c":S_c,
                "S":S,
                "holgura":holgura,
                "cumple":cumple,
                "memoria_e":memoria_e,
                "memoria_c":memoria_c,
                "desviacion": desviacion}

    def evaluar_volcamiento_pila(self, pila: Pila, cargas: List[float], FSV:float):
        """
        Evalua la Pila respecto al volcamiento
        
        Arguments:
            pila {Pila} -- Pila a evaluar
            cargas {Cargas} -- Información de cargas
            FSV {float} -- Factor de seguridad a vuelco
        
        Returns:
            Dict[float,float,float,bool,dict[], float] -- Diccionario con los resultados: (Mv, Me, fs, cumple, memoria, desviacion)
        """      
        _, p_corta, _ = pila.calculo_carga_lateral(cargas) 

        # Cargas
        F_zc, F_xc, F_yc = cargas

        # Solicitud y Capacidad
        F = math.sqrt(F_xc**2 + F_yc**2)
        Mv, Me, memoria = pila.calculo_volcamiento(F_zc, F)

        # Factor de seguridad
        # Cumple
        # Desviación
        if p_corta:
            fs = round(Me / Mv, 2)
            cumple = fs >= FSV
            desviacion = (FSV - fs) / FSV
        else:
            fs = None
            cumple = True
            desviacion = None  # revisar si no hay ningun problema con esto 

        return {"Mv":Mv,
                "Me":Me,
                "fs":fs,
                "p_corta":p_corta,
                "cumple":cumple,
                "memoria":memoria,
                "desviacion":desviacion}

    def evaluar_deslizamiento_pila(self, pila: Pila, cargas: List[float], FSLl:float, FSLc:float):
        """
        Evalua la pila respecto a la carga lateral
        
        Arguments:
            pila {Pila} -- pila evaluar
            cargas {List[float]} -- Conjunto de cargas (Vertical y lateral)
            FSL {float} -- Factor de seguridad a carga lateral
        
        Returns:
            Dict[float,float,float,bool,dict[], float] -- Diccionario con los resultados: (F, Q_L, fs, cumple, memoria, desviacion)
        """   

        # Cargas
        #F_zc, F = cargas

        _, F_xc, F_yc = cargas

        F = math.sqrt(F_xc**2 + F_yc**2)
        
        # Capacidad
        Q_L, p_corta, memoria = pila.calculo_carga_lateral(cargas)    
        
        if p_corta:
            FSL = FSLc
        else:
            FSL = FSLl

        # Factor de seguridad
        fs = round(Q_L / F, 2)
        
        # Cumple
        cumple = fs >= FSL

        # Desviación
        desviacion = (FSL - fs) / FSL    

        return {"F":F,
                "Q_L":Q_L,
                "fs":fs,
                "p_corta":p_corta,
                "cumple":cumple,
                "memoria":memoria,
                "desviacion":desviacion}

    
