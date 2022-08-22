import json
import time
from cimentaciones.data_services import DataServices
from cimentaciones.perfil import Perfil, Estrato, obtener_perfil
from cimentaciones.cargas import Cargas
from cimentaciones.cargas_por_cuerpo import CargasPorCuerpo
from cimentaciones.evaluador_pilastras import EvaluadorPilastras
from cimentaciones.optimizador_pilastras_por_torre import OptimizadorPilastrasPorTorre
from cimentaciones.util import format_duracion
from cimentaciones.pilastra import Pilastra
from cimentaciones.pilastra_geb import PilastraGeb
from cimentaciones.pilastra_das import PilastraDas
from cimentaciones.parametros_pilastra import get_parametros_default

def main():
    start_time = time.time()
    #conn_string = "host=p1378.concol.com dbname=sip_db user=test_user password=test_user"
    conn_string = "host=localhost dbname=sip_db user=postgres password=Magnus64"
    esquema = "cll_dlt_gtc"
    comentario = "Corrida completa"
    torres = []
    procesar_con_gamma_relleno_fijo = True   # <-- gamma relleno
    gamma_relleno = 16.4
    tener_en_cuenta_recomendacion = True
    guardar_corrida = True

    # Parámetros
    parametros = get_parametros_default()
    parametros['h_is'] = [0.3, 0.6, 1.2]
    # parametros['lista_hg'] = [3.0,4.0,5.0,6.0,7.0]
    # parametros['D_p_min'] = 1.2                          # D_p_min {float} -- Valor mínimo para las iteraciones de diametro de la pilastra D_p [m]
    # parametros['D_p_max'] = 2.0                          # D_p_max {float} -- Valor máximo para las iteraciones de diametro de la pilastra D_p [m]
    # parametros['D_p_paso'] = 0.1                         # D_p_paso {float} -- Incremento para las iteraciones de diametro de la pilastra D_p [m]

    # Data services
    data_services = DataServices(conn_string, esquema)

    # Info cargas
    info_cargas = Cargas(data_services)

    # Torres a correr
    lista_torres = data_services.listar_torres_obj()
    if torres and len(torres) > 0:
        if tener_en_cuenta_recomendacion:
            lista_torres = [t for t in lista_torres if t.recom_pilastra and t.tipo != "D3" and t.nombre in torres]
        else:
            lista_torres = [t for t in lista_torres if t.tipo != "D3" and t.nombre in torres]        
    else:
        lista_torres = [t for t in lista_torres if t.recom_pilastra and t.tipo != "D3"]

    # Torres con gamma de relleno fijo
    if procesar_con_gamma_relleno_fijo:
        for torre in lista_torres:
            torre.gamma_r = gamma_relleno        

    # Evaluador
    evaluador = EvaluadorPilastras()

    # Optimizador
    optimizador = OptimizadorPilastrasPorTorre(evaluador)
    parametros['n_soluciones'] = 3000
    pausar_en_error = True

    # Constructor de Pilastra
    constructorPilastra = Pilastra

    # Crea la corrida
    n_soluciones = parametros['n_soluciones']      # Número de soluciones almacenadas
    hg_por_pata = parametros['hg_por_pata']        # Indica si aparte de la lista de hgs a evaluar, se debe incluir el hg de cada pata
    nombre_corrida = "Corrida línea {}, {} torres. Constructor: {}.  Evaluador: {}. Optimizador: {}. Pilastra tipo {}. {} soluciones. {}".format(
        esquema,
        len(lista_torres),
        constructorPilastra.__name__,
        type(evaluador).__name__, 
        type(optimizador).__name__, 
        constructorPilastra.__name__,
        n_soluciones,
        comentario)
    corrida_id = None
    if guardar_corrida:
        corrida_id = data_services.guardar_corrida_pilastra({"nombre": nombre_corrida}, parametros)
    print("Corrida creada. id:{} - {}".format(corrida_id, nombre_corrida), flush=True )

    for torre in lista_torres:
        print(torre.nombre, flush=True)
        perfil, error_en_perfil, mensaje_error = obtener_perfil(data_services, vars(torre))

        resultados = None
        if error_en_perfil:
            print("Error en perfil", mensaje_error, flush=True)
        else:
            resultados = optimizador.optimizar(parametros, torre, perfil, info_cargas, hg_por_pata, n_soluciones, pausar_en_error, constructorPilastra)

        # Guarda corrida - torre
        cargas = info_cargas.obtener_cargas_as_dict(torre)
        if guardar_corrida:
            data_services.guardar_corrida_pilastra_torre(corrida_id, torre, perfil, cargas, error_en_perfil, mensaje_error, resultados)
        else:
            #print(json.dumps(resultados))
            # input("pausa...")
            pass

    end_time = time.time()
    duracion = end_time - start_time    
    print(format_duracion(duracion))


if __name__ == "__main__":
    main()
    

