import math
import numpy as np
import statistics
from typing import List, Dict, Tuple, Any
from .util import sin_g, cos_g, tan_g, cot_g, γ_agua, π, calcular_C_d, Memoria, calcular_I_f, rad, generar_serie
from .perfil import Perfil, Estrato
from .pila import Pila

class PilaIsa(Pila):
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
        super(PilaIsa, self).__init__(D_p, h_i, H, HG, h_c, h_con, θ_c, TP, θ, γ_c, E_p, perfil, campana, ω)

        self.D_c = self.D_p

        if campana:
            self.D_c = self.D_p + tan_g(self.θ_c) * self.h_con * 2
                
        self.validar_atributos()

        # t {float} -- Distacia de la cresta al centro de la pila
        self.t = h_i / tan_g(ω) if self.ω > 0 else None

        info_mat_relleno = self.perfil.calcular_material_relleno(self.h_i)
        self.tipo_mat_r, self.φ_r, self.c_u_r, self.γ_r  = (info_mat_relleno["tipo_mat"], info_mat_relleno["φ"], info_mat_relleno["c_u"], info_mat_relleno["γ"])

    def _calcular_tipo_mat(self,inicial, final):

        """Calcular tipo de material desde profundidad incial hasta profundidad final"""

        perfil,  = self.get_atributos("perfil")
        
        porcentajes = perfil.calcular_porcentaje_tipo_mat(inicial, final)

        if porcentajes["c"] /(porcentajes["c"] + porcentajes["g"]) >= 0.3:
            tipo_de_material = 'cohesivo'
        else:
            tipo_de_material = 'granular'

        return tipo_de_material

    def _calcular_ψ_tronco_piramidal(self) -> float:

        """Calcula ψ segun tipo de material"""
        D, = self.get_atributos("D")
        
        tipo_de_material = self._calcular_tipo_mat(0, D)

        if tipo_de_material == 'granular':
            ψ = 30
        elif tipo_de_material == 'cohesivo':
            ψ = 20

        return ψ

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
        ψ = self._calcular_ψ_tronco_piramidal()

        if campana:
            Qsw = π * γ_s * H * (D_c**2 / 2 + D_c * H * tan_g(ψ) / 2 + H**2 * tan_g(ψ)**2 / 3)
        else:
            Qsw = π * γ_s * H * (D_c**2 / 2 + D_c * H * tan_g(ψ) / 2 + H**2 * tan_g(ψ)**2 / 3  + (D_c**2 - D_p**2) / 4)

        #T_un: Carga última a tensión 
        T_tp = Qsw + W

        memoria = {"D_c":D_c, "W":W,  "A_p":A_p, "γ_s":γ_s, "H":H, "ψ":ψ, "Qsw":Qsw}

        return (T_tp, memoria)




