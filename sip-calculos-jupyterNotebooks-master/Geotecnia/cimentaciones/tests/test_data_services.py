import unittest
from ..data_services import listar_torres, listar_cargas, listar_estratos, guardar_corrida

class TestDataServices(unittest.TestCase):
    
    def test_listar_torres(self):
        torres: list = listar_torres(1)
        self.assertIsNotNone(torres)
        self.assertEqual(len(torres), 264)

    def test_listar_estratos(self):
        perfil_info = listar_estratos("TCLL323")
        self.assertIsNotNone(perfil_info)

if __name__ == '__main__':
    unittest.main()