import math
import json
import time
import copy
from cimentaciones.data_services import DataServices
from cimentaciones.perfil import Perfil, Estrato, obtener_perfil
from cimentaciones.cargas import Cargas
from cimentaciones.evaluador_pilas import EvaluadorPila
from cimentaciones.util import format_duracion
from cimentaciones.parametros_pila import get_parametros_default
from cimentaciones.util import γ_agua, generar_serie
from cimentaciones.pila import Pila
from cimentaciones.torre import Torre

def main():
    start_time = time.time()
    
    conexion = input("Conexíon 1-Local / 2-Local_Nube / 3-Nube")
    if conexion.upper() == "1":
        conn_string = "host=localhost dbname=sip_db user=postgres password=Magnus64"
    elif conexion.upper() == "2":
        conn_string = "host=69.64.45.207 dbname=wsp_1378 user=sergio password=YWSaFM3fxUGkSaWqMvIL"
    elif conexion.upper() == "3":
        conn_string = "host=localhost dbname=wsp_1378 user=sergio password=YWSaFM3fxUGkSaWqMvIL"
    else:
        return

    esquema = "cll_dlt_gtc"
    torres = ["TCLL049N","TCLL498","TCLL501","TCLL503"]
    guardar_corrida = True
    comentario = f"Corrida con campana"
    parametros = get_parametros_default()

    # Data services
    data_services = DataServices(conn_string, esquema)

    # Info cargas
    info_cargas = Cargas(data_services)

    # Torres a correr
    lista_torres = data_services.listar_torres_obj()
    if torres and len(torres) > 0:
        lista_torres = [t for t in lista_torres if t.tipo != "D3" and t.nombre in torres]        
    else:
        lista_torres = [t for t in lista_torres if t.tipo != "D3"]


    # Evaluador
    evaluador = EvaluadorPila()

    pausar_en_error = True

    # Crea la corrida
    
    nombre_corrida = f"Línea {esquema}, {len(lista_torres)} torres. {comentario}. Evaluador: {type(evaluador).__name__}"
    corrida_id = None
    if guardar_corrida:
        corrida_id = data_services.guardar_corrida_pila({"nombre": nombre_corrida}, parametros)
    print(f"Corrida creada. id: {corrida_id} - {nombre_corrida}", flush=True )


    D_p_min = parametros["D_p_min"]     # D_p_min {float} -- Valor mínimo para las iteraciones de diametro de la pila D_p [m]
    D_p_max = parametros["D_p_max"]     # D_p_max {float} -- Valor máximo para las iteraciones de diametro de la pila D_p [m]
    D_p_paso = parametros["D_p_paso"]   # D_p_paso {float} -- Incremento para las iteraciones de diametro de la pila D_p [m] 

    h_i_min = parametros['h_i_min']     # h_i_min {float} -- Valor mínimo para las iteraciones de la profundidad de inicio de la pila [m]
    h_i_max = parametros['h_i_max']     # h_i_max {float} -- Valor máximo para las iteraciones de la profundidad de inicio de la pila [m]
    h_i_paso = parametros['h_i_paso']   # h_i_paso {float} -- Incremento para las iteraciones de la profundidad de inicio de la pila [m]

    H_min = parametros['H_min']         # H_min {float} -- Valor mínimo para las iteraciones del espesor de la pila H [m] 
    H_max = parametros['H_max']         # H_max {float} -- Valor máximo para las iteraciones del espesor de la pila H [m]
    H_paso = parametros['H_paso']       # H_paso {float} -- Incremento para las iteraciones del espesor de la pila H [m] 

    lista_HG = parametros["lista_hg"]   # Lista de altura de pedestales a evaluar [m] 

    campana = parametros['campana']     # campana{bool} -- Boleano que define condicion de pila con o sin campana
    h_c = parametros['h_c']             # h_c {float} -- altura de campana [m]
    h_con = parametros['h_con']         # h_con {float} -- Altura de la sección conica de la campana[m]
    θ_c= parametros['θ_c']              # θ_c {float} --  Ángulo de la campana [°]

    usar_TP = parametros['usar_tp']     # usar_tp {bool} -- Indica si los cálculos deben usar el tp indicado o calcular el TP mínimo
    dict_TP = parametros['dict_tp']     # dict_tp {dict} --  Lado correspondiente a la sección transversal del pedestal por tipo de torre [m]
    d_agg = parametros["d_agg"]         # d_agg {float} -- Tamaño máximo nominal del agregado grueso [m]
    d_b_long = parametros["d_b_long"]   # d_b_long {float} -- Diámetro de barras de refuerzo longitudinal [m]
    d_b_trans = parametros["d_b_trans"] # d_b_trans {float} -- Diámetro de barras de refuerzo transversal [m]
    rec = parametros["rec"]             # rec {float} -- Longitud del recubrimiento del dado [m]

    γ_c = parametros['gamma_c']         # gamma_c {float} -- Peso unitario de la cimentación [kN/m³]
    E_p = parametros["E_p"]             # E_p {float} -- Modulo de elasticidad del material de la pila [kPa]

    FSC = parametros['fsc']                            # fsc {float} -- Factore de seguridad a compresión
    FST = parametros['fst']                            # fst {float} -- Factor de seguridad a tensión suelo granular
    FSV = parametros['fsv']                            # fsv {float} -- Factor de seguridad para volcamiento
    FSLl = parametros['fsll']                          # fsll {float} -- Factor de seguridad mínimo para cargas laterales
    FSLc = parametros['fslc']                          # fslc {float} -- Factor de seguridad mínimo para cargas laterales
    S_max_adm_g = parametros['s_max_adm_g']            # s_max_adm_g {float} -- Asentamiento máximo permitido suelos granulares [m]
    S_max_adm_c = parametros['s_max_adm_c']            # s_max_adm_c {float} -- Asentamiento máximo permitido suelos cohesivos [m]
    S_max_adm_r = parametros['s_max_adm_r']            # s_max_adm_r {float} -- Asentamiento máximo permitido roca [m]

    for torre in lista_torres:
        print(torre.nombre, flush=True)

        perfil, error_en_perfil, mensaje_error = obtener_perfil(data_services, vars(torre))
        θ = info_cargas.get_angulo_inclinacion(torre) # Ángulo del pedestal con respecto a la vertical [°]
        ω = torre.inclinacion_terreno or 0
        if usar_TP:
            TP = dict_TP[torre.tipo]
        else:
            ancho_aleta = info_cargas.get_ancho_aleta_conector_cortante(torre)
            TP = 2 * (1.5 * ancho_aleta + d_agg + d_b_long + d_b_trans + rec)
            TP = math.ceil(TP * 10) / 10         # Aproximación a la décima por arriba  

        resultados = []

        for D_p in generar_serie(D_p_min, D_p_max, D_p_paso, 2):
            for h_i in generar_serie(h_i_min, h_i_max, h_i_paso, 2):
                for H in generar_serie(H_min, H_max, H_paso, 2):
                    for HG in lista_HG:
                        try:
                            pila = Pila(D_p, h_i, H, HG, h_c, h_con, θ_c, TP, θ, γ_c, E_p, perfil, campana, ω)
                            resultado = dict(vars(pila))
                            del resultado["perfil"]
                            evaluacion = evaluador.evaluar(pila, torre, perfil, info_cargas, FSC, FST, FSV, FSLl, FSLc, S_max_adm_c, S_max_adm_g, S_max_adm_r)
                            resultado["evaluacion"] = evaluacion
                            resultado["cumple"] = all([evaluacion[key]["cumple"] for key in evaluacion])
                            resultado["error"] = False
                            resultado["mensaje_error"] = None                              
                        except Exception  as e:
                            resultado["error"] = True
                            resultado["mensaje_error"] = str(e)     
                            resultado["cumple"] = False
                        resultados.append(resultado)
        if guardar_corrida:
            cargas = info_cargas.obtener_cargas_as_dict(torre)
            data_services.guardar_corrida_pila_torre(corrida_id, torre, perfil, cargas, error_en_perfil, mensaje_error, resultados)

    end_time = time.time()
    duracion = end_time - start_time    
    print(format_duracion(duracion))


if __name__ == "__main__":
    main()
    

