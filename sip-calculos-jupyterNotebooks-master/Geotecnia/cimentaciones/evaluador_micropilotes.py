import math
import json
import copy
import sys, traceback
from typing import List, Dict, Tuple, Any
from .micropilotes import Micropilotes
from .perfil import Perfil
from .torre import Torre
from .cargas import Cargas
from .util import γ_agua, π
from .barra import Barra
from .calculo_momento_flector import calcular_longitud_camisa, calcular_momento_flector

DBFila = Dict[str, Any]

class EvaluadorMicropilotes():

    def evaluar(self, micropilotes: Micropilotes, torre: Torre, perfil: Perfil, info_cargas: Cargas, H_min: float, H_max: float, H_paso: float, D_d_min: float, D_d_max: float, D_d_paso: float, H_relleno_min: float, FSC: float, FSCD: float, FST: {float}, k: {int}, t: {int}, S_max_adm_c: {float}, S_max_adm_g: {float}, S_max_adm_r: {float}, rec: {float}, FSL: {float}):
        evaluacion = {}
        micropilotes.D_d = 0
        # Deslizamiento - máxima longitudinal                                            
        F_am, _, F_hl, F_ht = info_cargas.obtener_cargas_trabajo_maxima_horz_long_montante(torre)
        evaluacion["deslizamiento-long_max"] = self.evaluar_deslizamiento(micropilotes, torre, (F_am, F_hl), H_min, H_max, H_paso, D_d_min, D_d_max, D_d_paso, H_relleno_min, FSL)
        # Deslizamiento - máxima transversal
        F_am, _, F_hl, F_ht  = info_cargas.obtener_cargas_trabajo_maxima_horz_trans_montante(torre)
        evaluacion["deslizamiento-tran_max"] = self.evaluar_deslizamiento(micropilotes, torre, (F_am, F_ht), H_min, H_max, H_paso, D_d_min, D_d_max, D_d_paso, H_relleno_min, FSL)

        # Rigidez del dado
        cond_rigidez1 = round(micropilotes.S_em / math.sqrt(2),2) < round(2 * micropilotes.H,2) 
        cond_rigidez2 = round(math.degrees(math.atan2( micropilotes.H - rec, micropilotes.S_em / math.sqrt(2))),2) >= 25
        while (not cond_rigidez1 or not cond_rigidez2) and round(micropilotes.H + H_paso,2) <= H_max and round(micropilotes.D_f - (micropilotes.H + H_paso),2) >= H_relleno_min:
            micropilotes.H += H_paso
            cond_rigidez1 = round(micropilotes.S_em / math.sqrt(2),2) < round(2 * micropilotes.H,2) 
            cond_rigidez2 = round(math.degrees(math.atan2( micropilotes.H - rec, micropilotes.S_em / math.sqrt(2))),2) >= 25

        if not cond_rigidez1 or not cond_rigidez2:
            raise ValueError(f"No cumple criterio de rigidez del dado. Cond 1:{cond_rigidez1} S_em/√2 ={round(micropilotes.S_em / math.sqrt(2),2)} debe ser menor que 2*H={round(2 * micropilotes.H,2)}, Cond 2:{cond_rigidez2} atan((H-rec)/(S-em/√2))={round(math.degrees(math.atan2( micropilotes.H - rec, micropilotes.S_em / math.sqrt(2))),2)} debe ser mayor o igual a 25")

        # Asentamientos - Max comp/EDS
        F_zc, _, _ = info_cargas.obtener_cargas_trabajo_maxima_compresion_cartesiano(torre)
        F_zc_eds, _, _ = info_cargas.obtener_cargas_trabajo_maxima_compresion_eds_cartesiano(torre)
        evaluacion["asentamientos-comp_max"] = self.evaluar_asentamiento(micropilotes, torre, F_zc, F_zc_eds, k, t, S_max_adm_g, S_max_adm_c, S_max_adm_r )

        # Micropilote Adherencia Micropilote Suelo - Máxima compresión montante trabajo
        F_m, _, F_hl, F_ht = info_cargas.obtener_cargas_trabajo_maxima_compresion_montante(torre)
        evaluacion["mp-adh-mp-suelo-comp_max_m"] = self.evaluar_micropilote_adherencia_mp_suelo(micropilotes, torre, (F_m, F_hl, F_ht))

        # Micropilote Adherencia Micropilote Suelo - Máxima lateral montante trabajo
        F_m, _, F_hl, F_ht = info_cargas.obtener_cargas_trabajo_maxima_lateral_montante(torre)
        evaluacion["mp-adh-mp-suelo-lat_max_m"] = self.evaluar_micropilote_adherencia_mp_suelo(micropilotes, torre, (F_m, F_hl, F_ht))

        # Micropilote Adherencia Micropilote Suelo - Máxima tensión montante trabajo
        F_m, _, F_hl, F_ht = info_cargas.obtener_cargas_trabajo_maxima_tension_montante(torre)
        evaluacion["mp-adh-mp-suelo-tens_max_m"] = self.evaluar_micropilote_adherencia_mp_suelo_tension(micropilotes, torre, (F_m, F_hl, F_ht))

        # Micropilote Tensión - Máxima tensión montante diseño
        F_m, _, F_hl, F_ht = info_cargas.obtener_cargas_diseno_maxima_tension_montante(torre)
        evaluacion["mp-tension-tens_max_m_d"] = self.evaluar_micropilote_tension(micropilotes, torre, (F_m, F_hl, F_ht))

        # Micropilote Compresión - Máxima compresión montante diseño
        F_m, _, F_hl, F_ht = info_cargas.obtener_cargas_diseno_maxima_compresion_montante(torre)
        evaluacion["mp-compresion-comp_max_m_d"] = self.evaluar_micropilote_compresion(micropilotes, torre, (F_m, F_hl, F_ht))

        # Micropilote Compresión - Máxima lateral montante diseño
        F_m, _, F_hl, F_ht = info_cargas.obtener_cargas_diseno_maxima_lateral_montante(torre)
        evaluacion["mp-compresion-lat_max_m_d"] = self.evaluar_micropilote_compresion(micropilotes, torre, (F_m, F_hl, F_ht))

        # Micropilote Adherencia Barra grouting - Máxima compresión montante trabajo
        F_m, _, F_hl, F_ht = info_cargas.obtener_cargas_trabajo_maxima_compresion_montante(torre)
        evaluacion["mp-adh-barra-grouting-comp_max_m"] = self.evaluar_micropilote_adherencia_barra_grouting(micropilotes, torre, (F_m, F_hl, F_ht))

        # Micropilote Adherencia Barra grouting - Máxima lateral montante trabajo
        F_m, _, F_hl, F_ht = info_cargas.obtener_cargas_trabajo_maxima_lateral_montante(torre)
        evaluacion["mp-adh-barra-grouting-lat_max_m"] = self.evaluar_micropilote_adherencia_barra_grouting(micropilotes, torre, (F_m, F_hl, F_ht))

        # Micropilote Adherencia Barra grouting - Máxima tensión montante trabajo
        F_m, _, F_hl, F_ht = info_cargas.obtener_cargas_trabajo_maxima_tension_montante(torre)
        evaluacion["mp-adh-barra-grouting-tens_max_m"] = self.evaluar_micropilote_adherencia_barra_grouting(micropilotes, torre, (F_m, F_hl, F_ht))

        # Compresión dado - Máxima compresión montante
        F_m, _, _, _ = info_cargas.obtener_cargas_trabajo_maxima_compresion_montante(torre)
        evaluacion["compresion_dado-comp_max_m"] = self.evaluar_compresion_dado(micropilotes, torre, F_m, FSCD)                                            

        # Compresión micropilotes - Máxima compresión montante
        F_m, _, _, _ = info_cargas.obtener_cargas_trabajo_maxima_compresion_montante(torre)
        evaluacion["compresion_micropilotes-comp_max_m"] = self.evaluar_compresion_micropilotes(micropilotes, torre, F_m, FSC)

        # Arrancamiento - Tensión  máxima montante
        P_permS = evaluacion["compresion_micropilotes-comp_max_m"]["P_permS"]
        F_m, _, _, _ = info_cargas.obtener_cargas_trabajo_maxima_tension_montante(torre)
        evaluacion["arrancamiento-tens_max_m"] = self.evaluar_arrancamiento(micropilotes, torre, F_m, FST, P_permS)

        # Calcular longitud de la camisa
        if all([evaluacion[key]["cumple"] for key in evaluacion]):
            P_mp = max(evaluacion["mp-compresion-comp_max_m_d"]["P_mp"], evaluacion["mp-compresion-lat_max_m_d"]["P_mp"])
            P_c = evaluacion["mp-compresion-comp_max_m_d"]["P_c"]
            evaluacion["camisa"] = self.calcular_camisa(micropilotes, torre, P_mp, P_c)
            micropilotes.L_c = evaluacion["camisa"]["L_c"]
        else:
            evaluacion["camisa"] = {"cumple": False, "L_c": None, "desviacion": 999999, "M_max": None}
        return evaluacion

    def evaluar_micropilote_adherencia_mp_suelo(self, micropilotes: Micropilotes, torre: Torre, cargas: List[float]):
        # Cargas 
        F_m, F_hl, F_ht = cargas

        # Se garantiza conformidad de P_G con  L_b, D_p, N_m y proc_iny
        P_mp = micropilotes.calculo_carga_maxima_micropilote(F_m, F_hl, F_ht)

        P_G, memoria = micropilotes.calculo_resistencia_por_fuste_micropilote()

        # Factor de seguridad mínimo
        FS = 1.0

        if P_mp > 0:
            fs = P_G / P_mp                    # Trabajo compresión, lateral, tensión (adherencia_mp_suelo)
        else:
            fs = 1
        
        # Ajuste del factor de seguridad. 0.99 -> 1, 0.98 -> 0.98
        fs = self.ajustar_fs(fs, FS, 0.01)

        cumple = fs >= FS

        # Desviación
        desviacion = FS - fs

        return {
            "P_G": P_G,
            "P_mp": P_mp,
            "fs": fs,
            "cumple": cumple,
            "memoria": memoria,
            "desviacion": desviacion
        }

    def evaluar_micropilote_adherencia_mp_suelo_tension(self, micropilotes: Micropilotes, torre: Torre, cargas: List[float]):
        # Cargas 
        F_m, F_hl, F_ht = cargas

        # Se garantiza conformidad de P_G con  L_b, D_p, N_m y proc_iny
        P_mp = micropilotes.calculo_carga_maxima_micropilote_tension(F_m, F_hl, F_ht)

        P_G, memoria = micropilotes.calculo_resistencia_por_fuste_micropilote()

        # Factor de seguridad mínimo
        FS = 1.0

        if P_mp > 0:
            fs = P_G / P_mp                    # Trabajo compresión, lateral, tensión (adherencia_mp_suelo)
        else:
            fs = 1.0

        # Ajuste del factor de seguridad. 0.99 -> 1, 0.98 -> 0.98
        fs = self.ajustar_fs(fs, FS, 0.01)

        cumple = fs >= FS

        # Desviación
        desviacion = FS - fs

        return {
            "P_G": P_G,
            "P_mp": P_mp,
            "fs": fs,
            "cumple": cumple,
            "memoria": memoria,
            "desviacion": desviacion
        }

    def evaluar_micropilote_tension(self, micropilotes: Micropilotes, torre: Torre, cargas: List[float]):

        # Cargas 
        F_m, F_hl, F_ht = cargas

        # Se garantiza conformidad de P_G con  L_b, D_p, N_m y proc_iny
        P_mp = micropilotes.calculo_carga_maxima_micropilote_tension(F_m, F_hl, F_ht)

        P_t, memoria = micropilotes.calculo_carga_tension_varilla()

        # Factor de seguridad mínimo
        FS = 1.0

        if P_mp > 0:
            fs = P_t / P_mp                    # Diseño tensión (tension)
        else:
            fs = 1

        # Ajuste del factor de seguridad. 0.99 -> 1, 0.98 -> 0.98
        fs = self.ajustar_fs(fs, FS, 0.01)

        cumple = fs >= FS

        # Desviación
        desviacion = FS - fs

        return {
            "P_t": P_t,
            "fs": fs,
            "P_mp": P_mp,
            "cumple": cumple,
            "memoria": memoria,
            "desviacion": desviacion
        }

    def evaluar_micropilote_compresion(self, micropilotes: Micropilotes, torre: Torre, cargas: List[float]):

        # Cargas 
        F_m, F_hl, F_ht = cargas

        # Se garantiza conformidad de P_G con  L_b, D_p, N_m y proc_iny
        P_mp = micropilotes.calculo_carga_maxima_micropilote(F_m, F_hl, F_ht)

        P_c, memoria = micropilotes.calculo_carga_compresion_varilla()

        # Factor de seguridad mínimo
        FS = 1.0

        if P_mp > 0:
            fs = P_c / P_mp                    # Diseño compresión, lateral (compresion)
        else:
            fs = 1

        # Ajuste del factor de seguridad. 0.99 -> 1, 0.98 -> 0.98
        # fs = self.ajustar_fs(fs, FS, 0.01)
        fs = self.ajustar_fs(fs, FS, 0.02)

        cumple = fs >= FS

        # Desviación
        desviacion = FS - fs

        return {
            "P_c": P_c,
            "fs": fs,
            "P_mp": P_mp,
            "cumple": cumple,
            "memoria": memoria,
            "desviacion": desviacion
        }

    def evaluar_micropilote_adherencia_barra_grouting(self, micropilotes: Micropilotes, torre: Torre, cargas: List[float]):

        # Cargas 
        F_m, F_hl, F_ht = cargas

        # Se garantiza conformidad de P_G con  L_b, D_p, N_m y proc_iny
        P_mp = micropilotes.calculo_carga_maxima_micropilote(F_m, F_hl, F_ht)

        P_br_gr, memoria = micropilotes.calculo_adherencia_barra_grouting()

        # Factor de seguridad mínimo
        FS = 1.0

        if P_mp > 0:
            fs = P_br_gr / P_mp           # Trabajo compresión, lateral, tensión (adherencia_barra_grouting)
        else:
            fs = 1

        # Ajuste del factor de seguridad. 0.99 -> 1, 0.98 -> 0.98
        fs = self.ajustar_fs(fs, FS, 0.01)

        cumple = fs >= FS

        # Desviación
        desviacion = FS - fs

        return {
            "P_br_gr": P_br_gr,
            "fs": fs,
            "P_mp": P_mp,
            "cumple": cumple,
            "memoria": memoria,
            "desviacion": desviacion
        }

    def evaluar_deslizamiento(self, micropilotes: Micropilotes, torre: Torre, cargas: List[float], H_min, H_max, H_paso, D_d_min, D_d_max, D_d_paso, H_relleno_min ,FSL: float) -> Tuple[float,float,bool]:
        """
        Evalua los micropilotes respecto a carga lateral
        
        Arguments:
            micropilotes {Micropilotes} -- Micropilotes a evaluar
            torre {DBFila} -- Diccionario con los datos de la torre
            cargas {List[float]} -- Conjunto de cargas (Vertical y lateral)
            H_min {float} -- 
            H_max {float} -- 
            H_paso {float} -- 
            D_d_min {float} -- 
            D_d_max {float} -- 
            D_d_paso {float} -- 
            H_relleno_min {float} -- 
            f_carga_por_torre {bool} -- 
            f_carga_mp {float} -- 
            FSL {float} -- Factor de seguridad para cargas laterales
        
        Returns:
            Tuple[float,float,bool] -- Tupla con los resultados: (capacidad, holgura, cumple)
        """   

        # Cargas
        F_am, F = cargas
            
        # Capacidades
        Q_L, memoria_q_l = micropilotes.calculo_carga_lateral(F_am)
        
        # Factores de seguridad
        fs = Q_L / F
        
        while fs < FSL:
            if micropilotes.H + H_paso <= H_max and micropilotes.D_f - (micropilotes.H + H_paso) >= H_relleno_min and micropilotes.D_d == D_d_min:
                micropilotes.H += H_paso
            else:
                break
            Q_L, memoria_q_l = micropilotes.calculo_carga_lateral(F_am)
            fs = Q_L / F
            fs = self.ajustar_fs(fs, FSL, 0.01)

        # cumple
        cumple = fs >= FSL

        if cumple:
            c_remanente = 0
        else:
            c_remanente = (F - Q_L) / micropilotes.N_m

        # Desviación
        desviacion = (FSL - fs) / FSL

        return {
            "Q_L": Q_L,
            "fs": fs,
            "c_remanente": c_remanente,
            "cumple": cumple,
            "memoria_q_l": memoria_q_l,
            "desviacion": desviacion
        }

    def evaluar_compresion_dado(self, micropilotes: Micropilotes, torre: Torre, F_m: float, FSCD: float) -> Tuple[float,bool,float,float,bool]:
        """
        Evalua la zapata respecto a la compresión
        
        Arguments:
            micropilotes {Micropilotes} -- Zapata a evaluar
            torre {DBFila} -- Diccionario con los datos de la torre
            F_m {float} -- Carga en dirección del montante
        
        Returns:
            Tuple[float,bool,float,float,bool] -- Tupla con los resultados: (holgura Qmin, cumple Qmin, Capacidad Qmax, holgura Qmax, cumple Qmax)
        """    
        # Q_med: Esfuerzo actuante promedio bajo el dado [kN/m²]
        Q_med = ((1 - micropilotes.f_carga_mp) * F_m + micropilotes.peso_dado_seco())/(micropilotes.B * micropilotes.L - micropilotes.N_m * π / 4 * micropilotes.D_s **2)

        q_ult, memoria_q_ult = micropilotes.calculo_capacidad_portante()

        if round(micropilotes.f_carga_mp,2) == 1:
            fs = None
            cumple = True
            desviacion = None
        else:        
            fs = q_ult / Q_med
            fs = self.ajustar_fs(fs, FSCD, 0.01)
            cumple = fs >= FSCD
            desviacion = (FSCD - fs) / FSCD

        # memoria
        memoria = {"Q_med": Q_med, "memoria_q_ult": memoria_q_ult}

        return {
        "q_ult": q_ult,
        "fs": fs,
        "cumple": cumple,
        "memoria": memoria,
        "desviacion": desviacion}

    def evaluar_compresion_micropilotes(self, micropilotes: Micropilotes, torre: Torre, F_m: float, FSC: float) -> Tuple[float,bool,float,float,bool]:
        """
        Evalua la zapata respecto a la compresión
        
        Arguments:
            micropilotes {Micropilotes} -- Zapata a evaluar
            parametros {DBFila} -- Diccionario con los parámetros de diseño
            torre {DBFila} -- Diccionario con los datos de la torre
            F_m {float} -- Carga en dirección del montante
        
        Returns:
            Tuple[float,bool,float,float,bool] -- Tupla con los resultados: (holgura Qmin, cumple Qmin, Capacidad Qmax, holgura Qmax, cumple Qmax)
        """ 
        F_v = F_m 

        P_permS, memoria_pperms = micropilotes.calculo_carga_compresion()

        if micropilotes.f_carga_mp == 0:
            fs = None
            cumple = True
            desviacion = None
        else:
            fs = P_permS / F_v / micropilotes.f_carga_mp
            fs = self.ajustar_fs(fs, FSC, 0.01)
            cumple = fs >= FSC
            desviacion = (FSC - fs) / FSC

        # memoria
        memoria = {**{"F_v": F_v}, **memoria_pperms}

        return {
                "P_permS": P_permS,
                "fs": fs,
                "cumple": cumple,
                "memoria": memoria,
                "desviacion": desviacion}

    def evaluar_asentamiento(self, micropilotes: Micropilotes, torre: Torre, F_zc: float, F_zc_eds: float, k: int, t: int, S_max_adm_g: float, S_max_adm_c: float, S_max_adm_r: float) -> Tuple[float,float,bool]:
        """
        Evalua la zapata respecto a la tensión (arrancamiento)
        
        Arguments:
            micropilotes {Micropilotes} -- Micropilotes a evaluar
            torre {DBFila} -- Diccionario con los datos de la torre
            F_zc {float} -- Cargas vertical compresión máxima
            F_zc_eds {float} -- Cargas vertical compresión máxima EDS
            k {int} -- Número de segmentos para análisis de asentamiento
            t {int} Número de años para corrección 'Creep'
            S_max_adm_g {float} -- Asentamiento máximo admisible para suelos granulares
            S_max_adm_c {float} -- Asentamiento máximo admisible para suelos cohesivos
            S_max_adm_r {float} -- Asentamiento máximo admisible para roca
        
        Returns:
            Tuple[float,float,bool] -- Tupla con los resultados: (asentamiento, holgura, cumple)
        """

        # Capacidad
        S_e, S_c, kv, memoria_e, memoria_c = micropilotes.calculo_asentamiento(k, F_zc, F_zc_eds, t)
        S = S_e + S_c

        D = micropilotes.D_f + 2 / 3 * micropilotes.L_b

        tipos_mat_porcen = micropilotes.perfil.calcular_porcentaje_tipo_mat(D, D + 2 * micropilotes.x)
        if tipos_mat_porcen["c"] > 0 or tipos_mat_porcen["g"] > 0:
            if tipos_mat_porcen["c"] / (tipos_mat_porcen["c"] + tipos_mat_porcen["g"]) >= 0.3:
                S_max_adm = S_max_adm_c
            else:
                S_max_adm = S_max_adm_g  
        else:
            S_max_adm = S_max_adm_r

        # Holgura
        holgura = S_max_adm - S
        
        # Cumple
        cumple = holgura >= 0

        # Desviación
        desviacion = (S - S_max_adm)/ S_max_adm

        return {
                "S_e":S_e,
                "S_c":S_c,
                "S":S,
                "kv": kv,
                "holgura":holgura,
                "cumple":cumple,
                "memoria_e":memoria_e,
                "memoria_c":memoria_c,
                "desviacion": desviacion}

    def evaluar_arrancamiento(self, micropilotes: Micropilotes, torre: Torre, F_m: float, FST: float, P_permS: float) -> Tuple[float,str,float,bool]:
        """
        Evalua la zapata respecto a la tensión (arrancamiento)
        
        Arguments:
            micropilotes {Micropilotes} -- Micropilotes a evaluar
            torre {DBFila} -- Diccionario con los datos de la torre
            F_m {float} -- Carga en dirección del montante [kN]
            FST {float} -- 
            P_permS {float} --

        Returns:
            Tuple[float,float,str,bool] -- Tupla con los resultados: (capacidad, holgura, roca_o_suelo, cumple)
        """     

        # Capacidad
        Q_ug_roca, memoria_roca, Q_ug_suelo, memoria_suelo = micropilotes.calculo_tension()

        Q_ug = min(P_permS, (Q_ug_suelo or 0) + (Q_ug_roca or 0))    

        # fs
        fs = Q_ug / F_m
        #fs = self.ajustar_fs(fs, FST, 0.01)
        fs = self.ajustar_fs(fs, FST, 0.05)

        # Cumple
        cumple = fs >= FST

        # Desviación
        desviacion = (FST - fs) / FST

        # memoria
        memoria = {"Q_ug_roca": Q_ug_roca, "Q_ug_suelo": Q_ug_suelo, "P_permS": P_permS, "memoria_suelo": memoria_suelo, "memoria_roca": memoria_roca}

        return {
                "Q_ug": Q_ug,
                "fs": fs,
                "cumple": cumple,
                "memoria": memoria,
                "desviacion": desviacion}

    def ajustar_fs(self, fs, FS, prec):
        if FS - fs > 0 and FS - fs <= prec:
            fs = FS
        return fs

    def calcular_camisa(self, micropilotes: Micropilotes, torre: Torre, P_mp, P_c):
        M_adm = micropilotes.calculo_momento_admisible()
        if torre.dh is None:
            L_c = 0.0
            L_disipa = 0.0
            cumple = True
            desviacion = -1
            M_max = 0
            V_max = 0
            d1 = 0
            prof_M_max = 0
            momentos = []
            cortantes = []
        else:
            paso = 0.1
            modulos_balastro = micropilotes.perfil.calcular_modulos_balastro(micropilotes.D_p, torre.f_c)
            momentos, cortantes, d1 = calcular_momento_flector(micropilotes.L_b, micropilotes.D_p, torre.f_c, paso, modulos_balastro, micropilotes.D_f, micropilotes.θ, torre.dh, torre.dv)
            M_max = max(max([abs(m[1]) for m in momentos]), max([abs(m[2]) for m in momentos]))
            prof_M_max = [m[0] for m in momentos if abs(m[1]) == M_max or abs(m[2]) == M_max ][0]
            V_max = max(max([abs(c[1]) for c in cortantes]), max([abs(c[2]) for c in cortantes]))
            requiere_camisa = (P_mp / P_c + M_max / M_adm) > 1
            if requiere_camisa:
                M_lim = (1 - P_mp / P_c) * M_adm
                L_disipa = calcular_longitud_camisa(momentos, M_lim)
                anclaje = next(iter([geom["anclaje"] for geom in micropilotes.barra.geoms if geom["hg"]==micropilotes.HG]))
                L_c = math.ceil((L_disipa + anclaje + 0.20) / 0.5) * 0.5
                if L_c > 3.5 or (L_c / (micropilotes.L_b + anclaje)) > 0.5:
                    cumple = False
                else:
                    cumple = True
            else:
                L_c = 0.0
                L_disipa = 0.0
                cumple = True
            if not cumple:
                desviacion = (L_c - 3.0) / 3.0 if L_c > 3.0 else (L_c / (micropilotes.L_b + anclaje) - 0.5) / 0.5
            else:
                desviacion = (L_c - 3.0) / 3.0
        return {
            "L_c": L_c,
            "L_disipa": L_disipa,
            "P_mp": P_mp,
            "M_max": M_max,
            "P_c": P_c,
            "M_adm": M_adm,
            "V_max": V_max,
            "prof_M_max": prof_M_max,
            "d1": d1,
            "momentos": momentos,
            "cortantes": cortantes,
            "cumple": cumple,
            "desviacion": desviacion
        }
        