# pylint: disable=W
import unittest
import time
import copy
from ..data_services import DataServices
from ..cargas import Cargas
from ..zapata import Zapata
from ..perfil import Perfil, Estrato
from ..torre import Torre
from ..evaluador_zapatas import EvaluadorZapatas


class TestCalculosZapata(unittest.TestCase): 

    @classmethod
    def setUpClass(self):
        # Data services
        conn_string = "host=localhost dbname=sip_db user=postgres password=Magnus64"
        esquema = "cll_dlt_gtc"
        data_services = DataServices(conn_string, esquema)
        self.info_cargas = Cargas(data_services)        

    def test_evaluar(self):
        B = 3.8
        D = 4.0
        H = 0.4
        C = 4.6
        TP = 0.8
        θ = 6.80729388
        γ_c = 14.19
        α = 0
        ω = 0
        FSC = 3.0
        FST_g = 1.5 
        FST_c = 2.0
        k = 80
        t = 20
        S_max_adm_c = 0.10 
        S_max_adm_g = 0.05
        FSV = 1.5 
        FSL = 1.5 
        perfil = Perfil([
            Estrato( N = 19,ν = 0.3414656791495478,C_c = 0.14628745279040484,C_s = 0.037481217633865895,E_s = 10400.0,H_0 = 1.0,RQD = None,c_p = 34.46845624384901,ucs = None,c_u = 78.575,e_0 = 0.5814859761124849,γ_s = 17.345048769530752,φ_s = 28.781863323725567,σ_pp = 278.15549999999996,rechazo = False,roca_a = None,roca_m = None,roca_s = None,roca_γ = None,saturado = True,tipo_mat =  "c" ,roca_E_rm = None,roca_ν_rm = None,roca_φ_rm = None,origen = "real",descripcion =  "ARCILLA LIMOSA CON ARENA, DE PLASTICIDAD BAJA, HUMEDAD BAJA Y CONSISTENCIA MUY FIRME. DE COLOR CAFÉ CLARO" ,roca_c_p_rm = None,suelo_micropilotes =  "Suelos cohesivos"),
            Estrato(N= 19,ν= 0.3278626173687291,C_c= None,C_s= None,E_s= 27095.800853708795,H_0= 1.0,RQD= None,c_p= None,c_u= None,e_0= None,ucs= None,γ_s= 18.790571041101582,φ_s= 30.809878466781733,σ_pp= None,origen= "real",roca_a= None,roca_m= None,roca_s= None,rechazo= False,roca_γ= None,saturado= True,tipo_mat= "g",roca_E_rm= None,roca_ν_rm= None,roca_φ_rm= None,descripcion= "GRAVA LIMOSA, CON ARENA, DE HUMEDAD BAJA Y DENSIDAD MEDIA. DE COLOR CAFÉ CLARO",roca_c_p_rm= None,suelo_micropilotes= "Gravas"),
            Estrato(N = 43,ν = 0.29225427249536146,C_c = None,C_s = None,E_s = 37826.25401193108,H_0 = 1.95,RQD = None,c_p = None,c_u = None,e_0 = None,ucs = None,γ_s = 19.422970900474283,φ_s = 35.94395751360644,σ_pp = None,origen = "real",roca_a = None,roca_m = None,roca_s = None,rechazo = False,roca_γ = None,saturado = True,tipo_mat = "g",roca_E_rm = None,roca_ν_rm = None,roca_φ_rm = None,descripcion = "ARENA DE GRANO MEDIO A FINO, MAL GRADADA, CON ALGO DE LIMO Y ARCILLA, DE HUMEDAD BAJA, DENSA. DE COLOR CAFÉ CLARO.",roca_c_p_rm = None,suelo_micropilotes = "Arena"),
            Estrato(N = 31,ν = 0.3097195049500138,C_c = 0.12452015245214798,C_s = 0.029374719508274263,E_s = 9920.0,H_0 = 3.55,RQD = None,c_p = 55.59861482658107,c_u = 71.84,e_0 = 0.43291314674508596,ucs = None,γ_s = 19.199080830887315,φ_s = 33.457174722150285,σ_pp = 254.3136,origen = "virtual",roca_a = None,roca_m = None,roca_s = None,rechazo = False,roca_γ = None,saturado = True,tipo_mat = "c",roca_E_rm = None,roca_ν_rm = None,roca_φ_rm = None,descripcion = "LIMO CON ARENA, DE  PLASTICIDAD BAJA, HUMEDAD BAJA Y CONSISTENCIA DURA. DE COLOR CAFÉ OSCURO.",roca_c_p_rm = None,suelo_micropilotes = "Suelos cohesivos"),
            Estrato(N = 64,ν = 0.2993500531478042,C_c = None,C_s = None,E_s = 35637.13322951688,H_0 = 2.5,RQD = None,c_p = None,c_u = None,e_0 = None,ucs = None,γ_s = 18.90487588195132,φ_s = 34.938563002065386,σ_pp = None,origen = "virtual",roca_a = None,roca_m = None,roca_s = None,rechazo = False,roca_γ = None,saturado = True,tipo_mat = "g",roca_E_rm = None,roca_ν_rm = None,roca_φ_rm = None,descripcion = "ARENA LIMOSA CON ALGO DE GRAVAS, DE HUMEDAD BAJA, MUY COMPACTA Y DE COLOR HABANO.",roca_c_p_rm = None,suelo_micropilotes = "Arena")
        ], nivel_freatico_exploracion = 0.0, γ_r=16.4)
        torre = Torre( cota = None,  este = None,  tipo = "B100",  norte = None,  cuerpo = 3.0,  nombre = "TCLL286",  perfil = "TCLL286",  abscisa = 132005.871,  gamma_r = 16.4,  sumergido = True,  f_carga_mp = 0.429,  ped_pata_a = None,  ped_pata_b = None,  ped_pata_c = None,  ped_pata_d = None,  recom_zapata = True,  recom_especial = False,  recom_parrilla = False,  recom_pilastra = False,  zona_geotecnia = "8",  prof_min_desplante = 2.0,  recom_micropilotes = True,  inclinacion_terreno = 0.0,  inclinacion_base_zapata = 0.0)
        evaluador = EvaluadorZapatas()
        zapata = Zapata(B, B, D, H, C, TP, θ, γ_c, perfil, α, ω)
        evaluacion = evaluador.evaluar(zapata, torre, perfil, self.info_cargas, FSC, FST_g, FST_c, k, t, S_max_adm_c, S_max_adm_g, FSV, FSL)
        self.assertAlmostEqual(evaluacion["arrancamiento-tens_max"]["fs"], 1.23, 2)
        self.assertAlmostEqual(evaluacion["cap_port-comp_max"]["q_ult"], 622.11, 2)
        self.assertAlmostEqual(evaluacion["cap_port-comp_max"]["fs_Q_max"], 4.44, 2)
        self.assertAlmostEqual(evaluacion["deslizamiento-long_max"]["Q_L"], 948.62, 2)
        self.assertAlmostEqual(evaluacion["deslizamiento-long_max"]["fs"], 5.77, 2)
        self.assertAlmostEqual(evaluacion["volcamiento-long_max"]["Me"], 1818.32, 2)
        self.assertAlmostEqual(evaluacion["volcamiento-long_max"]["fs"], 1.12, 2)

    def test_avaluar_2(self):
        B = 3.0
        D = 3.5
        H = 0.4
        C = 3.6
        TP = 0.7
        θ = 5.90689248
        γ_c = 24.0
        α = 0
        ω = 0
        FSC = 3.0
        FST_g = 1.5 
        FST_c = 2.0
        k = 80
        t = 20
        S_max_adm_c = 0.10 
        S_max_adm_g = 0.05
        FSV = 1.5 
        FSL = 1.5 
        perfil = Perfil([        
            Estrato(N = 46,ν = 0.3476565505046287,C_c = 0.13071240296495304,C_s = 0.035842646684579385,E_s = 17280.0,H_0 = 1.5,RQD = None,c_p = 28.299352712093555,c_u = 175.11,e_0 = 0.3324403971962595,ucs = None,γ_s = 21.523679333309627,φ_s = 27.843957877381225,σ_pp = 619.8894000000001,origen = "real",roca_a = None,roca_m = None,roca_s = None,rechazo = False,roca_γ = None,saturado = False,tipo_mat = "c",roca_E_rm = None,roca_ν_rm = None,roca_φ_rm = None,descripcion = "ARCILLA ARENOSA DE COLOR MARRÓN, DE PLASTICIDAD BAJA, HUMEDAD BAJA Y  DE CONSISTENCIA MUY FIRME A DURA.",roca_c_p_rm = None,suelo_micropilotes = "Suelos cohesivos"),
            Estrato(N = 59,ν = 0.26898950094193463,C_c = None,C_s = None,E_s = 44850.199836733475,H_0 = 1.85,RQD = None,c_p = None,c_u = None,e_0 = None,ucs = None,γ_s = 19.569899712701826,φ_s = 39.191336055691984,σ_pp = None,origen = "real",roca_a = None,roca_m = None,roca_s = None,rechazo = False,roca_γ = None,saturado = False,tipo_mat = "g",roca_E_rm = None,roca_ν_rm = None,roca_φ_rm = None,descripcion = "ARENA ARCILLO LIMOSA DE GRANO FINO, DE COLOR MARRÓN, CON ALGUNAS GRAVAS, DE HUMEDAD BAJA, DENSA.",roca_c_p_rm = None,suelo_micropilotes = "Arena"),
            Estrato(N = 91,ν = 0.37932123470346246,C_c = 0.21014870976883773,C_s = 0.07499788391308779,E_s = 15360.0,H_0 = 6.65,RQD = None,c_p = 14.980654224565482,c_u = 148.17000000000002,e_0 = 0.5463481219193358,ucs = None,γ_s = 20.023123596237117,φ_s = 22.883622522132484,σ_pp = 524.5218000000001,origen = "virtual",roca_a = None,roca_m = None,roca_s = None,rechazo = False,roca_γ = None,saturado = False,tipo_mat = "c",roca_E_rm = None,roca_ν_rm = None,roca_φ_rm = None,descripcion = "DEPOSITO ALUVIAL CON CANTOS Y GRAVAS HASTA DE 7\" EN MATRIZ ARENO ARCILLOSA, MUY DENSA ALGO LIMOSA DE COLOR HABANO AMARILLENTOS CON VETAS DE OXIDACION Y VETAS BLANCAS.",roca_c_p_rm = None,suelo_micropilotes = "Arena")
        ], nivel_freatico_exploracion = 0.0, γ_r=16.4)
        torre = Torre(cota = None,este = None,tipo = "AA100",norte = None,cuerpo = 7.0,nombre = "TCLL422",perfil = "TCLL422",abscisa = 201954.889,gamma_r = 16.4,sumergido = False,f_carga_mp = None,ped_pata_a = None,ped_pata_b = None,ped_pata_c = None,ped_pata_d = None,recom_zapata = True,recom_especial = False,recom_parrilla = True,recom_pilastra = False,zona_geotecnia = "11",prof_min_desplante = 2.0,recom_micropilotes = False,inclinacion_terreno = 0.0,inclinacion_base_zapata = 0.0)
        evaluador = EvaluadorZapatas()
        zapata = Zapata(B, B, D, H, C, TP, θ, γ_c, perfil, α, ω)
        evaluacion = evaluador.evaluar(zapata, torre, perfil, self.info_cargas, FSC, FST_g, FST_c, k, t, S_max_adm_c, S_max_adm_g, FSV, FSL)
        self.assertAlmostEqual(evaluacion["arrancamiento-tens_max"]["fs"], 3.58, 2)
        self.assertAlmostEqual(evaluacion["cap_port-comp_max"]["q_ult"], 1263.38, 2)
        self.assertAlmostEqual(evaluacion["cap_port-comp_max"]["fs_Q_max"], 6.70, 2)
        self.assertAlmostEqual(evaluacion["deslizamiento-long_max"]["Q_L"], 1507.46, 2)
        self.assertAlmostEqual(evaluacion["deslizamiento-long_max"]["fs"], 17.01, 2)
        self.assertAlmostEqual(evaluacion["volcamiento-long_max"]["Me"], 2726.29, 2)
        self.assertAlmostEqual(evaluacion["volcamiento-long_max"]["fs"], 2.48, 2)
