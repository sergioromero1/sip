import json
from itertools import islice
from cimentaciones.data_services import DataServices
from cimentaciones.perfil import Perfil, Estrato, obtener_perfil
from cimentaciones.cargas import Cargas
from cimentaciones.cargas_por_cuerpo import CargasPorCuerpo
from cimentaciones.evaluador_zapatas import EvaluadorZapatas
from cimentaciones.optimizador_zapatas_por_torre import OptimizadorZapatasPorTorre
from cimentaciones.parametros_zapata import get_parametros_default

def main():
    # Inputs
    conn_string = "host=p1378.concol.com dbname=sip_db user=test_user password=test_user"
    esquema = "cll_dlt_gtc"
    nombre_corrida = "Corrida - Completa - cargas envolventes optimización por torre. Análisis para agrupación de cargas"
    n_soluciones = 1
    hg_por_pata = False

    # Data services
    data_services = DataServices(conn_string, esquema)

    # Parámetros
    parametros = get_parametros_default()
    json_parametros = json.dumps(parametros)

    # Info cargas
    info_cargas = Cargas(data_services)
    #info_cargas = CargasPorCuerpo(data_services)

    # Evaluador
    evaluador = EvaluadorZapatas()

    # Optimizador
    optimizador = OptimizadorZapatasPorTorre(evaluador)

    # Torres a correr
    lista_torres = data_services.listar_torres()
    # perfiles_completos = [
    #     "TCLL250","TCLL251","TCLL252","TCLL253","TCLL254","TCLL255","TCLL256","TCLL257","TCLL258","TCLL259","TCLL260","TCLL261","TCLL262","TCLL263","TCLL264",
    #     "TCLL265","TCLL266","TCLL267","TCLL268","TCLL269","TCLL276","TCLL294","TCLL296","TCLL297","TCLL299","TCLL300","TCLL301","TCLL302","TCLL303","TCLL304",
    #     "TCLL305","TCLL306","TCLL307","TCLL308","TCLL309","TCLL310","TCLL312N","TCLL313","TCLL314","TCLL315","TCLL316","TCLL317","TCLL318","TCLL319","TCLL320",
    #     "TCLL321","TCLL322","TCLL323","TCLL324","TCLL325","TCLL326","TCLL327","TCLL328","TCLL329","TCLL330","TCLL331","TCLL335","TCLL336","TCLL337","TCLL338",
    #     "TCLL345","TCLL348BV","TCLL352","TCLL353","TCLL354","TCLL355","TCLL356","TCLL357","TCLL358","TCLL359","TCLL360","TCLL361","TCLL362","TCLL363","TCLL364",
    #     "TCLL365","TCLL372","TCLL388","TCLL405","TCLL406","TCLL407","TCLL408","TCLL409","TCLL410","TCLL411","TCLL412","TCLL413","TCLL414","TCLL415","TCLL416",
    #     "TCLL417","TCLL418","TCLL419","TCLL420","TCLL421","TCLL422","TCLL423N","TCLL424","TCLL425","TCLL426","TCLL427","TCLL428","TCLL429","TCLL430","TCLL431",
    #     "TCLL432","TCLL433","TCLL434","TCLL435","TCLL436","TCLL437","TCLL438","TCLL439","TCLL440N","TCLL441N","TCLL442N","TCLL443N","TCLL444","TCLL445","TCLL446",
    #     "TCLL447","TCLL448","TCLL449","TCLL450","TCLL451","TCLL452","TCLL464N","TCLL466N","TCLL467","TCLL468","TCLL471","TCLL472N","TCLL473","TCLL474","TCLL475",
    #     "TCLL476","TCLL477","TCLL478N","TCLL479","TCLL480","TCLL481","TCLL482","TCLL483","TCLL484","TCLL485","TCLL486","TCLL487","TCLL488","TCLL489","TCLL490N",
    #     "TCLL491N","TCLL492","TCLL493","TCLL494","TCLL495","TCLL496","TCLL497","TCLL498","TCLL499N","TCLL500N","TCLL501","TCLL502","TCLL503","TCLL504","TCLL505",
    #     "TCLL506","TCLL507","TCLL508","TCLL509","TCLL510","TCLL511"]
    lista_torres = [t for t in lista_torres if t["recom_zapata"] == True]

    # Guarda corrida
    corrida_id = data_services.guardar_corrida_zapata({"nombre": nombre_corrida}, json_parametros)
    print("Corrida creada. id:{} - {}".format(corrida_id, nombre_corrida), flush=True )

    for torre in lista_torres:
        perfil, error_en_perfil, mensaje_error = obtener_perfil(data_services, torre)
        cargas = info_cargas.obtener_cargas_as_dict(torre)

        resultados = None
        if error_en_perfil:
            print(torre["nombre"], "Error en perfil", mensaje_error, flush=True)
        else:
            resultados = optimizador.optimizar(parametros, torre, perfil, info_cargas, hg_por_pata, n_soluciones)
            print(torre["nombre"], "OK", flush=True)

        # Guarda corrida - torre
        data_services.guardar_corrida_zapata_torre(corrida_id, torre, perfil, cargas, error_en_perfil, mensaje_error, resultados)

if __name__ == "__main__":
    main()
    

