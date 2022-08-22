import math
from typing import List, Dict, Tuple, Any
from .util import sin_g, cos_g, tan_g, cot_g, γ_agua, π, calcular_C_d, Memoria, calcular_I_f, rad
from .perfil import Perfil, Estrato
from .pilastra import Pilastra

class PilastraIsa(Pilastra):
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
        super(PilastraIsa, self).__init__(h_i, D_p, H, HG, TP, θ, γ_c, perfil, ω)

    