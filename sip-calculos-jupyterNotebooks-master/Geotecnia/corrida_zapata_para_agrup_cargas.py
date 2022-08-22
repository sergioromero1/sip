import json
from itertools import islice
from cimentaciones.data_services import DataServices
from cimentaciones.perfil import Perfil, Estrato, obtener_perfil
from cimentaciones.cargas import Cargas
from cimentaciones.cargas_por_cuerpo import CargasPorCuerpo
from cimentaciones.evaluador_zapatas import EvaluadorZapatas
from cimentaciones.optimizador_zapatas_por_pedestal import OptimizadorZapatasPorPedestal
from cimentaciones.optimizador_zapatas_por_torre import OptimizadorZapatasPorTorre
from cimentaciones.parametros_zapata import get_parametros_default

def main():
    # Inputs
    conn_string = "host=p1378.concol.com dbname=sip_db user=test_user password=test_user"
    esquema = "cll_dlt_gtc"
    nombre_corrida = "Corrida para agrupación de diseños"
    n_soluciones = 10
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
    optimizador = OptimizadorZapatasPorPedestal(evaluador)    

    # Torres a correr
    lista_torres = data_services.listar_torres()
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
    
