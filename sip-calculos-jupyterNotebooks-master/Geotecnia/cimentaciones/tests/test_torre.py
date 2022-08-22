import unittest
from ..torre import Torre
from ..data_services import DataServices

class TestTorre(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        pass

    def test_torre_data_1(self):
        conn_string = "host=localhost dbname=sip_db user=postgres password=Magnus64"
        esquema = "cll_dlt_gtc"
        data_services = DataServices(conn_string, esquema)
        torres = data_services.listar_torres_obj()
        for torre in torres:
            print(torre.nombre, torre.fc)



if __name__ == '__main__':
    unittest.main()