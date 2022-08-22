import math
from typing import List, Dict, Tuple, Any
from .util import sin_g, cos_g, tan_g, cot_g, γ_agua, π, calcular_C_d, Memoria, calcular_I_f, rad
from .perfil import Perfil, Estrato

class Zapata:
    """
    Cimentación tipo zapata en suelo

    Attributes:
        B {float} -- Ancho de la zapata [m]
        L {float} -- Largo de la zapata [m]
        D {float} -- Profundidad de la zapata [m]
        H {float} -- Espesor de la zapata [m]
        C {float} -- Altura total del pedestal [m]
        TP {float} -- Lado correspondiente a la sección transversal del pedestal [m]
        θ {float} -- Ángulo del pedestal con respecto a la vertical [°]
        γ_c {float} -- Peso unitario de la zapata [kN/m³]
        perfil {Perfil} -- Perfil estratigráfico en el suelo de la zapata
        γ_r {float} -- Peso unitario del relleno [kN/m³]
        φ_r {float} -- Ángulo de fricción del relleno [°]
        α {float} -- Ángulo de inclinación de la base [°]
        ω {float} -- Ángulo de inclinación del terreno [°]
    """
    ######################################################################
    # Constructor
    ######################################################################
    def __init__(self, B:float, 
                    L:float, 
                    D:float, 
                    H:float, 
                    C:float, 
                    TP:float, 
                    θ:float, 
                    γ_c:float, 
                    perfil:Perfil, 
                    α:float, 
                    ω:float):
        """
        Inicializa la zapata
        
        Arguments:
            B {float} -- Ancho de la zapata [m]
            L {float} -- Largo de la zapata [m]
            D {float} -- Profundidad de la zapata [m]
            H {float} -- Espesor de la zapata [m]
            C {float} -- Altura total del pedestal [m]
            TP {float} -- Lado correspondiente a la sección transversal del pedestal [m]
            θ {float} -- Ángulo del pedestal con respecto a la vertical [°]
            γ_c {float} -- Peso unitario de la zapata (seco) [kN/m³]
            perfil {Perfil} -- Perfil estratigráfico en el suelo de la zapata
            α {float} -- Ángulo de inclinación de la base [°]
            ω {float} -- Ángulo de inclinación del terreno [°]
        """        
        self.B = B
        self.L = L
        self.D = D
        self.H = H
        self.C = C
        self.TP = TP
        self.θ = θ
        self.γ_c = γ_c
        self.perfil = perfil
        self.α = α
        self.ω = ω
        self.HG = self.C + self.H - self.D


        info_mat_relleno = self.perfil.calcular_material_relleno(self.D - self.H)
        self.tipo_mat_r = info_mat_relleno["tipo_mat"]
        self.φ_r = info_mat_relleno["φ"]
        self.c_u_r =info_mat_relleno["c_u"] 
        self.γ_r = info_mat_relleno["γ"]
        self.γ_r_total  = info_mat_relleno["γ_total"]

        self.validar_atributos()

        self.ajustar_perfil()

    ######################################################################
    # Utilitarios
    ######################################################################
    def validar_atributos(self):
        #   - Obligatoriedad
        #   - Tipos y dominios
        #   - Restricciones en el perfil 
        pass

    def get_atributos(self, *nombres: str) -> Tuple:
        """Retorna los atributos solicitados como una tupla"""

        return (self.__dict__[nombre] for nombre in nombres)

    def volumen(self) -> float:
        """
        Calcula el volumen de la zapata.

        Returns:
            float -- Volumen de la zapata [m³]
        """
        B, L, H, C, TP, θ = self.get_atributos("B", "L", "H", "C", "TP", "θ")

        return B * L * H + TP**2 * C / cos_g(θ)

    def peso_seco(self) -> float:
        """
        Calcula el peso de la zapata con el peso unitario del concreto seco.

        Returns:
            float -- Peso de la zapata [kN]
        """
        γ_c,  = self.get_atributos("γ_c")

        return self.volumen() * γ_c

    def peso_efectivo(self) -> float:
        """
        Calcula el peso de la zapata con el peso unitario del concreto ajustado según saturación.

        Returns:
            float -- Peso de la zapata [kN]
        """
        γ_c, D, perfil  = self.get_atributos("γ_c", "D", "perfil")
        
        NF = perfil.calcular_NF()
        if NF is not None and NF < D:
            γ_c -= γ_agua
 
        return self.volumen() * γ_c        

    def volumen_relleno(self) -> float:
        """
        Calcula el volumen del relleno.

        Returns:
            float -- Volumen del relleno [m³]
        """
        B, L, D, H, TP, θ  = self.get_atributos("B", "L", "D", "H", "TP", "θ")

        return B * L * (D - H) - TP**2 * (D - H) / cos_g(θ)

    def peso_relleno_efectivo(self) -> float:
        """
        Calcula el peso del relleno.

        Returns:
            float -- Peso del relleno [kN]
        """
        γ_r,  = self.get_atributos("γ_r")

        return self.volumen_relleno() * γ_r

    def peso_relleno_seco(self) -> float:
        """
        Calcula el peso del relleno con el peso unitario seco del relleno .

        Returns:
            float -- Peso del relleno [kN]
        """
        γ_r,  = self.get_atributos("γ_r_total")

        return self.volumen_relleno() * γ_r

    def set_perfil(self, perfil: Perfil):
        self.perfil = perfil
        info_mat_relleno = self.perfil.calcular_material_relleno(self.D - self.H)
        self.tipo_mat_r, self.φ_r, self.c_u_r, self.γ_r  = (info_mat_relleno["tipo_mat"], info_mat_relleno["φ"], info_mat_relleno["c_u"], info_mat_relleno["γ"])     

    def ajustar_a_0_005(self, s):
        s_cm = math.floor(s * 100) / 100
        s_resto = s - s_cm
        if round(s_resto,3) < 0.005:
            return round(s_cm,3)
        elif s_resto < 0.007:
            return round(s_cm + 0.005,3)
        else:
            return round(s_cm + 0.01,3)

    def ajustar_perfil(self):
        B, D, perfil  = self.get_atributos("B", "D", "perfil")

        estrato_en_D = perfil.estrato_en(D + 0.01)

        B_lim = None
        if estrato_en_D.tipo_mat == "r":
            B_lim = 0
        else:
            # φ_D: Ángulo de fricción para calcular el límite inferior del 
            # suelo relevante para el cálculo de capacidad portante [°]
            φ_D = estrato_en_D.φ_s

            # B_lim: límite inferior del suelo relevante para
            # el cálculo de capacidad portante [m]
            B_lim = B * tan_g(45 + φ_D / 2.0)   

        # Para el cálculo del asentamiento se requiere D + 2 * B
        # y para el cálculo de capacidad portante D + B_lim
        profundidad_minima_requerida = D + max(2 * B, B_lim)

        prof_perfil = perfil.calcular_profundidad_total()

        # Se ajusta el último estrato si el perfil no alcanza la profundidad mínima requerida
        if prof_perfil < profundidad_minima_requerida:
            perfil[-1].H_0 +=  profundidad_minima_requerida - sum([estrato.H_0 for estrato in perfil])
            perfil[-1].prof_fin += profundidad_minima_requerida - sum([estrato.H_0 for estrato in perfil])

    ######################################################################
    # Cálculos capacidad portante (2.1)
    ######################################################################
    def calculo_capacidad_portante(self, T:float, F_zc:float) -> Tuple[float, Memoria]:

        B, D, perfil  = self.get_atributos("B", "D", "perfil")

        estrato_en_D = perfil.estrato_en(D + 0.01)

        if estrato_en_D.tipo_mat == "r":
            # Zapata em roca
            q_ult = 1.25 * math.sqrt(estrato_en_D.roca_s) * estrato_en_D.ucs * 1000 * (1 + math.sqrt(estrato_en_D.roca_m / math.sqrt(estrato_en_D.roca_s) + 1))
            return (q_ult,  {"tipo_mat": "r", "γ": estrato_en_D.roca_γ, "φ": estrato_en_D.roca_φ_rm}) 

        # φ_D: Ángulo de fricción para calcular el límite inferior del suelo relevante [°]
        φ_D = estrato_en_D.φ_s

        # B_lim: límite inferior del suelo relevante [m]
        B_lim = B * tan_g(45 + φ_D / 2)      
        
        # Porcentajes de tipos de material de suelo entre D y D + B_lim
        porcentajes = perfil.calcular_porcentaje_tipo_mat(D, D + B_lim)

        if porcentajes["c"] /(porcentajes["c"] + porcentajes["g"]) >= 0.3:
            return self.calculo_capacidad_portante_suelos_cohesivos(T, F_zc)
        else:
            return self.calculo_capacidad_portante_suelos_granulares(T, F_zc)

    def calculo_capacidad_portante_suelos_granulares(self, T:float, F_zc:float) -> Tuple[float, Memoria]:  
        """
        Calcula las capacidad portante última en suelos granulares (condición drenada).
        
        Arguments:
            T {float} -- Carga lateral (la mayor entre la carga Transversal y la Longitudinal) [kN]
            F_zc:  {float} -- Componente vertical de la carga a compresión [kN].

        Returns:
            Tuple[float, Memoria] -- (q_ult: Capacidad portante última [kN/m²], memoria)
        """
        B, L, D, HG, θ, perfil, α, ω  = self.get_atributos("B", "L", "D", "HG", "θ", "perfil", "α", "ω")

        # q: Esfuerzo de sobrecarga efectivo a la profundidad de cimentación [kN/m²]
        q = perfil.calcular_q(D)

        # W_p: Peso de la cimentación [kN]
        W_p = self.peso_seco()

        # W_r: Peso del relleno [kN]
        W_r = self.peso_relleno_seco()

        # F_vc: Carga total de compresión a nivel de fundación [kN]
        F_vc = F_zc + W_p + W_r

        # φ_D: Ángulo de fricción para calcular el límite inferior del suelo relevante [°]
        φ_D = perfil.estrato_en(D).φ_s

        # B_lim: límite inferior del suelo relevante [m]
        B_lim = B * tan_g(45 + φ_D / 2)

        # φ: Ángulo de fricción del suelo relevante [°]
        φ = perfil.calcular_promedio(D, D + B_lim, "φ_s", tipo_mat="g")

        # M: Momento en la base [kN·m]
        # ML, _ = self.calculo_momento_carga_lateral(T)
        ML = T * (D + HG)
        MX = self.calculo_momento_carga_axial(F_zc)
        M = ML + MX

        # N_q: Factor de capacidad portante debido a la sobrecarga. [-]
        N_q = math.exp(π * tan_g(φ)) * tan_g(45 + φ / 2)**2

        # N_γ: Factor de capacidad portante debido al peso unitario del suelo de fundación. [-]
        N_γ = 2 * (N_q + 1) * tan_g(φ)

        # φ_rel: Ángulo de fricción relativo [-]
        φ_rel = (φ - 25) / 20

        # ν: Relación de Poisson [-]
        ν = 0.1 + 0.3 * φ_rel

        # E: Módulo de Young para la prfundidad D [kN/m²]
        E = perfil.calcular_promedio(D, D + B_lim, 'E_s')
        
        # I_r: Índice de rigidez [-]
        I_r = E / 2 / (1 + ν) / q / tan_g(φ)

        # ∆: Deformación volumétrica [-]
        Δ = 0.005 * q * 0.0093238 * (1 - φ_rel)

        # I_rr: Índice de rigidez reducido [-]
        I_rr = I_r/(1 + I_r * Δ)

        # I_rc: Índice de rigidez crítico [-]
        I_rc = 1 / 2 * math.exp(3.30 - 0.45 * B / L) * cot_g(45 - φ / 2)

        # n: Exponente del factor de corrección por inclinación [-]
        n = (2 + L / B) / (1 + L / B) * cos_g(θ)**2 + (2 + L / B) / (1 + L / B) * sin_g(θ)**2

        # e: Excentricidad por momento [m]
        e = abs(M / F_vc)

        # B_p: Dimensión reducida de B debido a carga excéntrica [m]
        B_p = B - 2 * e

        # L_p: Dimensión reducida de L debido a carga excéntrica [m]
        L_p = L - 2 * e

        # ξ_γs, ξ_qs: Factores de corrección por Forma [-]
        ξ_γs = 1 - 0.4 * (B / L)
        ξ_qs = 1 + (B / L) * tan_g(φ)

        # ξ_γd, ξ_qd: Factores de corrección por Profundidad [-]
        ξ_γd = 1
        if D / B <= 1:
            ξ_qd = 1 + 2 * tan_g(φ) * (1 - sin_g(φ))**2 * (D / B)
        else:
            ξ_qd = 1 + 2 * tan_g(φ) * (1 - sin_g(φ))**2 * math.atan2(D, B)

        # ξ_qr, ξ_γr: Factores de corrección por Rigidez [-]
        if I_rr > I_rc:
            ξ_qr = 1
            ξ_γr = 1
        else:        
            ξ_qr = math.exp((-4.4 + 0.6 * (B / L)) * tan_g(φ) + (3.07 * sin_g(φ) * math.log10(2 * I_rr)/(1 + sin_g(φ))))
            ξ_γr = ξ_qr

        # c_p: Cohesión efectiva del suelo [kN/m²]
        c_p = perfil.calcular_promedio(0, D, "c_p", tipo_mat="g")
        if c_p is None:
            c_p = 0

        # ξ_γi, ξ_qi: Factores de corrección por Inclinación de la carga [-]
        ξ_γi = (1 - T / (F_vc + B_p * L_p * c_p * cot_g(φ)))**(n + 1)
        ξ_qi = (1 - T / (F_vc + B_p * L_p * c_p * cot_g(φ)))**(n)

        # ξ_γt, ξ_qt: Factores de corrección por Inclinación en la base [-]
        ξ_γt = (1 - rad(α) * tan_g(φ))**2
        ξ_qt = ξ_γt

        # ξ_γg, ξ_qg: Factores de corrección por Pendiente de la superficie del terreno [-]
        ξ_qg = (1 - tan_g(min(φ / 2, ω)))**2
        ξ_γg = ξ_qg

        # γ: Peso unitario promedio del suelo en D a D + B_lim [kN/m³]
        γ = perfil.calcular_promedio(D, D + B_lim, 'γ_se')
        
        # q_ult: Capacidad portante última [kN/m²]
        q_ult = 1 / 2 * B_p * γ * N_γ * ξ_γs * ξ_γd * ξ_γr * ξ_γi * ξ_γt * ξ_γg + q * N_q * ξ_qs * ξ_qd * ξ_qr * ξ_qi * ξ_qt * ξ_qg

        # memoria de cálculo
        memoria = {"tipo_mat": "g", "q":q, "W_p":W_p, "F_vc":F_vc, "γ": γ, "φ":φ, "e": e, "B_p": B_p, "L_p": L_p, "N_q":N_q, "N_γ":N_γ, "ν":ν, "E":E, "I_rr":I_rr, "I_rc":I_rc, "ξ_γs":ξ_γs, "ξ_γd":ξ_γd, "ξ_γr":ξ_γr, "ξ_γi":ξ_γi, "ξ_γt":ξ_γt, "ξ_γg":ξ_γg, "ξ_qs":ξ_qs, "ξ_qd":ξ_qd, "ξ_qr":ξ_qr, "ξ_qi":ξ_qi, "ξ_qt":ξ_qt, "ξ_qg":ξ_qg}

        return (q_ult, memoria)

    def calculo_capacidad_portante_suelos_cohesivos(self, T:float, F_zc:float) -> Tuple[float, Memoria]:
        """
        Calcula las capacidad portante en suelos cohesivos (condición no drenada).
        
        Arguments:
            T {float} -- Carga lateral [kN]
            F_zc {float} -- Componente vertical de la carga a compresión [kN]
        
        Returns:
            Tuple[float, Memoria] -- (q_ult: Capacidad portante última [kN/m²], memoria)
        """ 
        B, L, D, HG, θ, perfil, α, ω  = self.get_atributos("B", "L", "D", "HG", "θ", "perfil", "α", "ω")

        # W_p: Peso de la cimentación [kN]
        W_p = self.peso_seco()

        # W_r: Peso del relleno [kN]
        W_r = self.peso_relleno_seco()

        # F_vc: Carga total de compresión a nivel de fundación [kN]
        F_vc = F_zc + W_p + W_r        

        # φ_D: Ángulo de fricción para calcular el límite inferior del suelo relevante [°]
        φ_D = perfil.estrato_en(D).φ_s

        # B_lim: límite inferior del suelo relevante [m]
        B_lim = B * tan_g(45 + φ_D / 2)

        # M: Momento en la base [kN·m]
        # ML, _ = self.calculo_momento_carga_lateral(T)
        ML = T * (D + HG)
        MX = self.calculo_momento_carga_axial(F_zc)
        M = ML + MX

        # e: Excentricidad por momento [m]
        e = abs(M / F_vc)

        # B_p: Dimensión reducida de B debido a carga excéntrica [m]
        B_p = B - 2 * e

        # L_p: Dimensión reducida de L debido a carga excéntrica [m]
        L_p = L - 2 * e

        # n: Exponente del factor de corrección por inclinación [-]
        n = (2 + L / B) / (1 + L / B) * cos_g(θ)**2 + (2 + L / B) / (1 + L / B) * sin_g(θ)**2

        # c_u: Resistencia no drenada [kN/m²]
        c_u = perfil.calcular_promedio(D, D + B_lim, "c_u", tipo_mat="c")

        # E: Módulo de Young para la prfundidad D [kN/m²]
        E = perfil.calcular_promedio(D, D + B_lim, "E_s")

        # I_r: Índice de rigidez [-]
        I_r = E / 3 / c_u

        # I_r: Índice de rigidez reducido [-]
        I_rr = I_r

        # I_rc: Índice de rigidez crítico [-]
        I_rc = 1 / 2 * math.exp(3.30 - 0.45 * B / L)

        # q: Esfuerzo de sobrecarga total a la profundidad de cimentación D [kN/m²]
        q = perfil.calcular_q_con_γ_s(D)

        # ξ_cs, ξ_qs: Factores de corrección por Forma [-]
        ξ_cs = 1 + 0.2 * (B / L)
        ξ_qs = 1

        # ξ_cd, ξ_qd: Factores de corrección por Profundidad [-]
        if D / B <= 1:
            ξ_cd = 1 + 0.4 * (D / B)
        else:
            ξ_cd = 1 + 0.4 * math.atan2(D, B)
        ξ_qd = 1

        # ξ_cr, ξ_qr: Factores de corrección por Rigidez [-]
        if I_rr > I_rc:
            ξ_cr = 1
            ξ_qr = 1
        else:
            ξ_cr = 0.32 + 0.12 * (B / L) + 0.60 * math.log10*(I_rr)
            ξ_qr = 1

        # ξ_ci, ξ_qi: Factores de corrección por Inclinación de la carga [-]
        ξ_ci = 1 - n * T / (5.14 * c_u * B_p * L_p)
        ξ_qi = (1 - T / F_vc)**n

        # ξ_ct, ξ_qt: Factores de corrección por Inclinación de la base [-]
        ξ_ct = 1 - 2 * rad(α) / (2 + π)
        ξ_qt = 1

        # ξ_cg, ξ_qg: Factores de corrección por Pendiente de la superficie del terreno [-]
        ξ_cg = 1 - 2 * rad(ω) / (2 + π)
        ξ_qg = 1

        # N_c: Factor de capacidad portante debido a la cohesión. [-]
        N_c = 5.14

        # N_q: Factor de capacidad portante debido a la sobrecarga. [-]
        N_q = 1

        # q_ult: Capacidad portante última. [kN/m²]
        q_ult = N_c * c_u * ξ_cs * ξ_cd * ξ_cr * ξ_ci * ξ_ct * ξ_cg + q * N_q * ξ_qs * ξ_qd * ξ_qr * ξ_qi * ξ_qt * ξ_qg

        # γ: Peso unitario promedio del suelo en D a D + B_lim [kN/m³]
        γ = perfil.calcular_promedio(D, D + B_lim, 'γ_s')

        # memoria de cálculo
        memoria = {"tipo_mat": "c", "e":e, "B_p":B_p, "L_p":L_p, "n":n, "γ": γ, "c_u":c_u, "E":E, "I_r":I_r, "I_rr":I_rr, "I_rc":I_rc, "N_c": N_c, "N_q": N_q, "N_γ": 0, "q":q, "ξ_cs":ξ_cs, "ξ_qs":ξ_qs, "ξ_cd":ξ_cd, "ξ_qd":ξ_qd, "ξ_cr":ξ_cr, "ξ_qr":ξ_qr, "ξ_ci":ξ_ci, "ξ_qi":ξ_qi, "ξ_ct":ξ_ct, "ξ_qt":ξ_qt, "ξ_cg":ξ_cg, "ξ_qg":ξ_qg}

        return (q_ult, memoria)

    ######################################################################
    # Cálculos capacidad de carga al arrancamiento (2.2)
    ######################################################################
    def calculo_tension(self, q_adm:float) -> Tuple[float, Memoria]:
        """
        Calcula las capacidad a la tensión
        
        Arguments:
            q_adm {float} -- Capacidad admisible del suelo [kg/cm²]

        Returns:
            Tuple[float, Memoria] -- (T_u: Capacidad a la tensión última [kN], memoria)
        """
        D, perfil = self.get_atributos("D", "perfil")

        # tipo_mat_predominante
        tipo_mat_predominante = perfil.calcular_tipo_mat_predominante(0, D)
        
        # Capacidad
        if tipo_mat_predominante == "g":
            return self.calculo_tension_cono_tierra_suelos_granulares(q_adm)
        elif tipo_mat_predominante == "c":
            return self.calculo_tension_meyerhof_adams_suelos_cohesivos()

    def calculo_tension_cono_tierra_suelos_granulares(self, q_adm:float) -> Tuple[float, Memoria]:
        """
        Calcula las capacidad a la tensión con el método del cono de tierra para suelos granulares  (condición drenada).
        
        Arguments:
            q_adm {float} -- Capacidad admisible del suelo [kg/cm²]

        Returns:
            Tuple[float, Memoria] -- (T_u: Capacidad a la tensión última [kN], memoria)
        """
        B, L, D, H, TP, θ, perfil, γ_r  = self.get_atributos("B", "L", "D", "H", "TP", "θ", "perfil", "γ_r")

        # W_f: Peso de la cimentación [kN]
        W_f = self.peso_efectivo()

        # V_0: Volumen de la fundación bajo la superficie del terreno [m³]
        V_0 = B * L * H + TP**2 * (D - H) / cos_g(θ)

        # V_1: Área de la base por la profundidad [m³]
        V_1 = B * L * D

        # NF: Nivel freático [m]
        NF = perfil.calcular_NF()
        
        # ψ: Ángulo de inclinación de las paredes del cono [°]
        if NF == None or NF >= D:     # Seco
            if q_adm >=  98.066:               # 1 kg/cm²
                ψ = 30
            else:
                ψ = 20
        elif NF < D:                 # Semi-sumergido
            if q_adm >=  98.066:
                ψ_seco = 30
            else:
                ψ_seco = 20
            ψ = ((D - NF) * 15 + NF * ψ_seco) / D
            γ_r = ((D - NF) * 10 + NF * γ_r) / D

        # γ: Peso unitario promedio del suelo hasta la profundidad D [kN/m³]
        NF = perfil.calcular_NF()
        if NF is not None and NF < D:
            γ_r = 10 # γ_agua

        γ = perfil.calcular_promedio_γ(D)

        # W_s: Peso del suelo dentro de la superficie de falla [kN] 
        W_s = γ_r * (V_1 - V_0) + 1 / 6 * γ * D**2 * tan_g(ψ) * (12 * B + 8 * D * tan_g(ψ))

        # T_u: Capacidad al arranque [kN]
        T_u = W_f + W_s

        # memoria
        memoria = {"tipo_mat": "g", "W_f":W_f, "V_0":V_0, "V_1":V_1, "ψ":ψ, "γ":γ, "W_s":W_s}

        return (T_u, memoria)

    def calculo_tension_meyerhof_adams_suelos_cohesivos(self) -> Tuple[float, Memoria]:
        """
        Calcula la capacidad a la tensión con el método de Meyerhof y Adams para suelos cohesivos (condición no drenada).
        
        Returns:
            Tuple[float, Memoria] -- (T_u: Capacidad a la tensión última [kN], memoria)
        """
        B, L, D, perfil  = self.get_atributos("B", "L", "D", "perfil")

        # c_p: Cohesión efectiva del suelo [kN/m²]
        c_p = perfil.calcular_promedio(0, D, "c_p")

        # W_s: Peso del suelo contenido en los planos de corte [kN]
        W_s = self.peso_relleno_efectivo()

        # W_f: Peso de la cimentación [kN]
        W_f = self.peso_efectivo()

        # φ: Ángulo de fricción del suelo [°]
        φ = perfil.calcular_promedio(0, D, "φ_s", tipo_mat="c")
        
        # K_u: Coeficiente nominal de presión de tierras para arrancamiento en la superficie de ruptura [-]
        K_u = 0.496 * φ ** 0.18

        # M: Factor para cálculo de S_f [-], depende del rango de φ
        # S_f_max: Factor de forma máximo [-], depende del rango de φ
        if 0 < φ <= 20:
            M = 0.05
            S_f_max = 1.12    
        elif 20 < φ <= 25:
            M = 0.10
            S_f_max = 1.30    
        elif 25 < φ <= 30:
            M = 0.15
            S_f_max = 1.60    
        elif 30 < φ <= 35:
            M = 0.25
            S_f_max = 2.25    
        elif 35 < φ <= 40:
            M = 0.35
            S_f_max = 3.45    
        elif 40 < φ <= 45:
            M = 0.50
            S_f_max = 5.50
        elif 45 < φ <= 48:
            M = 0.60
            S_f_max = 7.60    

        # S_f: Factor de forma [-]
        S_f =  min(1 + M * D / B, S_f_max)

        # γ_s:  Peso unitario promedio del suelo hasta la profundidad D [kN/m³]
        γ_s = perfil.calcular_promedio_γ(D)

        # T_u: Capacidad al arranque [kN]
        T_u = W_s + W_f + 2 * c_p * D * (B + L) + γ_s * D**2 * (2 * S_f * B + L - B) * K_u * tan_g(φ)

        # memoria
        memoria = {"tipo_mat": "c", "W_s":W_s, "W_f":W_f, "φ":φ, "K_u":K_u, "M":M, "S_f_max":S_f_max, "S_f":S_f, "γ_s":γ_s}
        
        return (T_u, memoria)

    ######################################################################
    # Cálculos asentamientos (2.3)
    ######################################################################
    def calculo_asentamiento(self, k:int, F_zc:float, F_zc_eds:float, t:float) -> Tuple[float, Tuple[Memoria, Memoria]]:
        """
        Calcula el asentamiento

        Arguments:
            k {int} -- Número de capas para el análisis de asentamiento [-]
            F_vc {float} -- Componente vertical de la carga a compresión [kN]
            t {float} -- Tiempo en años para el cálculo del "Creep"

        Returns:
            Tuple[float, Tuple[Memoria,Memoria]] -- (S: Asentamiento [m], memoria elástica, memoria consolidación)
        """
        B, D, perfil = self.get_atributos("B", "D", "perfil")

        # tipo de material     
        tipos = perfil.calcular_tipo_mat_distintos(D, D + 2 * B)
        tipos = [t for t in tipos if t != "r"]

        # Capacidad
        if len(tipos) == 1:
            if tipos[0] == "c":
                S_e, memoria_e = self.calculo_asentamiento_elastico_suelos_cohesivos(F_zc)
                S_c, memoria_c = self.calculo_asentamiento_por_consolidacion(F_zc_eds)
                S_e = self.ajustar_a_0_005(S_e) # se ajustan los asentamientos a la precisión 0.5cm (a la izq de 0.5 floor, a la derecha round)
                S_c = self.ajustar_a_0_005(S_c)
                return (S_e, S_c, memoria_e, memoria_c)
            elif tipos[0] == "g":
                S_e, memoria_e = self.calculo_asentamiento_elastico_suelos_granulares(k, F_zc, t)
                S_e = self.ajustar_a_0_005(S_e) # se ajustan los asentamientos a la precisión 0.5cm (a la izq de 0.5 floor, a la derecha round)
                return (S_e, 0, memoria_e, None)
        elif len(tipos) == 2: # Mixto: Cohesivo y granular
            S_e, memoria_e = self.calculo_asentamiento_elastico_suelos_mixtos(F_zc, k, t)
            S_c, memoria_c = self.calculo_asentamiento_por_consolidacion(F_zc_eds)
        else: # Solo roca
            S_e, memoria_e = 0, {}
            S_c, memoria_c = 0, None
        
        # se ajustan los asentamientos a la precisión 0.5cm (a la izq de 0.5 floor, a la derecha round)
        S_e = self.ajustar_a_0_005(S_e)
        S_c = self.ajustar_a_0_005(S_c)
        
        return S_e, S_c, memoria_e, memoria_c

    def calculo_asentamiento_elastico_suelos_granulares(self, k:float, F_zc:float, t:float) -> Tuple[float, Memoria]:
        """
        Calcula el asentamiento siguiendo la expresión de Schmertman para suelos granulares (condición drenada). Se
        incluye la roca en el análisis, dado que su módulo está involucrado en el cálculo.

        Arguments:
            k {int} -- Número de capas para el análisis de asentamiento [-]
            F_vc {float} -- Componente vertical de la carga a compresión [kN]
            t {float} -- Tiempo en años para el cálculo del "Creep"

        Returns:
            Tuple[float, Memoria] -- (S: Asentamiento [m], memoria)
        """
        B, L, D, perfil = self.get_atributos("B", "L", "D", "perfil")

        # W_c: Peso de la cimentación [kN]
        W_c = self.peso_seco()

        # W_c: Peso deL relleno [kN]
        W_r = self.peso_relleno_seco()
        
        # q_0: Magnitud de la presión transmitida al suelo de fundación [kN/m²]
        q_0 = (F_zc + W_c + W_r) / B / L

        # σ_0f: Esfuerzo vertical efectivo inicial al nivel de fundación [kN/m²]
        σ_0f = perfil.calcular_q(D)

        # C_1: Factor de corrección por profundidad de la fundación [-]
        C_1 = 1 - 0.5 * σ_0f / q_0

        # C_2: Factor de corrección por “Creep” [-]
        C_2 = 1 + 0.20 * math.log10(t / 0.10)

        # Z: Lista con las profundidades para el cálculo de I_z (a mitad del segmento) [m]
        Z = [D + 2 * B / k * i + B / k for i in range(k)]

        # dz: Espesor de la capa de análisis [m]
        dz =  2 * B / k

        # S: Asentamiento [m]
        S = C_1 * C_2 * q_0 * dz * sum([self.interpolar_Iz_elastico(z - D) / perfil.estrato_en(z).E_s for z in Z if perfil.estrato_en(z).tipo_mat != "r"])

        # memoria
        memoria = {"tipo_mat": "g", "W_c":W_c, "W_r":W_r, "q_0":q_0, "σ_0f":σ_0f, "C_1":C_1, "C_2":C_2, "Z":Z, "dz":dz}

        return (S, memoria)

    def calculo_asentamiento_elastico_suelos_cohesivos(self, F_zc:float) -> Tuple[float, Memoria]:
        B, L, D, perfil = self.get_atributos("B", "L", "D", "perfil")

        # W_c: Peso de la cimentación [kN]
        W_c = self.peso_seco()

        # W_c: Peso deL relleno [kN]
        W_r = self.peso_relleno_seco()

        # q_0: Magnitud de la presión transmitida al suelo de fundación [kN/m²]
        q_0 = (F_zc + W_c + W_r) / B / L

        # S_ec : Asentamiento en elástico en suelo cohesivo [m]
        z = 0.0
        S_ec = 0.0
        Δz_acum = 0.0
        M = L / B
        α_cd = 4 # El incremento se hace para 4 zapatas de ancho B/2
        prof_ini = D
        prof_roca = perfil.calcular_profundidad_hasta_roca() 
        prof_fin = min(prof_roca, D + 2 * B) if prof_roca is not None else D + 2 * B
        iteraciones = []
        for estrato in perfil:
            if z + estrato.H_0 > prof_ini and z < prof_fin:
                if estrato.tipo_mat == "c":
                    E_s = estrato.E_s
                    ν = estrato.ν
                    if z < prof_ini:
                        if z + estrato.H_0 < prof_fin:
                            Δz = z + estrato.H_0 - prof_ini
                        else:
                            Δz = prof_fin - prof_ini
                    else:
                        if z + estrato.H_0 < prof_fin:
                            Δz = estrato.H_0
                        else:
                            Δz = prof_fin - z
                    Δz_acum += Δz
                    N = Δz_acum / B
                    I_1 = 1 / π * (M * math.log((1 + math.sqrt(M**2 + 1) * math.sqrt(M**2 + N**2))/ M / (1 + math.sqrt(M**2 + N**2 + 1))) + \
                                    math.log((M + math.sqrt(M**2 + 1) * math.sqrt(1 + N**2))/(M + math.sqrt(M**2 + N**2 + 1))))
                    I_2 = N / 2 / π * math.atan2(M, N * math.sqrt(M**2 + N**2 + 1))
                    I_p = I_1 + (1 - 2 * ν) / (1 - ν) * I_2
                    I_f = calcular_I_f(ν, Δz/B)
                    C_d = 1 / 2 * α_cd * I_p * I_f
                    S_ec += q_0 * B * C_d * (1 - ν**2) / E_s
                    iteraciones.append({"z":z, "Δz_acum":Δz_acum, "E_s":E_s, "ν":ν, "N":N, "I_1":I_1, "I_2":I_2, "I_p":I_p, "I_f":I_f, "C_d":C_d, "S_ec":S_ec})
            elif z >= prof_fin:
                break
            
            z += estrato.H_0

        # memoria
        memoria = {"tipo_mat": "c", "W_c":W_c, "W_r":W_r, "q_0":q_0, "M":M, "α_cd":α_cd, "iteraciones": iteraciones}

        return (S_ec, memoria)

    def calculo_asentamiento_elastico_suelos_mixtos(self, F_zc:float, k: int, t:float) -> Tuple[float, Memoria]:
        B, L, D, perfil = self.get_atributos("B", "L", "D", "perfil")

        # W_c:  Peso de la cimentación [kN]
        W_c = self.peso_seco()
        
        # W_r:  Peso del relleno [kN]
        W_r = self.peso_relleno_seco()

        # q_0: Cargas verticales [kN]
        q_0 = (F_zc + W_c + W_r) / B / L

        # σ_0f: Esfuerzo vertical efectivo inicial al nivel de fundación [kN/m²]
        σ_0f = perfil.calcular_q(D)

        # C_1: Factor de corrección por profundidad de la fundación [-]
        C_1 = 1 - 0.5 * σ_0f / q_0

        # C_2: Factor de corrección por “Creep” [-]
        C_2 = 1 + 0.20 * math.log10(t / 0.10)

        # S_e: Asentamiento [m]
        S_e = 0.0
        S_e_g = 0.0
        S_e_c = 0.0
        z = 0.0  # prof. ini de capa actual

        prof_ini = D
        prof_roca = perfil.calcular_profundidad_hasta_roca() 
        prof_fin = min(prof_roca, D + 2 * B) if prof_roca is not None else D + 2 * B
        H_ant = 0.0
        H = 0.0
        iteraciones = []
        for estrato in perfil:
            if z + estrato.H_0 > prof_ini and z < prof_fin:
                # Δz
                if z < prof_ini:
                    if z + estrato.H_0 < prof_fin:
                        Δz = z + estrato.H_0 - prof_ini
                    else:
                        Δz = prof_fin - prof_ini
                else:
                    if z + estrato.H_0 < prof_fin:
                        Δz = estrato.H_0
                    else:
                        Δz = prof_fin - z
                H += Δz
                if estrato.tipo_mat == "g":                    
                    ΔS     = self.asentamiento_incremental_granular(H, estrato, q_0, C_1, C_2, k)
                    ΔS_ant = self.asentamiento_incremental_granular(H_ant, estrato, q_0, C_1, C_2, k)
                    S_e_g += ΔS - ΔS_ant
                elif estrato.tipo_mat == "c":
                    ΔS =     self.asentamiento_incremental_cohesivo(H, estrato, q_0)
                    ΔS_ant = self.asentamiento_incremental_cohesivo(H_ant, estrato, q_0)
                    S_e_c += ΔS - ΔS_ant
                S_e += ΔS - ΔS_ant
                iteraciones.append({"H": H, "H_ant": H_ant, "S_e": S_e, "ΔS": ΔS, "ΔS_ant": ΔS_ant, "estrato": estrato.__dict__})
            elif z > prof_fin:
                break
            H_ant = H
            z += estrato.H_0

        # memoria
        memoria = {"tipo_mat": "m", "W_c":W_c, "W_r":W_r, "q_0":q_0, "σ_0f":σ_0f, "C_1":C_1, "C_2":C_2, "S_e_g": S_e_g, "S_e_c": S_e_c, "iteraciones": iteraciones}

        return (S_e, memoria)
    
    def asentamiento_incremental_granular(self, H: float, estrato: Estrato, q_0: float, C_1: float, C_2: float, k: int):
        if H == 0:
            return 0

        # Z: Lista con las profundidades para el cálculo de I_z (a mitad del segmento) [m]
        Z = [H / k / 2 + i * H / k for i in range(k)]

        # dz: Espesor de la capa de análisis [m]
        dz =  H / k

        # S: Asentamiento [m]
        S = C_1 * C_2 * q_0 * dz * sum([self.interpolar_Iz_elastico(z) / estrato.E_s for z in Z])

        return S

    def asentamiento_incremental_cohesivo(self, H: float, estrato: Estrato, q_0: float):
        if H == 0:
            return 0
        B, = self.get_atributos("B")
        C_d = calcular_C_d(H, B)
        return C_d * q_0 * B * (1 - estrato.ν**2) / estrato.E_s

    def calculo_asentamiento_por_consolidacion(self, F_zc:float) -> Tuple[float, Memoria]:
        """
        Calcula el asentamiento por consolidación

        Arguments:
            F_vc {float} -- Componente vertical de la carga a compresión [kN]
        
        Returns:
            Tuple[float, Memoria] -- (S: Asentamiento [m], memoria)
        """
        B, L, D, perfil = self.get_atributos("B", "L", "D", "perfil")

        # W_c:  Peso de la cimentación [kN]
        W_c = self.peso_relleno_seco()
        
        # W_c:  Peso del relleno [kN]
        W_r = self.peso_relleno_seco()

        # q_0: Cargas verticales [kN]
        q_0 = (F_zc + W_c + W_r) / B / L

        # d: Profundidad actual del loop de acumulación
        d = 0.0
        S_c = 0.0

        # memoria de cada iteracion
        iteraciones = []
        for estrato in perfil:
            if d + estrato.H_0 > D and d < D + 2 * B:
                if estrato.tipo_mat == "c" and estrato.saturado:
                    # H_c: Espesor de estrato compresible [m]
                    if d < D:
                        if d + estrato.H_0 > D + 2 * B:
                            H_c = 2 * B
                        else:
                            H_c = d + estrato.H_0 - D
                    elif d + estrato.H_0 > D + 2 * B:
                        H_c = D + 2 * B - d
                    else:
                        H_c = estrato.H_0
                    
                    # z: Profundidad desde D de evaluación de Iz para el estrato [m]
                    
                    if d < D:
                        z = H_c / 2
                    else:
                        z = d + H_c / 2 - D

                    # M, N, V, V_1: Factores para el cálculo de I_z (Newmark)
                    M = B / 2 / z
                    N = L / 2 / z
                    V = M**2 + N**2 + 1
                    V_1 = (M * N)**2

                    # I_z: Factor de influencia de la deformación unitaria
                    I_z = 1 / 4 / π *( 2 * M * N * math.sqrt(V) / (V + V_1) * (V + 1) / V  + math.atan2(2 * M * N * math.sqrt(V), V - V_1))

                    # Δσ_p: Incremento de esfuerzo vertical efectivo [kN/m²]
                    Δσ_p = 4 * q_0 * I_z

                    # σ_0p: Esfuerzo vertical efectivo inicial [kN/m²]
                    σ_0p = perfil.calcular_q(z + D)

                    # # estrato: Estrato en la profundidad z
                    # estrato = perfil.estrato_en(z + D)

                    # C_c: Coeficiente de compresibilidad, corresponde a la pendiente de la curva e-log⁡σ' del ensayo de consolidación durante la etapa de carga [-]
                    C_c = estrato.C_c

                    # C_s: Coeficiente de descarga, corresponde a la pendiente de la curva e-log⁡σ' del ensayo de consolidación durante la etapa de descarga.  [-]
                    C_s = estrato.C_s

                    # e_0: Relación de vacíos inicial [-]
                    e_0 = estrato.e_0

                    # σ_pp: Esfuerzo de preconsolidación [kPa]
                    σ_pp = estrato.σ_pp

                    # Corrección
                    σ_pp = max(σ_pp, σ_0p)

                    # S_c: Asentamiento por consolidación [m]
                    if σ_0p == σ_pp:
                        dS_c = C_c * H_c / (1 + e_0) * math.log10((σ_0p + Δσ_p) / σ_0p)
                    elif σ_0p + Δσ_p < σ_pp:
                        if ((σ_0p + Δσ_p) / σ_0p) < 0:
                            print("Error***********", σ_0p, Δσ_p, q_0, I_z, W_c)
                        dS_c = C_s * H_c / (1 + e_0) * math.log10((σ_0p + Δσ_p) / σ_0p)
                    elif σ_0p < σ_pp and  σ_pp <= σ_0p + Δσ_p:
                        dS_c = C_s * H_c / (1 + e_0) * math.log10(σ_pp / σ_0p)  +  C_c * H_c / (1 + e_0) * math.log10((σ_0p + Δσ_p) / σ_pp)
                    else:
                        raise ValueError(f"Valor de σ_pp (Esfuerzo de preconsolidación) fuera de rango (σ_0p, σ_pp): ({σ_0p}, {σ_pp})")
                    S_c += dS_c

                    iteraciones.append({"d":d,"H_c":H_c, "z":z, "M":M, "N":N, "V":V, "V_1":V_1, "I_z":I_z, "Δσ_p":Δσ_p, "σ_0p":σ_0p, "C_c":C_c, "C_s":C_s, "e_0":e_0, "σ_pp":σ_pp, "dS_c":dS_c})

            d += estrato.H_0

        # memoria
        memoria = {"W_c":W_c, "W_r":W_r, "q_0":q_0, "iteraciones": iteraciones}

        return (S_c, memoria)

    def interpolar_Iz_elastico(self, z:float) -> float:
        """
        Calcula el factor de influencia de la deformación unitaria

        Arguments:
            z {float} -- Distancia vertical, por debajo del centro de la cimentación, en donde se desea calcular el Iz

        Returns:
            float -- Valor del Iz a la distancia z
        """
        B, = self.get_atributos("B")

        # Iz es 0 cuando z = 0 o cuando z = 2B y 0.6 cuando z = B/2
        if z >= 0 and z < B / 2:
            return 1.2 / B * z
        elif z >= B / 2 and z < 2 * B:
            return -0.4 / B * z + 0.8
        else:
            return 0

    ######################################################################
    # Cálculos volcamiento (2.4)
    ######################################################################
    def calculo_volcamiento(self, F_zc:float, F:float, T_u:float) -> Tuple[float, float, Memoria]:
        """
        Calcula el momento de vuelco y el momento estabilizador es en suelos granulares o cohesivos (Solicitud y Capacidad).
        
        Arguments:
            Fz_c {float} -- Carga axial a tracción [kN]
            F {float} -- Máxima carga lateral asociada a la tracción máxima (Transversal o Longitudinal) [kN]
            T_u {float} -- Capacidad al arranque del cimiento [kN]        

        Returns:
            Tuple[float,float,Memoria] -- (Mv: Momento de vuelco [kN·m], Me: Momento estabilizador [kN·m], memoria)
        """
        B, D, HG, C, θ = self.get_atributos("B", "D", "HG", "C", "θ")

        # Mv:  Momento de vuelco [kN·m]
        Mv = F_zc * (B / 2 - C * tan_g(θ)) + F * (HG +  D)
        
        # Lx:  Brazo de aplicación de la carga generada por el peso del cimiento y la capacidad del arranque [m]
        Lx = B / 2

        # Me: Momento estabilizador [kN·m]
        Me = T_u * Lx

        # memoria
        memoria = {"Lx": Lx, "Mv": Mv}

        return (Mv, Me, memoria)

    ######################################################################
    # Cálculos capacidad a la carga lateral (2.5)
    ######################################################################
    def calculo_carga_lateral(self, F_zc: float) -> Tuple[float, Memoria]:
        B, L, D, H, TP, tipo_mat_r, c_u_r, φ_r, γ_r, perfil  = self.get_atributos("B", "L", "D", "H", "TP", "tipo_mat_r", "c_u_r", "φ_r", "γ_r", "perfil")

        K_pr = None
        if tipo_mat_r == "g":
            # K_pr: Coeficiente de presión pasivo de tierra del relleno de fundación [-]
            K_pr = (1 + sin_g(φ_r)) / (1 - sin_g(φ_r))
            fuerza_horz_pasiva_pedestal = K_pr * γ_r * (D - H)**2 * TP / 2
        elif tipo_mat_r == "c":
            fuerza_horz_pasiva_pedestal = (γ_r * (D - H) + 2 * c_u_r) * (D - H) * TP / 2

        # F_P: Fuerza horizontal producto del empuje pasivo [kN]
        F_P = self.calculo_integral_presion_lateral_pasiva(D - H, D) * B  + fuerza_horz_pasiva_pedestal

        K_ar = None
        if tipo_mat_r == "g":
            # K_ar: Coeficiente de presión activo de tierra del relleno de fundación [-]
            K_ar = (1 - sin_g(φ_r)) / (1 + sin_g(φ_r))
            fuerza_horz_activa_pedestal = K_ar * γ_r * (D - H)**2 * TP / 2
        elif tipo_mat_r == "c":
            fuerza_horz_activa_pedestal = max(0, γ_r * (D - H) - 2 * c_u_r) * (D - H) * TP / 2

        # F_A: Fuerza horizontal producto del empuje activo [kN]
        F_A = self.calculo_integral_presion_lateral_activa(D - H, D) * B  + fuerza_horz_activa_pedestal

        # R_LE: Resultante lateral debida a la diferencia de las fuerzas de los empujes [kN]
        R_LE = F_P - F_A

        # R_LF: Resultante lateral debida a la interacción entre el suelo de fundación y la base del cimiento [kN]
        tipo_mat_en_D = perfil.estrato_en(D + 0.01).tipo_mat
        if  tipo_mat_en_D == "c":
            
            # c_uf: Resistencia al corte no drenado del suelo inmediatamente debajo de D_f  [kN/m²] 
            c_uf = perfil.estrato_en(D + 0.01).c_u if perfil.estrato_en(D + 0.01).c_u is not None else 0

            #c_a: Adherencia para la interfaz cimiento-suelo (material cohesivo). [kN/m²]
            c_a = 2 / 3 * c_uf

            R_LF = c_a * B * L

        elif tipo_mat_en_D == "g":
            
            # φ_f: Ángulo de fricción del suelo inmediatamente debajo de D_f [°]
            φ_f = perfil.estrato_en(D + 0.01).φ_s if perfil.estrato_en(D + 0.01).φ_s is not None else 0

            # δ: Es el ángulo de fricción para la interfaz suelo-fundación (material granular) [°]
            δ = 2 / 3 * φ_f

            R_LF = F_zc * tan_g(δ)

        elif tipo_mat_en_D == "r":
            # φ_f: Ángulo de fricción del suelo inmediatamente debajo de D_f [°]
            φ_f = perfil.estrato_en(D + 0.01).roca_φ_rm if perfil.estrato_en(D + 0.01).roca_φ_rm is not None else 0

            # δ: Es el ángulo de fricción para la interfaz suelo-fundación (material granular) [°]
            δ = 2 / 3 * φ_f

            R_LF = F_zc * tan_g(δ)

        # Q_L: Resistencia a la carga lateral [kN]
        Q_L = R_LE + R_LF

        # memoria
        memoria = {"K_pr":K_pr, "F_P":F_P, "K_ar":K_ar, "F_A":F_A, "R_LE":R_LE, "R_LF":R_LF, "tipo_mat_en_D": tipo_mat_en_D}
        if tipo_mat_en_D == "c":
            memoria["c_a"] = c_a
        elif tipo_mat_en_D == "g":
            memoria["δ"] = δ

        return (Q_L, memoria)
    
    def calculo_integral_presion_lateral_activa(self, prof_ini, prof_fin):
        """Calcula la integral de la presión lateral activa desde la profundidad 'prof_ini' hasta la profundidad 'prof_fin'"""
        return self.calculo_integral_presion_lateral_activa_desde_0(prof_fin) - self.calculo_integral_presion_lateral_activa_desde_0(prof_ini)

    def calculo_integral_presion_lateral_pasiva(self, prof_ini, prof_fin):
        """Calcula la integral de la presión lateral pasiva desde la profundidad 'prof_ini' hasta la profundidad 'prof_fin'"""
        return self.calculo_integral_presion_lateral_pasiva_desde_0(prof_fin) - self.calculo_integral_presion_lateral_pasiva_desde_0(prof_ini)

    def calculo_integral_presion_lateral_activa_desde_0(self, prof):
        """Calcula la integral de la presión lateral activa desde la profundidad 0 hasta la profundidad 'prof'"""
        
        perfil, = self.get_atributos("perfil")

        z = 0.0
        acum = 0.0
        acum_esf_vert = 0.0
        for estrato in perfil:
            if round(z + estrato.H_0,2) < round(prof,2):
                Δ_z = estrato.H_0
            elif round(z,2) < round(prof,2):
                Δ_z = prof - z
            else:
                break
                        
            if estrato.tipo_mat == "g":
                φ_s = estrato.φ_s
                K_a = (1 - sin_g(φ_s)) / (1 + sin_g(φ_s))
                p_ant = acum_esf_vert * K_a
                p = (acum_esf_vert + estrato.γ_se * Δ_z) * K_a
            elif estrato.tipo_mat == "c":
                c_u = estrato.c_u
                p_ant = max(0, acum_esf_vert - 2 * c_u)
                p = max(0, acum_esf_vert + estrato.γ_se * Δ_z - 2 * c_u)
            else:
                raise ValueError(f"Cálculo de presión lateral activa en roca. profundidad = {z}")

            acum_esf_vert += estrato.γ_se * Δ_z
            acum += (p + p_ant) / 2 * Δ_z
            z += estrato.H_0

        return acum

    def calculo_integral_presion_lateral_pasiva_desde_0(self, prof):
        """Calcula la integral de la presión lateral pasiva desde la profundidad 0 hasta la profundidad 'prof'"""

        perfil, = self.get_atributos("perfil")

        z = 0.0
        acum = 0.0
        acum_esf_vert = 0.0
        for estrato in perfil:
            if round(z + estrato.H_0,2) < round(prof,2):
                Δ_z = estrato.H_0
            elif round(z,2) < round(prof,2):
                Δ_z = prof - z
            else:
                break
            
            if estrato.tipo_mat == "g":
                φ_s = estrato.φ_s
                K_p = (1 + sin_g(φ_s)) / (1 - sin_g(φ_s))
                p_ant = acum_esf_vert * K_p
                p = (acum_esf_vert + estrato.γ_se * Δ_z) * K_p
            elif estrato.tipo_mat == "c":
                c_u = estrato.c_u
                p_ant = acum_esf_vert + 2 * c_u
                p = (acum_esf_vert + estrato.γ_se * Δ_z) + 2 * c_u
            else:
                raise ValueError(f"Cálculo de presión lateral activa en roca. profundidad = {z}")

            acum_esf_vert += estrato.γ_se * Δ_z
            acum += (p + p_ant) / 2 * Δ_z
            z += estrato.H_0

        return acum

    ######################################################################
    # Cálculos esfuerzo actuante sobre el suelo (3.2.5.2.2)
    ######################################################################
    def calculo_esfuerzo_actuante_sobre_suelo(self, Fx_c:float, Fy_c:float, Fz_c:float) -> Tuple[float, float, Memoria]:
        """Calcula el empuje pasivo sobre suelos granulares
        
        Arguments:
            γ_r {float} -- Peso unitario del relleno [kN/m³]
            φ_r {float} --  Ánguro de fricción del relleno [°]
            Fx_c {float} -- Carga longitudinal cartesiana [kN]
            Fy_c {float} -- Carga transversal  cartesiana [kN]
            Fz_c {float} -- Carga a axial a compresión cartesiana [kN]
        
        Returns:
            Tuple[float,float,Memoria] -- (Q_max: Esfuerzo máximo actuante [kPa], Q_min: Esfuerzo mínimo actuante [kPa], memoria)
        """
        B, D, HG = self.get_atributos("B", "D", "HG")

        # W_c: Peso de la cimentación [kN]
        W_c = self.peso_seco()

        # W_r: Peso del relleno [kN]
        W_r = self.peso_relleno_seco()

        # Fvo: Carga total a compresión [kN]
        Fvo = Fz_c + W_c + W_r

        MX = self.calculo_momento_carga_axial(Fz_c)

        # MT_o
        # MT, _ =  self.calculo_momento_carga_lateral_zarpa(Fy_c) #Fy_c * (D + HG)
        MT =  Fy_c * (D + HG)
        MT_o = MT + MX

        # e_t: Excentricidad en la cara transversal [m]
        e_t = abs(MT_o / Fvo)

        # ML_o
        # ML, _ = self.calculo_momento_carga_lateral_zarpa(Fx_c) #Fx_c * (D + HG)
        ML = Fx_c * (D + HG)
        ML_o = ML + MX

        # e_l: Excentricidad en la cara longitudinal [m]
        e_l = abs(ML_o / Fvo)

        # B_t
        if e_t >= B / 6:
            B_t = (B - 2 * e_t)
        else:
            B_t = B
        
        # B_l
        if e_l >= B / 6:
            B_l = (B - 2 * e_l)
        else:
            B_l = B

        # A_p: Área efectiva de la zapata [m²]
        A_p = B_t * B_l

        # Q_to:
        Q_to = abs(6 * MT_o / B**3)
        
        # Q_lo:
        Q_lo = abs(6 * ML_o / B**3)

        # Q_med: Esfuerzo actuante promedio [kPa]
        Q_med = Fvo / A_p

        # Q_min: Esfuerzo mínimo actuante [kPa]
        Q_min = Q_med - Q_to - Q_lo

        # Q_max: Esfuerzo máximo actuante [kPa]
        Q_max = Q_med + Q_to + Q_lo

        # memoria
        memoria = {"W_c":W_c, "W_r":W_r, "Fvo":Fvo, "MX": MX, "MT": MT,"MT_o":MT_o, "ML": ML, "ML_o":ML_o, "e_t":e_t, "e_l":e_l, "B_t":B_t, "B_l":B_l, "A_p":A_p, "Q_to":Q_to, "Q_lo":Q_lo, "Q_med":Q_med}

        return (Q_max, Q_min, memoria)

    def calculo_momento_carga_lateral(self, F_c:float) -> Tuple[float, Memoria]:
        """Calcula el momento transversal o longitudinal dependiendo de acuerdo a la carga F_c
        
        Arguments:
            φ_s {float} -- Ángulo de fricción del suelo asumido para el cálculo del momento [°]
            F_c {float} -- Carga transversal o longitudinal cartesiana [kN]
        
        Returns:
            Tuple[float, Memoria] -- (Momento transversal o longitudinal dependiendo de la carga F_c [kN/m²], memoria)        
        """
        B, D, H, HG, TP, perfil, tipo_mat_r, γ_r, φ_r, c_u_r = self.get_atributos("B", "D", "H", "HG", "TP", "perfil", "tipo_mat_r", "γ_r", "φ_r", "c_u_r")
        
        # tipo_mat_H: Tipo de material predominande en el espesor de la zapata.
        tipo_mat_H = perfil.calcular_tipo_mat_predominante(D - H, D)
        
        # φ_s: Ángulo de fricción del suelo en el espesor de la zapata [°]
        φ_s = perfil.calcular_promedio(D - H, D, 'φ_s', tipo_mat= tipo_mat_H)

        # Kp_s: Coeficiente de presión pasiva del suelo [-]
        Kp_s = tan_g(45 + φ_s / 2)**2

        # Kp_r: Coeficiente de presión pasiva del relleno [-]
        Kp_r = tan_g(45 + φ_r / 2)**2

        γ_s = perfil.calcular_promedio(0, D, 'γ_s', tipo_mat= tipo_mat_H)

        c_u = None if tipo_mat_H == "g" else perfil.calcular_promedio(D - H, D, 'c_u', tipo_mat= tipo_mat_H)

        
        # F_p_disp_ped: Fuerza reacción pasivo disponible pedestal [kN]
        F_p_disp_ped = 1 / 2 * Kp_r * γ_r * (D - H)**2 * TP if tipo_mat_r == "g" else 2 * c_u_r * (D - H) * TP

        # F_p_disp_zap: Fuerza reacción pasivo disponible zarpa [kN]
        F_p_disp_zap = 1 / 2 * Kp_s * γ_s * (D**2 - (D - H)**2)* B if tipo_mat_H == "g" else 2 * c_u * H * B

        if F_p_disp_ped + F_p_disp_zap > F_c:
            # alt_pas_ped: Altura del pasivo que se desarrolla en el pedestal [m]
            alt_pas_ped = math.sqrt(2 * F_c / (Kp_r * γ_r * TP)) if tipo_mat_r == "g" else F_c / (2 * c_u_r * TP)
            alt_pas_ped = min(alt_pas_ped, D - H)

            # Cálculo fuerza reacción pasivo en el pedestal [kN]
            F_p_ped = 1 / 2 * Kp_r * γ_r * alt_pas_ped**2 * TP if tipo_mat_r == "g" else 2 * c_u_r * alt_pas_ped * TP

            # Cálculos de brazo
            brazo_ped = D - 2 / 3 * alt_pas_ped if tipo_mat_r == "g" else  D - 1 / 2 * alt_pas_ped

            # Momento pasivo pedestal [kN·m]
            M_pas = F_p_ped * brazo_ped

            # Cálculo fuerza reacción pasivo en la zapata [kN]
            if F_p_disp_ped < F_c:
                # alt_pas_zap: Altura del pasivo que se desarrolla en la zapata [m]
                if tipo_mat_H == "g":
                    alt_pas_zap = H - D + math.sqrt((D - H)**2 + 2 * (F_c - F_p_disp_ped) / (B * Kp_s * γ_s ))
                else:
                    alt_pas_zap = (F_c - F_p_disp_ped) / (2 * c_u * B)
                alt_pas_zap = min(alt_pas_zap, H)

                # Cálculos de brazo                
                if tipo_mat_r == "g":
                    a1 = (D - H)**2
                    a2 = (D - H + alt_pas_zap)**2
                    c = alt_pas_zap * ((2 * (a2 / a1 - 1) + 3)/(6 + 3 * (a2 / a1 - 1)))
                    brazo_zap = H - c
                else:
                    brazo_zap = H - 1 / 2 * alt_pas_zap

                F_p_zap = min(F_p_disp_zap, F_c - F_p_ped)
                
                M_pas += F_p_zap * brazo_zap
            else:
                F_p_zap = 0
                brazo_zap = 0
        else:
            brazo_ped = H + 1 / 3 * (D - H) if tipo_mat_r == "g" else H + 1 / 2 * (D - H)
            y_centroide = (1 / 2 * H**2 * (D - H) + H**3 / 6) / (H * ((D - H) + H / 2))
            brazo_zap = y_centroide
            F_p_zap = F_p_disp_zap
            F_p_ped = F_p_disp_ped
            M_pas = (F_p_ped * brazo_ped) + (F_p_zap * brazo_zap)

        M = F_c * (D + HG) - M_pas

        memoria = {"tipo_mat_H": tipo_mat_H, "φ_s": φ_s, "φ_r": φ_r, "c_u": c_u, "brazo_ped": brazo_ped, "brazo_zap": brazo_zap, "F_p_ped": F_p_ped, "F_p_zap": F_p_zap, "M_pas": M_pas}

        return (M, memoria)

    def calculo_momento_carga_lateral_zarpa(self, F_c:float) -> Tuple[float, Memoria]:
        """Calcula el momento transversal o longitudinal dependiendo de acuerdo a la carga F_c
        
        Arguments:
            φ_s {float} -- Ángulo de fricción del suelo asumido para el cálculo del momento [°]
            F_c {float} -- Carga transversal o longitudinal cartesiana [kN]
        
        Returns:
            Tuple[float, Memoria] -- (Momento transversal o longitudinal dependiendo de la carga F_c [kN/m²], memoria)        
        """
        B, D, H, HG, TP, perfil, tipo_mat_r, γ_r, φ_r, c_u_r = self.get_atributos("B", "D", "H", "HG", "TP", "perfil", "tipo_mat_r", "γ_r", "φ_r", "c_u_r")
        
        # tipo_mat_H: Tipo de material predominande en el espesor de la zapata.
        tipo_mat_H = perfil.calcular_tipo_mat_predominante(D - H, D)
        
        # φ_s: Ángulo de fricción del suelo en el espesor de la zapata [°]
        φ_s = perfil.calcular_promedio(D - H, D, 'φ_s', tipo_mat= tipo_mat_H)

        # Kp_s: Coeficiente de presión pasiva del suelo [-]
        Kp_s = tan_g(45 + φ_s / 2)**2

        # Kp_r: Coeficiente de presión pasiva del relleno [-]
        Kp_r = tan_g(45 + φ_r / 2)**2

        γ_s = perfil.calcular_promedio(0, D, 'γ_s', tipo_mat= tipo_mat_H)

        c_u = None if tipo_mat_H == "g" else perfil.calcular_promedio(D - H, D, 'c_u', tipo_mat= tipo_mat_H)

        # F_p_disp_zap: Fuerza reacción pasivo disponible zarpa [kN]
        F_p_disp_zap = 1 / 2 * Kp_s * γ_s * (D**2 - (D - H)**2)* B if tipo_mat_H == "g" else 2 * c_u * H * B

        if F_p_disp_zap > F_c:
            # Cálculo fuerza reacción pasivo en la zapata [kN]
            # alt_pas_zap: Altura del pasivo que se desarrolla en la zapata [m]
            if tipo_mat_H == "g":
                alt_pas_zap = H - D + math.sqrt((D - H)**2 + 2 * F_c / (B * Kp_s * γ_s ))
            else:
                alt_pas_zap = F_c / (2 * c_u * B)
            alt_pas_zap = min(alt_pas_zap, H)

            # Cálculos de brazo                
            if tipo_mat_r == "g":
                a1 = (D - H)**2
                a2 = (D - H + alt_pas_zap)**2
                c = alt_pas_zap * ((2 * (a2 / a1 - 1) + 3)/(6 + 3 * (a2 / a1 - 1)))
                brazo_zap = H - c
            else:
                brazo_zap = H - 1 / 2 * alt_pas_zap

            F_p_zap = min(F_p_disp_zap, F_c)
            
            M_pas = F_p_zap * brazo_zap
        else:
            # Cálculos de brazo                
            if tipo_mat_r == "g":
                a1 = (D - H)**2
                a2 = (D )**2
                c = H * ((2 * (a2 / a1 - 1) + 3)/(6 + 3 * (a2 / a1 - 1)))
                brazo_zap = H - c
            else:
                brazo_zap = H - 1 / 2 * H
            # y_centroide = (1 / 2 * H**2 * (D - H) + H**3 / 6) / (H * ((D - H) + H / 2))
            # brazo_zap = y_centroide
            F_p_zap = F_p_disp_zap
            M_pas =  F_p_zap * brazo_zap

        M = F_c * (D + HG) - M_pas

        memoria = {"tipo_mat_H": tipo_mat_H, "φ_s": φ_s, "φ_r": φ_r, "c_u": c_u,  "brazo_zap": brazo_zap, "F_p_zap": F_p_zap, "M_pas": M_pas}

        return (M, memoria)

    def calculo_momento_carga_axial(self, F_zc: float):
        D, HG, θ, H = self.get_atributos("D", "HG", "θ", "H")

        brazo = (D + HG - H) * tan_g(θ)
        M = - F_zc * brazo

        return M

