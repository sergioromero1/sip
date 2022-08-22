import json
import time
from cimentaciones.data_services import DataServices
from cimentaciones.perfil import Perfil, Estrato, obtener_perfil
from cimentaciones.cargas import Cargas
from cimentaciones.cargas_por_cuerpo import CargasPorCuerpo
from cimentaciones.evaluador_pilastras import EvaluadorPilastras
from cimentaciones.evaluador_pilastra_diseno import EvaluadorPilastraDiseno
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
    conjunto = "PED-ESP"
    comentario = f"Corrida con datos de diseño (grupos de pilastras definidos) - Conjunto {conjunto}"
    torres = []
    procesar_con_gamma_relleno_fijo = True   # <-- gamma relleno
    gamma_relleno = 16.4
    tener_en_cuenta_recomendacion = True
    guardar_corrida = True
    parametros = get_parametros_default()

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

    # valaluador en los puntos de diseño
    evaluador_diseno = EvaluadorPilastraDiseno(evaluador)
    pausar_en_error = True

    # Constructor de Pilastra
    constructorPilastra = Pilastra

    # Crea la corrida
    nombre_corrida = "Línea {}, {} torres. Constructor: {}.  Evaluador: {}. EvaluadorDiseño: {}. Pilastra tipo {}. {}".format(
        esquema,
        len(lista_torres),
        constructorPilastra.__name__,
        type(evaluador).__name__, 
        type(evaluador_diseno).__name__, 
        constructorPilastra.__name__,
        comentario)
    
    corrida_id = None
    if guardar_corrida:
        corrida_id = data_services.guardar_corrida_pilastra({"nombre": nombre_corrida}, parametros)
    print("Corrida creada. id:{} - {}".format(corrida_id, nombre_corrida), flush=True )

    lista_pilastras_en_grupo = data_services.listar_pilastras_en_grupo(conjunto)  

    for pilastra_en_grupo in lista_pilastras_en_grupo:
        torre = next(iter([t for t in lista_torres if t.nombre == pilastra_en_grupo["torre"]]))
        print(torre.nombre, flush=True)
        perfil, error_en_perfil, mensaje_error = obtener_perfil(data_services, vars(torre))

        resultados = None
        if error_en_perfil:
            print("Error en perfil", mensaje_error, flush=True)
        else:
            resultados = evaluador_diseno.evaluar(pilastra_en_grupo, parametros, torre, perfil, info_cargas, pausar_en_error, constructorPilastra)

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
    

