import math
import json
import copy
import sys, traceback
from typing import List, Dict, Tuple, Any
from .pilotes import Pilotes
from .perfil import Perfil
from .torre import Torre
from .cargas import Cargas
from .util import γ_agua

DBFila = Dict[str, Any]

class EvaluadorPilotes():

    def evaluar(self, pilotes:Pilotes, torre: Torre, perfil: Perfil, info_cargas: Cargas, FSC:float, FST:float, FSLl:float, FSLc:float, FSCp:float, S_max_adm_c: {float}, S_max_adm_g: {float}, S_max_adm_r: float, k: {int}, t: {int}):
        """Realiza todas las evaluaciones de estabilidad y demás restrcciones en los pilotes
                
        Arguments:
            pilotes {Pilotes} -- Pilotes a evaluar
            torre {Torre} -- Torre donde se evalúan los pilotes
            perfil {Perfil} -- Perfil estratigráfico asociado a la torre 
            info_cargas {Cargas} -- Información de cargas
            FSC {float} -- Factor de seguridad a compresión
            FST {float} -- Factor de seguridad a tensión
            FSL {float} -- Factor de seguridad a carga lateral
            S_max_adm_c {float} -- Asentamiento máximo suelo cohesivo
            S_max_adm_g {float} -- Asentamiento máximo suelo granular
        
        Returns:
            {Dict[]} -- Diccionario con la evaluación de los pilotes
        """

        evaluacion = {}

        # Capacidad portante del pilote más cargado- máxima compresión
        cargas = info_cargas.obtener_cargas_trabajo_maxima_compresion_cartesiano(torre)
        evaluacion["cap_port_pilote-comp_max"] = self.evaluar_capacidad_portante_pilote(pilotes, cargas, FSCp)
        # Capacidad portante del pilote más cargado - máxima longitudinal
        cargas = info_cargas.obtener_cargas_trabajo_maxima_longitudinal_cartesiano(torre)
        evaluacion["cap_port_pilote-long_max"] = self.evaluar_capacidad_portante_pilote(pilotes, cargas, FSCp)
        # Capacidad portante del pilote más cargado - máxima transversal
        cargas = info_cargas.obtener_cargas_trabajo_maxima_transversal_cartesiano(torre)
        evaluacion["cap_port_pilote-tran_max"] = self.evaluar_capacidad_portante_pilote(pilotes, cargas, FSCp)

        # Capacidad portante del grupo de pilotes - máxima compresión
        F_zc, _, _ = info_cargas.obtener_cargas_trabajo_maxima_compresion_cartesiano(torre)
        evaluacion["cap_port_grupo-comp_max"] = self.evaluar_capacidad_portante_grupo(pilotes, F_zc, FSC)
        # # Capacidad portante del grupo de pilotes - máxima longitudinal
        # F_zc, _, _  = info_cargas.obtener_cargas_trabajo_maxima_longitudinal_cartesiano(torre)
        # evaluacion["cap_port_grupo-long_max"] = self.evaluar_capacidad_portante_grupo(pilotes, F_zc, FSC)
        # # Capacidad portante del grupo de pilotes - máxima transversal
        # F_zc, _, _  = info_cargas.obtener_cargas_trabajo_maxima_transversal_cartesiano(torre)
        # evaluacion["cap_port_grupo-tran_max"] = self.evaluar_capacidad_portante_grupo(pilotes, F_zc, FSC)

        # Arrancamiento un pilote - máxima tensión
        cargas = info_cargas.obtener_cargas_trabajo_maxima_tesion_cartesiano(torre)
        evaluacion["arrancamiento_pilote-tens_max"] = self.evaluar_arrancamiento_pilote(pilotes, cargas, FST)

        # Arrancamiento grupo - máxima tensión
        F_zc, _, _ = info_cargas.obtener_cargas_trabajo_maxima_tesion_cartesiano(torre)
        evaluacion["arrancamiento_grupo-tens_max"] = self.evaluar_arrancamiento_grupo(pilotes, F_zc, FST)

        # Asentamiento - máxima compresión
        cargas = info_cargas.obtener_cargas_trabajo_maxima_compresion_cartesiano(torre)
        cargas_eds = info_cargas.obtener_cargas_trabajo_maxima_compresion_eds_cartesiano(torre)
        evaluacion["asentamiento-comp_max"] = self.evaluar_asentamiento(pilotes, cargas, cargas_eds, k, t, S_max_adm_c, S_max_adm_g, S_max_adm_r)

        # Deslizamiento pilote - máxima longitudinal
        cargas = info_cargas.obtener_cargas_trabajo_maxima_longitudinal_cartesiano(torre)
        evaluacion["deslizamiento_pilote-long_max"] = self.evaluar_deslizamiento_pilote(pilotes, cargas, FSLl, FSLc)
        # Deslizamiento pilote - máxima transversal
        cargas = info_cargas.obtener_cargas_trabajo_maxima_transversal_cartesiano(torre)
        evaluacion["deslizamiento_pilote-tran_max"] = self.evaluar_deslizamiento_pilote(pilotes, cargas, FSLl, FSLc)

        # Deslizamiento grupo - máxima longitudinal
        F_zc, F_xc, F_yc = info_cargas.obtener_cargas_trabajo_maxima_longitudinal_cartesiano(torre)
        evaluacion["deslizamiento_grupo-long_max"] = self.evaluar_deslizamiento_grupo(pilotes, F_xc, FSLl, FSLc)
        # Deslizamiento - máxima transversal
        F_zc, F_xc, F_yc = info_cargas.obtener_cargas_trabajo_maxima_transversal_cartesiano(torre)
        evaluacion["deslizamiento_grupo-tran_max"] = self.evaluar_deslizamiento_grupo(pilotes, F_yc, FSLl, FSLc)

        return evaluacion

    def evaluar_capacidad_portante_pilote(self, pilotes:Pilotes, cargas: List[float], FSCp:float):
        """
        Evalua los pilotes respecto a la compresión
        
        Arguments:
            pilotes {Pilotes} -- Pilotes a evaluar
            cargas {Cargas} -- Información de cargas
            FSCp {float} -- Factor de seguridad a compresión de un pilote
        
        Returns:
            Dict[float,float,float,bool,dict[], float] -- Diccionario con los resultados: (P_act, P_adm, fs, cumple, memoria, desviacion)
        """

        # Cargas
        F_zc, F_hl, F_ht = cargas

        P_act, _ = pilotes.calculo_carga_maxima_pilote(F_zc, F_hl, F_ht)

        # Solicitud, capacidad y memoria 
        q_ult, _, _, memoria_p, memoria_s = pilotes.calculo_capacidad_portante_pilote()

        # factor de seguridad respecto a Q_max
        fs = round(q_ult / P_act, 2)

        # Cumplimiento respecto a Q_max
        cumple = fs >= FSCp 

        # Desviación
        desviacion = (FSCp - fs) / FSCp

        return {"P_act":P_act, 
                "q_ult":q_ult,
                "fs":fs, 
                "cumple": cumple,
                "memoria_p":memoria_p, 
                "memoria_s":memoria_s, 
                "desviacion":desviacion} 

    def evaluar_capacidad_portante_grupo(self, pilotes:Pilotes, F_zc: float, FSC:float):
        """
        Evalua los pilotes respecto a la compresión
        
        Arguments:
            pilotes {Pilotes} -- Pilotes a evaluar
            cargas {Cargas} -- Información de cargas
            FSC {float} -- Factor de seguridad a compresión
        
        Returns:
            Dict[float,float,float,bool,dict[], float] -- Diccionario con los resultados: (P_act, P_adm, fs, cumple, memoria, desviacion)
        """

        P_act = pilotes.peso_dado() + pilotes.peso_relleno() + F_zc

        # Solicitud, capacidad y memoria 
        q_ult, memoria = pilotes.calculo_de_capacidad_portante()

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
                "memoria":memoria, 
                "desviacion":desviacion} 

    def evaluar_arrancamiento_pilote(self, pilotes:Pilotes, cargas: List[float], FST:float):
        """
        Evalua los pilotes respecto a la tensión (arrancamiento)
        
        Arguments:
            pilotes {Pilotes} -- Pilotes a evaluar
            cargas {Cargas} -- Información de cargas
            FST {float} -- Factor de seguridad a tensión
        
        Returns:
            Dict[float,float,float,bool,dict[], float] -- Diccionario con los resultados: (T_adm, fs, cumple, memoria, desviacion)
        """
        # Cargas
        F_zc, F_hl, F_ht = cargas

        P_act, _ = pilotes.calculo_carga_maxima_pilote_tension(F_zc, F_hl, F_ht)

        # Capacidad
        P_t, _, memoria = pilotes.calculo_tension_pilote()
    
        # Factor de seguridad
        # cumple
        # Desviación
        if P_act == 0:
            fs = None
            cumple = True
            desviacion = None
        else:
            fs =  round(P_t / P_act, 2)
            cumple = fs >= FST
            desviacion = (FST - fs) / FST

        return {"P_t":P_t,
                "fs":fs,
                "cumple":cumple,
                "memoria":memoria,
                "desviacion": desviacion}

    def evaluar_arrancamiento_grupo(self, pilotes:Pilotes, F_zc: float, FST:float):
        """
        Evalua los pilotes respecto a la tensión (arrancamiento)
        
        Arguments:
            pilotes {Pilotes} -- Pilotes a evaluar
            cargas {Cargas} -- Información de cargas
            FST {float} -- Factor de seguridad a tensión
        
        Returns:
            Dict[float,float,float,bool,dict[], float] -- Diccionario con los resultados: (T_adm, fs, cumple, memoria, desviacion)
        """
        P_act = F_zc

        # Capacidad
        P_t, memoria = pilotes.calculo_de_tension()
    
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

    def evaluar_asentamiento(self, pilotes: Pilotes, cargas: List[float], cargas_eds: List[float], k:int, t:int, S_max_adm_c: float, S_max_adm_g:float, S_max_adm_r: float):
        """
        Evalua los pilotes  respecto a la tensión (arrancamiento)
        
        Arguments:
            pilotes {Pilotes} -- Pilotes a evaluar
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

        D = pilotes.D_f + 2 / 3 * pilotes.H
        tipos_mat_porcen = pilotes.perfil.calcular_porcentaje_tipo_mat(D, D + 2 * pilotes.x)

        
        if tipos_mat_porcen["c"] > 0 or tipos_mat_porcen["g"] > 0:
            if round(tipos_mat_porcen["c"] / (tipos_mat_porcen["c"] + tipos_mat_porcen["g"]), 2) >= 0.3:
                S_max_adm = S_max_adm_c
            else:
                S_max_adm = S_max_adm_g  
        else:
            S_max_adm = S_max_adm_r

        # Cargas
        F_zc, _, _ = cargas
        F_zc_eds, _, _ = cargas_eds

        # Capacidad
        S_e, S_c, memoria_e, memoria_c = pilotes.calculo_asentamiento(k, F_zc, F_zc_eds, t)
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

    def evaluar_deslizamiento_pilote(self, pilotes: Pilotes, cargas: List[float], FSLl:float, FSLc:float):
        """
        Evalua los pilotes respecto a la carga lateral
        
        Arguments:
            pilotes {Pilotes} -- pilotes a evaluar
            cargas {List[float]} -- Conjunto de cargas (Vertical y lateral)
            FSL {float} -- Factor de seguridad a carga lateral
        
        Returns:
            Dict[float,float,float,bool,dict[], float] -- Diccionario con los resultados: (F, Q_L, fs, cumple, memoria, desviacion)
        """
        # Cargas
        #F_zc, F = cargas

        F_zc, F_hl, F_ht = cargas

        _, F = pilotes.calculo_carga_maxima_pilote(F_zc, F_hl, F_ht)
        
        # Capacidad
        Q_L, p_corta, memoria = pilotes.calculo_carga_lateral_pilote()  # esta funcion utiliza para un chequeo todos los casos de carga
        
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

    def evaluar_deslizamiento_grupo(self, pilotes: Pilotes, F_h: float, FSLl:float, FSLc:float):
        """
        Evalua los pilotes respecto a la carga lateral
        
        Arguments:
            pilotes {Pilotes} -- pilotes a evaluar
            cargas {List[float]} -- Conjunto de cargas (Vertical y lateral)
            FSL {float} -- Factor de seguridad a carga lateral
        
        Returns:
            Dict[float,float,float,bool,dict[], float] -- Diccionario con los resultados: (F, Q_L, fs, cumple, memoria, desviacion)
        """   
        
        # Capacidad
        Q_L, p_corta, memoria = pilotes.calculo_carga_lateral()  # esta funcion utiliza para un chequeo todos los casos de carga
        
        if p_corta:
            FSL = FSLc
        else:
            FSL = FSLl

        # Factor de seguridad
        fs = round(Q_L / F_h, 2)
        
        # Cumple
        cumple = fs >= FSL

        # Desviación
        desviacion = (FSL - fs) / FSL    

        return {"F_h":F_h,
                "Q_L":Q_L,
                "fs":fs,
                "p_corta":p_corta,
                "cumple":cumple,
                "memoria":memoria,
                "desviacion":desviacion}
    