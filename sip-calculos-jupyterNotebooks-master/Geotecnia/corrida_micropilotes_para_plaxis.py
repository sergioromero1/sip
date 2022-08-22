import json
from cimentaciones.data_services import DataServices
from cimentaciones.perfil import Perfil, Estrato, obtener_perfil
from cimentaciones.cargas import Cargas
from cimentaciones.evaluador_micropilotes import EvaluadorMicropilotes
from cimentaciones.optimizador_micropilotes_para_plaxis import OptimizadorMicropilotesParaPlaxis
from cimentaciones.util import γ_agua, generar_serie
from cimentaciones.parametros_micropilotes import get_parametros_default

def main():
    #conn_string = "host=p1378.concol.com dbname=sip_db user=test_user password=test_user"
    conn_string = "host=localhost dbname=sip_db user=postgres password=Magnus64"
    linea = input("Línea:")
    proc_iny = input("Proceso de inyección:")
    b_max = input("B_max (2.8):") or "2.8"

    usar_tabla_α_exp = False
    α_exp = 1.0

    esquema = linea + "_dlt_gtc"

    # Data services
    data_services = DataServices(conn_string, esquema)

    # Parámetros
    parametros = get_parametros_default()
    parametros['n_soluciones'] = 999999
    parametros["proc_iny"] = proc_iny
    parametros['b_max'] = float(b_max)
    parametros['d_f_max'] = 1.7
    parametros["h_relleno_min"] = 0.3
    parametros["h_max"] = 1.4

    json_parametros = json.dumps(parametros)

    # Info cargas
    info_cargas = Cargas(data_services)

    # Pedestal
    HG = 1.5
    
    # Casos Plaxis
    dict_casos_plaxis = { 
        "cll": [
            # ('Zona 275','A100', 'TCLL275'),
            # ('Zona 278','A100', 'TCLL278'),
            # ('Zona 279','B100', 'TCLL279'),
            # ('Zona 281','A100', 'TCLL281'),
            # ('Zona 324','A100', 'TCLL324'),
            # ('Zona 382','AA100', 'TCLL382'),
            # ('Zona 493','C100', 'TCLL493')
            # ('Zona 369','A100', 'TCLL369')
            # ('Zona 1','A100', 'TCLL266'),
            # ('Zona 1','AA100', 'TCLL266'),
            # ('Zona 1','B100', 'TCLL266'),
            # ('Zona 1','C100', 'TCLL266'),
            # ('Zona 1','D100', 'TCLL266'),
            # ('Zona 2','A100', 'TCLL276'),
            # ('Zona 3','A100', 'TCLL489V'),
            # ('Zona 3','AA100', 'TCLL489V'),
            # ('Zona 3','B100', 'TCLL489V'),
            # ('Zona 4','A100', 'TCLL487V'),
            # ('Zona 4','AA100', 'TCLL487V'),
            # ('Zona 4','B100', 'TCLL487V'),
            # ('Zona 4','C100', 'TCLL487V'),
            # ('Zona 4','D100', 'TCLL487V'),
            # ('Zona 5','A100', 'TCLL303'),
            # ('Zona 6','A100', 'TCLL504'),
            # ('Zona 6','AA100', 'TCLL504'),
            # ('Zona 6','B100', 'TCLL504'),
            # ('Zona 6','C100', 'TCLL504'),
            # ('Zona 7','A100', 'TCLL306'),
            # ('Zona 7','AA100', 'TCLL306'),
            # ('Zona 7','D100', 'TCLL306'),
            # ('Zona 8','A100', 'TCLL254'),
            # ('Zona 8','AA100', 'TCLL254'),
            # ('Zona 8','B100', 'TCLL254'),
            # ('Zona 9','A100', 'TCLL464N'),
            # ('Zona 9','AA100', 'TCLL464N'),
            # ('Zona 9','B100', 'TCLL464N'),
            # ('Zona 9','C100', 'TCLL464N'),
            # ('Zona 9','D100', 'TCLL464N')
            # ('Zona 10','A100', 'TCLL372'),
            # ('Zona 10','AA100', 'TCLL372'),
            # ('Zona 10','B100', 'TCLL372'),
            # ('Zona 11','A100', 'TCLL388'),
            # ('Zona 11','AA100', 'TCLL388'),
            # ('Zona 11','B100', 'TCLL388'),
            # ('Zona 11','C100', 'TCLL388'),
            # ('Zona 11','TR100', 'TCLL388'),
            # ('Zona 12','A100', 'TCLL500N'),
            # ('Zona 12','C100', 'TCLL500N'),
            ('Zona 12','D100', 'TCLL500N')
        ],
        "ln" : [
            # ('Grupo 73','A100', 'TCLL073'),
            # ('Grupo 76','A100', 'TCLL076'),
            # ('Grupo 172','AA100', 'TCLL172N'),
            # ('Grupo 1','A100', 'TCLL225'),
            ('Grupo 1','AA100', 'TCLL225'),
            # ('Grupo 2','A100', 'TCLL159NN'),
            # ('Grupo 2','AA100', 'TCLL159NN'),
            # ('Grupo 2','B100', 'TCLL159NN'),
            # ('Grupo 2','C100', 'TCLL159NN'),
            # ('Grupo 2','D100', 'TCLL159NN'),
            # ('Grupo 2','DT100', 'TCLL159NN'),
            # ('Grupo 3','A100', 'TCLL093')
            # ('Grupo 3','AA100', 'TCLL093'),
            # ('Grupo 3','B100', 'TCLL093'),
            # ('Grupo 3','C100', 'TCLL093'),
            # ('Grupo 3','D100', 'TCLL093'),
            # ('Grupo 3','TR100', 'TCLL093'),
            # ('Grupo 4','A100', 'TCLL024'),
            # ('Grupo 4','AA100', 'TCLL024'),
            # ('Grupo 4','B100', 'TCLL024'),
            # ('Grupo 4','C100', 'TCLL024'),
            # ('Grupo 5','A100', 'TCLL078'),
            # ('Grupo 5','AA100', 'TCLL078'),
            # ('Grupo 6','AA100', 'TCLL111N'),
            # ('Grupo 6','B100', 'TCLL111N'),
            # ('Grupo 6','C100', 'TCLL111N'),
            # ('Grupo 8','A100', 'TCLL144'),
            # ('Grupo 8','AA100', 'TCLL144'),
            # ('Grupo 8','B100', 'TCLL144'),
            # ('Grupo 8','C100', 'TCLL144'),
            # ('Grupo 8','D100', 'TCLL144'),
            ('Grupo 9','A100', 'TCLL148')
            # ('Grupo 9','AA100', 'TCLL148'),
            # ('Grupo 9','B100', 'TCLL148'),
            # ('Grupo 9','C100', 'TCLL148'),
            # ('Grupo 10','A100', 'TCLL205'),
            # ('Grupo 10','AA100', 'TCLL205'),
            # ('Grupo 10','B100', 'TCLL205'),
            # ('Grupo 10','C100', 'TCLL205'),
            # ('Grupo 10','D100', 'TCLL205')
            # ('Grupo 11','A100', 'TCLL188'),
            # ('Grupo 11','AA100', 'TCLL188'),
            # ('Grupo 11','B100', 'TCLL188')
        ],
        "ccla" : [
            # ("Grupo 1", "A126", "TCCLA-36"), # TCCLA
            # ("Grupo 1", "AA126", "TCCLA-36"), # TCCLA
            # ("Grupo 1", "C126", "TCCLA-36"), # TCCLA
            # ("Grupo 3", "A100", "TCCLA-141N"), # TCCLA
            # ("Grupo 3", "AL100", "TCCLA-141N"), # TCCLA
            # ("Grupo 3", "B126", "TCCLA-141N"), # TCCLA
            # ("Grupo 3", "C126", "TCCLA-141N"), # TCCLA
            # ("Grupo 4", "A100", "TCCLA-187"), # TCCLA
            # ("Grupo 4", "AL100", "TCCLA-187"), # TCCLA
            # ("Grupo 4", "B126", "TCCLA-187"), # TCCLA
            ("Grupo 4", "C126", "TCCLA-187"), # TCCLA
            ("Grupo 4", "D126", "TCCLA-187"), # TCCLA
            # ("Grupo 6", "A100", "TCCLA-223N"), # TCCLA
            # ("Grupo 6", "A126", "TCCLA-223N"), # TCCLA
            # ("Grupo 6", "AA126", "TCCLA-223N"), # TCCLA
            # ("Grupo 6", "AL100", "TCCLA-223N"), # TCCLA
            ("Grupo 6", "B126", "TCCLA-223N"), # TCCLA
            ("Grupo 6", "C126", "TCCLA-223N"), # TCCLA
            ("Grupo 6", "D126", "TCCLA-223N"), # TCCLA
            # ("Grupo 9", "A126", "TCCLA-45"), # TCCLA
            # ("Grupo 9", "AA126", "TCCLA-45"), # TCCLA
            # ("Grupo 9", "B126", "TCCLA-45"), # TCCLA
            # ("Grupo 9", "C126", "TCCLA-45"), # TCCLA
            ("Grupo 9", "D126", "TCCLA-45"), # TCCLA
            # ("Grupo 11", "A100", "TCCLA-193"), # TCCLA
            # ("Grupo 11", "AL100", "TCCLA-193"), # TCCLA
            # ("Grupo 11", "B126", "TCCLA-193"), # TCCLA
            ("Grupo 11", "D126", "TCCLA-193") # TCCLA
        ],
        "cclb" : [
            # ("Grupo 2", "A126", "TCCLB-67"), # TCCLB
            # ("Grupo 2", "AA126", "TCCLB-67"), # TCCLB
            # ("Grupo 2", "B126", "TCCLB-67"), # TCCLB
            # ("Grupo 2", "C126", "TCCLB-67"), # TCCLB
            # ("Grupo 5", "A100", "TCCLB-186"), # TCCLB
            # ("Grupo 5", "AL100", "TCCLB-186"), # TCCLB
            # ("Grupo 5", "B126", "TCCLB-186"), # TCCLB
            # ("Grupo 7", "A100", "TCCLB-224N"), # TCCLB
            ("Grupo 7", "B126", "TCCLB-224N"), # TCCLB
            # ("Grupo 8", "A100", "TCCLB-246"), # TCCLB
            # ("Grupo 8", "B126", "TCCLB-246"), # TCCLB
            ("Grupo 8", "D126", "TCCLB-246"), # TCCLB
            # ("Grupo 10", "A100", "TCCLB-72"), # TCCLB
            # ("Grupo 10", "A126", "TCCLB-72"), # TCCLB
            # ("Grupo 10", "AA126", "TCCLB-72"), # TCCLB
            # ("Grupo 10", "AL100", "TCCLB-72"), # TCCLB
            # ("Grupo 10", "B126", "TCCLB-72"), # TCCLB
            # ("Grupo 10", "C126", "TCCLB-72"), # TCCLB
            ("Grupo 10", "D126", "TCCLB-72"), # TCCLB
            # ("Grupo 12", "A100", "TCCLB-209"), # TCCLB
            # ("Grupo 12", "AL100", "TCCLB-209"), # TCCLB
            # ("Grupo 12", "B126", "TCCLB-209"), # TCCLB
            ("Grupo 12", "C126", "TCCLB-209"), # TCCLB
            ("Grupo 12", "D126", "TCCLB-209") # TCCLB
        ]
    }
    # Casos a correr
    lista_torres = data_services.listar_torres_obj()
    casos_plaxis = dict_casos_plaxis[linea]

    info_cargas = Cargas(data_services)

    # Evaluador
    evaluador = EvaluadorMicropilotes()

    # Optimizador
    optimizador = OptimizadorMicropilotesParaPlaxis(evaluador)

    nombre_corrida = "Corrida - para análisis Plaxis - línea {}. proceso de inyección {}. Evaluador: {}. Optimizador: {}, {} soluciones".format(
        esquema,
        parametros["proc_iny"],
        type(evaluador).__name__, 
        type(optimizador).__name__, 
        parametros['n_soluciones'] )
    corrida_id = data_services.guardar_corrida_micropilotes({"nombre": nombre_corrida, "parametros": json_parametros})
    print("Corrida creada. id:{} - {}".format(corrida_id, nombre_corrida), flush=True )

    for caso in casos_plaxis:
        for f_carga_mp in [1.0]: #generar_serie(0.6, 1.0, 0.02, 2):
            zona, tipo, nombre_torre = caso
            torre = [torre for torre in lista_torres if torre.perfil == nombre_torre ][0]
            perfil, error_en_perfil, mensaje_error = obtener_perfil(data_services, vars(torre))
            torre.tipo = tipo
            cargas = info_cargas.obtener_cargas_as_dict(torre)
            resultados = None
            if error_en_perfil:
                print(torre.nombre, "Error en perfil", mensaje_error, flush=True)
            else:
                resultados = optimizador.optimizar(parametros, torre, f_carga_mp, perfil, info_cargas, HG, usar_tabla_α_exp, α_exp, pausar_en_error=False)
                print(caso, f_carga_mp, "OK", flush=True)
            # Guarda corrida - torre
            observaciones = "Corrida para Plaxis. línea: '{}', grupo: '{}', Torre tipo: '{}', Fracción de carga micropilote: {}".format(esquema, zona, tipo, f_carga_mp)
            data_services.guardar_corrida_micropilotes_torre(corrida_id, torre, perfil, cargas, error_en_perfil, mensaje_error, resultados, observaciones)

    # for caso in casos_plaxis:
    #     for f_carga_mp in generar_serie(0.6, 1.0, 0.02, 2):
    #         zona, tipo, perfil = caso
    #         torre = {"nombre" : zona + " " + tipo, "tipo": tipo }
    #         cargas = info_cargas.obtener_cargas_as_dict(torre)
    #         resultados = None
    #         resultados = optimizador.optimizar(parametros, torre, f_carga_mp, perfil, info_cargas, HG)
    #         print(caso, f_carga_mp, "OK", flush=True)
    #         # Guarda corrida - torre
    #         observaciones = "Corrida para Plaxis. Línea: {}, zona: '{}', Torre tipo: '{}', Fracción de carga micropilote: {}".format(esquema, zona, tipo, f_carga_mp)
    #         data_services.guardar_corrida_micropilotes_torre(corrida_id, torre, perfil, cargas, None, None, resultados, observaciones)            

if __name__ == "__main__":
    main()
