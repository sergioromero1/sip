import math
import copy
from typing import List, Dict, Tuple, Any
from .util import sin_g, cos_g, tan_g, cot_g, γ_agua, π, calcular_C_d, Memoria, rad, calcular_I_f
from .perfil import Perfil, Estrato
from .barra import Barra
from .curvas import q_s_suelos_cohesivos, q_s_suelos_granulares

class Micropilotes:
    """
    Cimentación tipo micropilotes

    Attributes:
    """    
    def __init__(self, D_f: float, D_d: float, HG: float, H: float, TP: float, θ: float, γ_c:float, N_m: int, S_m: float, L_b: float, barra: Barra, D_p: float, 
                    η: float, proc_iny: str, f_pc: float, f_py: float,  A_camisa: float, db: float,  perfil: Perfil, α:float, ω:float, f_carga_mp: float,
                    α_exp: float, γ_l:float, L_c:float = 0.0):
        """
        Inicializa los micropilotes
        
        Arguments:
            D_f {float} -- Profundidad de la zapata [m]
            D_d {float} -- Altura del dentellón [m]
            HG {float} -- Altura del pedestal no enterrado [m]
            H {float} -- Espesor de la zapata [m]
            TP {float} -- Lado correspondiente a la sección transversal del pedestal [m]
            θ {float} -- Ángulo del pedestal con respecto a la vertical [°]
            γ_c {float} -- Peso unitario de la cimentación [kN/m³]
            N_m {int} -- Número de micropilotes
            S_m {float} -- Separación entre micropilotes [m]
            L_b {float} -- Longitud de la barra [m]
            barra {Barra} -- Barra del micropilote
            D_p {float} -- Diámetro de la perforación [m]
            η {float} -- Eficiencia de los micropilotes [-]
            proc_iny {str} -- Procedimiento de inyección (IGU, IRS)
            f_pc {float} -- Resistencia a la compresión del concreto [kPa]
            f_py {float} -- Esfuerzo de fluencia de la barra de refuerzo [kPa]
            A_camisa {float} -- Área nominal de la camisa [m²]
            db {float} -- Diámetro de la barra de refuerzo [m]
            perfil {Perfil} -- Perfil estratigráfico en el suelo
            α {float} -- Ángulo de inclinación de la base [°]
            ω {float} -- Ángulo de inclinación del terreno [°]
            f_carga_mp {float} -- Fracción de carga que toman los micropilotes [-]
            α_exp {float} -- Factor de expansión [-]
        """

        self.D_f = D_f
        self.D_d = D_d
        self.HG = HG
        self.H = H
        self.TP = TP
        self.θ = θ
        self.γ_c = γ_c
        self.N_m = N_m
        self.S_m = S_m
        self.L_b = L_b
        self.barra = barra
        self.D_p = D_p
        self.η = η
        self.proc_iny = proc_iny
        self.f_pc = f_pc
        self.f_py = f_py
        self.A_camisa = A_camisa
        self.db = db
        self.perfil = perfil
        self.α = α
        self.ω = ω
        self.f_carga_mp = f_carga_mp
        self.α_exp = α_exp
        self.γ_l = γ_l
        self.L_c = L_c

        # D_s {float} -- Diámetro del bulbo sellado [m]
        self.D_s = self.D_p * self.α_exp

        # dist_bor: Distancia del micropilote al borde del dado [m]
        self.dist_bor =  max(1.5 * self.D_s, 0.25)

        # S_em: Separación entre pilotes exteriores [m]
        self.S_em = self.S_m * (self.N_mL - 1)

        # x,y: Dimensiones efectivas del bloque que conforman los micropilotes
        self.x = self.y = self.S_em + self.D_s

        self.validar_atributos()

        self.ajustar_perfil()

    ######################################################################
    # Propiedades
    ######################################################################
    def get_en_sumergencia(self):
        D_f,  perfil = self.get_atributos("D_f", "perfil")
        NF = perfil.calcular_NF()
        return NF is not None and NF < D_f
    en_sumergencia = property(get_en_sumergencia)

    # B: Ancho de la zapata [m]    
    def get_B(self):
        anclaje = next(iter([geom["anclaje"] for geom in self.barra.geoms if geom["hg"]==self.HG]))
        B = 2 * self.dist_bor + (self.N_mL - 1) * self.S_m * math.sqrt(1 + tan_g(self.θ)**2) + 2 * anclaje * tan_g(self.θ)
        if self.D_d is not None and self.D_d > 0:
            B += 2 * self.E_d
        return B
    B = property(get_B)
    
    # L: Largo de la zapata [m] (Zapata cuadrada)
    def get_L(self):
        return self.B
    L = property(get_L)
    
    # E_d: Ancho del dentellón [m]    
    def get_E_d(self):
        return self.D_d
    E_d = property(get_E_d)
    
    # parametros_relleno
    def get_parametros_relleno(self):
        info_mat_relleno = self.perfil.calcular_material_relleno(self.D_f - self.H)
        return info_mat_relleno #{"tipo_mat": info_mat_relleno["tipo_mat"], "φ": info_mat_relleno["φ"], "c_u": info_mat_relleno["c_u"], "γ": info_mat_relleno["γ"]}
    parametros_relleno = property(get_parametros_relleno)

    # N_mL: Número de micropilotes por lado
    def get_N_mL(self):
        return self.N_m / 4 + 1
    N_mL = property(get_N_mL)

    # C: Altura total del pedestal [m]
    def get_C(self):
        return self.D_f + self.HG - self.H
    C = property(get_C)

    # volumen_dentellon: Volumen del dentellón [m²]
    def get_volumen_dentellon(self):
        return (4 * self.B - 4 * self.E_d) * self.E_d * self.D_d
    volumen_dentellon = property(get_volumen_dentellon)

    # peso_dentellon: Peso del dentellón [kN]
    def get_peso_dentellon(self):
        return self.volumen_dentellon * self.γ_c
    peso_dentellon = property(get_peso_dentellon)

    def get_volumen_dado(self):
        B, L, C, TP, θ, H, volumen_dentellon = self.get_atributos("B", "L", "C", "TP", "θ", "H", "volumen_dentellon")
        return (B * L * H +  TP**2 * C / cos_g(θ)) + volumen_dentellon
    volumen_dado = property(get_volumen_dado)

    def get_volumen_cono(self):
        B, D_f, H, C, HG, TP, θ  = self.get_atributos("B", "D_f", "H", "C", "HG", "TP", "θ")
        V_c = (B**2 * H +  TP**2 * (C - HG) / cos_g(θ)) 
        A_n = 30
        V_cono = D_f / 3 * (B**2 + (B + 2 * D_f * tan_g(A_n))**2 + math.sqrt(B**2 + (B + 2 * D_f * tan_g(A_n))**2 ) ) - V_c
        return V_cono
    volumen_cono = property(get_volumen_cono)

    def get_peso_cono(self):
        D_f, H, perfil = self.get_atributos("D_f", "H", "perfil")

        info_relleno = perfil.calcular_material_relleno(D_f - H)
        γ_r = info_relleno["γ"]

        return self.volumen_cono * γ_r
    peso_cono = property(get_peso_cono)    

    def get_peso_cono_seco(self):
        D_f, H, perfil = self.get_atributos("D_f", "H", "perfil")

        info_relleno = perfil.calcular_material_relleno(D_f - H)
        γ_r = info_relleno["γ_total"]

        return self.volumen_cono * γ_r
    peso_cono_seco = property(get_peso_cono_seco)    

    ######################################################################
    # Utilitarios
    ######################################################################

    def ajustar_perfil(self):
        B, x, D_f, L_b, perfil  = self.get_atributos("B", "x", "D_f", "L_b", "perfil")

        estrato_en_D = perfil.estrato_en(D_f + 0.01)

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

        # Para el cálculo del asentamiento se requiere D + 2 / 3 * L_b + 2 * x
        # y para el cálculo de capacidad portante D + B_lim
        profundidad_minima_requerida = D_f + max(2 / 3 * L_b + 2 * x, B_lim, L_b)

        prof_perfil = perfil.calcular_profundidad_total()

        # Se ajusta el último estrato si el perfil no alcanza la profundidad mínima requerida
        if prof_perfil < profundidad_minima_requerida:
            perfil[-1].H_0 +=  profundidad_minima_requerida - sum([estrato.H_0 for estrato in perfil]) 
            perfil[-1].prof_fin += profundidad_minima_requerida - sum([estrato.H_0 for estrato in perfil]) 

    def peso_dado_seco(self) -> float:
        B, L, C, TP, θ, H, γ_c, peso_dentellon = self.get_atributos("B", "L", "C", "TP", "θ", "H", "γ_c", "peso_dentellon")
        return (B * L * H +  TP**2 * C / cos_g(θ)) * γ_c + peso_dentellon

    def peso_dado(self) -> float:
        B, L, C, TP, θ, H, γ_c, peso_dentellon = self.get_atributos("B", "L", "C", "TP", "θ", "H", "γ_c", "peso_dentellon")
        if self.en_sumergencia:
            γ_c -= γ_agua            
        return (B * L * H +  TP**2 * C / cos_g(θ)) * γ_c + peso_dentellon

    def peso_micropilotes(self) -> float:
        D_s, L_b, N_m, γ_l = self.get_atributos("D_s", "L_b", "N_m", "γ_l")
        if self.en_sumergencia:
            γ_l -= γ_agua            
        return π / 4 * D_s**2 * L_b * N_m * γ_l     

    def volumen_relleno(self) -> float:
        """
        Calcula el volumen del relleno.

        Returns:
            float -- Volumen del relleno [m³]
        """
        B, L, D_f, H, TP, θ  = self.get_atributos("B", "L", "D_f", "H", "TP", "θ")

        return B * L * (D_f - H) - TP**2 * (D_f - H) / cos_g(θ)

    def peso_relleno(self) -> float:
        D_f, H, perfil = self.get_atributos("D_f", "H", "perfil")

        info_relleno = perfil.calcular_material_relleno(D_f - H)
        γ_r = info_relleno["γ"]

        return self.volumen_relleno() * γ_r

    def peso_relleno_seco(self) -> float:
        D_f, H, perfil = self.get_atributos("D_f", "H", "perfil")

        info_relleno = perfil.calcular_material_relleno(D_f - H)
        γ_r = info_relleno["γ_total"]

        return self.volumen_relleno() * γ_r

    def validar_atributos(self):
        #   - Obligatoriedad
        #   - Dominios especiales        
        #       - N_m solo puede tomar los valores: 1, 2, 3 ...?
        #       - proc_iny puede tomar los valores 'IRS' o 'IGU'
        #       - valores positivos
        #   - Restricciones en el perfil
        pass
    
    def get_atributos(self, *nombres: str) -> Tuple:
        """Retorna los atributos solicitados como una tupla"""

        #return (self.__dict__[nombre] for nombre in nombres)
        return (getattr(self, nombre) for nombre in nombres)

    def calculo_resistencia_por_fuste_micropilote(self) -> float:
        L_b, D_f, D_s, θ, proc_iny, perfil = self.get_atributos("L_b", "D_f", "D_s", "θ", "proc_iny", "perfil")

        # P_G: Capacidad de carga a compresión [kN]
        P_G = 0.0
        d = 0.0
        iteraciones = [] # memoria de cada iteracion
        NF_exploracion = perfil.get_nivel_freatico_exploracion()
        for estrato in perfil:
            if d + estrato.H_0 > D_f and d < D_f + L_b:
                # Δ_z
                if d < D_f:
                    if d + estrato.H_0 > D_f + L_b:
                        Δ_z = L_b
                    else:
                        Δ_z = d + estrato.H_0 - D_f
                elif d + estrato.H_0 > D_f + L_b:
                    Δ_z = D_f + L_b - d
                else:
                    Δ_z = estrato.H_0

                # q_s: Adherencia grouting-material térreo [kPa]
                if estrato.tipo_mat == "g":
                    N = estrato.N
                    # Corrección del N, cuando no se encontró saturado el estrato durante la exploración
                    if estrato.saturado and (NF_exploracion is None or d < NF_exploracion):
                        N = N / 2
                    q_s = q_s_suelos_granulares(proc_iny, N)
                elif estrato.tipo_mat == "c":
                    q_u = 2 * estrato.c_u
                    q_s = q_s_suelos_cohesivos(proc_iny, q_u)
                elif estrato.tipo_mat == "r":
                    ucs = estrato.ucs
                    q_s = 0.2 * ucs**0.5 * 1000

                P_G += q_s * π * D_s * Δ_z / cos_g(θ)

                iteraciones.append({"estrato_prof_ini": estrato.prof_ini,
                                    "Δ_z": Δ_z, 
                                    "q_s": q_s, 
                                    "tipo_mat": estrato.tipo_mat,
                                    "γ_rse": estrato.γ_rse, 
                                    "N": estrato.N, 
                                    "c_u": estrato.c_u, 
                                    "φ_s": estrato.φ_s, 
                                    "E_s": estrato.E_s,
                                    "roca_E_rm": estrato.roca_E_rm,
                                    "roca_φ_rm": estrato.roca_φ_rm,
                                    "RQD": estrato.RQD})

            d += estrato.H_0

        # 
        memoria = {"iteraciones": iteraciones}

        return (P_G, memoria)    

    def calculo_resistencia_por_fuste_micropilote_roca(self) -> float:
        L_b, D_f, θ, D_s, perfil = self.get_atributos("L_b", "D_f", "θ", "D_s", "perfil")

        # P_G: Capacidad de carga a compresión [kN]
        P_G = 0.0
        d = 0.0                
        iteraciones = [] # memoria de cada iteracion
        for estrato in perfil:
            if d + estrato.H_0 > D_f and d < D_f + L_b:
                # Δ_z
                if d < D_f:
                    if d + estrato.H_0 > D_f + L_b:
                        Δ_z = L_b
                    else:
                        Δ_z = d + estrato.H_0 - D_f
                elif d + estrato.H_0 > D_f + L_b:
                    Δ_z = D_f + L_b - d
                else:
                    Δ_z = estrato.H_0

                # q_s: Adherencia grouting-material térreo [kPa]
                if estrato.tipo_mat == "r":
                    ucs = estrato.ucs
                    q_s = 0.2 * ucs**0.5 * 1000
                    P_G += q_s * π * D_s * Δ_z / cos_g(θ)

                    iteraciones.append({"Δ_z": Δ_z, "q_s": q_s})

            d += estrato.H_0

        # 
        memoria = {"iteraciones": iteraciones}

        return (P_G, memoria)    

    ######################################################################
    # Capacidades varilla
    ######################################################################
    def calculo_carga_compresion_varilla(self) -> Tuple[float, Memoria]:
        """
        Calcula la capacidad a la carga a compresión en la varilla
        
        Returns:
            Tuple[float, Memoria] -- (P_c: Carga a compresión de la varilla [kN], memoria)
        """
        
        f_pc, barra, D_s, A_camisa, proc_iny  = self.get_atributos("f_pc", "barra", "D_s",  "A_camisa", "proc_iny")

        # A_grout: Área nominal de la lechada [m²]
        if proc_iny == "IGU":
            A_grout = π / 4 * (D_s**2)
        else:
            A_grout = π / 4 * (D_s**2 - barra.D**2)        
        
        # P_c: Carga a compresión de la varilla [kN]
        P_c = 0.4 * f_pc * A_grout + 0.47 * barra.f_y * (barra.area + A_camisa)

        # memoria
        memoria = {"A_grout": A_grout}

        return (P_c, memoria)
    
    def calculo_carga_tension_varilla(self) -> Tuple[float, Memoria]:
        """
        Calcula la capacidad a la carga a tesión en la varilla
        
        Returns:
            Tuple[float, Memoria] -- (P_t: Carga a tensión de la varilla [kN], memoria)
        """
        
        barra, A_camisa = self.get_atributos("barra", "A_camisa")
        
        # P_t: Carga a tensión de la varilla [kN]
        P_t = 0.55 * barra.f_y * (barra.area + A_camisa)

        # memoria
        memoria = {}
        
        return (P_t, memoria)

    def calculo_adherencia_barra_grouting(self) -> Tuple[float, Memoria]:
        """
        Calcula la capacidad de adherencia barra-grouting
        
        Returns:
            Tuple[float, Memoria] -- (P_br_gr: Capacidad de adherencia barra-grouting [kN], memoria)
        """

        L_b, barra = self.get_atributos("L_b", "barra")

        # P_br_gr: Adherencia barra-grouting [kPa]
        q_br_gr = 5000

        # P_br_gr: Capacidad de adherencia barra-grouting [kN]
        P_br_gr = q_br_gr * π * barra.D * L_b

        # memoria
        memoria = {"q_br_gr": q_br_gr}

        return (P_br_gr, memoria)
    
    def calculo_momento_admisible(self) -> float:
        barra, = self.get_atributos("barra")

        I = π / 64.0 * (barra.D**4 - barra.D_int**4) 
        M_adm = 0.55 * barra.f_y  * 2 * I / barra.D
        return M_adm

    ######################################################################
    # Cálculos capacidad portante (2.1)
    ######################################################################
    def calculo_capacidad_portante(self) -> Tuple[float, Memoria]:

        B, D_f, perfil  = self.get_atributos("B", "D_f", "perfil")

        prof_roca = perfil.calcular_profundidad_hasta_roca()

        if  prof_roca is not None and D_f >= prof_roca:
            return self.calculo_capacidad_portante_roca()
        else:
            # φ_D: Ángulo de fricción para calcular el límite inferior del suelo relevante [°]
            φ_D = perfil.estrato_en(D_f).φ_s

            # B_lim: límite inferior del suelo relevante [m]
            B_lim = B * tan_g(45 + φ_D / 2)          

            # prof_final
            prof_final = D_f + B_lim if prof_roca is None else min(D_f + B_lim , prof_roca)

            # Porcentajes de tipos de material de suelo entre D_f y D_f + B_lim
            porcentajes = perfil.calcular_porcentaje_tipo_mat(D_f, prof_final)

            # Se prefiere la formulación de suelos cohesivos si ellos constituyen el 30% o más
            if porcentajes["c"] >= 30.0:
                return self.calculo_capacidad_portante_suelos_cohesivos()
            else:
                return self.calculo_capacidad_portante_suelos_granulares()

    def calculo_capacidad_portante_suelos_granulares(self) -> Tuple[float, Memoria]:  
        """
        Calcula las capacidad portante última en suelos granulares (condición drenada). No se
        tene en cuenta los efectos de los momentos.
        
        Arguments:

        Returns:
            Tuple[float, Memoria] -- (q_ult: Capacidad portante última [kN/m²], memoria)
        """
        B, L, D_f, perfil, α, ω  = self.get_atributos("B", "L", "D_f", "perfil", "α", "ω")
        
        # q: Esfuerzo de sobrecarga efectivo a la profundidad de cimentación [kN/m²]
        q = perfil.calcular_q(D_f)

        # φ_D: Ángulo de fricción para calcular el límite inferior del suelo relevante [°]
        φ_D = perfil.estrato_en(D_f).φ_s

        # B_lim: límite inferior del suelo relevante [m]
        B_lim = B * tan_g(45 + φ_D / 2)

        # φ: Ángulo de fricción del suelo relevante [°]
        φ = perfil.calcular_promedio(D_f, D_f + B_lim, "φ_s", tipo_mat="g")

        # N_q: Factor de capacidad portante debido a la sobrecarga. [-]
        N_q = math.exp(π * tan_g(φ)) * tan_g(45 + φ / 2)**2

        # N_γ: Factor de capacidad portante debido al peso unitario del suelo de fundación. [-]
        N_γ = 2 * (N_q + 1) * tan_g(φ)

        # φ_rel: Ángulo de fricción relativo [-]
        φ_rel = (φ - 25) / 20

        # ν: Relación de Poisson [-]
        ν = 0.1 + 0.3 * φ_rel

        # E: Módulo de Young para la prfundidad D [kN/m²]
        E = perfil.calcular_promedio(D_f, D_f + B_lim, 'E_s')
        
        # I_r: Índice de rigidez [-]
        I_r = E / 2 / (1 + ν) / q / tan_g(φ)

        # ∆: Deformación volumétrica [-]
        Δ = 0.005 * q * 0.0093238 * (1 - φ_rel)

        # I_rr: Índice de rigidez reducido [-]
        I_rr = I_r/(1 + I_r * Δ)

        # I_rc: Índice de rigidez crítico [-]
        I_rc = 1 / 2 * math.exp(3.30 - 0.45 * B / L) * cot_g(45 - φ / 2)

        # ξ_γs, ξ_qs: Factores de corrección por Forma [-]
        ξ_γs = 1 - 0.4 * (B / L)
        ξ_qs = 1 + (B / L) * tan_g(φ)

        # ξ_γd, ξ_qd: Factores de corrección por Profundidad [-]
        ξ_γd = 1
        if D_f / B <= 1:
            ξ_qd = 1 + 2 * tan_g(φ) * (1 - sin_g(φ))**2 * (D_f / B)
        else:
            ξ_qd = 1 + 2 * tan_g(φ) * (1 - sin_g(φ))**2 * math.atan2(D_f, B)

        # ξ_qr, ξ_γr: Factores de corrección por Rigidez [-]
        if I_rr > I_rc:
            ξ_qr = 1
            ξ_γr = 1
        else:        
            ξ_qr = math.exp((-4.4 + 0.6 * (B / L)) * tan_g(φ) + (3.07 * sin_g(φ) * math.log10(2 * I_rr)/(1 + sin_g(φ))))
            ξ_γr = ξ_qr

        # ξ_γi, ξ_qi: Factores de corrección por Inclinación de la carga [-]
        ξ_γi = 1
        ξ_qi = 1

        # ξ_γt, ξ_qt: Factores de corrección por Inclinación en la base [-]
        ξ_γt = (1 - rad(α) * tan_g(φ))**2
        ξ_qt = ξ_γt

        # ξ_γg, ξ_qg: Factores de corrección por Pendiente de la superficie del terreno [-]
        ξ_qg = (1 - tan_g(min(φ / 2, ω)))**2
        ξ_γg = ξ_qg

        # γ: Peso unitario promedio del suelo en D a D + B_lim [kN/m³]
        γ = perfil.calcular_promedio(D_f, D_f + B_lim, 'γ_se')
        
        # q_ult: Capacidad portante última [kN/m²]
        q_ult = 1 / 2 * B * γ * N_γ * ξ_γs * ξ_γd * ξ_γr * ξ_γi * ξ_γt * ξ_γg + q * N_q * ξ_qs * ξ_qd * ξ_qr * ξ_qi * ξ_qt * ξ_qg

        # memoria de cálculo
        memoria = {"tipo_mat": "g" ,"q":q, "φ":φ, "N_q":N_q, "N_γ":N_γ, "ν":ν, "E":E, "I_rr":I_rr, "I_rc":I_rc, "ξ_γs":ξ_γs, "ξ_γd":ξ_γd, "ξ_γr":ξ_γr, "ξ_γi":ξ_γi, "ξ_γt":ξ_γt, "ξ_γg":ξ_γg, "ξ_qs":ξ_qs, "ξ_qd":ξ_qd, "ξ_qr":ξ_qr, "ξ_qi":ξ_qi, "ξ_qt":ξ_qt, "ξ_qg":ξ_qg, "γ":γ}

        return (q_ult, memoria)

    def calculo_capacidad_portante_suelos_cohesivos(self) -> Tuple[float, Memoria]:
        """
        Calcula las capacidad portante en suelos cohesivos (condición no drenada). No se
        tene en cuenta los efectos de los momentos.
        
        Arguments:

        Returns:
            Tuple[float, Memoria] -- (q_ult: Capacidad portante última [kN/m²], memoria)
        """ 
        B, L, D_f, perfil, α, ω  = self.get_atributos("B", "L", "D_f", "perfil", "α", "ω")

        # φ_D: Ángulo de fricción para calcular el límite inferior del suelo relevante [°]
        φ_D = perfil.estrato_en(D_f).φ_s

        # B_lim: límite inferior del suelo relevante [m]
        B_lim = B * tan_g(45 + φ_D / 2)

        # c_u: Resistencia no drenada [kN/m²]
        c_u = perfil.calcular_promedio(D_f, D_f + B_lim, "c_u")

        # E: Módulo de Young para la prfundidad D [kN/m²]
        E = perfil.calcular_promedio(D_f, D_f + B_lim, "E_s")

        # I_r: Índice de rigidez [-]
        I_r = E / 3 / c_u

        # I_r: Índice de rigidez reducido [-]
        I_rr = I_r

        # I_rc: Índice de rigidez crítico [-]
        I_rc = 1 / 2 * math.exp(3.30 - 0.45 * B / L)

        # q: Esfuerzo de sobrecarga total a la profundidad de cimentación D [kN/m²]
        q = perfil.calcular_q_con_γ_s(D_f)

        # ξ_cs, ξ_qs: Factores de corrección por Forma [-]
        ξ_cs = 1 + 0.2 * (B / L)
        ξ_qs = 1

        # ξ_cd, ξ_qd: Factores de corrección por Profundidad [-]
        if D_f / B <= 1:
            ξ_cd = 1 + 0.4 * (D_f / B)
        else:
            ξ_cd = 1 + 0.4 * math.atan2(D_f, B)
        ξ_qd = 1

        # ξ_cr, ξ_qr: Factores de corrección por Rigidez [-]
        if I_rr > I_rc:
            ξ_cr = 1
            ξ_qr = 1
        else:
            ξ_cr = 0.32 + 0.12 * (B / L) + 0.60 * math.log10*(I_rr)
            ξ_qr = 1

        # ξ_ci, ξ_qi: Factores de corrección por Inclinación de la carga [-]
        ξ_ci = 1
        ξ_qi = 1

        # ξ_ct, ξ_qt: Factores de corrección por Inclinación de la base [-]
        ξ_ct = 1 - 2 * rad(α) / (2 + π)
        ξ_qt = 1

        # ξ_cg, ξ_qg: Factores de corrección por Pendiente de la superficie del terreno [-]
        ξ_cg = 1 - 2 * rad(ω) / (2 + π)
        ξ_qg = 1

        # N_q: Factor de capacidad portante debido a la sobrecarga. [-]
        N_q = 1

        # N_γ: Factor de capacidad portante debido al peso unitario del suelo de fundación. [-]
        N_γ = 0

        # N_c: Factor de capacidad portante debido a la
        N_c = 5.14

        # q_ult: Capacidad portante última. [kN/m²]
        q_ult = N_c * c_u * ξ_cs * ξ_cd * ξ_cr * ξ_ci * ξ_ct * ξ_cg + q * N_q * ξ_qs * ξ_qd * ξ_qr * ξ_qi * ξ_qt * ξ_qg

        # memoria de cálculo
        memoria = {"tipo_mat": "c" ,"c_u":c_u, "E":E, "I_r":I_r, "I_rr":I_rr, "I_rc":I_rc, "q":q, "N_q": N_q, "N_γ": N_γ, "N_c": N_c, "ξ_cs":ξ_cs, "ξ_qs":ξ_qs, "ξ_cd":ξ_cd, "ξ_qd":ξ_qd, "ξ_cr":ξ_cr, "ξ_qr":ξ_qr, "ξ_ci":ξ_ci, "ξ_qi":ξ_qi, "ξ_ct":ξ_ct, "ξ_qt":ξ_qt, "ξ_cg":ξ_cg, "ξ_qg":ξ_qg}

        return (q_ult, memoria)

    def calculo_capacidad_portante_roca(self) -> Tuple[float, Memoria]:
        D_f, perfil = self.get_atributos("D_f", "perfil")

        estrato = perfil.estrato_en(D_f + 0.01)

        # q_ult: Capacidad portante última. [kN/m²]
        q_ult = 1.25 * math.sqrt(estrato.roca_s) * estrato.ucs * 1000 * (1 + math.sqrt(estrato.roca_m / math.sqrt(estrato.roca_s) + 1))

        return (q_ult, None)

    ######################################################################
    # Cálculos capacidad compresión
    ######################################################################
    def calculo_carga_compresion(self) -> Tuple[float, Memoria]:
        """
        Calcula la capacidad a compresión
        
        Returns:
            Tuple[float, Memoria] -- (P_permS: Capacidad a la compresión del grupo [kN], memoria)
        """

        N_m, η = self.get_atributos("N_m", "η")

        # P_G: Capacidad de carga a compresión de un micropilote[kN]
        P_G, memoria_iter = self.calculo_resistencia_por_fuste_micropilote()

        # P_permS: Capacidad a la compresión del grupo [kN]
        P_permS = P_G * N_m * η

        # memoria
        memoria = {"P_G": P_G}

        return (P_permS, {**memoria, **memoria_iter})

    ######################################################################
    # Cálculos asentamiento
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
        x, D_f, L_b, H, perfil, f_carga_mp = self.get_atributos("x", "D_f", "L_b", "H", "perfil", "f_carga_mp")

        # W_c: Peso de la cimentación [kN]
        W_c = self.peso_dado_seco()

        # W_r: Peso deL relleno [kN]
        W_r = self.peso_relleno_seco()
        

        # W_d: Peso del dentellón [kN]
        W_d = self.peso_dentellon

        # q_0: Magnitud de la presión transmitida al suelo de fundación [kN/m²]
        q_0 = (F_zc * f_carga_mp  + W_c + W_r + W_d) / x**2
        q_0_eds = (F_zc_eds * f_carga_mp  + W_c + W_r + W_d) / x**2

        #
        estrato = perfil.estrato_en(D_f + 0.01)
        if estrato.tipo_mat == "r":
            S_e, memoria_e = self.calculo_asentamiento_roca(D_f, F_zc)
            S_c, memoria_c = (0, None)
            q_0 = memoria_e["q_0"]
        else:
            #D: Profundidad de la zapata equivalente [m]
            D = D_f + 2 / 3 * L_b

            # tipo de material
            tipos = perfil.calcular_tipo_mat_distintos(D, D + 2 * x)
            tipos = [t for t in tipos if t != "r"]

            # Capacidad
            if len(tipos) == 1:
                if tipos[0] == "c":
                    S_e, memoria_e = self.calculo_asentamiento_elastico_suelos_cohesivos(D, x, q_0, perfil)
                    S_c, memoria_c = self.calculo_asentamiento_por_consolidacion(D, x, q_0_eds, perfil)
                elif tipos[0] == "g":
                    S_e, memoria_e = self.calculo_asentamiento_elastico_suelos_granulares(k, t, D, x, q_0, perfil)
                    S_c, memoria_c = (0, None)
            elif len(tipos) == 2:
                S_e, memoria_e = self.calculo_asentamiento_elastico_suelos_mixtos(k, t, D, x, q_0, perfil)
                S_c, memoria_c = self.calculo_asentamiento_por_consolidacion(D, x, q_0_eds, perfil)
            else: # solo roca
                S_e, memoria_e = self.calculo_asentamiento_roca(D, F_zc * f_carga_mp)
                S_c, memoria_c = (0, None)

        # Módulo de reacción vertical [kN/m³]
        kv = q_0 / (S_e + S_c)

        return (S_e, S_c, kv, memoria_e, memoria_c)

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
        prof_fin = prof_roca if prof_roca is not None else perfil.calcular_profundidad_total()
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
        prof_fin = prof_roca if prof_roca is not None else perfil.calcular_profundidad_total()
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
        B, perfil, parametros_relleno = self.get_atributos("B", "perfil", "parametros_relleno")

        # relleno
        γ_r = parametros_relleno["γ_total"]

        # estrato
        estrato = perfil.estrato_en(D + 0.01)

        # q_0: Cargas verticales [kN/m²]
        q_0 = (self.peso_dado_seco() + F_zc + γ_r * self.volumen_relleno()) / B**2

        #S: Asentamiento [m]
        S = 1.12 * q_0 * B * (1 - estrato.roca_ν_rm**2) / estrato.roca_E_rm

        #memoria
        memoria = {"q_0": q_0}

        return (S, memoria)

    ######################################################################
    # Cálculos capacidad de carga a la tensión
    ######################################################################
    def calculo_tension(self) -> Tuple[float, Memoria, float, Memoria]: # Retorna la capacidad por roca y suelo
        perfil, = self.get_atributos("perfil")

        Q_ug_roca, memoria_roca, Q_ug_suelo, memoria_suelo = None, None, None, None
        
        tipos_mat = perfil.calcular_tipo_mat_distintos(self.D_f, perfil.calcular_profundidad_total())
        if "r" in tipos_mat:
            Q_ug_roca, memoria_roca = self.calculo_tension_roca()
        else:
            Q_ug_roca, memoria_roca = 0, {}

        if "c" in tipos_mat and "g" in tipos_mat:
            Q_ug_suelo, memoria_suelo = self.calculo_tension_suelos_mixtos()
        elif "c" in tipos_mat:
            Q_ug_suelo, memoria_suelo = self.calculo_tension_suelos_cohesivos()
        elif "g" in tipos_mat:
            Q_ug_suelo, memoria_suelo = self.calculo_tension_suelos_granulares()

        return (Q_ug_roca, memoria_roca, Q_ug_suelo, memoria_suelo)

    def calculo_tension_suelos_granulares(self) -> Tuple[float, Memoria]:
        """
        Problemas/Dudas:
            - Se supone que el cálculo se hace de D_f a D_f + L_b ¿Qué pasa si se acaba el perfil antes?
            respuesta: Se debe analizar micropilotes con un L_b cubierto por la exploración
        """        
        D_f, θ, L_b, perfil, x = self.get_atributos("D_f", "θ", "L_b", "perfil", "x")

        # Q_ug: Capacidad de carga a la tensión [kN]
        Q_ug = 0
        d = 0.0
        A_base = 0
        interaciones = []
        for estrato in perfil:
            if d + estrato.H_0 > D_f and d < D_f + L_b and estrato.tipo_mat == "g":
                if d < D_f:
                    if d + estrato.H_0 < D_f + L_b:
                        Δ_z = d + estrato.H_0 - D_f
                    else:
                        Δ_z = L_b
                else:
                    if d + estrato.H_0 < D_f + L_b:
                        Δ_z = estrato.H_0
                    else:
                        Δ_z = D_f + L_b - d

                if d <= D_f:
                    A_top = (x +  L_b / 2)**2
                else:
                    A_top = A_base

                A_base = (math.sqrt(A_top) - Δ_z / cos_g(θ) / 2)**2

                Q_ug += (A_base + A_top + math.sqrt(A_base * A_top)) * Δ_z / cos_g(θ) / 3 * estrato.γ_rse
                interaciones.append({"Δ_z":Δ_z, "A_top": A_top, "A_base": A_base})
            elif d >=  D_f + L_b:
                break
            d += estrato.H_0

        # memoria
        memoria = {"tipo_mat":"g", "x": x, "interaciones": interaciones}
        
        return (Q_ug, memoria)

    def calculo_tension_suelos_cohesivos(self) -> Tuple[float, Memoria]:
        D_f, θ, N_m, L_b, D_s, perfil = self.get_atributos("D_f", "θ", "N_m", "L_b", "D_s", "perfil")
        x, y = self.get_atributos("x", "y")

        # Q_ug: Capacidad de carga a la tensión [kN]
        acum_Q_ug_1 = 0.0
        acum_Q_ug_2 = 0.0
        d = 0.0
        for estrato in perfil:
            if d + estrato.H_0 > D_f and d < D_f + L_b and estrato.tipo_mat == "c":
                if d < D_f:
                    if d + estrato.H_0 < D_f + L_b:
                        Δ_z = d + estrato.H_0 - D_f
                    else:
                        Δ_z = L_b
                else:
                    if d + estrato.H_0 < D_f + L_b:
                        Δ_z = estrato.H_0
                    else:
                        Δ_z = D_f + L_b - d
            
                acum_Q_ug_1 += Δ_z / cos_g(θ) * 2 * (x + y) * estrato.c_u
                acum_Q_ug_2 += Δ_z / cos_g(θ) * estrato.γ_rse
            elif d >=  D_f + L_b:
                break
            d += estrato.H_0
        
        Q_ug = acum_Q_ug_1 + self.peso_micropilotes() + self.peso_dado() + (x**2 - N_m *  π / 4 * D_s**2) * acum_Q_ug_2

        # memoria
        memoria = {"tipo_mat":"c", "x": x, "y": y, "acum_Q_ug_1": acum_Q_ug_1 }

        return (Q_ug, memoria)

    def calculo_tension_suelos_mixtos(self) -> Tuple[float, Memoria]:
        D_f, N_m, L_b, D_s, perfil, x = self.get_atributos("D_f", "N_m", "L_b", "D_s", "perfil", "x")

        d = 0.0
        Q_ug = 0.0
        for estrato in perfil:
            if d + estrato.H_0 > D_f and d < D_f + L_b and estrato.tipo_mat in ["c","g"]:
                # Δ_z, z
                if d < D_f:
                    if d + estrato.H_0 < D_f + L_b:
                        Δ_z = d + estrato.H_0 - D_f
                    else:
                        Δ_z = L_b
                    z = D_f + Δ_z / 2
                else:
                    if d + estrato.H_0 < D_f + L_b:
                        Δ_z = estrato.H_0
                    else:
                        Δ_z = D_f + L_b - d
                    z = d + Δ_z / 2

                if estrato.tipo_mat == "g":
                    σ_0 = perfil.calcular_q(z)
                    φ_s = estrato.φ_s
                    Q_ug += 4 * x * (1 - sin_g(φ_s)) * σ_0 * 2 / 3 * tan_g(φ_s) * Δ_z + (x**2 - N_m * π / 4 * D_s**2) * estrato.γ_rse * Δ_z
                elif estrato.tipo_mat == "c":
                    c_u = estrato.c_u
                    Q_ug += 4 * x * c_u * Δ_z + (x**2 - N_m * π / 4 * D_s**2) * estrato.γ_rse * Δ_z

            elif d >= D_f + L_b:
                break

            d += estrato.H_0
        
        Q_ug += self.peso_micropilotes() + self.peso_dado()

        # memoria
        memoria = {"tipo_mat":"m"}

        return (Q_ug, memoria)

    def calculo_tension_roca(self) -> Tuple[float, Memoria]:
        N_m, = self.get_atributos("N_m")

        # P_G: Capacidad de carga a compresión de un micropilote[kN]
        P_G, memoria_iter = self.calculo_resistencia_por_fuste_micropilote_roca()

        # Q_ug: Capacidad de carga a la tensión [kN]
        Q_ug = P_G * N_m + self.peso_micropilotes() + self.peso_dado()

        # memoria
        memoria = {"P_G": P_G}

        return (Q_ug, {**memoria, **memoria_iter})

    ######################################################################
    # Cálculos capacidad a la carga lateral
    ######################################################################
    def calculo_carga_lateral(self, F_am: float) -> Tuple[float, Memoria]:
        B, L, D, H, D_d, TP, parametros_relleno, perfil, f_carga_mp  = self.get_atributos("B", "L", "D_f", "H", "D_d", "TP", "parametros_relleno", "perfil", "f_carga_mp")
        tipo_mat_r = parametros_relleno["tipo_mat"]
        c_u_r = parametros_relleno["c_u"]
        φ_r = parametros_relleno["φ"]
        γ_r = parametros_relleno["γ"]

        K_pr = None
        if tipo_mat_r == "g":
            # K_pr: Coeficiente de presión pasivo de tierra del relleno de fundación [-]
            K_pr = (1 + sin_g(φ_r)) / (1 - sin_g(φ_r))
            fuerza_horz_pasiva_pedestal = K_pr * γ_r * (D - H)**2 * TP / 2
        elif tipo_mat_r == "c":
            fuerza_horz_pasiva_pedestal = (γ_r * (D - H) + 2 * c_u_r) * (D - H) * TP / 2
        elif tipo_mat_r == "r":
            K_pr = (1 + sin_g(φ_r)) / (1 - sin_g(φ_r))
            fuerza_horz_pasiva_pedestal =  K_pr * γ_r * (D - H)**2 * TP / 2 + 2 * c_u_r * math.sqrt(K_pr) * (D - H) * TP

        # F_P: Fuerza horizontal producto del empuje pasivo [kN]
        F_P = self.calculo_integral_presion_lateral_pasiva(D - H, D + D_d) * B  + fuerza_horz_pasiva_pedestal

        K_ar = None
        if tipo_mat_r == "g":
            # K_ar: Coeficiente de presión activo de tierra del relleno de fundación [-]
            K_ar = (1 - sin_g(φ_r)) / (1 + sin_g(φ_r))
            fuerza_horz_activa_pedestal = K_ar * γ_r * (D - H)**2 * TP / 2
        elif tipo_mat_r == "c":
            fuerza_horz_activa_pedestal = max(0, (γ_r * (D - H) - 2 * c_u_r) * (D - H) * TP / 2)
        elif tipo_mat_r == "r":
            K_ar = (1 - sin_g(φ_r)) / (1 + sin_g(φ_r))
            fuerza_horz_activa_pedestal =  max(0, K_ar * γ_r * (D - H)**2 * TP / 2 - 2 * c_u_r * math.sqrt(K_ar) * (D - H) * TP)

        # F_A: Fuerza horizontal producto del empuje activo [kN]
        F_A = self.calculo_integral_presion_lateral_activa(D - H, D + D_d) * B  + fuerza_horz_activa_pedestal

        # R_LE: Resultante lateral debida a la diferencia de las fuerzas de los empujes [kN]
        R_LE = F_P - F_A

        # φ_f: Ángulo de fricción del suelo inmediatamente debajo de D_f [°]
        estrato_D = perfil.estrato_en(D + 0.01)
        φ_f = estrato_D.roca_φ_rm if estrato_D.tipo_mat == "r" else estrato_D.φ_s

        # c_uf: Resistencia al corte no drenado del suelo inmediatamente debajo de D_f  [kN/m²] 
        c_uf = perfil.estrato_en(D + 0.01).c_u if perfil.estrato_en(D + 0.01).c_u is not None else 0

        # R_LF: Resultante lateral debida a la interacción entre el suelo de fundación y la base del cimiento [kN]
        if perfil.estrato_en(D + 0.01).tipo_mat == "c":
            R_LF = 2 / 3 * c_uf * B * L
        elif perfil.estrato_en(D + 0.01).tipo_mat in ["g", "r"]:
            R_LF = (F_am * (1 - f_carga_mp) + self.peso_dado()) * tan_g(2 / 3 * φ_f)

        # Q_L: Resistencia a la carga lateral [kN]
        Q_L = R_LE + R_LF
        #Q_L = R_LF

        # memoria
        memoria = {"K_pr":K_pr, "F_P":F_P, "K_ar":K_ar, "F_A":F_A, "R_LE":R_LE, "φ_f":φ_f, "c_uf":c_uf, "R_LF":R_LF}

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
            if z + estrato.H_0 < prof:
                Δ_z = estrato.H_0
            elif z < prof:
                Δ_z = prof - z
            else:
                break
                        
            if estrato.tipo_mat == "g":
                φ_s = estrato.φ_s
                K_a = (1 - sin_g(φ_s)) / (1 + sin_g(φ_s))
                p_ant = acum_esf_vert * K_a
                p = (acum_esf_vert + estrato.γ_rse * Δ_z) * K_a
            elif estrato.tipo_mat == "c":
                c_u = estrato.c_u
                p_ant = max(0, acum_esf_vert - 2 * c_u)
                p = max(0, acum_esf_vert + estrato.γ_rse * Δ_z - 2 * c_u) 
            elif estrato.tipo_mat == "r":
                φ_s = estrato.roca_φ_rm
                K_a = (1 - sin_g(φ_s)) / (1 + sin_g(φ_s))
                p_ant = acum_esf_vert * K_a
                p = (acum_esf_vert + estrato.γ_rse * Δ_z) * K_a
            else:
                raise ValueError(f"Cálculo de presión lateral activa estrato desconocido: '{estrato.tipo_mat}'. profundidad = {z}")

            acum_esf_vert += estrato.γ_rse * Δ_z
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
            elif estrato.tipo_mat == "r":
                φ_s = estrato.roca_φ_rm
                K_p = (1 + sin_g(φ_s)) / (1 - sin_g(φ_s))
                p_ant = acum_esf_vert * K_p
                p = (acum_esf_vert + estrato.γ_rse * Δ_z) * K_p
            else:
                raise ValueError(f"Cálculo de presión lateral pasiva estrato desconocido: '{estrato.tipo_mat}'. profundidad = {z}")

            acum_esf_vert += estrato.γ_rse * Δ_z
            acum += (p + p_ant) / 2 * Δ_z
            z += estrato.H_0

        return acum

    ######################################################################
    # Cálculos solicitudes
    ######################################################################
    def calculo_carga_maxima_micropilote(self, F_am:float, F_hl: float, F_ht:float):
        D_f, N_m, N_mL, HG, S_em, f_carga_mp = self.get_atributos("D_f", "N_m", "N_mL", "HG", "S_em", "f_carga_mp")
        
        W_dado = self.peso_dado_seco()
        W_relleno = self.peso_relleno_seco()

        # P_mp: Carga máxima de un micropilote [kN]
        P_mp = f_carga_mp * (F_am + W_dado + W_relleno) / N_m + (HG + D_f) * (F_hl + F_ht) / S_em / N_mL

        return P_mp

    def calculo_carga_maxima_micropilote_tension(self, F_am:float, F_hl: float, F_ht:float):
        D_f, N_m, N_mL, HG, S_em, f_carga_mp = self.get_atributos("D_f", "N_m", "N_mL", "HG", "S_em", "f_carga_mp")

        W_dado = self.peso_dado()
        W_cono = self.peso_cono

        # P_mp: Carga máxima de un micropilote [kN]
        P_mp = max(0, (F_am - W_dado - W_cono) / N_m + (HG + D_f) * (F_hl + F_ht) / S_em / N_mL)

        return P_mp

