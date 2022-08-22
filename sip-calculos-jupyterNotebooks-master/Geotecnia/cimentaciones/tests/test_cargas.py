import unittest
from ..cargas import Cargas
from ..data_services import DataServices

class TestCargas(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        conn_string = "host=p1378.concol.com dbname=sip_db user=test_user password=test_user"
        esquema = "cll_dlt_gtc"
        data_services = DataServices(conn_string, esquema)
        self.info_cargas = Cargas(data_services)
        
    @classmethod
    def tearDownClass(self):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_seleccionar_cargas(self):
        torre = {"tipo" : "A100"}
        tipo_carga = "TRABAJO"
        caso_cargas = "máxima carga a compresión"
        sistema_cargas = "cartesiano"
        componentes = ["compresion"]
        # print(self.cargas.cargas_maxima_compresion_cartesiano)
        F, = self.info_cargas.seleccionar_cargas(torre, tipo_carga, caso_cargas, sistema_cargas, componentes)
        self.assertEqual(F, 632.81)


if __name__ == '__main__':
    unittest.main()