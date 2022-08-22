import unittest
from ..util import sin_g, cos_g, tan_g, cot_g, π, calcular_C_d, calcular_I_f, generar_serie

class TestUtil(unittest.TestCase):
    def test_sin_g(self):
        self.assertAlmostEqual(sin_g(30), 0.500000, places=6)

    def test_cos_g(self):
        self.assertAlmostEqual(cos_g(30), 0.866025, places=6)

    def test_tan_g(self):
        self.assertAlmostEqual(tan_g(30), 0.577350, places=6)

    def test_cot_g(self):
        self.assertAlmostEqual(cot_g(30), 1.732051, places=6)

    def test_pi(self):
        self.assertAlmostEqual(π, 3.141593, places=6)

    def test_calcular_C_d(self):
        self.assertAlmostEqual(calcular_C_d(2, 1), 0.28, places=2) # Libro Fang (L/B=1, ν = 0.50) 0.29
        self.assertAlmostEqual(calcular_C_d(30, 3), 0.49, places=2)# Libro Fang (L/B=1, ν = 0.50) 0.48

    def test_calcular_I_f1(self):
        self.assertAlmostEqual(calcular_I_f(0.4, 0.42), 0.843, places=3)

    def test_calcular_I_f2(self):
        self.assertAlmostEqual(calcular_I_f(0.5, 0.12), 0.960, places=3)

    def test_calcular_I_f3(self):
        self.assertAlmostEqual(calcular_I_f(0.47, 0.45), 0.8725, places=4)

    def test_generate_series(self):
        self.assertEqual(generar_serie(0.1, 1.5, 0.1, 2), [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5])
        self.assertEqual(generar_serie(0.1, 1.4, 0.2, 2), [0.1, 0.3, 0.5, 0.7, 0.9, 1.1, 1.3])
        self.assertEqual(generar_serie(0.6, 1.0, 0.02, 2), [0.6,0.62,0.64,0.66,0.68,0.7,0.72,0.74,0.76,0.78,0.8,0.82,0.84,0.86,0.88,0.9,0.92,0.94,0.96,0.98,1])

if __name__ == '__main__':
    unittest.main()