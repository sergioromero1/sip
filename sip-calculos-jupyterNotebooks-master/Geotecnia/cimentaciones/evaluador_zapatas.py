import math
import json
import copy
import sys, traceback
from typing import List, Dict, Tuple, Any
from .zapata import Zapata
from .perfil import Perfil
from .torre import Torre
from .cargas import Cargas
from .util import γ_agua

DBFila = Dict[str, Any]

class EvaluadorZapatas():

    def evaluar(self, zapata: Zapata, torre: Torre, perfil: Perfil, info_cargas: Cargas, FSC: float, FST_g: {float}, FST_c: {float}, k: {int}, t: {int}, S_max_adm_c: {float}, S_max_adm_g: {float}, FSV: {float}, FSL: {float}):
        """Realiza todas las evaluaciones de estabilidad y demás restrcciones en la zapata
                
        Arguments:
            zapata {Zapata} -- Zapata a evaluar
            torre {Torre} -- Torre donde se evalúa la zapata
            perfil {Perfil} -- Perfil estratigráfico asociado a la torre 
            info_cargas {Cargas} -- Información de cargas
            FSC {float} -- Factor de seguridad a compresión
            FST_g {float} -- Factor de seguridad a tensión para suelos granulares
            FST_c {float} -- Factor de seguridad a tensión para suelos cohesivos
            k {int} --
            t {int} --
            S_max_adm_c {float} --
            S_max_adm_g {float} --
            FSV {float} -- Factor de seguridad a vuelco
            FSL {float} -- Factor de seguridad a carga lateral
        
        Returns:
            {Dict[]} -- Diccionario con la evaluación de pilastra 
        """
        evaluacion = {}

        # Capacidad portante - máxima compresión
        cargas = info_cargas.obtener_cargas_trabajo_maxima_compresion_cartesiano(torre)
        evaluacion["cap_port-comp_max"] = self.evaluar_capacidad_portante(zapata, cargas, FSC)
        # Capacidad portante - máxima longitudinal
        cargas = info_cargas.obtener_cargas_trabajo_maxima_longitudinal_cartesiano(torre)
        evaluacion["cap_port-long_max"] = self.evaluar_capacidad_portante(zapata, cargas, FSC)
        # Capacidad portante - máxima transversal
        cargas = info_cargas.obtener_cargas_trabajo_maxima_transversal_cartesiano(torre)
        evaluacion["cap_port-tran_max"] = self.evaluar_capacidad_portante(zapata, cargas, FSC)

        # Arrancamiento - máxima tensión
        cargas = info_cargas.obtener_cargas_trabajo_maxima_tesion_cartesiano(torre)
        q_ult = min(evaluacion["cap_port-comp_max"]["q_ult"],evaluacion["cap_port-long_max"]["q_ult"],evaluacion["cap_port-tran_max"]["q_ult"])
        evaluacion["arrancamiento-tens_max"] = self.evaluar_arrancamiento(zapata, perfil, cargas, q_ult, FSC, FST_g, FST_c)
        
        # Asentamiento - máxima compresión
        cargas = info_cargas.obtener_cargas_trabajo_maxima_compresion_cartesiano(torre)
        cargas_eds = info_cargas.obtener_cargas_trabajo_maxima_compresion_eds_cartesiano(torre)
        evaluacion["asentamiento-comp_max"] = self.evaluar_asentamiento(zapata, cargas, cargas_eds, k, t, S_max_adm_c, S_max_adm_g)
        
        # Volcamiento - máxima tensión
        T_u = evaluacion["arrancamiento-tens_max"]["T_u"]
        F_zc, F_xc, F_yc = info_cargas.obtener_cargas_trabajo_maxima_tesion_cartesiano(torre)
        evaluacion["volcamiento-tens_max"] = self.evaluar_volcamiento(zapata, (F_zc, max(F_xc, F_yc)), T_u, FSV)
        # Volcamiento - máxima longitudinal
        F_zc, F_xc, F_yc = info_cargas.obtener_cargas_trabajo_maxima_longitudinal_cartesiano(torre)
        evaluacion["volcamiento-long_max"] = self.evaluar_volcamiento(zapata, (F_zc, F_xc), T_u, FSV)
        # Volcamiento - máxima transversal
        F_zc, F_xc, F_yc = info_cargas.obtener_cargas_trabajo_maxima_transversal_cartesiano(torre)
        evaluacion["volcamiento-tran_max"] = self.evaluar_volcamiento(zapata, (F_zc, F_yc), T_u, FSV)
        
        # Deslizamiento - máxima longitudinal
        F_zc, F_xc, F_yc = info_cargas.obtener_cargas_trabajo_maxima_longitudinal_cartesiano(torre)
        evaluacion["deslizamiento-long_max"] = self.evaluar_deslizamiento(zapata, (F_zc, F_xc), FSL)
        # Deslizamiento - máxima transversal
        F_zc, F_xc, F_yc = info_cargas.obtener_cargas_trabajo_maxima_transversal_cartesiano(torre)
        evaluacion["deslizamiento-tran_max"] = self.evaluar_deslizamiento(zapata, (F_zc, F_yc), FSL)

        return evaluacion

    def evaluar_capacidad_portante(self, zapata: Zapata, cargas: List[float], FSC: float) -> Tuple[float,bool,float,float,bool]:
        """
        Evalua la zapata respecto a la compresión
        
        Arguments:
            zapata {Zapata} -- Zapata a evaluar
            cargas {Cargas} -- Información de cargas
            FSC {float} -- Factor de seguridad compresión
        
        Returns:
            Tuple[float,bool,float,float,bool] -- Tupla con los resultados: (holgura Qmin, cumple Qmin, Capacidad Qmax, holgura Qmax, cumple Qmax)
        """    

        # Cargas
        F_zc, F_xc, F_yc = cargas
        T = max(F_xc, F_yc)

        # Capacidad
        q_ult_neto, memoria_q_ult = zapata.calculo_capacidad_portante(T, F_zc)

        # Solicitud
        Q_max, Q_min, memoria_Q = zapata.calculo_esfuerzo_actuante_sobre_suelo(F_xc, F_yc, F_zc)

        # Holgura respecto a Q_min
        holgura_Q_min = Q_min

        # Cumplimiento respecto a Q_min
        cumple_Q_min = Q_min >= 0

        # factor de seguridad respecto a Q_max
        fs_Q_max = round(q_ult_neto / Q_max, 2)
        fs_Q_max = self.ajustar_fs(fs_Q_max, FSC, 0.05)

        # Cumplimiento respecto a Q_max
        cumple_Q_max = fs_Q_max >= FSC

        # Desviación
        desviacion = (FSC - fs_Q_max) / FSC

        return { "holgura_Q_min":holgura_Q_min, 
                "cumple_Q_min":cumple_Q_min, 
                "q_ult":q_ult, 
                "fs_Q_max":fs_Q_max, 
                "cumple_Q_max":cumple_Q_max, 
                "Q_min":Q_min, 
                "Q_max":Q_max, 
                "memoria_q_ult":memoria_q_ult, 
                "memoria_Q":memoria_Q,
                "cumple": cumple_Q_min and cumple_Q_max,
                "desviacion": desviacion}

    def evaluar_arrancamiento(self, zapata: Zapata, perfil: Perfil, cargas: List[float], q_ult: float, FSC: float, FST_g: float, FST_c: float) -> Tuple[float,float,bool]:
        """
        Evalua la zapata respecto a la tensión (arrancamiento)
        
        Arguments:
            zapata {Zapata} -- Zapata a evaluar
            perfil {Perfil} -- Perfil estratigráfico asociado a la torre 
            cargas {Cargas} -- Información de cargas
            q_ult {float} -- Capacidad portante última [kN/m²]
            FSC {float} -- Factore de seguridad a compresión
            FST_g {float} -- Factor de seguridad a tensión para suelos granulares
            FST_c {float} -- Factor de seguridad a tensión para suelos cohesivos
        
        Returns:
            Tuple[float,float,bool] -- Tupla con los resultados: (capacidad, holgura, cumple)
        """     

        # FST: Factor de seguridad a tensión
        tipo_mat_predominante = perfil.calcular_tipo_mat_predominante(0, zapata.D)
        if tipo_mat_predominante == "g":
            FST = FST_g
        elif tipo_mat_predominante == "c":
            FST = FST_c

        # Cargas
        F_zc, _, _ = cargas

        # Capacidad
        q_adm = q_ult / FSC
        T_u, memoria = zapata.calculo_tension(q_adm)

        # Factor de seguridad
        fs = round(T_u / F_zc, 2)
        fs = self.ajustar_fs(fs, FST, 0.01)
        
        # cumple
        cumple = fs >= FST

        # Desviación
        desviacion = (FST - fs) / FST

        #
        memoria["tipo_mat_predominante"] = tipo_mat_predominante

        return {"T_u":T_u,
                "fs":fs,
                "cumple":cumple,
                "memoria":memoria,
                "desviacion": desviacion}

    def evaluar_asentamiento(self, zapata: Zapata, cargas: List[float], cargas_eds: List[float], k: int, t: int, S_max_adm_c: float, S_max_adm_g: float) -> Tuple[float,float,bool]:
        """
        Evalua la zapata respecto a la tensión (arrancamiento)
        
        Arguments:
            zapata {Zapata} -- Zapata a evaluar
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
        tipos_mat_porcen = zapata.perfil.calcular_porcentaje_tipo_mat(zapata.D, zapata.D + 2 * zapata.B)
        if round(tipos_mat_porcen["r"], 2) == 100:
            S_max_adm = S_max_adm_g
        elif round(tipos_mat_porcen["c"] / (tipos_mat_porcen["c"] + tipos_mat_porcen["g"]), 2) >= 0.3:
            S_max_adm = S_max_adm_c  
        else:
            S_max_adm = S_max_adm_g

        # Cargas
        F_zc, _, _ = cargas
        F_zc_eds, _, _ = cargas_eds

        # Capacidad
        S_e, S_c, memoria_e, memoria_c = zapata.calculo_asentamiento(k, F_zc, F_zc_eds, t)
        S_e = round(S_e, 6)
        S_c = round(S_c, 6)
        S = round(S_e + S_c, 6)

        # Holgura
        holgura = round(S_max_adm - S, 6)
        
        # Cumple
        cumple = holgura >= 0

        # Desviación
        desviacion = (S - S_max_adm)/ S_max_adm

        memoria_e["S_max_adm"] = S_max_adm

        return {"S_e":S_e,
                "S_c":S_c,
                "S":S,
                "holgura":holgura,
                "cumple":cumple,
                "memoria_e":memoria_e,
                "memoria_c":memoria_c,
                "desviacion": desviacion}

    def evaluar_volcamiento(self, zapata: Zapata, cargas: List[float], T_u: float, FSV: float) -> Tuple[float,float,bool]:
        """
        Evalua la zapata respecto al volcamiento
        
        Arguments:
            zapata {Zapata} -- Zapata a evaluar
            cargas {Cargas} -- Información de cargas
            T_u {float} -- Capacidad al arranque del cimiento [kN]
            FSV {float} -- Factor de seguridad para volcamiento
        
        Returns:
            Tuple[float,float,bool] -- Tupla con los resultados: (capacidad, holgura, cumple)
        """      
        # Cargas
        F_zc, F = cargas

        # Solicitud y Capacidad
        Mv, Me, memoria = zapata.calculo_volcamiento(F_zc, F, T_u)

        # Factor de seguridad
        fs = round(Me / Mv, 2)
        fs = self.ajustar_fs(fs, FSV, 0.02)
        
        # Cumple
        cumple = fs >= FSV

        # Desviación
        desviacion = (FSV - fs) / FSV

        return {"Me":Me,
                "fs":fs,
                "cumple":cumple,
                "memoria":memoria,
                "desviacion": desviacion}

    def evaluar_deslizamiento(self, zapata: Zapata, cargas: List[float], FSL: float) -> Tuple[float,float,bool]:
        """
        Evalua la zapata respecto a la carga longitudinal
        
        Arguments:
            zapata {Zapata} -- Zapata a evaluar
            parametros {DBFila} -- Diccionario con los parámetros de diseño
            cargas {List[float]} -- Conjunto de cargas (Vertical y lateral)
            FSL {float} -- Factor de seguridad para cargas laterales
        
        Returns:
            Tuple[float,float,bool,dict] -- Tupla con los resultados: (capacidad, holgura, cumple, memoria)
        """   
        # Cargas
        F_zc, F = cargas
        
        # Capacidad
        Q_L, memoria = zapata.calculo_carga_lateral(F_zc)
        
        # Factor de seguridad
        fs = round(Q_L / F, 2)
        fs = self.ajustar_fs(fs, FSL, 0.01)
        
        # Cumple
        cumple = fs >= FSL    

        # Desviación
        desviacion = (FSL - fs) / FSL

        return {"Q_L": Q_L,
                "fs": fs,
                "cumple": cumple,
                "memoria": memoria,
                "desviacion": desviacion}

    def ajustar_fs(self, fs, FS, prec):
        if FS - fs > 0 and FS - fs <= prec:
            fs = FS
        return fs
