import json
import time
import copy
from cimentaciones.data_services import DataServices
from cimentaciones.perfil import Perfil, Estrato, obtener_perfil
from cimentaciones.cargas import Cargas
from cimentaciones.cargas_por_cuerpo import CargasPorCuerpo
from cimentaciones.evaluador_zapatas import EvaluadorZapatas
from cimentaciones.evaluador_zapata_diseno import EvaluadorZapataDiseno
from cimentaciones.util import format_duracion
from cimentaciones.parametros_zapata import get_parametros_default

def main():
    start_time = time.time()
    
    #conn_string = "host=p1378.concol.com dbname=sip_db user=test_user password=test_user"
    conn_string = "host=localhost dbname=sip_db user=postgres password=Magnus64"
    esquema = "cll_dlt_gtc"
    conjunto = "200727"
    # conjunto = '200728-PED-ESP'
    torres = []
    tener_en_cuenta_recomendacion = True
    guardar_corrida = False
    usar_geom_grupo = True
    comentario = f"Corrida con datos de diseño (grupos de zapatas definidos) - Conjunto {conjunto}. Geometrías de {'estrcuturas' if usar_geom_grupo else 'geotecnia' }"
    parametros = get_parametros_default()

    # Data services
    data_services = DataServices(conn_string, esquema)

    # Info cargas
    info_cargas = Cargas(data_services)

    # Torres a correr
    lista_torres = data_services.listar_torres_obj()
    if torres and len(torres) > 0:
        if tener_en_cuenta_recomendacion:
            lista_torres = [t for t in lista_torres if t.recom_zapata and t.tipo != "D3" and t.nombre in torres]
        else:
            lista_torres = [t for t in lista_torres if t.tipo != "D3" and t.nombre in torres]        
    else:
        lista_torres = [t for t in lista_torres if t.recom_zapata and t.tipo != "D3"]

    # Evaluador
    evaluador = EvaluadorZapatas()

    # Evalaluador en los puntos de diseño
    evaluador_diseno = EvaluadorZapataDiseno(evaluador)
    pausar_en_error = True

    # Crea la corrida
    
    nombre_corrida = f"Línea {esquema}, {len(lista_torres)} torres. {comentario}. Evaluador: {type(evaluador).__name__}. EvaluadorDiseño: {type(evaluador_diseno).__name__}"
    corrida_id = None
    if guardar_corrida:
        corrida_id = data_services.guardar_corrida_zapata({"nombre": nombre_corrida}, parametros)
    print(f"Corrida creada. id: {corrida_id} - {nombre_corrida}", flush=True )

    lista_zapatas_en_grupo = data_services.listar_zapatas_en_grupo(conjunto)   

    for zapata_en_grupo in lista_zapatas_en_grupo:
        torre = next(iter([t for t in lista_torres if t.nombre == zapata_en_grupo["torre"]]))
        print(torre.nombre, flush=True)
        
        perfil, error_en_perfil, mensaje_error = obtener_perfil(data_services, vars(torre))

        resultados = None
        if error_en_perfil:
            print(torre.nombre, "Error en perfil", mensaje_error, flush=True)
        else:
            # Si la zapata está en roca, remplaza toda la roca que está hasta D, con el último suelo.
            profundidad_roca = perfil.calcular_profundidad_hasta_roca()
            if profundidad_roca:
                perf_roca = zapata_en_grupo["d"] - profundidad_roca
                if perf_roca > 0:
                    perfil = copy.deepcopy(perfil)
                    perfil.extender_suelo_a_roca(perf_roca)

            # Evalúa
            resultados = evaluador_diseno.evaluar(zapata_en_grupo, parametros, torre, perfil, info_cargas, pausar_en_error, usar_geom_grupo)
            
        # Guarda corrida - torre
        cargas = info_cargas.obtener_cargas_as_dict(torre)
        if guardar_corrida:
            data_services.guardar_corrida_zapata_torre(corrida_id, torre, perfil, cargas, error_en_perfil, mensaje_error, resultados)
        else:
            #print(resultados)
            #input("pausa...")
            pass

    end_time = time.time()
    duracion = end_time - start_time    
    print(format_duracion(duracion))


if __name__ == "__main__":
    main()
    

