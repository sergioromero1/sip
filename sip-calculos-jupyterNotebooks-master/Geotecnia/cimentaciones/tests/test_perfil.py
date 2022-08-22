import unittest
from ..perfil import Perfil, Estrato
from ..util import γ_agua

class TestPerfil(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.perfil_1 = Perfil([
            Estrato(H_0=1.0, γ_s=20.0, E_s=6597, c_u=29.36, φ_s=24, saturado=False, tipo_mat="g"),
            Estrato(H_0=0.5, γ_s=19.0, E_s=6597, c_u=29.36, φ_s=24, saturado=False, tipo_mat="g"),
            Estrato(H_0=1.0, γ_s=21.0, E_s=6597, c_u=29.36, φ_s=24, saturado=True,  tipo_mat="g"),
            Estrato(H_0=2.0, γ_s=19.0, E_s=6597, c_u=29.36, φ_s=24, saturado=True,  tipo_mat="g"),
        ])
        self.perfil_2 = Perfil([
            Estrato(H_0=1.0, γ_s=20.0, E_s=6597, c_u=29.36, φ_s=24, saturado=False, tipo_mat="g"),
            Estrato(H_0=0.5, γ_s=19.0, E_s=6597, c_u=29.36, φ_s=24, saturado=False, tipo_mat="c", σ_pp= 80),
            Estrato(H_0=1.0, γ_s=21.0, E_s=6597, c_u=29.36, φ_s=24, saturado=True,  tipo_mat="g"),
            Estrato(H_0=2.0, γ_s=19.0, E_s=6597, c_u=29.36, φ_s=24, saturado=True,  tipo_mat="c", σ_pp= 80),
        ])
        self.perfil_3 = Perfil([
            Estrato(H_0=1.0, γ_s=20.0, E_s=6597, c_u=29.36, φ_s=24, saturado=False, tipo_mat="g"),
            Estrato(H_0=0.5, γ_s=19.0, E_s=6597, c_u=29.36, φ_s=24, saturado=False, tipo_mat="c", σ_pp= 80),
            Estrato(H_0=1.0, γ_s=21.0, E_s=6597, c_u=29.36, φ_s=24, saturado=False,  tipo_mat="g"),
            Estrato(H_0=2.0, γ_s=19.0, E_s=6597, c_u=29.36, φ_s=24, saturado=False,  tipo_mat="c", σ_pp= 80),
        ])
        self.perfil_4 = Perfil([
            Estrato(H_0=1.0, γ_s=20.0, E_s=6597, c_u=29.36, φ_s=24, saturado=True, tipo_mat="g"),
            Estrato(H_0=0.5, γ_s=19.0, E_s=6597, c_u=29.36, φ_s=24, saturado=True, tipo_mat="c", σ_pp= 80),
            Estrato(H_0=1.0, γ_s=21.0, E_s=6597, c_u=29.36, φ_s=24, saturado=True,  tipo_mat="g"),
            Estrato(H_0=2.0, γ_s=19.0, E_s=6597, c_u=29.36, φ_s=24, saturado=True,  tipo_mat="c", σ_pp= 80),
        ])

    def test_calcular_promedio_gamma(self):
        D = 1.7
        γ = self.perfil_1.calcular_promedio_γ(D)
        self.assertAlmostEqual(γ, 18.67, places=2)

    def test_calcular_promedio_gamma_exception(self):
        D = 5.0
        self.assertRaises(ValueError, self.perfil_1.calcular_promedio_γ, D)

    def test_calcular_NF(self):
        NF = self.perfil_1.calcular_NF()
        self.assertEqual(NF, 1.5)

    def test_calcular_NF_2(self):
        NF = self.perfil_3.calcular_NF()
        self.assertIsNone(NF)

    def test_calcular_NF_3(self):
        NF = self.perfil_4.calcular_NF()
        self.assertEqual(NF, 0.0)

    def test_calcular_promedio1(self):
        γ_s_prom = self.perfil_1.calcular_promedio(0, 4.5, "γ_s")
        self.assertAlmostEqual(γ_s_prom, 19.67, places=2)

    def test_calcular_promedio2(self):
        γ_s_prom = self.perfil_1.calcular_promedio(0.7, 2.2, "γ_s")
        self.assertAlmostEqual(γ_s_prom, 20.13, places=2)

    def test_calcular_promedio3(self):
        γ_s_prom = self.perfil_1.calcular_promedio(1.5, 5.0, "γ_s")
        self.assertAlmostEqual(γ_s_prom, 19.67, places=2)

    def test_calcular_promedio4(self):
        γ_s_prom = self.perfil_1.calcular_promedio(1.5, 5.0, "φ_s")
        self.assertAlmostEqual(γ_s_prom, 24, places=2)

    def test_calcular_q(self):
        D = 1.5
        q = self.perfil_1.calcular_q(D)
        self.assertAlmostEqual(q, 29.5, places=2)

    def test_calcular_tipo_mat_predominante1(self):
        prof_ini = 0.6
        prof_fin = 1.5
        tipo_mat_pred = self.perfil_2.calcular_tipo_mat_predominante(prof_ini, prof_fin)
        self.assertEqual(tipo_mat_pred, "c")

    def test_calcular_tipo_mat_predominante2(self):
        prof_ini = 2.5
        prof_fin = 2.9
        perfil = Perfil([
            Estrato(H_0 = 2.0, γ_s = 19.07, E_s = 15560, c_u = 139.40, φ_s = 28, saturado = False, tipo_mat = "c", c_p = 24.50, N = 39, ν= 0.31, C_c= 0.108, C_s= 0.012, e_0= 0.50, σ_pp= 180.24, rechazo= False),
            Estrato(H_0 = 0.5, γ_s = 17.49, E_s = 30750, c_u = 158.00, φ_s = 33, saturado = False, tipo_mat = "c", c_p = 39.50, N = 77, ν= 0.30, C_c= 0.082, C_s= 0.002, e_0= 0.60, σ_pp= 158.20, rechazo= False),
            Estrato(H_0 = 0.5, γ_s = 18.14, E_s = 12000, c_u = None,   φ_s = 34, saturado = False, tipo_mat = "g", c_p =  None, N = 23, ν= 0.31, C_c= None , C_s=  None, e_0= 0.54, σ_pp= None, rechazo= False),
            Estrato(H_0 = 3.0, γ_s = 19.57, E_s = 22650, c_u = 125.09, φ_s = 29, saturado = False, tipo_mat = "c", c_p = 28.97, N = 41, ν= 0.30, C_c= 0.116, C_s= 0.015, e_0= 0.50, σ_pp= 191.26, rechazo= True),
            Estrato(H_0 = 3.0, γ_s = 19.89, E_s =  6380, c_u =  48.07, φ_s = 27, saturado = False, tipo_mat = "c", c_p = 32.87, N = 16, ν= 0.33, C_c= 0.110, C_s= 0.013, e_0= 0.56, σ_pp= 186.54, rechazo= False),
            Estrato(H_0 = 1.0, γ_s = 18.97, E_s = 14000, c_u = None,   φ_s = 34, saturado = False, tipo_mat = "g", c_p =  None, N = 39, ν= 0.31, C_c= None , C_s=  None, e_0= 0.62, σ_pp= None, rechazo= True),
        ])
        tipo_mat_pred = perfil.calcular_tipo_mat_predominante(prof_ini, prof_fin)
        self.assertEqual(tipo_mat_pred, "g")

    def test_calcular_tipo_mat_distintos(self):
        prof_ini = 0.0
        prof_fin = 4.5
        tipos_mat = self.perfil_2.calcular_tipo_mat_distintos(prof_ini, prof_fin)
        self.assertEqual(tipos_mat, ["g","c"])

    def test_calcular_porcentaje_tipo_mat1(self):
        prof_ini = 0.0
        prof_fin = 4.5
        proc = self.perfil_2.calcular_porcentaje_tipo_mat(prof_ini, prof_fin)
        self.assertAlmostEqual(proc["c"], 2.5 / 4.5 * 100, places=4)
        self.assertAlmostEqual(proc["g"], 2 / 4.5 * 100, places=4 )
        self.assertAlmostEqual(proc["r"], 0.0, places=4)

    def test_calcular_porcentaje_tipo_mat2(self):
        prof_ini = 0.8
        prof_fin = 4.0
        proc = self.perfil_2.calcular_porcentaje_tipo_mat(prof_ini, prof_fin)
        self.assertAlmostEqual(proc["c"], (0.5 + 1.5) / 3.2 * 100, places=4)
        self.assertAlmostEqual(proc["g"], (0.2 + 1.0) / 3.2 * 100, places=4 )
        self.assertAlmostEqual(proc["r"], 0.0, places=4)

    def test_calcular_porcentaje_tipo_mat3(self):
        prof_ini = 2.7
        prof_fin = 4.0
        proc = self.perfil_2.calcular_porcentaje_tipo_mat(prof_ini, prof_fin)
        self.assertAlmostEqual(proc["c"], 100, places=4)
        self.assertAlmostEqual(proc["g"], 0.0, places=4 )
        self.assertAlmostEqual(proc["r"], 0.0, places=4)
    
    def test_clonar_saturado_1(self):
        perfil_clon = self.perfil_1.clonar_saturado()
        for k in range(len(perfil_clon)):
            self.assertTrue(perfil_clon[k].saturado)
            self.assertEqual(perfil_clon[k].H_0, self.perfil_1[k].H_0)
            self.assertEqual(perfil_clon[k].γ_s, self.perfil_1[k].γ_s)
            self.assertEqual(perfil_clon[k].E_s, self.perfil_1[k].E_s)
            self.assertEqual(perfil_clon[k].c_u, self.perfil_1[k].c_u)
            self.assertEqual(perfil_clon[k].φ_s, self.perfil_1[k].φ_s)
            self.assertEqual(perfil_clon[k].tipo_mat, self.perfil_1[k].tipo_mat)
        γ = self.perfil_1[0].γ_se
        γ_sat = perfil_clon[0].γ_se
        self.assertEqual(γ_sat, γ - γ_agua)

    def test_calcular_modulos_balastro_1(self):
        perfil = Perfil([
            Estrato(H_0 = 2.0, γ_s = 19.07, E_s = 15560, c_u = 139.40, φ_s = 28, saturado = False, tipo_mat = "c", c_p = 24.50, N = 39, ν= 0.31, C_c= 0.108, C_s= 0.012, e_0= 0.50, σ_pp= 180.24, rechazo= False),
            Estrato(H_0 = 0.5, γ_s = 17.49, E_s = 30750, c_u = 158.00, φ_s = 33, saturado = False, tipo_mat = "c", c_p = 39.50, N = 77, ν= 0.30, C_c= 0.082, C_s= 0.002, e_0= 0.60, σ_pp= 158.20, rechazo= False),
            Estrato(H_0 = 0.5, γ_s = 18.14, E_s = 12000, c_u = None,   φ_s = 34, saturado = False, tipo_mat = "g", c_p =  None, N = 23, ν= 0.31, C_c= None , C_s=  None, e_0= 0.54, σ_pp= None, rechazo= False),
            Estrato(H_0 = 3.0, γ_s = 19.57, E_s = 22650, c_u = 125.09, φ_s = 29, saturado = False, tipo_mat = "c", c_p = 28.97, N = 41, ν= 0.30, C_c= 0.116, C_s= 0.015, e_0= 0.50, σ_pp= 191.26, rechazo= True),
            Estrato(H_0 = 3.0, γ_s = 19.89, E_s =  6380, c_u =  48.07, φ_s = 27, saturado = False, tipo_mat = "c", c_p = 32.87, N = 16, ν= 0.33, C_c= 0.110, C_s= 0.013, e_0= 0.56, σ_pp= 186.54, rechazo= False),
            Estrato(H_0 = 1.0, γ_s = 18.97, E_s = 14000, c_u = None,   φ_s = 34, saturado = False, tipo_mat = "g", c_p =  None, N = 39, ν= 0.31, C_c= None , C_s=  None, e_0= 0.62, σ_pp= None, rechazo= True),
        ])
        print(perfil.calcular_modulos_balastro(0.115, 28))
        self.assertTrue(True)



if __name__ == '__main__':
    unittest.main()