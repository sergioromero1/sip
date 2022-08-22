import json
import time
from cimentaciones.data_services import DataServices
from cimentaciones.perfil import Perfil, Estrato, obtener_perfil
from cimentaciones.cargas import Cargas
from cimentaciones.evaluador_micropilotes import EvaluadorMicropilotes
from cimentaciones.encontrar_suelo_micropilotes import EncontrarSuelo
from cimentaciones.util import generar_serie, format_duracion
from cimentaciones.parametros_micropilotes import get_parametros_default


def main():
    start_time = time.time()
    #conn_string = "host=p1378.concol.com dbname=sip_db user=test_user password=test_user"
    conn_string = "host=localhost dbname=sip_db user=postgres password=Magnus64"
    esquema = "cll_dlt_gtc"
    procesar_con_gamma_relleno_fijo = True
    gamma_relleno = 16.4
    usar_tabla_α_exp = False
    α_exp = 1.0
    comentario = ""
    torres = []
    tener_en_cuenta_recomendacion = False
    guardar_corrida = True
    pausar_en_error = False

    # Data services
    data_services = DataServices(conn_string, esquema)

    # Info cargas
    info_cargas = Cargas(data_services)
    #info_cargas = CargasPorCuerpo(data_services)
    
    # Parámetros
    parametros = get_parametros_default()
    parametros["proc_iny"] = "IGU"
    parametros['b_max'] = 2.8
    parametros['d_f_max'] = 1.7
    parametros['n_soluciones'] = 999999999


    # Torres a correr
    lista_torres = data_services.listar_torres_obj()
    if torres and len(torres) > 0:
        if tener_en_cuenta_recomendacion:
            lista_torres = [t for t in lista_torres if t.recom_micropilotes and t.tipo != "D3" and t.nombre in torres]
        else:
            lista_torres = [t for t in lista_torres if t.tipo != "D3" and t.nombre in torres]
    else:
        lista_torres = [t for t in lista_torres if t.recom_micropilotes and t.tipo != "D3"]

    # Torres con gamma de relleno fijo
    if procesar_con_gamma_relleno_fijo:
        for torre in lista_torres:
            torre.gamma_r = gamma_relleno    

    # Evaluador
    evaluador = EvaluadorMicropilotes()

    # Optimizador
    optimizador = EncontrarSuelo(evaluador)

    # Crea la corrida
    n_soluciones = parametros['n_soluciones']             # Número de soluciones almacenadas
    f_carga_por_torre = parametros['f_carga_por_torre']   # Indica si la fracción de carga que toma el mp se toma por cada torre
    f_carga_mp_fijo = parametros['f_carga_mp_fijo']       # Si 'f_carga_por_torre' == False, fracción de carga fija que toma el mp de todas las torres
    info_f_carga = "por torre" if f_carga_por_torre else "fijo ({})".format(f_carga_mp_fijo)
    nombre_corrida = "Corrida {} torres - fracción de carga en mp {} - proceso de inyección {}. Evaluador: {}. Optimizador: {}, {} soluciones. {}".format(
        len(lista_torres), 
        info_f_carga,  
        parametros["proc_iny"], 
        type(evaluador).__name__, 
        type(optimizador).__name__, 
        n_soluciones,
        comentario)
    json_parametros = json.dumps(parametros)
    corrida_id = None
    # if guardar_corrida:
    #     corrida_id = data_services.guardar_corrida_micropilotes({"nombre": nombre_corrida, "parametros": json_parametros})
    # print("Corrida creada. id:{} - {}".format(corrida_id, nombre_corrida), flush=True )

    for torre in lista_torres:
        print(torre.nombre, flush=True)
        perfil, error_en_perfil, mensaje_error = obtener_perfil(data_services, vars(torre))

        resultados = None
        if error_en_perfil:
            print(torre.nombre, "Error en perfil", mensaje_error, flush=True)
        else:
            resultados = optimizador.optimizar(parametros, torre, perfil, info_cargas, usar_tabla_α_exp, α_exp, pausar_en_error)
            #print(torre.nombre, resultados)
            data_services.guardar_micropilotes_suelo(torre.nombre, resultados)
            
        # Guarda corrida - torre
        # cargas = info_cargas.obtener_cargas_as_dict(torre)
        # if guardar_corrida:
        #     data_services.guardar_corrida_micropilotes_torre(corrida_id, torre, perfil, cargas, error_en_perfil, mensaje_error, resultados, None)
        # else:
        #     #print(resultados)
        #     #input("pausa...")
        #     pass

    end_time = time.time()
    duracion = end_time - start_time    
    print(format_duracion(duracion))

if __name__ == "__main__":
    main()
