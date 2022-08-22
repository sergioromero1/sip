import json
import time
from cimentaciones.data_services import DataServices
from cimentaciones.perfil import Perfil, Estrato, obtener_perfil
from cimentaciones.cargas import Cargas
from cimentaciones.evaluador_micropilotes import EvaluadorMicropilotes
from cimentaciones.optimizador_micropilotes_por_torre import OptimizadorMicropilotesPorTorre
from cimentaciones.util import generar_serie, format_duracion
from cimentaciones.parametros_micropilotes import get_parametros_default


def main():
    start_time = time.time()
    #conn_string = "host=p1378.concol.com dbname=sip_db user=test_user password=test_user"
    conn_string = "host=localhost dbname=sip_db user=postgres password=Magnus64"
    esquema = "cll_dlt_gtc"
    usar_tabla_α_exp = False
    α_exp = 1.0

    ### IGU
    # comentario =  "Corrida completa. Pedestales convencionales. Barra R38-550"    
    # comentario =  "Corrida torres cambio f_carga_mp. Pedestales estándares. Barra R38-550"
    # comentario =  "Corrida extra Df hasta 1.7m. Pedestales estándares. Barra R38-550"
    # comentario =  "Corrida extra Df hasta 1.7m, B hasta 4m. Pedestales estándares. Barra R38-550"
    # comentario =  "Corrida torres no pasan parrilla. Pedestales estándares. Barra R38-550"
    # comentario =  "Corrida torres no pasan parrilla TCLL493. Pedestales estándares. Barra R38-550"
    # comentario =  "Corrida extra Df hasta 1.7m, B hasta 3.5m. Pedestales estándares. Barra R38-550"
    # comentario =  "Corrida extra para torre TCLL295 B hasta 3.5m. Pedestales estándares. Barra R38-550"
    # comentario =  "Corrida extra. Pedestales especiales. Bmax 4.0. Barra R38-550"

    ### IRS
    # comentario =  "Corrida completa. Pedestales estándares. Barra DSI GEWI 28 PLUS"
    # comentario =  "Corrida extra Df hasta 1.7m. Pedestales estándares. Barra DSI GEWI 28 PLUS"
    # comentario =  "Corrida extra Df hasta 1.7m, B hasta 4m. Pedestales estándares. Barra DSI GEWI 28 PLUS"
    # comentario =  "Corrida extra Df hasta 1.7m, B hasta 3.5m. Pedestales estándares. Barra DSI GEWI 28 PLUS"
    # comentario =  "Corrida extra. Pedestales especiales. Bmax 4.0. Barra DSI GEWI 28 PLUS"
    # comentario =  "Corrida extra, nuevas torres. Pedestales estándares. Barra DSI GEWI 28 PLUS"
    # comentario =  "Corrida extra, Torre TCLL106V. Pedestales espciales. Bmax 4.0. Barra DSI GEWI 28 PLUS"

    proc_iny = input("Proceso de inyección [IGU]: ") or "IGU"
    b_max = float(input("B_max [2.8], 3.5, ...: ") or "2.8")
    d_f_max = float(input("Df_max [1.5], 1.7, ...: ") or "1.5")
    lista_hg = [1.0, 1.5, 2.0, 3.0] if (input("Pedestales Conv/Esp [C]/E: ") or "C").upper() == "C" else [4.0, 5.0, 6.0, 7.0, 8.0]
    torres = []
    torres_a_procesar = input("Torres [Todas]: ")
    if torres_a_procesar.strip() != "" :
        torres = torres_a_procesar.replace(" ","").split(",")
    tener_en_cuenta_recomendacion = (input("Tener en cuenta la recomendacion [S]/N: ") or "S").upper() == "S" 
    bloque = int(input("Tamaño bloque [100]: ") or "100")
    salto = int(input("Salto [0]: ") or "0")
    comentario =  input("Comentarios: ") 
    guardar_corrida = True if (input("Guardar [S]/N:") or "S").upper() == "S" else False
    pausar_en_error = (input("Pausar en error S/[N]: ") or "N").upper() == "S" 

    # Parámetros
    parametros = get_parametros_default()
    parametros["proc_iny"] = proc_iny
    parametros['b_max'] = b_max
    parametros['d_f_max'] = d_f_max
    parametros['n_soluciones'] = 999999999
    parametros['lista_hg'] = lista_hg

    # Data services
    data_services = DataServices(conn_string, esquema)

    # Info cargas
    info_cargas = Cargas(data_services)
    #info_cargas = CargasPorCuerpo(data_services)
    
    # Torres a correr    
    lista_torres = data_services.listar_torres_obj()
    if torres and len(torres) > 0:
        if tener_en_cuenta_recomendacion:
            lista_torres = [t for t in lista_torres if t.recom_micropilotes and t.tipo != "D3" and t.nombre in torres]
        else:
            lista_torres = [t for t in lista_torres if t.tipo != "D3" and t.nombre in torres]
    else:
        lista_torres = [t for t in lista_torres if t.recom_micropilotes and t.tipo != "D3"]

    lista_torres = lista_torres[salto:salto+bloque]

    # Evaluador
    evaluador = EvaluadorMicropilotes()

    # Optimizador
    optimizador = OptimizadorMicropilotesPorTorre(evaluador)

    # Crea la corrida
    n_soluciones = parametros['n_soluciones']             # Número de soluciones almacenadas
    f_carga_por_torre = parametros['f_carga_por_torre']   # Indica si la fracción de carga que toma el mp se toma por cada torre
    f_carga_mp_fijo = parametros['f_carga_mp_fijo']       # Si 'f_carga_por_torre' == False, fracción de carga fija que toma el mp de todas las torres
    info_f_carga = "por torre" if f_carga_por_torre else "fijo ({})".format(f_carga_mp_fijo)
    nombre_corrida = "Corrida {} torres ({}/{})- fracción de carga en mp {} - proceso de inyección {}, B max [{}], D_f max [{}]. {}".format(
        len(lista_torres), 
        salto,
        bloque,
        info_f_carga,
        parametros["proc_iny"], 
        parametros['b_max'],
        parametros['d_f_max'],
        comentario)
    json_parametros = json.dumps(parametros)
    corrida_id = None
    if guardar_corrida:
        corrida_id = data_services.guardar_corrida_micropilotes({"nombre": nombre_corrida, "parametros": json_parametros})
    print("Corrida creada. id:{} - {}".format(corrida_id, nombre_corrida), flush=True )

    for torre in lista_torres:
        print(torre.nombre, flush=True)
        perfil, error_en_perfil, mensaje_error = obtener_perfil(data_services, vars(torre))

        resultados = None
        if error_en_perfil:
            print(torre.nombre, "Error en perfil", mensaje_error, flush=True)
        else:
            resultados = optimizador.optimizar(parametros, torre, perfil, info_cargas, usar_tabla_α_exp, α_exp, pausar_en_error)
            
        # Guarda corrida - torre
        cargas = info_cargas.obtener_cargas_as_dict(torre)
        if guardar_corrida:
            data_services.guardar_corrida_micropilotes_torre(corrida_id, torre, perfil, cargas, error_en_perfil, mensaje_error, resultados, None)
        else:
            #print(resultados)
            #input("pausa...")
            pass

    end_time = time.time()
    duracion = end_time - start_time    
    print(format_duracion(duracion))

if __name__ == "__main__":
    main()
