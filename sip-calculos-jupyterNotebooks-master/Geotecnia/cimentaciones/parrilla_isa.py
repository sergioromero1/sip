import math
from typing import List, Dict, Tuple, Any
from .util import sin_g, cos_g, tan_g, cot_g, γ_agua, π, calcular_C_d, Memoria, calcular_I_f, rad
from .perfil import Perfil, Estrato

class Parrilla:
    """
    Cimentación tipo zapata en suelo

    Attributes:
        B {float} -- Ancho de la zapata [m]
        L {float} -- Largo de la zapata [m]
        D {float} -- Profundidad de la zapata [m]
        C {float} -- Altura total del pedestal [m]
        θ {float} -- Ángulo del pedestal con respecto a la vertical [°]
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
                    peso:float,
                    esf_act_diseno: float,
                    mv_diseno: float,
                    perfil:Perfil,                     
                    α:float, 
                    ω:float):
        """
        Inicializa la zapata
        
        Arguments:
            B {float} -- Ancho de la zapata [m]
            L {float} -- Largo de la zapata [m]
            D {float} -- Profundidad de la zapata [m]
            C {float} -- Altura total del pedestal [m]
            θ {float} -- Ángulo del pedestal con respecto a la vertical [°]
            peso {float} -- Peso de la parrilla [kN]
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
        self.peso = peso
        self.esf_act_diseno = esf_act_diseno
        self.mv_diseno = mv_diseno
        self.perfil = perfil
        self.α = α
        self.ω = ω

        info_mat_relleno = self.perfil.calcular_material_relleno(self.D)
        self.tipo_mat_r, self.φ_r, self.c_u_r, self.γ_r  = (info_mat_relleno["tipo_mat"], info_mat_relleno["φ"], info_mat_relleno["c_u"], info_mat_relleno["γ"])
        self.γ_r_total  = info_mat_relleno["γ_total"]

        self.validar_atributos()

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

    def volumen_relleno(self) -> float:
        """
        Calcula el volumen del relleno.

        Returns:
            float -- Volumen del relleno [m³]
        """
        B, L, D = self.get_atributos("B", "L", "D")

        return B * L * D 

    def peso_relleno(self) -> float:
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
        info_mat_relleno = self.perfil.calcular_material_relleno(self.D)
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

    def calcular_parametros_de_suelo(self):
        """Calcula parametros """

        perfil, D = self.get_atributos("perfil", "D")

        # NF: Nivel freático [m]
        #NF = perfil.calcular_NF()

        # Porcentajes de tipos de material de suelo hasta D
        porcentajes = perfil.calcular_porcentaje_tipo_mat(0, D)

        if porcentajes["c"] /(porcentajes["c"] + porcentajes["g"]) >= 0.3:
            tipo_de_material = 'cohesivo'
            γ = perfil.calcular_promedio_γ(D)
            φ = perfil.calcular_promedio(0 , D, "φ_s")
            c_u = perfil.calcular_promedio(0, D, "c_u", tipo_mat="c")

        else:
            tipo_de_material = 'granular'
            γ = perfil.calcular_promedio_γ(D)
            φ = perfil.calcular_promedio(0 , D, "φ_s")
            c_u = perfil.calcular_promedio(0 , D, "c_u", tipo_mat="c")

        return γ, φ, c_u, tipo_de_material

    def calculo_capacidad_portante_isa(self, calcular_hasta_D = False):

        """
        Se requiere que se pueda escoger si 
        se utiliza el perfil hasta donde está o
        si se extiende el perfil. 
        En general la profundidad de exploración es 3m
        En el input debe estar la opcion extender perfil o 
        usar perfil hasta 3m. 
        cu, fi, gamma.
        """

        B, L, D, θ, ω, α, perfil = self.get_atributos("B", "L", "D", "θ", "ω","α", "perfil")

        estrato_en_D = perfil.estrato_en(D + 0.01)

        φ_D = estrato_en_D.φ_s
        B_lim = B * tan_g(45 + φ_D / 2.0)

        inicial  = D
        final = D + B_lim

        if calcular_hasta_D:
            inicial = 0
            final = D

        # Porcentajes de tipos de material de suelo hasta D
        porcentajes = perfil.calcular_porcentaje_tipo_mat(inicial, final)

        if porcentajes["c"] /(porcentajes["c"] + porcentajes["g"]) >= 0.3:
            tipo_de_material = 'cohesivo'
        else:
            tipo_de_material = 'granular'

        φ = perfil.calcular_promedio(inicial, final, "φ_s")

        c_u = perfil.calcular_promedio(inicial, final, "c_u", tipo_mat="c")

        q = perfil.calcular_q(D)
        
        s_q = 1 + (B / L) * tan_g(φ)

        s_γ = 1 - 0.4 * (B / L)

        i_c = (1 - θ / 90)**2

        i_q = (1 - θ / 90)**2

        #g_q, g_γ  Factores por inclinacion del terreno
        g_q = (1 - tan_g(ω))**2
        g_γ = g_q

        #b_q, b_γ Factores por inclinacion de la base
        b_q = (1 - rad(α) * tan_g(φ))**2
        b_γ = b_q

        if tipo_de_material == 'cohesivo':

            γ = perfil.calcular_promedio(inicial, final, 'γ_s')

            # N_c: Factor de capacidad portante debido a la cohesión. [-]
            N_c = 5.14
            
            # N_q: Factor de capacidad portante debido a la sobrecarga. [-]
            N_q = 1

            s_c = 1 + (B / L) * (N_q / N_c)

            d_q = 1 
            d_c = 1 + 0.4 * math.atan2(D, B) if D / B > 1 else 1 + 0.4 * (D / B)
            i_γ = 1

            #b_c: Factor por inclinacion de la base
            b_c = 1 - (2 * rad(ω) / 5.14 / tan_g(φ))

            #g_c: Factor por inclinacion del terreno
            g_c = i_q - ((1 - i_q) / 5.14 / tan_g(φ))
            #q_ult = c_u * N_c * s_c * d_c * i_c + q * N_q * s_q * d_q * i_q
            
            q_ult_neto = c_u * N_c * s_c * d_c * i_c * g_c * b_c

            memoria = {"γ":γ, "φ":φ, "c_u":c_u, "tipo_de_material":tipo_de_material, "N_c": N_c, "N_q":N_q, "q":q, "s_q":s_q, "s_γ":s_γ, "i_c":i_c, "i_q":i_q, "g_q":g_q, "g_γ":g_γ, "b_q":b_q, "b_γ":b_γ, "s_c":s_c, "d_q":d_q, "d_c":d_c, "i_γ":i_γ, "g_c":g_c, "b_c":b_c}

            # sigma u = cu*nc*fc + gamaq *dF
            # sigma nu = sigma u - gamaq * df
            # todo en esfuerzos totales

        elif tipo_de_material == 'granular':

            γ_d = perfil.estrato_en(D).γ_se

            N_q = math.exp(π * tan_g(φ)) * tan_g(45 + φ / 2)**2

            N_c = (N_q - 1) * (1 / tan_g(φ))

            s_c = 1 + (B / L) * (N_q / N_c)

            # c_p: Cohesión efectiva del suelo [kN/m²]
            c_p = perfil.calcular_promedio(0, D, "c_p", tipo_mat="g")
            if c_p is None:
                c_p = 0

            #N_γ: Factor de capacidad portante debido al peso unitario del suelo de fundación. [-]
            N_γ = 2 * (N_q + 1) * tan_g(φ)

            d_γ = 1
            d_q = 1 + 2 * tan_g(φ) * (1 - sin_g(φ))**2 * math.atan2(D, B) if D / B > 1 else 1 + 2 * tan_g(φ) * (1 - sin_g(φ))**2 * (D / B)
            d_c = d_q - (1 - d_q) / (N_c * tan_g(φ))
            i_γ = 1 - θ / φ
            γ_d = perfil.estrato_en(D).γ_se

            #b_c: Factor por inclinacion de la base
            b_c = 1 - (2 * rad(ω) / 5.14 / tan_g(φ))

            #g_c: Factor por inclinacion del terreno
            g_c = i_q - ((1 - i_q) / 5.14 / tan_g(φ))
            #q_ult = 1 / 2  * B * γ_d * N_γ * d_γ * s_γ * i_γ + q * N_q * s_q * d_q * i_q

            q_ult_neto = (c_p * N_c * s_c * d_c * i_c * g_c * b_c
                            + 1 / 2  * B * γ_d * N_γ * d_γ * s_γ * i_γ * g_γ * b_γ
                            + q * N_q * s_q * d_q * i_q * g_q * b_q
                            )- q 

            memoria = {"γ_d":γ_d, "φ":φ, "c_u":c_u, "tipo_de_material":tipo_de_material, "N_q":N_q, "N_c":N_c, "N_γ": N_γ, "c_p":c_p,"q":q, "s_q":s_q, "s_γ":s_γ, "i_c":i_c, "i_q":i_q, "g_q":g_q, "g_γ":g_γ, "b_q":b_q, "b_γ":b_γ, "s_c":s_c, "d_γ":d_γ, "d_q":d_q, "d_c":d_c, "i_γ":i_γ, "g_c":g_c, "b_c":b_c }

            # sigma u = c_prima*nc*fc + gamaq(sumergido o efectivo) *dF * Nq * fq + 1/2 gama suelo fundacion(sumergido oefec) *B_prima*n_gamma*f_gamma
            # sigma nu = sigma u - gamaq(efectivo) * df

        # memoria de cálculo
        return (q_ult_neto, memoria)

    ######################################################################
    # Cálculos capacidad de carga al arrancamiento (2.2)
    ######################################################################

    def calculo_tension_isa(self, q_adm):

        B, L, D, H, TP, θ, perfil = self.get_atributos("B", "L", "D", "H", "TP", "θ", "perfil")

        # v_z: Volumen de la fundación bajo la superficie del terreno [m³]
        v_z = B * L * H + TP**2 * (D - H) / cos_g(θ)

        # NF: Nivel freático [m]
        NF = perfil.calcular_NF()
        
        # ψ: Ángulo de inclinación de las paredes del cono [°]
        if NF == None or NF >= D:     # Seco
            if q_adm >=  98.066:               # 1 kg/cm²
                ψ = 30
            else:
                ψ = 20
        elif NF < D:                 # Semi-sumergido
            ψ = 15

        # γ: Peso unitario promedio del suelo hasta la profundidad D [kN/m³]
        γ = perfil.calcular_promedio_γ(D)

        v_cono = D / 3 * (B**2 + (B + 2 * D * tan_g(ψ))**2 + math.sqrt(B**2 * (B + 2 * D * tan_g(ψ))**2))

        W_cono = γ * (v_cono)

        # W_f: Peso de la cimentación [kN]
        W_f = self.peso

        T_u = W_f + W_cono

        # memoria
        memoria = {"tipo_mat": "g", "W_f":W_f, "v_z":v_z, "v_cono":v_cono, "ψ":ψ, "γ":γ}

        return (T_u, memoria)

    ######################################################################
    # Cálculos asentamientos (2.3)
    ######################################################################
    def calculo_asentamiento_isa(self, k:int, F_zc:float, F_zc_eds:float, t:float) -> Tuple[float, Tuple[Memoria, Memoria]]:
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

        prof_perfil = perfil.calcular_profundidad_total()

        # Se ajusta el último estrato si el perfil no alcanza a cubrir D + 2 * B
        if prof_perfil < D + 2 * B:
            perfil[-1].H_0 +=  D + 2 * B - sum([estrato.H_0 for estrato in perfil])

        # W_c: Peso de la cimentación [kN]
        W_c = self.peso

        # W_c: Peso deL relleno [kN]
        W_r = self.peso_relleno()
        
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
        W_c = self.peso

        # W_c: Peso deL relleno [kN]
        W_r = self.peso_relleno()

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
        W_c = self.peso
        
        # W_c:  Peso del relleno [kN]
        W_r = self.peso_relleno()

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
        prof_fin = prof_roca if prof_roca else perfil.calcular_profundidad_total()
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
        W_c = self.peso
        
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
    def calculo_volcamiento_isa(self, F_zc:float, F:float, T_u:float) -> Tuple[float, float, Memoria]:
        """
        Calcula el momento de vuelco y el momento estabilizador es en suelos granulares o cohesivos (Solicitud y Capacidad).
        
        Arguments:
            Fz_c {float} -- Carga axial a tracción [kN]
            F {float} -- Máxima carga lateral asociada a la tracción máxima (Transversal o Longitudinal) [kN]
            T_u {float} -- Capacidad al arranque del cimiento [kN]        

        Returns:
            Tuple[float,float,Memoria] -- (Mv: Momento de vuelco [kN·m], Me: Momento estabilizador [kN·m], memoria)
        """
        B, D, C, θ = self.get_atributos("B", "D", "C", "θ")

        # Mv:  Momento de vuelco [kN·m]
        Mv = F_zc * (B / 2 - C * tan_g(θ)) + F * C
        
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
    # def calculo_carga_lateral(self, F_zc: float) -> Tuple[float, Memoria]:
    #     B, L, D, perfil  = self.get_atributos("B", "L", "D", "perfil")

    #     # R_LF: Resultante lateral debida a la interacción entre el suelo de fundación y la base del cimiento [kN]
    #     tipo_mat_en_D = perfil.estrato_en(D + 0.01).tipo_mat
    #     if  tipo_mat_en_D == "c":
            
    #         # c_uf: Resistencia al corte no drenado del suelo inmediatamente debajo de D_f  [kN/m²] 
    #         c_uf = perfil.estrato_en(D + 0.01).c_u if perfil.estrato_en(D + 0.01).c_u is not None else 0

    #         #c_a: Adherencia para la interfaz cimiento-suelo (material cohesivo). [kN/m²]
    #         c_a = 2 / 3 * c_uf

    #         R_LF = c_a * B * L

    #     elif tipo_mat_en_D == "g":
            
    #         # φ_f: Ángulo de fricción del suelo inmediatamente debajo de D_f [°]
    #         φ_f = perfil.estrato_en(D + 0.01).φ_s if perfil.estrato_en(D + 0.01).φ_s is not None else 0

    #         # δ: Es el ángulo de fricción para la interfaz suelo-fundación (material granular) [°]
    #         δ = 2 / 3 * φ_f

    #         R_LF = F_zc * tan_g(δ)

    #     elif tipo_mat_en_D == "r":
    #         # φ_f: Ángulo de fricción del suelo inmediatamente debajo de D_f [°]
    #         φ_f = perfil.estrato_en(D + 0.01).roca_φ_rm if perfil.estrato_en(D + 0.01).roca_φ_rm is not None else 0

    #         # δ: Es el ángulo de fricción para la interfaz suelo-fundación (material granular) [°]
    #         δ = 2 / 3 * φ_f

    #         R_LF = F_zc * tan_g(δ)

    #     # Q_L: Resistencia a la carga lateral [kN]
    #     Q_L = R_LF

    #     # memoria
    #     memoria = {"R_LF":R_LF, "tipo_mat_en_D": tipo_mat_en_D}
    #     if tipo_mat_en_D == "c":
    #         memoria["c_a"] = c_a
    #     elif tipo_mat_en_D == "g":
    #         memoria["δ"] = δ

    #     return (Q_L, memoria)

    def calculo_carga_lateral_isa(self, F_zc: float) -> Tuple[float, Memoria]:
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
        B, D, C = self.get_atributos("B", "D", "C")

        # W_c: Peso de la cimentación [kN]
        W_c = self.peso

        # W_r: Peso del relleno [kN]
        W_r = self.peso_relleno_seco()

        # Fvo: Carga total a compresión [kN]
        Fvo = Fz_c + W_c + W_r

        MX = self.calculo_momento_carga_axial(Fz_c)

        # MT_o
        MT = Fy_c * C 
        MT_o = MT + MX

        # e_t: Excentricidad en la cara transversal [m]
        e_t = abs(MT_o / Fvo)

        # ML_o
        ML = Fx_c * C
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

        # Q_to: Incremento en los esfuerzos debido al momento transversal
        Q_to = abs(6 * MT_o / B**3)
        
        # Q_lo: Incremento en los esfuerzos debido al momento longitudinal
        Q_lo = abs(6 * ML_o / B**3)

        # Q_med: Esfuerzo actuante promedio [kPa]
        Q_med = Fvo / A_p

        # Q_min: Esfuerzo mínimo actuante [kPa]
        Q_min = Q_med - Q_to - Q_lo

        # Q_max: Esfuerzo máximo actuante [kPa]
        Q_max = Q_med + Q_to + Q_lo

        # memoria
        memoria = {"W_c":W_c, "W_r":W_r, "Fvo":Fvo, "MT": MT,"MT_o":MT_o, "ML": ML, "ML_o":ML_o, "e_t":e_t, "e_l":e_l, "B_t":B_t, "B_l":B_l, "A_p":A_p, "Q_to":Q_to, "Q_lo":Q_lo, "Q_med":Q_med}

        return (Q_max, Q_min, memoria)

    def calculo_momento_carga_lateral(self, F_c:float) -> Tuple[float, Memoria]:
        """Calcula el momento transversal o longitudinal dependiendo de acuerdo a la carga F_c
        
        Arguments:
            φ_s {float} -- Ángulo de fricción del suelo asumido para el cálculo del momento [°]
            F_c {float} -- Carga transversal o longitudinal cartesiana [kN]
        
        Returns:
            Tuple[float, Memoria] -- (Momento transversal o longitudinal dependiendo de la carga F_c [kN/m²], memoria)        
        """
        C, = self.get_atributos("C")

        M = F_c * C

        memoria = {}

        return (M, memoria)

    def calculo_momento_carga_axial(self, F_zc: float):
        C, θ = self.get_atributos("C", "θ")

        brazo = C * tan_g(θ)
        M = - F_zc * brazo

        return M

