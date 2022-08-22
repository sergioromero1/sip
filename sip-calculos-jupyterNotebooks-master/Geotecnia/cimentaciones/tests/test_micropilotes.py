import unittest
from ..micropilotes import Micropilotes
from ..perfil import Perfil, Estrato
from ..barra import Barra

class TestMicropilotes(unittest.TestCase):

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

    def test_calculo_carga_compresion_01(self):
        micropilotes = Micropilotes( D_p =0.13,L_b =6, HG = 0.5, N_m =8 ,
                                     proc_iny = "IGU" ,θ = 0, 
                                     D_f =1.1 , D_d =0 , 
                                     S_m =1.0 , H =0.5,
                                     P_anc = 0.1, TP =1 , 
                                     db = 0.019050, f_pc =420000 , f_py = 21000,
                                     perfil=self.perfil_1,
                                     barra=Barra(nombre = 'uno',D=0.0378,area=0.00075,f_y=530000, precio =20000),
                                     ####VALORES FIJOS###
                                     A_camisa = 0,η=1,γ_c=24 ,
                                     α=0, ω=0, f_carga_mp=1
                                    )
        P_G, memoria = micropilotes.calculo_carga_compresion()
        print(memoria)
        P_G = memoria["P_G"]
        self.assertAlmostEqual(P_G, 183.228, places=3)
      
    def test_calculo_carga_compresion_02(self):
        micropilotes = Micropilotes( D_p =0.115,L_b =4.5, HG = 0.5, N_m =4 ,
                                     proc_iny = "IRS" ,θ = 8, 
                                     D_f =1.0 , D_d =0 , 
                                     S_m =1.0 , H =0.6,
                                     P_anc = 0.1, TP =0.6 , 
                                     db = 0.019050, f_pc =420000 , f_py = 21000,
                                     perfil=self.perfil_3, 
                                     barra=Barra(nombre = 'uno',D=0.0378,area=0.00075,f_y=530000, precio =20000),
                                     ####VALORES FIJOS###
                                     A_camisa=0,η=1,γ_c=24 ,
                                     α=0, ω=0, f_carga_mp=1
                                    )
        P_G, memoria = micropilotes.calculo_carga_compresion()
        print(memoria)
        P_G = memoria["P_G"]
        self.assertAlmostEqual(P_G, 5283.940, places=3)

    def test_calculo_carga_compresion_03(self):
        perfil_1 = Perfil([
            Estrato(H_0 = 1.3, γ_s = 18.0, N=8,  E_s = 2500, c_u =  33.36, φ_s = 24, saturado = False, tipo_mat = "c", c_p = 0,σ_pp=23.4,C_c=0.12,C_s=0.07,e_0=0.38),
            Estrato(H_0 = 3.2, γ_s = 15.0, N=6,  E_s = 2000, c_u =  28.36, φ_s = 24, saturado = False, tipo_mat = "c", c_p = 0,σ_pp=83.8,C_c=0.18,C_s=0.09,e_0=0.25),
            Estrato(H_0 = 2.1, γ_s = 19.0, N=17, E_s = 4800, c_u =  80.36, φ_s = 24, saturado = False, tipo_mat = "c", c_p = 0,σ_pp=125.4,C_c=0.09,C_s=0.02,e_0=0.22),
            Estrato(H_0 = 10.0, γ_s = 20.0, N=20, E_s = 6800, c_u = 120.36, φ_s = 24, saturado = False, tipo_mat = "c", c_p = 0,σ_pp=300,C_c=0.05,C_s=0.009,e_0=0.18),
        ])
        micropilotes = Micropilotes( D_p =0.150,L_b =15 , HG = 1, N_m =9 ,
                                     proc_iny = "IGU" ,θ = 10, 
                                     D_f =1.4 , D_d =0 , 
                                     S_m =1.3 , H =0.8,
                                     P_anc = 0.5, TP =1 , 
                                     db = 0.0254, f_pc =420000 , f_py = 21000,
                                     perfil=perfil_1, 
                                     barra=Barra(nombre = 'uno',D=0.0378,area=0.00075,f_y=530000, precio =20000),
                                     ####VALORES FIJOS###
                                     A_camisa=0,η=1,γ_c=24 ,
                                     α=0, ω=0, f_carga_mp=1
                                    )
        P_G, memoria = micropilotes.calculo_carga_compresion()
        print (memoria)
        P_G = memoria["P_G"]
        self.assertAlmostEqual(P_G, 795.824, places=2)

    def test_calculo_carga_compresion_04(self):
        micropilotes = Micropilotes( D_p =0.150,L_b =10.2 , HG = 0.5, N_m =5 ,
                                     proc_iny = "IGU" ,θ = 0, 
                                     D_f =1 , D_d =0 , 
                                     S_m =1.5 , H =0.6,
                                     P_anc = 0.1, TP =1 , 
                                     db = 0.019050, f_pc =420000 , f_py = 21000,
                                     perfil=self.perfil_2, 
                                     barra=Barra(nombre = 'uno',D=0.0378,area=0.00075,f_y=530000, precio =20000),
                                     ####VALORES FIJOS###
                                     A_camisa=0,η=1,γ_c=24 ,
                                     α=0, ω=0, f_carga_mp=1
                                    )
        P_G, memoria = micropilotes.calculo_carga_compresion()
        print(memoria)
        self.assertAlmostEqual(P_G, 92256.623, places=3)

    def test_calculo_carga_compresion_05(self):#S
        micropilotes = Micropilotes( D_p =0.2,L_b =6 , HG = 0.5, N_m =12 ,
                                     proc_iny = "IGU" ,θ = 0, 
                                     D_f =1.4 , D_d =0 , 
                                     S_m =1.5 , H =0.6,
                                     P_anc = 0.1, TP =1 , 
                                     db = 0.019050, f_pc =420000 , f_py = 21000,
                                     perfil=self.perfil_1, 
                                     barra=Barra(nombre = 'uno',D=0.0378,area=0.00075,f_y=530000, precio =20000),
                                     ####VALORES FIJOS###
                                     A_camisa=0,η=1,γ_c=24 ,
                                     α=0, ω=0, f_carga_mp=1
                                    )
        P_G, memoria = micropilotes.calculo_carga_compresion()
        print(memoria)
        self.assertAlmostEqual(P_G, 3567.497, places=2)

    def test_calculo_carga_compresion_06(self):#S
        micropilotes = Micropilotes( D_p =0.2,L_b =6 , HG = 0.5, N_m =4 ,
                                     proc_iny = "IGU" ,θ = 0, 
                                     D_f =1.4 , D_d =0 , 
                                     S_m =1.5 , H =0.6,
                                     P_anc = 0.1, TP =1 , 
                                     db = 0.019050, f_pc =420000 , f_py = 21000,
                                     perfil=self.perfil_1, 
                                     barra=Barra(nombre = 'uno',D=0.0378,area=0.00075,f_y=530000, precio =20000),
                                     ####VALORES FIJOS###
                                     A_camisa=0,η=1,γ_c=24 ,
                                     α=0, ω=0, f_carga_mp=1
                                    )
        P_G, memoria = micropilotes.calculo_carga_compresion()
        print(memoria)
        self.assertAlmostEqual(P_G, 1189.17, places=2)

    def test_calculo_carga_compresion_07(self):#S
        micropilotes = Micropilotes( D_p =0.2,L_b =4 , HG = 0.5, N_m =12 ,
                                     proc_iny = "IGU" ,θ = 0, 
                                     D_f =1.4 , D_d =0 , 
                                     S_m =1.5 , H =0.6,
                                     P_anc = 0.1, TP =1 , 
                                     db = 0.019050, f_pc =420000 , f_py = 21000,
                                     perfil=self.perfil_1, 
                                     barra=Barra(nombre = 'uno',D=0.0378,area=0.00075,f_y=530000, precio =20000),
                                     ####VALORES FIJOS###
                                     A_camisa=0,η=1,γ_c=24 ,
                                     α=0, ω=0, f_carga_mp=1
                                    )
        P_G, memoria = micropilotes.calculo_carga_compresion()
        print(memoria)
        self.assertAlmostEqual(P_G, 1731.312, places=2)

    def test_calculo_carga_compresion_08(self):#S
        micropilotes = Micropilotes( D_p =0.2,L_b =8 , HG = 0.5, N_m =5 ,
                                     proc_iny = "IGU" ,θ = 0, 
                                     D_f =1.4 , D_d =0 , 
                                     S_m =1.5 , H =0.6,
                                     P_anc = 0.1, TP =1 , 
                                     db = 0.019050, f_pc =420000 , f_py = 21000,
                                     perfil=self.perfil_1, 
                                     barra=Barra(nombre = 'uno',D=0.0378,area=0.00075,f_y=530000, precio =20000),
                                     ####VALORES FIJOS###
                                     A_camisa=0,η=1,γ_c=24 ,
                                     α=0, ω=0, f_carga_mp=1
                                    )
        P_G, memoria = micropilotes.calculo_carga_compresion()
        print(memoria)
        self.assertAlmostEqual(P_G, 2317.22, places=2)

    def test_calculo_carga_compresion_09(self):
        micropilotes = Micropilotes( D_p =0.2,L_b =4 , HG = 0.5,N_m =8 ,
                                     proc_iny = "IGU" ,θ = 0, 
                                     D_f =1.4 , D_d =0 , 
                                     S_m =1.5 , H =0.6,
                                     P_anc = 0.1, TP =1 , 
                                     db = 0.019050, f_pc =420000 , f_py = 21000,
                                     perfil=self.perfil_1, 
                                     barra=Barra(nombre = 'uno',D=0.0378,area=0.00075,f_y=530000, precio =20000),
                                     ####VALORES FIJOS###
                                     A_camisa=0,η=1,γ_c=24 ,
                                     α=0, ω=0, f_carga_mp=1
                                    )
        P_G, memoria = micropilotes.calculo_carga_compresion()
        print(memoria)
        self.assertAlmostEqual(P_G, 1154.21, places=2)

    def test_calculo_carga_compresion_10(self):#S
        micropilotes = Micropilotes( D_p =0.15,L_b =6 , HG = 0.5, N_m =8 ,
                                     proc_iny = "IGU" ,θ = 0, 
                                     D_f =1.4 , D_d =0 , 
                                     S_m =1.5 , H =0.6,
                                     P_anc = 0.1, TP =1 , 
                                     db = 0.019050, f_pc =420000 , f_py = 21000,
                                     perfil=self.perfil_1, 
                                     barra=Barra(nombre = 'uno',D=0.0378,area=0.00075,f_y=530000, precio =20000),
                                     ####VALORES FIJOS###
                                     A_camisa=0,η=1,γ_c=24 ,
                                     α=0, ω=0, f_carga_mp=1
                                    )
        P_G, memoria = micropilotes.calculo_carga_compresion()
        print(memoria)
        self.assertAlmostEqual(P_G, 1783.75, places=2)

    def test_calculo_carga_compresion_varilla_1(self):
        micropilotes = Micropilotes( D_p =0.2,L_b =6 , HG = 0.5, N_m =12 ,
                                     proc_iny = "IGU" ,θ = 0, 
                                     D_f =1.4 , D_d =0 , 
                                     S_m =1.5 , H =0.6,
                                     P_anc = 0.1, TP =1 , 
                                     db = 0.019050, f_pc =21000 , f_py = 420000,
                                     perfil=self.perfil_1, 
                                     barra=Barra(nombre = 'uno',D=0.0378,area=0.00075,f_y=530000, precio =20000),
                                     ####VALORES FIJOS###
                                     A_camisa=0,η=1,γ_c=24 ,
                                     α=0, ω=0, f_carga_mp=1
                                    )
        micropilotes,memoria = micropilotes.calculo_carga_compresion_varilla()
        print(memoria)
        self.assertAlmostEqual(micropilotes,496.710,places=3)

    def test_calculo_carga_compresion_varilla_2(self):
        micropilotes = Micropilotes( D_p =0.115,L_b =4 , HG = 0.5, N_m =8 ,
                                     proc_iny = "IRS" ,θ = 0, 
                                     D_f =1.4 , D_d =0 , 
                                     S_m =1.5 , H =0.6,
                                     P_anc = 0.1, TP =1 , 
                                     db = 0.019050, f_pc =21000 , f_py = 420000,
                                     perfil=self.perfil_6, 
                                     barra=Barra(nombre = 'uno',D=0.0378,area=0.00075,f_y=530000, precio =20000),
                                     ####VALORES FIJOS###
                                     A_camisa=0,η=1,γ_c=24 ,
                                     α=0, ω=0, f_carga_mp=1
                                    )
        micropilotes,memoria = micropilotes.calculo_carga_compresion_varilla()
        print(memoria)
        self.assertAlmostEqual(micropilotes,373.711,places=3)
    
    def test_calculo_carga_tension_varilla_1(self):
        micropilotes = Micropilotes( D_p =0.15,L_b =6 , HG = 0.5 ,N_m =12 ,
                                     proc_iny = "IGU" ,θ = 0, 
                                     D_f =1.4 , D_d =0 , 
                                     S_m =1.5 , H =0.6,
                                     P_anc = 0.1, TP =1 ,
                                     db = 0.019050, f_pc =420000 , f_py = 21000,
                                     perfil=self.perfil_1, 
                                     barra=Barra(nombre = 'uno',D=0.0378,area=0.00075,f_y=530000, precio =20000),

                                     ####VALORES FIJOS###
                                     A_camisa=0,η=1,γ_c=24 ,
                                     α=0, ω=0, f_carga_mp=1
                                    )
        micropilotes,memoria = micropilotes.calculo_carga_tension_varilla()
        print(memoria)
        self.assertAlmostEqual(micropilotes,218.625,places=3)    

    def test_calculo_carga_tension_varilla_2(self):
        micropilotes = Micropilotes( D_p =0.2,L_b =6 , HG = 0.5 , N_m =12 ,
                                     proc_iny = "IGU" ,θ = 0, 
                                     D_f =1.4 , D_d =0 , 
                                     S_m =1.5 , H =0.6,
                                     P_anc = 0.1, TP =1 , 
                                     db = 0.019050, f_pc =420000 , f_py = 21000,
                                     perfil=self.perfil_1, 
                                     barra=Barra(nombre = 'uno',D=0.0378,area=0.00075,f_y=530000, precio =20000),
                                     ####VALORES FIJOS###
                                     A_camisa=0,η=1,γ_c=24 ,
                                     α=0, ω=0, f_carga_mp=1
                                    )
        micropilotes,memoria = micropilotes.calculo_carga_tension_varilla()
        print(memoria)
        self.assertAlmostEqual(micropilotes,218.625,places=3) 

    def test_calculo_adherencia_barra_grouting_1(self):
        micropilotes = Micropilotes( D_p =0.115,L_b =10 ,HG =0.5, N_m =8 ,
                                     proc_iny = "IGU" ,θ = 0, 
                                     D_f =1.4 , D_d =0 , 
                                     S_m =1.5 , H =0.6,
                                     P_anc = 0.1, TP =1 ,
                                     db = 0.019050, f_pc =420000 , f_py = 21000,
                                     perfil=self.perfil_6, 
                                     barra=Barra(nombre = 'uno',D=0.0378,area=0.00075,f_y=530000, precio =20000),
                                     ####VALORES FIJOS###
                                     A_camisa=0,η=1,γ_c=24 ,
                                     α=0, ω=0, f_carga_mp=1
                                    )
        micropilotes,memoria = micropilotes.calculo_adherencia_barra_grouting()
        print(memoria)
        self.assertAlmostEqual(micropilotes,5937.610,places=3)

    def test_calculo_adherencia_barra_grouting_2(self):
        micropilotes = Micropilotes( D_p =0.2,L_b =6 ,HG=0.5, N_m =12 ,
                                     proc_iny = "IRS" ,θ = 0, 
                                     D_f =1.4 , D_d =0 , 
                                     S_m =1.5 , H =0.6,
                                     P_anc = 0.1, TP =1 , 
                                     db = 0.019050, f_pc =420000 , f_py = 21000,
                                     perfil=self.perfil_6, 
                                     barra=Barra(nombre = 'uno',D=0.0378,area=0.00075,f_y=530000, precio =20000),
                                     ####VALORES FIJOS###
                                     A_camisa=0,η=1,γ_c=24 ,
                                     α=0, ω=0, f_carga_mp=1
                                    )
        micropilotes,memoria = micropilotes.calculo_adherencia_barra_grouting()   
        print(memoria)
        self.assertAlmostEquals(micropilotes,3562.566,places=3)

    def test_calculo_adherencia_barra_grouting_3(self):
        micropilotes = Micropilotes( D_p =0.2,L_b =6 , HG = 0.5, N_m =12 ,
                                     proc_iny = "IGU" ,θ = 0, 
                                     D_f =1.4 , D_d =0 , 
                                     S_m =1.5 , H =0.6,
                                     P_anc = 0.1, TP =1 , 
                                     db = 0.019050, f_pc =420000 , f_py = 21000,
                                     perfil=self.perfil_1, 
                                     barra=Barra(nombre = 'uno',D=0.0378,area=0.00075,f_y=530000, precio =20000),
                                     ####VALORES FIJOS###
                                     A_camisa=0,η=1,γ_c=24 ,
                                     α=0, ω=0, f_carga_mp=1
                                    )
        micropilotes,memoria = micropilotes.calculo_adherencia_barra_grouting()
        print(memoria)
        self.assertAlmostEquals(micropilotes,3562.566,places=3)

    def test_calculo_resistencia_por_fuste_micropilote_1(self):
        micropilotes = Micropilotes( D_p =0.2,L_b =6 , HG = 0.5, N_m =12 ,
                                     proc_iny = "IGU" ,θ = 0, 
                                     D_f =1.4 , D_d =0 , 
                                     S_m =1.5 , H =0.6,
                                     P_anc = 0.1, TP =1 ,
                                     db = 0.019050, f_pc =420000 , f_py = 21000,
                                     perfil=self.perfil_1, 
                                     barra=Barra(nombre = 'uno',D=0.0378,area=0.00075,f_y=530000, precio =20000),
                                     ####VALORES FIJOS###
                                     A_camisa=0,η=1,γ_c=24 ,
                                     α=0, ω=0, f_carga_mp=1
                                    )
        micropilotes, memoria = micropilotes.calculo_resistencia_por_fuste_micropilote()
        print (memoria)
        self.assertAlmostEqual(micropilotes, 297.291, places=2)   

    def test_calculo_resistencia_por_fuste_micropilote_2(self):
        micropilotes = Micropilotes( D_p =0.2,L_b =6 , HG = 0.5, N_m =12 ,
                                     proc_iny = "IGU" ,θ = 0, 
                                     D_f =1.4 , D_d =0 , 
                                     S_m =1.5 , H =0.6,
                                     P_anc = 0.1, TP =1 , 
                                     db = 0.019050, f_pc =420000 , f_py = 21000,
                                     perfil=self.perfil_2, 
                                     barra=Barra(nombre = 'uno',D=0.0378,area=0.00075,f_y=530000, precio =20000),
                                     ####VALORES FIJOS###
                                     A_camisa=0,η=1,γ_c=24 ,
                                     α=0, ω=0, f_carga_mp=1
                                    )
        micropilotes, memoria = micropilotes.calculo_resistencia_por_fuste_micropilote()
        print (memoria)
        self.assertAlmostEqual(micropilotes, 278.197, places=2)   

    def test_calculo_resistencia_por_fuste_micropilote_3(self):
        micropilotes = Micropilotes( D_p =0.2,L_b =6 , HG = 0.5, N_m =12 ,
                                     proc_iny = "IGU" ,θ = 0, 
                                     D_f =1.4 , D_d =0 , 
                                     S_m =1.5 , H =0.6,
                                     P_anc = 0.1, TP =1 ,
                                     db = 0.019050, f_pc =420000 , f_py = 21000,
                                     perfil=self.perfil_3, 
                                     barra=Barra(nombre = 'uno',D=0.0378,area=0.00075,f_y=530000, precio =20000),
                                     ####VALORES FIJOS###
                                     A_camisa=0,η=1,γ_c=24 ,
                                     α=0, ω=0, f_carga_mp=1
                                    )
        micropilotes, memoria = micropilotes.calculo_resistencia_por_fuste_micropilote()
        print (memoria)
        self.assertAlmostEqual(micropilotes, 31042.94, places=2)  

    def test_calculo_carga_lateral_01(self):
        micropilotes = Micropilotes( D_p =0.115,L_b =5 , HG = 0.5, N_m =8 ,
                                     proc_iny = "IGU" ,θ = 0, 
                                     D_f =1.4 , D_d =0 , 
                                     S_m =1.5 , H =0.6,
                                     P_anc = 0.1, TP =1 , 
                                     db = 0.019050, f_pc =420000 , f_py = 21000,
                                     perfil=self.perfil_1, 
                                     barra=Barra(nombre = 'uno',D=0.0378,area=0.00075,f_y=530000, precio =20000),
                                     ####VALORES FIJOS###
                                     A_camisa=0,η=1,γ_c=24 ,
                                     α=0, ω=0, f_carga_mp=1
                                    )   
        F_zc=800
        micropilotes,memoria= micropilotes.calculo_carga_lateral(F_zc)
        print(memoria) 
        self.assertAlmostEqual(micropilotes,428.562,places=3)  

    def test_calculo_carga_lateral_02(self):
        micropilotes = Micropilotes( D_p =0.115,L_b =7 , HG = 0.5, N_m =9 ,
                                     proc_iny = "IGU" ,θ = 0, 
                                     D_f =1.4 , D_d =0 , 
                                     S_m =1.5 , H =0.6,
                                     P_anc = 0.1, TP =1 , 
                                     db = 0.019050, f_pc =420000 , f_py = 21000,
                                     perfil=self.perfil_1, 
                                     barra=Barra(nombre = 'uno',D=0.0378,area=0.00075,f_y=530000, precio =20000),
                                     ####VALORES FIJOS###
                                     A_camisa=0,η=1,γ_c=24 ,
                                     α=0, ω=0, f_carga_mp=1
                                    )
        F_zc=800
        micropilotes,memoria= micropilotes.calculo_carga_lateral(F_zc)
        print(memoria) 
        self.assertAlmostEqual(micropilotes,499.937,places=3)   

    def test_calculo_tension_suelos_cohesivos_1(self):
        micropilotes = Micropilotes( D_p =0.2,L_b =6 , HG = 0.5,  N_m =12 ,
                                     proc_iny = "IGU" ,θ = 0, 
                                     D_f =1.4 , D_d =0 , 
                                     S_m =1.5 , H =0.6,
                                     P_anc = 0.1, TP =1 , 
                                     db = 0.019050, f_pc =420000 , f_py = 21000,
                                     perfil=self.perfil_1,
                                     barra=Barra(nombre = 'uno',D=0.0378,area=0.00075,f_y=530000, precio =20000),
                                     ####VALORES FIJOS###
                                     A_camisa=0,η=1,γ_c=24 ,
                                     α=0, ω=0, f_carga_mp=1
                                    )
        micropilotes,memoria=micropilotes.calculo_tension_suelos_cohesivos()
        print(memoria)
        self.assertAlmostEqual(micropilotes,9378.778,places=3)

    def test_Nml_1(self):
        micropilotes = Micropilotes( D_p =0.2,L_b =6 , HG = 1, N_m =12 ,
                                     proc_iny = "IGU" ,θ = 0, 
                                     D_f =1.4 , D_d =0 , 
                                     S_m =1.5 , H =0.6,
                                     P_anc = 0.1, TP =1 , 
                                     db = 0.019050, f_pc =420000 , f_py = 21000,
                                     perfil=self.perfil_1, 
                                     barra=Barra(nombre = 'uno',D=0.0378,area=0.00075,f_y=530000, precio =20000),
                                     ####VALORES FIJOS###
                                     A_camisa=0,η=1,γ_c=24 ,
                                     α=0, ω=0, f_carga_mp=1
                                    )
        Nml=micropilotes.N_mL
        print(Nml)
        self.assertAlmostEqual(Nml,4,places=0)

    def test_Nml_2(self):
        micropilotes = Micropilotes( D_p =0.2,L_b =6 , HG= 1, N_m =12 ,
                                     proc_iny = "IGU" ,θ = 0, 
                                     D_f =1.4 , D_d =0 ,
                                     S_m =1.5 , H =0.6,
                                     P_anc = 0.1, TP =1 ,
                                     db = 0.019050, f_pc =420000 , f_py = 21000,
                                     perfil=self.perfil_1, 
                                     barra=Barra(nombre = 'uno',D=0.0378,area=0.00075,f_y=530000, precio =20000),
                                     ####VALORES FIJOS###
                                     A_camisa=0,η=1,γ_c=24 ,
                                     α=0, ω=0, f_carga_mp=1
                                    )
        Nml=micropilotes.N_mL
        print(Nml) 
        self.assertAlmostEqual(Nml,4,places=0)
    
    def test_Nml_3(self):
        micropilotes = Micropilotes( D_p =0.2,L_b =6 , HG= 0.5, N_m =12 ,
                                     proc_iny = "IGU" ,θ = 0, 
                                     D_f =1.4 , D_d =0 ,
                                     S_m =1.5 , H =0.6,
                                     P_anc = 0.1, TP =1 ,
                                     db = 0.019050, f_pc =420000 , f_py = 21000,
                                     perfil=self.perfil_1, 
                                     barra=Barra(nombre = 'uno',D=0.0378,area=0.00075,f_y=530000, precio =20000),
                                     ####VALORES FIJOS###
                                     A_camisa=0,η=1,γ_c=24 ,
                                     α=0, ω=0, f_carga_mp=1
                                    )
        Nml=micropilotes.N_mL
        print(Nml) 
        self.assertAlmostEqual(Nml,4,places=0)
    
    def test_calculo_tension_suelos_granulares_1(self):
        micropilotes = Micropilotes( D_p =0.2,L_b =6 , HG = 0.5,  N_m =12 ,
                                     proc_iny = "IGU" ,θ = 0, 
                                     D_f =1.4 , D_d =0 , 
                                     S_m =1.5 , H =0.6,
                                     P_anc = 0.1, TP =1 , 
                                     db = 0.019050, f_pc =420000 , f_py = 21000,
                                     perfil=self.perfil_1, 
                                     barra=Barra(nombre = 'uno',D=0.0378,area=0.00075,f_y=530000, precio =20000),
                                     ####VALORES FIJOS###
                                     A_camisa=0,η=1,γ_c=24 ,
                                     α=0, ω=0, f_carga_mp=1
                                    )
        prueba, memoria = micropilotes.calculo_tension_suelos_granulares()
        print (memoria)
        self.assertAlmostEqual(prueba, 3914.781, places=3)            

    def test_calculo_tension_suelos_granulares_2(self):
        micropilotes = Micropilotes( D_p =0.2,L_b =6 , HG = 0.5, N_m =12 ,
                                     proc_iny = "IGU" ,θ = 0, 
                                     D_f =1.4 , D_d =0 , 
                                     S_m =1.5 , H =0.6,
                                     P_anc = 0.1, TP =1 , 
                                     db = 0.019050, f_pc =420000 , f_py = 21000,
                                     perfil=self.perfil_4s, 
                                     barra=Barra(nombre = 'uno',D=0.0378,area=0.00075,f_y=530000, precio =20000),
                                     ####VALORES FIJOS###
                                     A_camisa=0,η=1,γ_c=24 ,
                                     α=0, ω=0, f_carga_mp=1
                                    )
        prueba, memoria = micropilotes.calculo_tension_suelos_granulares()
        print (memoria)
        self.assertAlmostEqual(prueba, 2211.685, places=3) 

    def test_calculo_tension_suelos_granulares_3(self):
        micropilotes = Micropilotes( D_p =0.15,L_b =9 , HG = 0.5, N_m = 9 ,
                                     proc_iny = "IGU" ,θ = 0, 
                                     D_f =1.4 , D_d =0 , 
                                     S_m =1.5 , H =0.6,
                                     P_anc = 0.1, TP =1 , 
                                     db = 0.019050, f_pc =420000 , f_py = 21000,
                                     perfil=self.perfil_1, 
                                     barra=Barra(nombre = 'uno',D=0.0378,area=0.00075,f_y=530000, precio =20000),
                                     ####VALORES FIJOS###
                                     A_camisa=0,η=1,γ_c=24 ,
                                     α=0, ω=0, f_carga_mp=1
                                    )
        prueba, memoria = micropilotes.calculo_tension_suelos_granulares()
        print (memoria)
        self.assertAlmostEqual(prueba, 5441.978, places=3)  

    def test_calculo_tension_suelos_granulares_4(self):
        micropilotes = Micropilotes( D_p =0.15,L_b =9 , HG = 0.5, N_m = 12 ,
                                     proc_iny = "IGU" ,θ = 0, 
                                     D_f =1.4 , D_d =0 , 
                                     S_m =1.5 , H =0.6,
                                     P_anc = 0.1, TP =1 , 
                                     db = 0.019050, f_pc =420000 , f_py = 21000,
                                     perfil=self.perfil_1, 
                                     barra=Barra(nombre = 'uno',D=0.0378,area=0.00075,f_y=530000, precio =20000),
                                     ####VALORES FIJOS###
                                     A_camisa=0,η=1,γ_c=24 ,
                                     α=0, ω=0, f_carga_mp=1
                                    )
        prueba, memoria = micropilotes.calculo_tension_suelos_granulares()
        print (memoria)
        self.assertAlmostEqual(prueba, 7710.914, places=3) 

    def test_calculo_tension_suelos_cohesivos_2(self):
        micropilotes = Micropilotes( D_p =0.2,L_b =8 , HG =0.5,N_m =12 ,
                                     proc_iny = "IGU" ,θ = 0, 
                                     D_f =1.4 , D_d =0 , 
                                     S_m =1.5 , H =0.6,
                                     P_anc = 0.1, TP =1 , 
                                     db = 0.019050, f_pc =420000 , f_py = 21000,
                                     perfil=self.perfil_1, 
                                     barra=Barra(nombre = 'uno',D=0.0378,area=0.00075,f_y=530000, precio =20000),
                                     ####VALORES FIJOS###
                                     A_camisa=0,η=1,γ_c=24 ,
                                     α=0, ω=0, f_carga_mp=1
                                    )
        prueba, memoria = micropilotes.calculo_tension_suelos_cohesivos()
        print (memoria)
        self.assertAlmostEqual(prueba, 14818.357, places=3)   

    def test_calculo_tension_roca_1(self):
        micropilotes = Micropilotes( D_p =0.2,L_b =6 , HG = 0.5, N_m =12 ,
                                     proc_iny = "IGU" ,θ = 0, 
                                     D_f =1.4 , D_d =0 , 
                                     S_m =1.5 , H =0.6,
                                     P_anc = 0.1, TP =1 , 
                                     db = 0.019050, f_pc =420000 , f_py = 21000,
                                     perfil=self.perfil_1, 
                                     barra=Barra(nombre = 'uno',D=0.0378,area=0.00075,f_y=530000, precio =20000),
                                     ####VALORES FIJOS###
                                     A_camisa=0,η=1,γ_c=24 ,
                                     α=0, ω=0, f_carga_mp=1
                                    )
        prueba, memoria= micropilotes.calculo_tension_roca()
        print (memoria)
        self.assertAlmostEqual(prueba,480.296,places=3)

    def test_calculo_tension_roca_2(self):
        perfil_5 = Perfil([
            Estrato(H_0 = 0.8, γ_s = 16.5, N=18,    E_s =  7600, c_u =  60,    φ_s = 21, saturado = True, tipo_mat = "c", c_p = 0,σ_pp=16,C_c=0.12,C_s=0.003,e_0=1.2),
            Estrato(H_0 = 0.9, γ_s = 21.0, N=None ,  E_s = 50000, c_u =  None, φ_s = 23, saturado = True, tipo_mat = "r", c_p = 0, ucs=6000),
            Estrato(H_0 = 1.5, γ_s = 20.0, N=None,  E_s = 36800, c_u =  None,  φ_s = 24, saturado = True, tipo_mat = "r", c_p = 0,ucs=3250),
            Estrato(H_0 = 3.5, γ_s = 21.0, N=None,  E_s = 75800, c_u =  None,  φ_s = 26, saturado = True, tipo_mat = "r", c_p = 0, ucs=9500),
            Estrato(H_0 = 1.2, γ_s = 22.0, N=None,  E_s = 90000, c_u =  None,  φ_s = 25, saturado = True, tipo_mat = "r", c_p = 0,ucs=14000),
        ])       
        micropilotes = Micropilotes( D_p =0.2,L_b =6 , HG = 0.5, N_m =12 ,
                                     proc_iny = "IGU" ,θ = 0, 
                                     D_f =1.4 , D_d =0 , 
                                     S_m =1.5 , H =0.6,
                                     P_anc = 0.1, TP =1 , 
                                     db = 0.019050, f_pc =420000 , f_py = 21000,
                                     perfil=perfil_5, 
                                     barra=Barra(nombre = 'uno',D=0.0378,area=0.00075,f_y=530000, precio =20000),
                                     ####VALORES FIJOS###
                                     A_camisa=0,η=1,γ_c=24 ,
                                     α=0, ω=0, f_carga_mp=1
                                    )
        prueba, memoria= micropilotes.calculo_tension_roca()
        print (memoria)
        self.assertAlmostEqual(prueba,803773.781,places=3)

    def test_calculo_integral_presion_lateral_activa_desde_0_prueba_1(self):
        micropilotes = Micropilotes( D_p =0.2,L_b =6 , HG = 0.5, N_m =12 ,
                                     proc_iny = "IGU" ,θ = 0, 
                                     D_f =1.4 , D_d =0 , 
                                     S_m =1.5 , H =0.6,
                                     P_anc = 0.1, TP =1 , 
                                     db = 0.019050, f_pc =420000 , f_py = 21000,
                                     perfil=self.perfil_1, 
                                     barra=Barra(nombre = 'uno',D=0.0378,area=0.00075,f_y=530000, precio =20000),
                                     ####VALORES FIJOS###
                                     A_camisa=0,η=1,γ_c=24 ,
                                     α=0, ω=0, f_carga_mp=1
                                    )
        prof = 1.5
        prueba = micropilotes.calculo_integral_presion_lateral_activa_desde_0(prof)
        self.assertAlmostEqual(prueba, 0.00,places=3)

    def test_calculo_integral_presion_lateral_activa_desde_0_prueba_2(self):
        micropilotes = Micropilotes( D_p =0.2,L_b =6 , HG = 0.5, N_m =12 ,
                                     proc_iny = "IGU" ,θ = 0, 
                                     D_f =1.4 , D_d =0 , 
                                     S_m =1.5 , H =0.6,
                                     P_anc = 0.1, TP =1 , 
                                     db = 0.019050, f_pc =420000 , f_py = 21000,
                                     perfil=self.perfil_1, 
                                     barra=Barra(nombre = 'uno',D=0.0378,area=0.00075,f_y=530000, precio =20000),
                                     ####VALORES FIJOS###
                                     A_camisa=0,η=1,γ_c=24 ,
                                     α=0, ω=0, f_carga_mp=1
                                    )
        prof = 7
        prueba = micropilotes.calculo_integral_presion_lateral_activa_desde_0(prof)
        self.assertAlmostEqual(prueba, 23.488 ,places=3)

    def test_calculo_integral_presion_lateral_activa_desde_0_prueba_3(self):
        micropilotes = Micropilotes( D_p =0.115,L_b =6 , HG = 0.5, N_m =12 ,
                                     proc_iny = "IGU" ,θ = 0, 
                                     D_f =1.9 , D_d =0 , 
                                     S_m =1.5 , H =0.6,
                                     P_anc = 0.1, TP =1 , 
                                     db = 0.019050, f_pc =420000 , f_py = 21000,
                                     perfil=self.perfil_2, 
                                     barra=Barra(nombre = 'uno',D=0.0378,area=0.00075,f_y=530000, precio =20000),
                                     ####VALORES FIJOS###
                                     A_camisa=0,η=1,γ_c=24 ,
                                     α=0, ω=0, f_carga_mp=1
                                    )
        prof = 8
        prueba = micropilotes.calculo_integral_presion_lateral_activa_desde_0(prof)
        self.assertAlmostEqual(prueba, 35.7896,places=4)
        
    def test_calculo_integral_presion_lateral_activa_desde_0_prueba_4(self):
        micropilotes = Micropilotes( D_p =0.2,L_b =6 , HG = 0.5, N_m =12 ,
                                     proc_iny = "IGU" ,θ = 0, 
                                     D_f =1.4 , D_d =0 ,
                                     S_m =1.5 , H =0.6,
                                     P_anc = 0.1, TP =1 , 
                                     db = 0.019050, f_pc =420000 , f_py = 21000,
                                     perfil=self.perfil_2, 
                                     barra=Barra(nombre = 'uno',D=0.0378,area=0.00075,f_y=530000, precio =20000),
                                     ####VALORES FIJOS###
                                     A_camisa=0,η=1,γ_c=24 ,
                                     α=0, ω=0, f_carga_mp=1
                                    )
        prof = 9
        prueba = micropilotes.calculo_integral_presion_lateral_activa_desde_0(prof)
        self.assertAlmostEqual(prueba, 40.238,places=3)

    def test_calculo_integral_presion_lateral_pasiva_desde_0_prueba_1(self):
        micropilotes = Micropilotes( D_p =0.2,L_b =6 , HG = 0.5, N_m =12 ,
                                     proc_iny = "IGU" ,θ = 0, 
                                     D_f =1.4 , D_d =0 , 
                                     S_m =1.5 , H =0.6,
                                     P_anc = 0.1, TP =1 , 
                                     db = 0.019050, f_pc =420000 , f_py = 21000,
                                     perfil=self.perfil_1, 
                                     barra=Barra(nombre = 'uno',D=0.0378,area=0.00075,f_y=530000, precio =20000),
                                     ####VALORES FIJOS###
                                     A_camisa=0,η=1,γ_c=24 ,
                                     α=0, ω=0, f_carga_mp=1
                                    )
        prof = 9.6
        prueba = micropilotes.calculo_integral_presion_lateral_pasiva_desde_0(prof)
        self.assertAlmostEqual(prueba, 2110.5370,places=4)

    def test_calculo_integral_presion_lateral_pasiva_desde_0_prueba_2(self):
        micropilotes = Micropilotes( D_p =0.2,L_b =6 , HG = 0.5, N_m =12 ,
                                     proc_iny = "IGU" ,θ = 0, 
                                     D_f =1.4 , D_d =0 , 
                                     S_m =1.5 , H =0.6,
                                     P_anc = 0.1, TP =1 , 
                                     db = 0.019050, f_pc =420000 , f_py = 21000,
                                     perfil=self.perfil_1, 
                                     barra=Barra(nombre = 'uno',D=0.0378,area=0.00075,f_y=530000, precio =20000),
                                     ####VALORES FIJOS###
                                     A_camisa=0,η=1,γ_c=24 ,
                                     α=0, ω=0, f_carga_mp=1
                                    )
        prof = 1.5
        prueba = micropilotes.calculo_integral_presion_lateral_pasiva_desde_0(prof)
        self.assertAlmostEqual(prueba, 118.27,places=2)

    def test_calculo_integral_presion_lateral_pasiva_desde_0_prueba_3(self):
        micropilotes = Micropilotes( D_p =0.2,L_b =6 , HG = 0.5, N_m =12 ,
                                     proc_iny = "IGU" ,θ = 0, 
                                     D_f =1.4 , D_d =0 , 
                                     S_m =1.5 , H =0.6,
                                     P_anc = 0.1, TP =1 , 
                                     db = 0.019050, f_pc =420000 , f_py = 21000,
                                     perfil=self.perfil_1, 
                                     barra=Barra(nombre = 'uno',D=0.0378,area=0.00075,f_y=530000, precio =20000),
                                     ####VALORES FIJOS###
                                     A_camisa=0,η=1,γ_c=24 ,
                                     α=0, ω=0, f_carga_mp=1
                                    )
        prof = 10.6
        prueba = micropilotes.calculo_integral_presion_lateral_pasiva_desde_0(prof)
        self.assertAlmostEqual(prueba, 2532.557,places=4)

    def test_calculo_integral_presion_lateral_pasiva_desde_0_prueba_4(self):
        micropilotes = Micropilotes( D_p =0.2,L_b =6 , HG = 0.5, N_m =12 ,
                                     proc_iny = "IGU" ,θ = 0, 
                                     D_f =1.4 , D_d =0 , 
                                     S_m =1.5 , H =0.6,
                                     P_anc = 0.1, TP =1 , 
                                     db = 0.019050, f_pc =420000 , f_py = 21000,
                                     perfil=self.perfil_1, 
                                     barra=Barra(nombre = 'uno',D=0.0378,area=0.00075,f_y=530000, precio =20000),
                                     ####VALORES FIJOS###
                                     A_camisa=0,η=1,γ_c=24 ,
                                     α=0, ω=0, f_carga_mp=1
                                    )
        prof = 5
        prueba = micropilotes.calculo_integral_presion_lateral_pasiva_desde_0(prof)
        self.assertAlmostEqual(prueba, 553.565,places=4)

    def test_peso_dado_1(self):
        micropilotes = Micropilotes( D_p =0.13,L_b =9 , HG = 0.5, N_m =9 ,
                                     proc_iny = "IGU" ,θ = 0, 
                                     D_f =1.3 , D_d =0 , 
                                     S_m =1.2 , H =0.5,
                                     P_anc = 0.1, TP =1 , 
                                     db = 0.019050, f_pc =420000 , f_py = 21000,
                                     perfil=self.perfil_1, 
                                     barra=Barra(nombre = 'uno',D=0.0378,area=0.00075,f_y=530000, precio =20000),
                                     ####VALORES FIJOS###
                                     A_camisa=0,η=1,γ_c=24 ,
                                     α=0, ω=0, f_carga_mp=1
                                    )
        prueba = micropilotes.peso_dado()
        self.assertAlmostEqual(prueba, 154.08,places=3)

    def test_peso_dado_2(self):
        micropilotes = Micropilotes( D_p =0.2,L_b =6 , HG = 0.5, N_m =12 ,
                                     proc_iny = "IRS" ,θ = 0, 
                                     D_f =1.8 , D_d = 0.4, 
                                     S_m =1.5 , H =0.8,
                                     P_anc = 0.1, TP =0.8 , 
                                     db = 0.019050, f_pc =420000 , f_py = 21000,
                                     perfil=self.perfil_2, 
                                     barra=Barra(nombre = 'uno',D=0.0378,area=0.00075,f_y=530000, precio =20000),
                                     ####VALORES FIJOS###
                                     A_camisa=0,η=1,γ_c=24 ,
                                     α=0, ω=0, f_carga_mp=1
                                    )
        prueba = micropilotes.peso_dado()
        self.assertAlmostEqual(prueba, 711.936 ,places=3)

    def test_peso_micropilotes_1(self):
        micropilotes = Micropilotes( D_p =0.2,L_b =6 , HG = 0.5, N_m =12 ,
                                     proc_iny = "IRS" ,θ = 0, 
                                     D_f =1.8 , D_d =0 , 
                                     S_m =1.5 , H =0.8,
                                     P_anc = 0.1, TP =0.8 , 
                                     db = 0.019050, f_pc =420000 , f_py = 21000,
                                     perfil=self.perfil_2, 
                                     barra=Barra(nombre = 'uno',D=0.0378,area=0.00075,f_y=530000, precio =20000),
                                     ####VALORES FIJOS###
                                     A_camisa=0,η=1,γ_c=24 ,
                                     α=0, ω=0, f_carga_mp=1
                                    )
        prueba = micropilotes.peso_micropilotes()
        self.assertAlmostEqual(prueba, 122.145,places=3)

    def test_volumen_relleno_1(self):
        micropilotes = Micropilotes( D_p =0.2,L_b =6 , HG = 0.5, N_m =12 ,
                                     proc_iny = "IGU" ,θ = 0, 
                                     D_f =1.4 , D_d =0 ,
                                     S_m =1.5 , H =0.6,
                                     P_anc = 0.1, TP =1 , 
                                     db = 0.019050, f_pc =420000 , f_py = 21000,
                                     perfil=self.perfil_1, 
                                     barra=Barra(nombre = 'uno',D=0.0378,area=0.00075,f_y=530000, precio =20000),
                                     ####VALORES FIJOS###
                                     A_camisa=0,η=1,γ_c=24 ,
                                     α=0, ω=0, f_carga_mp=1
                                    )
        prueba = micropilotes.volumen_relleno()
        self.assertAlmostEqual(prueba, 20.5005,places=4)

    def test_calculo_resistencia_por_fuste_micropilote_roca_1(self):
        micropilotes = Micropilotes( D_p =0.2,L_b =6 , HG = 0.5, N_m =12 ,
                                     proc_iny = "IGU" ,θ = 10, 
                                     D_f =1.4 , D_d =0 , 
                                     S_m =1.5 , H =0.6,
                                     P_anc = 0.1, TP =1 , 
                                     db = 0.019050, f_pc =420000 , f_py = 21000,
                                     perfil=self.perfil_1, 
                                     barra=Barra(nombre = 'uno',D=0.0378,area=0.00075,f_y=530000, precio =20000),
                                     ####VALORES FIJOS###
                                     A_camisa=0,η=1,γ_c=24 ,
                                     α=0, ω=0, f_carga_mp=1
                                    )
        prueba,memoria = micropilotes.calculo_resistencia_por_fuste_micropilote_roca()
        print(memoria)
        self.assertAlmostEquals(prueba, 0,places=3)

    def test_calculo_resistencia_por_fuste_micropilote_roca_2(self):
        perfil_5 = Perfil([
            Estrato(H_0 = 0.8, γ_s = 16.5, N=18,    E_s =  7600, c_u =  60,    φ_s = 10, saturado = True, tipo_mat = "c", c_p = 0,σ_pp=16,C_c=0.12,C_s=0.003,e_0=1.2),
            Estrato(H_0 = 0.9, γ_s = 21.0, N=None ,  E_s = 50000, c_u =  None, φ_s = 10, saturado = True, tipo_mat = "r", c_p = 0, ucs=6000),
            Estrato(H_0 = 1.5, γ_s = 20.0, N=None,  E_s = 36800, c_u =  None,  φ_s = 10, saturado = True, tipo_mat = "r", c_p = 0,ucs=3250),
            Estrato(H_0 = 3.5, γ_s = 21.0, N=None,  E_s = 75800, c_u =  None,  φ_s = 10, saturado = True, tipo_mat = "r", c_p = 0, ucs=9500),
            Estrato(H_0 = 1.2, γ_s = 22.0, N=None,  E_s = 90000, c_u =  None,  φ_s = 10, saturado = True, tipo_mat = "r", c_p = 0,ucs=14000),
        ]) 
        micropilotes = Micropilotes( D_p =0.2,L_b =8 , HG = 0.5, N_m =12 ,
                                     proc_iny = "IRS" ,θ = 0, 
                                     D_f =1.4 , D_d =0 , 
                                     S_m =1.5 , H =0.6,
                                     P_anc = 0.3, TP =1 , 
                                     db = 0.019050, f_pc =420000 , f_py = 21000,
                                     perfil=perfil_5, 
                                     barra=Barra(nombre = 'uno',D=0.0378,area=0.00075,f_y=530000, precio =20000),
                                     ####VALORES FIJOS###
                                     A_camisa=0,η=1,γ_c=24 ,
                                     α=0, ω=0, f_carga_mp=1
                                    )
        prueba,memoria = micropilotes.calculo_resistencia_por_fuste_micropilote_roca()
        print(memoria)
        self.assertAlmostEquals(prueba, 89252.613,places=3)

    def test_calculo_resistencia_por_fuste_micropilote_roca_3(self):
        perfil_5 = Perfil([
            Estrato(H_0 = 0.8, γ_s = 16.5, N=18,     E_s =  7600, c_u =  60,    φ_s = 20, saturado = False, tipo_mat = "c", c_p = 0,σ_pp=16,C_c=0.12,C_s=0.003,e_0=1.2),
            Estrato(H_0 = 0.9, γ_s = 21.0, N=None ,  E_s = 50000, c_u =  None,  φ_s = 23, saturado = True, tipo_mat = "r", c_p = 0, ucs=6000),
            Estrato(H_0 = 1.5, γ_s = 20.0, N=None,   E_s = 36800, c_u =  None,  φ_s = 36, saturado = False, tipo_mat = "r", c_p = 0,ucs=3250),
            Estrato(H_0 = 3.5, γ_s = 21.0, N=None,   E_s = 75800, c_u =  None,  φ_s = 18, saturado = True, tipo_mat = "r", c_p = 0, ucs=9500),
            Estrato(H_0 = 1.2, γ_s = 22.0, N=None,   E_s = 90000, c_u =  None,  φ_s = 19, saturado = False, tipo_mat = "r", c_p = 0,ucs=14000),
        ]) 
        micropilotes = Micropilotes( D_p = 0.115, L_b = 10 , HG = 0.5, N_m =4 ,
                                     proc_iny = "IGU" ,θ = 0, 
                                     D_f =1.4 , D_d =0 , 
                                     S_m =1.5 , H =0.6,
                                     P_anc = 0.1, TP =1 , 
                                     db = 0.019050, f_pc =420000 , f_py = 21000,
                                     perfil=perfil_5, 
                                     barra=Barra(nombre = 'uno',D=0.0378,area=0.00075,f_y=530000, precio =20000),
                                     ####VALORES FIJOS###
                                     A_camisa=0,η=1,γ_c=24 ,
                                     α=0, ω=0, f_carga_mp=1
                                    )
        prueba,memoria = micropilotes.calculo_resistencia_por_fuste_micropilote_roca()
        print(memoria)
        self.assertAlmostEquals(prueba, 42766.877,places=3)
   
    def test_calculo_tension_suelos_mixtos_1(self):
        micropilotes = Micropilotes( D_p =0.2,L_b =6 , HG = 0.5, N_m =12 ,
                                     proc_iny = "IGU" ,θ = 0, 
                                     D_f =1.4 , D_d =0 , 
                                     S_m =1.5 , H =0.6,
                                     P_anc = 0.1, TP =1 , 
                                     db = 0.019050, f_pc =420000 , f_py = 21000,
                                     perfil=self.perfil_1, 
                                     barra=Barra(nombre = 'uno',D=0.0378,area=0.00075,f_y=530000, precio =20000),
                                     ####VALORES FIJOS###
                                     A_camisa=0,η=1,γ_c=24 ,
                                     α=0, ω=0, f_carga_mp=1
                                    )
        prueba,memoria = micropilotes.calculo_tension_suelos_mixtos()
        print(memoria)
        self.assertAlmostEquals(prueba, 9378.778,places=3)

    def test_calculo_tension_suelos_mixtos_2(self):
        micropilotes = Micropilotes( D_p =0.2,L_b =6 , HG = 0.5,  N_m =12 ,
                                     proc_iny = "IGU" ,θ = 0, 
                                     D_f =1.4 , D_d =0 , 
                                     S_m =1.5 , H =0.6,
                                     P_anc = 0.1, TP =1 , 
                                     db = 0.019050, f_pc =420000 , f_py = 21000,
                                     perfil=self.perfil_3, 
                                     barra=Barra(nombre = 'uno',D=0.0378,area=0.00075,f_y=530000, precio =20000),
                                     ####VALORES FIJOS###
                                     A_camisa=0,η=1,γ_c=24 ,
                                     α=0, ω=0, f_carga_mp=1
                                    )
        prueba,memoria = micropilotes.calculo_tension_suelos_mixtos()
        print(memoria)
        self.assertAlmostEquals(prueba, 3630.875, places=3)

    def test_calculo_asentamiento_1(self):
        micropilotes = Micropilotes( D_p =0.13,L_b =9 ,HG = 0.5, N_m =9 ,
                                     proc_iny = "IGU" ,θ = 0, 
                                     D_f =1.3 , D_d =0 , 
                                     S_m =1.2 , H =0.5,
                                     P_anc = 0.1, TP =1 , 
                                     db = 0.019050, f_pc =420000 , f_py = 21000,
                                     perfil=self.perfil_1, 
                                     barra=Barra(nombre = 'uno',D=0.0378,area=0.00075,f_y=530000, precio =20000),
                                     ####VALORES FIJOS###
                                     A_camisa=0,η=1,γ_c=24 ,
                                     α=0, ω=0, f_carga_mp=1
                                    )
        k = 10
        F_zc = 1500
        F_zc_eds = 200
        t = 50
        
        prueba, _, memoria, _ = micropilotes.calculo_asentamiento(k, F_zc, F_zc_eds, t)
        print (memoria)
        self.assertAlmostEqual(prueba, 0.01821, places=4) 
    
    def test_calculo_asentamiento_2(self):
        micropilotes = Micropilotes( D_p =0.13,L_b =9 , HG = 0.5, N_m =9 ,
                                     proc_iny = "IGU" ,θ = 0, 
                                     D_f =1.3 , D_d =0 ,
                                     S_m =1.2 , H =0.5,
                                     P_anc = 0.1, TP =1 , 
                                     db = 0.019050, f_pc =420000 , f_py = 21000,
                                     perfil=self.perfil_1Sat, 
                                     barra=Barra(nombre = 'uno',D=0.0378,area=0.00075,f_y=530000, precio =20000),
                                     ####VALORES FIJOS###
                                     A_camisa=0,η=1,γ_c=24 ,
                                     α=0, ω=0, f_carga_mp=1
                                    )
        k = 10
        F_zc = 1500
        F_zc_eds = 200
        t = 50
        prueba, _, memoria, _ = micropilotes.calculo_asentamiento(k, F_zc, F_zc_eds, t)
        print (memoria)
        self.assertAlmostEqual(prueba, 0.01776, places=4)   

    def test_calculo_asentamiento_3(self):
        micropilotes = Micropilotes( D_p =0.115,L_b =3.0 , HG = 0.5, N_m =4 ,
                                     proc_iny = "IGU" ,θ = 0, 
                                     D_f =1.2 , D_d =0 , 
                                     S_m =1.5 , H =0.6,
                                     P_anc = 0.1, TP =1 , 
                                     db = 0.019050, f_pc =420000 , f_py = 21000,
                                     perfil=self.perfil_3, 
                                     barra=Barra(nombre = 'uno',D=0.0378,area=0.00075,f_y=530000, precio =20000),
                                     ####VALORES FIJOS###
                                     A_camisa=0,η=1,γ_c=24 ,
                                     α=0, ω=0, f_carga_mp=1
                                    )
        k = 10
        F_zc = 1200
        F_zc_eds = 150
        t = 50
        prueba, _, memoria, _ = micropilotes.calculo_asentamiento(k, F_zc, F_zc_eds, t)
        print (memoria)
        self.assertAlmostEqual(prueba, 0.0313, places=4) 

    def test_calculo_asentamiento_4(self):
        micropilotes = Micropilotes( D_p =0.2,L_b =6 , HG = 0.5, N_m =12 ,
                                     proc_iny = "IGU" ,θ = 0, 
                                     D_f =1.4 , D_d =0 , 
                                     S_m =1.5 , H =0.6,
                                     P_anc = 0.1, TP =1 ,
                                     db = 0.019050, f_pc =420000 , f_py = 21000,
                                     perfil=self.perfil_1, 
                                     barra=Barra(nombre = 'uno',D=0.0378,area=0.00075,f_y=530000, precio =20000),
                                     ####VALORES FIJOS###
                                     A_camisa=0,η=1,γ_c=24 ,
                                     α=0, ω=0, f_carga_mp=1
                                    )
        k = 10
        F_zc = 1500
        F_zc_eds = 150
        t = 50
        prueba, _, memoria, _ = micropilotes.calculo_asentamiento(k, F_zc, F_zc_eds, t)
        print (memoria)
        self.assertAlmostEqual(prueba, 0.0194, places=4) 

    def test_calculo_asentamiento_5(self):
        micropilotes = Micropilotes( D_p =0.2,L_b =6 , HG = 0.5, N_m =12 ,
                                     proc_iny = "IGU" ,θ = 0, 
                                     D_f =1.4 , D_d =0 , 
                                     S_m =1.5 , H =0.6,
                                     P_anc = 0.1, TP =1 ,
                                     db = 0.019050, f_pc =420000 , f_py = 21000,
                                     perfil=self.perfil_1, 
                                     barra=Barra(nombre = 'uno',D=0.0378,area=0.00075,f_y=530000, precio =20000),
                                     ####VALORES FIJOS###
                                     A_camisa=0,η=1,γ_c=24 ,
                                     α=0, ω=0, f_carga_mp=1
                                    )
        k = 10
        F_zc = 1500
        F_zc_eds = 150
        t = 50
        prueba, _, memoria, _ = micropilotes.calculo_asentamiento(k, F_zc, F_zc_eds, t)
        print (memoria)
        self.assertAlmostEqual(prueba, 0.0194, places=4) 

    def test_calculo_asentamiento_6(self):
        micropilotes = Micropilotes( D_p =0.2,L_b =6 , HG= 0.5, N_m =12 ,
                                     proc_iny = "IGU" ,θ = 0, 
                                     D_f =1.4 , D_d =0 , 
                                     S_m =1.5 , H =0.6,
                                     P_anc = 0.1, TP =1 ,
                                     db = 0.019050, f_pc =420000 , f_py = 21000,
                                     perfil=self.perfil_1, 
                                     barra=Barra(nombre = 'uno',D=0.0378,area=0.00075,f_y=530000, precio =20000),
                                     ####VALORES FIJOS###
                                     A_camisa=0,η=1,γ_c=24 ,
                                     α=0, ω=0, f_carga_mp=1
                                    )
        k = 10
        F_zc = 3600
        F_zc_eds = 300
        t = 50
        prueba, _, memoria, _ = micropilotes.calculo_asentamiento(k, F_zc, F_zc_eds, t)
        print (memoria)
        self.assertAlmostEqual(prueba, 0.0374, places=4) 



if __name__ == '__main__':
    unittest.main()