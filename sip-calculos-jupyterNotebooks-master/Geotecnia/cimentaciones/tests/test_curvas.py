import unittest
from ..curvas import q_s_suelos_cohesivos, q_s_suelos_granulares

class TestCurvas(unittest.TestCase):

    def test_q_s_suelos_cohesivos_1(self):
        q_s = q_s_suelos_cohesivos("IGU", 443)
        self.assertEqual(q_s, 200)
        q_s = q_s_suelos_cohesivos("IGU", 100)
        self.assertEqual(q_s, 72)
        q_s = q_s_suelos_cohesivos("IGU", 54)
        self.assertEqual(q_s, 47)
        q_s = q_s_suelos_cohesivos("IGU", 20)
        self.assertAlmostEqual(q_s, 28.52173913, 5)
        q_s = q_s_suelos_cohesivos("IGU", 800)
        self.assertEqual(q_s, 200)

        q_s = q_s_suelos_cohesivos("IRS", 100)
        self.assertEqual(q_s, 200)
        q_s = q_s_suelos_cohesivos("IRS", 44.5)
        self.assertEqual(q_s, 116)
        q_s = q_s_suelos_cohesivos("IRS", 800)
        self.assertEqual(q_s, 400)
        q_s = q_s_suelos_cohesivos("IRS", 365)
        self.assertEqual(q_s, 400)


    def test_q_s_suelos_granulares_1(self):
        q_s = q_s_suelos_granulares("IGU", 67.6)
        self.assertEqual(q_s, 400)
        q_s = q_s_suelos_granulares("IGU", 9)
        self.assertEqual(q_s, 40)
        q_s = q_s_suelos_granulares("IGU", 200)
        self.assertEqual(q_s, 400)

        q_s = q_s_suelos_granulares("IRS", 55)
        self.assertEqual(q_s, 631)
        q_s = q_s_suelos_granulares("IRS", 200)
        self.assertEqual(q_s, 631)
        q_s = q_s_suelos_granulares("IRS", 9)
        self.assertEqual(q_s, 135.5)
