import math
import sys
import copy
import time
import json
from cimentaciones.data_services import DataServices
from cimentaciones.util import γ_agua, generar_serie,format_duracion
from cimentaciones.cargas import Cargas
from cimentaciones.zapata import Zapata
from cimentaciones.parametros_zapata import get_parametros_default
from cimentaciones.perfil import Perfil, obtener_perfil

def main():
    conn_string = "host=localhost dbname=sip_db user=postgres password=Magnus64"
    esquema = "cll_dlt_gtc"
    parametros = get_parametros_default()

    procesar_con_gamma_relleno_fijo = True
    gamma_relleno = 16.4
    usar_h_de_grupo = False
    usar_tp_de_grupo = False
    
    # conjunto = "PED-ESP-200728"
    # lista_HG = parametros["lista_hg_esp"]

    conjunto = "200727"
    lista_HG = parametros["lista_hg"]
    
    data_services = DataServices(conn_string, esquema)
    
    info_cargas = Cargas(data_services)

    torres = data_services.listar_torres_obj()
    if procesar_con_gamma_relleno_fijo:
        for torre in torres:
            torre.gamma_r = gamma_relleno

    grupos = data_services.listar_zapata_grupo(conjunto)
    for grupo in grupos:
        agregar_info_a_grupo(data_services, grupo, torres, info_cargas, parametros, usar_h_de_grupo, lista_HG, usar_tp_de_grupo)
        data_services.actualizar_zapata_grupo(grupo)
        print(grupo["tipo"], grupo["concreto"], grupo["b"], grupo["d"])
    print("Done")

def agregar_info_a_grupo(data_services, grupo, torres, info_cargas, parametros, usar_h_de_grupo, lista_HG, usar_tp_de_grupo):
    B = grupo["b"]
    D = grupo["d"]
    H_grupo = grupo["h_grupo"] 
    TP_grupo = grupo["tp_grupo"] 
    qs = {}
    for HG in lista_HG:
        qs[HG] = {"Q_max_d": sys.float_info.min, "Q_min_d": sys.float_info.min, 
                "Q_max_t": sys.float_info.min, "Q_min_t": sys.float_info.min, "q_ult": sys.float_info.max}
    TPs = []
    Hs = []
    materiales_relleno = []        
    for nombre_torre in grupo["torres"].split(","):
        torre = next(iter([t for t in torres if t.nombre == nombre_torre]))
        perfil, error_en_perfil, mensaje_error = obtener_perfil(data_services, vars(torre))
        
        if error_en_perfil:
            raise ValueError(mensaje_error)
        for HG in lista_HG:
            zapata = crear_zapata(torre, perfil, info_cargas, parametros, B, D, HG, H_grupo, usar_h_de_grupo, TP_grupo, usar_tp_de_grupo)
            if zapata:
                
                if not zapata.TP in TPs:
                    TPs.append(zapata.TP)

                if not zapata.H in Hs:
                    Hs.append(zapata.H)
                
                materiales_relleno.append(zapata.perfil.calcular_material_relleno(zapata.D - zapata.H))

                F_zc, F_xc, F_yc = info_cargas.obtener_cargas_diseno_maxima_compresion_cartesiano(torre)
                Q_max_d, Q_min_d, _ = zapata.calculo_esfuerzo_actuante_sobre_suelo(F_xc, F_yc, F_zc)
                
                if Q_max_d > qs[HG]["Q_max_d"]:
                    qs[HG]["Q_max_d"] = Q_max_d

                if Q_min_d > qs[HG]["Q_min_d"]:
                    qs[HG]["Q_min_d"] = Q_min_d

                F_zc, F_xc, F_yc = info_cargas.obtener_cargas_trabajo_maxima_compresion_cartesiano(torre)
                Q_max_t, Q_min_t, _ = zapata.calculo_esfuerzo_actuante_sobre_suelo(F_xc, F_yc, F_zc)

                if Q_max_t > qs[HG]["Q_max_t"]:
                    qs[HG]["Q_max_t"] = Q_max_t

                if Q_min_t > qs[HG]["Q_min_t"]:
                    qs[HG]["Q_min_t"] = Q_min_t

                F_zc, F_xc, F_yc = info_cargas.obtener_cargas_diseno_maxima_longitudinal_cartesiano(torre)
                Q_max_d, Q_min_d, _ = zapata.calculo_esfuerzo_actuante_sobre_suelo(F_xc, F_yc, F_zc)

                if Q_max_d > qs[HG]["Q_max_d"]:
                    qs[HG]["Q_max_d"] = Q_max_d

                if Q_min_d > qs[HG]["Q_min_d"]:
                    qs[HG]["Q_min_d"] = Q_min_d

                F_zc, F_xc, F_yc = info_cargas.obtener_cargas_trabajo_maxima_longitudinal_cartesiano(torre)
                Q_max_t, Q_min_t, _ = zapata.calculo_esfuerzo_actuante_sobre_suelo(F_xc, F_yc, F_zc)

                if Q_max_t > qs[HG]["Q_max_t"]:
                    qs[HG]["Q_max_t"] = Q_max_t

                if Q_min_t > qs[HG]["Q_min_t"]:
                    qs[HG]["Q_min_t"] = Q_min_t

                F_zc, F_xc, F_yc = info_cargas.obtener_cargas_diseno_maxima_transversal_cartesiano(torre)
                Q_max_d, Q_min_d, _ = zapata.calculo_esfuerzo_actuante_sobre_suelo(F_xc, F_yc, F_zc)
        
                if Q_max_d > qs[HG]["Q_max_d"]:
                    qs[HG]["Q_max_d"] = Q_max_d

                if Q_min_d > qs[HG]["Q_min_d"]:
                    qs[HG]["Q_min_d"] = Q_min_d

                F_zc, F_xc, F_yc = info_cargas.obtener_cargas_trabajo_maxima_transversal_cartesiano(torre)
                Q_max_t, Q_min_t, _ = zapata.calculo_esfuerzo_actuante_sobre_suelo(F_xc, F_yc, F_zc)
        
                if Q_max_t > qs[HG]["Q_max_t"]:
                    qs[HG]["Q_max_t"] = Q_max_t

                if Q_min_t > qs[HG]["Q_min_t"]:
                    qs[HG]["Q_min_t"] = Q_min_t

                F_zc, F_xc, F_yc = info_cargas.obtener_cargas_trabajo_maxima_compresion_cartesiano(torre)
                q_ult, _ = zapata.calculo_capacidad_portante(max(F_xc, F_yc), F_zc)

                if q_ult < qs[HG]["q_ult"]:
                    qs[HG]["q_ult"] = q_ult

                F_zc, F_xc, F_yc = info_cargas.obtener_cargas_trabajo_maxima_longitudinal_cartesiano(torre)
                q_ult, _ = zapata.calculo_capacidad_portante(max(F_xc, F_yc), F_zc)

                if q_ult < qs[HG]["q_ult"]:
                    qs[HG]["q_ult"] = q_ult

                F_zc, F_xc, F_yc = info_cargas.obtener_cargas_trabajo_maxima_transversal_cartesiano(torre)
                q_ult, _ = zapata.calculo_capacidad_portante(max(F_xc, F_yc), F_zc)

                if q_ult < qs[HG]["q_ult"]:
                    qs[HG]["q_ult"] = q_ult

    # Material de relleno
    cohesivos = [mat for mat in materiales_relleno if mat["tipo_mat"] == "c"]
    granulares= [mat for mat in materiales_relleno if mat["tipo_mat"] == "g"]
    φ_r = 0 if len(granulares) == 0 else sum([mat["φ"] for mat in granulares]) / len(granulares)
    c_u_r = 0 if len(cohesivos) == 0 else sum([mat["c_u"] for mat in cohesivos]) / len(cohesivos)
    γ_r = 0 if len(materiales_relleno) == 0 else sum([mat["γ"] for mat in materiales_relleno]) / len(materiales_relleno)
    if usar_h_de_grupo:
        grupo["qs_h_grupo"] = json.dumps(qs)
        grupo["qs_h_propio"] = json.dumps(grupo["qs_h_propio"])
        grupo["geometrias"] = json.dumps(grupo["geometrias"])
    else:
        grupo["qs_h_grupo"] = json.dumps(grupo["qs_h_grupo"])
        grupo["qs_h_propio"] = json.dumps(qs)
        grupo["geometrias"] = json.dumps({"TP_min" : min(TPs), "TP_max": max(TPs), "H_min": min(Hs), "H_max": max(Hs)})
    grupo["relleno"] = json.dumps({"φ_r": φ_r, "c_u_r": c_u_r, "γ_r": γ_r})

def crear_zapata(torre, perfil, info_cargas, parametros, B, D, HG, H_grupo, usar_h_de_grupo, TP_grupo, usar_tp_de_grupo):
    perf_roca_min = parametros["perf_roca_min"]                    # perf_roca_min {float} -- Perforación mínima de la zapata a la roca [m]
    perf_roca_max = parametros["perf_roca_max"]                    # perf_roca_max {float} -- Perforación máxima de la zapata a la roca [m]
    dist_atraccion_roca = parametros["dist_atraccion_roca"]        # dist_atraccion_roca {float} -- Distancia a la roca, a partir de la cual debe penetrar la zapata [m]
    perfil_ajustado = perfil
    profundidad_roca = perfil.calcular_profundidad_hasta_roca()    
    if profundidad_roca:
        perf_roca = round(D - profundidad_roca, 2)
        if perf_roca > perf_roca_max:
            raise ValueError(f"La zapata entra en la roca más de lo permitido: {perf_roca} > {perf_roca_max}")
        elif perf_roca >= -dist_atraccion_roca:
            if perf_roca < perf_roca_min:
                perf_roca = perf_roca_min
                D = profundidad_roca + perf_roca_min
            perfil_ajustado = copy.deepcopy(perfil)
            perfil_ajustado.extender_suelo_a_roca(perf_roca)

    # Peso unitario de la cimentación. Se corrige más adelante por saturación. [kN/m³]
    γ_c = parametros["gamma_c"]

    NF = perfil.calcular_NF()

    # Se satura todo el perfil si
    # el nivel freático esta por encima de
    # la profundidad de desplante
    if NF is not None and NF < D:
        perfil_ajustado = perfil_ajustado.clonar_saturado()
        ajuste_saturacion_perfil = True
    else:
        ajuste_saturacion_perfil = False

    # Ángulo del pedestal con respecto a la vertical [°]                        
    θ = info_cargas.get_angulo_inclinacion(torre)    

    # TP: Lado correspondiente a la sección transversal del pedestal [m]
    if usar_tp_de_grupo:  
        TP = TP_grupo
    else:
        usar_TP = parametros["usar_tp"] 
        if usar_TP:
            dict_TP = parametros["dict_tp"]
            TP = dict_TP[torre.tipo]
        else:
            d_agg = parametros["d_agg"]          # d_agg {float} -- Tamaño máximo nominal del agregado grueso [m]
            d_b_long = parametros["d_b_long"]    # d_b_long {float} -- Diámetro de barras de refuerzo longitudinal [m]
            d_b_trans = parametros["d_b_trans"]  # d_b_trans {float} -- Diámetro de barras de refuerzo transversal [m]
            rec = parametros["rec"]              # rec {float} -- Longitud del recubrimiento del dado [m]
            ancho_aleta = info_cargas.get_ancho_aleta_conector_cortante(torre)
            TP = 2 * (1.5 * ancho_aleta + d_agg + d_b_long + d_b_trans + rec)
            TP = math.ceil(TP * 10) / 10         # Aproximación a la décima por arriba

    # Espesor del dado [m]
    if usar_h_de_grupo:
        H = H_grupo
    else:
        H = parametros['h']                       
        usar_H = parametros['usar_h']
        if not usar_H:
            H = max(H, TP / 2)
    
    C = D + HG - H
    
    # Inclinación del terreno
    ω = torre.inclinacion_terreno or 0        
    
    # Inclinación de la base de la zapata
    α = torre.inclinacion_base_zapata or 0        

    return   Zapata(B, B, D, H, C, TP, θ, γ_c, perfil_ajustado, α, ω)

if __name__ == "__main__":
    main()