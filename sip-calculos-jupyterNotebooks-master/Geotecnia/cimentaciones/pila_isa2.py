import math
import numpy as np
import statistics
from typing import List, Dict, Tuple, Any
from .util import sin_g, cos_g, tan_g, cot_g, γ_agua, π, calcular_C_d, Memoria, calcular_I_f, rad, generar_serie
from .perfil import Perfil, Estrato

class Pila:
    """
    Cimentación tipo pila en suelo          

    Attributes:
        D_p {float} --  Diámetro de la pila [m] 
        h_i {float} -- Profundidad de inicio de la pila  [m]
        H {float} --    Longitud la pila [m]
        HG {float} -- Altura del pedestal no enterrado [m]
        h_c {float} --  Altura de la campana [m]
        h_con {float}-- Altura de la sección conica de la campana[m]
        θ_c {float} --  Ángulo de la campana [°]
        TP {float} --   Lado correspondiente a la sección transversal del pedestal [m]
        θ {float} --    Ángulo del pedestal respecto a la vertical [°]
        γ_c {float} --  Peso unitario del material de la cimentación [kN/m³]
        E_p {float} -- Módulo de elasticidad del pilote [kPa]
        perfil {Perfil} -- Perfil estratigráfico en el suelo de la pila
        campana{bool} -- Boleano que define condicion de pila con o sin campana
        ω {float} -- Ángulo de inclinación del terreno [°]
    """
    ######################################################################
    # Constructor
    ######################################################################

    def __init__(self, D_p:float, 
                    h_i:float,
                    H:float,
                    HG:float,
                    h_c:float,
                    h_con:float, 
                    θ_c:float, 
                    TP:float, 
                    θ:float, 
                    γ_c:float,
                    E_p:float, 
                    perfil:Perfil,
                    campana:bool,
                    ω: float):

        """
        Inicializa la pila 
        
        Arguments:
        D_p {float} --  Diámetro de la pila [m] 
        h_i {float} -- Profundidad de inicio de la pila  [m]
        H {float} --    Longitud la pila [m]
        HG {float} -- Altura del pedestal no enterrado [m]
        h_c {float} --  Altura de la campana [m]
        h_con {float}-- Altura de la sección conica de la campana[m]
        θ_c {float} --  Ángulo de la campana [°]
        TP {float} --   Lado correspondiente a la sección transversal del pedestal [m]
        θ {float} --    Ángulo del pedestal respecto a la vertical [°]
        γ_c {float} --  Peso unitario del material de la cimentación [kN/m³]
        E_p {float} -- Módulo de elasticidad del pilote [kPa]
        perfil {Perfil} -- Perfil estratigráfico en el suelo de la pila
        campana{bool} -- Boleano que define condicion de pila con o sin campana
        ω {float} -- Ángulo de inclinación del terreno [°]
        """

        self.D_p = D_p
        self.h_i = h_i
        self.H = H
        self.HG = HG
        self.h_c = h_c
        self.h_con = h_con
        self.θ_c = θ_c
        self.TP = TP
        self.θ = θ 
        self.γ_c = γ_c
        self.E_p = E_p
        self.perfil = perfil
        self.campana = campana
        self.ω = ω
        self.D_c = self.D_p

        if campana:
            self.D_c = self.D_p + tan_g(self.θ_c) * self.h_con * 2
                
        self.validar_atributos()

        # t {float} -- Distacia de la cresta al centro de la pila
        self.t = h_i / tan_g(ω) if self.ω > 0 else None

        info_mat_relleno = self.perfil.calcular_material_relleno(self.h_i)
        self.tipo_mat_r, self.φ_r, self.c_u_r, self.γ_r  = (info_mat_relleno["tipo_mat"], info_mat_relleno["φ"], info_mat_relleno["c_u"], info_mat_relleno["γ"])

    ######################################################################
    # Propiedades
    ######################################################################

    # C: Altura total del pedestal [m]
    def get_C(self):
        return self.h_i + self.HG
    C = property(get_C)

    # D : Profundidad de desplante de la pila [m]
    def get_D(self):
        return self.h_i + self.H
    D = property(get_D)

    # r: Factor de reducción por pendiente del talud[-]
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
        
        perfil, D_c, D_p  = self.get_atributos("perfil", "D_c", "D_p")
        
        #Pila debe estar siempre en un perfil seco
        nivel_freatico = perfil.calcular_NF()
            
        if nivel_freatico:
            raise ValueError (f'El perfil tiene nivel freatico a {nivel_freatico} m')

        # #D_c debe ser mayor o igual a D_p
        if D_c < D_p:
            raise ValueError (f'El diametro de la campana {D_c} m, es menor que el diametro de la pila {D_p}m ')

        #D no puede estar ubicado en roca
        perfil, D = self.get_atributos("perfil", "D")

        profundidad_roca = perfil.calcular_profundidad_hasta_roca()
        
        if profundidad_roca is not None and (D > profundidad_roca):
            raise ValueError ('Pila en roca')

    def get_atributos(self, *nombres: str) -> Tuple:
        """Retorna los atributos solicitados como una tupla"""

        #return (self.__dict__[nombre] for nombre in nombres)
        return (getattr(self, nombre) for nombre in nombres)

    def volumen(self) -> float:
        """
        Calcula el volumen de la pila
        incluye pedestal

        Returns:
            float -- Volumen de la pila [m³]
        """

        D_p, D_c, h_c, h_con, H, C, TP, θ, campana = self.get_atributos("D_p", "D_c", "h_c", "h_con", "H", "C", "TP", "θ", "campana")
        
        V_p = H * π * D_p**2 / 4 + TP**2 * C / cos_g(θ)

        if (D_p != D_c) and campana:
                        
            V1 = h_con * π / 3 *((D_p / 2)**2 + (D_c / 2)**2 + D_p / 2 * D_c / 2) # Volumen de la sección cónica completa
            V2 = π / 4 * D_c ** 2 * (h_c - h_con)             # Volumen de la sección cilíndrica despues del cono hasta la punta
            V3 = π / 4 * D_p ** 2 * h_c                       # Volumen de la sección cilíndrica con diametro D_p del interna en la longtud h_c (la que correspondería a logitud h_c de no haber campana)
            V_p += V1 + V2 - V3

        return V_p 

    def peso(self) -> float:
        """
        Calcula el peso de la pila

        Returns:
            float -- Peso de la pila [kN]
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

        return self.volumen_relleno() * γ_r

    def _interpolar_ku(self, φ) -> float:
        """
        Interpola la curva lineal a trozos de Ku(φ) segun la metodología de Das(2001)
        """
        φs = [20, 25, 30, 35, 40, 45]
        kus = [0.856, 0.888, 0.920, 0.936, 0.960, 0.960]

        if φ < φs[0] or φ > φs[-1]:
            raise ValueError("Valor φ fuera de rango [20 - 45]: " + str(φ))

        i1 = [i for i in range(len(φs)) if φs[i] <= φ ][-1] 
        i2 = [i for i in range(len(φs)) if φs[i] >= φ ][0]

        if i1 == i2:
            return kus[i1]
        else:
            return (kus[i2] - kus[i1]) / (φs[i2] - φs[i1]) * (φ - φs[i1])   + kus[i1]

    def _interpolar_m(self, φ) -> float:
        """
        Interpola la curva lineal a trozos de m(φ) segun la metodología de Das(2001)
        """
        φs = [20, 25, 30, 35, 40, 45]
        ms = [0.05, 0.10, 0.15, 0.25, 0.35, 0.50]

        if φ < φs[0] or φ > φs[-1]:
            raise ValueError("Valor φ fuera de rango [20 - 45]: " + str(φ))

        i1 = [i for i in range(len(φs)) if φs[i] <= φ ][-1] 
        i2 = [i for i in range(len(φs)) if φs[i] >= φ ][0]

        if i1 == i2:
            return ms[i1]
        else:
            return (ms[i2] - ms[i1]) / (φs[i2] - φs[i1]) * (φ - φs[i1])   + ms[i1]

    def _interpolar_N_q(self, φ) -> float:
        """
        Interpola la curva lineal a trozos de m(φ) segun la metodología de Das(2001)
        """
        
        φs = [20, 25, 28, 30, 32, 34, 36, 38, 40, 42, 45]
        nqs = [4, 5, 8, 12, 17, 22, 30, 40, 60, 80, 115]
        

        if φ < φs[0] or φ > φs[-1]:
            raise ValueError("Valor φ fuera de rango [20 - 45]: " + str(φ))

        i1 = [i for i in range(len(φs)) if φs[i] <= φ ][-1] 
        i2 = [i for i in range(len(φs)) if φs[i] >= φ ][0]

        if i1 == i2:
            return nqs[i1]
        else:
            return (nqs[i2] - nqs[i1]) / (φs[i2] - φs[i1]) * (φ - φs[i1])   + nqs[i1]

    def _interpolar_B_c(self, relacion_H_D) -> float:
        """
        Interpola la curva lineal a trozos de Bc segun la metodología de Das(2001)
        """
        r = relacion_H_D
        rs = [0, 0.12, 0.2, 0.25, 0.4, 0.55, 0.6, 0.8, 1,]
        bcs = [0, 1.8, 3.15, 3.6, 5.58, 7.2, 7.56, 8.55, 9]
        
        

        if r < rs[0] or r > rs[-1]:
            raise ValueError("Valor relacion_H_D fuera de rango [0 - 1]: " + str(r))

        i1 = [i for i in range(len(rs)) if rs[i] <= r ][-1] 
        i2 = [i for i in range(len(rs)) if rs[i] >= r ][0]

        if i1 == i2:
            return bcs[i1]
        else:
            return (bcs[i2] - bcs[i1]) / (rs[i2] - rs[i1]) * (r - rs[i1])  + bcs[i1]

    def _calcular_excentricidad(self, cargas) -> float:

        """ 
        Calcula la excentricidad debido a carga lateral 
        para un caso de carga
        """

        F_z, F_x, F_y = cargas

        h_i, HG, θ = self.get_atributos("h_i", "HG", "θ")

        M_L = F_x * (h_i + HG)

        M_T = F_y * (h_i + HG)

        M_V = F_z * tan_g(θ) * (h_i + HG)

        M_neto = math.sqrt((M_L - M_V)**2 + (M_T - M_V)**2)

        #F_RL:  Fuerza resultante por cargas laterales [kN]
        F_RL = math.sqrt(F_x**2 + F_y**2)

        return M_neto / F_RL

    def _calcular_φ(self, prof_ini, prof_fin) -> float:
        """calcula φ teniendo en cuenta las tangentes de φ y devuelve
            el promedio menos una desviación estandar        
        """

        perfil, = self.get_atributos("perfil")
        
        d = 0.0 
        h_acum = 0.0
        acum = 0.0
        lista_tanφ = []
        for estrato in perfil:
            if estrato.tipo_mat == 'g':
                if d + estrato.H_0 > prof_ini and d < prof_fin:
                    if d < prof_ini:
                        if d + estrato.H_0 > prof_fin:
                            dH = prof_fin - prof_ini
                        else:
                            dH = d + estrato.H_0 - prof_ini
                    elif d + estrato.H_0 > prof_fin:
                        dH = prof_fin - d
                    else:
                        dH=estrato.H_0
                    lista_tanφ.append(tan_g(estrato.φ_s))
                    acum += tan_g(estrato.φ_s) * dH #tangente de φ * dH
                    h_acum += dH
                elif d >= prof_fin:
                    break
            d += estrato.H_0

        if h_acum == 0:
            raise ValueError('En el segmento no se encuentran estratos granulares')
        
        if len(lista_tanφ) > 1:
            tan_φ = acum / h_acum - statistics.stdev(lista_tanφ)
        else:
            tan_φ = acum / h_acum
        
        if tan_φ > 1:
            raise ValueError(f'El valor de tan_φ promedio {tan_φ} es mayor que 1 ') 

        φ = math.atan(tan_φ) * 180 / π # usar atan2 ojo !!!!!!

        return φ 

    def _calcular_c_u(self, prof_ini, prof_fin) -> float:
        """calcula c_u  y devuelve
            el promedio menos una desviación estandar        
        """

        perfil, = self.get_atributos("perfil")
        
        d = 0.0 
        h_acum = 0.0
        acum = 0.0
        lista_c_u = []
        for estrato in perfil:
            if estrato.tipo_mat == 'c':
                if d + estrato.H_0 > prof_ini and d < prof_fin:
                    if d < prof_ini:
                        if d + estrato.H_0 > prof_fin:
                            dH = prof_fin - prof_ini
                        else:
                            dH = d + estrato.H_0 - prof_ini
                    elif d + estrato.H_0 > prof_fin:
                        dH = prof_fin - d
                    else:
                        dH=estrato.H_0
                    lista_c_u.append(estrato.c_u)
                    acum += estrato.c_u * dH #tangente de φ * dH
                    h_acum += dH
                elif d >= prof_fin:
                    break
            d += estrato.H_0

        if h_acum == 0:
            raise ValueError('En el segmento no se encuentran estratos cohesivos')
        
        if len(lista_c_u) > 1:
            c_u = acum / h_acum - statistics.stdev(lista_c_u)
        else:
            c_u = acum / h_acum
            
        return c_u

    def _calcular_longitud_transicion_granular(self, P, cargas) -> float: 
        """Calcula la longitud transicion para el caso granular
        """    
        
        D_p, D, H, perfil = self.get_atributos("D_p", "D", "H", "perfil")

        # e: Excentricidad por carga horizontal [m]
        e = self._calcular_excentricidad(cargas)
        
        #φ : Angulo de fricción del suelo [°]
        φ = self._calcular_φ(D - H, D)  

        #γ : Peso unitario del suelo [kN/m³]
        γ = perfil.calcular_promedio(D - H, D, 'γ_se')

        #k_p : coeficiente de presion pasiva [adim]
        k_p = tan_g(45 + φ / 2)**2

        a = γ * D_p * k_p
        b = 2 * P
        c = 2 * P * e

        #L_t_g : Longitud de transicion [m]
        raices = np.roots([a, 0, -b, -c])
        raices_positivas = np.where(raices > 0, raices, 0)
        L_t_g = max([float(raiz) for raiz in raices_positivas])

        return L_t_g

    def set_perfil(self, perfil: Perfil):
        self.perfil = perfil
        info_mat_relleno = self.perfil.calcular_material_relleno(self.D - self.H)
        self.tipo_mat_r, self.φ_r, self.c_u_r, self.γ_r  = (info_mat_relleno["tipo_mat"], info_mat_relleno["φ"], info_mat_relleno["c_u"], info_mat_relleno["γ"])

    ######################################################################
    # Cálculos capacidad portante 
    ######################################################################

    def calculo_capacidad_portante(self) -> Tuple[float, float, float, Memoria, Memoria]:
        """
        Calcula las capacidad portante
        
        Arguments:
            

        Returns:
            Tuple[float, float,float, Memoria, Memoria] -- (q_ult: Capacidad portante ultima [kN],
                                                            q_p: Capacidad portante por punta
                                                            q_s: Capacidad portante por fuste
                                                            memoria_p: memoria punta
                                                            memoria_s :memoria fuste)

        """

        D_c, D, perfil  = self.get_atributos("D_c", "D", "perfil")
        

        # φ_D: Ángulo de fricción para calcular el límite inferior del suelo relevante [°]
        φ_D = perfil.estrato_en(D).φ_s

        # B_lim: límite inferior del suelo relevante [m]
        B_lim = D_c * tan_g(45 + φ_D / 2)

        # Porcentajes de tipos de material de suelo entre D y D + B_lim
        porcentajes = perfil.calcular_porcentaje_tipo_mat(D, D + B_lim)

        # Se prefiere la formulación de suelos cohesivos si ellos constituyen el 30% o más
        if porcentajes["c"] >= 30.0:
            q_p, memoria_p = self._calculo_de_capacidad_portante_punta_cohesivo()
            q_s, memoria_s = self._calculo_de_capacidad_portante_fuste()
            q_ult = q_p + q_s
            return q_ult, q_p, q_s, memoria_p, memoria_s
        else:
            q_p, memoria_p = self._calculo_de_capacidad_portante_punta_granular()
            q_s, memoria_s = self._calculo_de_capacidad_portante_fuste()
            q_ult = q_p + q_s 
            return q_ult, q_p, q_s, memoria_p, memoria_s

    def _calculo_de_capacidad_portante_punta_granular(self) -> Tuple[float, Memoria]:
        
        """Calcula la capacidad portante por punta 

            para suelo granular
        """

        D_c, D, perfil  = self.get_atributos("D_c", "D", "perfil")
        
        # φ_D: Ángulo de fricción para calcular el límite inferior del suelo relevante [°]
        φ_D = perfil.estrato_en(D).φ_s

        # B_lim: límite inferior del suelo relevante [m]
        B_lim = D_c * tan_g(45 + φ_D / 2)
        
        # φ: Ángulo de fricción del suelo relevante [°]
        φ = perfil.calcular_promedio(D, D + B_lim, "φ_s", tipo_mat="g")
        
        # N_q_as: Factor de capacidad portante debido a la sobrecarga. [-]
        N_q_as = self._interpolar_N_q(φ)  # es diferente al de zapatas 
        
        # q: Esfuerzo de sobrecarga efectivo a la profundidad de cimentación [kN/m²]
        q = perfil.calcular_q(D)

        # A_p: Área de la pila en la punta [m²]
        A_p = π / 4 * D_c ** 2

        #Q_p: Capacidad portante en la punta [kN]
        Q_p = q * N_q_as * A_p
        
        #memoria
        memoria = {"D_c":D_c , "q":q, "N_q_as" :N_q_as,  "A_p":A_p}

        return (Q_p, memoria)

    def _calculo_de_capacidad_portante_punta_cohesivo(self) -> Tuple[float, Memoria]:
        
        """Calcula la capacidad portante por punta 

            para suelo cohesivo
        """
        
        D_c, D,  perfil  = self.get_atributos("D_c", "D","perfil")

        # φ_D: Ángulo de fricción para calcular el límite inferior del suelo relevante [°]
        φ_D = perfil.estrato_en(D).φ_s

        # B_lim: límite inferior del suelo relevante [m]
        B_lim = D_c * tan_g(45 + φ_D / 2)

        # A_p: Área de la pila en la punta [m²]
        A_p = π / 4 * D_c ** 2
    
        # c_u: Resistencia no drenada [kN/m²]  se le resta una desviacion estandar
        c_u = perfil.calcular_promedio(D, D + B_lim, "c_u")
        
        Q_p = 9 * c_u  * A_p
        
        memoria = {"D_c":D_c, "A_p":A_p, "c_u":c_u}

        return (Q_p, memoria)

    def _calculo_de_capacidad_portante_fuste(self) -> Tuple[float, Memoria]: 
        
        """Calcula la capacidad portante por fuste"""
        
        D, H, h_c, D_p, perfil, campana  = self.get_atributos("D", "H", "h_c", "D_p", "perfil", "campana")

        # Capacidad portante en el fuste [kN]
        iteraciones = []
        d = 0.0  # prof. ini de capa actual
        prof_ini = D - H 

        if campana:
            prof_fin = D - h_c
        else:
            prof_fin = D

        Q_s = 0.0
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

                if estrato.tipo_mat == "g":
                    q = perfil.calcular_q(z)
                    φ_s = estrato.φ_s
                    δ = φ_s * 2 / 3
                    K = 1 - sin_g(estrato.φ_s)
                    A_s = π * D_p * Δ_z
                    Q_s += K * q * A_s * tan_g(δ)
                    
                    iteraciones.append({"d":d, "Δ_z":Δ_z, "z":z, "q":q, "φ_s":φ_s, "K":K, "A_s":A_s, "Q_s":Q_s})

                elif estrato.tipo_mat == "c":
                    c_u = estrato.c_u
                    α = min(1 , 0.21 + 0.26 * 100 / c_u) 
                    A_s = π * D_p * Δ_z
                    Q_s += α * c_u * A_s

                    iteraciones.append({"d":d, "Δ_z":Δ_z, "z":z, "c_u":c_u, "α":α, "A_s":A_s, "Q_s":Q_s})
                
                else:
                    raise ValueError(f"Cálculo de capacidad del fuste en roca. profundidad = {d}")

            d += estrato.H_0

        #memoria
        memoria = {"iteraciones": iteraciones}

        return (Q_s , memoria)

    ######################################################################
    # Cálculos arrancamiento
    ######################################################################

    def calculo_tension(self) -> Tuple[float, Memoria]:
        """
        Calcula las capacidad a la tensión
        
        Arguments:
            
        Returns:
            Tuple[float, Memoria] -- (T_Fv: Capacidad a la tensión última [kN], memoria)

        """
        #to do:
            #Calcular cual da mas crítico entre granular y cohesivo e ir con el mas desfavorable 
            #por el momento está cohesivo
        
        D, perfil = self.get_atributos("D", "perfil")

        # Porcentajes de tipos de material de suelo entre 0 y D
        porcentajes = perfil.calcular_porcentaje_tipo_mat(0, D)
        
        if porcentajes["c"] >= 30.0:
            T_tp, memoria_tp = self._calculo_tension_tronco_piramidal_cohesivo()
        else:
            T_tp, memoria_tp = self._calculo_tension_tronco_piramidal_granular()

        T_fv, memoria_fv = self._calculo_tension_falla_vertical()
        
        if T_fv < T_tp:
            return T_fv, memoria_fv
        else:
            return T_tp, memoria_tp

    def _calculo_tension_falla_vertical(self) -> Tuple[float, Memoria]:
        
        """Calcula resistencia al arrancamiento

        mediante el método de falla vertical
        """

        campana, D_c, D_p, H, D, perfil = self.get_atributos("campana", "D_c", "D_p", "H", "D", "perfil")
        
        if campana:
            
            c_u = c_u = perfil.calcular_promedio(0, D, "c_u")
            
            T_un_1 = π / 4 * (D_c**2 - D_p**2) * 9 * c_u 

            T_un_2 =  π * (D_c + D_p) / 2 * c_u * H  

            if T_un_1 < T_un_2:
                T_fv = T_un_1 + self.peso()
                memoria_s = {"D_c":D_c, "D_p":D_p, "c_u":c_u }

            else:
                T_fv = T_un_2 + self.peso()
                memoria_s = {"D_c":D_c, "D_p":D_p, "c_u":c_u, "H":H}

        else:

            Q_s, memoria_s = self._calculo_de_capacidad_portante_fuste_tension()
            T_fv = Q_s + self.peso()

        return (T_fv, memoria_s)       

    def _calculo_de_capacidad_portante_fuste_tension(self) -> Tuple[float, Memoria]: 
        
        """Calcula la capacidad portante por fuste"""
        
        D, H, h_c, D_p, perfil, campana  = self.get_atributos("D", "H", "h_c", "D_p", "perfil","campana")

        # Capacidad portante en el fuste [kN]
        iteraciones = []
        d = 0.0  # prof. ini de capa actual
        prof_ini = D - H

        if campana:
            prof_fin = D - h_c
        else:
            prof_fin = D
        
        Q_s = 0.0
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

                if estrato.tipo_mat == "g":
                    q = perfil.calcular_q(z)
                    φ_s = estrato.φ_s
                    δ = φ_s * 2 / 3
                    K = 1 - sin_g(estrato.φ_s)
                    A_s =  A_s = π * D_p * Δ_z
                    Q_s += (2 / 3) * K * q * A_s * tan_g(δ)
                    
                    iteraciones.append({"d":d, "Δ_z":Δ_z, "z":z, "q":q, "φ_s":φ_s, "K":K, "A_s":A_s, "Q_s":Q_s})

                elif estrato.tipo_mat == "c":
                    c_u = estrato.c_u
                    α = min(1 , 0.21 + 0.26 * 100 / c_u) 
                    A_s = A_s = π * D_p * Δ_z
                    Q_s += α * c_u * A_s

                    iteraciones.append({"d":d, "Δ_z":Δ_z, "z":z, "c_u":c_u, "α":α, "A_s":A_s, "Q_s":Q_s})
                
                else:
                    raise ValueError(f"Cálculo de capacidad del fuste en roca. profundidad = {d}")

            d += estrato.H_0

        #memoria
        memoria = {"iteraciones": iteraciones}

        return (Q_s , memoria)

    def _calculo_tension_tronco_piramidal_granular(self) -> Tuple[float, Memoria]:

        """Calcula resistencia a la tensión 
        
        mediante el método de tronco piramidal para suelo cohesivo
        """

        D, H, D_c, perfil = self.get_atributos("D","H", "D_c", "perfil")

        # A_p: Área de la pila en la punta [m²]
        A_p = π / 4 * D_c**2
        
        # φ: Ángulo de fricción del suelo relevante [°]
        φ = perfil.calcular_promedio(0, D, "φ_s", tipo_mat="g")
        
        #K_u: coeficiente nominal de levantamiento [adimensional]
        k_u = self._interpolar_ku(φ)

        #m : Coeficiente de factor de forma [adimensional]
        m = self._interpolar_m(φ)
        
        #B_q: Factor de arrancamiento
        B_q = 2 * H * k_u * tan_g(φ) / D_c * (m * H / D_c + 1) + 1

        # γ_s:  Peso unitario promedio del suelo hasta la profundidad D [kN/m³]
        γ_s = perfil.calcular_promedio_γ(D)

        # T_ug : Carga a tensión
        T_ug = B_q * A_p * γ_s * H 
        
        #T_un: Carga última a tensión 
        T_tp = T_ug + self.peso()

        memoria = {"A_p":A_p, "γ_s":γ_s, "φ":φ, "k_u":k_u, "m":m, "B_q":B_q, "T_ug":T_ug, "D_c":D_c}

        return (T_tp, memoria)

    def _calculo_tension_tronco_piramidal_isa(self) -> Tuple[float, Memoria]:

        """Calcula resistencia a la tensión mediante el método de tronco piramidal
            para suelo cohesivo
        """
        D, H, D_c, D_p, campana, perfil = self.get_atributos("D", "H", "D_c", "D_p", "campana", "perfil")
        
        # A_p: Área de la pila en la punta [m²]
        A_p = π / 4 * D_c**2

        # W: peso pila [kN]
        W = self.peso()

        # γ_s:  Peso unitario promedio del suelo hasta la profundidad D [kN/m³]
        γ_s = perfil.calcular_promedio_γ(D)

        # ψ: Ángulo de inclinación de las paredes del cono [°]
        ψ = 15

        if campana:
            Qsw = π * γ_s * H * (D_c**2 / 2 + D_c * H * tan_g(ψ) / 2 + H**2 * tan_g(ψ)**2 / 3)
        else:
            Qsw = π * γ_s * H * (D_c**2 / 2 + D_c * H * tan_g(ψ) / 2 + H**2 * tan_g(ψ)**2 / 3  + (D_c**2 - D_p**2) / 4)

        # c_u: Cohesión no drenada del suelo [kN/m²]
        c_u = perfil.calcular_promedio(0, D, "c_u") # promedio de c_u de los estratos cohesivos

        #H_D_critica : relación Longitud y diametro crítica según Das (2001) [adim]
        H_D_critica = min(7, 0.107 * c_u + 2.5)

        #relacion_H_D : relacion entre relacion H y D_c y relacion critica [adim]
        relacion_H_D = (H / D_c) / H_D_critica

        # β: Factor de desconexión 
        if relacion_H_D > 1:
            B_c = 9
        else:
            B_c = self._interpolar_B_c(relacion_H_D)

        # γ_s:  Peso unitario promedio del suelo hasta la profundidad D [kN/m³]
        γ_s = perfil.calcular_promedio_γ(D)

        #T_un: Carga última a tensión 
        T_tp = c_u * B_c + γ_s * H * A_p

        memoria = {"D_c":D_c, "c_u":c_u, "B_c":B_c, "A_p":A_p, "γ_s":γ_s, "H":H }

        return (T_tp, memoria)

    ######################################################################
    # Cálculos carga lateral
    ######################################################################

    def calculo_carga_lateral(self, cargas:dict) -> Tuple[float, bool, Memoria]:
        """Calcula Carga lateral 

        Arguments:
            cargas {dict} -- diccionario con todos los casos de carga principales para calcular excentricidad
        
        Returns:
            Tuple[float, bool, Memoria] -- (P: resistencia lateral [m], condición de pila corta , memoria)

        """
        H, D, perfil = self.get_atributos("H", "D", "perfil")

        # Porcentajes de tipos de material de suelo entre D - H y D
        porcentajes = perfil.calcular_porcentaje_tipo_mat(D - H, D)

        # Se prefiere la formulación de suelos cohesivos si ellos constituyen el 30% o más
        if porcentajes["c"] >= 30.0:
            P, p_corta, memoria_p = self._calculo_carga_lateral_pila_cohesivo(cargas)
            return P, p_corta, memoria_p
        else:
            P, p_corta, memoria_p = self._calculo_carga_lateral_pila_granular(cargas)
            return P, p_corta, memoria_p

    #Este método requiere las cargas
    def _calculo_carga_lateral_pila_granular(self,cargas:dict) -> Tuple[float, bool, Memoria]:
        """Calcula carga lateral para pila suelo granular
        """
        D_p, D, H, perfil = self.get_atributos("D_p", "D", "H", "perfil")
        
        # e: Excentricidad por carga horizontal [m]
        e = self._calcular_excentricidad(cargas)

        # φ : Angulo de friccion interno del suelo[°]
        φ = self._calcular_φ(D - H, D)

        #γ: Peso unitario del suelo[kN/m³]
        γ = perfil.calcular_promedio(D - H, D, 'γ_se')

        #k_p: coeficiente de presion pasiva del suelo[-]
        k_p = tan_g(45 + φ / 2)**2

        # A_p: Área de la pila en la punta [m²]
        A_p = math.pi / 4 * D_p**2

        #B_equiv: Lado equivalente de una pila cuadrada [m]
        B_equiv = math.sqrt(A_p)

        # M_y: Momento de fluencia[kN m]
        M_y = 3236.211 * B_equiv * (B_equiv - 0.06)**2

        objetivo = 0.0001
        epsilon = 0.0001
        bajo = 0.0
        alto = 50000
        P = (alto + bajo) / 2 

        while abs((P - M_y / (e + 0.544 * math.sqrt( P /(γ * D_p * k_p)))) - objetivo) >= epsilon:
                        
            if (P - M_y / (e + 0.544 * math.sqrt( P /(γ * D_p * k_p)))) < objetivo:
                bajo = P
            else:
                alto = P
            
            #P : Resistencia a carga lateral [kN]
            P = (alto + bajo) / 2

        # L_e: Longitud transicion , si H < Le la pila es corta 
        L_e = self._calcular_longitud_transicion_granular(P, cargas)

        # ¿¿¿ Aquí se reemplazaría H donde va  L_e o se deja L_e?
        if H < L_e:
            p_corta = True
            P = 0.5 * γ * D_p * L_e**3 * k_p / (e + L_e)
        else:
            p_corta = False

        memoria = {"e":e , "φ":φ, "γ":γ, "k_p":k_p, "A_p":A_p, "B_equiv":B_equiv, "M_y":M_y, "L_e":L_e}

        return P, p_corta, memoria

    #Este método requiere las cargas
    def _calculo_carga_lateral_pila_cohesivo(self, cargas:dict) -> Tuple[float, bool, Memoria]:
        """Calcula carga lateral para pila suelo cohesivo
        """
        D_p, D, H = self.get_atributos("D_p", "D", "H")

        # e: Excentricidad por carga horizontal [m]
        e = self._calcular_excentricidad(cargas)
        
        # c_u: Cohesión no drenada del suelo [kN/m²]
        c_u = self._calcular_c_u(D - H, D)

        # A_p: Área de la pila en la punta [m²]
        A_p = π / 4 * D_p**2

        # B_equiv : Lado equivalente de una pila cuadrada [m]
        B_equiv = math.sqrt(A_p)

        # M_y: Momento de fluencia[kN m]    3234 = 0.65 * 0.5% * fy
        M_y = 3236.211 * B_equiv * (B_equiv - 0.06)**2

        #a, b ,c : parametros de la ecuación cuadrática
        a = 1 / (18 * c_u * D_p)
        b = e + 1.5 * D_p
        c = - M_y
        
        #P: carga para pila larga  
        P = (-b + math.sqrt(b**2 - 4 * a * c)) / (2 * a)
        
        #f: Longitud hasta zona de momento maximo [m]
        f = P / (9 * c_u * D_p)
        
        # g: longitud desde zona de momento maximo hasta final de la pila[m]
        g = math.sqrt(M_y / (2.25 * c_u * D_p))

        #L_e: Longitud de transicion [m]
        L_e = 1.5 * D_p + f + g

        # ¿¿¿ Aquí se reemplazaría H pdonde va  L_e o se deja L_e?
        if H < L_e:
            p_corta = True
            #a1, b1, c1 : parametros de la ecuación cuadrática
            a1 = 1
            b1 = 36 * c_u * D_p * e + 27 * c_u * D_p**2 + 18 * c_u * D_p * L_e
            c1 = -81 * c_u**2 * D_p**2 * (L_e - 1.5 * D_p)**2
            
            #P: carga ultima pila corta 
            P = (-b1 + math.sqrt(b1**2 - 4 * a1 * c1)) / (2 * a1)
        else:
            p_corta = False

        memoria = {"e":e , "c_u":c_u, "A_p":A_p, "B_equiv":B_equiv, "M_y":M_y, "P":P, "f":f, "g":g, "L_e":L_e,} 
        
        return P, p_corta, memoria

    def calculo_modulos_de_reaccion_horizontal(self) -> Tuple[float , Memoria]:
    
        # tabla con datos de una a otra profncidad tal k / Resuelto
        #I_p : Momento de inercia de la sección [m⁴]
        #E_s : Módulo de elasticidad del suelo [kN/m²]
        #ν : Relación de poisson [-]
        #k: Módulo de reacción horizontal [kN/m³]

        perfil, D_p, h_i, H, E_p = self.get_atributos("perfil", "D_p", "h_i", "H", "E_p")

        prof_ini = h_i
        prof_fin = h_i + H
        I_p = π * D_p**4 / 64
        metros = generar_serie(1, H, 1, 0)
        
        k = []
        for m in metros:
            dH = 0.0
            dH_acum = 0.0
            d = 0.0
            for estrato in perfil:
                if d + estrato.H_0 > prof_ini and d < prof_fin:
                    if d < prof_ini:
                        if d + estrato.H_0 > prof_fin:
                            dH = prof_fin - prof_ini
                        else:
                            dH = d + estrato.H_0 - prof_ini
                    elif d + estrato.H_0 > prof_fin:
                        dH = prof_fin - d
                    else:
                        dH=estrato.H_0
                elif d >= prof_fin:
                        break
                
                dH_acum += dH
                
                if m <= dH_acum:
                    k.append((0.65 / D_p) * (estrato.E_s * D_p**4 / E_p / I_p)**(1/12) * (estrato.E_s / (1 - estrato.ν**2)))
                    break
                
                d += estrato.H_0
        
        return k

    ######################################################################
    # Cálculos volcamiento
    ######################################################################

    # Se usa si es pila corta H < Le 
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

        # τ_adm : resistencia fuste  [kN]
        τ_adm, _ = self._calculo_de_capacidad_portante_fuste() 

        # M_wc : Momento estabilizador por peso de la cimentación [kN·m]
        M_wc = (self.peso()+ self.peso_relleno()) * D_p / 2

        #acum: area acumulada correspondiente al empuje pasivo [m²]
        acum = self._calculo_integral_presion_lateral_pasiva(D - H, D)       

        #areas_por_brazos: sumatoria de areas por brazos que componen el area respecto al empuje pasivo desde el inicio de la pila [m³]
        areas_por_brazos = self._calcular_areas_por_brazos(D)
        
        #centroide: centroide del area acumulada correspondiente al empuje pasivo, se mide hasta la profundidad D 
        centroide = areas_por_brazos / acum

        # R_p : Fuerza debida a Empuje pasivo en la pila  [kN]
        R_p = self._calculo_integral_presion_lateral_pasiva(D - H, D) * D_p * r

        # M_p : Momento por Empuje pasivo en la pila  [kN·m]
        M_p = R_p * centroide

        # F_r : Friccion por contacto fuste  [kN]
        F_r = τ_adm * π * D_p * H / 2

        # M_fr : Momento por Friccion fuste  [kN·m]
        M_fr = F_r * D_p * ( 1 / 2 + 1 / π )
                
        # Me: Momento estabilizador [kN·m]
        Me = M_wc + M_p + M_fr

        # Mv:  Momento de vuelco [kN·m]
        Mv = F_zc * (D_p / 2 - C * tan_g(θ)) + F * (C + H)

        # memoria
        memoria = {"M_wc": M_wc, "R_p": R_p, "M_p": M_p, "F_r": F_r, "M_fr":M_fr, "τ_adm":τ_adm}

        return (Mv, Me, memoria)

    def _calcular_areas_por_brazos(self, prof:float) -> float:
        """Calcula  el producto de las areas correspondientes al empuje lateral por sus respectivos
            brazos desde el inicio de la pila

            Se usa para calcular el centroide de la fuerza resultante por empuje pasivo 

            Returns:
            {float} -- areas_por_brazos: area representativa de empuje lateral de cada trapecio por su brazo correspondiente  desde el inicio de la pila [kN]
                                    
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

            if z + estrato.H_0 <= D - H:
                areas_por_brazos += 0
            else:
                areas_por_brazos += area_rectangulo * brazo_rectangulo + area_triangulo * brazo_triangulo
            
            acum_esf_vert += estrato.γ_rse * Δ_z
            z += estrato.H_0

        return areas_por_brazos
        
    def _calculo_integral_presion_lateral_pasiva(self, prof_ini, prof_fin):
        """Calcula la integral de la presión lateral pasiva desde la profundidad 'prof_ini' hasta la profundidad 'prof_fin'
        
            Returns:
            float -- ( acum: empuje lateral acumulado de los trapecios desde profundidad inicial hasta profundidad final [kN/m])

        """
        return self._calculo_integral_presion_lateral_pasiva_desde_0(prof_fin) - self._calculo_integral_presion_lateral_pasiva_desde_0(prof_ini)

    def _calculo_integral_presion_lateral_pasiva_desde_0(self, prof):
        """Calcula la integral de la presión lateral pasiva desde la profundidad 0 hasta la profundidad 'prof'
            
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
            
            acum_esf_vert += estrato.γ_rse * Δ_z
            acum += (p + p_ant) / 2 * Δ_z
            z += estrato.H_0

        return acum

    ######################################################################
    # Cálculos asentamiento
    ######################################################################
        
    def calculo_asentamiento(self, F_zc_eds:float) -> Tuple[float, float, Memoria, Memoria]:
        """Calcula asentamiento elastico y por consolidación

            asentamiento elastico por metodo de vesic o por metodo de transferencia 
        """

        q_ult, q_p, q_s, _, _ = self.calculo_capacidad_portante()

        S_transferencia, memoria_t = self._calculo_asentamiento_transferencia(q_s, q_p)
        
        S_vesic, memoria_v  = self._calculo_asentamiento_vesic(q_ult)
        
        if S_transferencia > S_vesic:
            S_e , memoria_e = S_transferencia, memoria_t
        else:
            S_e , memoria_e = S_vesic, memoria_v

        S_c , memoria_c = self._calculo_asentamiento_por_consolidacion(F_zc_eds)

        return S_e, S_c , memoria_e, memoria_c 
    
    #utiliza el módulo de la pila
    def _calculo_asentamiento_transferencia(self, q_s:float, q_p:float) -> Tuple[float, Memoria]:
        
        # q_s y q_p aplicar factor de seguridad  / factor de seguridad

        """
        Calcula el asentamiento elástico por el método de tranferencia de carga
        q_s {float}  -- Capacidad portante fuste 
        q_p {floar} -- Capacidad portante punta 
        """

        D_p, D_c, H, D, perfil, E_p  = self.get_atributos("D_p", "D_c", "H", "D", "perfil", "E_p")

        #A_s: Area del fuste [m²]
        A_s = π * D_p**2 / 4

        #A_p : Area de la pila [m²]
        A_p = π * D_c**2 / 4

        #E_s : Modulo de elasticidad del suelo [kN/m²]
        E_s = perfil.calcular_promedio(D, D + 2 * D_c, "E_s")

        #ν : Relación de poisson [adim]
        ν = perfil.calcular_promedio(D, D + 2 * D_c, "ν")
        
        #I_p: Factor de influencia que relaciona longitud de pila con diametro[-]
        I_p = 0.5   # segun libro de tomlinson

        #S_t : Asentamiento calculado por método de transferencia [m]
        S_t = (q_s + 2 * q_p) * H / (2 * A_s * E_p) + (π * q_p * D_c * (1 - ν**2) * I_p) / (4 * A_p * E_s) 

        memoria = {"A_s":A_s, "A_p":A_p, "E_p":E_p, "E_s":E_s, "ν":ν, "I_p":I_p, }
        
        return S_t, memoria

    #utiliza el módulo de la pila
    def _calculo_asentamiento_vesic(self, q_ult:float) -> Tuple[float, Memoria]:
        #q ult sobre factor de seguridad
        
        """ 
        Calcula el asentamiento elástico por el método de vésic

        q_ult {float} -- Capacidad portante ultima [kPa]
        """
        D_c, H, E_p  = self.get_atributos("D_c", "H", "E_p")

        #A_p: Area de la pila
        A_p = π * D_c**2 / 4

        #este metodo tiene en cuenta el 1% del diametro 3m --> 3cm
        #es q_ult o es applied pile load ?
        #S_v : Asentamiento calculado por metodo de vesic [m]
        S_v = D_c / 100 + q_ult * H / A_p / E_p 

        memoria = {"D_c":D_c, "E_p":E_p, "A_p":A_p, "q_ult":q_ult}

        return S_v, memoria

    def _calculo_asentamiento_por_consolidacion(self, F_zc:float) -> Tuple[float, Memoria]:
        
        """
        Calcula el asentamiento por consolidación

        Arguments:
            F_zc {float} -- Componente vertical de la carga a compresión [kN], debe ser las cargas EDS (diarias)
        
        Returns:
            Tuple[float, Memoria] -- (S: Asentamiento por consolidación [m], memoria)
        """
        D_c, D, perfil = self.get_atributos("D_c", "D", "perfil")
        
        #B equivalente
        B = L = D_c**0.5

        # W_c:  Peso de la cimentación [kN]
        W_c = self.peso()
        
        # W_c:  Peso del relleno [kN]
        W_r = self.peso_relleno()

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

                    # σ_pp: 
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

