import math
from typing import List, Dict, Tuple, Any
from .util import sin_g, cos_g, tan_g, cot_g, γ_agua, π, calcular_C_d, Memoria, calcular_I_f, rad
from .perfil import Perfil, Estrato
from .pilastra import Pilastra

class PilastraDas(Pilastra):
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
        super(PilastraDas, self).__init__( h_i, D_p, H, HG, TP, θ, γ_c, perfil, ω)

    def calcular_areas_por_brazos(self, prof:float) -> float:
        """Calcula  el producto de las areas correspondientes al empuje lateral por sus respectivos
            brazos desde el inicio de la pilastra

            Se usa para calcular el centroide de la fuerza resultante por empuje pasivo 

            Returns:
            {float} -- areas_por_brazos: area representativa de empuje lateral de cada trapecio por su brazo correspondiente  desde el inicio de la pilastra [kN]
                                    
        """

        perfil, D, H = self.get_atributos("perfil", "D", "H")

        areas_por_brazos = 0
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
                p = (acum_esf_vert + estrato.γ_se * Δ_z) * K_p
                area_rectangulo = Δ_z * min(p, p_ant)
                area_triangulo = (max(p, p_ant) - min(p, p_ant))/2
                brazo_rectangulo = Δ_z / 2 + D - (z + Δ_z)
                brazo_triangulo = Δ_z / 3 + D - (z + Δ_z)

            elif estrato.tipo_mat == "c":
                c_u = estrato.c_u
                p_ant = acum_esf_vert + 2 * c_u
                p = (acum_esf_vert + estrato.γ_se * Δ_z) + 2 * c_u
                area_rectangulo = Δ_z * min(p, p_ant)
                area_triangulo = (max(p, p_ant) - min(p, p_ant))/2
                brazo_rectangulo = Δ_z / 2 + D - (z + Δ_z)
                brazo_triangulo = Δ_z / 3 + D - (z + Δ_z)

            else:
                φ_rm = estrato.roca_φ_rm
                
                #Kp_roca : Coeficiente de presión pasiva de la roca [adimensional]
                Kp_roca = tan_g(45 + φ_rm / 2)**2

                #c_roca: cohesion efectiva en el estrato [kN/m²]
                c_roca = estrato.roca_c_p_rm

                #RQD : RQD del estrato [%]
                RQD = estrato.RQD

                _, _, γ = self.parametros_admisibles_de_resistencia(RQD)

                #γ_e : Peso unitario efectivo [kN/m³]
                γ_e = min(γ, estrato.γ_re)

                
                p_ant = acum_esf_vert * Kp_roca + 2 * c_roca * Kp_roca**0.5

                p = (acum_esf_vert + γ_e * Δ_z) * Kp_roca + 2 * c_roca * Kp_roca**0.5

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

    def calculo_integral_presion_lateral_pasiva_desde_0(self, prof):
        """Calcula la integral de la presión lateral pasiva desde la profundidad 0 hasta la profundidad 'prof'
        para estratos de roca calcula con  φ y c'


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
                p = (acum_esf_vert + estrato.γ_se * Δ_z) * K_p
            elif estrato.tipo_mat == "c":
                c_u = estrato.c_u
                p_ant = acum_esf_vert + 2 * c_u
                p = (acum_esf_vert + estrato.γ_se * Δ_z) + 2 * c_u
            
            else: 
                
                φ_rm = estrato.roca_φ_rm
                
                #Kp_roca : Coeficiente de presión pasiva de la roca [adimensional]
                Kp_roca = tan_g(45 + φ_rm / 2)**2
                
                c_roca = estrato.roca_c_p_rm
                
                #RQD : RQD del estrato [%]
                RQD = estrato.RQD
                
                _, _, γ = self.parametros_admisibles_de_resistencia(RQD)

                #γ_e : Peso unitario efectivo [kN/m³]
                γ_e = min(γ, estrato.γ_re)
                
                p_ant = acum_esf_vert * Kp_roca + 2 * c_roca * Kp_roca**0.5
                
                p = (acum_esf_vert + γ_e * Δ_z) * Kp_roca + 2 * c_roca * Kp_roca**0.5
                

            acum_esf_vert += estrato.γ_rse * Δ_z
            acum += (p + p_ant) / 2 * Δ_z
            z += estrato.H_0

        return acum