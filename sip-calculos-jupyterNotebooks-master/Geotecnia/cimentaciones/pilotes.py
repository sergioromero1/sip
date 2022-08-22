import math
import copy
import numpy as np
import statistics
from typing import List, Dict, Tuple, Any
from .util import sin_g, cos_g, tan_g, cot_g, γ_agua, π, calcular_C_d, Memoria, calcular_I_f, rad, generar_serie
from .perfil import Perfil, Estrato

class Pilotes:
    """
    Cimentación tipo pilote en suelo          

    Attributes:
        D_f {float} -- Profundidad de la zapata [m]
        H_z {float} -- altura del dado [m]
        n {float} -- Numero de pilotes[m]
        S_p {float} -- Separacion mínima de pilotes[m]
        D_p {float} --  Diámetro de los pilotes [m]
        H {float} --    Longitud de pilotes [m]
        HG {float} -- Altura del pedestal no enterrado [m]
        h_c {float} --  Altura de la campana [m]
        h_con {float}-- Altura de la sección conica de la campana[m]
        θ_c {float} --  Ángulo de la campana [°]
        TP {float} --   Lado correspondiente a la sección transversal del pedestal [m]
        θ {float} --    Ángulo del pedestal respecto a la vertical [°]
        γ_c {float} --  Peso unitario del material de la cimentación [kN/m³]
        d_bor {float] -- Distancia del pilote al borde del dado [m]
        f_carga_p {float} -- Fracción de carga que toman los pilotes [-]
        perfil {Perfil} -- Perfil estratigráfico en el suelo del pilote
        hincado {bool} -- Boleano que define condicion del pilote hincado o preexcavado
        campana{bool} -- Boleano que define condicion del pilote con o sin campana
        ω {float} -- Ángulo de inclinación del terreno [°]
    """
    ######################################################################
    # Constructor
    ######################################################################

    def __init__(self, D_f: float, H_z: float,
                        n:float, S_p:float,
                        D_p:float,
                        H:float, HG:float,
                        h_c:float, θ_c:float,
                        h_con:float,
                        TP:float, θ:float, 
                        γ_c:float, E_p:float,
                        d_bor:float,
                        f_carga_p: float, perfil:Perfil,
                        hincado:bool, campana:bool,
                        ω: float
                        ):

        """
        Inicializa el pilote
        
        Arguments:
        D_f {float} -- Profundidad de la zapata [m]
        H_z {float} -- altura del dado [m]
        n {float} -- Numero de pilotes[m]
        S_p {float} -- Separacion mínima de pilotes[m]
        D_p {float} --  Diámetro de los pilotes [m]
        H {float} --    Longitud de pilotes [m]
        HG {float} -- Altura del pedestal no enterrado [m]
        h_c {float} --  Altura de la campana [m]
        h_con {float}-- Altura de la sección conica de la campana[m]
        θ_c {float} --  Ángulo de la campana [°]
        TP {float} --   Lado correspondiente a la sección transversal del pedestal [m]
        θ {float} --    Ángulo del pedestal respecto a la vertical [°]
        γ_c {float} --  Peso unitario del material de la cimentación [kN/m³]
        E_p {float} -- Módulo de elasticidad del pilote [kPa]
        d_bor {float -- Distancia del pilote al borde del dado [m]
        f_carga_p {float} -- Fracción de carga que toman los pilotes [-]
        perfil {Perfil} -- Perfil estratigráfico en el suelo del pilote
        hincado {bool} -- Boleano que define condicion del pilote hincado o preexcavado
        campana{bool} -- Boleano que define condicion del pilote con o sin campana
        ω {float} -- Ángulo de inclinación del terreno [°]

        """

        self.D_f = D_f
        self.H_z = H_z
        self.n = n
        self.D_p = D_p
        self.H = H
        self.h_c = h_c
        self.h_con = h_con
        self.θ_c = θ_c
        self.HG = HG
        self.TP = TP
        self.θ = θ 
        self.γ_c = γ_c
        self.E_p = E_p
        self.d_bor = d_bor
        self.f_carga_p = f_carga_p
        self.perfil = perfil
        self.hincado = hincado
        self.campana = campana
        self.ω = ω
        self.D_c = self.D_p
        self.e = perfil.prof_lic_final - perfil.prof_lic_inicial if perfil.prof_lic_inicial is not None else 0

        info_mat_relleno = self.perfil.calcular_material_relleno(self.D_f - self.H_z)
        self.tipo_mat_r, self.φ_r, self.c_u_r, self.γ_r  = (info_mat_relleno["tipo_mat"], info_mat_relleno["φ"], info_mat_relleno["c_u"], info_mat_relleno["γ"])        

        self.validar_atributos()

        if hincado:
            campana = False

    
        #D_c {float} --  Diámetro de la campana del pilote [m]. Si es pilote con punta recta D_c == D_p
        if campana:
            self.D_c = self.D_p + tan_g(self.θ_c) * self.h_con * 2    #0.35 a la altura de la parte con pendiente de la campana, y 2 corresponde a dos lados
        
        #S_p: Separacion de pilotes [m]
        self.S_p = 2 * cos_g(45) * S_p if n and n == 5 else S_p

        # t {float} -- Distacia de la cresta del talud al centro de la zapata que contiene los pilotes
        self.t = self.D_f / tan_g(ω) if ω and ω > 0 else None

        #h. Altura de relleno 
        self.h = self.D_f - self.H_z

        # S_ep: Separación entre pilotes exteriores [m]
        self.S_ep = self.S_p * (self.N_pL - 1)

        # x,y: Dimensiones efectivas del bloque que conforman los pilotes
        self.x = self.y = self.S_ep + self.D_c

        #Diametro para un pilote que cubre el area del grupo de pilotes [m]
        self.x_c = self.x

        if campana:
            self.x_c = self.x + tan_g(self.θ_c) * self.h_con * 2

        
    ######################################################################
    # Propiedades
    ######################################################################

    # B: Ancho de la zapata [m]    
    def get_B(self):
        # B = 2 * self.dist_bor + (self.N_pL - 1) * self.S_p * math.sqrt(1 + tan_g(self.θ)**2) + 2 * self.P_anc * tan_g(self.θ)
        B = self.S_ep + self.D_c + 2 * self.d_bor
        return B
    B = property(get_B)

    # N_mL: Número de pilotes por lado
    def get_N_pL(self):
        return math.floor(self.n / 4 + 1)
    N_pL = property(get_N_pL)

    # C: Altura total del pedestal [m]
    def get_C(self):
        return self.D_f + self.HG - self.H_z
    C = property(get_C)

    # D : Profundidad de desplante del pilote [m]
    def get_D(self):
        return self.D_f + self.H
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

    def get_volumen_cono(self):
        B, D_f, H_z, C, HG, TP, θ  = self.get_atributos("B", "D_f", "H_z", "C", "HG", "TP", "θ")
        V_c = (B**2 * H_z +  TP**2 * (C - HG) / cos_g(θ)) 
        A_n = 30
        V_cono = D_f / 3 * (B**2 + (B + 2 * D_f * tan_g(A_n))**2 + math.sqrt(B**2 + (B + 2 * D_f * tan_g(A_n))**2 ) ) - V_c
        return V_cono
    volumen_cono = property(get_volumen_cono)

    def get_peso_cono(self):
        D_f, H_z, perfil = self.get_atributos("D_f", "H_z", "perfil")

        info_relleno = perfil.calcular_material_relleno(D_f - H_z)
        γ_r = info_relleno["γ"]

        return self.volumen_cono * γ_r
    peso_cono = property(get_peso_cono)

    def get_parametros_relleno(self):
        info_mat_relleno = self.perfil.calcular_material_relleno(self.D_f - self.H_z)
        return {"tipo_mat": info_mat_relleno["tipo_mat"], "φ": info_mat_relleno["φ"], "c_u": info_mat_relleno["c_u"], "γ": info_mat_relleno["γ"]}
    parametros_relleno = property(get_parametros_relleno)

    ######################################################################
    # Utilitarios
    ######################################################################

    def validar_atributos(self):
        #   - Obligatoriedad
        #   - Tipos y dominios
        #   - Restricciones en el perfil 
        
        perfil, D_c, D_p, h_c, h_con, θ_c, campana, n, D  = self.get_atributos("perfil", "D_c", "D_p", "h_c", "h_con", "θ_c", "campana", "n", "D")
        
        #D_c debe ser mayor o igual a D_p
        if D_c < D_p:
            raise ValueError (f'El diametro de la campana {D_c} m, es menor que el diametro de la pilote {D_p} m')

        profundidad_roca = perfil.calcular_profundidad_hasta_roca()
        
        if profundidad_roca is not None and D > profundidad_roca:
            raise ValueError ('Pilote en roca')

        # Parametros de entrada de campana deben ser mayores que 0 si campana == True y 0 si campana ==False
        if campana ==False and (h_c or h_con or θ_c ):
            raise ValueError (f'Hay valor de h_c: {h_c} o h_con: {h_con} o  θ_c: {θ_c} y campana es {campana} ')
        elif campana == True and (h_c is None or h_con is None or θ_c is None):
            raise ValueError (f'El valor de h_c: {h_c} o h_con: {h_con} o  θ_c: {θ_c} es None  campana es {campana} ')
        elif campana == True and (h_c <= 0 or h_con <= 0 or θ_c <= 0):
            raise ValueError (f'El valor de h_c: {h_c} o h_con: {h_con} o  θ_c: {θ_c} es menor o igual que 0 y  campana es {campana} ')
        
        
        if not (n == 4 or n==5 or n == 8 or n == 9):
            raise ValueError (f'El número de pilotes es diferente de 4 ,5, 8 o 9 :  {n}')

        if perfil.prof_lic_inicial is not None:
            if D > perfil.prof_lic_inicial and D < perfil.prof_lic_final:
                raise ValueError(f"Punta de pilotes en zona de licuación. D: {D}, prof_lic_inicial: {perfil.prof_lic_inicial}, prof_lic_final: {perfil.prof_lic_final}")

    def get_atributos(self, *nombres: str) -> Tuple:
        """Retorna los atributos solicitados como una tupla"""

        #return (self.__dict__[nombre] for nombre in nombres)
        return (getattr(self, nombre) for nombre in nombres)
    
    def volumen_pilote(self, D_p, D_c) -> float:
        """
        Calcula el volumen de un pilote

        Returns:
            float -- Volumen de un pilote [m³]
        """
        h_c, h_con, H = self.get_atributos("h_c", "h_con", "H")

        V_p = H * π * D_p**2 / 4 

        if D_p != D_c:
            # h_con = (D_c - D_p) / 2 / tan_g(θ_c)              # Altura de la sección cónica
            
            V1 = h_con * π / 3 *((D_p / 2)**2 + (D_c / 2)**2 + D_p / 2 * D_c / 2) # Volumen de la sección cónica completa
            V2 = π / 4 * D_c ** 2 * (h_c - h_con)             # Volumen de la sección cilíndrica despues del cono hasta la punta
            V3 = π / 4 * D_p ** 2 * h_c                       # Volumen de la sección cilíndrica sin campana en la longtud h_c
            V_p += V1 + V2 - V3
            
        return V_p 
    
    def peso_pilote(self, D_p, D_c) -> float: # TODO función de uso privado, se debe corregir a _
        """
        Calcula el peso de la pilote

        Returns:
            float -- Peso de la pilote [kN]
        """
        γ_c,  = self.get_atributos("γ_c")

        return self.volumen_pilote(D_p, D_c) * γ_c

    def volumen_dado(self) -> float:
        """"Inclue volumen del pedestal"""
        B, C, TP, θ, H_z  = self.get_atributos("B","C", "TP", "θ", "H_z")

        return (B**2 * H_z +  TP**2 * C / cos_g(θ))

    def peso_dado(self) -> float:
        """"Inclue peso del pedestal"""

        γ_c, = self.get_atributos("γ_c")

        return self.volumen_dado() * γ_c 

    def volumen_cimentacion(self) -> float:
        """
        Calcula el volumen de cimentación total
        """
        D_c, D_p, n  = self.get_atributos("D_c", "D_p", "n")
        volumen_dado = self.volumen_dado()
    
        volumen_pilote = self.volumen_pilote(D_p, D_c)
        volumen_cimentacion = volumen_dado + volumen_pilote * n

        return volumen_cimentacion

    def peso_cimentacion(self) -> float:

        γ_c, = self.get_atributos("γ_c")

        return self.volumen_cimentacion() * γ_c

    def volumen_relleno(self) -> float:
        """
        Calcula el volumen del relleno.

        Returns:
            float -- Volumen del relleno [m³]
        """

        B, D_f, H_z, TP, θ  = self.get_atributos("B", "D_f", "H_z", "TP", "θ")

        return B **2 * (D_f - H_z) - TP**2 * (D_f - H_z) / cos_g(θ)

    def peso_relleno(self) -> float:
        """
        Calcula el peso del relleno.

        Returns:
            float -- Peso del relleno [kN]
        """
        γ_r,  = self.get_atributos("γ_r")

        return self.volumen_relleno() * γ_r

    def _calcular_excentricidad_por_caso(self, F_x, F_y, F_z) -> float:
        """ 
        Calcula la excentricidad debido a carga lateral 
        para un caso de carga
        """
        
        H_z, C, θ = self.get_atributos("H_z", "C", "θ")

        M_L = F_x * (C + H_z)

        M_T = F_y * (C + H_z)

        M_V = F_z * tan_g(θ) * (C + H_z)

        M_neto = math.sqrt((M_L - M_V)**2 + (M_T - M_V)**2)

        #F_RL:  Fuerza resultante por cargas laterales [kN]
        F_RL = math.sqrt(F_x**2 + F_y**2)

        return M_neto / F_RL

    def calcular_excetricidad(self, cargas) -> float:
        """ 
        Calcula la excentricidad debido a carga lateral
        teniendo en cuenta los casos de carga compresion, tension, longitudinal maxima, transversal maxima
        """

        F_xc, F_yc, F_zc = cargas['F_xc'], cargas['F_yc'], cargas['F_zc']
        F_xt, F_yt, F_zt = cargas['F_xt'], cargas['F_yt'], cargas['F_zt']
        F_xl, F_yl, F_zl = cargas['F_xl'], cargas['F_yl'], cargas['F_zl']
        F_xtr, F_ytr, F_ztr = cargas['F_xtr'], cargas['F_ytr'], cargas['F_ztr']

        e_compresion = self._calcular_excentricidad_por_caso(F_xc, F_yc, F_zc) 
        e_tension = self._calcular_excentricidad_por_caso(F_xt, F_yt, F_zt)
        e_longitudinal = self._calcular_excentricidad_por_caso(F_xl, F_yl, F_zl)
        e_transversal = self._calcular_excentricidad_por_caso(F_xtr, F_ytr, F_ztr)

        e = max(e_compresion, e_tension, e_longitudinal, e_transversal)

        # retornar 0

        return e

    def calcular_φ(self, prof_ini, prof_fin) -> float:
        """calcula φ teniendo en cuenta las tangentes de φ y devuelve
            el promedio menos una desviación estandar        
        """

        perfil, = self.get_atributos("perfil")
        
        d = 0.0 
        lista_tanφ = []
        lista_h = []
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
                    lista_h.append(dH)
                elif d >= prof_fin:
                    break
            d += estrato.H_0

        if len(lista_tanφ) == 0:
            raise ValueError('En el segmento no se encuentran estratos granulares')

        tan_φ_prom, tan_φ_stdev = self.weighted_avg_and_std(lista_tanφ, lista_h)
        tan_φ = tan_φ_prom - tan_φ_stdev
                
        if tan_φ > 1:
            raise ValueError(f'El valor de tan_φ promedio {tan_φ} es mayor que 1 ') 

        φ = math.degrees(math.atan(tan_φ))

        return φ 

    def calcular_c_u(self, prof_ini, prof_fin) -> float:
        """calcula c_u  y devuelve
            el promedio menos una desviación estandar        
        """

        perfil, = self.get_atributos("perfil")
        
        d = 0.0 
        lista_c_u = []
        lista_h = []
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
                    lista_h.append(dH)
                elif d >= prof_fin:
                    break
            d += estrato.H_0

        if len(lista_c_u) == 0:
            raise ValueError('En el segmento no se encuentran estratos cohesivos')
        
        c_u_prom, c_u_stdev = self.weighted_avg_and_std(lista_c_u, lista_h)        
        c_u = c_u_prom - c_u_stdev

        return c_u

    def weighted_avg_and_std(self, values, weights):
        """
        Return the weighted average and standard deviation.

        values, weights -- Numpy ndarrays with the same shape.
        """
        average = np.average(values, weights=weights)
        # Fast and numerically precise:
        variance = np.average((values-average)**2, weights=weights)
        return (float(average), float(math.sqrt(variance)))        
    
    def calcular_longitud_transicion_granular(self, P) -> float: 
        """
        Calcula la longitud de transicion para el caso granular
        Arguments:
            D_p {float} -- Diametro del fuste 
        """            
        D_p, D, H, perfil, e = self.get_atributos("D_p", "D", "H", "perfil", "e")

        # # e: Excentricidad por carga horizontal [m]
        # e = self.calcular_excetricidad(cargas)
        
        #φ : Angulo de fricción del suelo [°]
        φ = self.calcular_φ(D - H, D)  

        #γ : Peso unitario del suelo [kN/m³]
        γ = perfil.calcular_promedio(D - H, D, 'γ_se')

        #k_p : coeficiente de presion pasiva [adim]
        k_p = tan_g(45 + φ / 2)**2

        #a, b, c: Parametros de la ecuacion cuadratica para resolver Longitud de transicion
        a = γ * D_p * k_p
        b = 2 * P
        c = 2 * P * e

        #L_t_g : Longitud de transicion [m]
        raices = np.roots([a, 0, -b, -c])
        raices_positivas = np.where(raices > 0, raices, 0)
        L_t_g = max([float(raiz) for raiz in raices_positivas])

        return L_t_g

    def interpolar_ku(self, φ) -> float:
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

    def interpolar_m(self, φ) -> float:
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

    def interpolar_N_q(self, φ) -> float:
        """
        Interpola la curva lineal a trozos de m(φ) segun la metodología de Das(2001)
        """
        hincado, = self.get_atributos("hincado")

        φs = [20, 25, 28, 30, 32, 34, 36, 38, 40, 42, 45]
        nqs = [4, 5, 8, 12, 17, 22, 30, 40, 60, 80, 115]

        if hincado:
            nqs = [8, 12, 20, 25, 35, 45, 60, 80, 120, 160, 230]

        if φ < φs[0] or φ > φs[-1]:
            raise ValueError("Valor φ fuera de rango [20 - 45]: " + str(φ))

        i1 = [i for i in range(len(φs)) if φs[i] <= φ ][-1] 
        i2 = [i for i in range(len(φs)) if φs[i] >= φ ][0]

        if i1 == i2:
            return nqs[i1]
        else:
            return (nqs[i2] - nqs[i1]) / (φs[i2] - φs[i1]) * (φ - φs[i1])   + nqs[i1]

    def interpolar_B_c(self, relacion_H_D) -> float:
        """
        Interpola la curva lineal a trozos de Bc segun la metodología de Das(2001) pag 708 para tension de suelo cohesivo, se usa la de preexcavados
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

    def set_perfil(self, perfil: Perfil):
        self.perfil = perfil
        info_mat_relleno = self.perfil.calcular_material_relleno(self.D - self.H)
        self.tipo_mat_r, self.φ_r, self.c_u_r, self.γ_r  = (info_mat_relleno["tipo_mat"], info_mat_relleno["φ"], info_mat_relleno["c_u"], info_mat_relleno["γ"])

    ######################################################################
    # Cálculos capacidad portante 
    ######################################################################
    
    def calculo_capacidad_portante_pilote(self) -> Tuple[float, float, float, Memoria, Memoria]:

        D_p, D_c  = self.get_atributos("D_p", "D_c")

        return self._calculo_capacidad_portante_pilote(D_p, D_c)

    def _calculo_capacidad_portante_pilote(self, D_p, D_c) -> Tuple[float, float, float, Memoria, Memoria]:
        """
        Calcula la capacidad portante para un pilote
        
        Arguments:
        D_c {float} -- Diametro de campana o pilote
            

        Returns:
            Tuple[float, float,float, Memoria, Memoria] -- (q_ult: Capacidad portante ultima [kN],
                                                            q_p: Capacidad portante por punta [kN]
                                                            q_s: Capacidad portante por fuste [kN]
                                                            memoria_p: memoria punta
                                                            memoria_s :memoria fuste)

        """

        D, perfil  = self.get_atributos("D", "perfil")

        # φ_D: Ángulo de fricción para calcular el límite inferior del suelo relevante [°]
        φ_D = perfil.estrato_en(D).φ_s

        # B_lim: límite inferior del suelo relevante [m]
        B_lim = D_c * tan_g(45 + φ_D / 2)

        # Porcentajes de tipos de material de suelo entre D y D + B_lim
        porcentajes = perfil.calcular_porcentaje_tipo_mat(D, D + B_lim)

        # Se prefiere la formulación de suelos cohesivos si ellos constituyen el 30% o más
        if porcentajes["c"] >= 30.0:
            q_p, memoria_p = self.calculo_de_capacidad_portante_punta_cohesivo(D_c)
            q_s, memoria_s = self.calculo_de_capacidad_portante_fuste(D_p)
            q_ult = q_p + q_s - self.peso_pilote(D_p, D_c)
            return (q_ult, q_p, q_s, memoria_p, memoria_s)
        else:
            q_p, memoria_p = self.calculo_de_capacidad_portante_punta_granular(D_c)
            q_s, memoria_s = self.calculo_de_capacidad_portante_fuste(D_p)
            q_ult = q_p + q_s -self.peso_pilote(D_p, D_c)
            return (q_ult, q_p, q_s, memoria_p, memoria_s)
    
    def calculo_de_capacidad_portante_punta_granular(self, D_c) -> Tuple[float, Memoria]:
        
        """Calcula la capacidad portante por punta 
            para suelo granular

            Returns:
            Tuple[float, Memoria] -- Q_p Capacidad portante por punta [kN], memoria
        """

        D, perfil  = self.get_atributos("D", "perfil")
        
        # φ_D: Ángulo de fricción para calcular el límite inferior del suelo relevante [°]
        φ_D = perfil.estrato_en(D).φ_s

        # B_lim: límite inferior del suelo relevante [m]
        B_lim = D_c * tan_g(45 + φ_D / 2)
        
        # φ: Ángulo de fricción del suelo relevante [°]
        φ = perfil.calcular_promedio(D, D + B_lim, "φ_s", tipo_mat="g")
        
        # N_q: Factor de capacidad portante debido a la sobrecarga. [-]
        N_q_as = self.interpolar_N_q(φ)  # es diferente al de zapatas 
        
        # q: Esfuerzo de sobrecarga efectivo a la profundidad de cimentación [kN/m²]
        q = perfil.calcular_q(D)

        # A_p: Área del pilote en la punta [m²]
        A_p = π / 4 * D_c ** 2

        #Q_p: Capacidad portante en la punta [kN]
        Q_p = q * N_q_as * A_p
        
        #memoria
        memoria = {"D_c":D_c , "q":q, "N_q_as" :N_q_as,  "A_p":A_p}

        return (Q_p, memoria)
    
    def calculo_de_capacidad_portante_punta_cohesivo(self, D_c) -> Tuple[float, Memoria]:
        
        """Calcula la capacidad portante por punta 

            para suelo cohesivo
        """
        
        D,  perfil  = self.get_atributos("D","perfil")

        # φ_D: Ángulo de fricción para calcular el límite inferior del suelo relevante [°]
        φ_D = perfil.estrato_en(D).φ_s

        # B_lim: límite inferior del suelo relevante [m]
        B_lim = D_c * tan_g(45 + φ_D / 2)

        # A_p: Área del pilote en la punta [m²]
        A_p = π / 4 * D_c ** 2
    
        # c_u: Resistencia no drenada [kN/m²]  se le resta una desviacion estandar
        # c_u = perfil.calcular_promedio(D, D + B_lim, "c_u")
        c_u = self.calcular_c_u(D, D + B_lim)
        
        Q_p = 9 * c_u  * A_p
        
        memoria = {"D_c":D_c, "A_p":A_p, "c_u":c_u}

        return (Q_p, memoria)
    
    def calculo_de_capacidad_portante_fuste(self, D_p) -> Tuple[float, Memoria]: 
        
        """Calcula la capacidad portante por fuste"""
        
        D, H, h_c, perfil, hincado, campana  = self.get_atributos("D", "H", "h_c", "perfil", "hincado", "campana")

        # Capacidad portante en el fuste [kN]
        iteraciones = []
        d = 0.0  # prof. ini de capa actual
        prof_ini = D - H 

        K_s = 0.5 

        if hincado:
            K_s = 1.5

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
                    #K = 1 - sin_g(estrato.φ_s)
                    A_s = π * D_p * Δ_z
                    Q_s += K_s * q * A_s * tan_g(δ)
                    
                    iteraciones.append({"d":d, "Δ_z":Δ_z, "z":z, "q":q, "φ_s":φ_s, "K_s":K_s, "A_s":A_s, "Q_s":Q_s})

                elif estrato.tipo_mat == "c":
                    c_u = estrato.c_u
                    α = min(1 , 0.21 + 0.26 * 100 / c_u)
                    if hincado:
                        α = min(1, -0.314 * math.log(c_u)+ 2.022)
                    A_s = π * D_p * Δ_z
                    Q_s += α * c_u * A_s

                    iteraciones.append({"d":d, "Δ_z":Δ_z, "z":z, "c_u":c_u, "α":α, "A_s":A_s, "Q_s":Q_s})
                
                else:
                    raise ValueError(f"Cálculo de capacidad del fuste en roca. profundidad = {d}")

            d += estrato.H_0

        #memoria
        memoria = {"iteraciones": iteraciones}

        return (Q_s , memoria)
    
    def calculo_de_capacidad_portante(self) -> Tuple[float, Memoria]: 
        
        """Calcula la capacidad portante del grupo"""

        D_c, D_p, S_p, D, n, H, perfil, hincado, x, x_c  = self.get_atributos("D_c", "D_p", "S_p", "D", "n", "H", "perfil", "hincado", "x", "x_c")

        # Porcentajes de tipos de material de suelo entre H - D y D 8 la longitud del pilote)
        porcentajes = perfil.calcular_porcentaje_tipo_mat(D - H, D)

        # β: Ángulo de relación D_c/S_p [°]
        β =  math.degrees(math.atan2(D_c, S_p)) 

        #m: numero de pilotes por lado [-]
        m = self.N_pL

        #n numero de pilotes en la otra dimension del dado[-]
        n1 = m

        # Factor de correccion por grupo
        E = 1 - β / 90 * ((m * (n1 - 1) + (m - 1) * n1) / m / n1)

        if hincado:
            # Se prefiere la formulación de suelos cohesivos si ellos constituyen el 30% o más
            if porcentajes["c"] < 30.0:
                E = 1
        
            #Q_cu_grupo: Capacidad portante del grupo [kN]
            q_ult ,_, _, _, _ = self._calculo_capacidad_portante_pilote(D_p, D_c)
            Q_cu_grupo = E * q_ult

        else:
            #Q_cu_grupo: Capacidad portante del grupo [kN]
            q_ult, _, _, _, _ = self._calculo_capacidad_portante_pilote(D_p, D_c)
            Q_cu_grupo = n * q_ult


        #Capacidad portante pilote equivalente 
        
        Q_equiv, _ , _ , _, _ = self._calculo_capacidad_portante_pilote(x, x_c)
        
        memoria = {"E":E, "β":β, "m":m, "n":n, "Q_equiv":Q_equiv}

        return Q_cu_grupo, memoria 

    ######################################################################
    # Cálculos arrancamiento
    ######################################################################

    def calculo_tension_pilote(self) -> Tuple[float, Memoria]:

        D_p, D_c  = self.get_atributos("D_p", "D_c")

        return self._calculo_tension_pilote(D_p, D_c)

    def _calculo_tension_pilote(self, D_p, D_c) -> Tuple[float, Memoria]:
        """
        Calcula las capacidad a la tensión de un pilote
        
        Arguments:
            

        Returns:
            Tuple[float, Memoria] -- (T_Fv: Capacidad a la tensión última [kN], memoria)

        """
        
        D, perfil = self.get_atributos("D", "perfil")

        # Porcentajes de tipos de material de suelo entre 0 y D
        porcentajes = perfil.calcular_porcentaje_tipo_mat(0, D)
        
        if porcentajes["c"] >= 30.0:
            T_tp, T_tp_s,  memoria_tp = self.calculo_tension_tronco_piramidal_cohesivo(D_p, D_c)
        else:
            T_tp, T_tp_s, memoria_tp = self.calculo_tension_tronco_piramidal_granular(D_p, D_c)
        
        T_fv, T_fv_s, memoria_fv = self.calculo_tension_falla_vertical(D_p, D_c)
        
        if T_fv < T_tp:
            return (T_fv, T_fv_s, memoria_fv)
        else:
            return (T_tp, T_tp_s, memoria_tp)
    
    def calculo_tension_falla_vertical(self, D_p, D_c) -> Tuple[float, Memoria]:
        
        """Calcula resistencia al arrancamiento de un pilote

        Arguments:
        D_c {float} -- Diametro de campana
        D_p {floar} -- Diametro de fuste  

        mediante el método de falla vertical
        """

        campana, H, D, D_f, perfil = self.get_atributos("campana", "H", "D", "D_f", "perfil")
        
        if campana:
            
            c_u = perfil.calcular_promedio(D_f, D, "c_u")
            
            T_su_1 = π / 4 * (D_c**2 - D_p**2) * 9 * c_u 

            T_su_2 =  π * (D_c + D_p) / 2 * c_u * H  

            if T_su_1 < T_su_2:
                T_tu = T_su_1 + self.peso_pilote(D_p, D_c)
                memoria_s = {"D_c":D_c, "D_p":D_p, "c_u":c_u }
                return (T_tu,  T_su_1, memoria_s)

            else:
                T_tu = T_su_2 + self.peso_pilote(D_p, D_c)
                memoria_s = {"D_c":D_c, "D_p":D_p, "c_u":c_u, "H":H}
                return (T_tu,  T_su_2, memoria_s)

        else:

            T_su, memoria_s = self.calculo_de_capacidad_portante_fuste_tension(D_p)
            T_tu = T_su + self.peso_pilote(D_p, D_c)
            return (T_tu, T_su, memoria_s)  
    
    def calculo_de_capacidad_portante_fuste_tension(self, D_p) -> Tuple[float, Memoria]: 
        
        """
        Calcula la capacidad portante por fuste

        Arguments:
        D_p {float} -- Diametro de fuste
        """
        
        D, H, h_c, perfil, campana, hincado  = self.get_atributos("D", "H", "h_c", "perfil","campana", "hincado")

        # Capacidad portante en el fuste [kN]
        iteraciones = []
        d = 0.0  # prof. ini de capa actual
        prof_ini = D - H

        K_s = 0.5 

        if hincado:
            K_s = 1.5

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
                    #K = 1 - sin_g(estrato.φ_s)
                    A_s = π * D_p * Δ_z
                    Q_s += (2 / 3) * K_s * q * A_s * tan_g(δ)  # esto cambia comparado con el otro del mismo nombre
                    
                    iteraciones.append({"d":d, "Δ_z":Δ_z, "z":z, "q":q, "φ_s":φ_s, "K_s":K_s, "A_s":A_s, "Q_s":Q_s})

                elif estrato.tipo_mat == "c":
                    c_u = estrato.c_u
                    α = min(1 , 0.21 + 0.26 * 100 / c_u) # revisar aquíno hay opción de hincado 
                    A_s = π * D_p * Δ_z
                    Q_s += α * c_u * A_s

                    iteraciones.append({"d":d, "Δ_z":Δ_z, "z":z, "c_u":c_u, "α":α, "A_s":A_s, "Q_s":Q_s})
                
                else:
                    raise ValueError(f"Cálculo de capacidad del fuste en roca. profundidad = {d}")

            d += estrato.H_0

        #memoria
        memoria = {"iteraciones": iteraciones}

        return (Q_s , memoria)
    
    def calculo_tension_tronco_piramidal_granular(self, D_p, D_c) -> Tuple[float, Memoria]:

        """Calcula resistencia al arrancamiento de un pilote
            mediante el método de tronco piramidal para suelo cohesivo

            Arguments:
            D_c {float} -- Diametro de campana o pilote
        """

        D, H, perfil = self.get_atributos("D","H", "perfil")

        # A_p: Área del pilote en la punta [m²]
        A_p = π / 4 * D_c**2
        
        # φ: Ángulo de fricción del suelo relevante [°]
        φ = perfil.calcular_promedio(0, D, "φ_s", tipo_mat="g")
        
        #K_u: coeficiente nominal de levantamiento [adimensional]
        k_u = self.interpolar_ku(φ)

        #m : Coeficiente de factor de forma [adimensional]
        m = self.interpolar_m(φ)
        
        #B_q: Factor de arrancamiento
        B_q = 2 * H * k_u * tan_g(φ) / D_c * (m * H / D_c + 1) + 1

        # γ_s:  Peso unitario promedio del suelo hasta la profundidad D [kN/m³]
        γ_s = perfil.calcular_promedio_γ(D)

        # T_ug : Carga a tensión
        T_su = B_q * A_p * γ_s * H 
        
        #T_un: Carga última a tensión 
        T_tu = T_su + self.peso_pilote(D_p, D_c)

        memoria = {"A_p":A_p, "γ_s":γ_s, "φ":φ, "k_u":k_u, "m":m, "B_q":B_q, "T_su":T_su, "D_c":D_c}

        return (T_tu, T_su, memoria)
    
    def calculo_tension_tronco_piramidal_cohesivo(self, D_p, D_c) -> Tuple[float, Memoria]:

        """
        Calcula resistencia a la tensión mediante el método de tronco piramidal
        para suelo cohesivo

        Arguments:
            D_c {float} -- Diametro de campana o pilote
        """
        D, H, perfil = self.get_atributos("D", "H", "perfil")
        
        # A_p: Área de la pilote en la punta [m²]
        A_p = π / 4 * D_c**2

        # c_u: Cohesión no drenada del suelo [kN/m²]
        c_u = c_u = perfil.calcular_promedio(0, D, "c_u") # promedio de c_u de los estratos cohesivos

        #H_D_critica : relación Longitud y diametro crítica según Das (2001) [adim]
        H_D_critica = min(7, 0.107 * c_u + 2.5)

        #relacion_H_D : relacion entre relacion H y D_c y relacion critica [adim]
        relacion_H_D = (H / D_c) / H_D_critica

        # β: Factor de desconexión 
        if relacion_H_D > 1:
            B_c = 9
        else:
            B_c = self.interpolar_B_c(relacion_H_D)

        # γ_s:  Peso unitario promedio del suelo hasta la profundidad D [kN/m³]
        γ_s = perfil.calcular_promedio_γ(D)

        #T_su: Carga última a tensión 
        T_su = (c_u * B_c + γ_s * H) * A_p

        #T_tu: Carga última a tensión 
        T_tu = T_su + self.peso_pilote(D_p, D_c)

        memoria = {"D_c":D_c, "c_u":c_u, "B_c":B_c, "A_p":A_p, "γ_s":γ_s, "H":H }

        return (T_tu, T_su, memoria)

    def calculo_de_tension(self) -> Tuple[float, Memoria]: 
        
        """Calcula la capacidad a tensión del grupo"""

        n, D_p, D_c, x, x_c = self.get_atributos("n", "D_p", "D_c", "x", "x_c")

        #Q_cu_grupo: Capacidad a tensión del grupo [kN]
        T, _ , _ = self._calculo_tension_pilote(D_p, D_c)

        Q_cu_grupo = n * T + self.peso_dado()

        #Capacidad a tensión pilote equivalente con el area del grupo
                
        _, T_e ,  _ = self._calculo_tension_pilote(x, x_c)
        
        Q_cu_grupo_e = T_e + self.peso_dado()
        
        memoria = {"n":n, "T":T, "T_e":T_e, "Q_cu_grupo_e":Q_cu_grupo_e}

        return Q_cu_grupo, memoria

    ######################################################################
    # Cálculos carga lateral
    ######################################################################

    def calculo_carga_lateral_pilote(self) -> Tuple[float, bool, Memoria]:
        """Calcula Carga lateral 

        Arguments:
            e: Excentricidad por carga horizontal [m]
        
        Returns:
            Tuple[float, bool, Memoria] -- (P: resistencia lateral [m], condición de pilote corto , memoria)

        """

        H, D, perfil = self.get_atributos("H", "D", "perfil")
        
        # Porcentajes de tipos de material de suelo entre D - H y D
        porcentajes = perfil.calcular_porcentaje_tipo_mat(D - H, D)

        # Se prefiere la formulación de suelos cohesivos si ellos constituyen el 30% o más
        if porcentajes["c"] >= 30.0:
            P, p_corta, memoria_p = self.calculo_carga_lateral_pilote_cohesivo()
            return P, p_corta, memoria_p
        else:
            P, p_corta, memoria_p = self.calculo_carga_lateral_pilote_granular()
            return P, p_corta, memoria_p

    #Este método requiere la excentricidad
    def calculo_carga_lateral_pilote_granular(self) -> Tuple[float, bool, Memoria]:
        """Calcula carga lateral para pilote suelo granular
            e: Excentricidad por carga horizontal [m]
        """
        D_p, D, H, perfil, r, e = self.get_atributos("D_p", "D", "H", "perfil", "r", "e")
        
        # # e: Excentricidad por carga horizontal [m]
        # e = self.calcular_excetricidad(cargas)

        # φ : Angulo de friccion interno del suelo[°]
        φ = self.calcular_φ(D - H, D)

        #γ: Peso unitario del suelo[kN/m³]
        γ = perfil.calcular_promedio(D - H, D, 'γ_se')

        #k_p: coeficiente de presion pasiva del suelo[-]
        k_p = tan_g(45 + φ / 2)**2

        # A_p: Área del pilote en la punta [m²]
        A_p = math.pi / 4 * D_p**2

        #B_equiv: Lado equivalente de un pilote cuadrado [m]
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

        # L_t: Longitud transicion , si H < Le la pilote es corto
        L_t = self.calcular_longitud_transicion_granular(P)

        if H < L_t:
            p_corta = True
            P = 0.5 * γ * D_p * H**3 * k_p / (e + H)
            
        else:
            p_corta = False

        P  = P * r

        memoria = {"e":e , "φ":φ, "γ":γ, "k_p":k_p, "A_p":A_p, "B_equiv":B_equiv, "M_y":M_y, "L_t":L_t}

        return P, p_corta, memoria

    #Este método requiere la excentricidad
    def calculo_carga_lateral_pilote_cohesivo(self) -> Tuple[float, bool, Memoria]:
        """Calcula carga lateral para pilote suele cohesivo
            e: Excentricidad por carga horizontal [m]

        """
        D_p, D, H, r, e = self.get_atributos("D_p", "D", "H", "r", "e")

        # # e: Excentricidad por carga horizontal [m]
        # e = self.calcular_excetricidad(cargas)
        
        # c_u: Cohesión no drenada del suelo [kN/m²]
        c_u = self.calcular_c_u(D - H, D)

        # A_p: Área del pilote en la punta [m²]
        A_p = π / 4 * D_p**2

        # B_equiv : Lado equivalente de un pilote cuadrado [m]
        B_equiv = math.sqrt(A_p)

        # M_y: Momento de fluencia[kN m]    #TODO  0.033 = 0.65 * 0.5% * fy; fy: Esfuerzo de fluencia del acero ? 
        M_y = 3234.21 * B_equiv * (B_equiv - 0.06)**2

        #a, b ,c : parametros de la ecuación cuadrática
        a = 1 / (18 * c_u * D_p)
        b = e + 1.5 * D_p
        c = - M_y

        if (b**2 - 4 * a * c < 0):
            print(b**2 - 4 * a * c)

        #P: carga para pilote largo 
        P = (-b + math.sqrt(b**2 - 4 * a * c)) / (2 * a)

        #f: Longitud hasta zona de momento maximo [m]
        f = P / 9 / c_u / D_p

        # g: longitud desde zona de momento maximo hasta final del pilote[m]
        g = math.sqrt(M_y / (2.25 * c_u * D_p))

        #L_t: Longitud de transicion [m]
        L_t = 1.5 * D_p + f + g

        if H < L_t:
            
            p_corta = True
            #a1, b1, c1 : parametros de la ecuación cuadrática
            a1 = 1
            b1 = 36 * c_u * D_p * e + 27 * c_u * D_p**2 + 18 * c_u * D_p * H
            c1 = -81 * c_u**2 * D_p**2 * (H - 1.5 * D_p)**2

            #P: carga ultima pilote corto
            P = (-b1 + math.sqrt( b1 **2 - 4* a1 *c1)) / (2 * a1)
        else:
            p_corta = False

        P  = P * r

        memoria = {"e":e , "c_u":c_u, "A_p":A_p, "B_equiv":B_equiv, "M_y":M_y, "P":P, "f":f, "g":g, "L_t":L_t,} 

        return P, p_corta, memoria

    def calculo_modulos_de_reaccion_horizontal(self):
        
        # tabla con datos de una a otra profncidad tal k / Resuelto
        #I_p : Momento de inercia de la sección [m⁴]
        #E_s : Módulo de elasticidad del suelo [kN/m²]
        #ν : Relación de poisson [-]
        #k: Módulo de reacción horizontal [kN/m³]

        perfil, D_p, D_f, H, E_p = self.get_atributos("perfil", "D_p", "D_f", "H", "E_p")

        prof_ini = D_f
        prof_fin = D_f + H
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

    def calculo_carga_lateral(self):

        """Calcula resistencia a la carga lateral del grupo de pilotes 
            según código colombiano de puentes numeral 10.7.2.4-1
        """
        
        S_p, D_p, n = self.get_atributos("S_p", "D_p", "n") 

        P, p_corta, memoria = self.calculo_carga_lateral_pilote()
            
        # Distribución de pilotes a lo largo de las filas de la configuración
        # espacial para cada número de pilotes total
        configuraciones = {
            '4' : {'fila1':2, 'fila2':2, 'fila3': 0, 'fila4':0, 'fila5':0},
            '5' : {'fila1':2, 'fila2':1, 'fila3': 2, 'fila4':0, 'fila5':0},
            '8' : {'fila1':3, 'fila2':2, 'fila3': 3, 'fila4':0, 'fila5':0},
            '9' : {'fila1':3, 'fila2':3 ,'fila3': 3, 'fila4':0, 'fila5':0},
            '12': {'fila1':5, 'fila2':2, 'fila3': 2, 'fila4':2, 'fila5':5},
            '16': {'fila1':5, 'fila2':2, 'fila3': 2, 'fila4':2, 'fila5':5},
            }

        for numero_pilotes in configuraciones.keys():
            if numero_pilotes == str(n):
                conf = configuraciones[numero_pilotes]
                break

        if len(conf) == 0:
            raise ValueError(f'Valor de n: {n} no corresponde a los casos para carga lateral')

        #S_p es separacion no hacia el pilote del centro sino hacia pilotes exteriores
        if S_p > 5 * D_p:
            P_grupo = P * (1 * conf['fila1'] + 0.85 * conf['fila2'] + 0.7 * conf['fila3'] + 0.7 * conf['fila4'] + 0.7 * conf['fila5'])
        else:
            P_grupo = P * (0.8 * conf['fila1'] + 0.4 * conf['fila2'] + 0.3 * conf['fila3'] + 0.3 * conf['fila4'] + 0.3 * conf['fila5'])

        memoria = {"P":P}

        return P_grupo, p_corta, memoria

    ######################################################################
    # Cálculos asentamiento
    ######################################################################
        
    def calculo_asentamiento(self, k:int, F_zc:float, F_zc_eds:float, t:float) -> Tuple[float, float, Memoria, Memoria]:
        """Calcula asentamiento elastico y por consolidación
        """

        x, D_f, H_z, H, perfil, f_carga_p = self.get_atributos("x", "D_f", "H_z", "H", "perfil", "f_carga_p")

        # W_c: Peso de la cimentación [kN]
        W_c = self.peso_dado()

        # W_r: Peso deL relleno [kN]
        info_relleno = perfil.calcular_material_relleno(D_f - H_z)
        W_r = self.volumen_relleno() * info_relleno["γ"]

        # q_0: Magnitud de la presión transmitida al suelo de fundación [kN/m²]
        q_0 = (F_zc * f_carga_p + W_c + W_r) / x**2
        
        
        q_0_eds = (F_zc_eds* f_carga_p + W_c + W_r) / x**2

        #
        estrato = perfil.estrato_en(D_f + 0.01)
        if estrato.tipo_mat == "r":
            S_e, memoria_e = self.calculo_asentamiento_roca(D_f, F_zc)
            return (S_e, 0, memoria_e, None)
        else:
            #D: Profundidad de la zapata equivalente [m]
            D = D_f + 2 / 3 * H

            # Ajuste del perfil, para que el estrato más profundo cubra la profundidad requerida
            prof_requerida = D + 2 * x
            delta_ultimo_estrato = prof_requerida - perfil.calcular_profundidad_total()
            if delta_ultimo_estrato > 0:
                perfil_asentamiento = copy.copy(perfil)
                perfil_asentamiento[-1].H_0 += delta_ultimo_estrato
            else:
                perfil_asentamiento = perfil

            # tipo de material
            tipos = perfil.calcular_tipo_mat_distintos(D, D + 2 * x)
            tipos = [t for t in tipos if t != "r"]

            # Capacidad
            if len(tipos) == 1:
                if tipos[0] == "c":
                    S_e, memoria_e = self.calculo_asentamiento_elastico_suelos_cohesivos(D, x, q_0, perfil_asentamiento)
                    S_c, memoria_c = self.calculo_asentamiento_por_consolidacion(D, x, q_0_eds, perfil_asentamiento)
                    return (S_e, S_c, memoria_e, memoria_c)
                elif tipos[0] == "g":
                    S_e, memoria_e = self.calculo_asentamiento_elastico_suelos_granulares(k, t, D, x, q_0, perfil_asentamiento)
                    return (S_e, 0, memoria_e, None)
            elif len(tipos) == 2:
                S_e, memoria_e = self.calculo_asentamiento_elastico_suelos_mixtos(k, t, D, x, q_0, perfil_asentamiento)
                S_c, memoria_c = self.calculo_asentamiento_por_consolidacion(D, x, q_0_eds, perfil_asentamiento)
                return (S_e, S_c, memoria_e, memoria_c)
            else: # solo roca
                S_e, memoria_e = self.calculo_asentamiento_roca(D, F_zc * f_carga_p)
                return (S_e, 0, memoria_e, None)

    def calculo_asentamiento_elastico_suelos_granulares(self, k:float, t:float, D: float, x: float, q_0: float, perfil: Perfil) -> Tuple[float, Memoria]:
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

        # σ_0f: Esfuerzo vertical efectivo inicial al nivel de fundación [kN/m²]
        σ_0f = perfil.calcular_q(D)

        # C_1: Factor de corrección por profundidad de la fundación [-]
        C_1 = max(0, 1 - 0.5 * σ_0f / q_0)

        # C_2: Factor de corrección por “Creep” [-]
        C_2 = 1 + 0.20 * math.log10(t / 0.10)

        # Z: Lista con las profundidades para el cálculo de I_z (a mitad del segmento) [m]
        Z = [D + 2 * x / k * i + x / k for i in range(k)]

        # dz: Espesor de la capa de análisis [m]
        dz =  2 * x / k

        # S: Asentamiento [m]
        S = C_1 * C_2 * q_0 * dz * sum([self.interpolar_Iz_elastico(z - D) / perfil.estrato_en(z).E_rs for z in Z])

        # memoria
        memoria = {"tipo_mat": "g", "σ_0f":σ_0f, "C_1":C_1, "C_2":C_2, "Z":Z, "dz":dz}

        return (S, memoria)

    def calculo_asentamiento_elastico_suelos_cohesivos(self, D: float, x: float, q_0: float, perfil: Perfil) -> Tuple[float, Memoria]:

        # S_ec : Asentamiento en elástico en suelo cohesivo [m]
        z = 0.0
        S_ec = 0.0
        Δz_acum = 0.0
        M = x / x
        α_cd = 4 # El incremento se hace para 4 zapatas de ancho B/2
        prof_ini = D
        prof_roca = perfil.calcular_profundidad_hasta_roca() 
        prof_fin = prof_roca if prof_roca else perfil.calcular_profundidad_total()
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
                    N = Δz_acum / x
                    I_1 = 1 / π * (M * math.log((1 + math.sqrt(M**2 + 1) * math.sqrt(M**2 + N**2))/ M / (1 + math.sqrt(M**2 + N**2 + 1))) + \
                                    math.log((M + math.sqrt(M**2 + 1) * math.sqrt(1 + N**2))/(M + math.sqrt(M**2 + N**2 + 1))))
                    I_2 = N / 2 / π * math.atan2(M, N * math.sqrt(M**2 + N**2 + 1))
                    I_p = I_1 + (1 - 2 * ν) / (1 - ν) * I_2
                    I_f = calcular_I_f(ν, Δz / x)
                    C_d = 1 / 2 * α_cd * I_p * I_f
                    S_ec += q_0 * x * C_d * (1 - ν**2) / E_s
                    iteraciones.append({"z":z, "Δz_acum":Δz_acum, "E_s":E_s, "ν":ν, "N":N, "I_1":I_1, "I_2":I_2, "I_p":I_p, "I_f":I_f, "C_d":C_d, "S_ec":S_ec})
            elif z >= prof_fin:
                break
            
            z += estrato.H_0

        # memoria
        memoria = {"tipo_mat": "c", "M":M, "α_cd":α_cd, "iteraciones": iteraciones}

        return (S_ec, memoria)

    def calculo_asentamiento_elastico_suelos_mixtos(self, k: int, t:float, D: float, x: float, q_0: float, perfil: Perfil) -> Tuple[float, Memoria]:

        # σ_0f: Esfuerzo vertical efectivo inicial al nivel de fundación [kN/m²]
        σ_0f = perfil.calcular_q(D)

        # C_1: Factor de corrección por profundidad de la fundación [-]
        C_1 = max(0, 1 - 0.5 * σ_0f / q_0)

        # C_2: Factor de corrección por “Creep” [-]
        C_2 = 1 + 0.20 * math.log10(t / 0.10)

        # S_e: Asentamiento [m]
        S_e = 0.0
        S_e_g = 0.0
        S_e_c = 0.0
        z = 0.0  # prof. ini de capa actual

        prof_ini = D
        prof_roca = perfil.calcular_profundidad_hasta_roca() 
        prof_fin = prof_roca if prof_roca else perfil.calcular_profundidad_total()
        Δz_acum_ant = 0.0
        Δz_acum = 0.0
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
                Δz_acum += Δz
                if estrato.tipo_mat == "g":                    
                    ΔS     = self.asentamiento_incremental_granular(Δz_acum, estrato, q_0, C_1, C_2, k)
                    ΔS_ant = self.asentamiento_incremental_granular(Δz_acum_ant, estrato, q_0, C_1, C_2, k)
                    S_e_g += ΔS - ΔS_ant
                elif estrato.tipo_mat == "c":
                    ΔS =     self.asentamiento_incremental_cohesivo(Δz_acum, estrato, q_0)
                    ΔS_ant = self.asentamiento_incremental_cohesivo(Δz_acum_ant, estrato, q_0)
                    S_e_c += ΔS - ΔS_ant
                S_e += ΔS - ΔS_ant
                iteraciones.append({"Δz_acum": Δz_acum, "Δz_acum_ant": Δz_acum_ant, "S_e": S_e, "ΔS": ΔS, "ΔS_ant": ΔS_ant, "estrato": estrato.__dict__})
            elif z > prof_fin:
                break
            Δz_acum_ant = Δz_acum
            z += estrato.H_0

        # memoria
        memoria = {"tipo_mat": "m", "σ_0f":σ_0f, "C_1":C_1, "C_2":C_2, "S_e_g": S_e_g, "S_e_c": S_e_c, "iteraciones": iteraciones}

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
        x, = self.get_atributos("x")
        C_d = calcular_C_d(H, x)
                
        return C_d * q_0 * x * (1 - estrato.ν**2) / estrato.E_s

    def calculo_asentamiento_por_consolidacion(self, D: float, x: float, q_0: float, perfil: Perfil) -> Tuple[float, Memoria]:
        """
        Calcula el asentamiento por consolidación

        Arguments:
            F_vc {float} -- Componente vertical de la carga a compresión [kN]
        
        Returns:
            Tuple[float, Memoria] -- (S: Asentamiento [m], memoria)
        """

        # d: Profundidad actual del loop de acumulación
        d = 0.0
        S_c = 0.0

        # memoria de cada iteracion
        iteraciones = []
        for estrato in perfil:
            if d + estrato.H_0 > D and d < D + 2 * x:
                if estrato.tipo_mat == "c" and estrato.saturado:
                    # H_c: Espesor de estrato compresible [m]
                    if d < D:
                        if d + estrato.H_0 > D + 2 * x:
                            H_c = 2 * x
                        else:
                            H_c = d + estrato.H_0 - D
                    elif d + estrato.H_0 > D + 2 * x:
                        H_c = D + 2 * x - d
                    else:
                        H_c = estrato.H_0
                    
                    # z: Profundidad desde D de evaluación de Iz para el estrato [m]
                    
                    if d < D:
                        z = H_c / 2
                    else:
                        z = d + H_c / 2 - D

                    # M, N, V, V_1: Factores para el cálculo de I_z (Newmark)
                    M = x / 2 / z
                    N = x / 2 / z
                    V = M**2 + N**2 + 1
                    V_1 = (M * N)**2

                    # I_z: Factor de influencia de la deformación unitaria
                    I_z = 1 / 4 / π *( 2 * M * N * math.sqrt(V) / (V + V_1) * (V + 1) / V  + math.atan2(2 * M * N * math.sqrt(V), V - V_1))

                    # Δσ_p: Incremento de esfuerzo vertical efectivo [kN/m²]
                    Δσ_p = 4 * q_0 * I_z

                    # σ_0p: Esfuerzo vertical efectivo inicial [kN/m²]
                    σ_0p = perfil.calcular_q(z + D)

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
                            print("Error***********", σ_0p, Δσ_p, q_0, I_z)
                        dS_c = C_s * H_c / (1 + e_0) * math.log10((σ_0p + Δσ_p) / σ_0p)
                    elif σ_0p < σ_pp and  σ_pp <= σ_0p + Δσ_p:
                        dS_c = C_s * H_c / (1 + e_0) * math.log10(σ_pp / σ_0p)  +  C_c * H_c / (1 + e_0) * math.log10((σ_0p + Δσ_p) / σ_pp)
                    else:
                        raise ValueError(f"Valor de σ_pp (Esfuerzo de preconsolidación) fuera de rango (σ_0p, σ_pp): ({σ_0p}, {σ_pp})")
                    S_c += dS_c

                    iteraciones.append({"d":d,"H_c":H_c, "z":z, "M":M, "N":N, "V":V, "V_1":V_1, "I_z":I_z, "Δσ_p":Δσ_p, "σ_0p":σ_0p, "C_c":C_c, "C_s":C_s, "e_0":e_0, "σ_pp":σ_pp, "dS_c":dS_c})

            d += estrato.H_0

        # memoria
        memoria = { "iteraciones": iteraciones}

        return (S_c, memoria)

    def interpolar_Iz_elastico(self, z:float) -> float:
        """
        Calcula el factor de influencia de la deformación unitaria

        Arguments:
            z {float} -- Distancia vertical, por debajo del centro de la cimentación, en donde se desea calcular el Iz

        Returns:
            float -- Valor del Iz a la distancia z
        """
        x, = self.get_atributos("x")

        # Iz es 0 cuando z = 0 o cuando z = 2x y 0.6 cuando z = x/2
        if z >= 0 and z < x / 2:
            return 1.2 / x * z
        elif z >= x / 2 and z < 2 * x:
            return -0.4 / x * z + 0.8
        else:
            return 0

    def calculo_asentamiento_roca(self, D:float, F_zc:float) -> Tuple[float, Memoria]:
        B, perfil, γ_r = self.get_atributos("B", "perfil", "γ_r")

        # estrato
        estrato = perfil.estrato_en(D + 0.01)

        # q_0: Cargas verticales [kN]
        q_0 = (self.peso_dado() + F_zc + γ_r * self.volumen_relleno()) / B**2

        #S: Asentamiento [m]
        S = 1.12 * q_0 * B * (1 - estrato.roca_ν_rm**2) / estrato.roca_E_rm

        #memoria
        memoria = {"q_0": q_0}

        return (S, memoria)

    def calculo_asentamiento_grupo(self, k:int, F_zc:float, F_zc_eds:float, t:float) -> Tuple[float, Memoria]:
        """
        Calcula el asentamiento del grupo de pilotes
        """
        D_c, D, x, perfil = self.get_atributos("D_c", "D", "x", "perfil")

        # φ_D: Ángulo de fricción para calcular el límite inferior del suelo relevante [°]
        φ_D = perfil.estrato_en(D).φ_s

        # B_lim: límite inferior del suelo relevante [m]
        B_lim = D_c * tan_g(45 + φ_D / 2)

        # Porcentajes de tipos de material de suelo entre D y D + B_lim
        porcentajes = perfil.calcular_porcentaje_tipo_mat(D, D + B_lim)

        if porcentajes["c"] >= 30.0:
            
            #S_g : Asentamiento grupo
            S_g = self.calculo_asentamiento(k, F_zc, F_zc_eds, t)

        else:
                        
            S_t = self.calculo_asentamiento(k, F_zc, F_zc_eds, t)

            S_g = S_t * math.sqrt(x / D_c)

        memoria = {}

        return S_g, memoria

    ######################################################################
    # Cálculos de fuerzas actuantes
    ######################################################################
    def calculo_carga_maxima_pilote(self, F_z:float, F_hl:float, F_ht:float):
        D_f, n, N_pL, HG, S_ep, f_carga_p = self.get_atributos("D_f", "n", "N_pL", "HG", "S_ep", "f_carga_p")

        w_dado = self.peso_dado()
        w_relleno = self.peso_relleno()

        # P_p: Carga máxima de un pilote [kN]
        P_p = f_carga_p * (F_z + w_dado + w_relleno) / n + (HG + D_f) * (F_hl + F_ht) / S_ep / N_pL

        P_h = math.sqrt(F_hl**2 + F_ht**2) / n

        return P_p, P_h

    def calculo_carga_maxima_pilote_tension(self, F_z:float, F_hl:float, F_ht:float):
        D_f, n, N_pL, HG, S_ep, f_carga_p = self.get_atributos("D_f", "n", "N_pL", "HG", "S_ep", "f_carga_p")

        W_dado = self.peso_dado()
        W_cono = self.peso_cono

        # P_p: Carga máxima de un pilote [kN]
        P_p = max(0, f_carga_p * (F_z - W_dado - W_cono) / n + (HG + D_f) * (F_hl + F_ht) / S_ep / N_pL) 

        P_h = math.sqrt(F_hl**2 + F_ht**2) / n

        return P_p, P_h
