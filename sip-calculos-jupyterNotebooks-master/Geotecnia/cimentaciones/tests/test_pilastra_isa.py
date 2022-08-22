# pylint: disable=W
import unittest
import time
import copy
from ..perfil import Perfil, Estrato
from ..pilastra_isa import PilastraIsa

class TestCalculosPilastraIsa(unittest.TestCase):
    
    @classmethod
    def setUpClass(self):
        # pilastra 1
        D_p, H, HG, h_i = 1.3, 3, 2, 1
        TP = 0.6
        θ, γ_c = 6, 24
        ω, t = 0, 0
        γ_r, φ_r = 16.4, 35
        perfil = Perfil([
            Estrato(H_0 = 1.0, γ_s = 21.0, E_s = 6597, c_u = 29.36, φ_s = 24, saturado = False, tipo_mat = "g", c_p = 0),
            Estrato(H_0 = 9.0, γ_s = 20.0, E_s = 130000, c_u = None, φ_s = None, saturado = False, tipo_mat = "r", c_p = 0, roca_φ_rm = 40, RQD = 20, ucs= 10, roca_a = 0.59, roca_s = 0.0067,  roca_m = 1.804),
        ], γ_r=γ_r, φ_r=φ_r)
        self.pilastra_1 = PilastraIsa(h_i,D_p, H, HG, TP, θ, γ_c, perfil, ω)    

        # pilastra 2
        D_p, H, HG, h_i = 2, 5, 1.5, 1
        TP = 0.6
        θ, γ_c = 6, 24
        ω, t = 0, 0
        γ_r, φ_r = 16.4, 35
        perfil = Perfil([
            Estrato(H_0 = 1.0, γ_s = 21.0, E_s = 6597, c_u = 0, φ_s = 24, saturado = False, tipo_mat = "g", c_p = 0),
            Estrato(H_0 = 9.0, γ_s = 18.0, E_s = 120000, c_u = None, φ_s = 42, saturado = False, tipo_mat = "r", c_p = 0, roca_φ_rm = 42, RQD = 20, ucs= 10, roca_a = 0.59, roca_s = 0.0067,  roca_m = 1.804),
        ], γ_r=γ_r, φ_r=φ_r)
        self.pilastra_2 = PilastraIsa(h_i,D_p, H, HG, TP, θ, γ_c, perfil, ω) 

        # pilastra 3
        D_p, H, HG, h_i = 1.5, 3, 1.2, 1
        TP = 0.6
        θ, γ_c = 6, 24
        ω, t = 0, 0
        γ_r, φ_r = 16.4, 35
        perfil = Perfil([
            Estrato(H_0 = 0.8, γ_s = 24.0, E_s = 7200, c_u = 35.20, φ_s = 27, saturado = False, tipo_mat = "c", ν = 0.28, c_p = 20, C_s = 0.013,e_0 = 1.91, σ_pp = 90),
            Estrato(H_0 = 9.0, γ_s = 18.0, E_s = 115000, c_u = None, φ_s = 42, saturado = False, tipo_mat = "r", c_p = 0, roca_φ_rm = 42, RQD = 20, ucs= 10, roca_a = 0.59, roca_s = 0.0067,  roca_m = 1.804),
        ], γ_r=γ_r, φ_r=φ_r)
        self.pilastra_3 = PilastraIsa(h_i, D_p, H, HG, TP, θ, γ_c, perfil, ω) 

        # pilastra 3_5
        D_p, H, HG, h_i = 1.5, 3, 1, 1
        TP = 0.6
        θ, γ_c = 6, 24
        ω, t = 0, 0
        γ_r, φ_r = 16.4, 35
        perfil = Perfil([
            Estrato(H_0 = 0.8, γ_s = 24.0, E_s = 7200, c_u = 35.20, φ_s = 27, saturado = False, tipo_mat = "c", ν = 0.28, c_p = 20, C_s = 0.013,e_0 = 1.91, σ_pp = 90),
            Estrato(H_0 = 1.0, γ_s = 18.0, E_s = 115000, c_u = None, φ_s = 42, saturado = False, tipo_mat = "r", c_p = 8, roca_φ_rm = 42, RQD = 20, ucs= 12, roca_a = 0.59, roca_s = 0.0067,  roca_m = 1.804),
            Estrato(H_0 = 0.5, γ_s = 18.0, E_s = 115000, c_u = None, φ_s = 42, saturado = False, tipo_mat = "r", c_p = 8, roca_φ_rm = 42, RQD = 20, ucs= 11, roca_a = 0.59, roca_s = 0.0067,  roca_m = 1.804),
            Estrato(H_0 = 7.5, γ_s = 18.0, E_s = 115000, c_u = None, φ_s = 42, saturado = False, tipo_mat = "r", c_p = 8, roca_φ_rm = 42, RQD = 20, ucs= 13, roca_a = 0.59, roca_s = 0.0067,  roca_m = 1.804),
        ], γ_r=γ_r, φ_r=φ_r)
        self.pilastra_3_5 = PilastraIsa(h_i, D_p, H, HG, TP, θ, γ_c, perfil, ω)     

        # pilastra 4
        D_p, H, HG, h_i = 1.5, 5, 1.5, 1
        TP = 0.6
        θ, γ_c = 6, 24
        ω, t = 0, 0
        γ_r, φ_r = 16.4, 35
        perfil = Perfil([
            Estrato(H_0 = 0.8, γ_s = 24.0, E_s = 7200, c_u = 35.20, φ_s = 27, saturado = False, tipo_mat = "c", ν = 0.28, c_p = 20, C_s = 0.013,e_0 = 1.91, σ_pp = 90),
            Estrato(H_0 = 9.0, γ_s = 18.0, E_s = 115000, c_u = None, φ_s = 42, saturado = False, tipo_mat = "r", c_p = 0, roca_φ_rm = 42, RQD = 20, ucs= 12, roca_a = 0.59, roca_s = 0.0067,  roca_m = 1.804),
        ], γ_r=γ_r, φ_r=φ_r)
        self.pilastra_4 = PilastraIsa(h_i, D_p, H, HG, TP, θ, γ_c, perfil, ω)    

        # pilastra 5
        D_p, H, HG, h_i = 1.5, 5, 0.8, 1
        TP = 0.6
        θ, γ_c = 6, 24
        ω, t = 0, 0
        γ_r, φ_r = 16.4, 35
        perfil = Perfil([
            Estrato(H_0 = 0.8, γ_s = 24.0, E_s = 7200, c_u = 35.20, φ_s = 27, saturado = False, tipo_mat = "c", ν = 0.28, c_p = 20, C_s = 0.013,e_0 = 1.91, σ_pp = 90),
            Estrato(H_0 = 4.0, γ_s = 18.0, E_s = 115000, c_u = None, φ_s = 42, saturado = False, tipo_mat = "r", c_p = 0, roca_φ_rm = 42, RQD = 20, ucs= 13, roca_a = 0.59, roca_s = 0.0067,  roca_m = 1.804),
            Estrato(H_0 = 5.0, γ_s = 18.0, E_s = 115000, c_u = None, φ_s = 42, saturado = False, tipo_mat = "r", c_p = 0, roca_φ_rm = 42, RQD = 20, ucs= 14, roca_a = 0.59, roca_s = 0.0067,  roca_m = 1.804)
        ], γ_r=γ_r, φ_r=φ_r)
        self.pilastra_5 = PilastraIsa(h_i, D_p, H, HG, TP, θ, γ_c, perfil, ω)    

        # pilastra 6
        D_p, H, HG, h_i = 1.5, 5, 1.2, 1
        TP = 0.6
        θ, γ_c = 6, 24
        ω, t = 0, 0
        γ_r, φ_r = 16.4, 35
        perfil = Perfil([
            Estrato(H_0 = 0.8, γ_s = 24.0, E_s = 7200, c_u = 35.20, φ_s = 27, saturado = False, tipo_mat = "c", ν = 0.28, c_p = 20, C_s = 0.013,e_0 = 1.91, σ_pp = 90),
            Estrato(H_0 = 3.0, γ_s = 18.0, E_s = 115000, c_u = None, φ_s = 42, saturado = False, tipo_mat = "r", c_p = 0, roca_φ_rm = 42, RQD = 20, ucs= 15, roca_a = 0.59, roca_s = 0.0067,  roca_m = 1.804),
            Estrato(H_0 = 1.5, γ_s = 18.0, E_s = 115000, c_u = None, φ_s = 42, saturado = False, tipo_mat = "r", c_p = 0, roca_φ_rm = 42, RQD = 20, ucs= 16, roca_a = 0.59, roca_s = 0.0067,  roca_m = 1.804),
            Estrato(H_0 = 5.0, γ_s = 18.0, E_s = 115000, c_u = None, φ_s = 42, saturado = False, tipo_mat = "r", c_p = 0, roca_φ_rm = 42, RQD = 20, ucs= 17, roca_a = 0.59, roca_s = 0.0067,  roca_m = 1.804)
        ], γ_r=γ_r, φ_r=φ_r)
        self.pilastra_6 = PilastraIsa(h_i, D_p, H, HG, TP, θ, γ_c, perfil, ω)    

    @classmethod
    def tearDownClass(self):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_volumen(self):
                
        pilastra = copy.copy(self.pilastra_1)

        vol = pilastra.volumen()
        self.assertAlmostEqual(vol, 5.07, places=2)

    def test_volumen2(self):
                
        pilastra = copy.copy(self.pilastra_2)

        vol = pilastra.volumen()
        self.assertAlmostEqual(vol, 16.61, places=2)
    
    def test_volumen3(self):
                
        pilastra = copy.copy(self.pilastra_2)
        pilastra.D_p = 1.5
        pilastra.H = 3.8
        pilastra.HG = 0.5
        pilastra.TP = 0.5
        pilastra.θ = 8

        vol = pilastra.volumen()
        self.assertAlmostEqual(vol, 7.09, places=2)

    def test_volumen4(self):
                
        pilastra = copy.copy(self.pilastra_2)
        pilastra.D_p = 1.8
        pilastra.H = 2.5
        pilastra.HG = 0.7
        pilastra.TP = 0.5
        pilastra.θ = 5

        vol = pilastra.volumen()
        self.assertAlmostEqual(vol, 6.79, places=2)

    def test_volumen_relleno(self):
                
        pilastra = copy.copy(self.pilastra_2)
        pilastra.D_p = 1.5
        pilastra.TP = 0.5
        pilastra.θ = 8
        pilastra.h = 2

        vol = pilastra.volumen_relleno()
        self.assertAlmostEqual(vol, 1.51, places=2)

    def test_volumen_relleno2(self):
                
        pilastra = copy.copy(self.pilastra_2)
        pilastra.D_p = 2
        pilastra.TP = 0.6
        pilastra.θ = 10
        pilastra.h = 1.8

        vol = pilastra.volumen_relleno()
        self.assertAlmostEqual(vol, 2.78, places=2)

    def test_calculo_compresion(self):

        pilastra = copy.copy(self.pilastra_1)
        F_zc = 800

        P_adm, P_act, memoria = pilastra.calculo_compresion(F_zc)

        self.assertAlmostEqual(P_adm, 1942.47, places=2)
        self.assertAlmostEqual(P_act, 937.46, places=2)

    def test_calculo_compresion2(self):

        pilastra = copy.copy(self.pilastra_1)
        F_zc = 600

        P_adm, P_act, memoria = pilastra.calculo_compresion(F_zc)

        self.assertAlmostEqual(P_adm, 1942.47, places=2)
        self.assertAlmostEqual(P_act, 737.46, places=2)

    def test_calculo_compresion3(self):

        pilastra = copy.copy(self.pilastra_1)
        F_zc = 900

        P_adm, P_act, memoria = pilastra.calculo_compresion(F_zc)

        self.assertAlmostEqual(P_adm, 1942.47, places=2)
        self.assertAlmostEqual(P_act, 1037.46, places=2)

    def test_calculo_compresion4(self):

        pilastra = copy.copy(self.pilastra_2)
        F_zc = 900

        P_adm, P_act, memoria = pilastra.calculo_compresion(F_zc)

        self.assertAlmostEqual(P_adm, 4775.32, places=2)
        self.assertAlmostEqual(P_act, 1344.30, places=2)

    def test_calculo_compresion5(self):

        pilastra = copy.copy(self.pilastra_3)
        F_zc = 1000

        P_adm, P_act, memoria = pilastra.calculo_compresion(F_zc)

        self.assertAlmostEqual(P_adm, 2426.17, places=2)
        self.assertAlmostEqual(P_act, 1169.39, places=2)

    def test_calculo_compresion6(self):

        pilastra = copy.copy(self.pilastra_4)
        F_zc = 1000

        P_adm, P_act, memoria = pilastra.calculo_compresion(F_zc)

        self.assertAlmostEqual(P_adm, 3119.36, places=2)
        self.assertAlmostEqual(P_act, 1256.82, places=2)

    def test_calculo_resistencia_admisible_fuste(self):

        pilastra = copy.copy(self.pilastra_2)

        P_adm, memoria = pilastra.calculo_resistencia_admisible_fuste()


        self.assertAlmostEqual(P_adm, 2310.64, places=2)

    def test_calculo_resistencia_admisible_fuste2(self):

        pilastra = copy.copy(self.pilastra_4)
        pilastra.H = 5
        P_adm, memoria = pilastra.calculo_resistencia_admisible_fuste()


        self.assertAlmostEqual(P_adm, 1732.98, places=2)

    def test_calculo_resistencia_admisible_fuste3(self):

        pilastra = copy.copy(self.pilastra_5)
        pilastra.H = 5
        P_adm, memoria = pilastra.calculo_resistencia_admisible_fuste()


        self.assertAlmostEqual(P_adm, 1732.98, places=2)

    def test_calculo_resistencia_admisible_fuste4(self):

        pilastra = copy.copy(self.pilastra_6)
        pilastra.H = 5
        P_adm, memoria = pilastra.calculo_resistencia_admisible_fuste()

        self.assertAlmostEqual(P_adm, 1732.98, places=2)

    def test_calculo_tension(self):

        pilastra = copy.copy(self.pilastra_1)

        T_adm, memoria = pilastra.calculo_tension()

        self.assertAlmostEqual(T_adm, 1038.61, places=2)

    def test_calculo_tension2(self):

        pilastra = copy.copy(self.pilastra_2)

        T_adm, memoria = pilastra.calculo_tension()

        self.assertAlmostEqual(T_adm, 2754.94, places=2)

    def test_calculo_tension3(self):

        pilastra = copy.copy(self.pilastra_3)

        T_adm, memoria = pilastra.calculo_tension()

        self.assertAlmostEqual(T_adm, 1209.18, places=2)

    def test_calculo_tension4(self):

        pilastra = copy.copy(self.pilastra_3_5)

        T_adm, memoria = pilastra.calculo_tension()

        self.assertAlmostEqual(T_adm, 1207.44, places=2)

    def test_calculo_volcamiento(self):

        pilastra = copy.copy(self.pilastra_1)
        pilastra.H = 5
        pilastra.D_p = 1.3
        F_zc = 900
        F = 300
        Mv, Me, memoria = pilastra.calculo_volcamiento(F_zc, F)

        self.assertAlmostEqual(Me, 14137.50, places=2)
        self.assertAlmostEqual(Mv, 2701.22, places=2)

    def test_calculo_volcamiento2(self):

        pilastra = copy.copy(self.pilastra_1)
        pilastra.H = 3
        pilastra.D_p = 3
        F_zc = 800
        F = 250
        Mv, Me, memoria = pilastra.calculo_volcamiento(F_zc, F)

        self.assertAlmostEqual(Me, 14524.03, places=2)
        self.assertAlmostEqual(Mv, 2447.75, places=2)

    def test_calculo_volcamiento3(self):

        pilastra = copy.copy(self.pilastra_2)
        pilastra.H = 4
        pilastra.D_p = 3
        pilastra.HG = 1
        F_zc = 1000
        F = 350
        Mv, Me, memoria = pilastra.calculo_volcamiento(F_zc, F)

        self.assertAlmostEqual(Me, 24145.20, places=2)
        self.assertAlmostEqual(Mv, 3389.79, places=2)

    def test_calculo_volcamiento4(self):

        pilastra = copy.copy(self.pilastra_3)
        pilastra.H = 5
        pilastra.D_p = 3
        pilastra.HG = 1
        F_zc = 1200
        F = 360
        Mv, Me, memoria = pilastra.calculo_volcamiento(F_zc, F)

        self.assertAlmostEqual(Me, 38107.33, places=2)
        self.assertAlmostEqual(Mv, 4067.75, places=2)

    def test_calculo_volcamiento5(self):

        pilastra = copy.copy(self.pilastra_3_5)
        pilastra.H = 5
        pilastra.D_p = 3
        pilastra.HG = 1
        F_zc = 1200
        F = 360
        Mv, Me, memoria = pilastra.calculo_volcamiento(F_zc, F)

        self.assertAlmostEqual(Me, 48823.18, places=2)
        self.assertAlmostEqual(Mv, 4067.75, places=2)

    def test_calculo_volcamiento6(self):

        pilastra = copy.copy(self.pilastra_3)
        pilastra.H = 3.5
        pilastra.D_p = 2.2
        pilastra.HG = 1
        F_zc = 1200
        F = 360
        Mv, Me, memoria = pilastra.calculo_volcamiento(F_zc, F)

        self.assertAlmostEqual(Me, 14084.56, places=2)
        self.assertAlmostEqual(Mv, 3047.75, places=2)

    def test_calculo_carga_lateral(self):

        pilastra = copy.copy(self.pilastra_1)

        F_zc = 850
        
        Q_L, memoria = pilastra.calculo_carga_lateral(F_zc)

        self.assertAlmostEqual(Q_L, 4165.61, places=2) # 2981.39

    def test_calculo_carga_lateral2(self):

        pilastra = copy.copy(self.pilastra_1)

        F_zc = 1000
        
        Q_L, memoria = pilastra.calculo_carga_lateral(F_zc)

        self.assertAlmostEqual(Q_L, 4240.94, places=2) # 3056.72

    def test_calculo_carga_lateral3(self):

        pilastra = copy.copy(self.pilastra_2)

        F_zc = 850
        
        Q_L, memoria = pilastra.calculo_carga_lateral(F_zc)

        self.assertAlmostEqual(Q_L, 11095.12, places=2) # 10308

    def test_calculo_carga_lateral4(self):

        pilastra = copy.copy(self.pilastra_2)

        F_zc = 1000
        
        Q_L, memoria = pilastra.calculo_carga_lateral(F_zc)

        self.assertAlmostEqual(Q_L, 11174.88, places=2) # 10387.76

    def test_calculo_carga_lateral5(self):

        pilastra = copy.copy(self.pilastra_3)

        F_zc = 850
        
        Q_L, memoria = pilastra.calculo_carga_lateral(F_zc)

        self.assertAlmostEqual(Q_L, 4813.07, places=2) # 3562.57

    def test_calculo_carga_lateral6(self):

        pilastra = copy.copy(self.pilastra_3_5)

        F_zc = 850
        
        Q_L, memoria = pilastra.calculo_carga_lateral(F_zc)

        self.assertAlmostEqual(Q_L, 5468.05, places=2) #4069.56
        
    def test_calculo_carga_lateral7(self):

        pilastra = copy.copy(self.pilastra_3)

        F_zc = 1000
        
        Q_L, memoria = pilastra.calculo_carga_lateral(F_zc)

        self.assertAlmostEqual(Q_L, 4892.82, places=2) # 3642.32
        
    def test_calculo_integral_presion_lateral_pasiva(self):

        pilastra = copy.copy(self.pilastra_3)

        D = 3.8

        H = 3

        R_p = pilastra.calculo_integral_presion_lateral_pasiva(D - H, D)

        self.assertAlmostEqual(R_p, 2837.47, places=2) #691.25

    def test_calculo_integral_presion_lateral_pasiva2(self):

        pilastra = copy.copy(self.pilastra_3_5)

        D = 3.8

        H = 3

        R_p = pilastra.calculo_integral_presion_lateral_pasiva(D - H, D)

        self.assertAlmostEqual(R_p, 3256.21, places=2)

    def test_calculo_integral_presion_lateral_pasiva_desde_0_1(self):

        pilastra = copy.copy(self.pilastra_3)

        D = 3.8

        H = 3

        R_p = pilastra.calculo_integral_presion_lateral_pasiva_desde_0(D - H)

        self.assertAlmostEqual(R_p, 64.0, places=2)

    def test_calculo_integral_presion_lateral_pasiva_desde_0_2(self):

        pilastra = copy.copy(self.pilastra_3_5)

        D = 3.8

        H = 3

        R_p = pilastra.calculo_integral_presion_lateral_pasiva_desde_0(D - H)

        self.assertAlmostEqual(R_p, 64.00, places=2)

    def test_calculo_integral_presion_lateral_pasiva_desde_0_3(self):

        pilastra = copy.copy(self.pilastra_3)

        D = 3.8

        H = 3

        R_p = pilastra.calculo_integral_presion_lateral_pasiva_desde_0(D)

        self.assertAlmostEqual(R_p, 2901.47, places=2) #755.25

    def test_calculo_integral_presion_lateral_pasiva_desde_0_4(self):

        pilastra = copy.copy(self.pilastra_3_5)

        D = 3.8

        H = 3

        R_p = pilastra.calculo_integral_presion_lateral_pasiva_desde_0(D)

        self.assertAlmostEqual(R_p, 3320.21, places=2) #867.91

    def test_calcular_areas_por_brazos(self):

        pilastra = copy.copy(self.pilastra_1)
        pilastra.H = 5
        D = 6
        H = 5
        
        areas_por_brazos = pilastra.calcular_areas_por_brazos(D)
        acum = pilastra.calculo_integral_presion_lateral_pasiva(D - H, D)

        centroide = areas_por_brazos / acum

        self.assertAlmostEqual(centroide, 1.91, places=2)

    
        