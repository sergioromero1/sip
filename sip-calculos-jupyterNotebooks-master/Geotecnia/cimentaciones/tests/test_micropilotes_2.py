import unittest
from ..micropilotes import Micropilotes
from ..perfil import Perfil, Estrato
from ..barra import Barra

class TestMicropilotes2(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        # Perfil 1
        self.perfil_1 = Perfil([
            Estrato(H_0 = 1.3, γ_s = 18.0, N=8,  E_s = 2500, c_u =  33.36, φ_s = 24, saturado = False, tipo_mat = "c",  ν = 0.25 , c_p = 0,σ_pp=23.4,C_c=0.12,C_s=0.07,e_0=0.38),
            Estrato(H_0 = 3.2, γ_s = 15.0, N=6,  E_s = 2000, c_u =  28.36, φ_s = 24, saturado = False, tipo_mat = "c",  ν = 0.35, c_p = 0,σ_pp=83.8,C_c=0.18,C_s=0.09,e_0=0.25),
            Estrato(H_0 = 2.1, γ_s = 19.0, N=17, E_s = 4800, c_u =  80.36, φ_s = 24, saturado = False, tipo_mat = "c",  ν = 0.30, c_p = 0,σ_pp=125.4,C_c=0.09,C_s=0.02,e_0=0.22),
            Estrato(H_0 = 4.0, γ_s = 20.0, N=20, E_s = 6800, c_u = 120.36, φ_s = 24, saturado = False, tipo_mat = "c",  ν = 0.25, c_p = 0,σ_pp=300,C_c=0.05,C_s=0.009,e_0=0.18),
        ])
        # Perfil 1NF
        self.perfil_1NF=Perfil([
            Estrato(H_0 = 1.3, γ_s = 18.0, N=8,  E_s = 2500, c_u =  33.36, φ_s = 24, saturado = False, tipo_mat = "c",  ν = 0.32, c_p = 0,σ_pp=23.4,C_c=0.12,C_s=0.07,e_0=0.38),
            Estrato(H_0 = 3.2, γ_s = 15.0, N=6,  E_s = 2000, c_u =  28.36, φ_s = 24, saturado = False, tipo_mat = "c",  ν = 0.31, c_p = 0,σ_pp=83.8,C_c=0.18,C_s=0.09,e_0=0.25),
            Estrato(H_0 = 2.1, γ_s = 19.0, N=17, E_s = 4800, c_u =  80.36, φ_s = 24, saturado = True, tipo_mat = "c",  ν = 0.25, c_p = 0,σ_pp=125.4,C_c=0.09,C_s=0.02,e_0=0.22),
            Estrato(H_0 = 4.0, γ_s = 20.0, N=20, E_s = 6800, c_u = 120.36, φ_s = 24, saturado = True, tipo_mat = "c",  ν = 0.35, c_p = 0,σ_pp=300,C_c=0.05,C_s=0.009,e_0=0.18),
        ])
        # Perfil 1_Sat
        self.perfil_1Sat = Perfil([
            Estrato(H_0 = 1.3, γ_s = 18.0, N=8,  E_s = 2500, c_u =  33.36, φ_s = 24, saturado = True, tipo_mat = "c", ν = 0.32, c_p = 0,σ_pp=23.4,C_c=0.12,C_s=0.07,e_0=0.38),
            Estrato(H_0 = 3.2, γ_s = 15.0, N=6,  E_s = 2000, c_u =  28.36, φ_s = 24, saturado = True, tipo_mat = "c",  ν = 0.26, c_p = 0,σ_pp=83.8,C_c=0.18,C_s=0.09,e_0=0.25),
            Estrato(H_0 = 2.1, γ_s = 19.0, N=17, E_s = 4800, c_u =  80.36, φ_s = 24, saturado = True, tipo_mat = "c",  ν = 0.30, c_p = 0,σ_pp=125.4,C_c=0.09,C_s=0.02,e_0=0.22),
            Estrato(H_0 = 4.0, γ_s = 20.0, N=20, E_s = 6800, c_u = 120.36, φ_s = 24, saturado = True, tipo_mat = "c",  ν = 0.27, c_p = 0,σ_pp=300,C_c=0.05,C_s=0.009,e_0=0.18),
        ])
        #Perfil 2
        self.perfil_2 = Perfil([
            Estrato(H_0 = 0.5, γ_s = 20.0, E_s =  9500, c_u =  38.00, φ_s = 20, saturado = False, tipo_mat = "c", ν = 0.30 ,c_p = 0, N=28,σ_pp=20,C_c=0.1,C_s=0.01,e_0=1.4),
            Estrato(H_0 = 0.7, γ_s = 16.0, E_s = 16000, c_u =  89.00, φ_s = 20, saturado = True,  tipo_mat = "c",  ν = 0.28 ,c_p = 0, N=23,σ_pp=23,C_c=0.04,C_s=0.004,e_0=2.10),
            Estrato(H_0 = 2.2, γ_s = 17.2, E_s = 13500, c_u =  None,  φ_s = 22.0, saturado = True,  tipo_mat = "g",  ν = 0.32 ,c_p = 0, N=18),
            Estrato(H_0 = 1.3, γ_s = 14.0, E_s = 19000, c_u =  None,  φ_s = 32.0, saturado = True,  tipo_mat = "g",  ν = 0.30 ,c_p = 0, N=28),
            Estrato(H_0 = 4.0, γ_s = 16.0, E_s = 23000, c_u =  150.0, φ_s = 20, saturado = True,  tipo_mat = "c",  ν = 0.35 ,c_p = 0, N=24,σ_pp=139,C_c=0.11,C_s=0.05,e_0=1.65),
            Estrato(H_0 = 2.8, γ_s = 20.0, E_s = 40000, c_u =  None,  φ_s = 20, saturado = True,  tipo_mat = "r",  ν = 0.25 ,c_p = 0, N=None , ucs=4500, roca_φ_rm = 38),
        ]) 
        
        #Perfil 3
        self.perfil_3 = Perfil([
            Estrato(H_0 = 2.2, γ_s = 16.9, E_s =  1500, c_u =  None, φ_s = 28.0, saturado = False, tipo_mat = "g",  ν = 0.30, c_p = 0, N=19),
            Estrato(H_0 = 1.3, γ_s = 17.3, E_s =  3650, c_u =  None, φ_s = 29.0, saturado = False, tipo_mat = "g",  ν = 0.31, c_p = 0, N=25),
            Estrato(H_0 = 0.7, γ_s = 16.8, E_s =  8000, c_u =  93,   φ_s = 20, saturado = False, tipo_mat = "c",  ν = 0.25, c_p = 0, N=22,σ_pp=70.6,C_c=0.2,C_s=0.08,e_0=0.9),
            Estrato(H_0 = 0.8, γ_s = 17.9, E_s = 15000, c_u =  None, φ_s = 35.0, saturado = False, tipo_mat = "g",  ν = 0.32, c_p = 0, N=60),
            Estrato(H_0 = 3.5, γ_s = 22.0, roca_E_rm = 50000, c_u =  None, φ_s = 20, saturado = True,  tipo_mat = "r",  ν = 0.28, c_p = 0, N=None , ucs=7800),
         ]) 
        # Perfil 4
        self.perfil_4 = Perfil([
            Estrato(H_0 = 2.3, γ_s = 20.0, N=30,  E_s =  4500, c_u =  None, φ_s = 28.0, saturado = False, tipo_mat = "g", ν = 0.30, c_p = 0),
            Estrato(H_0 = 1.6, γ_s = 18.5, N=28,  E_s =  2900, c_u =  None, φ_s = 24.3, saturado = False, tipo_mat = "g", ν = 0.35, c_p = 0),
            Estrato(H_0 = 3.1, γ_s = 19.3, N=29,  E_s = 18000, c_u =  None, φ_s = 33.0, saturado = False, tipo_mat = "g", ν = 0.22, c_p = 0),
            Estrato(H_0 = 2.6, γ_s = 17.6, N=25,  E_s = 16750, c_u =  None, φ_s = 26.0, saturado = False, tipo_mat = "g", ν = 0.28, c_p = 0),
        ])
        # Perfil 4 saturado
        self.perfil_4s = Perfil([
            Estrato(H_0 = 2.3, γ_s = 20.0, N=30,  E_s =  4500, c_u =  None, φ_s = 28.0, saturado = True, tipo_mat = "g", ν = 0.28, c_p = 0),
            Estrato(H_0 = 1.6, γ_s = 18.5, N=28,  E_s =  2900, c_u =  None, φ_s = 24.3, saturado = True, tipo_mat = "g", ν = 0.32, c_p = 0),
            Estrato(H_0 = 3.1, γ_s = 19.3, N=29,  E_s = 18000, c_u =  None, φ_s = 33.0, saturado = True, tipo_mat = "g", ν = 0.30, c_p = 0),
            Estrato(H_0 = 2.6, γ_s = 17.6, N=25,  E_s = 16750, c_u =  None, φ_s = 26.0, saturado = True, tipo_mat = "g", ν = 0.25, c_p = 0),
        ])        
        # Perfil 5
        self.perfil_5 = Perfil([
            Estrato(H_0 = 0.8, γ_s = 16.5, N=18,    E_s =  7600, c_u =  60,   φ_s = 20, saturado = False, tipo_mat = "c",  ν = 0.28, c_p = 0,σ_pp=16,C_c=0.12,C_s=0.003,e_0=1.2),
            Estrato(H_0 = 0.9, γ_s = 21.0, N=None ,  E_s = 50000, c_u =  None, φ_s = 20, saturado = False, tipo_mat = "r",  ν = 0.4, c_p = 0, ucs=6000),
            Estrato(H_0 = 1.5, γ_s = 20.0, N=None,  E_s = 36800, c_u =  None, φ_s = 20, saturado = False, tipo_mat = "r",  ν = 0.4, c_p = 0,ucs=3250),
            Estrato(H_0 = 3.5, γ_s = 21.0, N=None,  E_s = 75800, c_u =  None, φ_s = 20, saturado = False, tipo_mat = "r",  ν = 0.4, c_p = 0, ucs=9500),
            Estrato(H_0 = 1.2, γ_s = 22.0, N=None,  E_s = 90000, c_u =  None, φ_s = 20, saturado = False, tipo_mat = "r",  ν = 0.35, c_p = 0,ucs=14000),
        ]) 
        # Perfil 6
        self.perfil_6 = Perfil([
            Estrato(H_0 = 0.6, γ_s = 19.5, N=24  ,  E_s =  6000, c_u =   93.5, φ_s = 20, saturado = False, tipo_mat = "c", ν = 0.3, c_p = 0,σ_pp=12,C_c=0.1,C_s=0.008,e_0=0.1),
            Estrato(H_0 = 0.5, γ_s = 16.6, N=9   ,  E_s = 12500, c_u =   None, φ_s = 15,   saturado = False, tipo_mat = "g", ν = 0.25, c_p = 0),
            Estrato(H_0 = 0.8, γ_s = 18.3, N=21  ,  E_s =  9500, c_u =  110.0, φ_s = 20, saturado = False, tipo_mat = "c", ν = 0.35, c_p = 0,σ_pp=34.64,C_c=0.2,C_s=0.09,e_0=2.1),
            Estrato(H_0 = 1.3, γ_s = 17.5, N=18  ,  E_s = 19875, c_u =   None, φ_s = 24,   saturado = True,  tipo_mat = "g", ν = 0.32, c_p = 0),
            Estrato(H_0 = 1.5, γ_s = 14.9, N=23  ,  E_s =  8000, c_u =   28.0, φ_s = 20, saturado = True,  tipo_mat = "c", ν = 0.26, c_p = 0,σ_pp=70,C_c=0.01,C_s=0.001,e_0=0.85),
            Estrato(H_0 = 2.3, γ_s = 19.6, N=46  ,  E_s = 25000, c_u =   None, φ_s = 37,   saturado = True,  tipo_mat = "g", ν = 0.28, c_p = 0),
            Estrato(H_0 = 2.5, γ_s = 20.2, N=30,    E_s =  9500, c_u =  160.0, φ_s = 20, saturado = True,  tipo_mat = "c", ν = 0.35, c_p = 0,σ_pp=142,C_c=0.05,C_s=0.001,e_0=1.3),
            Estrato(H_0 = 3.2, γ_s = 21.3, N=None,  E_s = 75000, c_u =   None, φ_s = 20, saturado = True,  tipo_mat = "r", ν = 0.4, c_p = 0, ucs=12500),
        ]) 

    def test_calculo_carga_compresion1(self):
        micropilotes = Micropilotes(D_f=1.5, HG = 1, D_d=0,  H = 0.5, S_m = 0.4, 
                                    TP= 0.4,θ= 0,γ_c=24,N_m= 4,  P_anc=1,L_b= 4.5, 
                                    barra=Barra(nombre = 'uno',D=0.0378,area=0.00075,f_y=530000, precio =20000),
                                    D_p= 0.115,η= 1,proc_iny= "IGU",f_pc= 21000,f_py= 450000,
                                    A_camisa= 0, db = 0.0254, perfil=self.perfil_1, 
                                    α=0, ω=0, f_carga_mp=0.6)
        P_G, memoria = micropilotes.calculo_carga_compresion()
        print(memoria)
        P_G = memoria["P_G"]
        self.assertAlmostEqual(P_G, 106.37, places=2)
      
    def test_calculo_carga_compresion2(self):
        micropilotes= Micropilotes(D_f=1.2, HG = 1, D_d=0, P_anc=1, L_b= 15, H = 0.5,
                                    TP = 0.4, θ= 0, γ_c=24,S_m = 0.4, N_m= 4,
                                    barra=Barra(nombre = 'uno',D=0.0378,area=0.00075,f_y=530000, precio =20000),
                                    D_p= 0.115,η= 1,proc_iny= "IGU",f_pc= 21000,f_py= 450000,
                                    A_camisa= 0, db = 0.0254, perfil=self.perfil_6, 
                                    α=0, ω=0, f_carga_mp=0.6)
        P_G, memoria = micropilotes.calculo_carga_compresion()
        print(memoria)
        P_G = memoria["P_G"]
        self.assertAlmostEqual(P_G, 30041.64, places=2)

    def test_calculo_carga_compresion3(self):
        perfil_1 = Perfil([
            Estrato(H_0 = 1.3, γ_s = 18.0, N=8,  E_s = 2500, c_u =  33.36, φ_s = 24, saturado = False, tipo_mat = "c", c_p = 0, C_c = 0, C_s = 0.5,e_0 = 1.2, σ_pp = 30),
            Estrato(H_0 = 3.2, γ_s = 15.0, N=6,  E_s = 2000, c_u =  28.36, φ_s = 24, saturado = False, tipo_mat = "c", c_p = 0, C_c = 0, C_s = 0.5,e_0 = 1.2, σ_pp = 30),
            Estrato(H_0 = 2.1, γ_s = 19.0, N=17, E_s = 4800, c_u =  80.36, φ_s = 24, saturado = False, tipo_mat = "c", c_p = 0, C_c = 0, C_s = 0.5,e_0 = 1.2, σ_pp = 30),
            Estrato(H_0 = 9.9, γ_s = 20.0, N=20, E_s = 6800, c_u = 120.36, φ_s = 24, saturado = False, tipo_mat = "c", c_p = 0, C_c = 0, C_s = 0.5,e_0 = 1.2, σ_pp = 30),
        ])
        micropilotes = Micropilotes(D_f=1.5, HG = 1,D_d=0,  H = 0.5, S_m = 0.4, 
                                    TP= 0.4,θ= 0,γ_c=24,N_m= 8, P_anc=1, L_b= 15, 
                                    barra=Barra(nombre = 'uno',D=0.0378,area=0.00075,f_y=530000, precio =20000),
                                    D_p= 0.115,η= 1,proc_iny= "IGU",f_pc= 21000,f_py= 450000,
                                    A_camisa= 0, db = 0.0254, perfil=perfil_1, 
                                    α=0, ω=0, f_carga_mp=0.6)
        P_G, memoria = micropilotes.calculo_carga_compresion()
        print (memoria)
        P_G = memoria["P_G"]
        self.assertAlmostEqual(P_G, 604.17, places=2)

    def test_calculo_carga_compresion4(self):#S
        micropilotes = Micropilotes(D_f=1.5, HG = 0.5, D_d=0, H = 0.5, S_m = 0.4, 
                                    TP= 0.84, θ= 0, γ_c=24, N_m= 5, P_anc=1, L_b= 10.5, 
                                    barra=Barra(nombre = 'uno',D=0.0378,area=0.00075,f_y=530000, precio =20000),
                                    D_p= 0.15, η= 1, proc_iny= "IGU",f_pc= 21000,f_py= 420000,
                                    A_camisa= 0, db = 0.0254, perfil=self.perfil_1Sat, 
                                    α=0, ω=0, f_carga_mp=0.6)
        P_G, memoria = micropilotes.calculo_carga_compresion()
        print(memoria)
        P_G = memoria["P_G"]
        self.assertAlmostEqual(P_G, 214.54, places=2)

    def test_calculo_carga_compresion5(self):#S
        micropilotes = Micropilotes(D_f=1.5, HG = 0.5,  D_d=0, H = 0.5, S_m = 0.4, 
                                    TP= 0.95, θ= 0, γ_c=24, N_m= 5, P_anc=1, L_b= 10.5, 
                                    barra=Barra(nombre = 'uno',D=0.0378,area=0.00075,f_y=530000, precio =20000),
                                    D_p= 0.15, η= 1, proc_iny= "IGU",f_pc= 21000,f_py= 420000,
                                    A_camisa= 0, db = 0.0254, perfil=self.perfil_4, 
                                    α=0, ω=0, f_carga_mp=0.6)
        P_G, memoria = micropilotes.calculo_carga_compresion()
        print(memoria)
        P_G = memoria["P_G"]
        self.assertAlmostEqual(P_G, 606.14, places=2)

    def test_calculo_carga_compresion6(self):#S
        micropilotes = Micropilotes(D_f=1.5, HG = 0.5, D_d=0, H = 0.5, S_m = 0.4,
                                    TP= 0.95, θ= 0, γ_c=24, N_m= 5, P_anc=1, L_b= 10.5, 
                                    barra=Barra(nombre = 'uno',D=0.0378,area=0.00075,f_y=530000, precio =20000),
                                    D_p= 0.15, η= 1, proc_iny= "IGU",f_pc= 21000,f_py= 420000,
                                    A_camisa= 0, db = 0.0254, perfil=self.perfil_4s, 
                                    α=0, ω=0, f_carga_mp=0.6)
        P_G, memoria = micropilotes.calculo_carga_compresion()
        print(memoria)
        P_G = memoria["P_G"]
        self.assertAlmostEqual(P_G, 303.071, places=2)

    def test_calculo_carga_compresion7(self):#S
        micropilotes = Micropilotes(D_f=1.5, HG = 0.5, D_d=0, H = 0.5, S_m = 0.4,
                                    TP= 0.95, θ= 0, γ_c=24, N_m= 5, P_anc=1, L_b= 10.5, 
                                    barra=Barra(nombre = 'uno',D=0.0378,area=0.00075,f_y=530000, precio =20000),
                                    D_p= 0.15, η= 1, proc_iny= "IGU",f_pc= 21000,f_py= 420000,
                                    A_camisa= 0, db = 0.0254, perfil=self.perfil_1NF, 
                                    α=0, ω=0, f_carga_mp=0.6)
        P_G, memoria = micropilotes.calculo_carga_compresion()
        print(memoria)
        P_G = memoria["P_G"]
        self.assertAlmostEqual(P_G, 247.01, places=2)

    def test_calculo_carga_compresion8(self):#S
        micropilotes = Micropilotes(D_f=1.5, HG = 1,D_d=0, H = 0.5, S_m = 0.4,
                                TP= 0.95, θ= 0, γ_c=24, N_m= 5, P_anc=1, L_b= 8, 
                                barra=Barra(nombre = 'uno',D=0.0378,area=0.00075,f_y=530000, precio =20000),
                                D_p= 0.15, η= 1, proc_iny= "IGU",f_pc= 21000,f_py= 420000,
                                A_camisa= 0, db = 0.0254, perfil=self.perfil_6, 
                                α=0, ω=0, f_carga_mp=0.6)
        P_G, memoria = micropilotes.calculo_carga_compresion()
        print(memoria)
        P_G = memoria["P_G"]
        self.assertAlmostEqual(P_G, 387.40, places=2)

    def test_calculo_carga_compresion9(self):#S
        micropilotes = Micropilotes(D_f=1.5, HG = 1, D_d=0,   H = 0.5, S_m = 0.4, 
                                    TP= 0.7, θ= 0, γ_c=24, N_m= 5, P_anc=1, L_b= 8, 
                                    barra=Barra(nombre = 'uno',D=0.0378,area=0.00075,f_y=530000, precio =20000),
                                    D_p= 0.2, η= 1, proc_iny= "IGU",f_pc= 21000,f_py= 420000,
                                    A_camisa= 0, db = 0.0254, perfil=self.perfil_6, 
                                    α=0, ω=0, f_carga_mp=0.6)
        P_G, memoria = micropilotes.calculo_carga_compresion()
        print(memoria)
        P_G = memoria["P_G"]
        self.assertAlmostEqual(P_G, 516.54, places=2)

    def test_calculo_carga_compresion_10(self):#S
        micropilotes = Micropilotes(D_f=1.5, HG = 1.2,  D_d=0,  H = 0.5, S_m = 0.4, 
                                    TP= 0.6, θ= 0, γ_c=24, N_m= 5, P_anc=1, L_b= 8, 
                                    barra=Barra(nombre = 'uno',D=0.0378,area=0.00075,f_y=530000, precio =20000),
                                    D_p= 0.2, η= 1, proc_iny= "IGU",f_pc= 21000,f_py= 420000,
                                    A_camisa= 0, db = 0.0254, perfil=self.perfil_6, 
                                    α=0, ω=0, f_carga_mp=0.6)
        P_G, memoria = micropilotes.calculo_carga_compresion()
        print(memoria)
        P_G = memoria["P_G"]
        self.assertAlmostEqual(P_G, 516.54, places=2)

    def test_calculo_capacidad_portante1(self):#S
        micropilotes = Micropilotes(D_f=1.5,HG = 1,  D_d=0,  H = 0.5, S_m = 0.4,
                                    TP= 0.4, θ= 0, γ_c=24,N_m= 4,
                                    P_anc=1, L_b= 4.5, 
                                    barra=Barra(nombre = 'uno',D=0.0378,area=0.00075,f_y=530000, precio =20000),
                                    D_p= 0.115,η= 1,proc_iny= "IGU",f_pc= 21000,
                                    f_py= 450000,A_camisa= 0, db = 0.0254, 
                                    perfil=self.perfil_1, 
                                    α=0, ω=0, f_carga_mp=0.6)
        
        q_ult, memoria = micropilotes.calculo_capacidad_portante()
        print(memoria)
        self.assertAlmostEqual(q_ult, 273.420, places=2)

    def test_calculo_capacidad_portante2(self):#S
        micropilotes = Micropilotes(D_f=1.5,HG = 1, D_d=0, H = 0.5, S_m = 0.4,
                                    TP= 0.4, θ= 0, γ_c=24,N_m= 4,
                                    P_anc=1, L_b= 4.5, 
                                    barra=Barra(nombre = 'uno',D=0.0378,area=0.00075,f_y=530000, precio =20000),
                                    D_p= 0.115,η= 1,proc_iny= "IGU",f_pc= 21000,
                                    f_py= 450000,A_camisa= 0, db = 0.0254, 
                                    perfil=self.perfil_2, 
                                    α=0, ω=0, f_carga_mp=0.6)
        
        q_ult, memoria = micropilotes.calculo_capacidad_portante()
        print(memoria)
        self.assertAlmostEqual(q_ult, 262.15, places=2)

    def test_calculo_capacidad_portante3(self):#S
        micropilotes = Micropilotes(D_f=1.5,HG = 1, D_d=0,  H = 0.5, S_m = 0.4, 
                                    TP= 0.4, θ= 0, γ_c=24,N_m= 4,
                                    P_anc=1, L_b= 4.5, 
                                    barra=Barra(nombre = 'uno',D=0.0378,area=0.00075,f_y=530000, precio =20000),
                                    D_p= 0.115,η= 1,proc_iny= "IGU",f_pc= 21000,
                                    f_py= 450000,A_camisa= 0, db = 0.0254, 
                                    perfil=self.perfil_3, 
                                    α=0, ω=0, f_carga_mp=0.6)
        
        q_ult, memoria = micropilotes.calculo_capacidad_portante()
        print(memoria)
        self.assertAlmostEqual(q_ult, 880.06, places=2)

    def test_calculo_capacidad_portante4(self):#S
        micropilotes = Micropilotes(D_f=1.5,HG = 1, D_d=0, H = 0.5, S_m = 0.4,
                                    TP= 0.4, θ= 0, γ_c=24,N_m= 4,
                                    P_anc=1, L_b= 4.5, 
                                    barra=Barra(nombre = 'uno',D=0.0378,area=0.00075,f_y=530000, precio =20000),
                                    D_p= 0.115,η= 1,proc_iny= "IGU",f_pc= 21000,
                                    f_py= 450000,A_camisa= 0, db = 0.0254, 
                                    perfil=self.perfil_4, 
                                    α=0, ω=0, f_carga_mp=0.6)
        
        q_ult, memoria = micropilotes.calculo_capacidad_portante()
        print(memoria)
        self.assertAlmostEqual(q_ult, 790.44, places=2)

    def test_calculo_capacidad_portante5(self):#S
        micropilotes = Micropilotes(D_f=1.5,HG = 1, D_d=0, H = 0.5, S_m = 0.4, 
                                    TP= 0.4, θ= 0, γ_c=24,N_m= 4,
                                    P_anc=1, L_b= 4.5, 
                                    barra=Barra(nombre = 'uno',D=0.0378,area=0.00075,f_y=530000, precio =20000),
                                    D_p= 0.115,η= 1,proc_iny= "IGU",f_pc= 21000,
                                    f_py= 450000,A_camisa= 0, db = 0.0254, 
                                    perfil=self.perfil_4, 
                                    α=0, ω=0, f_carga_mp=0.6)
        
        q_ult, memoria = micropilotes.calculo_capacidad_portante()
        print(memoria)
        self.assertAlmostEqual(q_ult, 790.44, places=2)

    def test_calculo_capacidad_portante6(self):#S
        micropilotes = Micropilotes(D_f=1.7,HG = 1, D_d=0,  H = 0.5, S_m = 0.4,
                                    TP= 0.4, θ= 0, γ_c=24,N_m= 4,
                                    P_anc=1, L_b= 5, 
                                    barra=Barra(nombre = 'uno',D=0.0378,area=0.00075,f_y=530000, precio =20000),
                                    D_p= 0.054,η= 1,proc_iny= "IGU",f_pc= 21000,
                                    f_py= 450000,A_camisa= 0, db = 0.0254, 
                                    perfil=self.perfil_4, 
                                    α=0, ω=0, f_carga_mp=0.6)
        
        q_ult, memoria = micropilotes.calculo_capacidad_portante()
        print(memoria)
        self.assertAlmostEqual(q_ult, 844.90, places=2)

    def test_calculo_capacidad_portante7(self):#S
        micropilotes = Micropilotes(D_f=1.7,HG = 1, D_d=0,  H = 0.5, S_m = 0.4,
                                    TP= 0.4, θ= 0, γ_c=24,N_m= 5,
                                    P_anc=0.5, L_b= 5, 
                                    barra=Barra(nombre = 'uno',D=0.0378,area=0.00075,f_y=530000, precio =20000),
                                    D_p= 0.07,η= 1,proc_iny= "IGU",f_pc= 21000,
                                    f_py= 450000,A_camisa= 0, db = 0.0254, 
                                    perfil=self.perfil_4, 
                                    α=0, ω=0, f_carga_mp=0.6)
        
        q_ult, memoria = micropilotes.calculo_capacidad_portante()
        print(memoria)
        self.assertAlmostEqual(q_ult, 829.21, places=2)

    def test_calculo_capacidad_portante8(self):#S
        micropilotes = Micropilotes(D_f=1.4,HG = 1, D_d=0,  H = 0.6, S_m = 0.4, 
                                    TP= 0.6, θ= 0, γ_c=24,N_m= 5,
                                    P_anc=0.8, L_b= 5, 
                                    barra=Barra(nombre = 'uno',D=0.0378,area=0.00075,f_y=530000, precio =20000),
                                    D_p= 0.07,η= 1,proc_iny= "IGU",f_pc= 21000,
                                    f_py= 450000,A_camisa= 0, db = 0.0254, 
                                    perfil=self.perfil_4, 
                                    α=0, ω=0, f_carga_mp=0.7)
        
        q_ult, memoria = micropilotes.calculo_capacidad_portante()
        print(memoria)
        self.assertAlmostEqual(q_ult, 739.99, places=2)

    def test_calculo_capacidad_portante9(self):#S
        micropilotes = Micropilotes(D_f=1.5,HG = 1.1, D_d=0, H = 0.4, S_m = 0.4, 
                                    TP= 0.5, θ= 0, γ_c=24,N_m= 5,
                                    P_anc=1.2, L_b= 5, 
                                    barra=Barra(nombre = 'uno',D=0.0378,area=0.00075,f_y=530000, precio =20000),
                                    D_p= 0.12,η= 1,proc_iny= "IGU",f_pc= 21000,
                                    f_py= 450000,A_camisa= 0, db = 0.0254, 
                                    perfil=self.perfil_4, 
                                    α=0, ω=0, f_carga_mp=0.7)
        
        q_ult, memoria = micropilotes.calculo_capacidad_portante()
        print(memoria)
        self.assertAlmostEqual(q_ult, 771.60, places=2)

    def test_calculo_capacidad_portante_10(self):#S
        micropilotes = Micropilotes(D_f=1.5,HG = 1, D_d=0,  H = 0.5, S_m = 0.4,
                                    TP= 0.6, θ= 0, γ_c=24,N_m= 5,
                                    P_anc=0.4, L_b= 5, 
                                    barra=Barra(nombre = 'uno',D=0.0378,area=0.00075,f_y=530000, precio =20000),
                                    D_p= 0.12,η= 1,proc_iny= "IGU",f_pc= 21000,
                                    f_py= 450000,A_camisa= 0, db = 0.0254, 
                                    perfil=self.perfil_1Sat, 
                                    α=0, ω=0, f_carga_mp=0.5)
        
        q_ult, memoria = micropilotes.calculo_capacidad_portante()
        print(memoria)
        self.assertAlmostEqual(q_ult, 270.09, places=2)
    
    def test_calculo_capacidad_portante_11(self):#S
        micropilotes = Micropilotes(D_f=1.3,HG = 1, D_d=0,   H = 0.5, S_m = 0.4,
                                    TP= 0.6, θ= 0, γ_c=24,N_m= 5,
                                    P_anc=0.4, L_b= 5, 
                                    barra=Barra(nombre = 'uno',D=0.0378,area=0.00075,f_y=530000, precio =20000),
                                    D_p= 0.12,η= 1,proc_iny= "IGU",f_pc= 21000,
                                    f_py= 450000,A_camisa= 0, db = 0.0254, 
                                    perfil=self.perfil_1, 
                                    α=0, ω=0, f_carga_mp=0.5)
        
        q_ult, memoria = micropilotes.calculo_capacidad_portante()
        print(memoria)
        self.assertAlmostEqual(q_ult, 262.35, places=2)

    def test_calculo_carga_compresion_varilla1(self):
        micropilotes = Micropilotes(D_f=1.2, HG = 1, D_d=0,  H = 0.5, S_m = 0.4, 
                            TP= 0.4,θ= 0,γ_c=24,N_m= 8, P_anc=1, L_b= 15, 
                            barra=Barra(nombre = 'uno',D=0.0378,area=0.00075,f_y=530000, precio =20000),
                            D_p= 0.115,η= 1,proc_iny= "IGU",f_pc= 21000,f_py= 420000,
                            A_camisa= 0, db = 0.0254, perfil=self.perfil_1, 
                            α=0, ω=0, f_carga_mp=0.6)
        prueba3,memoria = micropilotes.calculo_carga_compresion_varilla()
        print(memoria)
        self.assertAlmostEqual(prueba3,282.97,places=2)
    
    def test_calculo_carga_tension_varilla1(self):
        micropilotes=Micropilotes(D_f=1.2, HG = 1, D_d=0,  H = 0.5, S_m = 0.4, 
                            TP= 0.4,θ= 0,γ_c=24,N_m= 8, P_anc=1, L_b= 15, 
                            barra=Barra(nombre = 'uno',D=0.0378,area=0.00075,f_y=530000, precio =20000),
                            D_p= 0.115,η= 1,proc_iny= "IGU",f_pc= 21000,f_py= 420000,
                            A_camisa= 0, db = 0.0254, perfil=self.perfil_1, 
                            α=0, ω=0, f_carga_mp=0.6)
        prueba4,memoria = micropilotes.calculo_carga_tension_varilla()
        print(memoria)
        self.assertAlmostEqual(prueba4,218.625,places=3)    

    def test_calculo_adherencia_barra_grouting1(self):
        micropilotes=Micropilotes(D_f=1.2, HG = 1, D_d=0,   H = 0.5, S_m = 0.4, 
                            TP= 0.4,θ= 0,γ_c=24,N_m= 8, P_anc=1, L_b= 15, 
                            barra=Barra(nombre = 'uno',D=0.0378,area=0.00075,f_y=530000, precio =20000),
                            D_p= 0.115,η= 1,proc_iny= "IGU",f_pc= 21000,f_py= 420000,
                            A_camisa= 0, db = 0.0254, perfil=self.perfil_1, 
                            α=0, ω=0, f_carga_mp=0.6)
        prueba5,memoria = micropilotes.calculo_adherencia_barra_grouting()
        print(memoria)
        self.assertAlmostEqual(prueba5,8906.415,places=3)

    def test_calculo_resistencia_por_fuste_micropilote1(self):
        micropilotes = Micropilotes(D_f=1.5, HG = 1, D_d=0,   H = 0.5, S_m = 0.4, 
                                    TP= 0.4,θ= 0,γ_c=24,N_m= 4, P_anc=1, L_b= 6, 
                                    barra=Barra(nombre = 'uno',D=0.0378,area=0.00075,f_y=530000, precio =20000),
                                    D_p= 0.2,η= 1,proc_iny= "IGU",f_pc= 21000,f_py= 420000,
                                    A_camisa= 0, db = 0.0254, perfil=self.perfil_4, 
                                    α=0, ω=0, f_carga_mp=0.6)
        prueba7, memoria = micropilotes.calculo_resistencia_por_fuste_micropilote()
        print (memoria)
        self.assertAlmostEqual(prueba7, 618.52, places=2)        

    def test_calculo_carga_lateral_suelos_granulares1(self):
        micropilotes = Micropilotes(D_p= 0.13,  H = 0.5, S_m = 0.4, L_b= 7.5,N_m= 9,
                                    D_f=1.5,P_anc=0.1,
                                    TP= 1,HG = 1,θ= 0,
                                    D_d=0.2,
                                    db = 0.0254,f_py= 420000,f_pc= 21000,                                   

                                    perfil=self.perfil_4, 
                                    #Otros calculos
                                    barra=Barra(nombre = 'uno',D=0.0378,area=0.00075,f_y=530000, precio =20000),
                                    η= 1,proc_iny= "IGU",
                                    A_camisa= 0, α=0, ω=0, 
                                    f_carga_mp=1,γ_c=24)
        F_zc=800
        prueba,memoria= micropilotes.calculo_carga_lateral(F_zc)
        print(memoria) 
        self.assertAlmostEqual(prueba,358.879,places=3)

    def test_calculo_carga_lateral_suelos_granulares2(self):
        micropilotes = Micropilotes(D_p= 0.13,  H = 0.5, S_m = 0.4, L_b= 7.5,N_m= 5,
                                    D_f=1.5,P_anc=0.05,
                                    TP= 1,θ= 0,
                                    D_d=0.0,HG = 1,
                                    db = 0.0254,f_py= 420000,f_pc= 21000,                                   

                                    perfil=self.perfil_4, 
                                    #Otros calculos
                                    barra=Barra(nombre = 'uno',D=0.0378,area=0.00075,f_y=530000, precio =20000),
                                    η= 1,proc_iny= "IGU",
                                    A_camisa= 0, α=0, ω=0, 
                                    f_carga_mp=1,γ_c=24)
        F_zc=800
        prueba,memoria= micropilotes.calculo_carga_lateral(F_zc)
        print(memoria) 
        self.assertAlmostEqual(prueba,316.147,places=3)

    def test_calculo_carga_lateral_suelos_granulares3(self):
        micropilotes = Micropilotes(D_p= 0.13,  H = 0.5, S_m = 0.4, L_b= 7.5,N_m= 5,
                                    D_f=1.5,P_anc=0.05,
                                    TP= 1,θ= 0,
                                    D_d=0.5,HG = 1,
                                    db = 0.0254,f_py= 420000,f_pc= 21000,                                   
                                    perfil=self.perfil_4, 
                                    #Otros calculos
                                    barra=Barra(nombre = 'uno',D=0.0378,area=0.00075,f_y=530000, precio =20000),
                                    η= 1,proc_iny= "IGU",
                                    A_camisa= 0, α=0, ω=0, 
                                    f_carga_mp=1,γ_c=24)
        F_zc=800
        prueba,memoria= micropilotes.calculo_carga_lateral(F_zc)
        print(memoria) 
        self.assertAlmostEqual(prueba,394.433,places=3)

    def test_calculo_carga_lateral_suelos_granulares4(self):
        micropilotes = Micropilotes(D_p= 0.13,  H = 0.5, S_m = 0.6, L_b= 7.5,N_m= 5,
                                    D_f=1.5,P_anc=0.05,
                                    TP= 1,θ= 0,
                                    D_d=0.5,HG = 1,
                                    db = 0.0254,f_py= 420000,f_pc= 21000,                                   
                                    perfil=self.perfil_1, 
                                    #Otros calculos
                                    barra=Barra(nombre = 'uno',D=0.0378,area=0.00075,f_y=530000, precio =20000),
                                    η= 1,proc_iny= "IGU",
                                    A_camisa= 0, α=0, ω=0, 
                                    f_carga_mp=1,γ_c=24)
        F_zc=800
        prueba,memoria= micropilotes.calculo_carga_lateral(F_zc)
        print(memoria) 
        self.assertAlmostEqual(prueba,233.605,places=3)

    def test_calculo_carga_lateral_suelos_granulares5(self):
        micropilotes = Micropilotes(D_p= 0.13,  H = 0.5, S_m = 0.3, L_b= 7.5,N_m= 5,
                                    D_f=1.5,P_anc=0.1,
                                    TP= 0.8,θ= 0,
                                    D_d=0.5,HG = 1,
                                    db = 0.0254,f_py= 420000,f_pc= 21000,                                   
                                    perfil=self.perfil_6, 
                                    #Otros calculos
                                    barra=Barra(nombre = 'uno',D=0.0378,area=0.00075,f_y=530000, precio =20000),
                                    η= 1,proc_iny= "IGU",
                                    A_camisa= 0, α=0, ω=0, 
                                    f_carga_mp=1,γ_c=24)
        F_zc = 800
        prueba,memoria= micropilotes.calculo_carga_lateral(F_zc)
        print(memoria) 
        self.assertAlmostEqual(prueba,467.251,places=3)

    def test_calculo_carga_lateral_suelos_granulares6(self):
        micropilotes = Micropilotes(D_p= 0.13,  H = 0.6, S_m = 0.3, L_b= 7.5,N_m= 5,
                                    D_f=1.5,P_anc=0.1,
                                    TP= 0.8,θ= 0,
                                    D_d=0.5, HG = 1.3,
                                    db = 0.0254,f_py= 420000,f_pc= 21000,                                   
                                    perfil=self.perfil_2, 
                                    #Otros calculos
                                    barra=Barra(nombre = 'uno',D=0.0378,area=0.00075,f_y=530000, precio =20000),
                                    η= 1,proc_iny= "IGU",
                                    A_camisa= 0, α=0, ω=0, 
                                    f_carga_mp=1,γ_c=24)
        F_zc = 800
        prueba,memoria= micropilotes.calculo_carga_lateral(F_zc)
        print(memoria) 
        self.assertAlmostEqual(prueba,346.562,places=3)

    def test_calculo_carga_lateral_suelos_granulares7(self):
        micropilotes = Micropilotes(D_p= 0.10,  H = 0.4, S_m = 0.8, L_b= 6.5,N_m= 5,
                                    D_f=1.5,P_anc=0.12,
                                    TP= 0.8,θ= 0,
                                    D_d=0.5,HG = 1.3,
                                    db = 0.0254,f_py= 420000,f_pc= 21000,                                   
                                    perfil=self.perfil_2, 
                                    #Otros calculos
                                    barra=Barra(nombre = 'uno',D=0.0378,area=0.00075,f_y=530000, precio =20000),
                                    η= 1,proc_iny= "IGU",
                                    A_camisa= 0, α=0, ω=0, 
                                    f_carga_mp=0.6,γ_c=24)
        F_zc = 1000
        prueba,memoria= micropilotes.calculo_carga_lateral(F_zc)
        print(memoria) 
        self.assertAlmostEqual(prueba,382.144,places=3)

    def test_calculo_carga_lateral_suelos_granulares8(self):
        micropilotes = Micropilotes(D_p= 0.08,  H = 0.5, S_m = 0.4, L_b= 5.5,N_m= 5,
                                    D_f=1.5,P_anc=0.07,
                                    TP= 0.7,θ = 0,
                                    D_d=0.5,HG = 1.3,
                                    db = 0.0254,f_py= 420000,f_pc= 21000,                                   
                                    perfil=self.perfil_2, 
                                    #Otros calculos
                                    barra=Barra(nombre = 'uno',D=0.0378,area=0.00075,f_y=530000, precio =20000),
                                    η= 1,proc_iny= "IGU",
                                    A_camisa= 0, α=0, ω=0, 
                                    f_carga_mp=0.7,γ_c=24)
        F_zc = 900
        prueba,memoria= micropilotes.calculo_carga_lateral(F_zc)
        print(memoria) 
        self.assertAlmostEqual(prueba,354.952,places=3)

    def test_calculo_carga_lateral_suelos_granulares9(self):
        micropilotes = Micropilotes(D_p= 0.1,  H = 0.5, S_m = 0.4, L_b= 10,N_m= 9,
                                    D_f=1.5,P_anc=0.92,
                                    TP= 0.8,θ = 0,
                                    D_d=0.2,HG = 1,
                                    db = 0.0254,f_py= 420000,f_pc= 21000,                                   
                                    perfil=self.perfil_3, 
                                    #Otros calculos
                                    barra=Barra(nombre = 'uno',D=0.0378,area=0.00075,f_y=530000, precio =20000),
                                    η= 1,proc_iny= "IGU",
                                    A_camisa= 0, α=0, ω=0, 
                                    f_carga_mp=0.7,γ_c=24)
        F_zc = 900
        prueba,memoria= micropilotes.calculo_carga_lateral(F_zc)
        print(memoria) 
        self.assertAlmostEqual(prueba,378.218,places=3)

    def test_calculo_carga_lateral_suelos_granulares_10(self):
        micropilotes = Micropilotes(D_p= 0.13, H = 0.6, S_m = 0.4, L_b= 8.5, N_m= 9,
                                    D_f=1.5,P_anc=0.5,
                                    TP= 0.8,θ = 0,
                                    D_d=0.4,HG = 1,
                                    db = 0.0254,f_py= 420000,f_pc= 21000,                                   
                                    perfil=self.perfil_1Sat, 
                                    #Otros calculos
                                    barra=Barra(nombre = 'uno',D=0.0378,area=0.00075,f_y=530000, precio =20000),
                                    η= 1,proc_iny= "IGU",
                                    A_camisa= 0, α=0, ω=0, 
                                    f_carga_mp=0.5,γ_c=24)
        F_zc = 800
        prueba,memoria = micropilotes.calculo_carga_lateral(F_zc)
        print(memoria) 
        self.assertAlmostEqual(prueba,207.770,places=3)    

    def test_Nml_1(self):
        micropilotes = Micropilotes(D_f=1.0, HG = 1, D_d=0,  H= 0.5, 
                                TP= 0.4,θ= 0,γ_c=24,N_m= 8, S_m = 0.4, P_anc=1, L_b= 15, 
                                barra=Barra(nombre = 'uno',D=0.0378,area=0.00075,f_y=530000, precio =20000),
                                D_p= 0.115,η= 1,proc_iny= "IGU",f_pc= 21000,f_py= 420000,
                                A_camisa= 0, db = 0.0254, perfil=self.perfil_4, 
                                α=0, ω=0, f_carga_mp=0.6)
        Nml=micropilotes.N_mL
        print(Nml) 

    def test_Nml_2(self):
        micropilotes = Micropilotes(D_f=1.0, HG = 1, D_d=0,  H= 0.5,
                                TP= 0.4,θ= 0,γ_c=24,N_m= 5, S_m = 0.4, P_anc=1, L_b= 15, 
                                barra=Barra(nombre = 'uno',D=0.0378,area=0.00075,f_y=530000, precio =20000),
                                D_p= 0.115,η= 1,proc_iny= "IGU",f_pc= 21000,f_py= 420000,
                                A_camisa= 0, db = 0.0254, perfil=self.perfil_4, 
                                α=0, ω=0, f_carga_mp=0.6)
        Nml=micropilotes.N_mL
        print(Nml)  
    
    def test_Nml_3(self):
        micropilotes = Micropilotes(D_f=1.0, HG = 1, D_d=0, H= 0.5, 
                                TP= 0.5,θ= 0,γ_c=24,N_m= 12, S_m = 0.4, P_anc=1, L_b= 15, 
                                barra=Barra(nombre = 'uno',D=0.0378,area=0.00075,f_y=530000, precio =20000),
                                D_p= 0.115,η= 1,proc_iny= "IGU",f_pc= 21000,f_py= 420000,
                                A_camisa= 0, db = 0.0254, perfil=self.perfil_4, 
                                α=0, ω=0, f_carga_mp=0.6)
        Nml=micropilotes.N_mL
        print(Nml) 
        self.assertAlmostEqual(Nml,4,places=0)

    def test_calculo_resistencia_por_fuste_micropilote2(self):
        micropilotes = Micropilotes(D_f=1.5, HG = 1, D_d=0,  H = 0.5, S_m = 0.4, 
                                    TP= 0.4,θ= 0,γ_c=24,N_m= 4, P_anc=1, L_b= 6, 
                                    barra=Barra(nombre = 'uno',D=0.0378,area=0.00075,f_y=530000, precio =20000),
                                    D_p= 0.115,η= 1,proc_iny= "IGU",f_pc= 21000,f_py= 420000,
                                    A_camisa= 0, db = 0.0254, perfil=self.perfil_1Sat, 
                                    α=0, ω=0, f_carga_mp=0.6)
        prueba7, memoria = micropilotes.calculo_resistencia_por_fuste_micropilote()
        print (memoria)
        self.assertAlmostEqual(prueba7, 86.62, places=2)   

    def test_calculo_resistencia_por_fuste_micropilote3(self):
        micropilotes = Micropilotes(D_f=1.5, HG = 1, D_d=0,  H = 0.5, S_m = 0.4, 
                                    TP= 0.4,θ= 0,γ_c=24,N_m= 4, P_anc=1, L_b= 6, 
                                    barra=Barra(nombre = 'uno',D=0.0378,area=0.00075,f_y=530000, precio =20000),
                                    D_p= 0.115,η= 1,proc_iny= "IGU",f_pc= 21000,f_py= 420000,
                                    A_camisa= 0, db = 0.0254, perfil=self.perfil_1NF, 
                                    α=0, ω=0, f_carga_mp=0.6)
        prueba, memoria = micropilotes.calculo_resistencia_por_fuste_micropilote()
        print (memoria)
        self.assertAlmostEqual(prueba, 111.51, places=2)  
    
    def test_calculo_asentamiento1(self):
        micropilotes = Micropilotes(D_f=1.5, HG = 1,
                                    D_d=0,  H = 0.5, S_m = 0.4,TP= 0.8,
                                    θ= 0,γ_c=24,N_m= 8, 
                                    P_anc=0.3, L_b= 4.5, 
                                    barra=Barra(nombre = 'uno',D=0.0378,area=0.00075,f_y=530000, precio =20000),
                                    D_p= 0.2,η= 1,proc_iny= "IGU",
                                    f_pc= 21000,f_py= 420000,
                                    A_camisa= 0, db = 0.0254, 
                                    perfil=self.perfil_4, 
                                    α=0, ω=0, 
                                    f_carga_mp=0.6)
        k = 10
        F_zc = 1000
        F_zc_eds = 100
        t = 50
    
        prueba, _, memoria, _ = micropilotes.calculo_asentamiento(k, F_zc, F_zc_eds, t)
        print (memoria)
        self.assertAlmostEqual(prueba, 0.0322, places=4)   

    def test_calculo_tension_suelos_granulares1(self):
        micropilotes = Micropilotes(D_f=1.5, HG = 1, D_d=0, 
                                    H = 0.6, S_m = 1, TP= 0.8,θ= 0,γ_c=24,
                                    N_m= 8, P_anc=0.3, L_b= 4.5, 
                                    barra=Barra(nombre = 'uno',D=0.0378,area=0.00075,f_y=530000, precio =20000),
                                    D_p= 0.2,η= 1,proc_iny= "IGU",f_pc= 21000,f_py= 420000,
                                    A_camisa= 0, db = 0.0254, perfil=self.perfil_4, 
                                    α=0, ω=0, f_carga_mp=0.6
                                    )

        prueba, memoria = micropilotes.calculo_tension_suelos_granulares()
        print (memoria)
        self.assertAlmostEqual(prueba, 1007.089, places=3)            

    def test_calculo_tension_suelos_cohesivos1(self):
        micropilotes = Micropilotes(D_f=1.5, HG = 1, D_d=0,  H = 0.5, S_m = 0.9, 
                                    TP= 0.8,θ= 0,γ_c=24,N_m= 8, P_anc=0.3, L_b= 4.5, 
                                    barra=Barra(nombre = 'uno',D=0.0378,area=0.00075,f_y=530000, precio =20000),
                                    D_p= 0.2,η= 1,proc_iny= "IGU",f_pc= 21000,f_py= 420000,
                                    A_camisa= 0, db = 0.0254, perfil=self.perfil_1, 
                                    α=0, ω=0, f_carga_mp=0.6)
        prueba, memoria = micropilotes.calculo_tension_suelos_cohesivos()
        print (memoria)
        self.assertAlmostEqual(prueba, 2075.150, places=3)   

    def test_calculo_tension_roca1(self):
        micropilotes = Micropilotes(D_p= 0.150, L_b= 4.5,N_m= 4,
                                    D_f=1.2,P_anc=0.1,
                                    TP= 1,  H = 0.5, S_m = 0.4,
                                    θ= 0,D_d=0.0,HG = 1,
                                    db = 0.0254,f_py= 420000,f_pc= 21000,                                   
                                    perfil=self.perfil_3, 
                                    #Otros calculos
                                    barra=Barra(nombre = 'uno',D=0.0378,area=0.00075,f_y=530000, precio =20000),
                                    η= 1,proc_iny= "IGU",
                                    A_camisa= 0, α=0, ω=0, 
                                    f_carga_mp=1,γ_c=24)
        prueba, memoria= micropilotes.calculo_tension_roca()
        print (memoria)
        self.assertAlmostEqual(prueba,26863.436,places=3)

    
    def test_calculo_integral_presion_lateral_activa_desde_0_prueba1(self):
        micropilotes = Micropilotes(D_f=1.5, HG = 1,
                                    D_d=0, H = 0.5, S_m = 0.4, TP= 0.8,
                                    θ= 0,γ_c=24,N_m= 8, 
                                    P_anc=0.3, L_b= 4.5, 
                                    barra=Barra(nombre = 'uno',D=0.0378,area=0.00075,f_y=530000, precio =20000),
                                    D_p= 0.2,η= 1,proc_iny= "IGU",
                                    f_pc= 21000,f_py= 420000,
                                    A_camisa= 0, db = 0.0254, 
                                    perfil=self.perfil_4, 
                                    α=0, ω=0, 
                                    f_carga_mp=0.6)
        prof = 1.5
        prueba = micropilotes.calculo_integral_presion_lateral_activa_desde_0(prof)
        self.assertAlmostEqual(prueba, 8.123,places=3)

    def test_calculo_integral_presion_lateral_activa_desde_0_prueba2(self):
        micropilotes = Micropilotes(D_f=1.5, HG = 1,
                                    D_d=0,  H = 0.5, S_m = 0.4, TP= 0.8,
                                    θ= 0,γ_c=24,N_m= 8, 
                                    P_anc=0.3, L_b= 4.5, 
                                    barra=Barra(nombre = 'uno',D=0.0378,area=0.00075,f_y=530000, precio =20000),
                                    D_p= 0.2,η= 1,proc_iny= "IGU",
                                    f_pc= 21000,f_py= 420000,
                                    A_camisa= 0, db = 0.0254, 
                                    perfil=self.perfil_4, 
                                    α=0, ω=0, 
                                    f_carga_mp=0.6)
        prof = 7
        prueba = micropilotes.calculo_integral_presion_lateral_activa_desde_0(prof)
        self.assertAlmostEqual(prueba, 156.085,places=3)

    def test_calculo_integral_presion_lateral_activa_desde_0_prueba3(self):
        micropilotes = Micropilotes(D_f=1.5, HG = 1,
                                    D_d=0,  H = 0.5, S_m = 0.4, TP= 0.8,
                                    θ= 0,γ_c=24,N_m= 8, 
                                    P_anc=0.3, L_b= 4.5, 
                                    barra=Barra(nombre = 'uno',D=0.0378,area=0.00075,f_y=530000, precio =20000),
                                    D_p= 0.2,η= 1,proc_iny= "IGU",
                                    f_pc= 21000,f_py= 420000,
                                    A_camisa= 0, db = 0.0254, 
                                    perfil=self.perfil_6, 
                                    α=0, ω=0, 
                                    f_carga_mp=0.6)
        prof = 9.5
        prueba = micropilotes.calculo_integral_presion_lateral_activa_desde_0(prof)
        self.assertAlmostEqual(prueba, 62.7210,places=4)
    def test_calculo_integral_presion_lateral_activa_desde_0_prueba4(self):
        micropilotes = Micropilotes(D_f=1.5, HG = 1,
                                    D_d=0,  H = 0.5, S_m = 0.4, TP= 0.8,
                                    θ= 0,γ_c=24,N_m= 8, 
                                    P_anc=0.3, L_b= 4.5, 
                                    barra=Barra(nombre = 'uno',D=0.0378,area=0.00075,f_y=530000, precio =20000),
                                    D_p= 0.2,η= 1,proc_iny= "IGU",
                                    f_pc= 21000,f_py= 420000,
                                    A_camisa= 0, db = 0.0254, 
                                    perfil=self.perfil_6, 
                                    α=0, ω=0, 
                                    f_carga_mp=0.6)
        prof = 9
        prueba = micropilotes.calculo_integral_presion_lateral_activa_desde_0(prof)
        self.assertAlmostEqual(prueba, 62.721,places=3)

    def test_calculo_integral_presion_lateral_pasiva_desde_0_prueba1(self):
        micropilotes = Micropilotes(D_p= 0.2, L_b= 4.5,N_m= 9,
                                    D_f=1.5,P_anc=0.1,
                                    TP= 1,  H = 0.5, S_m = 0.4,
                                    θ= 0,D_d=0.2,HG = 1,
                                    db = 0.0254,f_py= 420000,f_pc= 21000,                                   
                                    perfil=self.perfil_4, 
                                    #Otros calculos
                                    barra=Barra(nombre = 'uno',D=0.0378,area=0.00075,f_y=530000, precio =20000),
                                    η= 1,proc_iny= "IGU",
                                    A_camisa= 0, α=0, ω=0, 
                                    f_carga_mp=1,γ_c=24)
        prof = 9.6
        prueba = micropilotes.calculo_integral_presion_lateral_pasiva_desde_0(prof)
        self.assertAlmostEqual(prueba, 2543.5577,places=4)

    def test_calculo_integral_presion_lateral_pasiva_desde_0_prueba2(self):
        micropilotes = Micropilotes(D_p= 0.2, L_b= 4.5,N_m= 9,
                                    D_f=1.5,P_anc=0.1,
                                    TP= 1,  H = 0.5, S_m = 0.4,
                                    θ= 0,D_d=0.2,HG = 1,
                                    db = 0.0254,f_py= 420000,f_pc= 21000,                                   
                                    perfil=self.perfil_4, 
                                    #Otros calculos
                                    barra=Barra(nombre = 'uno',D=0.0378,area=0.00075,f_y=530000, precio =20000),
                                    η= 1,proc_iny= "IGU",
                                    A_camisa= 0, α=0, ω=0, 
                                    f_carga_mp=1,γ_c=24)
        prof = 1.5
        prueba = micropilotes.calculo_integral_presion_lateral_pasiva_desde_0(prof)
        self.assertAlmostEqual(prueba, 62.32,places=2)

    def test_calculo_integral_presion_lateral_pasiva_desde_0_prueba3(self):
        micropilotes = Micropilotes(D_p= 0.2, L_b= 4.5,N_m= 9,
                                    D_f=1.5,P_anc=0.1,
                                    TP= 1, H = 0.5, S_m = 0.4,
                                    θ= 0,D_d=0.2,HG = 1,
                                    db = 0.0254,f_py= 420000,f_pc= 21000,                                   
                                    perfil=self.perfil_1, 
                                    #Otros calculos
                                    barra=Barra(nombre = 'uno',D=0.0378,area=0.00075,f_y=530000, precio =20000),
                                    η= 1,proc_iny= "IGU",
                                    A_camisa= 0, α=0, ω=0, 
                                    f_carga_mp=1,γ_c=24)
        prof = 10.6
        prueba = micropilotes.calculo_integral_presion_lateral_pasiva_desde_0(prof)
        self.assertAlmostEqual(prueba, 2532.557,places=3)

    def test_calculo_integral_presion_lateral_pasiva_desde_0_prueba4(self):
        micropilotes = Micropilotes(D_p= 0.2, L_b= 4.5,N_m= 9,
                                    D_f=1.5,P_anc=0.1,
                                    TP= 1, H = 0.5, S_m = 0.4,
                                    θ= 0,D_d=0.2,HG = 1,
                                    db = 0.0254,f_py= 420000,f_pc= 21000,                                   
                                    perfil=self.perfil_3, 
                                    #Otros calculos
                                    barra=Barra(nombre = 'uno',D=0.0378,area=0.00075,f_y=530000, precio =20000),
                                    η= 1,proc_iny= "IGU",
                                    A_camisa= 0, α=0, ω=0, 
                                    f_carga_mp=1,γ_c=24)
        prof = 5
        prueba = micropilotes.calculo_integral_presion_lateral_pasiva_desde_0(prof)
        self.assertAlmostEqual(prueba, 702.8068,places=4)

if __name__ == '__main__':
    unittest.main()
