# pylint: disable=W
import unittest
import time
import copy
from ..pila_isa import PilaIsa
from ..perfil import Perfil, Estrato

class TestCalculosPila(unittest.TestCase): 
    
    @classmethod
    def setUpClass(self):

        #Pila 1
        D_p, h_i, H, HG = 0.8, 0.5, 3, 0.7
        h_c, h_con, θ_c = None, None, None           
        TP, θ, γ_c = 0.6, 8 , 24
        E_p = 29400000
        campana = None
        ω = 0
        γ_r, φ_r = 16.4, 35
        perfil = Perfil([
            Estrato(H_0 = 5.0, γ_s = 21.0, E_s = 6597, c_u = 0, φ_s = 24, saturado = False, tipo_mat = "g", ν = 0.3, c_p = 0),
            Estrato(H_0 = 5.0, γ_s = 21.0, E_s = 7000, c_u = 0, φ_s = 27, saturado = False, tipo_mat = "g", ν = 0.35, c_p = 0),
        ], γ_r=γ_r, φ_r=φ_r)
        self.pila_1 = PilaIsa(D_p, h_i, H, HG, h_c, h_con, θ_c, TP, θ, γ_c, E_p, perfil, campana, ω)

        #Pila 2
        D_p, h_i, H, HG = 2, 1.2, 4, 2
        h_c, h_con, θ_c = None, None, None             
        TP, θ, γ_c = 0.6, 8 , 24
        E_p = 29400000
        campana = False
        ω = 0
        γ_r, φ_r = 16.4, 35
        perfil = Perfil([
            Estrato(H_0 = 1.0, γ_s = 21.0, E_s = 9324, c_u = 0, φ_s = 24, saturado = False, tipo_mat = "g",ν = 0.4, c_p = 0),
            Estrato(H_0 = 2.0, γ_s = 21.0, E_s = 15000, c_u = 0, φ_s = 24, saturado = False, tipo_mat = "g", ν = 0.35,c_p = 0),
            Estrato(H_0 = 2.1, γ_s = 21.0, E_s = 15000, c_u = 0, φ_s = 28, saturado = False, tipo_mat = "g", ν = 0.3, c_p = 0),
            Estrato(H_0 = 1.7, γ_s = 19.0, E_s = 5000, c_u = 24.63, φ_s = 25, saturado = False, tipo_mat = "c", ν = 0.3, c_p = 20, C_s = 0.014,e_0 = 1.91, σ_pp = 90),
            Estrato(H_0 = 1.5, γ_s = 19.0, E_s = 5000, c_u = 24.63, φ_s = 20, saturado = False, tipo_mat = "c", ν = 0.3,c_p = 0, C_s = 1,e_0 = 1.91, σ_pp = 90),
            Estrato(H_0 = 3.0, γ_s = 19.0, E_s = 5000, c_u = 24.63, φ_s = 20, saturado = False, tipo_mat = "c", ν = 0.3,c_p = 0, C_s = 1,e_0 = 1.91, σ_pp = 90),
            # Estrato(H_0 = 6.5, γ_s = 24.0, E_s = 130000, c_u = None, φ_s = None, saturado = False, tipo_mat = "r", ν = 0.4, c_p = 0, roca_φ_rm = 40, RQD = 20),
        ], γ_r=γ_r, φ_r=φ_r)
        self.pila_2 = PilaIsa(D_p, h_i, H, HG, h_c, h_con, θ_c, TP, θ, γ_c, E_p, perfil, campana, ω)

        #Pila 3
        D_p, h_i, H, HG = 1.7, 2, 3.5, 1.5
        h_c, h_con, θ_c = 0.5, 0.3, 30             
        TP, θ, γ_c = 0.6, 8 , 24
        E_p = 29400000
        campana = True
        ω = 0
        γ_r, φ_r = 16.4, 35
        perfil = Perfil([
            Estrato(H_0 = 1.5, γ_s = 21.0, E_s = 9324, c_u = 0, φ_s = 32, saturado = False, tipo_mat = "g", ν = 0.3, c_p = 0),
            Estrato(H_0 = 1.7, γ_s = 21.0, E_s = 15000, c_u = 0, φ_s = 28, saturado = False, tipo_mat = "g", ν = 0.3, c_p = 0),
            Estrato(H_0 = 1.7, γ_s = 19.0, E_s = 5000, c_u = 24.63, φ_s = 25, saturado = False, tipo_mat = "c", ν = 0.3, c_p = 20, C_s = 0.014,e_0 = 1.91, σ_pp = 90),
            Estrato(H_0 = 1.5, γ_s = 18.0, E_s = 12000, c_u = 26.13, φ_s = 22, saturado = False, tipo_mat = "c", ν = 0.3,  c_p = 15, C_s = 0.015,e_0 = 1.91, σ_pp = 90),
            Estrato(H_0 = 1.5, γ_s = 18.0, E_s = 12000, c_u = 26.13, φ_s = 22, saturado = False, tipo_mat = "c", ν = 0.3,  c_p = 15, C_s = 0.015,e_0 = 1.91, σ_pp = 90),
            Estrato(H_0 = 1.7, γ_s = 19.0, E_s = 5000, c_u = 24.63, φ_s = 25, saturado = False, tipo_mat = "c", ν = 0.3, c_p = 20, C_s = 0.014,e_0 = 1.91, σ_pp = 90),
            # Estrato(H_0 = 3.5, γ_s = 24.0, E_s = 130000, c_u = None, φ_s = None, saturado = False, tipo_mat = "r", ν = 0.3, c_p = 0, roca_φ_rm = 40, RQD = 20),
        ], γ_r=γ_r, φ_r=φ_r)
        self.pila_3 = PilaIsa(D_p, h_i, H, HG, h_c, h_con, θ_c, TP, θ, γ_c, E_p, perfil, campana, ω)

        #Pila 4
        D_p, h_i, H, HG = 1.8, 0.5, 2.5, 1 
        h_c, h_con, θ_c = None, None, None             
        TP, θ, γ_c = 0.6, 8 , 24
        E_p = 29400000
        campana = False
        ω = 0
        γ_r, φ_r = 16.4, 35
        perfil = Perfil([
            Estrato(H_0 = 1.5, γ_s = 21.0, E_s = 9324, c_u = 0, φ_s = 32, saturado = False, tipo_mat = "g",ν = 0.3, c_p = 0),
            Estrato(H_0 = 1.6, γ_s = 21.0, E_s = 15000, c_u = 0, φ_s = 28, saturado = False, tipo_mat = "g", ν = 0.2, c_p = 0),
            Estrato(H_0 = 1.2, γ_s = 19.0, E_s = 9324, c_u = 0, φ_s = 32, saturado = False, tipo_mat = "g", ν = 0.4, c_p = 0),
            Estrato(H_0 = 1.8, γ_s = 18.4, E_s = 13200, c_u = 0, φ_s = 27, saturado = False, tipo_mat = "g", ν = 0.3, c_p = 0),
            Estrato(H_0 = 1.7, γ_s = 21.0, E_s = 9324, c_u = 0, φ_s = 32, saturado = False, tipo_mat = "g", ν = 0.3, c_p = 0),
            Estrato(H_0 = 1.7, γ_s = 21.0, E_s = 15000, c_u = 0, φ_s = 28, saturado = False, tipo_mat = "g", ν = 0.3, c_p = 0),
            Estrato(H_0 = 3.0, γ_s = 21.0, E_s = 15000, c_u = 0, φ_s = 28, saturado = False, tipo_mat = "g", ν = 0.3, c_p = 0),
            # Estrato(H_0 = 3.5, γ_s = 24.0, E_s = 130000, c_u = None, φ_s = None, saturado = False, tipo_mat = "r", c_p = 0, ν = 0.3, roca_φ_rm = 40, RQD = 20),
        ], γ_r=γ_r, φ_r=φ_r)
        self.pila_4 = PilaIsa(D_p, h_i, H, HG, h_c, h_con, θ_c, TP, θ, γ_c, E_p, perfil, campana, ω)

        #Pila 5
        D_p, h_i, H, HG = 2.5, 1.3, 3, 1.5
        h_c, h_con, θ_c = None, None, None             
        TP, θ, γ_c = 0.6, 8 , 24
        E_p = 29400000
        campana = False
        ω = 0
        γ_r, φ_r = 16.4, 35
        perfil = Perfil([
            Estrato(H_0 = 1.2, γ_s = 19.0, E_s = 5000, c_u = 25.12, φ_s = 23, saturado = False, tipo_mat = "c", ν = 0.28, c_p = 20, C_s = 0.013,e_0 = 1.91, σ_pp = 90),
            Estrato(H_0 = 1.5, γ_s = 17.0, E_s = 14500, c_u = 26.13, φ_s = 24, saturado = False, tipo_mat = "c", ν = 0.32, c_p = 15, C_s = 0.015,e_0 = 1.91, σ_pp = 85),
            Estrato(H_0 = 1.6, γ_s = 19.0, E_s = 5000, c_u = 24.63, φ_s = 28, saturado = False, tipo_mat = "c", ν = 0.27, c_p = 20, C_s = 0.014,e_0 = 1.91, σ_pp = 112),
            Estrato(H_0 = 1.5, γ_s = 18.0, E_s = 12000, c_u = 19.42, φ_s = 22, saturado = False, tipo_mat = "c", ν = 0.3, c_p = 15, C_s = 0.017,e_0 = 1.91, σ_pp = 68),
            Estrato(H_0 = 1.2, γ_s = 19.0, E_s = 5000, c_u = 25.12, φ_s = 23, saturado = False, tipo_mat = "c", ν = 0.28, c_p = 20, C_s = 0.013,e_0 = 1.91, σ_pp = 90),
            Estrato(H_0 = 1.5, γ_s = 17.0, E_s = 14500, c_u = 26.13, φ_s = 24, saturado = False, tipo_mat = "c", ν = 0.32, c_p = 15, C_s = 0.015,e_0 = 1.91, σ_pp = 85),
            Estrato(H_0 = 1.6, γ_s = 19.0, E_s = 5000, c_u = 24.63, φ_s = 28, saturado = False, tipo_mat = "c", ν = 0.27, c_p = 20, C_s = 0.014,e_0 = 1.91, σ_pp = 112),
            Estrato(H_0 = 1.5, γ_s = 18.0, E_s = 12000, c_u = 19.42, φ_s = 22, saturado = False, tipo_mat = "c", ν = 0.3, c_p = 15, C_s = 0.017,e_0 = 1.91, σ_pp = 68),
            # Estrato(H_0 = 3.5, γ_s = 24.0, E_s = 130000, c_u = None, φ_s = None, saturado = False, tipo_mat = "r", ν = 0.32, c_p = 0, roca_φ_rm = 40, RQD = 20),
        ], γ_r=γ_r, φ_r=φ_r)
        self.pila_5 = PilaIsa(D_p, h_i, H, HG, h_c, h_con, θ_c, TP, θ, γ_c, E_p, perfil, campana, ω)

        #Pila 6
        D_p, h_i, H, HG = 2.2, 0.8, 2.5, 1.5
        h_c, h_con, θ_c = 0.5, 0.3, 30             
        TP, θ, γ_c = 0.6, 8 , 24
        E_p = 29400000
        campana = True
        ω = 0
        γ_r, φ_r = 16.4, 35
        perfil = Perfil([
            Estrato(H_0 = 1.0, γ_s = 18.0, E_s = 5000, c_u = None, φ_s = 23, saturado = False, tipo_mat = "g",ν = 0.4, c_p = 0),
            Estrato(H_0 = 1.5, γ_s = 17.5, E_s = 14500, c_u = 26.13, φ_s = 24, saturado = False, tipo_mat = "c",ν = 0.25, c_p = 15, C_s = 0.015,e_0 = 1.91, σ_pp = 85),
            Estrato(H_0 = 1.7, γ_s = 19.2, E_s = 5000, c_u = None, φ_s = 28, saturado = False, tipo_mat = "g",ν = 0.32, c_p = 0),
            Estrato(H_0 = 1.2, γ_s = 18.1, E_s = 12000, c_u = 19.42, φ_s = 22, saturado = False, tipo_mat = "c",ν = 0.35, c_p = 15, C_s = 0.017,e_0 = 1.91, σ_pp = 68),
            Estrato(H_0 = 3.5, γ_s = 22.4, E_s = 13000, c_u = None, φ_s = 31, saturado = False, tipo_mat = "g",ν = 0.3, c_p = 0),
        ], γ_r=γ_r, φ_r=φ_r)
        
        self.pila_6 = PilaIsa(D_p, h_i, H, HG, h_c, h_con, θ_c, TP, θ, γ_c, E_p, perfil, campana, ω)

        #Pila 7
        D_p, h_i, H, HG = 1.9, 1, 3.2, 2
        h_c, h_con, θ_c = None, None, None             
        TP, θ, γ_c = 0.6, 8 , 24
        E_p = 29400000
        campana = False
        ω = 0
        γ_r, φ_r = 16.4, 35
        perfil = Perfil([
            Estrato(H_0 = 1.5, γ_s = 21.0, E_s = 9324, c_u = 0, φ_s = 32, saturado = False, tipo_mat = "g",ν = 0.3, c_p = 0),
            Estrato(H_0 = 1.0, γ_s = 21.0, E_s = 15000, c_u = 0, φ_s = 26, saturado = False, tipo_mat = "g", ν = 0.2, c_p = 0),
            Estrato(H_0 = 1.5, γ_s = 19.0, E_s = 9324, c_u = 0, φ_s = 32, saturado = False, tipo_mat = "g", ν = 0.4, c_p = 0),
            Estrato(H_0 = 1.6, γ_s = 18.0, E_s = 7000, c_u = 24.63, φ_s = 26, saturado = False, tipo_mat = "c", c_p = 18, C_s = 0.014,e_0 = 1.91, σ_pp = 112),
            Estrato(H_0 = 1.4, γ_s = 18.4, E_s = 13200, c_u = 0, φ_s = 29, saturado = False, tipo_mat = "g", ν = 0.3, c_p = 0),
            Estrato(H_0 = 1.7, γ_s = 19.0, E_s = 9324, c_u = 0, φ_s = 32, saturado = False, tipo_mat = "g", ν = 0.4, c_p = 0),
            Estrato(H_0 = 1.6, γ_s = 18.0, E_s = 7000, c_u = 24.63, φ_s = 26, saturado = False, tipo_mat = "c", c_p = 18, C_s = 0.014,e_0 = 1.91, σ_pp = 112),
            # Estrato(H_0 = 3.5, γ_s = 24.0, E_s = 130000, c_u = None, φ_s = None, saturado = False, tipo_mat = "r", c_p = 0, ν = 0.3, roca_φ_rm = 40, RQD = 20),
        ], γ_r=γ_r, φ_r=φ_r)
        self.pila_7 = PilaIsa(D_p, h_i, H, HG, h_c, h_con, θ_c, TP, θ, γ_c, E_p, perfil, campana, ω)

        #Pila 8
        D_p, h_i, H, HG = 0.8, 0.5, 3, 0.7
        h_c, h_con, θ_c = 0.8, 0.4, 20           
        TP, θ, γ_c = 0.6, 8 , 24
        E_p = 29400000
        campana = True
        ω = 0
        γ_r, φ_r = 16.4, 35
        perfil = Perfil([
            Estrato(H_0 = 5.0, γ_s = 21.0, E_s = 6597, c_u = 0, φ_s = 24, saturado = False, tipo_mat = "g", ν = 0.3, c_p = 0),
            Estrato(H_0 = 5.0, γ_s = 21.0, E_s = 7000, c_u = 0, φ_s = 27, saturado = False, tipo_mat = "g", ν = 0.35, c_p = 0),
        ], γ_r=γ_r, φ_r=φ_r)
        self.pila_8 = PilaIsa(D_p, h_i, H, HG, h_c, h_con, θ_c, TP, θ, γ_c, E_p, perfil, campana, ω)

    @classmethod
    def tearDownClass(self):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_calcular_φ(self):
        pila = copy.copy(self.pila_4)
        φ = pila._calcular_φ(2.5, 4)

        self.assertAlmostEqual(φ, 27.55, places=2)

    def test_calcular_c_u(self):
        pila = copy.copy(self.pila_3)
        φ = pila._calcular_c_u(2, 3.5)

        self.assertAlmostEqual(φ, 24.63, places=2)

    def test_calcular_excentricidad(self):
        pila = copy.copy(self.pila_5)
        cargas = 1000, 200, 300
        e = pila._calcular_excentricidad(cargas)

        self.assertAlmostEqual(e, 1.32, places=2)

    def test_calcular_longitud_transicion_granular(self):
        pila = copy.copy(self.pila_4)
        cargas = 1000, 200, 300
        P = 2000
        L_t_g = pila._calcular_longitud_transicion_granular(P, cargas)

        self.assertAlmostEqual(L_t_g, 6.67, places=2)

    def test_interpolar_ku(self):
        pila = copy.copy(self.pila_4)
        φ = 25

        ku = pila._interpolar_ku(φ)

        self.assertAlmostEqual(ku, 0.888, places=2 )

    def test_interpolar_m(self):
        pila = copy.copy(self.pila_4)
        φ = 25

        m = pila._interpolar_m(φ)

        self.assertAlmostEqual(m, 0.1, places=2)

    def test_interpolar_N_q(self):
        pila = copy.copy(self.pila_4)
        φ = 25

        N_q = pila._interpolar_N_q(φ)

        self.assertAlmostEqual(N_q, 5, places=2)

    def test_interpolar_B_c(self):
        pila = copy.copy(self.pila_4)
        relacion_H_D = 0.8

        B_c = pila._interpolar_B_c(relacion_H_D)

        self.assertAlmostEqual(B_c, 8.55, places=2)
        
    def test_volumen(self):
        
        pila = self.pila_1
        vol = pila.volumen()
        self.assertAlmostEqual(vol, 1.944,places=3)

    def test_volumen2(self):
        
        pila = copy.copy(self.pila_2)
        vol = pila.volumen()

        self.assertAlmostEqual(vol, 13.73, places=2)

    def test_volumen3(self):
        
        pila = copy.copy(self.pila_3)
        vol = pila.volumen()

        self.assertAlmostEqual(vol, 9.57, places=2)

    def test_volumen_4(self):
        
        pila = self.pila_8
        vol = pila.volumen()
        self.assertAlmostEqual(vol, 2.199,places=3)

    def test_calculo_de_capacidad_portante(self):

        pila = copy.copy(self.pila_1)
        _, Q_p, Q_s, memoria_p, memoria_s = pila.calculo_capacidad_portante()
        print(memoria_p)
        print(memoria_s)
        self.assertAlmostEqual(Q_p, 177.34, places=2)
        self.assertAlmostEqual(Q_s, 53.87, places=2)

    def test_calculo_de_capacidad_portante2(self):

        pila = copy.copy(self.pila_2)
        _, Q_p, Q_s, memoria_p, memoria_s = pila.calculo_capacidad_portante()
        print(memoria_p)
        print(memoria_s)
        self.assertAlmostEqual(Q_p, 696.40, places=2)
        self.assertAlmostEqual(Q_s, 301.46, places=2)

    def test_calculo_de_capacidad_portante3(self):

        pila = copy.copy(self.pila_3)
        _, Q_p, Q_s, memoria_p, memoria_s = pila.calculo_capacidad_portante()
        print(memoria_p)
        print(memoria_s)
        self.assertAlmostEqual(Q_p, 764.22, places=2)
        self.assertAlmostEqual(Q_s, 300.29, places=2)

    def test_calculo_de_capacidad_portante4(self):

        pila = copy.copy(self.pila_6)
        _, Q_p, Q_s, memoria_p, memoria_s = pila.calculo_capacidad_portante()
        print(memoria_p)
        print(memoria_s)
        self.assertAlmostEqual(Q_p, 3727.32, places=2)
        self.assertAlmostEqual(Q_s, 292.15, places=2)

    def test_calculo_de_capacidad_portante5(self):

        pila = copy.copy(self.pila_7)
        _, Q_p, Q_s, memoria_p, memoria_s = pila.calculo_capacidad_portante()
        print(memoria_p)
        print(memoria_s)
        self.assertAlmostEqual(Q_p, 289.38, places=2)
        self.assertAlmostEqual(Q_s, 197.45, places=2)

    def test_calculo_de_capacidad_portante_punta_granular(self):
        pila = copy.copy(self.pila_4)
        Q_p, memoria = pila._calculo_de_capacidad_portante_punta_granular()
        print(memoria)

        self.assertAlmostEqual(Q_p, 1614.78, places = 2)

    def test_calculo_de_capacidad_portante_punta_granular2(self):
        pila = copy.copy(self.pila_6)
        
        Q_p, memoria = pila._calculo_de_capacidad_portante_punta_granular()
        print(memoria)

        self.assertAlmostEqual(Q_p, 3727.32, places = 2)

    def test_calculo_de_capacidad_portante_punta_granular3(self):
        pila = copy.copy(self.pila_4)
        
        pila.H = 1.5
        
        Q_p, memoria = pila._calculo_de_capacidad_portante_punta_granular()
        print(memoria)

        self.assertAlmostEqual(Q_p, 1147.87, places = 2)

    def test_calculo_de_capacidad_portante_punta_granular4(self):
        pila = copy.copy(self.pila_4)
        .2
        .7
        
        Q_p, memoria = pila._calculo_de_capacidad_portante_punta_granular()
        print(memoria)

        self.assertAlmostEqual(Q_p, 1614.78, places = 2)

    def test_calculo_de_capacidad_portante_punta_granular5(self):
        pila = copy.copy(self.pila_4)
        pila.D_p = 1.8
        pila.D_c = 2.3
        
        Q_p, memoria = pila._calculo_de_capacidad_portante_punta_granular()
        print(memoria)

        self.assertAlmostEqual(Q_p, 2902.44, places = 2)

    def test_calculo_de_capacidad_portante_punta_granular6(self):
        pila = copy.copy(self.pila_4)
        pila.D_p = 1
        pila.D_c = 1.5
        
        Q_p, memoria = pila._calculo_de_capacidad_portante_punta_granular()
        print(memoria)

        self.assertAlmostEqual(Q_p, 1212.05, places = 2)

    def test_calculo_de_capacidad_portante_punta_granular7(self):
        pila = copy.copy(self.pila_4)
        pila.D_p = 1
        pila.D_c = 1.5
        
        Q_p, memoria = pila._calculo_de_capacidad_portante_punta_granular()
        print(memoria)

        self.assertAlmostEqual(Q_p, 1212.05, places = 2)

    def test_calculo_de_capacidad_portante_punta_granular8(self):
        pila = copy.copy(self.pila_4)
        pila.D_p = 1
        pila.D_c = 1
        pila.TP = 0.7
        
        Q_p, memoria = pila._calculo_de_capacidad_portante_punta_granular()
        print(memoria)

        self.assertAlmostEqual(Q_p, 676.05, places = 2)

    def test_calculo_de_capacidad_portante_punta_granular9(self):
        pila = copy.copy(self.pila_4)
        pila.D_p = 1
        pila.D_c = 1
        pila.TP = 0.7
        
        Q_p, memoria = pila._calculo_de_capacidad_portante_punta_granular()
        print(memoria)

        self.assertAlmostEqual(Q_p, 676.05, places = 2)

    def test_calculo_de_capacidad_portante_punta_granular_10(self):
        pila = copy.copy(self.pila_4)
        pila.D_p = 1.2
        pila.D_c = 1.2
        pila.TP = 0.7
        
        pila.set_perfil(Perfil([
            Estrato(H_0 = 1.5, γ_s = 22.0, E_s = 9324, c_u = 0, φ_s = 28, saturado = False, tipo_mat = "g",ν = 0.3, c_p = 0),
            Estrato(H_0 = 1.0, γ_s = 21.0, E_s = 15000, c_u = 0, φ_s = 25, saturado = False, tipo_mat = "g", ν = 0.2, c_p = 0),
            Estrato(H_0 = 1.2, γ_s = 19.5, E_s = 9324, c_u = 0, φ_s = 23, saturado = False, tipo_mat = "g", ν = 0.4, c_p = 0),
            Estrato(H_0 = 1.3, γ_s = 19.2, E_s = 13200, c_u = 0, φ_s = 25, saturado = False, tipo_mat = "g", ν = 0.3, c_p = 0),
            Estrato(H_0 = 3.5, γ_s = 24.0, E_s = 130000, c_u = None, φ_s = None, saturado = False, tipo_mat = "r", c_p = 0, ν = 0.3, roca_φ_rm = 40, RQD = 20),
        ]))

        Q_p, memoria = pila._calculo_de_capacidad_portante_punta_granular()
        print(memoria)

        self.assertAlmostEqual(Q_p, 349.36, places = 2)

    def test_calculo_de_capacidad_portante_punta_granular_11(self):
        pila = copy.copy(self.pila_4)
        pila.D_p = 1.2
        pila.D_c = 1.5
        pila.TP = 0.7
        
        pila.set_perfil(Perfil([
            Estrato(H_0 = 1.5, γ_s = 22.0, E_s = 9324, c_u = 0, φ_s = 28, saturado = False, tipo_mat = "g",ν = 0.3, c_p = 0),
            Estrato(H_0 = 1.0, γ_s = 21.0, E_s = 15000, c_u = 0, φ_s = 25, saturado = False, tipo_mat = "g", ν = 0.2, c_p = 0),
            Estrato(H_0 = 1.2, γ_s = 19.5, E_s = 9324, c_u = 0, φ_s = 23, saturado = False, tipo_mat = "g", ν = 0.4, c_p = 0),
            Estrato(H_0 = 1.3, γ_s = 19.2, E_s = 13200, c_u = 0, φ_s = 25, saturado = False, tipo_mat = "g", ν = 0.3, c_p = 0),
            Estrato(H_0 = 3.5, γ_s = 24.0, E_s = 130000, c_u = None, φ_s = None, saturado = False, tipo_mat = "r", c_p = 0, ν = 0.3, roca_φ_rm = 40, RQD = 20),
        ]))

        Q_p, memoria = pila._calculo_de_capacidad_portante_punta_granular()
        print(memoria)

        self.assertAlmostEqual(Q_p, 547.51, places = 2)

    def test__calculo_de_capacidad_portante_punta_cohesivo(self):
        pila = copy.copy(self.pila_5)
                
        Q_p, memoria = pila._calculo_de_capacidad_portante_punta_cohesivo()
        print(memoria)

        self.assertAlmostEqual(Q_p, 1034.65, places = 2)

    def test__calculo_de_capacidad_portante_punta_cohesivo2(self):
        pila = copy.copy(self.pila_5)
        pila.D_p = 1.5
        pila.D_c = 2
        Q_p, memoria = pila._calculo_de_capacidad_portante_punta_cohesivo()
        print(memoria)

        self.assertAlmostEqual(Q_p, 643.02, places = 2)

    def test__calculo_de_capacidad_portante_punta_cohesivo3(self):
        pila = copy.copy(self.pila_3)
        
        Q_p, memoria = pila._calculo_de_capacidad_portante_punta_cohesivo()
        print(memoria)

        self.assertAlmostEqual(Q_p, 764.22, places = 2)

    def test__calculo_de_capacidad_portante_punta_cohesivo4(self):
        pila = copy.copy(self.pila_3)
        
        pila.D_p = 1
        pila.D_c = 1.4
        Q_p, memoria = pila._calculo_de_capacidad_portante_punta_cohesivo()
        print(memoria)

        self.assertAlmostEqual(Q_p, 362.02, places = 2)

    def test__calculo_de_capacidad_portante_punta_cohesivo5(self):
        pila = copy.copy(self.pila_5)
        
        pila.D_p = 1.3
        pila.D_c = 1.7
        Q_p, memoria = pila._calculo_de_capacidad_portante_punta_cohesivo()
        print(memoria)

        self.assertAlmostEqual(Q_p, 452.37, places = 2)

    def test__calculo_de_capacidad_portante_punta_cohesivo6(self):
        pila = copy.copy(self.pila_5)

        pila.D_p = 1.5
        pila.D_c = 1.8
        
        Q_p, memoria = pila._calculo_de_capacidad_portante_punta_cohesivo()
        print(memoria)

        self.assertAlmostEqual(Q_p, 512.22, places = 2)

    def test__calculo_de_capacidad_portante_punta_cohesivo7(self):
        pila = copy.copy(self.pila_5)

        pila.D_p = 1.7
        pila.D_c = 2.0
        
        Q_p, memoria = pila._calculo_de_capacidad_portante_punta_cohesivo()
        print(memoria)

        self.assertAlmostEqual(Q_p, 643.02, places = 2)

    def test__calculo_de_capacidad_portante_punta_cohesivo8(self):
        pila = copy.copy(self.pila_5)

        pila.D_p = 0.8
        pila.D_c = 1.0
        
        Q_p, memoria = pila._calculo_de_capacidad_portante_punta_cohesivo()
        print(memoria)

        self.assertAlmostEqual(Q_p, 141.25, places = 2)

    def test__calculo_de_capacidad_portante_punta_cohesivo9(self):
        pila = copy.copy(self.pila_3)
        
        pila.D_p = 1.3
        pila.D_c = 1.6
        Q_p, memoria = pila._calculo_de_capacidad_portante_punta_cohesivo()
        print(memoria)

        self.assertAlmostEqual(Q_p, 472.84, places = 2)

    def test__calculo_de_capacidad_portante_punta_cohesivo_10(self):
        pila = copy.copy(self.pila_3)
        
        pila.D_p = 1.5
        pila.D_c = 1.8
        Q_p, memoria = pila._calculo_de_capacidad_portante_punta_cohesivo()
        print(memoria)

        self.assertAlmostEqual(Q_p, 594.98, places = 2)

    def test_calculo_de_capacidad_portante_fuste(self):
        pila = copy.copy(self.pila_3)
        Q_s, memoria = pila._calculo_de_capacidad_portante_fuste()
        print(memoria)

        self.assertAlmostEqual(Q_s, 300.29, places = 2)

    def test_calculo_de_capacidad_portante_fuste2(self):
        pila = copy.copy(self.pila_3)
        pila.D_p = 2.6
        Q_s, memoria = pila._calculo_de_capacidad_portante_fuste()
        print(memoria)

        self.assertAlmostEqual(Q_s, 459.27, places = 2)

    def test_calculo_de_capacidad_portante_fuste3(self):
        pila = copy.copy(self.pila_3)
        pila.D_p = 2.6
        pila.H = 2
        Q_s, memoria = pila._calculo_de_capacidad_portante_fuste()
        print(memoria)

        self.assertAlmostEqual(Q_s, 156.27, places = 2)

    def test_calculo_de_capacidad_portante_fuste4(self):
        pila = copy.copy(self.pila_3)
        pila.D_p = 2.6
        pila.H = 3
        Q_s, memoria = pila._calculo_de_capacidad_portante_fuste()
        print(memoria)

        self.assertAlmostEqual(Q_s, 357.46, places = 2)

    def test_calculo_de_capacidad_portante_fuste5(self):
        pila = copy.copy(self.pila_3)
        pila.D_p = 2.6        
        pila.H = 1.5
        Q_s, memoria = pila._calculo_de_capacidad_portante_fuste()
        print(memoria)

        self.assertAlmostEqual(Q_s, 76.86, places = 2)

    def test_calculo_de_capacidad_portante_fuste6(self):
        pila = copy.copy(self.pila_1)
        
        Q_s, memoria = pila._calculo_de_capacidad_portante_fuste()
        print(memoria)

        self.assertAlmostEqual(Q_s, 53.87, places = 2)

    def test_calculo_de_capacidad_portante_fuste7(self):
        pila = copy.copy(self.pila_2)
        
        Q_s, memoria = pila._calculo_de_capacidad_portante_fuste()
        print(memoria)

        self.assertAlmostEqual(Q_s, 301.46, places = 2)

    def test_calculo_de_capacidad_portante_fuste8(self):
        pila = copy.copy(self.pila_4)
        
        Q_s, memoria = pila._calculo_de_capacidad_portante_fuste()
        print(memoria)

        self.assertAlmostEqual(Q_s, 93.64, places = 2)

    def test_calculo_de_capacidad_portante_fuste9(self):
        pila = copy.copy(self.pila_5)
        
        Q_s, memoria = pila._calculo_de_capacidad_portante_fuste()
        print(memoria)

        self.assertAlmostEqual(Q_s, 596.82, places = 2)

    def test_calculo_de_capacidad_portante_fuste_10(self):
        pila = copy.copy(self.pila_5)
        pila.D_p = 2.6

        Q_s, memoria = pila._calculo_de_capacidad_portante_fuste()
        print(memoria)

        self.assertAlmostEqual(Q_s, 620.70, places = 2)

    def test_calculo_tension(self):

        pila = copy.copy(self.pila_3)
        T_u, memoria = pila.calculo_tension()
        print(memoria)
        
        self.assertAlmostEqual(T_u, 297.44, places=2)

    def test_calculo_tension2(self):

        pila = copy.copy(self.pila_2)
        T_u, memoria = pila.calculo_tension()
        print(memoria)
        
        self.assertAlmostEqual(T_u, 535.64, places=2)

    def test_calculo_tension3(self):

        pila = copy.copy(self.pila_4)
        T_u, memoria = pila.calculo_tension()
        print(memoria)
        
        self.assertAlmostEqual(T_u, 228.19, places=2)

    def test_calculo_tension4(self):

        pila = copy.copy(self.pila_5)
        T_u, memoria = pila.calculo_tension()
        print(memoria)
        
        self.assertAlmostEqual(T_u, 356.13, places=2)

    def test_calculo_tension5(self):

        pila = copy.copy(self.pila_1)
        T_u, memoria = pila.calculo_tension()
        print(memoria)
        
        self.assertAlmostEqual(T_u, 82.57, places=2)

    def test_calculo_tension_tronco_piramidal_granular(self):

        pila = copy.copy(self.pila_3)
        T_tp, memoria = pila._calculo_tension_tronco_piramidal_granular()
        print(memoria)
        
        self.assertAlmostEqual(T_tp, 983.58, places=2)

    def test_calculo_tension_tronco_piramidal_granular2(self):

        pila = copy.copy(self.pila_3)
        pila.D_p = 2
        pila.D_c = 2.5
        T_tp, memoria = pila._calculo_tension_tronco_piramidal_granular()
        print(memoria)
        
        self.assertAlmostEqual(T_tp, 1269.08, places=2)

    def test_calculo_tension_tronco_piramidal_granular3(self):

        pila = copy.copy(self.pila_3)
        pila.D_p = 3
        pila.D_c = 3.5
        T_tp, memoria = pila._calculo_tension_tronco_piramidal_granular()
        print(memoria)
        
        self.assertAlmostEqual(T_tp, 2140.08, places=2)

    def test_calculo_tension_tronco_piramidal_granular4(self):

        pila = copy.copy(self.pila_4)
        pila.D_p = 3
               
        pila.set_perfil(Perfil([
            Estrato(H_0 = 1.5, γ_s = 22.0, E_s = 9324, c_u = 0, φ_s = 35, saturado = False, tipo_mat = "g",ν = 0.3, c_p = 0),
            Estrato(H_0 = 1.0, γ_s = 21.0, E_s = 15000, c_u = 0, φ_s = 41, saturado = False, tipo_mat = "g", ν = 0.2, c_p = 0),
            Estrato(H_0 = 1.5, γ_s = 20.5, E_s = 9324, c_u = 0, φ_s = 31, saturado = False, tipo_mat = "g", ν = 0.4, c_p = 0),
            Estrato(H_0 = 1.3, γ_s = 19.2, E_s = 13200, c_u = 0, φ_s = 28, saturado = False, tipo_mat = "g", ν = 0.3, c_p = 0),
            Estrato(H_0 = 3.5, γ_s = 24.0, E_s = 130000, c_u = None, φ_s = None, saturado = False, tipo_mat = "r", c_p = 0, ν = 0.3, roca_φ_rm = 40, RQD = 20),
        ]))
        
        T_tp, memoria = pila._calculo_tension_tronco_piramidal_granular()
        print(memoria)
        
        self.assertAlmostEqual(T_tp, 936.56, places=2)

    def test_calculo_tension_tronco_piramidal_granular5(self):

        pila = copy.copy(self.pila_3)
        
        T_tp, memoria = pila._calculo_tension_tronco_piramidal_granular()
        print(memoria)
        
        self.assertAlmostEqual(T_tp, 983.58, places=2)

    def test_calculo_tension_tronco_piramidal_granular6(self):

        pila = copy.copy(self.pila_7)
        
        T_tp, memoria = pila._calculo_tension_tronco_piramidal_granular()
        print(memoria)
        
        self.assertAlmostEqual(T_tp, 850.92, places=2)

    def test_calculo_tension_tronco_piramidal_granular7(self):

        pila = copy.copy(self.pila_7)
        pila.D_p = 2.5
        
        T_tp, memoria = pila._calculo_tension_tronco_piramidal_granular()
        print(memoria)
        
        self.assertAlmostEqual(T_tp, 1010.16, places=2)

    def test_calculo_tension_tronco_piramidal_granular8(self):

        pila = copy.copy(self.pila_7)
        pila.D_p = 2.5
        pila.H = 2.4
        
        T_tp, memoria = pila._calculo_tension_tronco_piramidal_granular()
        print(memoria)
        
        self.assertAlmostEqual(T_tp, 673.97, places=2)

    def test_calculo_tension_tronco_piramidal_granular9(self):

        pila = copy.copy(self.pila_7)
        pila.D_p = 2.7
        pila.H = 2.6
        
        
        T_tp, memoria = pila._calculo_tension_tronco_piramidal_granular()
        print(memoria)
        
        self.assertAlmostEqual(T_tp, 802.98, places=2)

    def test_calculo_tension_tronco_piramidal_granular_10(self):

        pila = copy.copy(self.pila_7)
        pila.D_p = 2.9
        pila.H = 2.8
        
        
        T_tp, memoria = pila._calculo_tension_tronco_piramidal_granular()
        print(memoria)
        
        self.assertAlmostEqual(T_tp, 948.54, places=2)

    def test_calculo_tension_tronco_piramidal_cohesivo(self):

        pila = copy.copy(self.pila_2)
        
        T_tp, memoria = pila._calculo_tension_tronco_piramidal_cohesivo()
        print(memoria)
        
        self.assertAlmostEqual(T_tp, 267.42, places=2)

    def test_calculo_tension_tronco_piramidal_cohesivo2(self):

        pila = copy.copy(self.pila_2)
        pila.D_p = 3.2
        pila.D_c = 3.6
        
        T_tp, memoria = pila._calculo_tension_tronco_piramidal_cohesivo()
        print(memoria)
        
        self.assertAlmostEqual(T_tp, 856.28, places=2)

    def test_calculo_tension_tronco_piramidal_cohesivo3(self):

        pila = copy.copy(self.pila_2)
        pila.D_p = 1.5
        pila.D_c = 1.9
        
        T_tp, memoria = pila._calculo_tension_tronco_piramidal_cohesivo()
        print(memoria)
        
        self.assertAlmostEqual(T_tp, 241.80, places=2)

    def test_calculo_tension_tronco_piramidal_cohesivo4(self):

        pila = copy.copy(self.pila_3)
        
        T_tp, memoria = pila._calculo_tension_tronco_piramidal_cohesivo()
        print(memoria)
        
        self.assertAlmostEqual(T_tp, 297.44, places=2)

    def test_calculo_tension_tronco_piramidal_cohesivo5(self):

        pila = copy.copy(self.pila_3)
        pila.D_p = 3
        pila.D_c = 3.4
        
        T_tp, memoria = pila._calculo_tension_tronco_piramidal_cohesivo()
        print(memoria)
        
        self.assertAlmostEqual(T_tp, 679.70, places=2)

    def test_calculo_tension_tronco_piramidal_cohesivo6(self):

        pila = copy.copy(self.pila_3)
        pila.H = 2.5
                
        T_tp, memoria = pila._calculo_tension_tronco_piramidal_cohesivo()
        print(memoria)
        
        self.assertAlmostEqual(T_tp, 205.24, places=2)

    def test_calculo_tension_tronco_piramidal_cohesivo7(self):

        pila = copy.copy(self.pila_5)
        
        T_tp, memoria = pila._calculo_tension_tronco_piramidal_cohesivo()
        print(memoria)
        
        self.assertAlmostEqual(T_tp, 356.13, places=2)

    def test_calculo_tension_tronco_piramidal_cohesivo8(self):

        pila = copy.copy(self.pila_5)
        pila.D_p = 3
        pila.D_c = 3.4
        
        T_tp, memoria = pila._calculo_tension_tronco_piramidal_cohesivo()
        print(memoria)
        
        self.assertAlmostEqual(T_tp, 565.15, places=2)

    def test_calculo_tension_tronco_piramidal_cohesivo9(self):

        pila = copy.copy(self.pila_5)
        pila.D_p = 3
        pila.D_c = 3.4
        pila.H = 1.2
        
        T_tp, memoria = pila._calculo_tension_tronco_piramidal_cohesivo()
        print(memoria)
        
        self.assertAlmostEqual(T_tp, 221.57, places=2)

    def test_calculo_tension_tronco_piramidal_cohesivo_10(self):

        pila = copy.copy(self.pila_5)
        pila.H = 2.5
        
        T_tp, memoria = pila._calculo_tension_tronco_piramidal_cohesivo()
        print(memoria)
        
        self.assertAlmostEqual(T_tp, 299.88, places=2)

    def test_calculo_tension_tronco_piramidal_cohesivo_11(self):

        pila = copy.copy(self.pila_5)
        pila.D_p = 3
        pila.D_c = 3.4
        pila.H = 2
        .5
        
        
        T_tp, memoria = pila._calculo_tension_tronco_piramidal_cohesivo()
        print(memoria)
        
        self.assertAlmostEqual(T_tp, 371.53, places=2)

    def test_calculo_tension_tronco_piramidal_cohesivo_12(self):

        pila = copy.copy(self.pila_6)
        
        T_tp, memoria = pila._calculo_tension_tronco_piramidal_cohesivo()
        print(memoria)
        
        self.assertAlmostEqual(T_tp, 305.85, places=2)

    def test_calculo_tension_tronco_piramidal_cohesivo_13(self):

        pila = copy.copy(self.pila_6)
        pila.D_p = 2.2
        pila.D_c = 2.6
        pila.H = 1.8
        
        
        
        T_tp, memoria = pila._calculo_tension_tronco_piramidal_cohesivo()
        print(memoria)
        
        self.assertAlmostEqual(T_tp, 221.47, places=2)

    def test_calculo_tension_tronco_piramidal_cohesivo_14(self):

        pila = copy.copy(self.pila_6)
        pila.D_p = 1.8
        pila.D_c = 2.2
        pila.H = 2
        
        .5
        
        T_tp, memoria = pila._calculo_tension_tronco_piramidal_cohesivo()
        print(memoria)
        
        self.assertAlmostEqual(T_tp, 205.60, places=2)

    def test_calculo_tension_tronco_piramidal_cohesivo_15(self):

        pila = copy.copy(self.pila_7)
        
        T_tp, memoria = pila._calculo_tension_tronco_piramidal_cohesivo()
        print(memoria)
        
        self.assertAlmostEqual(T_tp, 191.86, places=2)

    def test_calculo_carga_lateral(self):
        
        cargas = 1000, 200, 100  
         
        pila = copy.copy(self.pila_3)
        P, p_corta, memoria = pila.calculo_carga_lateral(cargas)
        print(memoria)
        print(p_corta)
        self.assertAlmostEqual(P, 1701.35, places=2)

    def test_calculo_carga_lateral2(self):
        
        cargas = 900, 120, 150

        pila = copy.copy(self.pila_3)
        P, p_corta, memoria = pila.calculo_carga_lateral(cargas)
        print(memoria)
        print(p_corta)
        self.assertAlmostEqual(P, 1849.40, places=2)

    def test_calculo_carga_lateral3(self):
        
        cargas = 800, 500, 450 

        pila = copy.copy(self.pila_3)
        P, p_corta, memoria = pila.calculo_carga_lateral(cargas)
        print(memoria)
        print(p_corta)
        self.assertAlmostEqual(P, 1423.77, places=2)

    def test_calculo_carga_lateral4(self):
        
        cargas = 700, 200, 300

        pila = copy.copy(self.pila_3)
        P, p_corta, memoria = pila.calculo_carga_lateral(cargas)
        print(memoria)
        print(p_corta)
        self.assertAlmostEqual(P, 1502.43, places=2)

    def test_calculo_carga_lateral5(self):
        
        cargas = 1000, 200, 100

        pila = copy.copy(self.pila_2)
        P, p_corta, memoria = pila.calculo_carga_lateral(cargas)
        print(memoria)
        print(p_corta)
        self.assertAlmostEqual(P, 3792.01, places=2)

    def test_calculo_carga_lateral6(self):
        
        cargas = 900, 120, 150

        pila = copy.copy(self.pila_2)
        P, p_corta, memoria = pila.calculo_carga_lateral(cargas)
        print(memoria)
        print(p_corta)
        self.assertAlmostEqual(P, 4210.23, places=2)

    def test_calculo_carga_lateral7(self):
        
        cargas = 800, 500, 450

        pila = copy.copy(self.pila_2)
        P, p_corta, memoria = pila.calculo_carga_lateral(cargas)
        print(memoria)
        print(p_corta)
        self.assertAlmostEqual(P, 3056.70, places=2)

    def test_calculo_carga_lateral8(self):
        
        cargas = 700, 200, 300

        pila = copy.copy(self.pila_2)
        P, p_corta, memoria = pila.calculo_carga_lateral(cargas)
        print(memoria)
        print(p_corta)
        self.assertAlmostEqual(P, 3258.96, places=2)

    def test_calculo_carga_lateral9(self):
        
        cargas = 1000, 200, 100

        pila = copy.copy(self.pila_4)
        P, p_corta, memoria = pila.calculo_carga_lateral(cargas)
        print(memoria)
        print(p_corta)
        self.assertAlmostEqual(P, 3345.43, places=2)

    def test_calculo_carga_lateral_10(self):
        
        cargas = 900, 120, 150

        pila = copy.copy(self.pila_4)
        P, p_corta, memoria = pila.calculo_carga_lateral(cargas)
        print(memoria)
        print(p_corta)
        self.assertAlmostEqual(P, 3541.37, places=2)

    def test_calculo_carga_lateral_11(self):
        
        cargas = 800, 500, 450

        pila = copy.copy(self.pila_4)
        P, p_corta, memoria = pila.calculo_carga_lateral(cargas)
        print(memoria)
        print(p_corta)
        self.assertAlmostEqual(P, 2958.68, places=2)

    def test_calculo_carga_lateral_12(self):
        
        cargas = 700, 200, 300

        pila = copy.copy(self.pila_4)
        P, p_corta, memoria = pila.calculo_carga_lateral(cargas)
        print(memoria)
        print(p_corta)
        self.assertAlmostEqual(P, 3071.33, places=2)

    def test_calculo_carga_lateral_13(self):
        
        cargas = 1000, 200, 100

        pila = copy.copy(self.pila_5)
        P, p_corta, memoria = pila.calculo_carga_lateral(cargas)
        print(memoria)
        print(p_corta)
        self.assertAlmostEqual(P, 4005.04, places=2)

    def test_calculo_carga_lateral_14(self):
        
        cargas = 900, 120, 150

        pila = copy.copy(self.pila_5)
        P, p_corta, memoria = pila.calculo_carga_lateral(cargas)
        print(memoria)
        print(p_corta)
        self.assertAlmostEqual(P, 4193.22, places=2)

    def test_calculo_carga_lateral_15(self):
        
        cargas = 800, 500, 450

        pila = copy.copy(self.pila_5)
        P, p_corta, memoria = pila.calculo_carga_lateral(cargas)
        print(memoria)
        print(p_corta)
        self.assertAlmostEqual(P, 3619.75, places=2)

    def test_calculo_carga_lateral_16(self):
        
        cargas = 700, 200, 300

        pila = copy.copy(self.pila_5)
        P, p_corta, memoria = pila.calculo_carga_lateral(cargas)
        print(memoria)
        print(p_corta)
        self.assertAlmostEqual(P, 3733.92, places=2)

    def test_calculo_carga_lateral_17(self):
        
        cargas = 1000, 200, 100

        pila = copy.copy(self.pila_6)
        P, p_corta, memoria = pila.calculo_carga_lateral(cargas)
        print(memoria)
        print(p_corta)
        self.assertAlmostEqual(P, 3171.23, places=2)

    def test_calculo_carga_lateral_18(self):
        
        cargas = 900, 120, 150

        pila = copy.copy(self.pila_6)
        P, p_corta, memoria = pila.calculo_carga_lateral(cargas)
        print(memoria)
        print(p_corta)
        self.assertAlmostEqual(P, 3315.36, places=2)

    def test_calculo_carga_lateral_19(self):
        
        cargas = 800, 500, 450

        pila = copy.copy(self.pila_6)
        P, p_corta, memoria = pila.calculo_carga_lateral(cargas)
        print(memoria)
        print(p_corta)
        self.assertAlmostEqual(P, 2875.34, places=2)

    def test_calculo_carga_lateral_20(self):
        
        cargas = 700, 200, 300

        pila = copy.copy(self.pila_6)
        P, p_corta, memoria = pila.calculo_carga_lateral(cargas)
        print(memoria)
        print(p_corta)
        self.assertAlmostEqual(P, 2963.14, places=2)

    def test_calculo_modulos_de_reaccion_horizontal(self):
        
        pila = copy.copy(self.pila_3)

        k = pila.calculo_modulos_de_reaccion_horizontal()
        
        self.assertTrue(k)

    def test_calculo_volcamiento(self):
            
        F_zc = 1050
        F = 350

        pila = copy.copy(self.pila_1)
        Mv, Me, memoria = pila.calculo_volcamiento(F_zc, F)
        print(memoria)
        self.assertAlmostEqual(Mv, 1712.92, places=2)
        self.assertAlmostEqual(Me, 477.40, places=2)

    def test_calculo_volcamiento2(self):
        
        F_zc = 1050
        F = 350

        pila = copy.copy(self.pila_2)
        Mv, Me, memoria = pila.calculo_volcamiento(F_zc, F)
        print(memoria)
        self.assertAlmostEqual(Mv, 3097.78, places=2)
        self.assertAlmostEqual(Me, 13135.81, places=2)

    def test_calculo_volcamiento3(self):
        
        F_zc = 1050
        F = 350

        pila = copy.copy(self.pila_3)
        Mv, Me, memoria = pila.calculo_volcamiento(F_zc, F)
        print(memoria)
        self.assertAlmostEqual(Mv, 2826.01, places=2)
        self.assertAlmostEqual(Me, 8526.00, places=2)

    def test_calculo_volcamiento4(self):
        
        F_zc = 2000
        F = 530

        pila = copy.copy(self.pila_4)
        Mv, Me, memoria = pila.calculo_volcamiento(F_zc, F)
        print(memoria)
        self.assertAlmostEqual(Mv, 3498.38, places=2)
        self.assertAlmostEqual(Me, 2482.97, places=2)

    def test_calculo_volcamiento5(self):
        
        F_zc = 2000
        F = 630

        pila = copy.copy(self.pila_5)
        Mv, Me, memoria = pila.calculo_volcamiento(F_zc, F)
        print(memoria)
        self.assertAlmostEqual(Mv, 5366.97, places=2)
        self.assertAlmostEqual(Me, 18224.62, places=2)

    def test_calculo_volcamiento6(self):
        
        F_zc = 2000
        F = 630

        pila = copy.copy(self.pila_6)
        Mv, Me, memoria = pila.calculo_volcamiento(F_zc, F)
        print(memoria)
        self.assertAlmostEqual(Mv, 4577.51, places=2)
        self.assertAlmostEqual(Me, 6743.80, places=2)

    def test_calculo_volcamiento7(self):
        
        F_zc = 2000
        F = 630

        pila = copy.copy(self.pila_7)
        Mv, Me, memoria = pila.calculo_volcamiento(F_zc, F)
        print(memoria)
        self.assertAlmostEqual(Mv, 4962.75, places=2)
        self.assertAlmostEqual(Me, 6938.68, places=2)

    def test_calculo_volcamiento8(self):
        
        F_zc = 2000
        F = 630

        pila = copy.copy(self.pila_8)
        Mv, Me, memoria = pila.calculo_volcamiento(F_zc, F)
        print(memoria)
        self.assertAlmostEqual(Mv, 3108.70, places=2)
        self.assertAlmostEqual(Me, 424.89, places=2)

    def test_calculo_volcamiento9(self):
        
        F_zc = 2200
        F = 750

        pila = copy.copy(self.pila_8)
        Mv, Me, memoria = pila.calculo_volcamiento(F_zc, F)
        print(memoria)
        self.assertAlmostEqual(Mv, 3658.97, places=2)
        self.assertAlmostEqual(Me, 424.89, places=2)

    def test_calculo_volcamiento_10(self):
        
        F_zc = 1500
        F = 800

        pila = copy.copy(self.pila_8)
        Mv, Me, memoria = pila.calculo_volcamiento(F_zc, F)
        print(memoria)
        self.assertAlmostEqual(Mv, 3707.03, places=2)
        self.assertAlmostEqual(Me, 424.89, places=2)

    def test_calculo_asentamiento(self):
        pila = copy.copy(self.pila_1)
        
        F_zc = 900 * 0.3

        S_e, S_c , memoria_e, memoria_c = pila.calculo_asentamiento(F_zc)
        print(memoria_e)
        print(memoria_c)
        self.assertAlmostEqual(S_e, 0.015, places=2)
        self.assertAlmostEqual(S_c, 0.0, places=1)

    def test_calculo_asentamiento2(self):
        pila = copy.copy(self.pila_2)
        
        F_zc = 900 *0.3
        
        S_e, S_c , memoria_e, memoria_c = pila.calculo_asentamiento(F_zc)
        print(memoria_e)
        print(memoria_c)
        self.assertAlmostEqual(S_e, 0.03, places=2)
        self.assertAlmostEqual(S_c, 0.0, places=1)

    def test_calculo_asentamiento3(self):
        pila = copy.copy(self.pila_3)
        
        F_zc = 900 * 0.3
        
        S_e, S_c , memoria_e, memoria_c = pila.calculo_asentamiento(F_zc)
        print(memoria_e)
        print(memoria_c)
        self.assertAlmostEqual(S_e, 0.02, places=2)
        self.assertAlmostEqual(S_c, 0.0, places=1)

    def test_calculo_asentamiento4(self):
        pila = copy.copy(self.pila_4)
        
        F_zc = 900 * 0.3
    
        S_e, S_c , memoria_e, memoria_c = pila.calculo_asentamiento(F_zc)
        print(memoria_e)
        print(memoria_c)
        self.assertAlmostEqual(S_e, 0.035, places=2)
        self.assertAlmostEqual(S_c, 0.0, places=1)

    def test_calculo_asentamiento5(self):
        pila = copy.copy(self.pila_5)
    
        F_zc = 900 * 0.2

        S_e, S_c , memoria_e, memoria_c = pila.calculo_asentamiento(F_zc)
        print(memoria_e)
        print(memoria_c)
        self.assertAlmostEqual(S_e, 0.03, places=2)
        self.assertAlmostEqual(S_c, 0.0, places=1)

    def test_calculo_asentamiento6(self):
        pila = copy.copy(self.pila_6)
        F_zc = 200

        S_e, S_c , memoria_e, memoria_c = pila.calculo_asentamiento(F_zc)
        print(memoria_e)
        print(memoria_c)
        self.assertAlmostEqual(S_e, 0.0581, places=3)
        self.assertAlmostEqual(S_c, 0.0, places=1)

    def test_calculo_asentamiento7(self):
        pila = copy.copy(self.pila_7)
        
        F_zc = 900 * 0.15

        S_e, S_c , memoria_e, memoria_c = pila.calculo_asentamiento(F_zc)
        print(memoria_e)
        print(memoria_c)
        self.assertAlmostEqual(S_e, 0.019, places=3)
        self.assertAlmostEqual(S_c, 0.0, places=1)

    def test_calculo_asentamiento8(self):
        pila = copy.copy(self.pila_8)
        
        F_zc = 900 * 0.15

        S_e, S_c , memoria_e, memoria_c = pila.calculo_asentamiento(F_zc)
        print(memoria_e)
        print(memoria_c)
        self.assertAlmostEqual(S_e, 0.021, places=3)
        self.assertAlmostEqual(S_c, 0.0, places=1)

    def test_calculo_asentamiento9(self):
        pila = copy.copy(self.pila_6)
        
        F_zc = 1500 * 0.15

        S_e, S_c , memoria_e, memoria_c = pila.calculo_asentamiento(F_zc)
        print(memoria_e)
        print(memoria_c)
        self.assertAlmostEqual(S_e, 0.058, places=3)
        self.assertAlmostEqual(S_c, 0.0, places=1)

    def test_calculo_asentamiento_10(self):
        pila = copy.copy(self.pila_2)
        
        F_zc = 1500 * 0.15

        S_e, S_c , memoria_e, memoria_c = pila.calculo_asentamiento(F_zc)
        print(memoria_e)
        print(memoria_c)
        self.assertAlmostEqual(S_e, 0.032, places=3)
        self.assertAlmostEqual(S_c, 0.0, places=1)

    def test_calculo_tension_tronco_piramidal_isa(self):

        pila = copy.copy(self.pila_3)
        T_tp, memoria = pila._calculo_tension_tronco_piramidal_isa()
        print(memoria)
        
        self.assertAlmostEqual(T_tp, 1098.09, places=2)

    def test_calculo_tension_tronco_piramidal_isa_2(self):

        pila = copy.copy(self.pila_3)
        pila.D_p = 2
        pila.D_c = 2.5
        T_tp, memoria = pila._calculo_tension_tronco_piramidal_isa()
        print(memoria)
        
        self.assertAlmostEqual(T_tp, 1468.56, places=2)

    def test_calculo_tension_tronco_piramidal_isa_3(self):

        pila = copy.copy(self.pila_3)
        pila.D_p = 3
        pila.D_c = 3.5
        T_tp, memoria = pila._calculo_tension_tronco_piramidal_isa()
        print(memoria)
        
        self.assertAlmostEqual(T_tp, 2607.01, places=2)

if __name__ == '__main__':
    unittest.main()