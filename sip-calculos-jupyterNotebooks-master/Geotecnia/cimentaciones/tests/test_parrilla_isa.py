# pylint: disable=W
import unittest
import time
import copy
from ..parrilla_isa import Parrilla
from ..perfil import Perfil, Estrato

class TestCalculosParillaIsa(unittest.TestCase): 
    
    @classmethod
    def setUpClass(self):
        # Parrilla 1
        B, L, D, H, C = 5, 5, 1.5, 0.4, 2
        TP, θ = 0.6, 0
        γ_r, φ_r = 16.4, 23
        α, ω = 0, 30
        esf_act_diseno = 0
        mv_diseno = 0
        peso = 800
        perfil = Perfil([
            Estrato(H_0 = 1.0, γ_s = 20.0, E_s = 6597, c_u = 0, φ_s = 24, saturado = False, tipo_mat = "g", c_p = 0),
            Estrato(H_0 = 0.5, γ_s = 19.0, E_s = 6597, c_u = 0, φ_s = 24, saturado = True, tipo_mat = "g", c_p = 0),
            Estrato(H_0 = 1.0, γ_s = 21.0, E_s = 6597, c_u = 0, φ_s = 24, saturado = True, tipo_mat = "g", c_p = 0),
            Estrato(H_0 = 2.0, γ_s = 19.0, E_s = 6597, c_u = 0, φ_s = 24, saturado = True, tipo_mat = "g", c_p = 0)
        ], γ_r=γ_r, φ_r=φ_r)
        self.parrilla_1 = Parrilla(B, B, D, H, D, TP, θ, peso, esf_act_diseno, mv_diseno, perfil, α, ω)

        # Parrilla 2
        B, L, D, H, C = 3, 3, 1.8, 0.4, 2
        TP, θ = 0.6, 0
        γ_r, φ_r = 16.4, 35
        α, ω = 0, 30
        esf_act_diseno = 0
        mv_diseno = 0
        peso = 800
        perfil = Perfil([
            Estrato(H_0 = 1.0, γ_s = 20.0, E_s = 6807, c_u = 31.26, φ_s = 35, saturado = False, tipo_mat = "g", c_p = 0),
            Estrato(H_0 = 0.5, γ_s = 19.0, E_s = 6597, c_u = 29.36, φ_s = 27, saturado = True, tipo_mat = "g", c_p = 0),
            Estrato(H_0 = 1.0, γ_s = 21.0, E_s = 6687, c_u = 27.53, φ_s = 23, saturado = True, tipo_mat = "g", c_p = 0),
            Estrato(H_0 = 2.0, γ_s = 19.0, E_s = 6200, c_u = 25.56, φ_s = 21, saturado = True, tipo_mat = "g", c_p = 0),
        ], γ_r=γ_r, φ_r=φ_r)
        self.parrilla_2 = Parrilla(B, B, D, H, D, TP, θ, peso, esf_act_diseno, mv_diseno, perfil, α, ω)

        # Parrilla 3
        B, L, D, H, C = 5, 5, 1.5, 0.4, 2
        TP, θ = 0.6, 0
        γ_r, φ_r = 16.4, 35
        α, ω = 0, 30
        esf_act_diseno = 0
        mv_diseno = 0
        peso = 800
        perfil = Perfil([
            Estrato(H_0 = 1.0, γ_s = 15.0, E_s = 5000, c_u = 24.63, φ_s = 20, saturado = False, tipo_mat = "c", c_p = 0, C_s = 1,e_0 = 1.91, σ_pp = 90),
            Estrato(H_0 = 1.0, γ_s = 15.0, E_s = 5000, c_u = 24.63, φ_s = 20, saturado = False, tipo_mat = "c", c_p = 0, C_s = 1,e_0 = 1.91, σ_pp = 90),
            Estrato(H_0 = 1.5, γ_s = 15.0, E_s = 5000, c_u = 24.63, φ_s = 20, saturado = False, tipo_mat = "c", c_p = 0, C_s = 1,e_0 = 1.91, σ_pp = 90),
        ], γ_r=γ_r, φ_r=φ_r)
        self.parrilla_3 = Parrilla(B, B, D, H, D, TP, θ, peso, esf_act_diseno, mv_diseno, perfil, α, ω)
       

        # Parrilla 4       
        B, L, D, H, C = 2, 2, 1.5, 0.4, 1.75
        TP, θ = 0.6, 6.9617521
        γ_r, φ_r = 16.4, 35
        α, ω = 0, 30
        esf_act_diseno = 0
        mv_diseno = 0
        peso = 800
        perfil = Perfil([
            Estrato(H_0 = 0.5, γ_s = 17.5, E_s = 3500, c_u = 24.63, φ_s = 38, saturado = False, tipo_mat = "c", c_p = 0, C_s = 0.002,e_0 = 1.91, σ_pp = 90),
            Estrato(H_0 = 1.1, γ_s = 21.4, E_s = 4200, c_u = 0.00, φ_s = 32, saturado = True, tipo_mat = "g", c_p = 0),
            Estrato(H_0 = 0.7, γ_s = 23.6, E_s = 5300, c_u = 24.34, φ_s = 30, saturado = True, tipo_mat = "c", c_p = 0, C_s = 0.003,e_0 = 1.91, σ_pp = 90),
            Estrato(H_0 = 1.2, γ_s = 27.2, E_s = 2800, c_u = 0.00, φ_s = 29, saturado = True, tipo_mat = "g", c_p = 0),
            Estrato(H_0 = 1.3, γ_s = 18.3, E_s = 2400, c_u = 25.40, φ_s = 27, saturado = True, tipo_mat = "c", c_p = 4, C_s = 0.004,e_0 = 1.91, σ_pp = 90),
            Estrato(H_0 = 0.9, γ_s = 20.2, E_s = 3600, c_u = 23.52, φ_s = 35, saturado = True, tipo_mat = "g", c_p = 0),
        ], γ_r=γ_r, φ_r=φ_r)
        self.parrilla_4 = Parrilla(B, B, D, H, D, TP, θ, peso, esf_act_diseno, mv_diseno, perfil, α, ω)

        # Parrilla 5
        B, L, D, H, C = 5, 5, 1.5, 0.4, 2
        TP, θ = 0.6, 8
        γ_r, φ_r = 16.4, 35
        α, ω = 0, 30
        esf_act_diseno = 0
        mv_diseno = 0
        peso = 800
        perfil = Perfil([
            Estrato(H_0 = 1.0, γ_s = 19.0, E_s = 5550, c_u = 12.63, φ_s = 22, saturado = False, tipo_mat = "c", c_p = 20.2, C_s = 0.4,e_0 = 1.15, σ_pp = 55),
            Estrato(H_0 = 0.5, γ_s = 24.0, E_s = 5420, c_u = 15.63, φ_s = 18, saturado = True, tipo_mat = "c", c_p = 21.3, C_s = 0.4,e_0 = 1.15, σ_pp = 55),
            Estrato(H_0 = 1.3, γ_s = 25.0, E_s = 4350, c_u = 17.63, φ_s = 15, saturado = True, tipo_mat = "c", c_p = 15.6, C_s = 0.4,e_0 = 1.15, σ_pp = 55),
            Estrato(H_0 = 1.5, γ_s = 26.0, E_s = 6000, c_u = 21.63, φ_s = 19, saturado = True, tipo_mat = "c", c_p = 10.8, C_s = 0.4,e_0 = 1.15, σ_pp = 55),
        ], γ_r=γ_r, φ_r=φ_r)
        self.parrilla_5 = Parrilla(B, B, D, H, D, TP, θ, peso, esf_act_diseno, mv_diseno, perfil, α, ω)

        # Parrilla 6 Roca con granular
        B, L, D, H, C = 5, 5, 1, 0.4, 1.5
        TP, θ = 0.6, 8
        γ_r, φ_r = 16.4, 35
        α, ω = 0, 30
        esf_act_diseno = 0
        mv_diseno = 0
        peso = 800
        perfil = Perfil([
            Estrato(H_0 = 1.0, γ_s = 19.0, E_s = 5550, c_u = 0, φ_s = 34, saturado = False, tipo_mat = "g", c_p = 0),
            Estrato(H_0 = 0.5, γ_s = 24.0, E_s = 5420, c_u = 0, φ_s = 32, saturado = True, tipo_mat = "g", c_p = 0),
            Estrato(H_0 = 1.3, γ_s = 25.0, E_s = 4350, c_u = 0, φ_s = 28, saturado = True, tipo_mat = "g", c_p = 0),
            Estrato(H_0 = 5, γ_s = 26.0, E_s = 115000, c_u = None, φ_s = None, saturado = True, tipo_mat = "r", c_p = None),
        ], γ_r=γ_r, φ_r=φ_r)
        self.parrilla_6 = Parrilla(B, B, D, H, D, TP, θ, peso, esf_act_diseno, mv_diseno, perfil, α, ω)

        # Parrilla 7 Roca con cohesivo
        B, L, D, H, C = 5, 5, 1, 0.4, 1.5
        TP, θ = 0.6, 8
        γ_r, φ_r = 16.4, 35
        α, ω = 0, 30
        esf_act_diseno = 0
        mv_diseno = 0
        peso = 800
        perfil = Perfil([
            Estrato(H_0 = 0.8, γ_s = 19.0, E_s = 5550, c_u = 12.63, φ_s = 23, saturado = False, tipo_mat = "c", ν = 0.3, c_p = 20.1, C_s = 0.004,e_0 = 1.91, σ_pp = 90),
            Estrato(H_0 = 0.7, γ_s = 24.0, E_s = 5420, c_u = 15.63, φ_s = 15, saturado = True, tipo_mat = "c", ν = 0.5, c_p = 18.4, C_s = 0.004,e_0 = 1.91, σ_pp = 90),
            Estrato(H_0 = 1.2, γ_s = 25.0, E_s = 4350, c_u = 17.63, φ_s = 17, saturado = True, tipo_mat = "c", ν = 0.4, c_p = 17.4, C_s = 0.004,e_0 = 1.91, σ_pp = 90),
            Estrato(H_0 = 4.8, γ_s = 26.0, E_s = 110000, c_u = None, φ_s = None, saturado = True, tipo_mat = "r", c_p = None),
        ], γ_r=γ_r, φ_r=φ_r)
        self.parrilla_7 = Parrilla(B, B, D, H, D, TP, θ, peso, esf_act_diseno, mv_diseno, perfil, α, ω)

        # Parrilla 8 Roca con mixto
        B, L, D, H, C = 5, 5, 1, 0.4, 1.5
        TP, θ = 0.6, 8
        γ_r, φ_r = 16.4, 35
        α, ω = 0, 30
        esf_act_diseno = 0
        mv_diseno = 0
        peso = 800
        perfil = Perfil([
            Estrato(H_0 = 0.9, γ_s = 19.0, E_s = 5550, c_u = 12.63, φ_s = 24, saturado = False, tipo_mat = "c", c_p = 20.2, C_c = 0, C_s = 0.5,e_0 = 1.2, σ_pp = 30),
            Estrato(H_0 = 0.5, γ_s = 24.0, E_s = 5420, c_u = 0.00, φ_s = 17, saturado = True, tipo_mat = "g", c_p = 0),
            Estrato(H_0 = 0.8, γ_s = 23.2, E_s = 4350, c_u = 17.63, φ_s = 16, saturado = True, tipo_mat = "c", c_p = 15.6, C_c = 0, C_s = 0.4,e_0 = 1.15, σ_pp = 55),
            Estrato(H_0 = 1.2, γ_s = 25.4, E_s = 4350, c_u = 0.00, φ_s = 15, saturado = True, tipo_mat = "g", c_p = 0),
            Estrato(H_0 = 5.1, γ_s = 26.0, E_s = 100000, c_u = None, φ_s = None, saturado = True, tipo_mat = "r", c_p = 10.8),
        ], γ_r=γ_r, φ_r=φ_r)
        self.parrilla_8 = Parrilla(B, B, D, H, D, TP, θ, peso, esf_act_diseno, mv_diseno, perfil, α, ω)

        # Parrilla 9
        B, L, D, H, C = 2.5, 2.5, 1, 0.4, 2
        TP, θ = 0.6, 8
        γ_r, φ_r = 16.4, 35
        α, ω = 0, 30
        esf_act_diseno = 0
        mv_diseno = 0
        peso = 800
        perfil = Perfil([
            Estrato(H_0 = 0.5, γ_s = 19.0, E_s = 5550, c_u = 12.63, φ_s = 22, saturado = False, tipo_mat = "c", c_p = 20.2, C_s = 1,e_0 = 1.91, σ_pp = 90),
            Estrato(H_0 = 0.5, γ_s = 24.0, E_s = 5420, c_u = 15.63, φ_s = 18, saturado = True, tipo_mat = "c", c_p = 21.3, C_s = 1,e_0 = 1.91, σ_pp = 90),
            Estrato(H_0 = 1.0, γ_s = 25.0, E_s = 4350, c_u = 0.000, φ_s = 15, saturado = True, tipo_mat = "g", c_p = 0),
            Estrato(H_0 = 1.5, γ_s = 26.0, E_s = 6000, c_u = 21.63, φ_s = 19, saturado = True, tipo_mat = "c", c_p = 10.8, C_s = 1,e_0 = 1.91, σ_pp = 90),
        ], γ_r=γ_r, φ_r=φ_r)
        self.parrilla_9 = Parrilla(B, B, D, H, D, TP, θ, peso, esf_act_diseno, mv_diseno, perfil, α, ω)
        
        # Parrilla 10 
        B, L, D, H, C = 2.5, 2.5, 1, 0.4, 2
        TP, θ = 0.6, 8
        γ_r, φ_r = 16.4, 23
        α, ω = 0, 0
        esf_act_diseno = 0
        mv_diseno = 0
        peso = 800
        perfil = Perfil([
            Estrato(H_0 = 4.5, γ_s = 20.099, E_s = 8760, c_u = 55.564, φ_s = 24.89, saturado = True, tipo_mat = "c", ν = 0.3666, c_p = 12.2249,C_c = 0.209, C_s = 0.0715, e_0 = 0.6444, σ_pp = 196.6954),
            Estrato(H_0 = 2.85, γ_s = 21.232, E_s = 8391, c_u = 50.38, φ_s = 25.2, saturado = True, tipo_mat = "c", ν = 0.3647, c_p = 17.684, C_c = 0.1778, C_s = 0.05827,e_0 = 0.4877, σ_pp = 178.3727),
            Estrato(H_0 = 2.65, γ_s = 20.306, E_s = 24587, c_u = None, φ_s = 29.604, saturado = True, tipo_mat = "g", ν = 0.3358, c_p = None, C_c = None,  C_s = None, e_0 = None, σ_pp = None),
        ], γ_r=γ_r, φ_r=φ_r)
        self.parrilla_10 = Parrilla(B, B, D, H, D, TP, θ, peso, esf_act_diseno, mv_diseno, perfil, α, ω)

        # Parrilla 11
        B, L, D, H, C = 2.5, 2.5, 3, 0.4, 2.2
        TP, θ = 0.6, 8
        γ_r, φ_r = 16.4, 23
        α, ω = 0, 0
        esf_act_diseno = 0
        mv_diseno = 0
        peso = 800
        perfil = Perfil([
            Estrato(H_0 = 1.5, γ_s = 20.099, E_s = 8760, c_u = 55.564, φ_s = 24.89, saturado = True, tipo_mat = "c", ν = 0.3666, c_p = 12.2249,C_c = 0.209, C_s = 0.0715, e_0 = 0.6444, σ_pp = 196.6954),
            Estrato(H_0 = 1.7, γ_s = 21.232, E_s = 8391, c_u = 50.38, φ_s = 25.2, saturado = True, tipo_mat = "c", ν = 0.3647, c_p = 17.684, C_c = 0.1778, C_s = 0.05827,e_0 = 0.4877, σ_pp = 178.3727),
        ], γ_r=γ_r, φ_r=φ_r)
        self.parrilla_11 = Parrilla(B, B, D, H, D, TP, θ, peso, esf_act_diseno, mv_diseno, perfil, α, ω)


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
        B, TP, perfil = self.parrilla_1.get_atributos("B", "TP", "perfil")
        self.assertEqual(B, 5)
        self.assertEqual(TP, 0.6)
        self.assertEqual(perfil[1].γ_s, 19.0)

    def test_calculo_capacidad_portante_suelos_granulares(self):
                
        parrilla = self.parrilla_1

        q_ult, memoria = parrilla.calculo_capacidad_portante_isa()
        print(memoria)
        self.assertAlmostEqual(q_ult, 65.37, places=2) #289.11
    
    def test_calculo_capacidad_portante_suelos_granulares2(self):
        
        parrilla = copy.deepcopy(self.parrilla_1)
        parrilla.D = 2

        T =  39.1285
        F_zc = 251.34
        q_ult, memoria = parrilla.calculo_capacidad_portante_isa()
        print(memoria)
        self.assertAlmostEqual(q_ult, 82.35, places=2) #349.69

    def test_calculo_capacidad_portante_suelos_granulares3(self):
        
        parrilla = copy.deepcopy(self.parrilla_1)
        parrilla.D = 2.5

        T =  39.1285
        F_zc = 251.34
        
        q_ult, memoria = parrilla.calculo_capacidad_portante_isa()
        #print(memoria)
        self.assertAlmostEqual(q_ult, 95.15, places=2) #412.92

    def test_calculo_capacidad_portante_suelos_granulares4(self):
        
        parrilla = copy.deepcopy(self.parrilla_1)
        parrilla.D = 3

        T =  39.1285
        F_zc = 251.34

        q_ult, memoria = parrilla.calculo_capacidad_portante_isa()
        #print(memoria)
        self.assertAlmostEqual(q_ult, 101.81, places=2) #470.11

    def test_calculo_capacidad_portante_suelos_granulares5(self):
        parrilla = copy.deepcopy(self.parrilla_1)
        parrilla.B = 1.5
        parrilla.L = 1.5
        parrilla.D = 3
        parrilla.ajustar_perfil()
        
        T =  39.1285
        F_zc = 251.34
        
        q_ult, _ = parrilla.calculo_capacidad_portante_isa()
        self.assertAlmostEqual(q_ult, 101.45, places=2) #404.09

    def test_calculo_capacidad_portante_suelos_granulares6(self):
        parrilla = copy.deepcopy(self.parrilla_1)
        parrilla.B = 1.5
        parrilla.L = 1.5
        parrilla.D = 3
        parrilla.ajustar_perfil()

        T =  39.3
        F_zc = 416.16

        q_ult, _ = parrilla.calculo_capacidad_portante_isa()
        self.assertAlmostEqual(q_ult, 101.45, places=2) #429.82

    def test_calculo_capacidad_portante_suelos_granulares7(self):
        parrilla = copy.deepcopy(self.parrilla_1)
        parrilla.B = 1.5
        parrilla.L = 1.5
        parrilla.D = 1.6
        γ_r, φ_r = 16, 23 
        parrilla.set_perfil(Perfil([
            Estrato(H_0 = 1.0, γ_s = 20.0, E_s = 6400, c_u = 0, φ_s = 32, saturado = False, tipo_mat = "g", c_p = 0),
            Estrato(H_0 = 0.5, γ_s = 19.0, E_s = 7100, c_u = 0, φ_s = 35, saturado = False, tipo_mat = "g", c_p = 0),
            Estrato(H_0 = 1.0, γ_s = 21.0, E_s = 6200, c_u = 0, φ_s = 21, saturado = True, tipo_mat = "g", c_p = 0),
            Estrato(H_0 = 2.0, γ_s = 19.0, E_s = 5900, c_u = 0, φ_s = 25, saturado = True, tipo_mat = "g", c_p = 0),
        ], γ_r=γ_r, φ_r=φ_r))
        parrilla.ajustar_perfil()

        T =  39.3
        F_zc = 416.16

        q_ult, memoria = parrilla.calculo_capacidad_portante_isa()
        print(memoria)
        self.assertAlmostEqual(q_ult, 65.53, places=2) #289.44

    def test_calculo_capacidad_portante_suelos_cohesivos(self):
        parrilla = copy.deepcopy(self.parrilla_1)
        parrilla.θ = 6.9617521
        γ_r, φ_r = 16, 23
        parrilla.set_perfil(Perfil([
            Estrato(H_0 = 1.0, γ_s = 20.0, E_s = 6597, c_u = 29.36, φ_s = 24, saturado = False, tipo_mat="c",C_s = 0.002,e_0 = 1.91, σ_pp = 90),
            Estrato(H_0 = 0.5, γ_s = 19.0, E_s = 6597, c_u = 29.36, φ_s = 24, saturado = False, tipo_mat="g"),
            Estrato(H_0 = 1.0, γ_s = 21.0, E_s = 6597, c_u = 29.36, φ_s = 24, saturado = False, tipo_mat="c",C_s = 0.002,e_0 = 1.91, σ_pp = 90),
            Estrato(H_0 = 2.0, γ_s = 19.0, E_s = 6597, c_u = 29.36, φ_s = 24, saturado = False, tipo_mat="c",C_s = 0.002,e_0 = 1.91, σ_pp = 90),
        ], γ_r=γ_r, φ_r=φ_r))
        parrilla.ω = 0
        
        T = 39.3
        F_zc = 251.34

        q_ult, memoria = parrilla.calculo_capacidad_portante_isa()
        print(memoria)
        self.assertAlmostEqual(q_ult, 135.14, places=2)  #227.25
    
    def test_calculo_capacidad_portante_suelos_cohesivos2(self):
        parrilla = copy.deepcopy(self.parrilla_1)
        parrilla.θ = 6.9617521
        parrilla.D = 2
        γ_r, φ_r = 16, 23
        parrilla.set_perfil(Perfil([
            Estrato(H_0 = 1.0, γ_s = 20.0, E_s = 6597, c_u = 29.36, φ_s = 24, saturado = False, tipo_mat="c", C_s = 0.002,e_0 = 1.91, σ_pp = 90),
            Estrato(H_0 = 0.5, γ_s = 19.0, E_s = 6597, c_u = 29.36, φ_s = 24, saturado = False, tipo_mat="c", C_s = 0.002,e_0 = 1.91, σ_pp = 90),
            Estrato(H_0 = 1.0, γ_s = 21.0, E_s = 6597, c_u = 29.36, φ_s = 24, saturado = False, tipo_mat="g"),
            Estrato(H_0 = 2.0, γ_s = 19.0, E_s = 6597, c_u = 29.36, φ_s = 24, saturado = False, tipo_mat="c", C_s = 0.002,e_0 = 1.91, σ_pp = 90),
        ], γ_r=γ_r, φ_r=φ_r))
        parrilla.ω = 0

        T = 39.3
        F_zc = 251.34
        q_ult, memoria = parrilla.calculo_capacidad_portante_isa()
        print(memoria)
        self.assertAlmostEqual(q_ult, 139.97, places=2) #244.67
        
    def test_calculo_capacidad_portante_suelos_cohesivos3(self):
        parrilla = copy.deepcopy(self.parrilla_1)
        parrilla.θ = 6.9617521
        parrilla.D = 2.7
        γ_r, φ_r = 16, 23
        parrilla.set_perfil(Perfil([
            Estrato(H_0 = 1.0, γ_s = 20.0, E_s = 6597, c_u = 29.36, φ_s = 24, saturado = False, tipo_mat="c", C_s = 0.002,e_0 = 1.91, σ_pp = 90),
            Estrato(H_0 = 0.5, γ_s = 19.0, E_s = 6597, c_u = 29.36, φ_s = 24, saturado = False, tipo_mat="c", C_s = 0.002,e_0 = 1.91, σ_pp = 90),
            Estrato(H_0 = 1.0, γ_s = 21.0, E_s = 6597, c_u = 29.36, φ_s = 24, saturado = False, tipo_mat="c", C_s = 0.002,e_0 = 1.91, σ_pp = 90),
            Estrato(H_0 = 2.0, γ_s = 19.0, E_s = 6597, c_u = 29.36, φ_s = 24, saturado = False, tipo_mat="c", C_s = 0.002,e_0 = 1.91, σ_pp = 90),
        ], γ_r=γ_r, φ_r=φ_r))
        parrilla.ω = 0

        T = 39.3
        F_zc = 251.34

        q_ult, _ = parrilla.calculo_capacidad_portante_isa()
        self.assertAlmostEqual(q_ult, 146.73, places=2) #268.76

    def test_calculo_capacidad_portante_suelos_cohesivos4(self):
        parrilla = copy.deepcopy(self.parrilla_1)
        parrilla.θ = 6.9617521
        parrilla.B = 3
        parrilla.L = 3
        parrilla.D = 2.7
        γ_r, φ_r = 16, 23
        parrilla.set_perfil(Perfil([
            Estrato(H_0 = 1.0, γ_s = 20.0, E_s = 6597, c_u = 29.36, φ_s = 24, saturado = False, tipo_mat="c",C_s = 0.002,e_0 = 1.91, σ_pp = 90),
            Estrato(H_0 = 0.5, γ_s = 19.0, E_s = 6597, c_u = 29.36, φ_s = 24, saturado = False, tipo_mat="c", C_s = 0.002,e_0 = 1.91, σ_pp = 90),
            Estrato(H_0 = 1.0, γ_s = 21.0, E_s = 6597, c_u = 29.36, φ_s = 24, saturado = False, tipo_mat="c", C_s = 0.002,e_0 = 1.91, σ_pp = 90),
            Estrato(H_0 = 2.0, γ_s = 19.0, E_s = 6597, c_u = 29.36, φ_s = 24, saturado = False, tipo_mat="c",C_s = 0.002,e_0 = 1.91, σ_pp = 90),
        ], γ_r=γ_r, φ_r=φ_r))
        parrilla.ω = 0
        parrilla.ajustar_perfil()

        T = 39.3
        F_zc = 251.34

        q_ult, _ = parrilla.calculo_capacidad_portante_isa()
        
        self.assertAlmostEqual(q_ult, 164.10, places=2) #284.28
        
    def test_calculo_capacidad_portante_suelos_cohesivos5(self):
        parrilla = copy.deepcopy(self.parrilla_1)
        parrilla.θ = 6.9617521
        parrilla.B = 2
        parrilla.L = 2
        parrilla.D = 2.7
        γ_r, φ_r = 16, 23
        parrilla.set_perfil(Perfil([
            Estrato(H_0 = 1.0, γ_s = 20.0, E_s = 6597, c_u = 29.36, φ_s = 24, saturado = False, tipo_mat="c",C_s = 0.002,e_0 = 1.91, σ_pp = 90),
            Estrato(H_0 = 0.5, γ_s = 19.0, E_s = 6597, c_u = 29.36, φ_s = 24, saturado = False, tipo_mat="c", C_s = 0.002,e_0 = 1.91, σ_pp = 90),
            Estrato(H_0 = 1.0, γ_s = 21.0, E_s = 6597, c_u = 29.36, φ_s = 24, saturado = False, tipo_mat="c", C_s = 0.002,e_0 = 1.91, σ_pp = 90),
            Estrato(H_0 = 2.0, γ_s = 19.0, E_s = 6597, c_u = 29.36, φ_s = 24, saturado = False, tipo_mat="c", C_s = 0.002,e_0 = 1.91, σ_pp = 90),
        ], γ_r=γ_r, φ_r=φ_r))
        parrilla.ω = 0
        parrilla.ajustar_perfil()
        T = 39.3
        F_zc = 251.34

        q_ult, _ = parrilla.calculo_capacidad_portante_isa()
        
        self.assertAlmostEqual(q_ult, 165.71, places=2) #266.11

    def test_calculo_capacidad_portante_suelos_cohesivos6(self):
        parrilla = copy.deepcopy(self.parrilla_1)
        parrilla.θ = 6.9617521
        parrilla.B = 2
        parrilla.L = 2
        parrilla.D = 2.7
        γ_r, φ_r = 16, 23
        parrilla.set_perfil(Perfil([
            Estrato(H_0 = 1.0, γ_s = 20.0, E_s = 6597, c_u = 29.36, φ_s = 24, saturado = False, tipo_mat="c", C_s = 0.002,e_0 = 1.91, σ_pp = 90),
            Estrato(H_0 = 0.5, γ_s = 19.0, E_s = 6597, c_u = 29.36, φ_s = 24, saturado = False, tipo_mat="c", C_s = 0.002,e_0 = 1.91, σ_pp = 90),
            Estrato(H_0 = 1.0, γ_s = 21.0, E_s = 6597, c_u = 29.36, φ_s = 24, saturado = False, tipo_mat="c", C_s = 0.002,e_0 = 1.91, σ_pp = 90),
            Estrato(H_0 = 2.0, γ_s = 19.0, E_s = 6597, c_u = 29.36, φ_s = 24, saturado = False, tipo_mat="c", C_s = 0.002,e_0 = 1.91, σ_pp = 90),
        ], γ_r=γ_r, φ_r=φ_r))
        parrilla.ω = 30
        parrilla.ajustar_perfil()
        T = 39.3
        F_zc = 251.34

        q_ult, memoria = parrilla.calculo_capacidad_portante_isa()
        print(memoria)
        self.assertAlmostEqual(q_ult, 89.88, places=2) #221.53

    def test_calculo_capacidad_portante_suelos_cohesivos7(self):
        parrilla = copy.deepcopy(self.parrilla_1)
        parrilla.θ = 6.9617521
        parrilla.B = 2
        parrilla.L = 2
        parrilla.D = 2.7
        γ_r, φ_r = 16, 23
        parrilla.set_perfil(Perfil([
            Estrato(H_0 = 1.0, γ_s = 20.0, E_s = 6597, c_u = 29.36, φ_s = 24, saturado = False, tipo_mat="c", C_s = 0.002,e_0 = 1.91, σ_pp = 90),
            Estrato(H_0 = 0.5, γ_s = 19.0, E_s = 6597, c_u = 29.36, φ_s = 24, saturado = False, tipo_mat="c", C_s = 0.002,e_0 = 1.91, σ_pp = 90),
            Estrato(H_0 = 1.0, γ_s = 21.0, E_s = 6597, c_u = 29.36, φ_s = 24, saturado = False, tipo_mat="c", C_s = 0.002,e_0 = 1.91, σ_pp = 90),
            Estrato(H_0 = 2.0, γ_s = 19.0, E_s = 6597, c_u = 29.36, φ_s = 24, saturado = False, tipo_mat="c", C_s = 0.002,e_0 = 1.91, σ_pp = 90),
        ], γ_r=γ_r, φ_r=φ_r))
        parrilla.ω = 45
        parrilla.ajustar_perfil()
        T = 39.3
        F_zc = 251.34

        q_ult, _ = parrilla.calculo_capacidad_portante_isa()
        
        self.assertAlmostEqual(q_ult, 51.97, places=2) #199.24

    def test_calculo_capacidad_portante_suelos_cohesivos8(self):
        parrilla = copy.deepcopy(self.parrilla_9)
        parrilla.θ = 6.9617521
        
        
        parrilla.ω = 0
        T = 39.3
        F_zc = 600

        q_ult, memoria = parrilla.calculo_capacidad_portante_isa()
        print(memoria)
        self.assertAlmostEqual(q_ult, 99.53, places=2) #159.79
        
    def test_calculo_carga_lateral1(self):
        parrilla = copy.deepcopy(self.parrilla_3)
        
        F_zc = 52.6
        Q_L, memoria = parrilla.calculo_carga_lateral_isa(F_zc)
        #print(memoria)
        self.assertAlmostEqual(Q_L, 562.10, places=2)

    def test_calculo_carga_lateral2(self):
        parrilla = copy.deepcopy(self.parrilla_3)
        parrilla.B = 3
        parrilla.L = 3
        parrilla.D = 1.8
        γ_r, φ_r = 16, 23
        parrilla.set_perfil(Perfil([
            Estrato(H_0 = 1.0, γ_s = 15.0, E_s = 4000, c_u = 24.63, φ_s = 22, saturado = False, tipo_mat="c", C_s = 0.002,e_0 = 1.91, σ_pp = 90),
            Estrato(H_0 = 0.8, γ_s = 15.0, E_s = 4000, c_u = 27.53, φ_s = 23, saturado = False, tipo_mat="c", C_s = 0.002,e_0 = 1.91, σ_pp = 90),
            Estrato(H_0 = 1.5, γ_s = 15.0, E_s = 4000, c_u = 24.63, φ_s = 20, saturado = False, tipo_mat="c", C_s = 0.002,e_0 = 1.91, σ_pp = 90),
        ], γ_r=γ_r, φ_r=φ_r))
        parrilla.ajustar_perfil()
        

        F_zc = 55.6
        Q_L, memoria = parrilla.calculo_carga_lateral_isa(F_zc)
        #print(memoria)
        self.assertAlmostEqual(Q_L, 262.95, places=2)

    def test_calculo_carga_lateral3(self):
        parrilla = copy.deepcopy(self.parrilla_3)
        parrilla.B = 3
        parrilla.L = 3
        parrilla.D = 1.8
        γ_r, φ_r = 16, 23
        parrilla.set_perfil(Perfil([
            Estrato(H_0 = 1.0, γ_s = 15.0, E_s = 4000, c_u = 24.63, φ_s = 22, saturado = False, tipo_mat="c", C_s = 0.002,e_0 = 1.91, σ_pp = 90),
            Estrato(H_0 = 0.8, γ_s = 15.0, E_s = 4000, c_u = 27.53, φ_s = 23, saturado = False, tipo_mat="c", C_s = 0.002,e_0 = 1.91, σ_pp = 90),
            Estrato(H_0 = 1.5, γ_s = 15.0, E_s = 4000, c_u = 24.63, φ_s = 20, saturado = False, tipo_mat="c", C_s = 0.002,e_0 = 1.91, σ_pp = 90),
        ], γ_r=γ_r, φ_r=φ_r))
        parrilla.ajustar_perfil()

        F_zc = 55.6
        Q_L, memoria = parrilla.calculo_carga_lateral_isa(F_zc)
        #print(memoria)
        self.assertAlmostEqual(Q_L, 262.95, places=2)

    def test_calculo_carga_lateral4(self):
        parrilla = copy.deepcopy(self.parrilla_3)
        parrilla.B = 2.5
        parrilla.L = 2.5
        parrilla.D = 1.8
        γ_r, φ_r = 16, 23
        parrilla.set_perfil(Perfil([
            Estrato(H_0 = 1.0, γ_s = 15.0, E_s = 4000, c_u = 24.63, φ_s = 22, saturado = False, tipo_mat="c", C_s = 0.002,e_0 = 1.91, σ_pp = 90),
            Estrato(H_0 = 0.8, γ_s = 15.0, E_s = 4000, c_u = 27.53, φ_s = 23, saturado = False, tipo_mat="c", C_s = 0.002,e_0 = 1.91, σ_pp = 90),
            Estrato(H_0 = 1.5, γ_s = 15.0, E_s = 4000, c_u = 24.63, φ_s = 20, saturado = False, tipo_mat="c", C_s = 0.002,e_0 = 1.91, σ_pp = 90),
        ], γ_r=γ_r, φ_r=φ_r))
        parrilla.ajustar_perfil()

        F_zc = 55.6
        Q_L, memoria = parrilla.calculo_carga_lateral_isa(F_zc)
        #print(memoria)
        self.assertAlmostEqual(Q_L, 201.98, places=2)

    def test_calculo_carga_lateral5(self):
        parrilla = copy.deepcopy(self.parrilla_3)
        parrilla.B = 2.5
        parrilla.L = 2.5
        parrilla.D = 2.0
        γ_r, φ_r = 16, 23
        parrilla.set_perfil(Perfil([
            Estrato(H_0 = 1.0, γ_s = 15.0, E_s = 4000, c_u = 24.63, φ_s = 22, saturado = False, tipo_mat="c", C_s = 0.002,e_0 = 1.91, σ_pp = 90),
            Estrato(H_0 = 0.8, γ_s = 15.0, E_s = 4000, c_u = 27.53, φ_s = 23, saturado = False, tipo_mat="c", C_s = 0.002,e_0 = 1.91, σ_pp = 90),
            Estrato(H_0 = 1.5, γ_s = 15.0, E_s = 4000, c_u = 24.63, φ_s = 20, saturado = False, tipo_mat="c", C_s = 0.002,e_0 = 1.91, σ_pp = 90),
        ], γ_r=γ_r, φ_r=φ_r))
        parrilla.ajustar_perfil()

        F_zc = 55.6
        Q_L, memoria = parrilla.calculo_carga_lateral_isa(F_zc)
        #print(memoria)
        self.assertAlmostEqual(Q_L, 206.45, places=2)

    def test_calculo_carga_lateral6(self):
        
        F_zc = 55.6

        Q_L, memoria = self.parrilla_2.calculo_carga_lateral_isa(F_zc)
        print(memoria)
        self.assertAlmostEqual(Q_L, 82.571, places=3)

    def test_calculo_carga_lateral7(self):
        
        F_zc = 67.68

        Q_L, memoria = self.parrilla_2.calculo_carga_lateral_isa(F_zc)
        #print(memoria)
        self.assertAlmostEqual(Q_L, 85.883, places=3)

    def test_calculo_carga_lateral8(self):
        
        F_zc = 1200

        Q_L, memoria = self.parrilla_2.calculo_carga_lateral_isa(F_zc)
        #print(memoria)
        self.assertAlmostEqual(Q_L, 396.359, places=3)

    def test_calculo_carga_lateral10(self):
        
        parrilla = copy.deepcopy(self.parrilla_2)
        parrilla.B = 3.5
        parrilla.L = 3.5
        parrilla.ajustar_perfil()
        F_zc = 75.66

        Q_L, memoria = parrilla.calculo_carga_lateral_isa(F_zc)
        #print(memoria)
        self.assertAlmostEqual(Q_L, 98.101, places=3)

    def test_calculo_tension_cono_tierra_suelos_granulares(self):
        parrilla = copy.deepcopy(self.parrilla_1)
        parrilla.θ = 8
        γ_r, φ_r = 16.4, 23
        parrilla.set_perfil(Perfil([
            Estrato(H_0 = 1.0, γ_s = 20.0, E_s = 5000, c_u = None, φ_s = 26, saturado = False, tipo_mat="g"),
            Estrato(H_0 = 0.5, γ_s = 19.0, E_s = 5000, c_u = None, φ_s = 28, saturado = False, tipo_mat="g"),
            Estrato(H_0 = 1.0, γ_s = 21.0, E_s = 5000, c_u = None, φ_s = 29, saturado = False, tipo_mat="g"),
            Estrato(H_0 = 2.0, γ_s = 19.0, E_s = 5000, c_u = None, φ_s = 25, saturado = False, tipo_mat="g"),
        ], γ_r=γ_r, φ_r=φ_r))
        
        q_adm = 200
        
        T_u, memoria = parrilla.calculo_tension_isa(q_adm)
        print(memoria)
        self.assertAlmostEqual(T_u, 1822.48, places=2)

    def test_calculo_tension_cono_tierra_suelos_granulares2(self):
        parrilla = copy.deepcopy(self.parrilla_1)
        parrilla.θ = 8

        q_adm = 200
        
        T_u, memoria = parrilla.calculo_tension_isa(q_adm)
        print(memoria)
        self.assertAlmostEqual(T_u, 1519.03, places=2)

    def test_calculo_tension_cono_tierra_suelos_granulares3(self):
        parrilla = copy.deepcopy(self.parrilla_1)
        parrilla.θ = 8
        parrilla.γ_r = 15
        parrilla.B = 3
        parrilla.L = 3
        parrilla.ajustar_perfil()
                
        q_adm = 200
        
        T_u, memoria = parrilla.calculo_tension_isa(q_adm)
        #print(memoria)
        self.assertAlmostEqual(T_u, 1085.96, places=2)

    def test_calculo_tension_cono_tierra_suelos_granulares4(self):
        parrilla = copy.deepcopy(self.parrilla_1)
        parrilla.θ = 8
        parrilla.γ_r = 15
        parrilla.B = 3
        parrilla.L = 3
        parrilla.D = 1.8
        parrilla.ajustar_perfil()
        q_adm = 200
        
        T_u, memoria = parrilla.calculo_tension_isa(q_adm)
        #print(memoria)
        self.assertAlmostEqual(T_u, 1141.13, places=2)

    def test_calculo_tension_cono_tierra_suelos_granulares5(self):
        parrilla = copy.deepcopy(self.parrilla_1)
        parrilla.θ = 8
        parrilla.γ_r = 15
        parrilla.B = 2.5
        parrilla.L = 2.5
        parrilla.D = 2
        parrilla.ajustar_perfil()
        q_adm = 200
        
        T_u, memoria = parrilla.calculo_tension_isa(q_adm)
        #print(memoria)
        self.assertAlmostEqual(T_u, 1081.14, places=2)

    def test_calculo_tension_cono_tierra_suelos_granulares6(self):
        parrilla = copy.deepcopy(self.parrilla_1)
        parrilla.θ = 8
        parrilla.γ_r = 15
        parrilla.B = 2.5
        parrilla.L = 2.5
        parrilla.D = 2
        γ_r, φ_r = 16.4, 23
        parrilla.set_perfil(Perfil([
            Estrato(H_0 = 1.0, γ_s = 20.0, E_s = 6597, c_u = 0, φ_s = 24, saturado = True, tipo_mat = "g", c_p = 0),
            Estrato(H_0 = 0.5, γ_s = 19.0, E_s = 6597, c_u = 0, φ_s = 24, saturado = True, tipo_mat = "g", c_p = 0),
            Estrato(H_0 = 1.0, γ_s = 21.0, E_s = 6597, c_u = 0, φ_s = 24, saturado = True, tipo_mat = "g", c_p = 0),
            Estrato(H_0 = 2.0, γ_s = 19.0, E_s = 6597, c_u = 0, φ_s = 24, saturado = True, tipo_mat = "g", c_p = 0),
        ], γ_r=γ_r, φ_r=φ_r))
        parrilla.ajustar_perfil()

        q_adm = 200
        
        T_u, memoria = parrilla.calculo_tension_isa(q_adm)
        #print(memoria)
        self.assertAlmostEqual(T_u, 989.79, places=2)

    def test_calculo_tension_cono_tierra_suelos_granulares7(self):
        parrilla = copy.deepcopy(self.parrilla_1)
        parrilla.θ = 8
        parrilla.γ_r = 15
        parrilla.B = 2.5
        parrilla.L = 2.5
        parrilla.D = 2
        γ_r, φ_r = 16.4, 23
        parrilla.set_perfil(Perfil([
            Estrato(H_0 = 1.0, γ_s = 16.0, E_s = 6597, c_u = 0, φ_s = 24, saturado = False, tipo_mat = "g", c_p = 0),
            Estrato(H_0 = 0.5, γ_s = 17.0, E_s = 6597, c_u = 0, φ_s = 24, saturado = False, tipo_mat = "g", c_p = 0),
            Estrato(H_0 = 1.0, γ_s = 16.0, E_s = 6597, c_u = 0, φ_s = 24, saturado = False, tipo_mat = "g", c_p = 0),
            Estrato(H_0 = 2.0, γ_s = 17.0, E_s = 6597, c_u = 0, φ_s = 24, saturado = False, tipo_mat = "g", c_p = 0),
        ], γ_r=γ_r, φ_r=φ_r))
        parrilla.ajustar_perfil()

        q_adm = 200
        
        T_u, memoria = parrilla.calculo_tension_isa(q_adm)
        #print(memoria)
        self.assertAlmostEqual(T_u, 1248.54, places=2)

    def test_calculo_tension_cono_tierra_suelos_granulares8(self):
        parrilla = copy.deepcopy(self.parrilla_1)
        parrilla.θ = 8
        parrilla.γ_r = 15
        parrilla.B = 2.5
        parrilla.L = 2.5
        parrilla.D = 2
        γ_r, φ_r = 16.4, 23
        parrilla.set_perfil(Perfil([
            Estrato(H_0 = 1.0, γ_s = 16.0, E_s = 6597, c_u = 0, φ_s = 24, saturado = True, tipo_mat = "g", c_p = 0),
            Estrato(H_0 = 0.5, γ_s = 17.0, E_s = 6597, c_u = 0, φ_s = 24, saturado = True, tipo_mat = "g", c_p = 0),
            Estrato(H_0 = 1.0, γ_s = 16.0, E_s = 6597, c_u = 0, φ_s = 24, saturado = True, tipo_mat = "g", c_p = 0),
            Estrato(H_0 = 2.0, γ_s = 17.0, E_s = 6597, c_u = 0, φ_s = 24, saturado = True, tipo_mat = "g", c_p = 0),
        ], γ_r=γ_r, φ_r=φ_r))
        parrilla.ajustar_perfil()

        q_adm = 200
        
        T_u, memoria = parrilla.calculo_tension_isa(q_adm)
        print(memoria)
        self.assertAlmostEqual(T_u, 919.94, places=2)

    # def test_calculo_tension_meyerhof_adams_suelos_cohesivos(self):
    #     parrilla = copy.deepcopy(self.parrilla_3)
    #     parrilla.θ = 8
    #     parrilla.γ_c =  23.53
    #     γ_r, φ_r = 16.4, 23
    #     parrilla.set_perfil(Perfil([
    #         Estrato(H_0 = 1.0, γ_s = 20.0, E_s = 5000, c_u = 32, φ_s = 24, saturado = False, c_p=20.2,tipo_mat="c", C_s = 0.002,e_0 = 1.91, σ_pp = 90),
    #         Estrato(H_0 = 0.5, γ_s = 19.0, E_s = 5000, c_u = 34, φ_s = 24, saturado = True, c_p=20.2,tipo_mat="c", C_s = 0.002,e_0 = 1.91, σ_pp = 90),
    #         Estrato(H_0 = 1.0, γ_s = 21.0, E_s = 5000, c_u = 35, φ_s = 24, saturado = True, c_p=20.2,tipo_mat="c", C_s = 0.002,e_0 = 1.91, σ_pp = 90),
    #         Estrato(H_0 = 2.0, γ_s = 19.0, E_s = 5000, c_u = 28, φ_s = 24, saturado = True, c_p=20.2,tipo_mat="c", C_s = 0.002,e_0 = 1.91, σ_pp = 90),
    #     ], γ_r=γ_r, φ_r=φ_r))
    #     T_u, _ = parrilla.calculo_tension_meyerhof_adams_suelos_cohesivos()
    #     self.assertAlmostEqual(T_u, 1080.45, places=2)

    # def test_calculo_tension_meyerhof_adams_suelos_cohesivos2(self):
        
    #     T_u, memoria = self.parrilla_5.calculo_tension_meyerhof_adams_suelos_cohesivos()
        
    #     #print(memoria)
    #     self.assertAlmostEqual(T_u, 1072.98 , places=2)

    # def test_calculo_tension_meyerhof_adams_suelos_cohesivos3(self):
        
    #     parrilla = copy.deepcopy(self.parrilla_5)
    #     γ_r, φ_r = 16, 23
    #     parrilla.set_perfil(Perfil([
    #         Estrato(H_0 = 1.0, γ_s = 19.0, E_s = 5550, c_u = 12.63, φ_s = 22, saturado = False, tipo_mat = "c", c_p = 20.2, C_s = 0.002,e_0 = 1.91, σ_pp = 90),
    #         Estrato(H_0 = 0.5, γ_s = 24.0, E_s = 5420, c_u = 15.63, φ_s = 18, saturado = True, tipo_mat = "g", c_p = 0),
    #         Estrato(H_0 = 1.3, γ_s = 25.0, E_s = 4350, c_u = 17.63, φ_s = 15, saturado = True, tipo_mat = "c", c_p = 15.6, C_s = 0.002,e_0 = 1.91, σ_pp = 90),
    #         Estrato(H_0 = 1.5, γ_s = 26.0, E_s = 6000, c_u = 21.63, φ_s = 19, saturado = True, tipo_mat = "c", c_p = 10.8, C_s = 0.002,e_0 = 1.91, σ_pp = 90),
    #     ], γ_r=γ_r, φ_r=φ_r))
    #     T_u, memoria = parrilla.calculo_tension_meyerhof_adams_suelos_cohesivos()
        
    #     #print(memoria)
    #     self.assertAlmostEqual(T_u, 859.97 , places=2)

    # def test_calculo_tension_meyerhof_adams_suelos_cohesivos4(self):
        
    #     parrilla = copy.deepcopy(self.parrilla_5)
    #     parrilla.D = 2.5
    #     γ_r, φ_r = 6, 23
    #     parrilla.set_perfil(Perfil([
    #         Estrato(H_0 = 1.0, γ_s = 19.0, E_s = 5550, c_u = 12.63, φ_s = 22, saturado = True, tipo_mat = "c", c_p = 20.2, C_s = 0.002,e_0 = 1.91, σ_pp = 90),
    #         Estrato(H_0 = 0.5, γ_s = 24.0, E_s = 5420, c_u = 15.63, φ_s = 18, saturado = True, tipo_mat = "g", c_p = 0),
    #         Estrato(H_0 = 1.3, γ_s = 25.0, E_s = 4350, c_u = 17.63, φ_s = 15, saturado = True, tipo_mat = "c", c_p = 15.6, C_s = 0.002,e_0 = 1.91, σ_pp = 90),
    #         Estrato(H_0 = 1.5, γ_s = 26.0, E_s = 6000, c_u = 21.63, φ_s = 19, saturado = True, tipo_mat = "g", c_p = 0),
    #     ], γ_r=γ_r, φ_r=φ_r))
    #     T_u, memoria = parrilla.calculo_tension_meyerhof_adams_suelos_cohesivos()
        
    #     print(memoria)
    #     self.assertAlmostEqual(T_u, 892.49 , places=2)

    # def test_calculo_tension_meyerhof_adams_suelos_cohesivos5(self):
        
    #     parrilla = copy.deepcopy(self.parrilla_5)
    #     parrilla.D = 2.5
    #     parrilla.B = 2.5
    #     parrilla.L = 2.5
    #     γ_r, φ_r = 16, 23
    #     parrilla.set_perfil(Perfil([
    #         Estrato(H_0 = 1.0, γ_s = 19.0, E_s = 5550, c_u = 12.63, φ_s = 22, saturado = False, tipo_mat = "c", c_p = 20.2, C_s = 0.002,e_0 = 1.91, σ_pp = 90),
    #         Estrato(H_0 = 0.5, γ_s = 24.0, E_s = 5420, c_u = 15.63, φ_s = 18, saturado = True, tipo_mat = "g", c_p = 0),
    #         Estrato(H_0 = 1.3, γ_s = 25.0, E_s = 4350, c_u = 17.63, φ_s = 15, saturado = True, tipo_mat = "c", c_p = 15.6, C_s = 0.002,e_0 = 1.91, σ_pp = 90),
    #         Estrato(H_0 = 1.5, γ_s = 26.0, E_s = 6000, c_u = 21.63, φ_s = 19, saturado = True, tipo_mat = "g", c_p = 0),
    #     ], γ_r=γ_r, φ_r=φ_r))
    #     parrilla.ajustar_perfil()
    #     T_u, memoria = parrilla.calculo_tension_meyerhof_adams_suelos_cohesivos()
        
    #     #print(memoria)
    #     self.assertAlmostEqual(T_u, 630.88 , places=2)

    # def test_calculo_tension_meyerhof_adams_suelos_cohesivos6(self):
        
    #     parrilla = copy.deepcopy(self.parrilla_5)
    #     parrilla.D = 2.5
    #     parrilla.B = 2.5
    #     parrilla.L = 2.5
    #     parrilla.H = 0.3
    #     parrilla.TP = 0.3
    #     parrilla.γ_c =  14
    #     γ_r, φ_r = 16, 23
    #     parrilla.set_perfil(Perfil([
    #         Estrato(H_0 = 1.0, γ_s = 19.0, E_s = 5550, c_u = 12.63, φ_s = 25, saturado = True, tipo_mat = "c", c_p = 20.2, C_s = 0.002,e_0 = 1.91, σ_pp = 90),
    #         Estrato(H_0 = 0.5, γ_s = 21.0, E_s = 5420, c_u = 15.63, φ_s = 24, saturado = True, tipo_mat = "g", c_p = 0),
    #         Estrato(H_0 = 1.5, γ_s = 22.0, E_s = 6000, c_u = 21.63, φ_s = 25, saturado = True, tipo_mat = "g", c_p = 0),
    #         Estrato(H_0 = 1.3, γ_s = 21.0, E_s = 4350, c_u = 17.63, φ_s = 24, saturado = True, tipo_mat = "c", c_p = 15.6, C_s = 0.002,e_0 = 1.91, σ_pp = 90),
    #     ], γ_r=γ_r, φ_r=φ_r))
    #     parrilla.ajustar_perfil()
    #     T_u, memoria = parrilla.calculo_tension_meyerhof_adams_suelos_cohesivos()
        
    #     print(memoria)
    #     self.assertAlmostEqual(T_u, 447.62 , places=2)


    def test_calculo_esfuerzo_actuante_sobre_suelo(self):
        parrilla = copy.deepcopy(self.parrilla_4)
        parrilla.D = 1.9
        parrilla.φ_r = 23
        γ_r, φ_r = 16.4, 23
        parrilla.set_perfil(Perfil([
            Estrato(H_0 = 1.0, γ_s = 19.5, E_s = 3000, c_u = None, φ_s = 38, saturado = False, tipo_mat = 'g'),
            Estrato(H_0 = 1.0, γ_s = 19.5, E_s = 3000, c_u = None, φ_s = 38, saturado = False, tipo_mat = 'g'),
            Estrato(H_0 = 1.0, γ_s = 19.5, E_s = 3000, c_u = None, φ_s = 38, saturado = False, tipo_mat = 'g'),
            Estrato(H_0 = 1.0, γ_s = 19.5, E_s = 3000, c_u = 25, φ_s = 38, saturado = False, tipo_mat = 'c', C_s = 0.002,e_0 = 1.91, σ_pp = 90),
        ], γ_r=γ_r, φ_r=φ_r))

        Fx_c = 38.06
        Fy_c = 39.30
        Fz_c = 275.23   
        Q_max, Q_min, memoria = parrilla.calculo_esfuerzo_actuante_sobre_suelo(Fx_c, Fy_c, Fz_c)
        print(memoria)
        self.assertAlmostEqual(Q_min, 288.55, places =2)
        self.assertAlmostEqual(Q_max, 311.38, places =2)

    def test_calculo_esfuerzo_actuante_sobre_suelo2(self):
        parrilla = copy.deepcopy(self.parrilla_4)
        parrilla.B = 5
        parrilla.L = 5
        parrilla.C =2
        parrilla.φ_r = 23
        γ_r, φ_r = 16.4, 23
        parrilla.set_perfil(Perfil([
            Estrato(H_0 = 1.0, γ_s = 19.5, E_s = 3000, c_u = None, φ_s = 38, saturado = False, tipo_mat = 'g'),
            Estrato(H_0 = 1.0, γ_s = 19.5, E_s = 3000, c_u = None, φ_s = 38, saturado = False, tipo_mat = 'g'),
            Estrato(H_0 = 1.0, γ_s = 19.5, E_s = 3000, c_u = None, φ_s = 38, saturado = False, tipo_mat = 'g'),
            Estrato(H_0 = 1.0, γ_s = 19.5, E_s = 3000, c_u = 22, φ_s = 38, saturado = False, tipo_mat = 'c', C_s = 0.002,e_0 = 1.91, σ_pp = 90),
        ], γ_r=γ_r, φ_r=φ_r))
        parrilla.ajustar_perfil()

        Fx_c = 38.06
        Fy_c = 39.30
        Fz_c = 275.23   
        Q_max, Q_min, memoria = parrilla.calculo_esfuerzo_actuante_sobre_suelo(Fx_c, Fy_c, Fz_c)
        print(memoria)
        self.assertAlmostEqual(Q_min, 66.64, places =2)
        self.assertAlmostEqual(Q_max, 68.58, places =2)

    def test_calculo_esfuerzo_actuante_sobre_suelo3(self):
        parrilla = copy.deepcopy(self.parrilla_4)
        
        Fx_c = 38.06
        Fy_c = 39.30
        Fz_c = 275.23   
        Q_max, Q_min, memoria = parrilla.calculo_esfuerzo_actuante_sobre_suelo(Fx_c, Fy_c, Fz_c)
        #print(memoria)
        self.assertAlmostEqual(Q_min, 281.99, places =2)
        self.assertAlmostEqual(Q_max, 304.82, places =2)

    def test_calculo_esfuerzo_actuante_sobre_suelo4(self):
        parrilla = copy.deepcopy(self.parrilla_4)
        
        Fx_c = 103.11
        Fy_c = 89.53
        Fz_c = 736.62   
        Q_max, Q_min, memoria = parrilla.calculo_esfuerzo_actuante_sobre_suelo(Fx_c, Fy_c, Fz_c)
        #print(memoria)
        self.assertAlmostEqual(Q_min, 393.48, places =2)
        self.assertAlmostEqual(Q_max, 424.03, places =2)

    def test_calculo_esfuerzo_actuante_sobre_suelo5(self):
        parrilla = copy.deepcopy(self.parrilla_4)
        
        Fx_c = 93.73
        Fy_c = 88.62
        Fz_c = 661.62   
        Q_max, Q_min, memoria = parrilla.calculo_esfuerzo_actuante_sobre_suelo(Fx_c, Fy_c, Fz_c)
        #print(memoria)
        self.assertAlmostEqual(Q_min, 366.64, places =2)
        self.assertAlmostEqual(Q_max, 413.37, places =2)

    def test_calculo_esfuerzo_actuante_sobre_suelo6(self):
        parrilla = copy.deepcopy(self.parrilla_7)
        
        Fx_c = 312.3
        Fy_c = 302.1
        Fz_c = 1441.77   
        Q_max, Q_min, memoria = parrilla.calculo_esfuerzo_actuante_sobre_suelo(Fx_c, Fy_c, Fz_c)
        #print(memoria)
        self.assertAlmostEqual(Q_min, 96.03, places =2)
        self.assertAlmostEqual(Q_max, 116.11, places =2)

    def test_calculo_esfuerzo_actuante_sobre_suelo7(self):
        parrilla = copy.deepcopy(self.parrilla_1)
        
        Fx_c = 209.57
        Fy_c = 203.94
        Fz_c = 1153.71   
        Q_max, Q_min, memoria = parrilla.calculo_esfuerzo_actuante_sobre_suelo(Fx_c, Fy_c, Fz_c)
        #print(memoria)
        self.assertAlmostEqual(Q_min, 72.98, places =2)
        self.assertAlmostEqual(Q_max, 132.52, places =2)
    
    def test_calculo_esfuerzo_actuante_sobre_suelo8(self):
        parrilla = copy.deepcopy(self.parrilla_3)
        
        Fx_c = 77.12
        Fy_c = 66.99
        Fz_c = 552.75  
        Q_max, Q_min, memoria = parrilla.calculo_esfuerzo_actuante_sobre_suelo(Fx_c, Fy_c, Fz_c)
        print(memoria)
        self.assertAlmostEqual(Q_min, 68.33, places =2)
        self.assertAlmostEqual(Q_max, 89.09, places =2)

    def test_calculo_esfuerzo_actuante_sobre_suelo9(self):
        parrilla = copy.deepcopy(self.parrilla_4)
        
        Fx_c = 95.4
        Fy_c = 100.2
        Fz_c = 1000  
        Q_max, Q_min, memoria = parrilla.calculo_esfuerzo_actuante_sobre_suelo(Fx_c, Fy_c, Fz_c)
        #print(memoria)
        self.assertAlmostEqual(Q_min, 419.91, places =2)
        self.assertAlmostEqual(Q_max, 529.29, places =2)

    def test_calculo_esfuerzo_actuante_sobre_suelo_10(self):
        parrilla = copy.deepcopy(self.parrilla_4)
        
        Fx_c = 350.85
        Fy_c = 400.24
        Fz_c = 500
        Q_max, Q_min, memoria = parrilla.calculo_esfuerzo_actuante_sobre_suelo(Fx_c, Fy_c, Fz_c)
        print(memoria)
        self.assertAlmostEqual(Q_min, -158.07, places =2)
        self.assertAlmostEqual(Q_max, 1257.14, places =2)
    
    def test_calculo_esfuerzo_actuante_sobre_suelo_11(self):
        parrilla = copy.deepcopy(self.parrilla_4)
        
        Fx_c = 433.85
        Fy_c = 420.24
        Fz_c = 2005.41 
        Q_max, Q_min, memoria = parrilla.calculo_esfuerzo_actuante_sobre_suelo(Fx_c, Fy_c, Fz_c)
        print(memoria)
        self.assertAlmostEqual(Q_min, 316.07, places =2)
        self.assertAlmostEqual(Q_max, 1135.84, places =2)


    def test_calculo_asentamiento_por_consolidacion(self):
        
        parrilla = copy.deepcopy(self.parrilla_8)
        parrilla.B = 2
        parrilla.L = 2
        parrilla.D = 1.9
        parrilla.C = 1.75
        parrilla.θ = 6.9617521
        parrilla.ajustar_perfil()

        F_zc = 1550

        S_c, memoria = parrilla.calculo_asentamiento_por_consolidacion(F_zc)
        print(memoria)
        self.assertAlmostEqual(S_c, 0.01245, places =4)

    def test_calculo_asentamiento_por_consolidacion2(self):
        
        parrilla = copy.deepcopy(self.parrilla_8)
        
        F_zc = 1400

        S_c, memoria = parrilla.calculo_asentamiento_por_consolidacion(F_zc)
        #print(memoria)
        self.assertAlmostEqual(S_c, 0.040154, places =5)

    def test_calculo_asentamiento_por_consolidacion3(self):
        
        parrilla = copy.deepcopy(self.parrilla_8)
        
        F_zc = 500

        S_c, memoria = parrilla.calculo_asentamiento_por_consolidacion(F_zc)
        #print(memoria)
        self.assertAlmostEqual(S_c, 0.040154, places =5)

    def test_calculo_asentamiento_por_consolidacion4(self):
        
        parrilla = copy.deepcopy(self.parrilla_8)
        
        F_zc = 900

        S_c, memoria = parrilla.calculo_asentamiento_por_consolidacion(F_zc)
        #print(memoria)
        self.assertAlmostEqual(S_c, 0.04015, places =5)

    def test_calculo_asentamiento_por_consolidacion5(self):
        
        parrilla = copy.deepcopy(self.parrilla_8)
        
        F_zc = 250

        S_c, memoria = parrilla.calculo_asentamiento_por_consolidacion(F_zc)
        #print(memoria)
        self.assertAlmostEqual(S_c, 0.0401548, places =5)

    def test_calculo_asentamiento_por_consolidacion6(self):
        
        parrilla = copy.deepcopy(self.parrilla_8)
        
        F_zc = 400

        S_c, memoria = parrilla.calculo_asentamiento_por_consolidacion(F_zc)
        #print(memoria)
        self.assertAlmostEqual(S_c, 0.0401548, places =5)

    def test_calculo_asentamiento_por_consolidacion7(self):
        
        parrilla = copy.deepcopy(self.parrilla_8)
        
        F_zc = 1000

        S_c, memoria = parrilla.calculo_asentamiento_por_consolidacion(F_zc)
        #print(memoria)
        self.assertAlmostEqual(S_c, 0.0401548, places =5)

    def test_calculo_asentamiento_por_consolidacion8(self):
        
        parrilla = copy.deepcopy(self.parrilla_8)
        parrilla.D = 0.5
        parrilla.C = 1
        F_zc = 2000

        S_c, memoria = parrilla.calculo_asentamiento_por_consolidacion(F_zc)
        #print(memoria)
        self.assertAlmostEqual(S_c, 0.040154, places =5)

    def test_calculo_asentamiento_por_consolidacion9(self):
        
        parrilla = copy.deepcopy(self.parrilla_10)
        parrilla.D = 4.5
        parrilla.C = 4.6
        F_zc = 198.48

        S_c, memoria = parrilla.calculo_asentamiento_por_consolidacion(F_zc)
        print(memoria)
        self.assertAlmostEqual(S_c, 0.05428, places =5)

    def test_calculo_asentamiento_por_consolidacion_10(self):
        
        parrilla = copy.deepcopy(self.parrilla_10)
        parrilla.D = 3.5
        parrilla.C = 3.6
        F_zc = 198.48

        S_c, memoria = parrilla.calculo_asentamiento_por_consolidacion(F_zc)
        print(memoria)
        self.assertAlmostEqual(S_c, 0.06909, places =5)

    def test_calculo_asentamiento_por_consolidacion_11(self):
        
        parrilla = copy.deepcopy(self.parrilla_10)
        parrilla.D = 5.2
        parrilla.C = 5.3
        F_zc = 198.48

        S_c, memoria = parrilla.calculo_asentamiento_por_consolidacion(F_zc)
        print(memoria)
        self.assertAlmostEqual(S_c, 0.05741, places =5)

    def test_calculo_asentamiento_por_consolidacion_12(self):
        
        parrilla = copy.deepcopy(self.parrilla_10)
        parrilla.D = 5.5
        parrilla.C = 5.6
        F_zc = 198.48

        S_c, memoria = parrilla.calculo_asentamiento_por_consolidacion(F_zc)
        print(memoria)
        self.assertAlmostEqual(S_c, 0.05492, places =5)

    def test_calculo_asentamiento_elastico_suelos_granulares(self):
        
        parrilla = copy.deepcopy(self.parrilla_6)
        
        parrilla.B = 3.5
        parrilla.L = 3.5
        parrilla.D = 1.5
        parrilla.H = 0.3
        parrilla.C = 0.8
        parrilla.TP = 0.4
        parrilla.θ = 0
        parrilla.γ_c = 23.53
        parrilla.set_perfil(Perfil([
            Estrato(H_0 = 2, γ_s = 9.4, E_s = 7000, c_u = None, φ_s = 22, saturado = False, tipo_mat="g"),
            Estrato(H_0 = 2, γ_s = 9.4, E_s = 17500, c_u = None, φ_s = 23, saturado = False, tipo_mat="g"),
        ]))
        parrilla.γ_r = 9.4
        parrilla.ajustar_perfil()

        k = 4
        t = 20
        F_zc = 1800.14021
        S, memoria = parrilla.calculo_asentamiento_elastico_suelos_granulares(k, F_zc, t)
        #print(memoria)
        self.assertAlmostEqual(S, 0.0384279, places=7)

    def test_calculo_asentamiento_elastico_suelos_granulares2(self):
        
        parrilla = copy.deepcopy(self.parrilla_6)
        
        k = 6
        t = 50
        F_zc = 2224.14021
        S, memoria = parrilla.calculo_asentamiento_elastico_suelos_granulares(k, F_zc, t)
        #print(memoria)
        self.assertAlmostEqual(S, 0.015087, places=6)

    def test_calculo_asentamiento_elastico_suelos_granulares3(self):
        
        parrilla = copy.deepcopy(self.parrilla_6)
        parrilla.D = 1.5
        k = 6
        t = 50
        F_zc = 2224.14021
        S, memoria = parrilla.calculo_asentamiento_elastico_suelos_granulares(k, F_zc, t)
        #print(memoria)
        self.assertAlmostEqual(S, 0.01564, places=5)

    def test_calculo_asentamiento_elastico_suelos_granulares4(self):
        
        parrilla = copy.deepcopy(self.parrilla_6)
        parrilla.D = 1.5
        parrilla.B = 3
        parrilla.L = 3
        parrilla.ajustar_perfil()
        k = 6
        t = 50
        F_zc = 2224.14021
        S, memoria = parrilla.calculo_asentamiento_elastico_suelos_granulares(k, F_zc, t)
        #print(memoria)
        self.assertAlmostEqual(S, 0.024606, places=6)

    def test_calculo_asentamiento_elastico_suelos_granulares5(self):
        
        parrilla = copy.deepcopy(self.parrilla_6)
        parrilla.D = 1.5
        parrilla.B = 3
        parrilla.L = 3
        parrilla.ajustar_perfil()
        k = 6
        t = 50
        F_zc = 1500.30
        S, memoria = parrilla.calculo_asentamiento_elastico_suelos_granulares(k, F_zc, t)
        #print(memoria)
        self.assertAlmostEqual(S, 0.018912, places=6)

    def test_calculo_asentamiento_elastico_suelos_granulares6(self):
        
        parrilla = copy.deepcopy(self.parrilla_6)
        
        parrilla.B = 3
        parrilla.L = 3
        parrilla.D = 1.7
        parrilla.C = 1.7
        parrilla.TP = 0.4
        parrilla.θ = 0
        parrilla.set_perfil(Perfil([
            Estrato(H_0 = 2, γ_s = 9.4, E_s = 7000, c_u = None, φ_s = 25, saturado = False, tipo_mat="g"),
            Estrato(H_0 = 2, γ_s = 9.4, E_s = 17500, c_u = None, φ_s = 31, saturado = False, tipo_mat="g"),
        ]))
        parrilla.γ_r = 16
        parrilla.ajustar_perfil()

        k = 80
        t = 30
        F_zc = 1800.14021
        S, memoria = parrilla.calculo_asentamiento_elastico_suelos_granulares(k, F_zc, t)
        #print(memoria)
        self.assertAlmostEqual(S, 0.04810, places=5)

    def test_calculo_asentamiento_elastico_suelos_granulares7(self):
        parrilla = copy.deepcopy(self.parrilla_7)
        parrilla.B = 3.5
        parrilla.L = 3.5
        parrilla.D = 1.5
        parrilla.C = 1.5
        parrilla.TP = 0.4
        parrilla.θ = 8
        parrilla.γ_r = 15
        parrilla.set_perfil(Perfil([
            Estrato(H_0 = 5, γ_s = 9.4, E_s = 7000, c_u = None, φ_s = 29, saturado = False, tipo_mat="g", ν=0.5),
            Estrato(H_0 = 5, γ_s = 9.4, E_s = 17500, c_u = None, φ_s = 34, saturado = False, tipo_mat="g", ν=0.5),
        ],γ_r=16.4))
        parrilla.ajustar_perfil()
        
        k = 80
        t = 30
        F_zc = 1500
        
        S, memoria = parrilla.calculo_asentamiento_elastico_suelos_granulares(k, F_zc, t)
        #print(memoria)
        self.assertAlmostEqual(S, 0.07368, places=4)

    def test_calculo_asentamiento_elastico_suelos_cohesivos(self):
        parrilla = copy.deepcopy(self.parrilla_7)
        parrilla.B = 3.5
        parrilla.L = 3.5
        parrilla.D = 1.5
        parrilla.C = 1.5
        parrilla.TP = 0.4
        parrilla.θ = 8
        parrilla.set_perfil(Perfil([
            Estrato(H_0 = 5, γ_s = 9.4, E_s = 7000, c_u = 20.3, φ_s = 21, saturado =False, tipo_mat="c", ν=0.5,C_s = 1,e_0 = 1.91, σ_pp = 90),
            Estrato(H_0 = 5, γ_s = 9.4, E_s = 17500, c_u = 32.4, φ_s = 20, saturado = False, tipo_mat="c", ν=0.5, C_s = 1,e_0 = 1.91, σ_pp = 90),
        ],γ_r=16.4))
        parrilla.ajustar_perfil()
        
        F_zc = 1500
        
        S, memoria = parrilla.calculo_asentamiento_elastico_suelos_cohesivos(F_zc)
        #print(memoria)
        self.assertAlmostEqual(S, 0.01305, places=4)

    def test_calculo_asentamiento_elastico_suelos_cohesivos2(self):
        parrilla = copy.deepcopy(self.parrilla_7)
                
        F_zc = 500
        
        S, memoria = parrilla.calculo_asentamiento_elastico_suelos_cohesivos(F_zc)
        #print(memoria)
        self.assertAlmostEqual(S, 0.00319, places=4)

    def test_calculo_asentamiento_elastico_suelos_cohesivos3(self):
        parrilla = copy.deepcopy(self.parrilla_7)
                
        F_zc = 650
        
        S, memoria = parrilla.calculo_asentamiento_elastico_suelos_cohesivos(F_zc)
        #print(memoria)
        self.assertAlmostEqual(S, 0.00352, places=5)

    def test_calculo_asentamiento_elastico_suelos_cohesivos4(self):
        parrilla = copy.deepcopy(self.parrilla_7)
        parrilla.B = 4
        parrilla.L = 4
        parrilla.ajustar_perfil()

        F_zc = 650
        
        S, memoria = parrilla.calculo_asentamiento_elastico_suelos_cohesivos(F_zc)
        #print(memoria)
        self.assertAlmostEqual(S, 0.00523, places=5)

    def test_calculo_asentamiento_elastico_suelos_cohesivos5(self):
        parrilla = copy.deepcopy(self.parrilla_7)
        parrilla.B = 3
        parrilla.L = 3

        F_zc = 650
        
        S, memoria = parrilla.calculo_asentamiento_elastico_suelos_cohesivos(F_zc)
        #print(memoria)
        self.assertAlmostEqual(S, 0.00877, places=5)

    def test_calculo_asentamiento_elastico_suelos_cohesivos6(self):
        parrilla = copy.deepcopy(self.parrilla_7)
        parrilla.B = 3
        parrilla.L = 3
        parrilla.D = 1.5
        parrilla.ajustar_perfil()

        F_zc = 650
        
        S, memoria = parrilla.calculo_asentamiento_elastico_suelos_cohesivos(F_zc)
        #print(memoria)
        self.assertAlmostEqual(S, 0.00601, places=5)


    def test_asentamiento_incremental_granular(self):

        parrilla = copy.deepcopy(self.parrilla_1)
        C_1 = 0.93282668
        C_2 = 1.520412
        q_0 = 227.14641322
        estrato = Estrato(H_0=0.8, γ_s=15.0, E_s=15000, c_u=None, φ_s=25, saturado=False, tipo_mat="g",ν=0.45)
        H = 1.5
        k = 80
        S = parrilla.asentamiento_incremental_granular(H, estrato, q_0, C_1, C_2, k)
        
        self.assertAlmostEqual(S, 0.005798, places =5)

    def test_asentamiento_incremental_granular2(self):

        parrilla = copy.deepcopy(self.parrilla_1)
        C_1 = 0.93282668
        C_2 = 1.520412
        q_0 = 227.14641322
        estrato = Estrato(H_0=0.8, γ_s=15.0, E_s=15000, c_u=None, φ_s=26, saturado=False, tipo_mat="g",ν=0.45)
        H = 0.7
        k = 80
        S = parrilla.asentamiento_incremental_granular(H, estrato, q_0, C_1, C_2, k)
        
        self.assertAlmostEqual(S, 0.0012628, places =4)
    
    def test_asentamiento_incremental_granular3(self):

        parrilla = copy.deepcopy(self.parrilla_1)
        C_1 = 0.93282668
        C_2 = 1.520412
        q_0 = 227.14641322
        estrato = Estrato(H_0=0.8, γ_s=15.0, E_s=15000, c_u=None, φ_s=31, saturado=False, tipo_mat="g",ν=0.45)
        H = 1.5
        k = 80
        S1 = parrilla.asentamiento_incremental_granular(H, estrato, q_0, C_1, C_2, k)
        H = 0.7
        S2 = parrilla.asentamiento_incremental_granular(H, estrato, q_0, C_1, C_2, k)
        
        self.assertAlmostEqual(S1, 0.005798, places =5)
        self.assertAlmostEqual(S2, 0.001262, places =5)

    def test_calculo_asentamiento_elastico_suelos_mixtos(self):
        
        parrilla = copy.deepcopy(self.parrilla_8)
        parrilla.B = 3
        parrilla.L = 3
        parrilla.D = 2
        parrilla.C = 2
        TP = 0.6
        parrilla.θ = 8
        γ_r, φ_r = 16, 23
        parrilla.set_perfil(Perfil([
            Estrato(H_0=1.0, γ_s=20.0, E_s=6100, c_u=None, φ_s=35, saturado=False, tipo_mat="g",ν=0.3),
            Estrato(H_0=1.2, γ_s=21.0, E_s=8500, c_u=23, φ_s=38, saturado=False, tipo_mat="c",ν=0.4,C_s = 0.002,e_0 = 1.91, σ_pp = 90),
            Estrato(H_0=0.8, γ_s=15.0, E_s=15000, c_u=None, φ_s=25, saturado=False, tipo_mat="g",ν=0.45),
            Estrato(H_0=1.1, γ_s=12.0, E_s=12000, c_u=24, φ_s=25, saturado=False, tipo_mat="c",ν=0.4, C_s = 0.002,e_0 = 1.91, σ_pp = 90),
            Estrato(H_0=1.5, γ_s=15.0, E_s=8000, c_u=None, φ_s=31, saturado=True, tipo_mat="g",ν=0.35),
            
        ], γ_r=γ_r, φ_r=φ_r))
        parrilla.ajustar_perfil()
        t = 40
        k = 80
        F_zc = 1800

        S, memoria = parrilla.calculo_asentamiento_elastico_suelos_mixtos(F_zc, k, t)
        #print(memoria)
        self.assertAlmostEqual(memoria["iteraciones"][1]["S_e"], 0.0055, places =4)

    def test_calculo_asentamiento_elastico_suelos_mixtos2(self):
        
        parrilla = copy.deepcopy(self.parrilla_8)
        parrilla.B = 3
        parrilla.L = 3
        parrilla.D = 1.5
        parrilla.C = 2
        TP = 0.6
        parrilla.θ = 8
        parrilla.γ_c = 23.53
        γ_r, φ_r = 16, 23
        parrilla.set_perfil(Perfil([
            Estrato(H_0=1.0, γ_s=20.0, E_s=6100, c_u=None, φ_s=35, saturado=False, tipo_mat="g",ν=0.3),
            Estrato(H_0=1.2, γ_s=21.0, E_s=8500, c_u=23, φ_s=38, saturado=False, tipo_mat="c",ν=0.4, C_s = 0.002,e_0 = 1.91, σ_pp = 90),
            Estrato(H_0=0.8, γ_s=15.0, E_s=15000, c_u=None, φ_s=31, saturado=False, tipo_mat="g",ν=0.45),
            Estrato(H_0=1.1, γ_s=12.0, E_s=12000, c_u=24, φ_s=28, saturado=False, tipo_mat="c",ν=0.4, C_s = 0.002,e_0 = 1.91, σ_pp = 90),
            Estrato(H_0=1.5, γ_s=15.0, E_s=22000, c_u=None, φ_s=31, saturado=True, tipo_mat="g",ν=0.35),
        ], γ_r=γ_r, φ_r=φ_r))
        parrilla.ajustar_perfil()
        t = 40
        k = 80
        F_zc = 2000

        S, memoria = parrilla.calculo_asentamiento_elastico_suelos_mixtos(F_zc, k, t)
        #print(memoria)
        self.assertAlmostEqual(S, 0.0354, places =4)

    def test_calculo_asentamiento_elastico_suelos_mixtos3(self):
        
        parrilla = copy.deepcopy(self.parrilla_8)
        parrilla.B = 2.8
        parrilla.L = 2.8
        parrilla.D = 1.5
        parrilla.C = 2
        TP = 0.6
        parrilla.θ = 8
        parrilla.γ_c = 23.53
        γ_r, φ_r = 16, 23
        parrilla.set_perfil(Perfil([
            Estrato(H_0=1.0, γ_s=20.0, E_s=6100, c_u=None, φ_s=35, saturado=False, tipo_mat="g",ν=0.3),
            Estrato(H_0=1.2, γ_s=21.0, E_s=10500, c_u=23, φ_s=38, saturado=False, tipo_mat="c",ν=0.4, C_s = 0.002,e_0 = 1.91, σ_pp = 90),
            Estrato(H_0=0.8, γ_s=15.0, E_s=13000, c_u=None, φ_s=32, saturado=False, tipo_mat="g",ν=0.45),
            Estrato(H_0=1.1, γ_s=12.0, E_s=11000, c_u=24, φ_s=24, saturado=False, tipo_mat="c",ν=0.4, C_s = 0.002,e_0 = 1.91, σ_pp = 90),
            Estrato(H_0=1.5, γ_s=15.0, E_s=22000, c_u=None, φ_s=31, saturado=True, tipo_mat="g",ν=0.35),
            
        ], γ_r=γ_r, φ_r=φ_r))
        parrilla.ajustar_perfil()
        t = 40
        k = 80
        F_zc = 2000

        S, memoria = parrilla.calculo_asentamiento_elastico_suelos_mixtos(F_zc, k, t)
        #print(memoria)
        self.assertAlmostEqual(S, 0.0401, places =4)

    def test_calculo_asentamiento_elastico_suelos_mixtos4(self):
        
        parrilla = copy.deepcopy(self.parrilla_8)
        parrilla.B = 2.5
        parrilla.L = 2.5
        parrilla.D = 1.5
        parrilla.C = 2
        TP = 0.6
        parrilla.θ = 8
        parrilla.γ_c = 23.53
        γ_r, φ_r = 16, 23
        parrilla.set_perfil(Perfil([
            Estrato(H_0=1.0, γ_s=20.0, E_s=16100, c_u=None, φ_s=35, saturado=False, tipo_mat="g",ν=0.3),
            Estrato(H_0=1.5, γ_s=21.0, E_s=21500, c_u=23, φ_s=38, saturado=False, tipo_mat="c",ν=0.4, C_s = 0.002,e_0 = 1.91, σ_pp = 90),
            Estrato(H_0=0.8, γ_s=15.0, E_s=15000, c_u=None, φ_s=19, saturado=False, tipo_mat="g",ν=0.45),
            Estrato(H_0=1.6, γ_s=12.0, E_s=17000, c_u=24, φ_s=25, saturado=False, tipo_mat="c",ν=0.4, C_s = 0.002,e_0 = 1.91, σ_pp = 90),
            Estrato(H_0=1.5, γ_s=15.0, E_s=25000, c_u=None, φ_s=31, saturado=True, tipo_mat="g",ν=0.35),
            
        ], γ_r=γ_r, φ_r=φ_r))
        parrilla.ajustar_perfil()
        t = 40
        k = 80
        F_zc = 2000

        S, memoria = parrilla.calculo_asentamiento_elastico_suelos_mixtos(F_zc, k, t)
        #print(memoria)
        self.assertAlmostEqual(S, 0.0342, places =4)

    def test_calculo_asentamiento_elastico_suelos_mixtos5(self):
        
        parrilla = copy.deepcopy(self.parrilla_8)
        parrilla.B = 2.5
        parrilla.L = 2.5
        parrilla.D = 1.5
        parrilla.C = 2
        γ_r, φ_r = 16, 23
        parrilla.set_perfil(Perfil([
            Estrato(H_0=1.0, γ_s=20.0, E_s=16100, c_u=None, φ_s=35, saturado=False, tipo_mat="g",ν=0.3),
            Estrato(H_0=1.5, γ_s=21.0, E_s=21500, c_u=23, φ_s=38, saturado=False, tipo_mat="c",ν=0.4, C_s = 0.002,e_0 = 1.91, σ_pp = 90),
            Estrato(H_0=0.8, γ_s=15.0, E_s=15000, c_u=None, φ_s=36, saturado=False, tipo_mat="g",ν=0.45),
            Estrato(H_0=1.6, γ_s=12.0, E_s=17000, c_u=24, φ_s=31, saturado=False, tipo_mat="c",ν=0.4, C_s = 0.002,e_0 = 1.91, σ_pp = 90),
            Estrato(H_0=1.5, γ_s=15.0, E_s=25000, c_u=None, φ_s=31, saturado=True, tipo_mat="g",ν=0.35),
            
        ], γ_r=γ_r, φ_r=φ_r))
        parrilla.ajustar_perfil()
        t = 45
        k = 100
        F_zc = 2000

        S, memoria = parrilla.calculo_asentamiento_elastico_suelos_mixtos(F_zc, k, t)
        #print(memoria)
        self.assertAlmostEqual(S, 0.0344, places =4)
        
    def test_calculo_volcamiento(self):
        
        parrilla = copy.deepcopy(self.parrilla_5)
        parrilla.B = 4
        parrilla.L = 4
        parrilla.ajustar_perfil()

        F_zc =  275.23
        F = 39.3
        T_u = 900

        Mv, Me, memoria = parrilla.calculo_volcamiento_isa(F_zc, F, T_u)
        #print(memoria)
        self.assertAlmostEqual(Mv, 551.39 , places=2)
        self.assertAlmostEqual(Me, 1800.00 , places=2)

    def test_calculo_volcamiento2(self):
        
        parrilla = copy.deepcopy(self.parrilla_5)
        parrilla.B = 3
        parrilla.L = 3

        parrilla.ajustar_perfil()
                
        F_zc =  275.23
        F = 39.3
        T_u = 700

        Mv, Me, memoria = parrilla.calculo_volcamiento_isa(F_zc, F, T_u)
        #print(memoria)
        self.assertAlmostEqual(Mv, 413.77 , places=2)
        self.assertAlmostEqual(Me, 1050.00 , places=2)

    def test_calculo_volcamiento3(self):
        
        parrilla = copy.deepcopy(self.parrilla_5)
        parrilla.B = 3
        parrilla.L = 3
        parrilla.D = 2

        parrilla.ajustar_perfil()
                
        F_zc =  324.85
        F = 55.08
        T_u = 700

        Mv, Me, memoria = parrilla.calculo_volcamiento_isa(F_zc, F, T_u)
        #print(memoria)
        self.assertAlmostEqual(Mv, 501.41 , places=2)
        self.assertAlmostEqual(Me, 1050.00 , places=2)

    def test_calculo_volcamiento4(self):
        
        parrilla = copy.deepcopy(self.parrilla_5)
        parrilla.B = 2.5
        parrilla.L = 2.5
        parrilla.D = 2

        parrilla.ajustar_perfil()
                
        F_zc =  324.85
        F = 55.08
        T_u = 700

        Mv, Me, memoria = parrilla.calculo_volcamiento_isa(F_zc, F, T_u)
        #print(memoria)
        self.assertAlmostEqual(Mv, 420.20 , places=2)
        self.assertAlmostEqual(Me, 875.00, places=2)

    def test_calculo_volcamiento5(self):
        
        parrilla = copy.deepcopy(self.parrilla_5)
        parrilla.B = 2
        parrilla.L = 2
        parrilla.D = 2

        parrilla.ajustar_perfil()
                
        F_zc =  324.85
        F = 55.08
        T_u = 850

        Mv, Me, memoria = parrilla.calculo_volcamiento_isa(F_zc, F, T_u)
        #print(memoria)
        self.assertAlmostEqual(Mv, 338.99 , places=2)
        self.assertAlmostEqual(Me, 850.00 , places=2)

    def test_calculo_momento_carga_lateral(self):
        parrilla = copy.deepcopy(self.parrilla_4)
        parrilla.D = 1.9
        γ_r, φ_r = 16, 23
        parrilla.set_perfil(Perfil([
            Estrato(H_0 = 1.0, γ_s = 19.5, E_s = 6000, c_u = None, φ_s = 38, saturado = False, tipo_mat = 'g'),
            Estrato(H_0 = 1.0, γ_s = 19.5, E_s = 6000, c_u = None, φ_s = 38, saturado = False, tipo_mat = 'g'),
            Estrato(H_0 = 1.0, γ_s = 19.5, E_s = 6000, c_u = None, φ_s = 38, saturado = False, tipo_mat = 'g'),
            Estrato(H_0 = 1.0, γ_s = 19.5, E_s = 6000, c_u = None, φ_s = 38, saturado = False, tipo_mat = 'g'),
        ], γ_r=γ_r, φ_r=φ_r))

        F_c = 39.3
        Fz_c = 275.23   
        
        M_o, memoria = parrilla.calculo_carga_lateral_isa(F_c)
        #print(memoria)
        self.assertAlmostEqual(M_o, 143.70, places =2)

    def test_calculo_momento_carga_axial(self):
        parrilla = copy.deepcopy(self.parrilla_4)
        parrilla.D = 1.9
        γ_r, φ_r = 16.4, 23
        parrilla.set_perfil(Perfil([
            Estrato(H_0 = 1.0, γ_s = 19.5, E_s = 6000, c_u = None, φ_s = 38, saturado = False, tipo_mat = 'g'),
            Estrato(H_0 = 1.0, γ_s = 19.5, E_s = 6000, c_u = None, φ_s = 38, saturado = False, tipo_mat = 'g'),
            Estrato(H_0 = 1.0, γ_s = 19.5, E_s = 6000, c_u = None, φ_s = 38, saturado = False, tipo_mat = 'g'),
            Estrato(H_0 = 1.0, γ_s = 19.5, E_s = 6000, c_u = None, φ_s = 38, saturado = False, tipo_mat = 'g'),
        ], γ_r=γ_r, φ_r=φ_r))

        F_c = 39.3
        Fz_c = 275.23   
        
        M_o = parrilla.calculo_momento_carga_axial(Fz_c)
        
        self.assertAlmostEqual(M_o, -50.41, places =2)

    def test_calculo_momento_carga_lateral2(self):
        parrilla = copy.deepcopy(self.parrilla_4)
        parrilla.B = 5
        parrilla.L = 5
        parrilla.C =2
        parrilla.φ_r = 23
        γ_r, φ_r = 16, 23
        parrilla.set_perfil(Perfil([
            Estrato(H_0 = 1.0, γ_s = 19.5, E_s = 6000, c_u = None, φ_s = 38, saturado = False, tipo_mat = 'g'),
            Estrato(H_0 = 1.0, γ_s = 19.5, E_s = 6000, c_u = None, φ_s = 38, saturado = False, tipo_mat = 'g'),
            Estrato(H_0 = 1.0, γ_s = 19.5, E_s = 6000, c_u = None, φ_s = 38, saturado = False, tipo_mat = 'g'),
            Estrato(H_0 = 1.0, γ_s = 19.5, E_s = 6000, c_u = None, φ_s = 38, saturado = False, tipo_mat = 'g'),
        ], γ_r=γ_r, φ_r=φ_r))
        parrilla.ajustar_perfil()

        F_c = 39.3
        Fz_c = 251.34   
        
        M_o, memoria = parrilla.calculo_momento_carga_lateral(F_c)
        #print(memoria)
        self.assertAlmostEqual(M_o, 78.6, places =2)

    def test_calculo_momento_carga_axial2(self):
        parrilla = copy.deepcopy(self.parrilla_4)
        parrilla.B = 5
        parrilla.L = 5
        parrilla.C =2
        parrilla.φ_r = 23
        γ_r, φ_r = 16.4, 23
        parrilla.set_perfil(Perfil([
            Estrato(H_0 = 1.0, γ_s = 19.5, E_s = 6000, c_u = None, φ_s = 38, saturado = False, tipo_mat = 'g'),
            Estrato(H_0 = 1.0, γ_s = 19.5, E_s = 6000, c_u = None, φ_s = 38, saturado = False, tipo_mat = 'g'),
            Estrato(H_0 = 1.0, γ_s = 19.5, E_s = 6000, c_u = None, φ_s = 38, saturado = False, tipo_mat = 'g'),
            Estrato(H_0 = 1.0, γ_s = 19.5, E_s = 6000, c_u = None, φ_s = 38, saturado = False, tipo_mat = 'g'),
        ], γ_r=γ_r, φ_r=φ_r))
        parrilla.ajustar_perfil()

        F_c = 39.3
        Fz_c = 251.34   
        
        M_o = parrilla.calculo_momento_carga_axial(Fz_c)
        #print(memoria)
        self.assertAlmostEqual(M_o, -61.38, places =2)

    def test_calculo_momento_carga_lateral3(self):
        parrilla = copy.deepcopy(self.parrilla_4)
        
        F_c = 39.3
        Fz_c = 275.23   
        
        M_o, memoria = parrilla.calculo_momento_carga_lateral(F_c)
        print(memoria)
        self.assertAlmostEqual(M_o, 58.95, places =2)

    def test_calculo_momento_carga_axial3(self):
        parrilla = copy.deepcopy(self.parrilla_4)
        
        F_c = 39.3
        Fz_c = 275.23   
        
        M_o = parrilla.calculo_momento_carga_axial(Fz_c)
        self.assertAlmostEqual(M_o, -50.41, places =2)

    def test_calculo_momento_carga_lateral4(self):
        parrilla = copy.deepcopy(self.parrilla_4)
        
        F_c = 45.32
        Fz_c = 320.23   
        
        M_o, memoria = parrilla.calculo_momento_carga_lateral(F_c)
        #print(memoria)
        self.assertAlmostEqual(M_o, 67.98, places =2)

    def test_calculo_momento_carga_axial4(self):
        parrilla = copy.deepcopy(self.parrilla_4)
        
        F_c = 45.32
        Fz_c = 320.23   
        
        M_o = parrilla.calculo_momento_carga_axial(Fz_c)
        self.assertAlmostEqual(M_o, -58.65, places =2)
    
    def test_calculo_momento_carga_lateral5(self):
        parrilla = copy.deepcopy(self.parrilla_4)
        
        F_c = 71.42
        Fz_c = 268.58   
        
        M_o, memoria = parrilla.calculo_momento_carga_lateral(F_c)
        print(memoria)
        self.assertAlmostEqual(M_o, 107.13, places =2)

    def test_calculo_momento_carga_axial5(self):
        parrilla = copy.deepcopy(self.parrilla_4)
        
        F_c = 71.42
        Fz_c = 268.58   
        
        M_o = parrilla.calculo_momento_carga_axial(Fz_c)
        self.assertAlmostEqual(M_o, -49.19, places =2)

    def test_calculo_momento_carga_lateral6(self):
        parrilla = copy.deepcopy(self.parrilla_4)
        
        Fx_c = 350.85
        Fy_c = 400.24
        Fz_c = 500.56  
        F_c = Fx_c
        M_o, memoria = parrilla.calculo_momento_carga_lateral(F_c)
        print(memoria)
        self.assertAlmostEqual(M_o, 526.28, places =2)

    def test_calculo_momento_carga_lateral7(self):
        parrilla = copy.deepcopy(self.parrilla_4)
        
        Fx_c = 433.85
        Fy_c = 420.24
        Fz_c = 2005.41  
        F_c = Fx_c
        M_o, memoria = parrilla.calculo_momento_carga_lateral(F_c)
        print(memoria)
        self.assertAlmostEqual(M_o, 650.78, places =2)

    def test_calculo_momento_carga_lateral8(self):
        parrilla = copy.deepcopy(self.parrilla_4)
        
        Fx_c = 14.45
        Fy_c = 13.22
        Fz_c = 300.23  
        F_c = Fx_c
        M_o, memoria = parrilla.calculo_momento_carga_lateral(F_c)
        print(memoria)
        self.assertAlmostEqual(M_o, 21.67, places =2)

    def test_calculo_integral_presion_lateral_activa_desde_0_prueba_1(self):
        
        parrilla = copy.deepcopy(self.parrilla_1)
        parrilla.perfil = self.perfil10

        prof = 1.5
        prueba = parrilla.calculo_integral_presion_lateral_activa_desde_0(prof)
        self.assertAlmostEqual(prueba, 0.0,places=3)

    def test_calculo_integral_presion_lateral_activa_desde_0_prueba_2(self):
        
        parrilla = copy.deepcopy(self.parrilla_1)
        parrilla.perfil = self.perfil11

        prof = 1.5
        prueba = parrilla.calculo_integral_presion_lateral_activa_desde_0(prof)
        self.assertAlmostEqual(prueba, 9.878,places=3)

    def test_calculo_integral_presion_lateral_pasiva_desde_0_prueba_1(self):
        
        parrilla = copy.deepcopy(self.parrilla_1)
        parrilla.perfil = self.perfil11

        prof = 1.5
        prueba = parrilla.calculo_integral_presion_lateral_pasiva_desde_0(prof)
        self.assertAlmostEqual(prueba, 37.47,places=3)


    # def test_rendimiento(self):
    #     parrilla = copy.deepcopy(self.parrilla_8)
    #     parrilla.B = 2.5
    #     parrilla.L = 2.5  
    #     parrilla.ajustar_perfil()         
    #     F_zc = 450

    #     start = time.time()
    #     for i in range(800000):
    #         S, memoria = parrilla.calculo_asentamiento_elastico_suelos_mixtos(F_zc)
    #     end = time.time()
    #     print(end - start)

if __name__ == '__main__':
    unittest.main()