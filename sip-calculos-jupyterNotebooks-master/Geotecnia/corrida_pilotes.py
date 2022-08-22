import json
import time
from cimentaciones.data_services import DataServices
from cimentaciones.perfil import Perfil, Estrato, obtener_perfil
from cimentaciones.cargas import Cargas
from cimentaciones.cargas_por_cuerpo import CargasPorCuerpo
from cimentaciones.evaluador_pilotes import EvaluadorPilotes
from cimentaciones.optimizador_pilotes_por_torre import OptimizadorPilotesPorTorre
from cimentaciones.util import format_duracion
from cimentaciones.pilotes import Pilotes
from cimentaciones.parametros_pilotes import get_parametros_default

def main():
    start_time = time.time()
    #conn_string = "host=p1378.concol.com dbname=sip_db user=test_user password=test_user"
    conn_string = "host=localhost dbname=sip_db user=postgres password=Magnus64"
    esquema = "cll_dlt_gtc"
    comentario = "Torre TCLL274"
    #torres = ["TCLL296V"]
    #torres = ["TCLL274"]
    torres = ["TCLL274"]
    guardar_corrida = True
    tener_en_cuenta_recomendacion = False    

    # Parámetros
    parametros = get_parametros_default()
    parametros['hincado'] = False
    parametros['d_f_max'] = 2.0

    # Data services
    data_services = DataServices(conn_string, esquema)

    # Info cargas
    info_cargas = Cargas(data_services)

    # Torres a correr
    lista_torres = data_services.listar_torres_obj()
    if torres and len(torres) > 0:
        if tener_en_cuenta_recomendacion:
            lista_torres = [t for t in lista_torres if t.recom_especial and t.tipo != "D3" and t.nombre in torres]
        else:
            lista_torres = [t for t in lista_torres if t.tipo != "D3" and t.nombre in torres]        
    else:
        lista_torres = [t for t in lista_torres if t.recom_especial and t.tipo != "D3"]

    # Evaluador
    evaluador = EvaluadorPilotes()

    # Optimizador
    optimizador = OptimizadorPilotesPorTorre(evaluador)
    parametros['n_soluciones'] = 3000
    pausar_en_error = True

    # Crea la corrida
    n_soluciones = parametros['n_soluciones']      # Número de soluciones almacenadas
    nombre_corrida = "Corrida línea {}, {} torres. Evaluador: {}. Optimizador: {}. {} soluciones. {}".format(
        esquema,
        len(lista_torres),
        type(evaluador).__name__, 
        type(optimizador).__name__, 
        n_soluciones,
        comentario)
    corrida_id = None
    if guardar_corrida:
        corrida_id = data_services.guardar_corrida_pilotes({"nombre": nombre_corrida}, parametros)
    print("Corrida creada. id:{} - {}".format(corrida_id, nombre_corrida), flush=True )

    for torre in lista_torres:
        print(torre.nombre, flush=True)
        perfil, error_en_perfil, mensaje_error = obtener_perfil(data_services, vars(torre))

        resultados = None
        if error_en_perfil:
            print("Error en perfil", mensaje_error, flush=True)
        else:
            resultados = optimizador.optimizar(parametros, torre, perfil, info_cargas, pausar_en_error)

        # Guarda corrida - torre
        cargas = info_cargas.obtener_cargas_as_dict(torre)
        if guardar_corrida:
            data_services.guardar_corrida_pilotes_torre(corrida_id, torre, perfil, cargas, error_en_perfil, mensaje_error, resultados)
        else:
            #print(json.dumps(resultados))
            # input("pausa...")
            pass

    end_time = time.time()
    duracion = end_time - start_time    
    print(format_duracion(duracion))


if __name__ == "__main__":
    main()
    

