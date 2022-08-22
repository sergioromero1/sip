# pylint: disable=W
import unittest
import time
import copy
from ..zapata import Zapata
from ..perfil import Perfil, Estrato

class TestCalculosZapata(unittest.TestCase): 
    
    @classmethod
    def setUpClass(self):
        # Zapata 1
        B, L, D, H, C = 5, 5, 1.5, 0.4, 2
        TP, θ, γ_c = 0.6, 0, 23.54
        γ_r, φ_r = 16.4, 23
        α, ω = 0, 30
        perfil = Perfil([
            Estrato(H_0 = 1.0, γ_s = 20.0, E_s = 6597, c_u = 0, φ_s = 24, saturado = False, tipo_mat = "g", c_p = 0),
            Estrato(H_0 = 0.5, γ_s = 19.0, E_s = 6597, c_u = 0, φ_s = 24, saturado = True, tipo_mat = "g", c_p = 0),
            Estrato(H_0 = 1.0, γ_s = 21.0, E_s = 6597, c_u = 0, φ_s = 24, saturado = True, tipo_mat = "g", c_p = 0),
            Estrato(H_0 = 2.0, γ_s = 19.0, E_s = 6597, c_u = 0, φ_s = 24, saturado = True, tipo_mat = "g", c_p = 0)
        ], γ_r=γ_r, φ_r=φ_r)
        self.zapata_1 = Zapata(B, L, D, H, C, TP, θ, γ_c, perfil, α, ω)

        # Zapata 2
        B, L, D, H, C = 3, 3, 1.8, 0.4, 2
        TP, θ, γ_c = 0.6, 0, 23.54
        γ_r, φ_r = 16.4, 35
        α, ω = 0, 30
        perfil = Perfil([
            Estrato(H_0 = 1.0, γ_s = 20.0, E_s = 6807, c_u = 31.26, φ_s = 35, saturado = False, tipo_mat = "g", c_p = 0),
            Estrato(H_0 = 0.5, γ_s = 19.0, E_s = 6597, c_u = 29.36, φ_s = 27, saturado = True, tipo_mat = "g", c_p = 0),
            Estrato(H_0 = 1.0, γ_s = 21.0, E_s = 6687, c_u = 27.53, φ_s = 23, saturado = True, tipo_mat = "g", c_p = 0),
            Estrato(H_0 = 2.0, γ_s = 19.0, E_s = 6200, c_u = 25.56, φ_s = 21, saturado = True, tipo_mat = "g", c_p = 0),
        ], γ_r=γ_r, φ_r=φ_r)
        self.zapata_2 = Zapata(B, L, D, H, C, TP, θ, γ_c, perfil, α, ω)

        # Zapata 3
        B, L, D, H, C = 5, 5, 1.5, 0.4, 2
        TP, θ, γ_c = 0.6, 0, 23.54
        γ_r, φ_r = 16.4, 35
        α, ω = 0, 30
        perfil = Perfil([
            Estrato(H_0 = 1.0, γ_s = 15.0, E_s = 5000, c_u = 24.63, φ_s = 20, saturado = False, tipo_mat = "c", c_p = 0, C_s = 1,e_0 = 1.91, σ_pp = 90),
            Estrato(H_0 = 1.0, γ_s = 15.0, E_s = 5000, c_u = 24.63, φ_s = 20, saturado = False, tipo_mat = "c", c_p = 0, C_s = 1,e_0 = 1.91, σ_pp = 90),
            Estrato(H_0 = 1.5, γ_s = 15.0, E_s = 5000, c_u = 24.63, φ_s = 20, saturado = False, tipo_mat = "c", c_p = 0, C_s = 1,e_0 = 1.91, σ_pp = 90),
        ], γ_r=γ_r, φ_r=φ_r)
        self.zapata_3 = Zapata(B, L, D, H, C, TP, θ, γ_c, perfil, α, ω)
        
        # Zapata 4

        # Zapata 4       
        B, L, D, H, C = 2, 2, 1.5, 0.4, 1.75
        TP, θ, γ_c = 0.6, 6.9617521, 24
        γ_r, φ_r = 16.4, 35
        α, ω = 0, 30
        perfil = Perfil([
            Estrato(H_0 = 0.5, γ_s = 17.5, E_s = 3500, c_u = 24.63, φ_s = 38, saturado = False, tipo_mat = "c", c_p = 0, C_s = 0.002,e_0 = 1.91, σ_pp = 90),
            Estrato(H_0 = 1.1, γ_s = 21.4, E_s = 4200, c_u = 0.00, φ_s = 32, saturado = True, tipo_mat = "g", c_p = 0),
            Estrato(H_0 = 0.7, γ_s = 23.6, E_s = 5300, c_u = 24.34, φ_s = 30, saturado = True, tipo_mat = "c", c_p = 0, C_s = 0.003,e_0 = 1.91, σ_pp = 90),
            Estrato(H_0 = 1.2, γ_s = 27.2, E_s = 2800, c_u = 0.00, φ_s = 29, saturado = True, tipo_mat = "g", c_p = 0),
            Estrato(H_0 = 1.3, γ_s = 18.3, E_s = 2400, c_u = 25.40, φ_s = 27, saturado = True, tipo_mat = "c", c_p = 4, C_s = 0.004,e_0 = 1.91, σ_pp = 90),
            Estrato(H_0 = 0.9, γ_s = 20.2, E_s = 3600, c_u = 23.52, φ_s = 35, saturado = True, tipo_mat = "g", c_p = 0),
        ], γ_r=γ_r, φ_r=φ_r)
        self.zapata_4 = Zapata(B, L, D, H, C, TP, θ, γ_c, perfil, α, ω)

        # Zapata 5
        B, L, D, H, C = 5, 5, 1.5, 0.4, 2
        TP, θ, γ_c = 0.6, 8, 23.54
        γ_r, φ_r = 16.4, 35
        α, ω = 0, 30
        perfil = Perfil([
            Estrato(H_0 = 1.0, γ_s = 19.0, E_s = 5550, c_u = 12.63, φ_s = 22, saturado = False, tipo_mat = "c", c_p = 20.2, C_s = 0.4,e_0 = 1.15, σ_pp = 55),
            Estrato(H_0 = 0.5, γ_s = 24.0, E_s = 5420, c_u = 15.63, φ_s = 18, saturado = True, tipo_mat = "c", c_p = 21.3, C_s = 0.4,e_0 = 1.15, σ_pp = 55),
            Estrato(H_0 = 1.3, γ_s = 25.0, E_s = 4350, c_u = 17.63, φ_s = 15, saturado = True, tipo_mat = "c", c_p = 15.6, C_s = 0.4,e_0 = 1.15, σ_pp = 55),
            Estrato(H_0 = 1.5, γ_s = 26.0, E_s = 6000, c_u = 21.63, φ_s = 19, saturado = True, tipo_mat = "c", c_p = 10.8, C_s = 0.4,e_0 = 1.15, σ_pp = 55),
        ], γ_r=γ_r, φ_r=φ_r)
        self.zapata_5 = Zapata(B, L, D, H, C, TP, θ, γ_c, perfil, α, ω)

        # Zapata 6 Roca con granular
        B, L, D, H, C = 5, 5, 1, 0.4, 1.5
        TP, θ, γ_c = 0.6, 8, 23.54
        γ_r, φ_r = 16.4, 35
        α, ω = 0, 30
        perfil = Perfil([
            Estrato(H_0 = 1.0, γ_s = 19.0, E_s = 5550, c_u = 0, φ_s = 34, saturado = False, tipo_mat = "g", c_p = 0),
            Estrato(H_0 = 0.5, γ_s = 24.0, E_s = 5420, c_u = 0, φ_s = 32, saturado = True, tipo_mat = "g", c_p = 0),
            Estrato(H_0 = 1.3, γ_s = 25.0, E_s = 4350, c_u = 0, φ_s = 28, saturado = True, tipo_mat = "g", c_p = 0),
            Estrato(H_0 = 5, γ_s = 26.0, E_s = 115000, c_u = None, φ_s = None, saturado = True, tipo_mat = "r", c_p = None),
        ], γ_r=γ_r, φ_r=φ_r)
        self.zapata_6 = Zapata(B, L, D, H, C, TP, θ, γ_c, perfil, α, ω)

        # Zapata 7 Roca con cohesivo
        B, L, D, H, C = 5, 5, 1, 0.4, 1.5
        TP, θ, γ_c = 0.6, 8, 23.54
        γ_r, φ_r = 16.4, 35
        α, ω = 0, 30
        perfil = Perfil([
            Estrato(H_0 = 0.8, γ_s = 19.0, E_s = 5550, c_u = 12.63, φ_s = 23, saturado = False, tipo_mat = "c", ν = 0.3, c_p = 20.1, C_s = 0.004,e_0 = 1.91, σ_pp = 90),
            Estrato(H_0 = 0.7, γ_s = 24.0, E_s = 5420, c_u = 15.63, φ_s = 15, saturado = True, tipo_mat = "c", ν = 0.5, c_p = 18.4, C_s = 0.004,e_0 = 1.91, σ_pp = 90),
            Estrato(H_0 = 1.2, γ_s = 25.0, E_s = 4350, c_u = 17.63, φ_s = 17, saturado = True, tipo_mat = "c", ν = 0.4, c_p = 17.4, C_s = 0.004,e_0 = 1.91, σ_pp = 90),
            Estrato(H_0 = 4.8, γ_s = 26.0, E_s = 110000, c_u = None, φ_s = None, saturado = True, tipo_mat = "r", c_p = None),
        ], γ_r=γ_r, φ_r=φ_r)
        self.zapata_7 = Zapata(B, L, D, H, C, TP, θ, γ_c, perfil, α, ω)

        # Zapata 8 Roca con mixto
        B, L, D, H, C = 5, 5, 1, 0.4, 1.5
        TP, θ, γ_c = 0.6, 8, 23.54
        γ_r, φ_r = 16.4, 35
        α, ω = 0, 30
        perfil = Perfil([
            Estrato(H_0 = 0.9, γ_s = 19.0, E_s = 5550, c_u = 12.63, φ_s = 24, saturado = False, tipo_mat = "c", c_p = 20.2, C_c = 0, C_s = 0.5,e_0 = 1.2, σ_pp = 30),
            Estrato(H_0 = 0.5, γ_s = 24.0, E_s = 5420, c_u = 0.00, φ_s = 17, saturado = True, tipo_mat = "g", c_p = 0),
            Estrato(H_0 = 0.8, γ_s = 23.2, E_s = 4350, c_u = 17.63, φ_s = 16, saturado = True, tipo_mat = "c", c_p = 15.6, C_c = 0, C_s = 0.4,e_0 = 1.15, σ_pp = 55),
            Estrato(H_0 = 1.2, γ_s = 25.4, E_s = 4350, c_u = 0.00, φ_s = 15, saturado = True, tipo_mat = "g", c_p = 0),
            Estrato(H_0 = 5.1, γ_s = 26.0, E_s = 100000, c_u = None, φ_s = None, saturado = True, tipo_mat = "r", c_p = 10.8),
        ], γ_r=γ_r, φ_r=φ_r)
        self.zapata_8 = Zapata(B, L, D, H, C, TP, θ, γ_c, perfil, α, ω)

        # Zapata 9
        B, L, D, H, C = 2.5, 2.5, 1, 0.4, 2
        TP, θ, γ_c = 0.6, 8, 23.54
        γ_r, φ_r = 16.4, 35
        α, ω = 0, 30
        perfil = Perfil([
            Estrato(H_0 = 0.5, γ_s = 19.0, E_s = 5550, c_u = 12.63, φ_s = 22, saturado = False, tipo_mat = "c", c_p = 20.2, C_s = 1,e_0 = 1.91, σ_pp = 90),
            Estrato(H_0 = 0.5, γ_s = 24.0, E_s = 5420, c_u = 15.63, φ_s = 18, saturado = True, tipo_mat = "c", c_p = 21.3, C_s = 1,e_0 = 1.91, σ_pp = 90),
            Estrato(H_0 = 1.0, γ_s = 25.0, E_s = 4350, c_u = 0.000, φ_s = 15, saturado = True, tipo_mat = "g", c_p = 0),
            Estrato(H_0 = 1.5, γ_s = 26.0, E_s = 6000, c_u = 21.63, φ_s = 19, saturado = True, tipo_mat = "c", c_p = 10.8, C_s = 1,e_0 = 1.91, σ_pp = 90),
        ], γ_r=γ_r, φ_r=φ_r)
        self.zapata_9 = Zapata(B, L, D, H, C, TP, θ, γ_c, perfil, α, ω)
        
        # zapata 10 
        B, L, D, H, C = 2.5, 2.5, 1, 0.4, 2
        TP, θ, γ_c = 0.6, 8, 24
        γ_r, φ_r = 16.4, 23
        α, ω = 0, 0
        perfil = Perfil([
            Estrato(H_0 = 4.5, γ_s = 20.099, E_s = 8760, c_u = 55.564, φ_s = 24.89, saturado = True, tipo_mat = "c", ν = 0.3666, c_p = 12.2249,C_c = 0.209, C_s = 0.0715, e_0 = 0.6444, σ_pp = 196.6954),
            Estrato(H_0 = 2.85, γ_s = 21.232, E_s = 8391, c_u = 50.38, φ_s = 25.2, saturado = True, tipo_mat = "c", ν = 0.3647, c_p = 17.684, C_c = 0.1778, C_s = 0.05827,e_0 = 0.4877, σ_pp = 178.3727),
            Estrato(H_0 = 2.65, γ_s = 20.306, E_s = 24587, c_u = None, φ_s = 29.604, saturado = True, tipo_mat = "g", ν = 0.3358, c_p = None, C_c = None,  C_s = None, e_0 = None, σ_pp = None),
        ], γ_r=γ_r, φ_r=φ_r)
        self.zapata_10 = Zapata(B, L, D, H, C, TP, θ, γ_c, perfil, α, ω)

        # zapata 11
        B, L, D, H, C = 2.5, 2.5, 3, 0.4, 2.2
        TP, θ, γ_c = 0.6, 8, 24
        γ_r, φ_r = 16.4, 23
        α, ω = 0, 0
        perfil = Perfil([
            Estrato(H_0 = 1.5, γ_s = 20.099, E_s = 8760, c_u = 55.564, φ_s = 24.89, saturado = True, tipo_mat = "c", ν = 0.3666, c_p = 12.2249,C_c = 0.209, C_s = 0.0715, e_0 = 0.6444, σ_pp = 196.6954),
            Estrato(H_0 = 1.7, γ_s = 21.232, E_s = 8391, c_u = 50.38, φ_s = 25.2, saturado = True, tipo_mat = "c", ν = 0.3647, c_p = 17.684, C_c = 0.1778, C_s = 0.05827,e_0 = 0.4877, σ_pp = 178.3727),
        ], γ_r=γ_r, φ_r=φ_r)
        self.zapata_11 = Zapata(B, L, D, H, C, TP, θ, γ_c, perfil, α, ω)


        self.perfil10 = Perfil([
            Estrato(H_0 = 1.3, γ_s = 18.0, N=8,  E_s = 2500, c_u =  33.36, φ_s = 24, saturado = False, tipo_mat = "c", c_p = 0,σ_pp=23.4,C_c=0.12,C_s=0.07,e_0=0.38),
            Estrato(H_0 = 3.2, γ_s = 15.0, N=6,  E_s = 2000, c_u =  28.36, φ_s = 24, saturado = False, tipo_mat = "c", c_p = 0,σ_pp=83.8,C_c=0.18,C_s=0.09,e_0=0.25),
            Estrato(H_0 = 2.1, γ_s = 19.0, N=17, E_s = 4800, c_u =  80.36, φ_s = 24, saturado = False, tipo_mat = "c", c_p = 0,σ_pp=125.4,C_c=0.09,C_s=0.02,e_0=0.22),
            Estrato(H_0 = 4.0, γ_s = 20.0, N=20, E_s = 6800, c_u = 120.36, φ_s = 24, saturado = False, tipo_mat = "c", c_p = 0,σ_pp=300,C_c=0.05,C_s=0.009,e_0=0.18),
        ], γ_r=γ_r, φ_r=φ_r)

        self.perfil11 = Perfil([
            Estrato(H_0 = 1.3, γ_s = 18.0, N=8,  E_s = 2500, c_u =  5.36, φ_s = 24, saturado = False, tipo_mat = "c", c_p = 0,σ_pp=23.4,C_c=0.12,C_s=0.07,e_0=0.38),
            Estrato(H_0 = 3.2, γ_s = 15.0, N=6,  E_s = 2000, c_u =  8.36, φ_s = 24, saturado = False, tipo_mat = "c", c_p = 0,σ_pp=83.8,C_c=0.18,C_s=0.09,e_0=0.25),
            Estrato(H_0 = 2.1, γ_s = 19.0, N=17, E_s = 4800, c_u =  80.36, φ_s = 24, saturado = False, tipo_mat = "c", c_p = 0,σ_pp=125.4,C_c=0.09,C_s=0.02,e_0=0.22),
            Estrato(H_0 = 4.0, γ_s = 20.0, N=20, E_s = 6800, c_u = 120.36, φ_s = 24, saturado = False, tipo_mat = "c", c_p = 0,σ_pp=300,C_c=0.05,C_s=0.009,e_0=0.18),
        ], γ_r=γ_r, φ_r=φ_r)


    @classmethod
    def tearDownClass(self):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_atributos(self):
        B, TP, perfil = self.zapata_1.get_atributos("B", "TP", "perfil")
        self.assertEqual(B, 5)
        self.assertEqual(TP, 0.6)
        self.assertEqual(perfil[1].γ_s, 19.0)

    def test_calculo_capacidad_portante_suelos_granulares(self):
                
        zapata = self.zapata_1

        T =  39.1285
        F_zc = 251.34

        q_ult, memoria = zapata.calculo_capacidad_portante_suelos_granulares( T, F_zc)
        print(memoria)
        self.assertAlmostEqual(q_ult, 289.11, places=2)
    
    def test_calculo_capacidad_portante_suelos_granulares2(self):
        
        zapata = copy.deepcopy(self.zapata_1)
        zapata.D = 2

        T =  39.1285
        F_zc = 251.34
        q_ult, memoria = zapata.calculo_capacidad_portante_suelos_granulares(T, F_zc)
        print(memoria)
        self.assertAlmostEqual(q_ult, 349.69, places=2)

    def test_calculo_capacidad_portante_suelos_granulares3(self):
        
        zapata = copy.deepcopy(self.zapata_1)
        zapata.D = 2.5

        T =  39.1285
        F_zc = 251.34
        
        q_ult, memoria = zapata.calculo_capacidad_portante_suelos_granulares(T, F_zc)
        #print(memoria)
        self.assertAlmostEqual(q_ult, 412.92, places=2)

    def test_calculo_capacidad_portante_suelos_granulares4(self):
        
        zapata = copy.deepcopy(self.zapata_1)
        zapata.D = 3

        T =  39.1285
        F_zc = 251.34

        q_ult, memoria = zapata.calculo_capacidad_portante_suelos_granulares(T, F_zc)
        #print(memoria)
        self.assertAlmostEqual(q_ult, 470.11, places=2)

    def test_calculo_capacidad_portante_suelos_granulares5(self):
        zapata = copy.deepcopy(self.zapata_1)
        zapata.B = 1.5
        zapata.L = 1.5
        zapata.D = 3
        zapata.ajustar_perfil()
        
        T =  39.1285
        F_zc = 251.34
        
        q_ult, _ = zapata.calculo_capacidad_portante_suelos_granulares(T, F_zc)
        self.assertAlmostEqual(q_ult, 404.09, places=2)

    def test_calculo_capacidad_portante_suelos_granulares6(self):
        zapata = copy.deepcopy(self.zapata_1)
        zapata.B = 1.5
        zapata.L = 1.5
        zapata.D = 3
        zapata.ajustar_perfil()

        T =  39.3
        F_zc = 416.16

        q_ult, _ = zapata.calculo_capacidad_portante_suelos_granulares(T, F_zc)
        self.assertAlmostEqual(q_ult, 429.82, places=2)

    def test_calculo_capacidad_portante_suelos_granulares7(self):
        zapata = copy.deepcopy(self.zapata_1)
        zapata.B = 1.5
        zapata.L = 1.5
        zapata.D = 1.6
        γ_r, φ_r = 16, 23 
        zapata.set_perfil(Perfil([
            Estrato(H_0 = 1.0, γ_s = 20.0, E_s = 6400, c_u = 0, φ_s = 32, saturado = False, tipo_mat = "g", c_p = 0),
            Estrato(H_0 = 0.5, γ_s = 19.0, E_s = 7100, c_u = 0, φ_s = 35, saturado = False, tipo_mat = "g", c_p = 0),
            Estrato(H_0 = 1.0, γ_s = 21.0, E_s = 6200, c_u = 0, φ_s = 21, saturado = True, tipo_mat = "g", c_p = 0),
            Estrato(H_0 = 2.0, γ_s = 19.0, E_s = 5900, c_u = 0, φ_s = 25, saturado = True, tipo_mat = "g", c_p = 0),
        ], γ_r=γ_r, φ_r=φ_r))
        zapata.ajustar_perfil()

        T =  39.3
        F_zc = 416.16

        q_ult, memoria = zapata.calculo_capacidad_portante_suelos_granulares(T, F_zc)
        print(memoria)
        self.assertAlmostEqual(q_ult, 289.44, places=2)

    def test_calculo_capacidad_portante_suelos_cohesivos(self):
        zapata = copy.deepcopy(self.zapata_1)
        zapata.θ = 6.9617521
        γ_r, φ_r = 16, 23
        zapata.set_perfil(Perfil([
            Estrato(H_0 = 1.0, γ_s = 20.0, E_s = 6597, c_u = 29.36, φ_s = 24, saturado = False, tipo_mat="c",C_s = 0.002,e_0 = 1.91, σ_pp = 90),
            Estrato(H_0 = 0.5, γ_s = 19.0, E_s = 6597, c_u = 29.36, φ_s = 24, saturado = False, tipo_mat="g"),
            Estrato(H_0 = 1.0, γ_s = 21.0, E_s = 6597, c_u = 29.36, φ_s = 24, saturado = False, tipo_mat="c",C_s = 0.002,e_0 = 1.91, σ_pp = 90),
            Estrato(H_0 = 2.0, γ_s = 19.0, E_s = 6597, c_u = 29.36, φ_s = 24, saturado = False, tipo_mat="c",C_s = 0.002,e_0 = 1.91, σ_pp = 90),
        ], γ_r=γ_r, φ_r=φ_r))
        zapata.ω = 0
        
        T = 39.3
        F_zc = 251.34

        q_ult, memoria = zapata.calculo_capacidad_portante_suelos_cohesivos(T, F_zc)
        print(memoria)
        self.assertAlmostEqual(q_ult, 227.25, places=2)
    
    def test_calculo_capacidad_portante_suelos_cohesivos2(self):
        zapata = copy.deepcopy(self.zapata_1)
        zapata.θ = 6.9617521
        zapata.D = 2
        γ_r, φ_r = 16, 23
        zapata.set_perfil(Perfil([
            Estrato(H_0 = 1.0, γ_s = 20.0, E_s = 6597, c_u = 29.36, φ_s = 24, saturado = False, tipo_mat="c", C_s = 0.002,e_0 = 1.91, σ_pp = 90),
            Estrato(H_0 = 0.5, γ_s = 19.0, E_s = 6597, c_u = 29.36, φ_s = 24, saturado = False, tipo_mat="c", C_s = 0.002,e_0 = 1.91, σ_pp = 90),
            Estrato(H_0 = 1.0, γ_s = 21.0, E_s = 6597, c_u = 29.36, φ_s = 24, saturado = False, tipo_mat="g"),
            Estrato(H_0 = 2.0, γ_s = 19.0, E_s = 6597, c_u = 29.36, φ_s = 24, saturado = False, tipo_mat="c", C_s = 0.002,e_0 = 1.91, σ_pp = 90),
        ], γ_r=γ_r, φ_r=φ_r))
        zapata.ω = 0

        T = 39.3
        F_zc = 251.34

        q_ult, memoria = zapata.calculo_capacidad_portante_suelos_cohesivos(T, F_zc)
        print(memoria)
        self.assertAlmostEqual(q_ult, 244.67, places=2)
        
    def test_calculo_capacidad_portante_suelos_cohesivos3(self):
        zapata = copy.deepcopy(self.zapata_1)
        zapata.θ = 6.9617521
        zapata.D = 2.7
        γ_r, φ_r = 16, 23
        zapata.set_perfil(Perfil([
            Estrato(H_0 = 1.0, γ_s = 20.0, E_s = 6597, c_u = 29.36, φ_s = 24, saturado = False, tipo_mat="c", C_s = 0.002,e_0 = 1.91, σ_pp = 90),
            Estrato(H_0 = 0.5, γ_s = 19.0, E_s = 6597, c_u = 29.36, φ_s = 24, saturado = False, tipo_mat="c", C_s = 0.002,e_0 = 1.91, σ_pp = 90),
            Estrato(H_0 = 1.0, γ_s = 21.0, E_s = 6597, c_u = 29.36, φ_s = 24, saturado = False, tipo_mat="c", C_s = 0.002,e_0 = 1.91, σ_pp = 90),
            Estrato(H_0 = 2.0, γ_s = 19.0, E_s = 6597, c_u = 29.36, φ_s = 24, saturado = False, tipo_mat="c", C_s = 0.002,e_0 = 1.91, σ_pp = 90),
        ], γ_r=γ_r, φ_r=φ_r))
        zapata.ω = 0

        T = 39.3
        F_zc = 251.34

        q_ult, _ = zapata.calculo_capacidad_portante_suelos_cohesivos(T, F_zc)
        self.assertAlmostEqual(q_ult, 268.76, places=2)

    def test_calculo_capacidad_portante_suelos_cohesivos4(self):
        zapata = copy.deepcopy(self.zapata_1)
        zapata.θ = 6.9617521
        zapata.B = 3
        zapata.L = 3
        zapata.D = 2.7
        γ_r, φ_r = 16, 23
        zapata.set_perfil(Perfil([
            Estrato(H_0 = 1.0, γ_s = 20.0, E_s = 6597, c_u = 29.36, φ_s = 24, saturado = False, tipo_mat="c",C_s = 0.002,e_0 = 1.91, σ_pp = 90),
            Estrato(H_0 = 0.5, γ_s = 19.0, E_s = 6597, c_u = 29.36, φ_s = 24, saturado = False, tipo_mat="c", C_s = 0.002,e_0 = 1.91, σ_pp = 90),
            Estrato(H_0 = 1.0, γ_s = 21.0, E_s = 6597, c_u = 29.36, φ_s = 24, saturado = False, tipo_mat="c", C_s = 0.002,e_0 = 1.91, σ_pp = 90),
            Estrato(H_0 = 2.0, γ_s = 19.0, E_s = 6597, c_u = 29.36, φ_s = 24, saturado = False, tipo_mat="c",C_s = 0.002,e_0 = 1.91, σ_pp = 90),
        ], γ_r=γ_r, φ_r=φ_r))
        zapata.ω = 0
        zapata.ajustar_perfil()

        T = 39.3
        F_zc = 251.34

        q_ult, _ = zapata.calculo_capacidad_portante_suelos_cohesivos(T, F_zc)
        
        self.assertAlmostEqual(q_ult, 284.28, places=2)
        
    def test_calculo_capacidad_portante_suelos_cohesivos5(self):
        zapata = copy.deepcopy(self.zapata_1)
        zapata.θ = 6.9617521
        zapata.B = 2
        zapata.L = 2
        zapata.D = 2.7
        γ_r, φ_r = 16, 23
        zapata.set_perfil(Perfil([
            Estrato(H_0 = 1.0, γ_s = 20.0, E_s = 6597, c_u = 29.36, φ_s = 24, saturado = False, tipo_mat="c",C_s = 0.002,e_0 = 1.91, σ_pp = 90),
            Estrato(H_0 = 0.5, γ_s = 19.0, E_s = 6597, c_u = 29.36, φ_s = 24, saturado = False, tipo_mat="c", C_s = 0.002,e_0 = 1.91, σ_pp = 90),
            Estrato(H_0 = 1.0, γ_s = 21.0, E_s = 6597, c_u = 29.36, φ_s = 24, saturado = False, tipo_mat="c", C_s = 0.002,e_0 = 1.91, σ_pp = 90),
            Estrato(H_0 = 2.0, γ_s = 19.0, E_s = 6597, c_u = 29.36, φ_s = 24, saturado = False, tipo_mat="c", C_s = 0.002,e_0 = 1.91, σ_pp = 90),
        ], γ_r=γ_r, φ_r=φ_r))
        zapata.ω = 0
        zapata.ajustar_perfil()
        T = 39.3
        F_zc = 251.34

        q_ult, _ = zapata.calculo_capacidad_portante_suelos_cohesivos(T, F_zc)
        
        self.assertAlmostEqual(q_ult, 266.11, places=2)

    def test_calculo_capacidad_portante_suelos_cohesivos6(self):
        zapata = copy.deepcopy(self.zapata_1)
        zapata.θ = 6.9617521
        zapata.B = 2
        zapata.L = 2
        zapata.D = 2.7
        γ_r, φ_r = 16, 23
        zapata.set_perfil(Perfil([
            Estrato(H_0 = 1.0, γ_s = 20.0, E_s = 6597, c_u = 29.36, φ_s = 24, saturado = False, tipo_mat="c", C_s = 0.002,e_0 = 1.91, σ_pp = 90),
            Estrato(H_0 = 0.5, γ_s = 19.0, E_s = 6597, c_u = 29.36, φ_s = 24, saturado = False, tipo_mat="c", C_s = 0.002,e_0 = 1.91, σ_pp = 90),
            Estrato(H_0 = 1.0, γ_s = 21.0, E_s = 6597, c_u = 29.36, φ_s = 24, saturado = False, tipo_mat="c", C_s = 0.002,e_0 = 1.91, σ_pp = 90),
            Estrato(H_0 = 2.0, γ_s = 19.0, E_s = 6597, c_u = 29.36, φ_s = 24, saturado = False, tipo_mat="c", C_s = 0.002,e_0 = 1.91, σ_pp = 90),
        ], γ_r=γ_r, φ_r=φ_r))
        zapata.ω = 30
        zapata.ajustar_perfil()
        T = 39.3
        F_zc = 251.34

        q_ult, _ = zapata.calculo_capacidad_portante_suelos_cohesivos(T, F_zc)
        
        self.assertAlmostEqual(q_ult, 221.53, places=2)

    def test_calculo_capacidad_portante_suelos_cohesivos7(self):
        zapata = copy.deepcopy(self.zapata_1)
        zapata.θ = 6.9617521
        zapata.B = 2
        zapata.L = 2
        zapata.D = 2.7
        γ_r, φ_r = 16, 23
        zapata.set_perfil(Perfil([
            Estrato(H_0 = 1.0, γ_s = 20.0, E_s = 6597, c_u = 29.36, φ_s = 24, saturado = False, tipo_mat="c", C_s = 0.002,e_0 = 1.91, σ_pp = 90),
            Estrato(H_0 = 0.5, γ_s = 19.0, E_s = 6597, c_u = 29.36, φ_s = 24, saturado = False, tipo_mat="c", C_s = 0.002,e_0 = 1.91, σ_pp = 90),
            Estrato(H_0 = 1.0, γ_s = 21.0, E_s = 6597, c_u = 29.36, φ_s = 24, saturado = False, tipo_mat="c", C_s = 0.002,e_0 = 1.91, σ_pp = 90),
            Estrato(H_0 = 2.0, γ_s = 19.0, E_s = 6597, c_u = 29.36, φ_s = 24, saturado = False, tipo_mat="c", C_s = 0.002,e_0 = 1.91, σ_pp = 90),
        ], γ_r=γ_r, φ_r=φ_r))
        zapata.ω = 45
        zapata.ajustar_perfil()
        T = 39.3
        F_zc = 251.34

        q_ult, _ = zapata.calculo_capacidad_portante_suelos_cohesivos(T, F_zc)
        
        self.assertAlmostEqual(q_ult, 199.24, places=2)

    def test_calculo_capacidad_portante_suelos_cohesivos8(self):
        zapata = copy.deepcopy(self.zapata_9)
        zapata.θ = 6.9617521
        
        
        zapata.ω = 0
        T = 39.3
        F_zc = 600

        q_ult, memoria = zapata.calculo_capacidad_portante_suelos_cohesivos(T, F_zc)
        print(memoria)
        self.assertAlmostEqual(q_ult, 159.79, places=2)

    def test_calculo_capacidad_portante_suelos_cohesivos9(self):
        zapata = copy.deepcopy(self.zapata_11)
        
        zapata.ω = 0
        T = 39.3
        F_zc = 600

        q_ult, memoria = zapata.calculo_capacidad_portante_suelos_cohesivos(T, F_zc)
        print(memoria)
        self.assertAlmostEqual(q_ult, 460.01, places=2)
        
    def test_calculo_carga_lateral1(self):
        zapata = copy.deepcopy(self.zapata_3)
        
        F_zc = 52.6
        Q_L, memoria = zapata.calculo_carga_lateral(F_zc)
        #print(memoria)
        self.assertAlmostEqual(Q_L, 562.10, places=2)

    def test_calculo_carga_lateral2(self):
        zapata = copy.deepcopy(self.zapata_3)
        zapata.B = 3
        zapata.L = 3
        zapata.D = 1.8
        γ_r, φ_r = 16, 23
        zapata.set_perfil(Perfil([
            Estrato(H_0 = 1.0, γ_s = 15.0, E_s = 4000, c_u = 24.63, φ_s = 22, saturado = False, tipo_mat="c", C_s = 0.002,e_0 = 1.91, σ_pp = 90),
            Estrato(H_0 = 0.8, γ_s = 15.0, E_s = 4000, c_u = 27.53, φ_s = 23, saturado = False, tipo_mat="c", C_s = 0.002,e_0 = 1.91, σ_pp = 90),
            Estrato(H_0 = 1.5, γ_s = 15.0, E_s = 4000, c_u = 24.63, φ_s = 20, saturado = False, tipo_mat="c", C_s = 0.002,e_0 = 1.91, σ_pp = 90),
        ], γ_r=γ_r, φ_r=φ_r))
        zapata.ajustar_perfil()
        

        F_zc = 55.6
        Q_L, memoria = zapata.calculo_carga_lateral(F_zc)
        #print(memoria)
        self.assertAlmostEqual(Q_L, 262.75, places=2)

    def test_calculo_carga_lateral3(self):
        zapata = copy.deepcopy(self.zapata_3)
        zapata.B = 3
        zapata.L = 3
        zapata.D = 1.8
        γ_r, φ_r = 16, 23
        zapata.set_perfil(Perfil([
            Estrato(H_0 = 1.0, γ_s = 15.0, E_s = 4000, c_u = 24.63, φ_s = 22, saturado = False, tipo_mat="c", C_s = 0.002,e_0 = 1.91, σ_pp = 90),
            Estrato(H_0 = 0.8, γ_s = 15.0, E_s = 4000, c_u = 27.53, φ_s = 23, saturado = False, tipo_mat="c", C_s = 0.002,e_0 = 1.91, σ_pp = 90),
            Estrato(H_0 = 1.5, γ_s = 15.0, E_s = 4000, c_u = 24.63, φ_s = 20, saturado = False, tipo_mat="c", C_s = 0.002,e_0 = 1.91, σ_pp = 90),
        ], γ_r=γ_r, φ_r=φ_r))
        zapata.ajustar_perfil()

        F_zc = 55.6
        Q_L, memoria = zapata.calculo_carga_lateral(F_zc)
        #print(memoria)
        self.assertAlmostEqual(Q_L, 262.75, places=2)

    def test_calculo_carga_lateral4(self):
        zapata = copy.deepcopy(self.zapata_3)
        zapata.B = 2.5
        zapata.L = 2.5
        zapata.D = 1.8
        γ_r, φ_r = 16, 23
        zapata.set_perfil(Perfil([
            Estrato(H_0 = 1.0, γ_s = 15.0, E_s = 4000, c_u = 24.63, φ_s = 22, saturado = False, tipo_mat="c", C_s = 0.002,e_0 = 1.91, σ_pp = 90),
            Estrato(H_0 = 0.8, γ_s = 15.0, E_s = 4000, c_u = 27.53, φ_s = 23, saturado = False, tipo_mat="c", C_s = 0.002,e_0 = 1.91, σ_pp = 90),
            Estrato(H_0 = 1.5, γ_s = 15.0, E_s = 4000, c_u = 24.63, φ_s = 20, saturado = False, tipo_mat="c", C_s = 0.002,e_0 = 1.91, σ_pp = 90),
        ], γ_r=γ_r, φ_r=φ_r))
        zapata.ajustar_perfil()

        F_zc = 55.6
        Q_L, memoria = zapata.calculo_carga_lateral(F_zc)
        #print(memoria)
        self.assertAlmostEqual(Q_L, 201.79, places=2)

    def test_calculo_carga_lateral5(self):
        zapata = copy.deepcopy(self.zapata_3)
        zapata.B = 2.5
        zapata.L = 2.5
        zapata.D = 2.0
        γ_r, φ_r = 16, 23
        zapata.set_perfil(Perfil([
            Estrato(H_0 = 1.0, γ_s = 15.0, E_s = 4000, c_u = 24.63, φ_s = 22, saturado = False, tipo_mat="c", C_s = 0.002,e_0 = 1.91, σ_pp = 90),
            Estrato(H_0 = 0.8, γ_s = 15.0, E_s = 4000, c_u = 27.53, φ_s = 23, saturado = False, tipo_mat="c", C_s = 0.002,e_0 = 1.91, σ_pp = 90),
            Estrato(H_0 = 1.5, γ_s = 15.0, E_s = 4000, c_u = 24.63, φ_s = 20, saturado = False, tipo_mat="c", C_s = 0.002,e_0 = 1.91, σ_pp = 90),
        ], γ_r=γ_r, φ_r=φ_r))
        zapata.ajustar_perfil()

        F_zc = 55.6
        Q_L, memoria = zapata.calculo_carga_lateral(F_zc)
        #print(memoria)
        self.assertAlmostEqual(Q_L, 206.42, places=2)

    def test_calculo_carga_lateral6(self):
        B = 5
        L = B
        D = 1.5
        H = 0.4
        C = 1.6
        TP = 0.6
        γ_r, φ_r = 16, 23
        perfil = Perfil([
            Estrato(H_0 = 1.0, γ_s = 15.0, E_s = 5000, c_u = 0, φ_s = 22, saturado = False, tipo_mat="g"),
            Estrato(H_0 = 1.0, γ_s = 15.0, E_s = 5000, c_u = 0, φ_s = 10, saturado = False, tipo_mat="g"),
            Estrato(H_0 = 1.5, γ_s = 15.0, E_s = 5000, c_u = 0, φ_s = 28, saturado = False, tipo_mat="g"),
        ], γ_r=γ_r, φ_r=φ_r)
        γ_r = 15
        φ_r = 22
        zapata = Zapata(B, L, D, H, C, TP, None, None, perfil, None, None)

        F_zc = 52.6
        
        Q_L, _ = zapata.calculo_carga_lateral(F_zc)
        self.assertAlmostEqual(Q_L, 44.79, places=2)

    def test_calculo_carga_lateral7(self):
        
        F_zc = 55.6

        Q_L, memoria = self.zapata_2.calculo_carga_lateral(F_zc)
        print(memoria)
        self.assertAlmostEqual(Q_L, 82.571, places=3)

    def test_calculo_carga_lateral8(self):
        
        F_zc = 67.68

        Q_L, memoria = self.zapata_2.calculo_carga_lateral(F_zc)
        #print(memoria)
        self.assertAlmostEqual(Q_L, 85.883, places=3)

    def test_calculo_carga_lateral9(self):
        
        F_zc = 1200

        Q_L, memoria = self.zapata_2.calculo_carga_lateral(F_zc)
        #print(memoria)
        self.assertAlmostEqual(Q_L, 396.359, places=3)

    def test_calculo_carga_lateral10(self):
        
        zapata = copy.deepcopy(self.zapata_2)
        zapata.B = 3.5
        zapata.L = 3.5
        zapata.ajustar_perfil()
        F_zc = 75.66

        Q_L, memoria = zapata.calculo_carga_lateral(F_zc)
        #print(memoria)
        self.assertAlmostEqual(Q_L, 98.101, places=3)

    def test_calculo_tension_cono_tierra_suelos_granulares(self):
        zapata = copy.deepcopy(self.zapata_1)
        zapata.θ = 8
        γ_r, φ_r = 16.4, 23
        zapata.set_perfil(Perfil([
            Estrato(H_0 = 1.0, γ_s = 20.0, E_s = 5000, c_u = None, φ_s = 26, saturado = False, tipo_mat="g"),
            Estrato(H_0 = 0.5, γ_s = 19.0, E_s = 5000, c_u = None, φ_s = 28, saturado = False, tipo_mat="g"),
            Estrato(H_0 = 1.0, γ_s = 21.0, E_s = 5000, c_u = None, φ_s = 29, saturado = False, tipo_mat="g"),
            Estrato(H_0 = 2.0, γ_s = 19.0, E_s = 5000, c_u = None, φ_s = 25, saturado = False, tipo_mat="g"),
        ], γ_r=γ_r, φ_r=φ_r))
        
        q_adm = 200
        
        T_u, memoria = zapata.calculo_tension_cono_tierra_suelos_granulares(q_adm)
        #print(memoria)
        self.assertAlmostEqual(T_u, 981.93, places=2)

    def test_calculo_tension_cono_tierra_suelos_granulares2(self):
        zapata = copy.deepcopy(self.zapata_1)
        zapata.θ = 8

        q_adm = 200
        
        T_u, memoria = zapata.calculo_tension_cono_tierra_suelos_granulares(q_adm)
        #print(memoria)
        self.assertAlmostEqual(T_u, 606.36, places=2)

    def test_calculo_tension_cono_tierra_suelos_granulares3(self):
        zapata = copy.deepcopy(self.zapata_1)
        zapata.θ = 8
        zapata.γ_r = 15
        zapata.B = 3
        zapata.L = 3
        zapata.ajustar_perfil()
                
        q_adm = 200
        
        T_u, memoria = zapata.calculo_tension_cono_tierra_suelos_granulares(q_adm)
        #print(memoria)
        self.assertAlmostEqual(T_u, 273.68, places=2)

    def test_calculo_tension_cono_tierra_suelos_granulares4(self):
        zapata = copy.deepcopy(self.zapata_1)
        zapata.θ = 8
        zapata.γ_r = 15
        zapata.B = 3
        zapata.L = 3
        zapata.D = 1.8
        zapata.ajustar_perfil()
        q_adm = 200
        
        T_u, memoria = zapata.calculo_tension_cono_tierra_suelos_granulares(q_adm)
        #print(memoria)
        self.assertAlmostEqual(T_u, 333.01, places=2)

    def test_calculo_tension_cono_tierra_suelos_granulares5(self):
        zapata = copy.deepcopy(self.zapata_1)
        zapata.θ = 8
        zapata.γ_r = 15
        zapata.B = 2.5
        zapata.L = 2.5
        zapata.D = 2
        zapata.ajustar_perfil()
        q_adm = 200
        
        T_u, memoria = zapata.calculo_tension_cono_tierra_suelos_granulares(q_adm)
        #print(memoria)
        self.assertAlmostEqual(T_u, 291.17, places=2)

    def test_calculo_tension_cono_tierra_suelos_granulares6(self):
        zapata = copy.deepcopy(self.zapata_1)
        zapata.θ = 8
        zapata.γ_r = 15
        zapata.B = 2.5
        zapata.L = 2.5
        zapata.D = 2
        γ_r, φ_r = 16.4, 23
        zapata.set_perfil(Perfil([
            Estrato(H_0 = 1.0, γ_s = 20.0, E_s = 6597, c_u = 0, φ_s = 24, saturado = True, tipo_mat = "g", c_p = 0),
            Estrato(H_0 = 0.5, γ_s = 19.0, E_s = 6597, c_u = 0, φ_s = 24, saturado = True, tipo_mat = "g", c_p = 0),
            Estrato(H_0 = 1.0, γ_s = 21.0, E_s = 6597, c_u = 0, φ_s = 24, saturado = True, tipo_mat = "g", c_p = 0),
            Estrato(H_0 = 2.0, γ_s = 19.0, E_s = 6597, c_u = 0, φ_s = 24, saturado = True, tipo_mat = "g", c_p = 0),
        ], γ_r=γ_r, φ_r=φ_r))
        zapata.ajustar_perfil()

        q_adm = 200
        
        T_u, memoria = zapata.calculo_tension_cono_tierra_suelos_granulares(q_adm)
        #print(memoria)
        self.assertAlmostEqual(T_u, 200.90, places=2)

    def test_calculo_tension_cono_tierra_suelos_granulares7(self):
        zapata = copy.deepcopy(self.zapata_1)
        zapata.θ = 8
        zapata.γ_r = 15
        zapata.B = 2.5
        zapata.L = 2.5
        zapata.D = 2
        γ_r, φ_r = 16.4, 23
        zapata.set_perfil(Perfil([
            Estrato(H_0 = 1.0, γ_s = 16.0, E_s = 6597, c_u = 0, φ_s = 24, saturado = False, tipo_mat = "g", c_p = 0),
            Estrato(H_0 = 0.5, γ_s = 17.0, E_s = 6597, c_u = 0, φ_s = 24, saturado = False, tipo_mat = "g", c_p = 0),
            Estrato(H_0 = 1.0, γ_s = 16.0, E_s = 6597, c_u = 0, φ_s = 24, saturado = False, tipo_mat = "g", c_p = 0),
            Estrato(H_0 = 2.0, γ_s = 17.0, E_s = 6597, c_u = 0, φ_s = 24, saturado = False, tipo_mat = "g", c_p = 0),
        ], γ_r=γ_r, φ_r=φ_r))
        zapata.ajustar_perfil()

        q_adm = 200
        
        T_u, memoria = zapata.calculo_tension_cono_tierra_suelos_granulares(q_adm)
        #print(memoria)
        self.assertAlmostEqual(T_u, 475.84, places=2)

    def test_calculo_tension_cono_tierra_suelos_granulares8(self):
        zapata = copy.deepcopy(self.zapata_1)
        zapata.θ = 8
        zapata.γ_r = 15
        zapata.B = 2.5
        zapata.L = 2.5
        zapata.D = 2
        γ_r, φ_r = 16.4, 23
        zapata.set_perfil(Perfil([
            Estrato(H_0 = 1.0, γ_s = 16.0, E_s = 6597, c_u = 0, φ_s = 24, saturado = True, tipo_mat = "g", c_p = 0),
            Estrato(H_0 = 0.5, γ_s = 17.0, E_s = 6597, c_u = 0, φ_s = 24, saturado = True, tipo_mat = "g", c_p = 0),
            Estrato(H_0 = 1.0, γ_s = 16.0, E_s = 6597, c_u = 0, φ_s = 24, saturado = True, tipo_mat = "g", c_p = 0),
            Estrato(H_0 = 2.0, γ_s = 17.0, E_s = 6597, c_u = 0, φ_s = 24, saturado = True, tipo_mat = "g", c_p = 0),
        ], γ_r=γ_r, φ_r=φ_r))
        zapata.ajustar_perfil()

        q_adm = 200
        
        T_u, memoria = zapata.calculo_tension_cono_tierra_suelos_granulares(q_adm)
        print(memoria)
        self.assertAlmostEqual(T_u, 177.93, places=2)

    def test_calculo_tension_meyerhof_adams_suelos_cohesivos(self):
        zapata = copy.deepcopy(self.zapata_3)
        zapata.θ = 8
        zapata.γ_c =  23.53
        γ_r, φ_r = 16.4, 23
        zapata.set_perfil(Perfil([
            Estrato(H_0 = 1.0, γ_s = 20.0, E_s = 5000, c_u = 32, φ_s = 24, saturado = False, c_p=20.2,tipo_mat="c", C_s = 0.002,e_0 = 1.91, σ_pp = 90),
            Estrato(H_0 = 0.5, γ_s = 19.0, E_s = 5000, c_u = 34, φ_s = 24, saturado = True, c_p=20.2,tipo_mat="c", C_s = 0.002,e_0 = 1.91, σ_pp = 90),
            Estrato(H_0 = 1.0, γ_s = 21.0, E_s = 5000, c_u = 35, φ_s = 24, saturado = True, c_p=20.2,tipo_mat="c", C_s = 0.002,e_0 = 1.91, σ_pp = 90),
            Estrato(H_0 = 2.0, γ_s = 19.0, E_s = 5000, c_u = 28, φ_s = 24, saturado = True, c_p=20.2,tipo_mat="c", C_s = 0.002,e_0 = 1.91, σ_pp = 90),
        ], γ_r=γ_r, φ_r=φ_r))
        T_u, memoria = zapata.calculo_tension_meyerhof_adams_suelos_cohesivos()
        #print(memoria)
        self.assertAlmostEqual(T_u, 1080.45, places=2)

    def test_calculo_tension_meyerhof_adams_suelos_cohesivos2(self):
        
        T_u, memoria = self.zapata_5.calculo_tension_meyerhof_adams_suelos_cohesivos()
        
        #print(memoria)
        self.assertAlmostEqual(T_u, 1072.98 , places=2)

    def test_calculo_tension_meyerhof_adams_suelos_cohesivos3(self):
        
        zapata = copy.deepcopy(self.zapata_5)
        γ_r, φ_r = 16, 23
        zapata.set_perfil(Perfil([
            Estrato(H_0 = 1.0, γ_s = 19.0, E_s = 5550, c_u = 12.63, φ_s = 22, saturado = False, tipo_mat = "c", c_p = 20.2, C_s = 0.002,e_0 = 1.91, σ_pp = 90),
            Estrato(H_0 = 0.5, γ_s = 24.0, E_s = 5420, c_u = 15.63, φ_s = 18, saturado = True, tipo_mat = "g", c_p = 0),
            Estrato(H_0 = 1.3, γ_s = 25.0, E_s = 4350, c_u = 17.63, φ_s = 15, saturado = True, tipo_mat = "c", c_p = 15.6, C_s = 0.002,e_0 = 1.91, σ_pp = 90),
            Estrato(H_0 = 1.5, γ_s = 26.0, E_s = 6000, c_u = 21.63, φ_s = 19, saturado = True, tipo_mat = "c", c_p = 10.8, C_s = 0.002,e_0 = 1.91, σ_pp = 90),
        ], γ_r=γ_r, φ_r=φ_r))
        T_u, memoria = zapata.calculo_tension_meyerhof_adams_suelos_cohesivos()
        
        #print(memoria)
        self.assertAlmostEqual(T_u, 859.97 , places=2)

    def test_calculo_tension_meyerhof_adams_suelos_cohesivos4(self):
        
        zapata = copy.deepcopy(self.zapata_5)
        zapata.D = 2.5
        γ_r, φ_r = 6, 23
        zapata.set_perfil(Perfil([
            Estrato(H_0 = 1.0, γ_s = 19.0, E_s = 5550, c_u = 12.63, φ_s = 22, saturado = True, tipo_mat = "c", c_p = 20.2, C_s = 0.002,e_0 = 1.91, σ_pp = 90),
            Estrato(H_0 = 0.5, γ_s = 24.0, E_s = 5420, c_u = 15.63, φ_s = 18, saturado = True, tipo_mat = "g", c_p = 0),
            Estrato(H_0 = 1.3, γ_s = 25.0, E_s = 4350, c_u = 17.63, φ_s = 15, saturado = True, tipo_mat = "c", c_p = 15.6, C_s = 0.002,e_0 = 1.91, σ_pp = 90),
            Estrato(H_0 = 1.5, γ_s = 26.0, E_s = 6000, c_u = 21.63, φ_s = 19, saturado = True, tipo_mat = "g", c_p = 0),
        ], γ_r=γ_r, φ_r=φ_r))
        T_u, memoria = zapata.calculo_tension_meyerhof_adams_suelos_cohesivos()
        
        print(memoria)
        self.assertAlmostEqual(T_u, 892.49 , places=2)

    def test_calculo_tension_meyerhof_adams_suelos_cohesivos5(self):
        
        zapata = copy.deepcopy(self.zapata_5)
        zapata.D = 2.5
        zapata.B = 2.5
        zapata.L = 2.5
        γ_r, φ_r = 16, 23
        zapata.set_perfil(Perfil([
            Estrato(H_0 = 1.0, γ_s = 19.0, E_s = 5550, c_u = 12.63, φ_s = 22, saturado = False, tipo_mat = "c", c_p = 20.2, C_s = 0.002,e_0 = 1.91, σ_pp = 90),
            Estrato(H_0 = 0.5, γ_s = 24.0, E_s = 5420, c_u = 15.63, φ_s = 18, saturado = True, tipo_mat = "g", c_p = 0),
            Estrato(H_0 = 1.3, γ_s = 25.0, E_s = 4350, c_u = 17.63, φ_s = 15, saturado = True, tipo_mat = "c", c_p = 15.6, C_s = 0.002,e_0 = 1.91, σ_pp = 90),
            Estrato(H_0 = 1.5, γ_s = 26.0, E_s = 6000, c_u = 21.63, φ_s = 19, saturado = True, tipo_mat = "g", c_p = 0),
        ], γ_r=γ_r, φ_r=φ_r))
        zapata.ajustar_perfil()
        T_u, memoria = zapata.calculo_tension_meyerhof_adams_suelos_cohesivos()
        
        #print(memoria)
        self.assertAlmostEqual(T_u, 630.88 , places=2)

    def test_calculo_tension_meyerhof_adams_suelos_cohesivos6(self):
        
        zapata = copy.deepcopy(self.zapata_5)
        zapata.D = 2.5
        zapata.B = 2.5
        zapata.L = 2.5
        zapata.H = 0.3
        zapata.TP = 0.3
        zapata.γ_c =  14
        γ_r, φ_r = 16, 23
        zapata.set_perfil(Perfil([
            Estrato(H_0 = 1.0, γ_s = 19.0, E_s = 5550, c_u = 12.63, φ_s = 25, saturado = True, tipo_mat = "c", c_p = 20.2, C_s = 0.002,e_0 = 1.91, σ_pp = 90),
            Estrato(H_0 = 0.5, γ_s = 21.0, E_s = 5420, c_u = 15.63, φ_s = 24, saturado = True, tipo_mat = "g", c_p = 0),
            Estrato(H_0 = 1.5, γ_s = 22.0, E_s = 6000, c_u = 21.63, φ_s = 25, saturado = True, tipo_mat = "g", c_p = 0),
            Estrato(H_0 = 1.3, γ_s = 21.0, E_s = 4350, c_u = 17.63, φ_s = 24, saturado = True, tipo_mat = "c", c_p = 15.6, C_s = 0.002,e_0 = 1.91, σ_pp = 90),
        ], γ_r=γ_r, φ_r=φ_r))
        zapata.ajustar_perfil()
        T_u, memoria = zapata.calculo_tension_meyerhof_adams_suelos_cohesivos()
        
        print(memoria)
        self.assertAlmostEqual(T_u, 447.62 , places=2)


    def test_calculo_esfuerzo_actuante_sobre_suelo(self):
        zapata = copy.deepcopy(self.zapata_4)
        zapata.D = 1.9
        zapata.φ_r = 23
        γ_r, φ_r = 16.4, 23
        zapata.set_perfil(Perfil([
            Estrato(H_0 = 1.0, γ_s = 19.5, E_s = 3000, c_u = None, φ_s = 38, saturado = False, tipo_mat = 'g'),
            Estrato(H_0 = 1.0, γ_s = 19.5, E_s = 3000, c_u = None, φ_s = 38, saturado = False, tipo_mat = 'g'),
            Estrato(H_0 = 1.0, γ_s = 19.5, E_s = 3000, c_u = None, φ_s = 38, saturado = False, tipo_mat = 'g'),
            Estrato(H_0 = 1.0, γ_s = 19.5, E_s = 3000, c_u = 25, φ_s = 38, saturado = False, tipo_mat = 'c', C_s = 0.002,e_0 = 1.91, σ_pp = 90),
        ], γ_r=γ_r, φ_r=φ_r))

        Fx_c = 38.06
        Fy_c = 39.30
        Fz_c = 275.23   
        Q_max, Q_min, memoria = zapata.calculo_esfuerzo_actuante_sobre_suelo(Fx_c, Fy_c, Fz_c)
        print(memoria)
        self.assertAlmostEqual(Q_min, 65.02, places =2)
        self.assertAlmostEqual(Q_max, 144.15, places =2)

    def test_calculo_esfuerzo_actuante_sobre_suelo2(self):
        zapata = copy.deepcopy(self.zapata_4)
        zapata.B = 5
        zapata.L = 5
        zapata.C =2
        zapata.φ_r = 23
        γ_r, φ_r = 16.4, 23
        zapata.set_perfil(Perfil([
            Estrato(H_0 = 1.0, γ_s = 19.5, E_s = 3000, c_u = None, φ_s = 38, saturado = False, tipo_mat = 'g'),
            Estrato(H_0 = 1.0, γ_s = 19.5, E_s = 3000, c_u = None, φ_s = 38, saturado = False, tipo_mat = 'g'),
            Estrato(H_0 = 1.0, γ_s = 19.5, E_s = 3000, c_u = None, φ_s = 38, saturado = False, tipo_mat = 'g'),
            Estrato(H_0 = 1.0, γ_s = 19.5, E_s = 3000, c_u = 22, φ_s = 38, saturado = False, tipo_mat = 'c', C_s = 0.002,e_0 = 1.91, σ_pp = 90),
        ], γ_r=γ_r, φ_r=φ_r))
        zapata.ajustar_perfil()

        Fx_c = 38.06
        Fy_c = 39.30
        Fz_c = 275.23   
        Q_max, Q_min, memoria = zapata.calculo_esfuerzo_actuante_sobre_suelo(Fx_c, Fy_c, Fz_c)
        print(memoria)
        self.assertAlmostEqual(Q_min, 36.75, places =2)
        self.assertAlmostEqual(Q_max, 41.42, places =2)

    def test_calculo_esfuerzo_actuante_sobre_suelo3(self):
        zapata = copy.deepcopy(self.zapata_4)
        
        Fx_c = 38.06
        Fy_c = 39.30
        Fz_c = 275.23   
        Q_max, Q_min, memoria = zapata.calculo_esfuerzo_actuante_sobre_suelo(Fx_c, Fy_c, Fz_c)
        #print(memoria)
        self.assertAlmostEqual(Q_min, 62.10, places =2)
        self.assertAlmostEqual(Q_max, 135.14, places =2)

    def test_calculo_esfuerzo_actuante_sobre_suelo4(self):
        zapata = copy.deepcopy(self.zapata_4)
        
        Fx_c = 103.11
        Fy_c = 89.53
        Fz_c = 736.62   
        Q_max, Q_min, memoria = zapata.calculo_esfuerzo_actuante_sobre_suelo(Fx_c, Fy_c, Fz_c)
        #print(memoria)
        self.assertAlmostEqual(Q_min, 139.44, places =2)
        self.assertAlmostEqual(Q_max, 288.49, places =2)

    def test_calculo_esfuerzo_actuante_sobre_suelo5(self):
        zapata = copy.deepcopy(self.zapata_4)
        
        Fx_c = 93.73
        Fy_c = 88.62
        Fz_c = 661.62   
        Q_max, Q_min, memoria = zapata.calculo_esfuerzo_actuante_sobre_suelo(Fx_c, Fy_c, Fz_c)
        #print(memoria)
        self.assertAlmostEqual(Q_min, 113.25, places =2)
        self.assertAlmostEqual(Q_max, 277.19, places =2)

    def test_calculo_esfuerzo_actuante_sobre_suelo6(self):
        zapata = copy.deepcopy(self.zapata_7)
        
        Fx_c = 312.3
        Fy_c = 302.1
        Fz_c = 1441.77   
        Q_max, Q_min, memoria = zapata.calculo_esfuerzo_actuante_sobre_suelo(Fx_c, Fy_c, Fz_c)
        #print(memoria)
        self.assertAlmostEqual(Q_min, 50.44, places =2)
        self.assertAlmostEqual(Q_max, 104.15, places =2)

    def test_calculo_esfuerzo_actuante_sobre_suelo7(self):
        zapata = copy.deepcopy(self.zapata_1)
        
        Fx_c = 209.57
        Fy_c = 203.94
        Fz_c = 1153.71   
        Q_max, Q_min, memoria = zapata.calculo_esfuerzo_actuante_sobre_suelo(Fx_c, Fy_c, Fz_c)
        #print(memoria)
        self.assertAlmostEqual(Q_min, 26.39, places =2)
        self.assertAlmostEqual(Q_max, 121.66, places =2)
    
    def test_calculo_esfuerzo_actuante_sobre_suelo8(self):
        zapata = copy.deepcopy(self.zapata_3)
        
        Fx_c = 77.12
        Fy_c = 66.99
        Fz_c = 552.75  
        Q_max, Q_min, memoria = zapata.calculo_esfuerzo_actuante_sobre_suelo(Fx_c, Fy_c, Fz_c)
        print(memoria)
        self.assertAlmostEqual(Q_min, 33.38, places =2)
        self.assertAlmostEqual(Q_max, 66.59, places =2)

    def test_calculo_esfuerzo_actuante_sobre_suelo9(self):
        zapata = copy.deepcopy(self.zapata_4)
        
        Fx_c = 95.4
        Fy_c = 100.2
        Fz_c = 1000  
        Q_max, Q_min, memoria = zapata.calculo_esfuerzo_actuante_sobre_suelo(Fx_c, Fy_c, Fz_c)
        #print(memoria)
        self.assertAlmostEqual(Q_min, 272.07, places =2)
        self.assertAlmostEqual(Q_max, 287.55, places =2)

    def test_calculo_esfuerzo_actuante_sobre_suelo_10(self):
        zapata = copy.deepcopy(self.zapata_4)
        
        Fx_c = 350.85
        Fy_c = 400.24
        Fz_c = 500
        Q_max, Q_min, memoria = zapata.calculo_esfuerzo_actuante_sobre_suelo(Fx_c, Fy_c, Fz_c)
        print(memoria)
        self.assertAlmostEqual(Q_min, 14591.02, places =2)
        self.assertAlmostEqual(Q_max, 16692.75, places =2)
    
    def test_calculo_esfuerzo_actuante_sobre_suelo_11(self):
        zapata = copy.deepcopy(self.zapata_4)
        
        Fx_c = 433.85
        Fy_c = 420.24
        Fz_c = 2005.41 
        Q_max, Q_min, memoria = zapata.calculo_esfuerzo_actuante_sobre_suelo(Fx_c, Fy_c, Fz_c)
        print(memoria)
        self.assertAlmostEqual(Q_min, -203.26, places =2)
        self.assertAlmostEqual(Q_max, 1265.59, places =2)


    def test_calculo_asentamiento_por_consolidacion(self):
        
        zapata = copy.deepcopy(self.zapata_8)
        zapata.B = 2
        zapata.L = 2
        zapata.D = 1.9
        zapata.C = 1.75
        zapata.θ = 6.9617521
        zapata.ajustar_perfil()

        F_zc = 1550

        S_c, memoria = zapata.calculo_asentamiento_por_consolidacion(F_zc)
        print(memoria)
        self.assertAlmostEqual(S_c, 0.01245, places =4)

    def test_calculo_asentamiento_por_consolidacion2(self):
        
        zapata = copy.deepcopy(self.zapata_8)
        
        F_zc = 1400

        S_c, memoria = zapata.calculo_asentamiento_por_consolidacion(F_zc)
        #print(memoria)
        self.assertAlmostEqual(S_c, 0.040154, places =5)

    def test_calculo_asentamiento_por_consolidacion3(self):
        
        zapata = copy.deepcopy(self.zapata_8)
        
        F_zc = 500

        S_c, memoria = zapata.calculo_asentamiento_por_consolidacion(F_zc)
        #print(memoria)
        self.assertAlmostEqual(S_c, 0.040154, places =5)

    def test_calculo_asentamiento_por_consolidacion4(self):
        
        zapata = copy.deepcopy(self.zapata_8)
        
        F_zc = 900

        S_c, memoria = zapata.calculo_asentamiento_por_consolidacion(F_zc)
        #print(memoria)
        self.assertAlmostEqual(S_c, 0.04015, places =5)

    def test_calculo_asentamiento_por_consolidacion5(self):
        
        zapata = copy.deepcopy(self.zapata_8)
        
        F_zc = 250

        S_c, memoria = zapata.calculo_asentamiento_por_consolidacion(F_zc)
        #print(memoria)
        self.assertAlmostEqual(S_c, 0.0401548, places =5)

    def test_calculo_asentamiento_por_consolidacion6(self):
        
        zapata = copy.deepcopy(self.zapata_8)
        
        F_zc = 400

        S_c, memoria = zapata.calculo_asentamiento_por_consolidacion(F_zc)
        #print(memoria)
        self.assertAlmostEqual(S_c, 0.0401548, places =5)

    def test_calculo_asentamiento_por_consolidacion7(self):
        
        zapata = copy.deepcopy(self.zapata_8)
        
        F_zc = 1000

        S_c, memoria = zapata.calculo_asentamiento_por_consolidacion(F_zc)
        #print(memoria)
        self.assertAlmostEqual(S_c, 0.0401548, places =5)

    def test_calculo_asentamiento_por_consolidacion8(self):
        
        zapata = copy.deepcopy(self.zapata_8)
        zapata.D = 0.5
        zapata.C = 1
        F_zc = 2000

        S_c, memoria = zapata.calculo_asentamiento_por_consolidacion(F_zc)
        #print(memoria)
        self.assertAlmostEqual(S_c, 0.040154, places =5)

    def test_calculo_asentamiento_por_consolidacion9(self):
        
        zapata = copy.deepcopy(self.zapata_10)
        zapata.D = 4.5
        zapata.C = 4.6
        F_zc = 198.48

        S_c, memoria = zapata.calculo_asentamiento_por_consolidacion(F_zc)
        print(memoria)
        self.assertAlmostEqual(S_c, 0.04641, places =5)

    def test_calculo_asentamiento_por_consolidacion_10(self):
        
        zapata = copy.deepcopy(self.zapata_10)
        zapata.D = 3.5
        zapata.C = 3.6
        F_zc = 198.48

        S_c, memoria = zapata.calculo_asentamiento_por_consolidacion(F_zc)
        print(memoria)
        self.assertAlmostEqual(S_c, 0.05220, places =5)

    def test_calculo_asentamiento_por_consolidacion_11(self):
        
        zapata = copy.deepcopy(self.zapata_10)
        zapata.D = 5.2
        zapata.C = 5.3
        F_zc = 198.48

        S_c, memoria = zapata.calculo_asentamiento_por_consolidacion(F_zc)
        print(memoria)
        self.assertAlmostEqual(S_c, 0.05170, places =5)

    def test_calculo_asentamiento_por_consolidacion_12(self):
        
        zapata = copy.deepcopy(self.zapata_10)
        zapata.D = 5.5
        zapata.C = 5.6
        F_zc = 198.48

        S_c, memoria = zapata.calculo_asentamiento_por_consolidacion(F_zc)
        print(memoria)
        self.assertAlmostEqual(S_c, 0.05258, places =5)

    def test_calculo_asentamiento_elastico_suelos_granulares(self):
        
        zapata = copy.deepcopy(self.zapata_6)
        
        zapata.B = 3.5
        zapata.L = 3.5
        zapata.D = 1.5
        zapata.H = 0.3
        zapata.C = 0.8
        zapata.TP = 0.4
        zapata.θ = 0
        zapata.γ_c = 23.53
        zapata.set_perfil(Perfil([
            Estrato(H_0 = 2, γ_s = 9.4, E_s = 7000, c_u = None, φ_s = 22, saturado = False, tipo_mat="g"),
            Estrato(H_0 = 2, γ_s = 9.4, E_s = 17500, c_u = None, φ_s = 23, saturado = False, tipo_mat="g"),
        ]))
        zapata.γ_r = 9.4
        zapata.ajustar_perfil()

        k = 4
        t = 20
        F_zc = 1800.14021
        S, memoria = zapata.calculo_asentamiento_elastico_suelos_granulares(k, F_zc, t)
        #print(memoria)
        self.assertAlmostEqual(S, 0.0291974, places=7)

    def test_calculo_asentamiento_elastico_suelos_granulares2(self):
        
        zapata = copy.deepcopy(self.zapata_6)
        
        k = 6
        t = 50
        F_zc = 2224.14021
        S, memoria = zapata.calculo_asentamiento_elastico_suelos_granulares(k, F_zc, t)
        #print(memoria)
        self.assertAlmostEqual(S, 0.011692, places=6)

    def test_calculo_asentamiento_elastico_suelos_granulares3(self):
        
        zapata = copy.deepcopy(self.zapata_6)
        zapata.D = 1.5
        k = 6
        t = 50
        F_zc = 2224.14021
        S, memoria = zapata.calculo_asentamiento_elastico_suelos_granulares(k, F_zc, t)
        #print(memoria)
        self.assertAlmostEqual(S, 0.012227, places=6)

    def test_calculo_asentamiento_elastico_suelos_granulares4(self):
        
        zapata = copy.deepcopy(self.zapata_6)
        zapata.D = 1.5
        zapata.B = 3
        zapata.L = 3
        zapata.ajustar_perfil()
        k = 6
        t = 50
        F_zc = 2224.14021
        S, memoria = zapata.calculo_asentamiento_elastico_suelos_granulares(k, F_zc, t)
        #print(memoria)
        self.assertAlmostEqual(S, 0.018565, places=6)

    def test_calculo_asentamiento_elastico_suelos_granulares5(self):
        
        zapata = copy.deepcopy(self.zapata_6)
        zapata.D = 1.5
        zapata.B = 3
        zapata.L = 3
        zapata.ajustar_perfil()
        k = 6
        t = 50
        F_zc = 1500.30
        S, memoria = zapata.calculo_asentamiento_elastico_suelos_granulares(k, F_zc, t)
        #print(memoria)
        self.assertAlmostEqual(S, 0.0128710, places=6)

    def test_calculo_asentamiento_elastico_suelos_granulares6(self):
        
        zapata = copy.deepcopy(self.zapata_6)
        
        zapata.B = 3
        zapata.L = 3
        zapata.D = 1.7
        zapata.H = 0.5
        zapata.C = 1.7
        zapata.TP = 0.4
        zapata.θ = 0
        zapata.γ_c = 23.53
        zapata.set_perfil(Perfil([
            Estrato(H_0 = 2, γ_s = 9.4, E_s = 7000, c_u = None, φ_s = 25, saturado = False, tipo_mat="g"),
            Estrato(H_0 = 2, γ_s = 9.4, E_s = 17500, c_u = None, φ_s = 31, saturado = False, tipo_mat="g"),
        ]))
        zapata.γ_r = 16
        zapata.ajustar_perfil()

        k = 80
        t = 30
        F_zc = 1800.14021
        S, memoria = zapata.calculo_asentamiento_elastico_suelos_granulares(k, F_zc, t)
        #print(memoria)
        self.assertAlmostEqual(S, 0.03495, places=5)

    def test_calculo_asentamiento_elastico_suelos_granulares7(self):
        zapata = copy.deepcopy(self.zapata_7)
        zapata.B = 3.5
        zapata.L = 3.5
        zapata.D = 1.5
        zapata.H = 0.3
        zapata.C = 1.3
        zapata.TP = 0.4
        zapata.θ = 8
        zapata.γ_c = 23.53
        zapata.γ_r = 15
        zapata.set_perfil(Perfil([
            Estrato(H_0 = 5, γ_s = 9.4, E_s = 7000, c_u = None, φ_s = 29, saturado = False, tipo_mat="g", ν=0.5),
            Estrato(H_0 = 5, γ_s = 9.4, E_s = 17500, c_u = None, φ_s = 34, saturado = False, tipo_mat="g", ν=0.5),
        ],γ_r=16.4))
        zapata.ajustar_perfil()
        
        k = 80
        t = 30
        F_zc = 1500
        
        S, memoria = zapata.calculo_asentamiento_elastico_suelos_granulares(k, F_zc, t)
        #print(memoria)
        self.assertAlmostEqual(S, 0.05107, places=4)

    def test_calculo_asentamiento_elastico_suelos_cohesivos(self):
        zapata = copy.deepcopy(self.zapata_7)
        zapata.B = 3.5
        zapata.L = 3.5
        zapata.D = 1.5
        zapata.H = 0.3
        zapata.C = 1.3
        zapata.TP = 0.4
        zapata.θ = 8
        zapata.γ_c = 23.53
        zapata.set_perfil(Perfil([
            Estrato(H_0 = 5, γ_s = 9.4, E_s = 7000, c_u = 20.3, φ_s = 21, saturado =False, tipo_mat="c", ν=0.5,C_s = 1,e_0 = 1.91, σ_pp = 90),
            Estrato(H_0 = 5, γ_s = 9.4, E_s = 17500, c_u = 32.4, φ_s = 20, saturado = False, tipo_mat="c", ν=0.5, C_s = 1,e_0 = 1.91, σ_pp = 90),
        ],γ_r=16.4))
        zapata.ajustar_perfil()
        
        F_zc = 1500
        
        S, memoria = zapata.calculo_asentamiento_elastico_suelos_cohesivos(F_zc)
        #print(memoria)
        self.assertAlmostEqual(S, 0.0087, places=4)

    def test_calculo_asentamiento_elastico_suelos_cohesivos2(self):
        zapata = copy.deepcopy(self.zapata_7)
                
        F_zc = 500
        
        S, memoria = zapata.calculo_asentamiento_elastico_suelos_cohesivos(F_zc)
        #print(memoria)
        self.assertAlmostEqual(S, 0.00218, places=4)

    def test_calculo_asentamiento_elastico_suelos_cohesivos3(self):
        zapata = copy.deepcopy(self.zapata_7)
                
        F_zc = 650
        
        S, memoria = zapata.calculo_asentamiento_elastico_suelos_cohesivos(F_zc)
        #print(memoria)
        self.assertAlmostEqual(S, 0.00248, places=5)

    def test_calculo_asentamiento_elastico_suelos_cohesivos4(self):
        zapata = copy.deepcopy(self.zapata_7)
        zapata.B = 4
        zapata.L = 4
        zapata.ajustar_perfil()

        F_zc = 650
        
        S, memoria = zapata.calculo_asentamiento_elastico_suelos_cohesivos(F_zc)
        #print(memoria)
        self.assertAlmostEqual(S, 0.00325, places=5)

    def test_calculo_asentamiento_elastico_suelos_cohesivos5(self):
        zapata = copy.deepcopy(self.zapata_7)
        zapata.B = 3
        zapata.L = 3

        F_zc = 650
        
        S, memoria = zapata.calculo_asentamiento_elastico_suelos_cohesivos(F_zc)
        #print(memoria)
        self.assertAlmostEqual(S, 0.00484, places=5)

    def test_calculo_asentamiento_elastico_suelos_cohesivos6(self):
        zapata = copy.deepcopy(self.zapata_7)
        zapata.B = 3
        zapata.L = 3
        zapata.D = 1.5
        zapata.ajustar_perfil()

        F_zc = 650
        
        S, memoria = zapata.calculo_asentamiento_elastico_suelos_cohesivos(F_zc)
        #print(memoria)
        self.assertAlmostEqual(S, 0.00353, places=5)


    def test_asentamiento_incremental_granular(self):

        zapata = copy.deepcopy(self.zapata_1)
        C_1 = 0.93282668
        C_2 = 1.520412
        q_0 = 227.14641322
        estrato = Estrato(H_0=0.8, γ_s=15.0, E_s=15000, c_u=None, φ_s=25, saturado=False, tipo_mat="g",ν=0.45)
        H = 1.5
        k = 80
        S = zapata.asentamiento_incremental_granular(H, estrato, q_0, C_1, C_2, k)
        
        self.assertAlmostEqual(S, 0.005798, places =5)

    def test_asentamiento_incremental_granular2(self):

        zapata = copy.deepcopy(self.zapata_1)
        C_1 = 0.93282668
        C_2 = 1.520412
        q_0 = 227.14641322
        estrato = Estrato(H_0=0.8, γ_s=15.0, E_s=15000, c_u=None, φ_s=26, saturado=False, tipo_mat="g",ν=0.45)
        H = 0.7
        k = 80
        S = zapata.asentamiento_incremental_granular(H, estrato, q_0, C_1, C_2, k)
        
        self.assertAlmostEqual(S, 0.0012628, places =4)
    
    def test_asentamiento_incremental_granular3(self):

        zapata = copy.deepcopy(self.zapata_1)
        C_1 = 0.93282668
        C_2 = 1.520412
        q_0 = 227.14641322
        estrato = Estrato(H_0=0.8, γ_s=15.0, E_s=15000, c_u=None, φ_s=31, saturado=False, tipo_mat="g",ν=0.45)
        H = 1.5
        k = 80
        S1 = zapata.asentamiento_incremental_granular(H, estrato, q_0, C_1, C_2, k)
        H = 0.7
        S2 = zapata.asentamiento_incremental_granular(H, estrato, q_0, C_1, C_2, k)
        
        self.assertAlmostEqual(S1, 0.005798, places =5)
        self.assertAlmostEqual(S2, 0.001262, places =5)

    def test_calculo_asentamiento_elastico_suelos_mixtos(self):
        
        zapata = copy.deepcopy(self.zapata_8)
        zapata.B = 3
        zapata.L = 3
        zapata.D = 1.5
        zapata.C = 2
        TP = 0.6
        zapata.θ = 8
        zapata.γ_c = 23.53
        γ_r, φ_r = 16, 23
        zapata.set_perfil(Perfil([
            Estrato(H_0=1.0, γ_s=20.0, E_s=6100, c_u=None, φ_s=35, saturado=False, tipo_mat="g",ν=0.3),
            Estrato(H_0=1.2, γ_s=21.0, E_s=8500, c_u=23, φ_s=38, saturado=False, tipo_mat="c",ν=0.4,C_s = 0.002,e_0 = 1.91, σ_pp = 90),
            Estrato(H_0=0.8, γ_s=15.0, E_s=15000, c_u=None, φ_s=25, saturado=False, tipo_mat="g",ν=0.45),
            Estrato(H_0=1.1, γ_s=12.0, E_s=12000, c_u=24, φ_s=25, saturado=False, tipo_mat="c",ν=0.4, C_s = 0.002,e_0 = 1.91, σ_pp = 90),
            Estrato(H_0=1.5, γ_s=15.0, E_s=8000, c_u=None, φ_s=31, saturado=True, tipo_mat="g",ν=0.35),
            
        ], γ_r=γ_r, φ_r=φ_r))
        zapata.ajustar_perfil()
        t = 40
        k = 80
        F_zc = 1800

        S, memoria = zapata.calculo_asentamiento_elastico_suelos_mixtos(F_zc, k, t)
        print(memoria)
        self.assertAlmostEqual(memoria["iteraciones"][1]["S_e"], 0.0095, places =4)

    def test_calculo_asentamiento_elastico_suelos_mixtos2(self):
        
        zapata = copy.deepcopy(self.zapata_8)
        zapata.B = 3
        zapata.L = 3
        zapata.D = 1.5
        zapata.C = 2
        TP = 0.6
        zapata.θ = 8
        zapata.γ_c = 23.53
        γ_r, φ_r = 16, 23
        zapata.set_perfil(Perfil([
            Estrato(H_0=1.0, γ_s=20.0, E_s=6100, c_u=None, φ_s=35, saturado=False, tipo_mat="g",ν=0.3),
            Estrato(H_0=1.2, γ_s=21.0, E_s=8500, c_u=23, φ_s=38, saturado=False, tipo_mat="c",ν=0.4, C_s = 0.002,e_0 = 1.91, σ_pp = 90),
            Estrato(H_0=0.8, γ_s=15.0, E_s=15000, c_u=None, φ_s=31, saturado=False, tipo_mat="g",ν=0.45),
            Estrato(H_0=1.1, γ_s=12.0, E_s=12000, c_u=24, φ_s=28, saturado=False, tipo_mat="c",ν=0.4, C_s = 0.002,e_0 = 1.91, σ_pp = 90),
            Estrato(H_0=1.5, γ_s=15.0, E_s=22000, c_u=None, φ_s=31, saturado=True, tipo_mat="g",ν=0.35),
        ], γ_r=γ_r, φ_r=φ_r))
        zapata.ajustar_perfil()
        t = 40
        k = 80
        F_zc = 2000

        S, memoria = zapata.calculo_asentamiento_elastico_suelos_mixtos(F_zc, k, t)
        #print(memoria)
        self.assertAlmostEqual(S, 0.02613, places =4)

    def test_calculo_asentamiento_elastico_suelos_mixtos3(self):
        
        zapata = copy.deepcopy(self.zapata_8)
        zapata.B = 2.8
        zapata.L = 2.8
        zapata.D = 1.5
        zapata.C = 2
        TP = 0.6
        zapata.θ = 8
        zapata.γ_c = 23.53
        γ_r, φ_r = 16, 23
        zapata.set_perfil(Perfil([
            Estrato(H_0=1.0, γ_s=20.0, E_s=6100, c_u=None, φ_s=35, saturado=False, tipo_mat="g",ν=0.3),
            Estrato(H_0=1.2, γ_s=21.0, E_s=10500, c_u=23, φ_s=38, saturado=False, tipo_mat="c",ν=0.4, C_s = 0.002,e_0 = 1.91, σ_pp = 90),
            Estrato(H_0=0.8, γ_s=15.0, E_s=13000, c_u=None, φ_s=32, saturado=False, tipo_mat="g",ν=0.45),
            Estrato(H_0=1.1, γ_s=12.0, E_s=11000, c_u=24, φ_s=24, saturado=False, tipo_mat="c",ν=0.4, C_s = 0.002,e_0 = 1.91, σ_pp = 90),
            Estrato(H_0=1.5, γ_s=15.0, E_s=22000, c_u=None, φ_s=31, saturado=True, tipo_mat="g",ν=0.35),
            
        ], γ_r=γ_r, φ_r=φ_r))
        zapata.ajustar_perfil()
        t = 40
        k = 80
        F_zc = 2000

        S, memoria = zapata.calculo_asentamiento_elastico_suelos_mixtos(F_zc, k, t)
        #print(memoria)
        self.assertAlmostEqual(S, 0.0295, places =4)

    def test_calculo_asentamiento_elastico_suelos_mixtos4(self):
        
        zapata = copy.deepcopy(self.zapata_8)
        zapata.B = 2.5
        zapata.L = 2.5
        zapata.D = 1.5
        zapata.C = 2
        TP = 0.6
        zapata.θ = 8
        zapata.γ_c = 23.53
        γ_r, φ_r = 16, 23
        zapata.set_perfil(Perfil([
            Estrato(H_0=1.0, γ_s=20.0, E_s=16100, c_u=None, φ_s=35, saturado=False, tipo_mat="g",ν=0.3),
            Estrato(H_0=1.5, γ_s=21.0, E_s=21500, c_u=23, φ_s=38, saturado=False, tipo_mat="c",ν=0.4, C_s = 0.002,e_0 = 1.91, σ_pp = 90),
            Estrato(H_0=0.8, γ_s=15.0, E_s=15000, c_u=None, φ_s=19, saturado=False, tipo_mat="g",ν=0.45),
            Estrato(H_0=1.6, γ_s=12.0, E_s=17000, c_u=24, φ_s=25, saturado=False, tipo_mat="c",ν=0.4, C_s = 0.002,e_0 = 1.91, σ_pp = 90),
            Estrato(H_0=1.5, γ_s=15.0, E_s=25000, c_u=None, φ_s=31, saturado=True, tipo_mat="g",ν=0.35),
            
        ], γ_r=γ_r, φ_r=φ_r))
        zapata.ajustar_perfil()
        t = 40
        k = 80
        F_zc = 2000

        S, memoria = zapata.calculo_asentamiento_elastico_suelos_mixtos(F_zc, k, t)
        #print(memoria)
        self.assertAlmostEqual(S, 0.02503, places =4)

    def test_calculo_asentamiento_elastico_suelos_mixtos5(self):
        
        zapata = copy.deepcopy(self.zapata_8)
        zapata.B = 2.5
        zapata.L = 2.5
        zapata.D = 1.5
        zapata.C = 2
        γ_r, φ_r = 16, 23
        zapata.set_perfil(Perfil([
            Estrato(H_0=1.0, γ_s=20.0, E_s=16100, c_u=None, φ_s=35, saturado=False, tipo_mat="g",ν=0.3),
            Estrato(H_0=1.5, γ_s=21.0, E_s=21500, c_u=23, φ_s=38, saturado=False, tipo_mat="c",ν=0.4, C_s = 0.002,e_0 = 1.91, σ_pp = 90),
            Estrato(H_0=0.8, γ_s=15.0, E_s=15000, c_u=None, φ_s=36, saturado=False, tipo_mat="g",ν=0.45),
            Estrato(H_0=1.6, γ_s=12.0, E_s=17000, c_u=24, φ_s=31, saturado=False, tipo_mat="c",ν=0.4, C_s = 0.002,e_0 = 1.91, σ_pp = 90),
            Estrato(H_0=1.5, γ_s=15.0, E_s=25000, c_u=None, φ_s=31, saturado=True, tipo_mat="g",ν=0.35),
            
        ], γ_r=γ_r, φ_r=φ_r))
        zapata.ajustar_perfil()
        t = 45
        k = 100
        F_zc = 2000

        S, memoria = zapata.calculo_asentamiento_elastico_suelos_mixtos(F_zc, k, t)
        #print(memoria)
        self.assertAlmostEqual(S, 0.02516, places =4)
        
    def test_calculo_volcamiento(self):
        
        zapata = copy.deepcopy(self.zapata_5)
        zapata.B = 4
        zapata.L = 4
        zapata.ajustar_perfil()

        F_zc =  275.23
        F = 39.3
        T_u = 900

        Mv, Me, memoria = zapata.calculo_volcamiento(F_zc, F, T_u)
        #print(memoria)
        self.assertAlmostEqual(Mv, 567.41789 , places=2)
        self.assertAlmostEqual(Me, 1800 , places=2)

    def test_calculo_volcamiento2(self):
        
        zapata = copy.deepcopy(self.zapata_5)
        zapata.B = 3
        zapata.L = 3

        zapata.ajustar_perfil()
                
        F_zc =  275.23
        F = 39.3
        T_u = 700

        Mv, Me, memoria = zapata.calculo_volcamiento(F_zc, F, T_u)
        #print(memoria)
        self.assertAlmostEqual(Mv, 429.80289 , places=2)
        self.assertAlmostEqual(Me, 1050 , places=2)

    def test_calculo_volcamiento3(self):
        
        zapata = copy.deepcopy(self.zapata_5)
        zapata.B = 3
        zapata.L = 3
        zapata.D = 2

        zapata.ajustar_perfil()
                
        F_zc =  324.85
        F = 55.08
        T_u = 700

        Mv, Me, memoria = zapata.calculo_volcamiento(F_zc, F, T_u)
        #print(memoria)
        self.assertAlmostEqual(Mv, 555.70 , places=2)
        self.assertAlmostEqual(Me, 1050 , places=2)

    def test_calculo_volcamiento4(self):
        
        zapata = copy.deepcopy(self.zapata_5)
        zapata.B = 2.5
        zapata.L = 2.5
        zapata.D = 2

        zapata.ajustar_perfil()
                
        F_zc =  324.85
        F = 55.08
        T_u = 700

        Mv, Me, memoria = zapata.calculo_volcamiento(F_zc, F, T_u)
        #print(memoria)
        self.assertAlmostEqual(Mv, 474.49 , places=2)
        self.assertAlmostEqual(Me, 875 , places=2)

    def test_calculo_volcamiento5(self):
        
        zapata = copy.deepcopy(self.zapata_5)
        zapata.B = 2
        zapata.L = 2
        zapata.D = 2

        zapata.ajustar_perfil()
                
        F_zc =  324.85
        F = 55.08
        T_u = 850

        Mv, Me, memoria = zapata.calculo_volcamiento(F_zc, F, T_u)
        #print(memoria)
        self.assertAlmostEqual(Mv, 393.27 , places=2)
        self.assertAlmostEqual(Me, 850 , places=2)

    def test_calculo_momento_carga_lateral(self):
        zapata = copy.deepcopy(self.zapata_4)
        zapata.D = 1.9
        γ_r, φ_r = 16, 23
        zapata.set_perfil(Perfil([
            Estrato(H_0 = 1.0, γ_s = 19.5, E_s = 6000, c_u = None, φ_s = 38, saturado = False, tipo_mat = 'g'),
            Estrato(H_0 = 1.0, γ_s = 19.5, E_s = 6000, c_u = None, φ_s = 38, saturado = False, tipo_mat = 'g'),
            Estrato(H_0 = 1.0, γ_s = 19.5, E_s = 6000, c_u = None, φ_s = 38, saturado = False, tipo_mat = 'g'),
            Estrato(H_0 = 1.0, γ_s = 19.5, E_s = 6000, c_u = None, φ_s = 38, saturado = False, tipo_mat = 'g'),
        ], γ_r=γ_r, φ_r=φ_r))

        F_c = 39.3
        Fz_c = 275.23   
        
        M_o, memoria = zapata.calculo_momento_carga_lateral(F_c)
        #print(memoria)
        self.assertAlmostEqual(M_o, 72.60, places =2)

    def test_calculo_momento_carga_axial(self):
        zapata = copy.deepcopy(self.zapata_4)
        zapata.D = 1.9
        γ_r, φ_r = 16.4, 23
        zapata.set_perfil(Perfil([
            Estrato(H_0 = 1.0, γ_s = 19.5, E_s = 6000, c_u = None, φ_s = 38, saturado = False, tipo_mat = 'g'),
            Estrato(H_0 = 1.0, γ_s = 19.5, E_s = 6000, c_u = None, φ_s = 38, saturado = False, tipo_mat = 'g'),
            Estrato(H_0 = 1.0, γ_s = 19.5, E_s = 6000, c_u = None, φ_s = 38, saturado = False, tipo_mat = 'g'),
            Estrato(H_0 = 1.0, γ_s = 19.5, E_s = 6000, c_u = None, φ_s = 38, saturado = False, tipo_mat = 'g'),
        ], γ_r=γ_r, φ_r=φ_r))

        F_c = 39.3
        Fz_c = 275.23   
        
        M_o = zapata.calculo_momento_carga_axial(Fz_c)
        
        self.assertAlmostEqual(M_o, -72.26, places =2)

    def test_calculo_momento_carga_lateral2(self):
        zapata = copy.deepcopy(self.zapata_4)
        zapata.B = 5
        zapata.L = 5
        zapata.C =2
        zapata.φ_r = 23
        γ_r, φ_r = 16, 23
        zapata.set_perfil(Perfil([
            Estrato(H_0 = 1.0, γ_s = 19.5, E_s = 6000, c_u = None, φ_s = 38, saturado = False, tipo_mat = 'g'),
            Estrato(H_0 = 1.0, γ_s = 19.5, E_s = 6000, c_u = None, φ_s = 38, saturado = False, tipo_mat = 'g'),
            Estrato(H_0 = 1.0, γ_s = 19.5, E_s = 6000, c_u = None, φ_s = 38, saturado = False, tipo_mat = 'g'),
            Estrato(H_0 = 1.0, γ_s = 19.5, E_s = 6000, c_u = None, φ_s = 38, saturado = False, tipo_mat = 'g'),
        ], γ_r=γ_r, φ_r=φ_r))
        zapata.ajustar_perfil()

        F_c = 39.3
        Fz_c = 251.34   
        
        M_o, memoria = zapata.calculo_momento_carga_lateral(F_c)
        #print(memoria)
        self.assertAlmostEqual(M_o, 64.66, places =2)

    def test_calculo_momento_carga_axial2(self):
        zapata = copy.deepcopy(self.zapata_4)
        zapata.B = 5
        zapata.L = 5
        zapata.C =2
        zapata.φ_r = 23
        γ_r, φ_r = 16.4, 23
        zapata.set_perfil(Perfil([
            Estrato(H_0 = 1.0, γ_s = 19.5, E_s = 6000, c_u = None, φ_s = 38, saturado = False, tipo_mat = 'g'),
            Estrato(H_0 = 1.0, γ_s = 19.5, E_s = 6000, c_u = None, φ_s = 38, saturado = False, tipo_mat = 'g'),
            Estrato(H_0 = 1.0, γ_s = 19.5, E_s = 6000, c_u = None, φ_s = 38, saturado = False, tipo_mat = 'g'),
            Estrato(H_0 = 1.0, γ_s = 19.5, E_s = 6000, c_u = None, φ_s = 38, saturado = False, tipo_mat = 'g'),
        ], γ_r=γ_r, φ_r=φ_r))
        zapata.ajustar_perfil()

        F_c = 39.3
        Fz_c = 251.34   
        
        M_o = zapata.calculo_momento_carga_axial(Fz_c)
        #print(memoria)
        self.assertAlmostEqual(M_o, -53.71, places =2)

    def test_calculo_momento_carga_lateral3(self):
        zapata = copy.deepcopy(self.zapata_4)
        
        F_c = 39.3
        Fz_c = 275.23   
        
        M_o, memoria = zapata.calculo_momento_carga_lateral(F_c)
        print(memoria)
        self.assertAlmostEqual(M_o, 61.46, places =2)

    def test_calculo_momento_carga_axial3(self):
        zapata = copy.deepcopy(self.zapata_4)
        
        F_c = 39.3
        Fz_c = 275.23   
        
        M_o = zapata.calculo_momento_carga_axial(Fz_c)
        self.assertAlmostEqual(M_o, -58.81, places =2)

    def test_calculo_momento_carga_lateral4(self):
        zapata = copy.deepcopy(self.zapata_4)
        
        F_c = 45.32
        Fz_c = 320.23   
        
        M_o, memoria = zapata.calculo_momento_carga_lateral(F_c)
        #print(memoria)
        self.assertAlmostEqual(M_o, 72.92, places =2)

    def test_calculo_momento_carga_axial4(self):
        zapata = copy.deepcopy(self.zapata_4)
        
        F_c = 45.32
        Fz_c = 320.23   
        
        M_o = zapata.calculo_momento_carga_axial(Fz_c)
        self.assertAlmostEqual(M_o, -68.43, places =2)
    
    def test_calculo_momento_carga_lateral5(self):
        zapata = copy.deepcopy(self.zapata_4)
        
        F_c = 71.42
        Fz_c = 268.58   
        
        M_o, memoria = zapata.calculo_momento_carga_lateral(F_c)
        print(memoria)
        self.assertAlmostEqual(M_o, 124.73, places =2)

    def test_calculo_momento_carga_axial5(self):
        zapata = copy.deepcopy(self.zapata_4)
        
        F_c = 71.42
        Fz_c = 268.58   
        
        M_o = zapata.calculo_momento_carga_axial(Fz_c)
        self.assertAlmostEqual(M_o, -57.39, places =2)

    def test_calculo_momento_carga_lateral6(self):
        zapata = copy.deepcopy(self.zapata_4)
        
        Fx_c = 350.85
        Fy_c = 400.24
        Fz_c = 500.56  
        F_c = Fx_c
        M_o, memoria = zapata.calculo_momento_carga_lateral(F_c)
        print(memoria)
        self.assertAlmostEqual(M_o, 725.14, places =2)

    def test_calculo_momento_carga_lateral7(self):
        zapata = copy.deepcopy(self.zapata_4)
        
        Fx_c = 433.85
        Fy_c = 420.24
        Fz_c = 2005.41  
        F_c = Fx_c
        M_o, memoria = zapata.calculo_momento_carga_lateral(F_c)
        print(memoria)
        self.assertAlmostEqual(M_o, 903.59, places =2)

    def test_calculo_momento_carga_lateral8(self):
        zapata = copy.deepcopy(self.zapata_4)
        
        Fx_c = 14.45
        Fy_c = 13.22
        Fz_c = 300.23  
        F_c = Fx_c
        M_o, memoria = zapata.calculo_momento_carga_lateral(F_c)
        print(memoria)
        self.assertAlmostEqual(M_o, 16.457, places =2)

    def test_calculo_integral_presion_lateral_activa_desde_0_prueba_1(self):
        
        zapata = copy.deepcopy(self.zapata_1)
        zapata.perfil = self.perfil10

        prof = 1.5
        prueba = zapata.calculo_integral_presion_lateral_activa_desde_0(prof)
        self.assertAlmostEqual(prueba, 0.0,places=3)

    def test_calculo_integral_presion_lateral_activa_desde_0_prueba_2(self):
        
        zapata = copy.deepcopy(self.zapata_1)
        zapata.perfil = self.perfil11

        prof = 1.5
        prueba = zapata.calculo_integral_presion_lateral_activa_desde_0(prof)
        self.assertAlmostEqual(prueba, 9.878,places=3)

    def test_calculo_integral_presion_lateral_pasiva_desde_0_prueba_1(self):
        
        zapata = copy.deepcopy(self.zapata_1)
        zapata.perfil = self.perfil11

        prof = 1.5
        prueba = zapata.calculo_integral_presion_lateral_pasiva_desde_0(prof)
        self.assertAlmostEqual(prueba, 37.47,places=3)


    # def test_rendimiento(self):
    #     zapata = copy.deepcopy(self.zapata_8)
    #     zapata.B = 2.5
    #     zapata.L = 2.5  
    #     zapata.ajustar_perfil()         
    #     F_zc = 450

    #     start = time.time()
    #     for i in range(800000):
    #         S, memoria = zapata.calculo_asentamiento_elastico_suelos_mixtos(F_zc)
    #     end = time.time()
    #     print(end - start)

if __name__ == '__main__':
    unittest.main()