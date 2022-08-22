import math
import sys
import copy
import time
from cimentaciones.data_services import DataServices
from cimentaciones.util import γ_agua, generar_serie,format_duracion
from cimentaciones.cargas import Cargas
from cimentaciones.zapata import Zapata
from cimentaciones.parametros_zapata import get_parametros_default
from cimentaciones.perfil import Perfil, obtener_perfil

def main():
    start_time = time.time()

    #conn_string = "host=p1378.concol.com dbname=sip_db user=test_user password=test_user"
    conn_string = "host=localhost dbname=sip_db user=postgres password=Magnus64"
    esquema = "cll_dlt_gtc"
    corrida_id = 306
    parametros = get_parametros_default()    
    lista_HG = parametros["lista_hg_esp"]
    porc_sobrecosto_max = 20
    porc_sobrecosto_max_pocas = 60
    umbral = 10
    if porc_sobrecosto_max_pocas and umbral:
        escenario = f"{porc_sobrecosto_max}%-{umbral}-{porc_sobrecosto_max_pocas}%"
    else:
        escenario = f"{porc_sobrecosto_max}%"

    guardar_corrida = True

    data_services = DataServices(conn_string, esquema)
    listado_torres = data_services.listar_torres_obj()
    conjuntos = data_services.listar_conjuntos_zapatas_a_agrupar(corrida_id)

    for conjunto in conjuntos:
        start_time_conjunto = time.time()
        print(f"Conjunto {conjunto['tipo']}, {conjunto['resistencia_min_conc']}, {conjunto['relacion_a_mc_max']},  {conjunto['cant']} Torres", flush=True)

        # Guardar resultados en temporal
        data_services.guardar_resultados_zapatas_en_temp(corrida_id, conjunto["tipo"], conjunto["resistencia_min_conc"], conjunto["relacion_a_mc_max"])
        concreto_desc = f"{conjunto['resistencia_min_conc']}Mpa - rel a/mc: {conjunto['relacion_a_mc_max']}"
        torres_cubiertas = []

        # Selección de grupos
        grupos = []
        orden = 1
        while True:
            if porc_sobrecosto_max_pocas and umbral:
                porc_sobrecosto_max_sel = porc_sobrecosto_max if conjunto['cant'] - len(torres_cubiertas) > umbral else porc_sobrecosto_max_pocas
            else:
                porc_sobrecosto_max_sel = porc_sobrecosto_max
            grupos_posibles = data_services.listar_grupos_zapata_posibles(torres_cubiertas) 
            if (len(grupos_posibles) == 0):
                break       
            cobertura_grupo, b_grupo, d_grupo, costo_grupo, costo_optimo_grupo, sobrecosto_grupo, torres_grupo = 0, None, None, 999999999999, 999999999999, 999999999999, None
            for grupo_posible in grupos_posibles:
                b, d = float(grupo_posible["b"]), float(grupo_posible["d"])
                record = data_services.calcular_grupo_zapatas_cobertura_sobrecosto(b, d, porc_sobrecosto_max_sel, torres_cubiertas)
                cobertura, costo, costo_optimo, sobrecosto, torres = record["cobertura"], record["costo"], record["costo_optimo"], record["sobrecosto"], record["torres"]
                if cobertura > 0:
                    if (cobertura, -sobrecosto) > (cobertura_grupo, -sobrecosto_grupo):
                        cobertura_grupo, b_grupo, d_grupo, costo_grupo, costo_optimo_grupo, sobrecosto_grupo, torres_grupo = cobertura, b, d, costo, costo_optimo, sobrecosto, torres
            grupo = {"zapata_corrida_id": corrida_id,
                    "tipo": conjunto["tipo"], 
                    "concreto":  concreto_desc, 
                    "orden": orden, 
                    "b": b_grupo, 
                    "d": d_grupo, 
                    "cobertura": cobertura_grupo, 
                    "costo": round(costo_grupo,2), 
                    "costo_optimo": round(costo_optimo_grupo,2), 
                    "porc_sobrecosto": round((costo_grupo - costo_optimo_grupo)/costo_optimo_grupo * 100,1), 
                    "porc_sobrecosto_max": porc_sobrecosto_max_sel,
                    "torres": torres_grupo}
            agregar_info_a_grupo(data_services, corrida_id, grupo, listado_torres, lista_HG)
            grupos.append(grupo)
            if guardar_corrida:
                data_services.guardar_zapata_corrida_grupo2(grupo, escenario)
            torres_cubiertas += torres_grupo
            orden += 1
            print(f"Grupo B:{grupo['b']}, D:{grupo['d']}, cobertura: {grupo['cobertura']}, costo: {grupo['costo']}, costo_optimo: {grupo['costo_optimo']}, porc_sobrecosto: {grupo['porc_sobrecosto']}%, torres: {len(grupo['torres'])}", flush=True)
    
        end_time_conjunto = time.time()
        duracion_conjunto = end_time_conjunto - start_time_conjunto    
        print(format_duracion(duracion_conjunto))
    
    end_time = time.time()
    duracion = end_time - start_time    
    print(format_duracion(duracion))

def agregar_info_a_grupo(data_services, corrida_id, grupo, torres, lista_HG):
    parametros = get_parametros_default()
    info_cargas = Cargas(data_services)

    B = grupo["b"]
    D = grupo["d"]
    qs = {}
    for HG in lista_HG:
        qs[HG] = {"Q_max_d": sys.float_info.min, "Q_min_d": sys.float_info.min, 
                "Q_max_t": sys.float_info.min, "Q_min_t": sys.float_info.min, "q_ult": sys.float_info.max}
    TPs = []
    Hs = []
    materiales_relleno = []        
    for nombre_torre in grupo["torres"]:
        torre = next(iter([t for t in torres if t.nombre == nombre_torre]))
        perfil, error_en_perfil, mensaje_error = obtener_perfil(data_services, vars(torre))
        if error_en_perfil:
            raise ValueError(mensaje_error)
        for HG in lista_HG:
            zapata = crear_zapata(torre, perfil, info_cargas, parametros, B, D, HG)
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
    grupo["qs"] = qs
    grupo["relleno"] = {"φ_r": φ_r, "c_u_r": c_u_r, "γ_r": γ_r}
    grupo["geometrias"] = {"TP_min" : min(TPs), "TP_max": max(TPs), "H_min": min(Hs), "H_max": max(Hs)}

def crear_zapata(torre, perfil, info_cargas, parametros, B, D, HG):
    perf_roca_min = parametros["perf_roca_min"]                    # perf_roca_min {float} -- Perforación mínima de la zapata a la roca [m]
    perf_roca_max = parametros["perf_roca_max"]                    # perf_roca_max {float} -- Perforación máxima de la zapata a la roca [m]
    dist_atraccion_roca = parametros["dist_atraccion_roca"]        # dist_atraccion_roca {float} -- Distancia a la roca, a partir de la cual debe penetrar la zapata [m]
    perfil_ajustado = perfil
    profundidad_roca = perfil.calcular_profundidad_hasta_roca()    
    if profundidad_roca:
        perf_roca = round(D - profundidad_roca, 2)
        if perf_roca > perf_roca_max:
            return None
        elif perf_roca >= -dist_atraccion_roca:
            if perf_roca < perf_roca_min:
                perf_roca = perf_roca_min
                D = profundidad_roca + perf_roca_min
            perfil_ajustado = copy.deepcopy(perfil)
            perfil_ajustado.extender_suelo_a_roca(perf_roca)

    # Peso unitario de la cimentación. Se corrige más adelante por saturación. [kN/m³]
    γ_c = parametros["gamma_c"]

    # Ángulo del pedestal con respecto a la vertical [°]                        
    θ = info_cargas.get_angulo_inclinacion(torre)    

    # TP: Lado correspondiente a la sección transversal del pedestal [m]    
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
    H = parametros['h']                       
    usar_H = parametros['usar_h']
    if not usar_H:
        H = max(H, TP / 2)
    
    C = D + HG - H
    
    NF = perfil.calcular_NF()
    if NF and NF < D:
        perfil_ajustado = perfil_ajustado.clonar_saturado()
        γ_c_ajustado = γ_c - γ_agua
    else:
        γ_c_ajustado = γ_c

    # Inclinación del terreno
    ω = torre.inclinacion_terreno or 0        
    
    # Inclinación de la base de la zapata
    α = torre.inclinacion_base_zapata or 0        

    return   Zapata(B, B, D, H, C, TP, θ, γ_c_ajustado, perfil_ajustado, α, ω)

if __name__ == "__main__":
    main()