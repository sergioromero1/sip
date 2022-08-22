import json
from itertools import islice
from cimentaciones.data_services import DataServices
from cimentaciones.perfil import Perfil, Estrato, obtener_perfil
from cimentaciones.cargas import Cargas
from cimentaciones.cargas_por_cuerpo import CargasPorCuerpo
from cimentaciones.evaluador_zapatas import EvaluadorZapatas
from cimentaciones.optimizador_zapatas_por_pedestal import OptimizadorZapatasPorPedestal
from cimentaciones.parametros_zapata import get_parametros_default

def main():
    # Inputs
    conn_string = "host=p1378.concol.com dbname=sip_db user=test_user password=test_user"
    esquema = "cll_dlt_gtc"
    nombre_corrida = "Corrida - torre A/AA en un mismo perfil"

    # Data services
    data_services = DataServices(conn_string, esquema)

    # Parámetros
    parametros = get_parametros_default()
    json_parametros = json.dumps(parametros)

    # Info cargas
    #info_cargas = Cargas(data_services)
    info_cargas = CargasPorCuerpo(data_services)

    # Evaluador
    evaluador = EvaluadorZapatas()    

    # Optimizador
    optimizador = OptimizadorZapatasPorPedestal(evaluador)    

    # Número de soluciones almacenadas
    n_soluciones = 10        

    # Torres a correr
    lista_torres = data_services.listar_torres()
    torre = [t for t in lista_torres if t["nombre"] == "TCLL256"][0]

    # Guarda corrida
    corrida_id = data_services.guardar_corrida_zapata({"nombre": nombre_corrida}, json_parametros)

    perfil, error_en_perfil, mensaje_error = obtener_perfil(data_services, torre)

    # A100
    torre["nombre"] = "TCLL256 - A100"
    torre["tipo"] = "A100"
    cargas = info_cargas.obtener_cargas_as_dict(torre)
    resultados = None
    # Guarda corrida - torre
    if error_en_perfil:
        print(torre["nombre"], "Error en perfil", mensaje_error, flush=True)
    else:
        resultados = optimizador.optimizar(parametros, torre, perfil, info_cargas, False, n_soluciones)
        print(torre["nombre"], "OK", flush=True)
    # Guarda corrida - torre
    data_services.guardar_corrida_zapata_torre(corrida_id, torre, perfil, cargas, error_en_perfil, mensaje_error, resultados)

    # AA100
    torre["nombre"] = "TCLL256 - AA100"
    torre["tipo"] = "AA100"
    cargas = info_cargas.obtener_cargas_as_dict(torre)
    resultados = None
    # Guarda corrida - torre
    if error_en_perfil:
        print(torre["nombre"], "Error en perfil", mensaje_error, flush=True)
    else:
        resultados = optimizador.optimizar(parametros, torre, perfil, info_cargas, False, n_soluciones)
        print(torre["nombre"], "OK", flush=True)
    # Guarda corrida - torre
    data_services.guardar_corrida_zapata_torre(corrida_id, torre, perfil, cargas, error_en_perfil, mensaje_error, resultados)

if __name__ == "__main__":
    main()
    
