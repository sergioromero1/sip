import math
from typing import List, Dict, Tuple, Any
from .util import sin_g, cos_g, tan_g, cot_g, γ_agua, π, calcular_C_d, Memoria, calcular_I_f, rad
from .perfil import Perfil, Estrato

class Pilastra:
    """
    Cimentación tipo pilastra en roca

    Attributes:
        h_i {float} -- Profundidad de inicio de la pilastra  [m]
        D_p {float} -- Diametro de la pilastra  [m]
        H {float} -- Altura de la pilastra  [m]
        HG {float} -- Altura del pedestal no enterrado [m]
        TP {float} -- Lado correspondiente a la sección transversal del pedestal [m]
        θ {float} -- Ángulo del pedestal con respecto a la vertical [°]
        γ_c {float} -- Peso unitario de la pilastra [kN/m³]
        perfil {Perfil} -- Perfil estratigráfico en el suelo de la pilastra
        ω {float} -- Ángulo de inclinación del terreno [°]
    """
    ######################################################################
    # Constructor
    ######################################################################
    def __init__(self,
                    h_i:float,
                    D_p:float,
                    H:float, 
                    HG:float,
                    TP:float, 
                    θ:float, 
                    γ_c:float,
                    perfil:Perfil,
                    ω: float
                    ):
                    
        """
        Inicializa la pilastra
        
        Arguments:
            h_i {float} -- Profundidad de inicio de la pilastra  [m]
            D_p {float} -- Diametro de la pilastra  [m]
            H {float} -- Altura de la pilastra  [m]
            HG {float} -- Altura del pedestal no enterrado [m]
            TP {float} -- Lado correspondiente a la sección transversal del pedestal [m]
            θ {float} -- Ángulo del pedestal con respecto a la vertical [°]
            γ_c {float} -- Peso unitario de la pilastra [kN/m³]
            perfil {Perfil} -- Perfil estratigráfico en el suelo de la pilastra
            ω {float} -- Ángulo de inclinación del terreno [°]
        """        
        self.h_i = h_i
        self.D_p = D_p
        self.H = H
        self.HG = HG
        self.TP = TP
        self.θ = θ
        self.γ_c = γ_c
        self.ω = ω or 0
        self.perfil = perfil

        self.validar_atributos()

        # t {float} -- Distacia de la cresta al centro de la pilastra
        self.t = h_i / tan_g(ω) if self.ω > 0 else None

        info_mat_relleno = self.perfil.calcular_material_relleno(self.h_i)
        self.tipo_mat_r, self.φ_r, self.c_u_r, self.γ_r  = (info_mat_relleno["tipo_mat"], info_mat_relleno["φ"], info_mat_relleno["c_u"], info_mat_relleno["γ"])

    ######################################################################
    # Propiedades
    ######################################################################

    # C: Altura total del pedestal [m]
    def get_C(self):
        return self.D + self.HG - self.H
    C = property(get_C)

    # D: Profundidad de la pilastra [m]
    def get_D(self):
        return self.h_i + self.H
    D = property(get_D)

    # r: Factor de reducción por pendiente del terreno
    # Mezazigh y levacher ( Verhoef, 2015 ) - 

    def get_r(self):
        ω, D_p, t = self.get_atributos("ω", "D_p", "t" )
        r = 1.0
        if ω > 0:
            t_lim = 4 * D_p * (6 * tan_g(ω) - 1)
            r = (17 - 15 * tan_g(ω)) / 100 * t / D_p + (1- tan_g(ω)) / 2
            if t > t_lim:
                r = 1.0
        
        return r
    r = property(get_r)

    ######################################################################
    # Utilitarios
    ######################################################################
    def validar_atributos(self):
        #   - Obligatoriedad
        #   - Tipos y dominios
        #   - Restricciones en el perfil 
        
        #Pilastra debe estar siempre en un perfil seco 
        perfil, = self.get_atributos("perfil")

        nivel_freatico = perfil.calcular_NF()

        if nivel_freatico:
            raise ValueError (f'Pilastra en suelo potencialmente saturado, se encontró nivel freático a {nivel_freatico} m')

        #La roca para la pilastra debe existir y debe estar siempre a 1 metro  o menos de la superficie del terreno
        perfil,= self.get_atributos("perfil")

        profundidad_roca = perfil.calcular_profundidad_hasta_roca()
        
        if profundidad_roca is None:
            raise ValueError ('Pilastra en perfil sin roca')

    def get_atributos(self, *nombres: str) -> Tuple:
        """Retorna los atributos solicitados como una tupla"""

        #return (self.__dict__[nombre] for nombre in nombres)
        return (getattr(self, nombre) for nombre in nombres)

    def volumen(self) -> float:
        """
        Calcula el volumen de la pilastra.

        Returns:
            float -- Volumen de la pilastra [m³]
        """
        D_p, H, C, TP, θ = self.get_atributos("D_p", "H", "C", "TP", "θ")
        
        return π * D_p ** 2 / 4 * H + TP**2 * C / cos_g(θ)

    def peso(self) -> float:
        """ 
        Calcula el peso de la pilastra.

        Returns:
            float -- Peso de la pilastra [kN]
        """
        γ_c,  = self.get_atributos("γ_c")

        return self.volumen() * γ_c

    def volumen_relleno(self) -> float:
        """
        Calcula el volumen del relleno.

        Returns:
            float -- Volumen del relleno [m³]
        """
        D_p, TP, θ, h_i = self.get_atributos("D_p", "TP", "θ", "h_i")
    
        return π * D_p ** 2 / 4 * h_i - TP**2 * h_i / cos_g(θ)

    def peso_relleno(self) -> float:
        """
        Calcula el peso del relleno.

        Returns:
            float -- Peso del relleno [kN]
        """
        γ_r,  = self.get_atributos("γ_r")
        volumen_relleno = self.volumen_relleno()
        if volumen_relleno > 0:
            return  volumen_relleno * γ_r
        else:
            return 0.0

    def set_perfil(self, perfil: Perfil):
        self.perfil = perfil
        self.tipo_mat_r, self.φ_r, self.c_u_r, self.γ_r  = perfil.calcular_material_relleno(self.h_i)

    def parametros_admisibles_de_resistencia(self, RQD):
        """
        Retorna parametros admisibles de resistencia de acuerdo con RQD del perfil

        Arguments: RQD -- RQD de la roca

        returns:
            Tuple[float,float,Memoria] -- (τ_adm: Friccion cimiento roca admisible [kN/m²],
                                            σ_adm: Esfuerzo neto de compresion admisible [kN/m²],
                                            γ: Peso unitario [kN/m³])
        
        """
        
        if RQD <= 25:
            τ_adm = 73.55
            σ_adm = 784.53
            γ = 17.65

        elif RQD <= 40:
            τ_adm = 117.68
            σ_adm = 1765.2
            γ = 19.61

        else:
            τ_adm = 137.29
            σ_adm = 2255.53
            γ = 19.61


        return (τ_adm, σ_adm, γ)

    ######################################################################
    # Cálculos compresión
    ######################################################################

    def calculo_compresion(self, F_zc:float) -> Tuple[float, Memoria]:
        """
        Calcula las capacidad portante última
        
        Arguments:
            F_zc:  {float} -- Componente vertical de la carga a compresión [kN].

        Returns:
            Tuple[float, Memoria] -- (P_adm: Resistenci admisible a compresion [kN], P_act: Fuerza actuante a compresion[kN])
        """         

        #P_f_adm : Resistencia admisible por fuste [kN]
        P_f_adm, _ =  self.calculo_resistencia_admisible_fuste()
        
        #P_p_adm : Resistencia admisible por punta [kN]
        P_p_adm, _ = self.calculo_resistencia_admisible_punta_compresion()
        
        #P_adm : Resistencia admisible a compresión [kN]
        P_adm = P_f_adm + P_p_adm

        #P_act : Esfuerzo actuante a compresión [kN]
        P_act = self.peso() + self.peso_relleno() + F_zc  

        memoria =  {"P_f_adm": P_f_adm, "P_p_adm": P_p_adm}

        return (P_adm, P_act, memoria)

    def calculo_resistencia_admisible_fuste(self):
        
        """
        Calcula la resistencia admisible por fuste

        Arguments:
            
        Returns:
            Tuple[float, Memoria] -- (P_f_adm: Resistencia admisible a por fuste [kN] ,
                                        memoria )
        """

        D, H, D_p, perfil = self.get_atributos("D", "H", "D_p", "perfil")

        # Resistencia admisible por fuste [kN]
        iteraciones = []
        d = 0.0  # prof. ini de capa actual
        prof_ini = D - H 
        prof_fin = D

        P_f_adm = 0.0
        for estrato in perfil:
            if d + estrato.H_0 > prof_ini and d < prof_fin:
                # Δ_z, z
                if d < prof_ini:
                    if d + estrato.H_0 < prof_fin:
                        Δ_z = d + estrato.H_0 - prof_ini
                    else:
                        Δ_z = prof_fin - prof_ini
                    z = prof_ini + Δ_z / 2
                else:
                    if d + estrato.H_0 < prof_fin:
                        Δ_z = estrato.H_0
                    else:
                        Δ_z = prof_fin - d
                    z = d + Δ_z / 2

                if estrato.tipo_mat == "r":
                    
                    #RQD : RQD del estrato [%]
                    RQD = estrato.RQD

                    #τ_adm : Friccion cimiento roca admisible  correspondiente al estrato [kN/m²]
                    τ_adm, _, _ = self.parametros_admisibles_de_resistencia(RQD)
                    
                    #P_f_adm : Resistencia admisible por fuste [kN]
                    P_f_adm +=  τ_adm * π * D_p * Δ_z
                    
                    iteraciones.append({"RQD":RQD, "τ_adm":τ_adm, "Δ_z":Δ_z, "P_f_adm":P_f_adm, "z":z})
                
            d += estrato.H_0

        #memoria
        memoria = {"iteraciones": iteraciones}
        
        return (P_f_adm , memoria)

    def calculo_resistencia_admisible_punta_compresion(self):

        """
        Calcula la resistencia admisible por punta a compresión

        Arguments:
            
        Returns:
            Tuple[float, Memoria] -- (P_p_adm: Resistencia admisible a por punta [kN],
                                        memoria )
        """
        
        D_p, D, perfil = self.get_atributos("D_p", "D", "perfil")

        estrato = perfil.estrato_en(D)

        #RQD : RQD del estrato en la punta de la pilastra [%]
        RQD = estrato.RQD

        #σ_adm : Esfuerzo neto admisible a compresión 
        _, σ_adm, _ = self.parametros_admisibles_de_resistencia(RQD)

        #P_p_adm : Resistencia admisible por punta [kN]
        P_p_adm = σ_adm * π * D_p **2 /4

        memoria = {"RQD":RQD, "σ_adm":σ_adm}

        return P_p_adm, memoria

    ######################################################################
    # Cálculos tensión 
    ######################################################################
    def calculo_tension(self) -> float:
        """
        Calcula las capacidad a la tensión
        
        Arguments:
            
        Returns:
            T_adm: Resistencia admisible a tensión [kN]
            Tuple[float, Memoria] -- (T_adm : Resistencia admisible a tensión [kN] ,
                                        memoria )
        """
    
        W_c = self.peso()

        W_r = self.peso_relleno()

        #F_t: Resistencia admisible por fuste [kN]
        F_t, _ = self.calculo_resistencia_admisible_fuste()

        #T_adm : Resistencia admisible a tensión [kN]
        T_adm =  F_t + W_c + W_r

        memoria = {"F_t":F_t, "W_c":W_c, "W_r":W_r}

        return (T_adm, memoria)

    ######################################################################
    # Cálculos volcamiento
    ######################################################################
    def calculo_volcamiento(self, F_zc:float, F:float) -> Tuple[float, float, Memoria]:
        """
        Calcula el momento de vuelco y el momento estabilizador es en suelos granulares o cohesivos (Solicitud y Capacidad).
        
        Arguments:
            Fz_c {float} -- Carga axial a tracción [kN]
            F {float} -- Resultante carga lateral asociada a la tracción máxima (Transversal y Longitudinal) [kN]        

        Returns:
            Tuple[float,float,Memoria] -- (Mv: Momento de vuelco [kN·m], Me: Momento estabilizador [kN·m], memoria)
        """
        D_p, H, C, θ, D, r  = self.get_atributos("D_p", "H", "C", "θ", "D", "r")
        
        # M_wc : Momento estabilizador por peso de la cimentación [kN·m]
        M_wc = (self.peso()+ self.peso_relleno()) * D_p / 2

        #acum: area acumulada correspondiente al empuje pasivo [m²]
        acum = self.calculo_integral_presion_lateral_pasiva(D - H, D)

        #areas_por_brazos: sumatoria de areas por brazos que componen el area respecto al empuje pasivo desde el inicio de la pilastra [m³]
        areas_por_brazos = self.calcular_areas_por_brazos(D)
        
        #centroide: centroide del area acumulada correspondiente al empuje pasivo, se mide hasta la profundidad D 
        centroide = areas_por_brazos / acum

        # R_p : Empuje pasivo en la pilastra  [kN]
        R_p = self.calculo_integral_presion_lateral_pasiva(D - H, D) * D_p * r

        # M_p : Momento por Empuje pasivo en la pilastra  [kN·m]
        M_p = R_p * centroide

        # F_r : Friccion por contacto roca fuste  [kN]
        F_, _ = self.calculo_resistencia_admisible_fuste() 
        F_r = F_ / 2

        # M_fr : Momento por Friccion roca fuste  [kN·m]
        M_fr = F_r * D_p * ( 1 / 2 + 1 / π )
                
        # Me: Momento estabilizador [kN·m]
        Me = M_wc + M_p + M_fr

        # Mv:  Momento de vuelco [kN·m]
        Mv = F_zc * (D_p / 2 - C * tan_g(θ)) + F * (C + H)

        # memoria
        memoria = {"M_wc": M_wc, "R_p": R_p, "M_p": M_p, "F_r": F_r, "M_fr":M_fr, "centroide":centroide, "r":r}
        
        return (Mv, Me, memoria)

    def calcular_areas_por_brazos(self, prof:float) -> float:
        """Calcula  el producto de las areas correspondientes al empuje lateral por sus respectivos
            brazos desde el inicio de la pilastra

            Se usa para calcular el centroide de la fuerza resultante por empuje pasivo 

            Returns:
            {float} -- areas_por_brazos: area representativa de empuje lateral de cada trapecio por su brazo correspondiente  desde el inicio de la pilastra [kN]
                                    
        """

        perfil, D, H = self.get_atributos("perfil", "D", "H")
        areas_por_brazos = 0.0
        z = 0.0
        acum_esf_vert = 0.0

        #Δ_z: Espesor de estrato competente
        for estrato in perfil:
            if z + estrato.H_0 < prof:
                Δ_z = estrato.H_0
            elif z < prof:
                Δ_z = prof - z
            else:
                break
            
            if estrato.tipo_mat == "g":
                φ_s = estrato.φ_s
                K_p = (1 + sin_g(φ_s)) / (1 - sin_g(φ_s))
                p_ant = acum_esf_vert * K_p
                p = (acum_esf_vert + estrato.γ_rse * Δ_z) * K_p
                area_rectangulo = Δ_z * min(p, p_ant)
                area_triangulo = (max(p, p_ant) - min(p, p_ant))/2
                brazo_rectangulo = Δ_z / 2 + (z + Δ_z)
                brazo_triangulo = Δ_z / 3 + (z + Δ_z)

            elif estrato.tipo_mat == "c":
                c_u = estrato.c_u
                p_ant = acum_esf_vert + 2 * c_u
                p = (acum_esf_vert + estrato.γ_rse * Δ_z) + 2 * c_u
                area_rectangulo = Δ_z * min(p, p_ant)
                area_triangulo = (max(p, p_ant) - min(p, p_ant))/2
                brazo_rectangulo = Δ_z / 2 + (z + Δ_z)
                brazo_triangulo = Δ_z / 3 + (z + Δ_z)

            else:
                # método de Zhang

                #RQD : RQD del estrato [%]
                RQD = estrato.RQD
                
                #τ_adm : Friccion cimiento roca admisible  correspondiente al estrato [kN/m²]
                #γ: Peso unitario [kN/m³]
                τ_adm, _, γ = self.parametros_admisibles_de_resistencia(RQD)

                #γ_e : Peso unitario efectivo [kN/m³]
                γ_e = min(γ, estrato.γ_rse)

                #roca_a: Parámetro a de roca[-] 
                roca_a = estrato.roca_a

                #roca_s: Parámetro s de roca[-] 
                roca_s = estrato.roca_s

                #roca_m: Parámetro m de roca[-]  
                roca_m = estrato.roca_m

                #ucs: Resistencia a la compresión uniaxial [kPa] , entra en MPa
                ucs = estrato.ucs * 1000

                p_ant = acum_esf_vert + ucs * (roca_m * acum_esf_vert / ucs + roca_s)**roca_a + τ_adm

                p = (acum_esf_vert + γ_e * Δ_z) + ucs * (roca_m * (acum_esf_vert + γ_e * Δ_z) / ucs + roca_s)**roca_a + τ_adm

                area_rectangulo = Δ_z * min(p, p_ant)
                area_triangulo = (max(p, p_ant) - min(p, p_ant))/2
                brazo_rectangulo = Δ_z / 2 + D - (z + Δ_z)
                brazo_triangulo = Δ_z / 3 + D - (z + Δ_z)

            if z + estrato.H_0 <= D - H:
                areas_por_brazos += 0
            else:
                areas_por_brazos += area_rectangulo * brazo_rectangulo + area_triangulo * brazo_triangulo
            
            acum_esf_vert += estrato.γ_rse * Δ_z
            z += estrato.H_0

        return areas_por_brazos

    ######################################################################
    # Cálculos capacidad a la carga lateral 
    ######################################################################
    def calculo_carga_lateral(self, F_zc: float) -> Tuple[float, Memoria]:
        """
        Calcula capacidad ante carga lateral
        
        Arguments:
            Fz_c {float} -- Componente vertical de la carga a compresión [kN]
                    
        Returns:
            Tuple[float,Memoria] -- (Q_L Resistencia a la carga lateral [kN], memoria)
        """

        D_p, H, D, r, perfil = self.get_atributos("D_p", "H", "D", "r", "perfil")

        estrato = perfil.estrato_en(D)

        #φ_rm : Angulo de friccion roca en la profundidad D[°]
        φ_rm = estrato.roca_φ_rm
        
        # F_P: Fuerza horizontal producto del empuje pasivo [kN]  # En metodologías de suelo va *3
        F_p = self.calculo_integral_presion_lateral_pasiva(D - H, D) * D_p   

        # R_LF: Resultante lateral debida a la interacción entre el suelo de fundación y la base del cimiento [kN]
        R_LF = F_zc * tan_g(2 / 3 * φ_rm)

        # Q_L: Resistencia a la carga lateral [kN]
        Q_L = (F_p + R_LF) * r

        memoria = {"F_p": F_p, "R_LF":R_LF, "φ_rm": φ_rm, "r": r}

        return (Q_L, memoria)

    def calculo_integral_presion_lateral_pasiva(self, prof_ini, prof_fin):
        """Calcula la integral de la presión lateral pasiva desde la profundidad 'prof_ini' hasta la profundidad 'prof_fin'
        
            Returns:
            float -- ( acum: empuje lateral acumulado de los trapecios desde profundidad inicial hasta profundidad final [kN/m])

        """
        return self.calculo_integral_presion_lateral_pasiva_desde_0(prof_fin) - self.calculo_integral_presion_lateral_pasiva_desde_0(prof_ini)

    def calculo_integral_presion_lateral_pasiva_desde_0(self, prof):
        """Calcula la integral de la presión lateral pasiva desde la profundidad 0 hasta la profundidad 'prof'
            para rocas calcula por el metodo de Zhang
        Returns:
            float -- ( acum: empuje lateral acumulado de los trapecios desde 0 [kN/m])

        """
        perfil, = self.get_atributos("perfil")

        z = 0.0
        acum = 0.0
        acum_esf_vert = 0.0

        #Δ_z: Espesor de estrato competente
        for estrato in perfil:
            if z + estrato.H_0 < prof:
                Δ_z = estrato.H_0
            elif z < prof:
                Δ_z = prof - z
            else:
                break
            
            if estrato.tipo_mat == "g":
                φ_s = estrato.φ_s
                K_p = (1 + sin_g(φ_s)) / (1 - sin_g(φ_s))
                p_ant = acum_esf_vert * K_p
                p = (acum_esf_vert + estrato.γ_rse * Δ_z) * K_p
            elif estrato.tipo_mat == "c":
                c_u = estrato.c_u
                p_ant = acum_esf_vert + 2 * c_u
                p = (acum_esf_vert + estrato.γ_rse * Δ_z) + 2 * c_u
            
            else: 

                #RQD : RQD del estrato [%]
                RQD = estrato.RQD
                
                #τ_adm : Friccion cimiento roca admisible  correspondiente al estrato [kN/m²]
                #γ: Peso unitario [kN/m³]
                τ_adm, _, γ = self.parametros_admisibles_de_resistencia(RQD)

                #γ_e : Peso unitario efectivo [kN/m³]
                γ_e = min(γ, estrato.γ_rse)

                #roca_a: Parámetro a de roca[-] 
                roca_a = estrato.roca_a

                #roca_s: Parámetro s de roca[-] 
                roca_s = estrato.roca_s

                #roca_m: Parámetro m de roca[-] 
                roca_m = estrato.roca_m

                #ucs: Resistencia a la compresión uniaxial [MPa]
                ucs = estrato.ucs * 1000

                p_ant = acum_esf_vert + ucs * (roca_m * acum_esf_vert / ucs + roca_s)**roca_a + τ_adm

                p = (acum_esf_vert + γ_e * Δ_z) + ucs * (roca_m * (acum_esf_vert + γ_e * Δ_z) / ucs + roca_s)**roca_a + τ_adm

            acum_esf_vert += estrato.γ_rse * Δ_z
            acum += (p + p_ant) / 2 * Δ_z
            z += estrato.H_0

        return acum
        