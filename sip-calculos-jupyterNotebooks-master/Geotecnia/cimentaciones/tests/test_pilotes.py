import unittest
import time
import copy
from ..perfil import Perfil, Estrato
from ..pilotes import Pilotes

class TestCalculosPilotes(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        
        #Pilotes 1
        D_f, H_z = 1.5, 0.5
        n, S_p = 4, 0.3
        D_p, H, HG = 1.0, 5, 0.5
        h_c, h_con, θ_c = None, None, None            
        TP, θ, γ_c = 0.6, 8 , 24
        E_p = 29000000
        d_bor = 0.3
        f_carga_p = 1
        hincado = False
        campana = False 
        ω = 0
        perfil = Perfil([
            Estrato(H_0 = 5.0, γ_s = 21.0, E_s = 6597, c_u = 0, φ_s = 24, saturado = False, tipo_mat = "g", ν = 0.3, c_p = 0),
            Estrato(H_0 = 5.0, γ_s = 21.0, E_s = 7000, c_u = 0, φ_s = 27, saturado = False, tipo_mat = "g", ν = 0.35, c_p = 0),
            Estrato(H_0 = 5.0, γ_s = 20.0, E_s = 130000, c_u = None, φ_s = None, saturado = False, tipo_mat = "r", ν = 0.4, c_p = 0, roca_φ_rm = 40, RQD = 20, roca_E_rm = 130000),
        ])
        self.pilotes_1 = Pilotes(D_f, H_z, n, S_p, D_p, H, HG, h_c, h_con, θ_c, TP, θ, γ_c, E_p, d_bor, f_carga_p, perfil, hincado, campana, ω)

        #Pilotes 2
        D_f, H_z = 1.5, 0.5
        n, S_p = 4, 3.6
        D_p, H, HG = 1.2, 4, 0.5
        h_c, h_con, θ_c = None, None, None
        TP, θ, γ_c = 0.6, 8 , 24
        E_p = 29000000
        d_bor = 0.3              
        f_carga_p = 1
        hincado = False
        campana = False
        ω = 0
        perfil = Perfil([
            Estrato(H_0 = 1.0, γ_s = 21.0, E_s = 9324, c_u = 0, φ_s = 24, saturado = False, tipo_mat = "g",ν = 0.4, c_p = 0),
            Estrato(H_0 = 1.4, γ_s = 21.0, E_s = 15000, c_u = 0, φ_s = 24, saturado = False, tipo_mat = "g", ν = 0.35,c_p = 0),
            Estrato(H_0 = 1.9, γ_s = 19.0, E_s = 5000, c_u = 24.63, φ_s = 20, saturado = False, tipo_mat = "c", ν = 0.3,c_p = 0, C_s = 1,e_0 = 1.91, σ_pp = 90),
            Estrato(H_0 = 2.0, γ_s = 19.0, E_s = 7500, c_u = 24.63, φ_s = 20, saturado = False, tipo_mat = "c", ν = 0.3,c_p = 0, C_s = 1,e_0 = 1.91, σ_pp = 90),
            Estrato(H_0 = 2.0, γ_s = 19.0, E_s = 7500, c_u = 24.63, φ_s = 20, saturado = False, tipo_mat = "c", ν = 0.3,c_p = 0, C_s = 1,e_0 = 1.91, σ_pp = 90),
            Estrato(H_0 = 1.0, γ_s = 21.0, E_s = 9000, c_u = 0, φ_s = 24, saturado = False, tipo_mat = "g", ν = 0.35,c_p = 0),
            Estrato(H_0 = 2.0, γ_s = 21.0, E_s = 10000, c_u = 0, φ_s = 25, saturado = False, tipo_mat = "g", ν = 0.35,c_p = 0),
            Estrato(H_0 = 6.5, γ_s = 24.0, E_s = 130000, c_u = None, φ_s = None, saturado = False, tipo_mat = "r", ν = 0.4, c_p = 0, roca_φ_rm = 40, RQD = 20, roca_E_rm = 130000),
        ])
        self.pilotes_2 = Pilotes(D_f, H_z, n, S_p, D_p, H, HG, h_c, h_con, θ_c, TP, θ, γ_c, E_p, d_bor, f_carga_p, perfil, hincado, campana, ω)

        #Pilotes 3
        D_f, H_z = 1.5, 0.5
        n, S_p = 5, 3.6
        D_p, H, HG = 1.4, 8.1, 1
        h_c, h_con, θ_c = None, None, None            
        TP, θ, γ_c = 0.6, 8 , 24
        E_p = 29000000
        d_bor = 0.3
        f_carga_p = 1
        hincado = False
        campana = False
        ω = 0
        perfil = Perfil([
            Estrato(H_0 = 1.5, γ_s = 21.0, E_s = 9324, c_u = 0, φ_s = 32, saturado = False, tipo_mat = "g", ν = 0.3, c_p = 0),
            Estrato(H_0 = 1.0, γ_s = 21.0, E_s = 15000, c_u = 0, φ_s = 28, saturado = False, tipo_mat = "g", ν = 0.3, c_p = 0),
            Estrato(H_0 = 1.7, γ_s = 19.0, E_s = 5000, c_u = 24.63, φ_s = 25, saturado = False, tipo_mat = "c", ν = 0.3, c_p = 20, C_s = 0.014,e_0 = 1.91, σ_pp = 90),
            Estrato(H_0 = 1.5, γ_s = 18.0, E_s = 12000, c_u = 26.13, φ_s = 22, saturado = False, tipo_mat = "c", ν = 0.3,  c_p = 15, C_s = 0.015,e_0 = 1.91, σ_pp = 90),
            Estrato(H_0 = 1.1, γ_s = 18.0, E_s = 12000, c_u = 26.13, φ_s = 22, saturado = False, tipo_mat = "c", ν = 0.3,  c_p = 15, C_s = 0.015,e_0 = 1.91, σ_pp = 90),
            Estrato(H_0 = 3.5, γ_s = 18.0, E_s = 12000, c_u = 26.13, φ_s = 22, saturado = False, tipo_mat = "c", ν = 0.3,  c_p = 15, C_s = 0.015,e_0 = 1.91, σ_pp = 90),
            # Estrato(H_0 = 3.5, γ_s = 24.0, E_s = 130000, c_u = None, φ_s = None, saturado = False, tipo_mat = "r", ν = 0.3, c_p = 0, roca_φ_rm = 40, RQD = 20, roca_E_rm = 130000),
        ])
        self.pilotes_3 = Pilotes(D_f, H_z, n, S_p, D_p, H, HG, h_c, h_con, θ_c, TP, θ, γ_c, E_p, d_bor, f_carga_p, perfil, hincado, campana, ω)

        #Pilotes 4
        D_f, H_z = 1.5, 0.5
        n, S_p = 8, 0.3
        D_p, H, HG = 1.5, 2.5, 1
        h_c, h_con, θ_c = None, None, None          
        TP, θ, γ_c = 0.6, 8 , 24
        E_p = 29000000
        d_bor = 0.3
        f_carga_p = 1
        hincado = False
        campana = False
        ω = 0
        perfil = Perfil([
            Estrato(H_0 = 1.5, γ_s = 21.0, E_s = 9324, c_u = 0, φ_s = 32, saturado = False, tipo_mat = "g",ν = 0.3, c_p = 0),
            Estrato(H_0 = 1.0, γ_s = 21.0, E_s = 15000, c_u = 0, φ_s = 28, saturado = False, tipo_mat = "g", ν = 0.2, c_p = 0),
            Estrato(H_0 = 1.2, γ_s = 19.0, E_s = 9324, c_u = 0, φ_s = 32, saturado = False, tipo_mat = "g", ν = 0.4, c_p = 0),
            Estrato(H_0 = 1.3, γ_s = 18.4, E_s = 13200, c_u = 0, φ_s = 27, saturado = False, tipo_mat = "g", ν = 0.3, c_p = 0),
            Estrato(H_0 = 1.2, γ_s = 19.0, E_s = 9324, c_u = 0, φ_s = 32, saturado = False, tipo_mat = "g", ν = 0.4, c_p = 0),
            Estrato(H_0 = 1.3, γ_s = 18.4, E_s = 13200, c_u = 0, φ_s = 27, saturado = False, tipo_mat = "g", ν = 0.3, c_p = 0),
            Estrato(H_0 = 1.7, γ_s = 21.0, E_s = 11000, c_u = 24.63, φ_s = 26, saturado = False, tipo_mat = "c", ν = 0.3, c_p = 20, C_s = 0.014,e_0 = 1.91, σ_pp = 90),
            Estrato(H_0 = 3.5, γ_s = 24.0, E_s = 130000, c_u = None, φ_s = None, saturado = False, tipo_mat = "r", c_p = 0, ν = 0.3, roca_φ_rm = 40, RQD = 20, roca_E_rm = 130000),
        ])
        self.pilotes_4 = Pilotes(D_f, H_z, n, S_p, D_p, H, HG, h_c, h_con, θ_c, TP, θ, γ_c, E_p, d_bor, f_carga_p, perfil, hincado, campana, ω)

        #Pilotes 5
        D_f, H_z = 1.5, 0.5
        n, S_p = 4, 0.3
        D_p, H, HG = 0.8, 3.5, 1
        h_c, h_con, θ_c = None, None, None     
        TP, θ, γ_c = 0.6, 8,  24
        E_p = 29000000
        d_bor = 0.3
        f_carga_p = 1
        hincado = False
        campana = False
        ω = 0
        perfil = Perfil([
            Estrato(H_0 = 1.2, γ_s = 19.0, E_s = 5000, c_u = 25.12, φ_s = 23, saturado = False, tipo_mat = "c", ν = 0.28, c_p = 20, C_s = 0.013,e_0 = 1.91, σ_pp = 90),
            Estrato(H_0 = 1.5, γ_s = 17.0, E_s = 14500, c_u = 26.13, φ_s = 24, saturado = False, tipo_mat = "c", ν = 0.32, c_p = 15, C_s = 0.015,e_0 = 1.91, σ_pp = 85),
            Estrato(H_0 = 1.6, γ_s = 19.0, E_s = 5000, c_u = 24.63, φ_s = 28, saturado = False, tipo_mat = "c", ν = 0.27, c_p = 20, C_s = 0.014,e_0 = 1.91, σ_pp = 112),
            Estrato(H_0 = 1.5, γ_s = 18.0, E_s = 12000, c_u = 19.42, φ_s = 22, saturado = False, tipo_mat = "c", ν = 0.3, c_p = 15, C_s = 0.017,e_0 = 1.91, σ_pp = 68),
            Estrato(H_0 = 1.2, γ_s = 19.0, E_s = 5000, c_u = 25.12, φ_s = 23, saturado = False, tipo_mat = "c", ν = 0.28, c_p = 20, C_s = 0.013,e_0 = 1.91, σ_pp = 90),
            Estrato(H_0 = 1.5, γ_s = 17.0, E_s = 14500, c_u = 26.13, φ_s = 24, saturado = False, tipo_mat = "c", ν = 0.32, c_p = 15, C_s = 0.015,e_0 = 1.91, σ_pp = 85),
            Estrato(H_0 = 1.7, γ_s = 18.4, E_s = 13200, c_u = 0, φ_s = 27, saturado = False, tipo_mat = "g", ν = 0.3, c_p = 0),
            Estrato(H_0 = 2.1, γ_s = 19.0, E_s = 9324, c_u = 0, φ_s = 32, saturado = False, tipo_mat = "g", ν = 0.4, c_p = 0),
            Estrato(H_0 = 3.5, γ_s = 24.0, E_s = 130000, c_u = None, φ_s = None, saturado = False, tipo_mat = "r", ν = 0.32, c_p = 0, roca_φ_rm = 40, RQD = 20,roca_E_rm = 130000),
        ])
        self.pilotes_5 = Pilotes(D_f, H_z, n, S_p, D_p, H, HG, h_c, h_con, θ_c, TP, θ, γ_c, E_p, d_bor, f_carga_p, perfil, hincado, campana, ω)

        #Pilotes 6
        D_f, H_z = 1.5, 0.5
        n, S_p = 4, 2.1
        D_p, H, HG = 0.7, 6, 1.5
        h_c, h_con, θ_c = None, None, None            
        TP, θ, γ_c = 0.6, 8 , 24
        E_p = 29000000
        d_bor = 0.3
        f_carga_p = 1
        hincado = False
        campana = False
        ω = 0
        perfil = Perfil([
            Estrato(H_0 = 1.0, γ_s = 18.0, E_s = 5000, c_u = None, φ_s = 23, saturado = False, tipo_mat = "g",ν = 0.4, c_p = 0),
            Estrato(H_0 = 1.5, γ_s = 17.5, E_s = 14500, c_u = 26.13, φ_s = 24, saturado = False, tipo_mat = "c",ν = 0.25, c_p = 15, C_s = 0.015,e_0 = 1.91, σ_pp = 85),
            Estrato(H_0 = 1.7, γ_s = 19.2, E_s = 5000, c_u = None, φ_s = 28, saturado = False, tipo_mat = "g",ν = 0.32, c_p = 0),
            Estrato(H_0 = 1.2, γ_s = 18.1, E_s = 12000, c_u = 19.42, φ_s = 22, saturado = False, tipo_mat = "c",ν = 0.35, c_p = 15, C_s = 0.017,e_0 = 1.91, σ_pp = 68),
            Estrato(H_0 = 3.5, γ_s = 22.4, E_s = 13000, c_u = None, φ_s = 31, saturado = False, tipo_mat = "g",ν = 0.3, c_p = 0),
        ])
        self.pilotes_6 = Pilotes(D_f, H_z, n, S_p, D_p, H, HG, h_c, h_con, θ_c, TP, θ, γ_c, E_p, d_bor, f_carga_p, perfil, hincado, campana, ω)

        #Pilotes 7
        D_f, H_z = 1.5, 0.5
        n, S_p = 5, 0.3
        D_p, H, HG = 1.3, 2.8, 1.5
        h_c, h_con, θ_c = None, None, None          
        TP, θ, γ_c = 0.6, 8 , 24
        E_p = 29000000
        d_bor = 0.3
        f_carga_p = 1
        hincado = False
        campana = False
        ω = 0
        perfil = Perfil([
            Estrato(H_0 = 1.5, γ_s = 21.0, E_s = 9324, c_u = 0, φ_s = 32, saturado = False, tipo_mat = "g",ν = 0.3, c_p = 0),
            Estrato(H_0 = 1.0, γ_s = 21.0, E_s = 15000, c_u = 0, φ_s = 26, saturado = False, tipo_mat = "g", ν = 0.2, c_p = 0),
            Estrato(H_0 = 1.2, γ_s = 19.0, E_s = 9324, c_u = 0, φ_s = 32, saturado = False, tipo_mat = "g", ν = 0.4, c_p = 0),
            Estrato(H_0 = 1.4, γ_s = 18.0, E_s = 7000, c_u = 24.63, φ_s = 26, saturado = False, tipo_mat = "c", ν = 0.4, c_p = 18, C_s = 0.014,e_0 = 1.91, σ_pp = 112),
            Estrato(H_0 = 1.7, γ_s = 18.4, E_s = 13200, c_u = 0, φ_s = 29, saturado = False, tipo_mat = "g", ν = 0.3, c_p = 0),
            Estrato(H_0 = 1.5, γ_s = 19.0, E_s = 5000, c_u = 25.12, φ_s = 23, saturado = False, tipo_mat = "c", ν = 0.28, c_p = 20, C_s = 0.013,e_0 = 1.91, σ_pp = 90),
            Estrato(H_0 = 1.6, γ_s = 17.0, E_s = 14500, c_u = 26.13, φ_s = 24, saturado = False, tipo_mat = "c", ν = 0.32, c_p = 15, C_s = 0.015,e_0 = 1.91, σ_pp = 85),
            Estrato(H_0 = 1.9, γ_s = 18.4, E_s = 13200, c_u = 0, φ_s = 27, saturado = False, tipo_mat = "g", ν = 0.3, c_p = 0),
            Estrato(H_0 = 3.5, γ_s = 24.0, E_s = 130000, c_u = None, φ_s = None, saturado = False, tipo_mat = "r", c_p = 0, ν = 0.3, roca_φ_rm = 40, RQD = 20, roca_E_rm = 130000),
        ])
        self.pilotes_7 = Pilotes(D_f, H_z, n, S_p, D_p, H, HG, h_c, h_con, θ_c, TP, θ, γ_c, E_p, d_bor, f_carga_p, perfil, hincado, campana, ω)

    @classmethod
    def tearDownClass(self):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_calcular_φ(self):
        pilotes = copy.copy(self.pilotes_4)
        φ = pilotes.calcular_φ(2.5, 4)

        self.assertAlmostEqual(φ, 27.49, places=2 )

    def test_volumen(self):
        
        pilotes = self.pilotes_1
        vol = pilotes.volumen_cimentacion()

        self.assertAlmostEqual(vol, 18.06, places=2)

    def test_volumen2(self):
        
        pilotes = self.pilotes_2
        vol = pilotes.volumen_cimentacion()

        self.assertAlmostEqual(vol, 33.22, places=2)

    def test_calculo_de_capacidad_portante_pilote(self):

        pilotes = self.pilotes_3
        
        _, Q_p, Q_s, memoria_p, memoria_s = pilotes.calculo_capacidad_portante_pilote()
        # print(memoria_p)
        # print(memoria_s)
        self.assertAlmostEqual(Q_p, 362.02, places=2)
        self.assertAlmostEqual(Q_s, 835.96, places=2)

    def test_calculo_de_capacidad_portante_punta_granular(self):
        pilotes = self.pilotes_4
        D_p = D_c = pilotes.D_p
        Q_p, memoria = pilotes.calculo_de_capacidad_portante_punta_granular(D_c)
        print(memoria)

        self.assertAlmostEqual(Q_p, 1557.09, places = 2)

    def test_calculo_de_capacidad_portante_punta_granular2(self):
        pilotes = self.pilotes_6
        D_p = D_c = pilotes.D_p
        Q_p, memoria = pilotes.calculo_de_capacidad_portante_punta_granular(D_c)
        print(memoria)

        self.assertAlmostEqual(Q_p, 812.76, places = 2)

    def test_calculo_de_capacidad_portante_punta_granular3(self):
        pilotes = copy.copy(self.pilotes_4)
        D_p = D_c = pilotes.D_p
        pilotes.H = 1.5
        
        Q_p, memoria = pilotes.calculo_de_capacidad_portante_punta_granular(D_c)
        print(memoria)

        self.assertAlmostEqual(Q_p, 1226.67, places = 2)

    def test_calculo_de_capacidad_portante_punta_granular4(self):
        pilotes = copy.copy(self.pilotes_4)
        D_p = D_c = pilotes.D_p
                
        Q_p, memoria = pilotes.calculo_de_capacidad_portante_punta_granular(D_c)
        print(memoria)

        self.assertAlmostEqual(Q_p, 1557.09, places = 2)

    def test_calculo_de_capacidad_portante_punta_granular5(self):
        pilotes = copy.copy(self.pilotes_4)
        
        D_c = 2.3
        
        Q_p, memoria = pilotes.calculo_de_capacidad_portante_punta_granular(D_c)
        print(memoria)

        self.assertAlmostEqual(Q_p, 3166.00, places = 2)

    def test_calculo_de_capacidad_portante_punta_granular6(self):
        pilotes = copy.copy(self.pilotes_4)
        
        D_c = 1.5
        
        Q_p, memoria = pilotes.calculo_de_capacidad_portante_punta_granular(D_c)
        print(memoria)

        self.assertAlmostEqual(Q_p, 1557.09, places = 2)

    def test_calculo_de_capacidad_portante_punta_granular7(self):
        pilotes = copy.copy(self.pilotes_4)
        D_c = 1.1
        
        Q_p, memoria = pilotes.calculo_de_capacidad_portante_punta_granular(D_c)
        print(memoria)

        self.assertAlmostEqual(Q_p, 801.01, places = 2)

    def test_calculo_de_capacidad_portante_punta_granular8(self):
        pilotes = copy.copy(self.pilotes_4)
        D_c = 1.7
        pilotes.TP = 0.7
        
        pilotes.set_perfil(Perfil([
            Estrato(H_0 = 1.5, γ_s = 21.0, E_s = 9324, c_u = 0, φ_s = 25, saturado = False, tipo_mat = "g",ν = 0.3, c_p = 0),
            Estrato(H_0 = 1.0, γ_s = 21.0, E_s = 15000, c_u = 0, φ_s = 22, saturado = False, tipo_mat = "g", ν = 0.2, c_p = 0),
            Estrato(H_0 = 1.2, γ_s = 19.0, E_s = 9324, c_u = 0, φ_s = 21, saturado = False, tipo_mat = "g", ν = 0.4, c_p = 0),
            Estrato(H_0 = 1.3, γ_s = 18.4, E_s = 13200, c_u = 0, φ_s = 23, saturado = False, tipo_mat = "g", ν = 0.3, c_p = 0),
            Estrato(H_0 = 3.5, γ_s = 24.0, E_s = 130000, c_u = None, φ_s = None, saturado = False, tipo_mat = "r", c_p = 0, ν = 0.3, roca_φ_rm = 40, RQD = 20),
        ]))

        Q_p, memoria = pilotes.calculo_de_capacidad_portante_punta_granular(D_c)
        print(memoria)

        self.assertAlmostEqual(Q_p, 843.85, places = 2)

    def test_calculo_de_capacidad_portante_punta_granular9(self):
        pilotes = copy.copy(self.pilotes_4)
        D_c = 1.5
        
        pilotes.TP = 0.7
        
        pilotes.set_perfil(Perfil([
            Estrato(H_0 = 1.5, γ_s = 22.0, E_s = 9324, c_u = 0, φ_s = 28, saturado = False, tipo_mat = "g",ν = 0.3, c_p = 0),
            Estrato(H_0 = 1.0, γ_s = 21.0, E_s = 15000, c_u = 0, φ_s = 25, saturado = False, tipo_mat = "g", ν = 0.2, c_p = 0),
            Estrato(H_0 = 1.2, γ_s = 19.5, E_s = 9324, c_u = 0, φ_s = 23, saturado = False, tipo_mat = "g", ν = 0.4, c_p = 0),
            Estrato(H_0 = 1.3, γ_s = 19.2, E_s = 13200, c_u = 0, φ_s = 25, saturado = False, tipo_mat = "g", ν = 0.3, c_p = 0),
            Estrato(H_0 = 3.5, γ_s = 24.0, E_s = 130000, c_u = None, φ_s = None, saturado = False, tipo_mat = "r", c_p = 0, ν = 0.3, roca_φ_rm = 40, RQD = 20),
        ]))

        Q_p, memoria = pilotes.calculo_de_capacidad_portante_punta_granular(D_c)
        print(memoria)

        self.assertAlmostEqual(Q_p, 734.78, places = 2)

    def test_calculo_de_capacidad_portante_punta_granular_10(self):
        pilotes = copy.copy(self.pilotes_4)
        D_c = 1.2
        pilotes.TP = 0.7
        
        pilotes.set_perfil(Perfil([
            Estrato(H_0 = 1.5, γ_s = 22.0, E_s = 9324, c_u = 0, φ_s = 28, saturado = False, tipo_mat = "g",ν = 0.3, c_p = 0),
            Estrato(H_0 = 1.0, γ_s = 21.0, E_s = 15000, c_u = 0, φ_s = 25, saturado = False, tipo_mat = "g", ν = 0.2, c_p = 0),
            Estrato(H_0 = 1.2, γ_s = 19.5, E_s = 9324, c_u = 0, φ_s = 23, saturado = False, tipo_mat = "g", ν = 0.4, c_p = 0),
            Estrato(H_0 = 1.3, γ_s = 19.2, E_s = 13200, c_u = 0, φ_s = 25, saturado = False, tipo_mat = "g", ν = 0.3, c_p = 0),
            Estrato(H_0 = 3.5, γ_s = 24.0, E_s = 130000, c_u = None, φ_s = None, saturado = False, tipo_mat = "r", c_p = 0, ν = 0.3, roca_φ_rm = 40, RQD = 20),
        ]))

        Q_p, memoria = pilotes.calculo_de_capacidad_portante_punta_granular(D_c)
        print(memoria)

        self.assertAlmostEqual(Q_p, 470.26, places = 2)

    def test_calculo_de_capacidad_portante_punta_granular_11(self):
        pilotes = copy.copy(self.pilotes_4)
        D_c = 1.0
        pilotes.TP = 0.7
        
        pilotes.set_perfil(Perfil([
            Estrato(H_0 = 1.5, γ_s = 22.0, E_s = 9324, c_u = 0, φ_s = 28, saturado = False, tipo_mat = "g",ν = 0.3, c_p = 0),
            Estrato(H_0 = 1.0, γ_s = 21.0, E_s = 15000, c_u = 0, φ_s = 25, saturado = False, tipo_mat = "g", ν = 0.2, c_p = 0),
            Estrato(H_0 = 1.2, γ_s = 19.5, E_s = 9324, c_u = 0, φ_s = 23, saturado = False, tipo_mat = "g", ν = 0.4, c_p = 0),
            Estrato(H_0 = 1.3, γ_s = 19.2, E_s = 13200, c_u = 0, φ_s = 25, saturado = False, tipo_mat = "g", ν = 0.3, c_p = 0),
            Estrato(H_0 = 3.5, γ_s = 24.0, E_s = 130000, c_u = None, φ_s = None, saturado = False, tipo_mat = "r", c_p = 0, ν = 0.3, roca_φ_rm = 40, RQD = 20),
        ]))

        Q_p, memoria = pilotes.calculo_de_capacidad_portante_punta_granular(D_c)
        print(memoria)

        self.assertAlmostEqual(Q_p,326.57, places = 2)

    def test_calculo_de_capacidad_portante_punta_cohesivo(self):
        pilotes = copy.copy(self.pilotes_5)
        D_c = pilotes.D_p
        Q_p, memoria = pilotes.calculo_de_capacidad_portante_punta_cohesivo(D_c)
        print(memoria)

        self.assertAlmostEqual(Q_p, 78.01, places = 2)

    def test_calculo_de_capacidad_portante_punta_cohesivo2(self):
        pilotes = copy.copy(self.pilotes_5)
        
        D_c = 1.6
        Q_p, memoria = pilotes.calculo_de_capacidad_portante_punta_cohesivo(D_c)
        print(memoria)

        self.assertAlmostEqual(Q_p, 357.17, places = 2)

    def test_calculo_de_capacidad_portante_punta_cohesivo3(self):
        pilotes = copy.copy(self.pilotes_3)
        
        D_c = 0.9
        Q_p, memoria = pilotes.calculo_de_capacidad_portante_punta_cohesivo(D_c)
        print(memoria)

        self.assertAlmostEqual(Q_p, 149.61, places = 2)

    def test_calculo_de_capacidad_portante_punta_cohesivo4(self):
        pilotes = copy.copy(self.pilotes_3)
        
        D_c = 1.4
        Q_p, memoria = pilotes.calculo_de_capacidad_portante_punta_cohesivo(D_c)
        print(memoria)

        self.assertAlmostEqual(Q_p, 362.02, places = 2)

    def test_calculo_de_capacidad_portante_punta_cohesivo5(self):
        pilotes = copy.copy(self.pilotes_5)
        D_c = 1.7
        Q_p, memoria = pilotes.calculo_de_capacidad_portante_punta_cohesivo(D_c)
        print(memoria)

        self.assertAlmostEqual(Q_p, 406.55, places = 2)

    def test_calculo_de_capacidad_portante_fuste(self):
        pilotes = copy.copy(self.pilotes_3)
        D_p = pilotes.D_p
        Q_s, memoria = pilotes.calculo_de_capacidad_portante_fuste(D_p)
        print(memoria)

        self.assertAlmostEqual(Q_s, 835.96, places = 2)

    def test_calculo_de_capacidad_portante_fuste2(self):
        pilotes = copy.copy(self.pilotes_3)
        D_p = 2.6
        Q_s, memoria = pilotes.calculo_de_capacidad_portante_fuste(D_p)
        print(memoria)

        self.assertAlmostEqual(Q_s, 1552.50, places = 2)

    def test_calculo_de_capacidad_portante_fuste3(self):
        pilotes = copy.copy(self.pilotes_3)
        D_p = 2.6
        pilotes.H = 2
        Q_s, memoria = pilotes.calculo_de_capacidad_portante_fuste(D_p)
        print(memoria)

        self.assertAlmostEqual(Q_s, 259.13, places = 2)

    def test_calculo_de_capacidad_portante_fuste4(self):
        pilotes = copy.copy(self.pilotes_3)
        D_p = 2.6
        
        pilotes.H = 3
        Q_s, memoria = pilotes.calculo_de_capacidad_portante_fuste(D_p)
        print(memoria)

        self.assertAlmostEqual(Q_s, 463.99, places = 2)

    def test_calculo_de_capacidad_portante_fuste5(self):
        pilotes = copy.copy(self.pilotes_3)
        D_p = 2.6
        
        pilotes.H = 1.5
        Q_s, memoria = pilotes.calculo_de_capacidad_portante_fuste(D_p)
        print(memoria)

        self.assertAlmostEqual(Q_s, 158.54, places = 2)

    def test_calculo_de_capacidad_portante_fuste6(self):
        pilotes = copy.copy(self.pilotes_1)
        D_p = pilotes.D_p
        Q_s, memoria = pilotes.calculo_de_capacidad_portante_fuste(D_p)
        print(memoria)

        self.assertAlmostEqual(Q_s, 200.04, places = 2)

    def test_calculo_de_capacidad_portante_fuste7(self):
        pilotes = copy.copy(self.pilotes_2)
        D_p = pilotes.D_p
        Q_s, memoria = pilotes.calculo_de_capacidad_portante_fuste(D_p)
        print(memoria)

        self.assertAlmostEqual(Q_s, 307.76, places = 2)

    def test_calculo_de_capacidad_portante_fuste8(self):
        pilotes = copy.copy(self.pilotes_4)
        D_p = pilotes.D_p
        Q_s, memoria = pilotes.calculo_de_capacidad_portante_fuste(D_p)
        print(memoria)

        self.assertAlmostEqual(Q_s, 121.92, places = 2)

    def test_calculo_de_capacidad_portante_fuste9(self):
        pilotes = copy.copy(self.pilotes_5)
        D_p = pilotes.D_p
        Q_s, memoria = pilotes.calculo_de_capacidad_portante_fuste(D_p)
        print(memoria)

        self.assertAlmostEqual(Q_s, 212.01, places = 2)

    def test_calculo_de_capacidad_portante_fuste_10(self):
        pilotes = copy.copy(self.pilotes_5)
        D_p = 2.6

        Q_s, memoria = pilotes.calculo_de_capacidad_portante_fuste(D_p)
        print(memoria)

        self.assertAlmostEqual(Q_s, 689.05, places = 2)

    def test_calculo_tension_pilote(self):

        pilotes = copy.copy(self.pilotes_3)
        
        T_u, T_u2, memoria = pilotes.calculo_tension_pilote()
        print(memoria)
        
        self.assertAlmostEqual(T_u, 799.71, places=2)

    def test_calculo_tension_tronco_piramidal_granular(self):

        pilotes = copy.copy(self.pilotes_3)
        D_p = D_c  = pilotes.D_p
        T_tp, _, memoria = pilotes.calculo_tension_tronco_piramidal_granular(D_p, D_c)
        print(memoria)
        
        self.assertAlmostEqual(T_tp, 3365.72, places=2)

    def test_calculo_tension_tronco_piramidal_granular2(self):

        pilotes = copy.copy(self.pilotes_3)
        D_p = 0.6
        D_c = 0.6
        T_tp, _, memoria = pilotes.calculo_tension_tronco_piramidal_granular(D_p, D_c)
        print(memoria)
        
        self.assertAlmostEqual(T_tp, 2083.60, places=2)

    def test_calculo_tension_tronco_piramidal_granular3(self):

        pilotes = copy.copy(self.pilotes_3)
        D_p = 0.7
        D_c = 0.7
        T_tp, _, memoria = pilotes.calculo_tension_tronco_piramidal_granular(D_p, D_c)
        print(memoria)
        
        self.assertAlmostEqual(T_tp, 2224.73, places=2)

    def test_calculo_tension_tronco_piramidal_granular4(self):

        pilotes = copy.copy(self.pilotes_4)
        D_p = 1.8
        D_c = 1.8
        pilotes.H = 2.5
        
        pilotes.set_perfil(Perfil([
            Estrato(H_0 = 1.5, γ_s = 22.0, E_s = 9324, c_u = 0, φ_s = 35, saturado = False, tipo_mat = "g",ν = 0.3, c_p = 0),
            Estrato(H_0 = 1.0, γ_s = 21.0, E_s = 15000, c_u = 0, φ_s = 41, saturado = False, tipo_mat = "g", ν = 0.2, c_p = 0),
            Estrato(H_0 = 1.5, γ_s = 20.5, E_s = 9324, c_u = 0, φ_s = 31, saturado = False, tipo_mat = "g", ν = 0.4, c_p = 0),
            Estrato(H_0 = 1.3, γ_s = 19.2, E_s = 13200, c_u = 0, φ_s = 28, saturado = False, tipo_mat = "g", ν = 0.3, c_p = 0),
            Estrato(H_0 = 3.5, γ_s = 24.0, E_s = 130000, c_u = None, φ_s = None, saturado = False, tipo_mat = "r", c_p = 0, ν = 0.3, roca_φ_rm = 40, RQD = 20),
        ]))
        
        T_tp, _, memoria = pilotes.calculo_tension_tronco_piramidal_granular(D_p, D_c)
        print(memoria)
        
        self.assertAlmostEqual(T_tp, 618.06, places=2)

    def test_calculo_tension_tronco_piramidal_granular5(self):

        pilotes = copy.copy(self.pilotes_3)
        D_p = D_c  = pilotes.D_p
        T_tp, _, memoria = pilotes.calculo_tension_tronco_piramidal_granular(D_p, D_c)
        print(memoria)
        
        self.assertAlmostEqual(T_tp, 3365.72, places=2)

    def test_calculo_tension_tronco_piramidal_granular6(self):

        pilotes = copy.copy(self.pilotes_7)
        D_p = D_c  = pilotes.D_p
        T_tp, _, memoria = pilotes.calculo_tension_tronco_piramidal_granular(D_p, D_c)
        print(memoria)
        
        self.assertAlmostEqual(T_tp, 395.47, places=2)

    def test_calculo_tension_tronco_piramidal_granular7(self):

        pilotes = copy.copy(self.pilotes_7)
        D_c = D_p = pilotes.D_p
        
        T_tp, _, memoria = pilotes.calculo_tension_tronco_piramidal_granular(D_p, D_c)
        print(memoria)
        
        self.assertAlmostEqual(T_tp, 395.47, places=2)

    def test_calculo_tension_tronco_piramidal_granular8(self):

        pilotes = copy.copy(self.pilotes_7)
        D_p = D_c  = pilotes.D_p
        pilotes.H = 2.4
        
        
        T_tp, _, memoria = pilotes.calculo_tension_tronco_piramidal_granular(D_p, D_c)
        print(memoria)
        
        self.assertAlmostEqual(T_tp, 306.78, places=2)

    def test_calculo_tension_tronco_piramidal_granular9(self):

        pilotes = copy.copy(self.pilotes_7)
        D_p = D_c  = pilotes.D_p
        pilotes.H = 2.6

        
        T_tp, _, memoria = pilotes.calculo_tension_tronco_piramidal_granular(D_p, D_c)
        print(memoria)
        
        self.assertAlmostEqual(T_tp, 349.53, places=2)

    def test_calculo_tension_tronco_piramidal_granular_10(self):

        pilotes = copy.copy(self.pilotes_7)
        D_p = D_c  = pilotes.D_p
        pilotes.H = 4.7
        
        
        T_tp, _, memoria = pilotes.calculo_tension_tronco_piramidal_granular(D_p, D_c)
        print(memoria)
        
        self.assertAlmostEqual(T_tp, 994.94, places=2)

    def test_calculo_tension_tronco_piramidal_cohesivo(self):

        pilotes = copy.copy(self.pilotes_2)
        D_p = D_c = pilotes.D_p
        T_tp, _, memoria = pilotes.calculo_tension_tronco_piramidal_cohesivo(D_p, D_c)
        print(memoria)
        
        self.assertAlmostEqual(T_tp, 334.00, places=2)

    def test_calculo_tension_tronco_piramidal_cohesivo2(self):

        pilotes = copy.copy(self.pilotes_2)
        D_p = 1.7
        D_c = 1.7
        
        T_tp, _, memoria = pilotes.calculo_tension_tronco_piramidal_cohesivo(D_p, D_c)
        print(memoria)
        
        self.assertAlmostEqual(T_tp, 634.37, places=2)

    def test_calculo_tension_tronco_piramidal_cohesivo3(self):

        pilotes = copy.copy(self.pilotes_2)
        D_p = 1.6
        D_c = 1.6
        
        T_tp, _, memoria = pilotes.calculo_tension_tronco_piramidal_cohesivo(D_p, D_c)
        print(memoria)
        
        self.assertAlmostEqual(T_tp, 567.63, places=2)

    def test_calculo_tension_tronco_piramidal_cohesivo4(self):

        pilotes = copy.copy(self.pilotes_3)
        D_p = D_c = pilotes.D_p
        T_tp, _, memoria = pilotes.calculo_tension_tronco_piramidal_cohesivo(D_p, D_c)
        print(memoria)
        
        self.assertAlmostEqual(T_tp, 799.71, places=2)

    def test_calculo_tension_tronco_piramidal_cohesivo5(self):

        pilotes = copy.copy(self.pilotes_3)
        D_p = 2
        D_c = 2
        
        T_tp, _, memoria = pilotes.calculo_tension_tronco_piramidal_cohesivo(D_p, D_c)
        print(memoria)
        
        self.assertAlmostEqual(T_tp, 1617.53, places=2)

    def test_calculo_tension_tronco_piramidal_cohesivo6(self):

        pilotes = copy.copy(self.pilotes_3)
        D_p = D_c = pilotes.D_p
        pilotes.H = 2.5
                
        T_tp, _, memoria = pilotes.calculo_tension_tronco_piramidal_cohesivo(D_p, D_c)
        print(memoria)
        
        self.assertAlmostEqual(T_tp, 266.82, places=2)

    def test_calculo_tension_tronco_piramidal_cohesivo7(self):

        pilotes = copy.copy(self.pilotes_5)
        D_p = D_c = pilotes.D_p
        T_tp, _, memoria = pilotes.calculo_tension_tronco_piramidal_cohesivo(D_p, D_c)
        print(memoria)
        
        self.assertAlmostEqual(T_tp, 181.02, places=2)

    def test_calculo_tension_tronco_piramidal_cohesivo8(self):

        pilotes = copy.copy(self.pilotes_5)
        D_p = 1.4
        D_c = 1.4
        
        T_tp, _, memoria = pilotes.calculo_tension_tronco_piramidal_cohesivo(D_p, D_c)
        print(memoria)
        
        self.assertAlmostEqual(T_tp, 473.85, places=2)

    def test_calculo_tension_tronco_piramidal_cohesivo9(self):

        pilotes = copy.copy(self.pilotes_5)
        D_p = 1.3
        D_c = 1.3
        pilotes.H = 1.2
        
        T_tp, _, memoria = pilotes.calculo_tension_tronco_piramidal_cohesivo(D_p, D_c)
        print(memoria)
        
        self.assertAlmostEqual(T_tp, 160.23, places=2)

    def test_calculo_tension_tronco_piramidal_cohesivo_10(self):

        pilotes = copy.copy(self.pilotes_5)
        D_p = D_c = pilotes.D_p
        pilotes.H = 2.5
        
        T_tp, _, memoria = pilotes.calculo_tension_tronco_piramidal_cohesivo(D_p, D_c)
        print(memoria)
        
        self.assertAlmostEqual(T_tp, 149.35, places=2)

    def test_calculo_tension_tronco_piramidal_cohesivo_11(self):

        pilotes = copy.copy(self.pilotes_5)
        D_p = 1.8
        D_c = 1.8
        pilotes.H = 2
        
        
        T_tp, _,memoria = pilotes.calculo_tension_tronco_piramidal_cohesivo(D_p, D_c)
        print(memoria)
        
        self.assertAlmostEqual(T_tp, 425.85, places=2)

    def test_calculo_tension_tronco_piramidal_cohesivo_12(self):

        pilotes = copy.copy(self.pilotes_6)
        D_p = D_c = pilotes.D_p
        T_tp, _, memoria = pilotes.calculo_tension_tronco_piramidal_cohesivo(D_p, D_c)
        print(memoria)
        
        self.assertAlmostEqual(T_tp, 180.43, places=2)

    def test_calculo_tension_tronco_piramidal_cohesivo_13(self):

        pilotes = copy.copy(self.pilotes_6)
        D_p = 1.9
        D_c = 1.9
        pilotes.H = 1.8
        
        
        T_tp,_, memoria = pilotes.calculo_tension_tronco_piramidal_cohesivo(D_p, D_c)
        print(memoria)
        
        self.assertAlmostEqual(T_tp, 421.65, places=2)

    def test_calculo_tension_tronco_piramidal_cohesivo_14(self):

        pilotes = copy.copy(self.pilotes_6)
        D_p = 0.9
        D_c = 0.9
        pilotes.H = 2
        
        T_tp, _, memoria = pilotes.calculo_tension_tronco_piramidal_cohesivo(D_p, D_c)
        print(memoria)
        
        self.assertAlmostEqual(T_tp, 149.88, places=2)

    def test_calculo_tension_tronco_piramidal_cohesivo_15(self):

        pilotes = copy.copy(self.pilotes_7)
        D_p = D_c = pilotes.D_p
        T_tp,_, memoria = pilotes.calculo_tension_tronco_piramidal_cohesivo(D_p, D_c)
        print(memoria)
        
        self.assertAlmostEqual(T_tp, 201.51, places=2)

    def test_calculo_carga_lateral_pilote(self):
        # cargas = {}
        # cargas['F_xc'], cargas['F_yc'], cargas['F_zc'] = 1000, 200, 100  
        # cargas['F_xt'], cargas['F_yt'], cargas['F_zt'] = 900, 120, 150 
        # cargas['F_xl'], cargas['F_yl'], cargas['F_zl'] = 800, 500, 450 
        # cargas['F_xtr'], cargas['F_ytr'], cargas['F_ztr'] = 700, 200, 300

        e = 1

        pilotes = self.pilotes_3
        P, p_corta, memoria = pilotes.calculo_carga_lateral_pilote(e)
        print(memoria)
        print(p_corta)
        self.assertAlmostEqual(P, 128.93, places=2)

    def test_calculo_carga_lateral(self):
        e = 0

        pilotes = self.pilotes_3
        P, _,memoria = pilotes.calculo_carga_lateral(e)
        print(memoria)
       
        self.assertAlmostEqual(P, 337.70, places=2)

    def test_calculo_carga_lateral2(self):
        e = 0

        pilotes = self.pilotes_2
        P, _,memoria = pilotes.calculo_carga_lateral(e)
        print(memoria)
       
        self.assertAlmostEqual(P, 257.42, places=2)

    def test_calculo_carga_lateral3(self):
        e = 1

        pilotes = self.pilotes_3
        P, _,memoria = pilotes.calculo_carga_lateral(e)
        print(memoria)
        
        self.assertAlmostEqual(P, 335.22, places=2)

    def test_calculo_carga_lateral4(self):
        # cargas = {}
        # cargas['F_xc'], cargas['F_yc'], cargas['F_zc'] = 1000, 200, 100  
        # cargas['F_xt'], cargas['F_yt'], cargas['F_zt'] = 900, 120, 150 
        # cargas['F_xl'], cargas['F_yl'], cargas['F_zl'] = 800, 500, 450 
        # cargas['F_xtr'], cargas['F_ytr'], cargas['F_ztr'] = 700, 200, 300
        e = 0

        pilotes = self.pilotes_5
        P, _, memoria = pilotes.calculo_carga_lateral(e)
        print(memoria)
        self.assertAlmostEqual(P, 189.41, places=2)

    def test_calculo_carga_lateral5(self):
        # cargas = {}
        # cargas['F_xc'], cargas['F_yc'], cargas['F_zc'] = 1000, 200, 100  
        # cargas['F_xt'], cargas['F_yt'], cargas['F_zt'] = 900, 120, 150 
        # cargas['F_xl'], cargas['F_yl'], cargas['F_zl'] = 800, 500, 450 
        # cargas['F_xtr'], cargas['F_ytr'], cargas['F_ztr'] = 700, 200, 300
        e = 0

        pilotes = self.pilotes_6
        P, _, memoria = pilotes.calculo_carga_lateral(e)
        print(memoria)
        self.assertAlmostEqual(P, 21.55, places=2)

    def test_calculo_modulos_de_reaccion_horizontal(self):
        
        pilotes = copy.copy(self.pilotes_1)

        k = pilotes.calculo_modulos_de_reaccion_horizontal()
        
        self.assertTrue(k)

    def test_calculo_modulos_de_reaccion_horizontal2(self):
        
        pilotes = copy.copy(self.pilotes_2)

        k = pilotes.calculo_modulos_de_reaccion_horizontal()
        
        self.assertTrue(k)

    def test_calculo_asentamiento(self):
        pilotes = copy.copy(self.pilotes_1)
        
        k = 20
        F_zc = 800
        F_zc_eds = 150
        t = 50

        S_e, S_c , memoria_e, memoria_c = pilotes.calculo_asentamiento(k, F_zc, F_zc_eds, t)
        print(memoria_e)
        print(memoria_c)
        self.assertAlmostEqual(S_e, 0.08, places=2)
        self.assertAlmostEqual(S_c, 0.0, places=1)

    def test_calculo_asentamiento2(self):
        pilotes = copy.copy(self.pilotes_2)
        
        k = 20
        F_zc = 700
        F_zc_eds = 110
        t = 50

        S_e, S_c , memoria_e, memoria_c = pilotes.calculo_asentamiento(k, F_zc, F_zc_eds, t)
        # print(memoria_e)
        # print(memoria_c)
        self.assertAlmostEqual(S_e, 0.009, places=3)
        self.assertAlmostEqual(S_c, 0.0, places=1)

    def test_calculo_asentamiento3(self):
        pilotes = copy.copy(self.pilotes_3)
        
        k = 20
        F_zc = 900
        F_zc_eds = 250
        t = 50

        S_e, S_c , memoria_e, memoria_c = pilotes.calculo_asentamiento(k, F_zc, F_zc_eds, t)
        print(memoria_e)
        print(memoria_c)
        self.assertAlmostEqual(S_e, 0.006, places=2)
        self.assertAlmostEqual(S_c, 0.0, places=1)

    def test_calculo_asentamiento4(self):
        pilotes = copy.copy(self.pilotes_4)
        
        k = 20
        F_zc = 950
        F_zc_eds = 80
        t = 50

        S_e, S_c , memoria_e, memoria_c = pilotes.calculo_asentamiento(k, F_zc, F_zc_eds, t)
        # print(memoria_e)
        # print(memoria_c)
        self.assertAlmostEqual(S_e, 0.040, places=2)
        self.assertAlmostEqual(S_c, 0.0, places=1)

    def test_calculo_asentamiento5(self):
        pilotes = copy.copy(self.pilotes_5)
        
        k = 20
        F_zc = 650
        F_zc_eds = 200
        t = 50

        S_e, S_c , memoria_e, memoria_c = pilotes.calculo_asentamiento(k, F_zc, F_zc_eds, t)
        # print(memoria_e)
        # print(memoria_c)
        self.assertAlmostEqual(S_e, 0.061, places=2)
        self.assertAlmostEqual(S_c, 0.0, places=1)

    def test_calculo_asentamiento6(self):
        pilotes = copy.copy(self.pilotes_6)
        
        
        k = 20
        F_zc = 855
        F_zc_eds = 168
        t = 50

        S_e, S_c , memoria_e, memoria_c = pilotes.calculo_asentamiento(k, F_zc, F_zc_eds, t)
        # print(memoria_e)
        # print(memoria_c)
        self.assertAlmostEqual(S_e, 0.021, places=3)
        self.assertAlmostEqual(S_c, 0.0, places=1)

    def test_calculo_asentamiento7(self):
        pilotes = copy.copy(self.pilotes_7)
        
        k = 20
        F_zc = 920
        F_zc_eds = 115
        t = 50

        S_e, S_c , memoria_e, memoria_c = pilotes.calculo_asentamiento(k, F_zc, F_zc_eds, t)
        # print(memoria_e)
        # print(memoria_c)
        self.assertAlmostEqual(S_e, 0.036, places=3)
        self.assertAlmostEqual(S_c, 0.0, places=1)

        
if __name__ == "__main__":
    unittest.main()