import json
import time
from cimentaciones.data_services import DataServices
from cimentaciones.perfil import Perfil, Estrato, obtener_perfil
from cimentaciones.cargas import Cargas
from cimentaciones.evaluador_micropilotes import EvaluadorMicropilotes
from cimentaciones.evaluador_micropilotes_diseno import EvaluadorMicropilotesDiseno
from cimentaciones.util import generar_serie, format_duracion
from cimentaciones.parametros_micropilotes import get_parametros_default

def main():
    start_time = time.time()
    #conn_string = "host=p1378.concol.com dbname=sip_db user=test_user password=test_user"
    conn_string = "host=localhost dbname=sip_db user=postgres password=Magnus64"
    esquema = "cll_dlt_gtc"
    # conjunto = "IGU-PED-ESP-200718"
    # conjunto = "IGU-PED-ESP-200730"
    # conjunto = "IRS-c_cob-15%-i18"
    # conjunto = "IGU-c_cob-15%-i17-r"
    conjunto = "IGU-c_cob_lc-15%-i24a-r"
    # conjunto = "IRS-c_cob_lc-15%-i25a-r"
    # conjunto = "IGU-PED-ESP-200730"
    # conjunto = "IRS-PED-ESP-200801"
    procesar_con_gamma_relleno_fijo = True
    gamma_relleno = 16.4
    usar_tabla_α_exp = False
    α_exp = 1.0
    usar_geom_grupo = True
    guardar_corrida = True
    pausar_en_error = False

    # Data services
    data_services = DataServices(conn_string, esquema)

    # Info cargas
    info_cargas = Cargas(data_services)
    
    # Parámetros
    parametros = get_parametros_default()

    lista_HG = parametros['lista_hg']
    # lista_HG = parametros['lista_hg_esp']

    # Torres a correr
    lista_torres = data_services.listar_torres_obj()

    # Torres con gamma de relleno fijo
    if procesar_con_gamma_relleno_fijo:
        for torre in lista_torres:
            torre.gamma_r = gamma_relleno    

    # Evaluador
    evaluador = EvaluadorMicropilotes()

    # Evaluador en grupo
    evaluador_en_grupo = EvaluadorMicropilotesDiseno(evaluador)

    # Crea la corrida
    f_carga_por_torre = parametros['f_carga_por_torre']   # Indica si la fracción de carga que toma el mp se toma por cada torre
    f_carga_mp_fijo = parametros['f_carga_mp_fijo']       # Si 'f_carga_por_torre' == False, fracción de carga fija que toma el mp de todas las torres
    info_f_carga = "por torre" if f_carga_por_torre else "fijo ({})".format(f_carga_mp_fijo)
    comentario_geom = f"H/TP/Anclaje {'del grupo' if usar_geom_grupo else 'propios'}."
    nombre_corrida = f"Prueba de conjunto {conjunto}. {len(lista_torres)} Torres. {comentario_geom}"
    json_parametros = json.dumps(parametros)
    corrida_id = None
    if guardar_corrida:
        corrida_id = data_services.guardar_corrida_micropilotes({"nombre": nombre_corrida, "parametros": json_parametros})
    print("Corrida creada. id:{} - {}".format(corrida_id, nombre_corrida), flush=True )

    lista_micropilotes_en_grupo = data_services.listar_micropilote_en_grupo(conjunto) 

    # # Se le quitan 5cm para prueba por estructuras
    # for micropilotes_en_grupo in lista_micropilotes_en_grupo:
    #     micropilotes_en_grupo["l_b"] -= 0.05
    

    for micropilotes_en_grupo in lista_micropilotes_en_grupo:
        # if micropilotes_en_grupo["id"] != 2097:
        #     continue

        torre = next(iter([t for t in lista_torres if t.nombre == micropilotes_en_grupo["torre"]]))
        print(torre.nombre, flush=True)
        perfil, error_en_perfil, mensaje_error = obtener_perfil(data_services, vars(torre))


        resultados = None
        if error_en_perfil:
            print(torre.nombre, "Error en perfil", mensaje_error, flush=True)
        else:
            resultados = evaluador_en_grupo.evaluar(micropilotes_en_grupo, parametros, torre, perfil, info_cargas, usar_tabla_α_exp, α_exp, pausar_en_error, usar_geom_grupo, lista_HG)
            
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
