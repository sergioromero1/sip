import math
from typing import List, Dict, Tuple, Any
from .util import sin_g, cos_g, tan_g, cot_g, γ_agua, π, calcular_C_d, Memoria, calcular_I_f, rad
from .perfil import Perfil, Estrato
from .pilastra import Pilastra

class PilastraGeb(Pilastra):
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
        super(PilastraGeb, self).__init__(h_i, D_p, H, HG, TP, θ, γ_c, perfil, ω)

    def get_r(self):
        return 1.0

    def calculo_carga_lateral(self, F_zc: float) -> Tuple[float, Memoria]:
        """
        Calcula capacidad ante carga lateral
        
        Arguments:
            Fz_c {float} -- Componente vertical de la carga a compresión [kN]
                
        Returns:
            Tuple[float,Memoria] -- (Q_L Resistencia a la carga lateral [kN], memoria)
        """
        
        D_p, H, D, perfil = self.get_atributos("D_p", "H", "D", "perfil")
        
        estrato = perfil.estrato_en(D)
        
        #RQD : RQD del estrato [%]
        RQD = estrato.RQD
        
        #γ: Peso unitario [kN/m³]
        _, _, γ = self.parametros_admisibles_de_resistencia(RQD)
        
        #φ_rm : Angulo de friccion roca en la profundidad D[°]
        φ_rm = estrato.roca_φ_rm
        
        #Kp_roca : Coeficiente de presión pasiva de la roca [adimensional]
        Kp_roca = tan_g(45 + φ_rm / 2)**2
        
        #γ_e : Peso unitario efectivo [kN/m³]
        γ_e = min(γ, estrato.γ_rse)
        
        # F_p : Empuje pasivo en la pilastra  [kN]
        F_p = 3 * γ_e * Kp_roca * H ** 2 * D_p / 2
        
        # R_LF: Resultante lateral debida a la interacción entre el suelo de fundación y la base del cimiento [kN]
        R_LF = F_zc * tan_g(2 / 3 * φ_rm)
        
        # Q_L: Resistencia a la carga lateral [kN]
        Q_L = F_p + R_LF
        

        memoria = {"F_p": F_p, "R_LF":R_LF, "φ_rm": φ_rm}
        
        return (Q_L, memoria)

    def calculo_volcamiento(self, F_zc:float, F:float) -> Tuple[float, float, Memoria]:
        """
        Calcula el momento de vuelco y el momento estabilizador es en suelos granulares o cohesivos (Solicitud y Capacidad).
        
        Arguments:
            Fz_c {float} -- Carga axial a tracción [kN]
            F {float} -- Resultante carga lateral asociada a la tracción máxima (Transversal y Longitudinal) [kN]        

        Returns:
            Tuple[float,float,Memoria] -- (Mv: Momento de vuelco [kN·m], Me: Momento estabilizador [kN·m], memoria)
        """
        D_p, H, C, θ, D, perfil  = self.get_atributos("D_p", "H", "C", "θ", "D", "perfil")

        estrato = perfil.estrato_en(D)

        #RQD : RQD del estrato [%]
        RQD = estrato.RQD

        _, _, γ = self.parametros_admisibles_de_resistencia(RQD)

        # M_wc : Momento estabilizador por peso de la cimentación [kN·m]
        M_wc = (self.peso()+ self.peso_relleno()) * D_p / 2        #falta el peso del relleno

        φ_rm = estrato.roca_φ_rm
        #Kp_roca : Coeficiente de presión pasiva de la roca [adimensional]
        Kp_roca = tan_g(45 + φ_rm / 2)**2

        γ_e = min(γ, estrato.γ_rs)
        # R_p : Empuje pasivo en la pilastra  [kN]
        R_p = γ_e * Kp_roca * H ** 2 * D_p / 2

        # M_p : Momento por Empuje pasivo en la pilastra  [kN·m]
        M_p = R_p * H / 3
    
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
        memoria = {"M_wc": M_wc, "R_p": R_p, "M_p": M_p, "F_r": F_r, "M_fr":M_fr,}
        
        return (Mv, Me, memoria)