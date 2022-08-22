import json
import time
import copy
from cimentaciones.data_services import DataServices
from cimentaciones.perfil import Perfil, Estrato, obtener_perfil
from cimentaciones.cargas import Cargas
from cimentaciones.cargas_por_cuerpo import CargasPorCuerpo
from cimentaciones.evaluador_parrillas import EvaluadorParrillas
from cimentaciones.evaluador_parrilla_diseno import EvaluadorParrillasDiseno
from cimentaciones.util import format_duracion
from cimentaciones.parametros_parrilla import get_parametros_default

def main():
    start_time = time.time()
    
    #conn_string = "host=p1378.concol.com dbname=sip_db user=test_user password=test_user"
    conn_string = "host=localhost dbname=sip_db user=postgres password=Magnus64"
    esquema = "cll_dlt_gtc"
    comentario = f"Corrida de validación de parrillas"
    tipo_parrilla = 'Pesada'
    tener_en_cuenta_recomendacion = True
    guardar_corrida = True
    parametros = get_parametros_default()

    # Data services
    data_services = DataServices(conn_string, esquema)

    # Info cargas
    info_cargas = Cargas(data_services)

    # Torres a correr
    torres = [] #["TCLL184A","TCLL184B","TCLL185","TCLL185A","TCLL186"]

    lista_torres = data_services.listar_torres_obj()
    if torres and len(torres) > 0:
        if tener_en_cuenta_recomendacion:
            lista_torres = [t for t in lista_torres if t.recom_parrilla and t.tipo != "D3" and t.nombre in torres]
        else:
            lista_torres = [t for t in lista_torres if t.tipo != "D3" and t.nombre in torres]        
    else:
        lista_torres = [t for t in lista_torres if t.recom_parrilla and t.tipo != "D3"]

    # Evaluador
    evaluador = EvaluadorParrillas()

    # Evalaluador en los puntos de diseño
    evaluador_diseno = EvaluadorParrillasDiseno(evaluador)
    pausar_en_error = True

    # Crea la corrida
    nombre_corrida = f"Línea {esquema}, {len(lista_torres)} torres. Evaluador: {type(evaluador).__name__}. EvaluadorDiseño: {type(evaluador_diseno).__name__}. {comentario}"
    
    corrida_id = None
    if guardar_corrida:
        corrida_id = data_services.guardar_corrida_parrilla({"nombre": nombre_corrida}, parametros)
    print(f"Corrida creada. id: {corrida_id} - {nombre_corrida}", flush=True )

    lista_datos_parrillas = data_services.listar_datos_parrillas(tipo_parrilla)   

    for datos_parrilla in lista_datos_parrillas:
        torre = next(iter([t for t in lista_torres if t.nombre == datos_parrilla["torre"]]))
        print(torre.nombre, flush=True)
        
        perfil, error_en_perfil, mensaje_error = obtener_perfil(data_services, vars(torre))

        resultados = None
        if error_en_perfil:
            print(torre.nombre, "Error en perfil", mensaje_error, flush=True)
        else:
            # Si la parrilla está en roca, remplaza toda la roca que está hasta D, con el último suelo.
            profundidad_roca = perfil.calcular_profundidad_hasta_roca()
            if profundidad_roca:
                perf_roca = datos_parrilla["d"] - profundidad_roca
                if perf_roca > 0:
                    perfil = copy.deepcopy(perfil)
                    perfil.extender_suelo_a_roca(perf_roca)

            # Evalúa
            resultados = evaluador_diseno.evaluar(datos_parrilla, parametros, torre, perfil, info_cargas, pausar_en_error)
            
        # Guarda corrida - torre
        cargas = info_cargas.obtener_cargas_as_dict(torre)
        if guardar_corrida:
            data_services.guardar_corrida_parrilla_torre(corrida_id, torre, perfil, cargas, error_en_perfil, mensaje_error, resultados)
        else:
            #print(resultados)
            #input("pausa...")
            pass

    end_time = time.time()
    duracion = end_time - start_time    
    print(format_duracion(duracion))


if __name__ == "__main__":
    main()
    

