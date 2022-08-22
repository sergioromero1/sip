import json
import time
from cimentaciones.data_services import DataServices
from cimentaciones.perfil import Perfil, Estrato, obtener_perfil
from cimentaciones.cargas import Cargas
from cimentaciones.cargas_por_cuerpo import CargasPorCuerpo
from cimentaciones.evaluador_zapatas import EvaluadorZapatas
from cimentaciones.optimizador_zapatas_por_torre import OptimizadorZapatasPorTorre
from cimentaciones.util import format_duracion
from cimentaciones.parametros_zapata import get_parametros_default

def main():
    start_time = time.time()
    
    #conn_string = "host=p1378.concol.com dbname=sip_db user=test_user password=test_user"
    conn_string = "host=localhost dbname=sip_db user=postgres password=Magnus64"
    esquema = "cll_dlt_gtc"

    b_min = float(input("B_max [2.0]: ") or "2.0")
    b_max = float(input("B_max [4.5]: ") or "4.5")
    d_min = float(input("D_min [2.0]: ") or "2.0")
    d_max = float(input("D_max [4.0]: ") or "4.0")
    lista_hg = [0.25, 0.5, 1.0, 1.5, 2.0] if (input("Pedestales Conv/Esp [C]/E: ") or "C").upper() == "C" else [3.0, 4.0, 5.0, 6.0, 7.0]
    torres = []
    torres_a_procesar = input("Torres [Todas]: ")
    if torres_a_procesar.strip() != "" :
        torres = torres_a_procesar.replace(" ","").split(",")
    tener_en_cuenta_recomendacion = (input("Tener en cuenta la recomendacion [S]/N: ") or "S").upper() == "S" 
    # bloque = int(input("Tamaño bloque [100]: ") or "100")
    # salto = int(input("Salto [0]: ") or "0")
    comentario =  input("Comentarios: ") 
    guardar_corrida = True if (input("Guardar [S]/N:") or "S").upper() == "S" else False
    pausar_en_error = (input("Pausar en error S/[N]: ") or "N").upper() == "S" 

    # Parámetros
    parametros = get_parametros_default()

    correr_con_H_de_grupo = False
    grupo_corrida_zapata_id = None
    tener_en_cuenta_recomendacion = True
    parametros["optimo_por_profundidad"] = False
    parametros["usar_prof_min_desp_por_torre"] = True
    parametros['n_soluciones'] = 9999999
    parametros['b_min'] = b_min                           # b_min {float} -- Valor mínimo para las iteraciones de ancho de la zapata B [m]
    parametros['b_max'] = b_max                           # b_max {float} -- Valor máximo para las iteraciones de ancho de la zapata B [m]
    parametros['d_min'] = d_min                           # d_min {float} -- Valor mínimo para las iteraciones de la profundidad de la zapata B [m]
    parametros['d_max'] = d_max                           # d_max {float} -- Valor máximo para las iteraciones de la profundidad de la zapata B [m]
    parametros["lista_hg"] = lista_hg

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

    # Optimizador
    optimizador = OptimizadorZapatasPorTorre(evaluador)
    optimo_por_profundidad = parametros["optimo_por_profundidad"]
    usar_prof_min_desp_por_torre = parametros["usar_prof_min_desp_por_torre"]
    pausar_en_error = True

    # Crea la corrida
    n_soluciones = parametros['n_soluciones']      # Número de soluciones almacenadas
    hg_por_pata = parametros['hg_por_pata']        # Indica si aparte de la lista de hgs a evaluar, se debe incluir el hg de cada pata

    # comentario_soluciones = "Óptimos por profundidad" if optimo_por_profundidad else str(n_soluciones) + " soluciones"
    comentario_H = f"Hs de los grupos de corrida {grupo_corrida_zapata_id}" if correr_con_H_de_grupo else "Hs calculados individualmente"
    nombre_corrida = f"Línea {esquema}, {len(lista_torres)} torres. {(comentario + '. ') if comentario != '' else ''}{comentario_H}. HGs:{parametros['lista_hg']}.B: {parametros['b_min']}-{parametros['b_max']}. D: {parametros['d_min']}-{parametros['d_max']}. Evaluador: {type(evaluador).__name__}. Optimizador: {type(optimizador).__name__}"
    
    corrida_id = None
    if guardar_corrida:
        corrida_id = data_services.guardar_corrida_zapata({"nombre": nombre_corrida}, parametros)
    print(f"Corrida creada. id: {corrida_id} - {nombre_corrida}", flush=True )

    if correr_con_H_de_grupo:
        torres_h = data_services.listar_grupos_zapatas_por_torre(grupo_corrida_zapata_id)

    for torre in lista_torres:
        print(torre.nombre, flush=True)
        perfil, error_en_perfil, mensaje_error = obtener_perfil(data_services, vars(torre))

        H = None
        if correr_con_H_de_grupo:
            H = next(iter([ t["h_est"] for t in torres_h if t["torre"] == torre.nombre]), None)

        resultados = None
        if error_en_perfil:
            print("Error en perfil", mensaje_error, flush=True)
        else:
            resultados = optimizador.optimizar(parametros, torre, perfil, info_cargas, hg_por_pata, n_soluciones, optimo_por_profundidad, pausar_en_error, usar_prof_min_desp_por_torre, H)

        # Guarda corrida - torre
        cargas = info_cargas.obtener_cargas_as_dict(torre)
        if guardar_corrida:
            data_services.guardar_corrida_zapata_torre(corrida_id, torre, perfil, cargas, error_en_perfil, mensaje_error, resultados)
        else:
            #print(json.dumps(resultados))
            # input("pausa...")
            pass

    end_time = time.time()
    duracion = end_time - start_time    
    print(format_duracion(duracion))


if __name__ == "__main__":
    main()
    

