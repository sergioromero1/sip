import math
import sys
from typing import List, Dict, Tuple, Any
from operator import itemgetter
from cimentaciones.data_services import DataServices
from cimentaciones.perfil import Perfil, obtener_perfil
from cimentaciones.cargas import Cargas
from cimentaciones.zapata import Zapata
from cimentaciones.util import γ_agua, generar_serie
from cimentaciones.parametros_zapata import get_parametros_default

def main():
    # Inputs
    corrida_id = 135
    tipo = '(D100|DT100)'
    tipo_cemento = 'UG'
    resistencia_concreto = 28
    relacion_agua_cemento = 0.45
    concreto = f"tipo = {tipo_cemento}, f'c = {resistencia_concreto} MPa, rel a/c = {relacion_agua_cemento}"
    sobrecosto_max = 10
    hg = 2.0

    print("Corrida: {}, Tipo: {}, Concreto: {}, Sobrecosto máx: {}".format(corrida_id, tipo, concreto, sobrecosto_max))

    #conn_string = "host=p1378.concol.com dbname=sip_db user=test_user password=test_user"
    conn_string = "host=localhost dbname=sip_db user=postgres password=Magnus64"
    esquema = "cll_dlt_gtc"
    data_services = DataServices(conn_string, esquema) 
    parametros = get_parametros_default()
    b_ini = parametros["b_min"]        # B_min {float} -- Valor mínimo para las iteraciones de ancho de la zapata B [m]
    b_fin = parametros["b_max"]        # B_max {float} -- Valor máximo para las iteraciones de ancho de la zapata B [m]
    b_paso = parametros["b_paso"]      # B_paso {float} -- Incremento para las iteraciones de ancho de la zapata B [m]
    d_ini = parametros["d_min"]        # D_min {float} -- Valor mínimo para las iteraciones de la profundidad de la zapata D [m]
    d_fin = parametros["d_max"]        # D_max {float} -- Valor máximo para las iteraciones de la profundidad de la zapata D [m]
    d_paso = parametros["d_paso"]      # D_paso {float} -- Incremento para las iteraciones de la profundidad de la zapata D [m]
    
    geometrias = data_services.listar_geometrias_zapata_por_tipo_torre(tipo)
    tp, h, theta = float(geometrias["tp"]), float(geometrias["h"]), float(geometrias["theta"])
    
    casos = data_services.listar_agrupacion_soluciones_corrida_zapata_por_b_d(corrida_id, tipo, resistencia_concreto, relacion_agua_cemento)
    if len(casos) > 0:
        disenos = []
        for b in generar_serie(b_ini, b_fin, b_paso, 2):
            for d in generar_serie(d_ini, d_fin, d_paso, 2):
                disenos.append((b, d))

        soluciones = []
        orden = 1
        while len(casos) > 0:
            candidatos = []        
            for diseno in disenos:
                b, d = diseno
                cobertura, sobrecosto, vol_pond_total, vol_pond_bd_total = calcular_cobertura_y_sobrecosto(b, d, h, hg, tp, theta, casos, sobrecosto_max)
                if (cobertura > 0):
                    candidatos.append((diseno, cobertura, -sobrecosto, vol_pond_total, vol_pond_bd_total))
            # selecciona el candidato que maximiza la cobertura y, en caso de empate, el -sobrecosto
            candidatos = sorted(candidatos, key=itemgetter(1, 2))
            escogido = candidatos[-1]

            casos = eliminar_casos(casos, escogido[0])
            disenos = eliminar_disenos(disenos, escogido[0])
            soluciones.append({
                                "zapata_corrida_id": corrida_id,
                                "tipo": tipo,
                                "concreto": concreto,
                                "orden": orden,
                                "b": escogido[0][0],
                                "d": escogido[0][1],
                                "cantidad": escogido[1],
                                "porc_sobrecosto": -escogido[2],
                                "vol_optimos": escogido[3],
                                "vol_grupo": escogido[4],
                                "porc_sobrecosto_max": sobrecosto_max
                        })
            orden += 1
        
        print("Torres en los grupos: {}".format(sum([solucion["cantidad"] for solucion in soluciones])))

        info_cargas = Cargas(data_services)
        torres = data_services.listar_torres_corrida_zapata(corrida_id, tipo, resistencia_concreto, relacion_agua_cemento)

        lista_HG = parametros["lista_hg"]
        for solucion in soluciones:
            B, D = float(solucion["b"]), float(solucion["d"])

            # Encuentra las torres cubiertas por esta solución   
            torres_cubiertas = [torre for torre in torres if float(torre["b"]) <= B and float(torre["d"]) <= D]
            if len(torres_cubiertas) != solucion["cantidad"]:
                raise ValueError("No coinciden las torres cubiertas de la agrupación con el del procesamiento individual en grupo {}. {} <> {} ".format(solucion["orden"], solucion["cantidad"], len(torres_cubiertas)))
            solucion["torres_cubiertas"] = torres_cubiertas
            
            # Resta las torres ya cubiertas de la lista de torres
            torres = [torre for torre in torres if float(torre["b"]) > B or float(torre["d"]) > D] 
            
            qs = {}
            for HG in lista_HG:
                qs[HG] = {"Q_max_d": sys.float_info.min, "Q_min_d": sys.float_info.min, 
                        "Q_max_t": sys.float_info.min, "Q_min_t": sys.float_info.min, "q_ult": sys.float_info.max}
            TPs = []
            Hs = []
            materiales_relleno = []
            for torre in torres_cubiertas:
                perfil, error_en_perfil, mensaje_error = obtener_perfil(data_services, torre)
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

            solucion["qs"] = qs
            
            # Material de relleno
            cohesivos = [mat for mat in materiales_relleno if mat["tipo_mat"] == "c"]
            granulares= [mat for mat in materiales_relleno if mat["tipo_mat"] == "g"]
            φ_r = 0 if len(granulares) == 0 else sum([mat["φ"] for mat in granulares]) / len(granulares)
            c_u_r = 0 if len(cohesivos) == 0 else sum([mat["c_u"] for mat in cohesivos]) / len(cohesivos)
            γ_r = 0 if len(materiales_relleno) == 0 else sum([mat["γ"] for mat in materiales_relleno]) / len(materiales_relleno)
            solucion["relleno"] = {"φ_r": φ_r, "c_u_r": c_u_r, "γ_r": γ_r}

            # Geometrías
            solucion["geometrias"] = {"TP_min" : min(TPs), "TP_max": max(TPs), "H_min": min(Hs), "H_max": max(Hs)}


            data_services.guardar_zapata_corrida_grupo(solucion)


def crear_zapata(torre, perfil, info_cargas, parametros, B, D, HG):
    γ_c = parametros["gamma_c"]                   # Peso unitario de la cimentación. Se corrige más adelante por saturación. [kN/m³]
    θ = info_cargas.get_angulo_inclinacion(torre) # Ángulo del pedestal con respecto a la vertical [°]    
    usar_TP = parametros["usar_tp"] # 
    if usar_TP:
        dict_TP = parametros["dict_tp"]
        TP = dict_TP[torre["tipo"]]
    else:
        d_agg = parametros["d_agg"]          # Tamaño máximo nominal del agregado grueso [m]
        d_b_long = parametros["d_b_long"]    # Diámetro de barras de refuerzo longitudinal [m]
        d_b_trans = parametros["d_b_trans"]  # Diámetro de barras de refuerzo transversal [m]
        rec = parametros["rec"]              # Longitud del recubrimiento del dado [m]
        ancho_aleta = info_cargas.get_ancho_aleta_conector_cortante(torre)
        TP = 2 * (1.5 * ancho_aleta + d_agg + d_b_long + d_b_trans + rec)
    
    H = parametros['h']                       # Espesor del dado [m]
    usar_H = parametros['usar_h']
    if not usar_H:
        H = max(H, TP / 2)
    
    C = D + HG - H
    
    # pvs = info_cargas.get_proyeccion_vertical_stub(torre) # Proyección vertical del stub
    # if C < pvs + 0.15 - H:
    #     return None

    NF = perfil.calcular_NF()
    if NF and NF < D:
        perfil_ajustado = perfil.clonar_saturado()
        γ_c_ajustado = γ_c - γ_agua
    else:
        perfil_ajustado = perfil
        γ_c_ajustado = γ_c

    return Zapata(B, B, D, H, C, TP, θ, γ_c_ajustado, perfil_ajustado, 0, 0)

def calcular_esfuerzo_actuante_sobre_suelo_y_capacidad_portante(zapata: Zapata, cargas_diseno: List[float], cargas_trabajo: List[float]):
    F_zc, F_xc, F_yc = cargas_diseno
    Q_max, Q_min, _ = zapata.calculo_esfuerzo_actuante_sobre_suelo(F_xc, F_yc, F_zc)
    F_zc, F_xc, F_yc = cargas_trabajo
    T = max(F_xc, F_yc)
    q_ult, _ = zapata.calculo_capacidad_portante(T, F_zc)
    return Q_max, Q_min, q_ult

def eliminar_casos(casos, diseno_escogido):
    return [caso for caso in casos if round(float(caso["b"]),1) > round(diseno_escogido[0],1) or round(float(caso["d"]),1) > round(diseno_escogido[1],1)]

def eliminar_disenos(disenos, diseno_escogido):
    return [diseno for diseno in disenos if round(diseno[0],1) > round(diseno_escogido[0],1) or round(diseno[1],1) > round(diseno_escogido[1],1)]

def calcular_cobertura_y_sobrecosto(b, d, h, hg, tp, theta, casos, sobrecosto_max):
    casos_cubiertos = [caso for caso in casos if round(float(caso["b"]),1) <= round(b,1) and round(float(caso["d"]),1) <= round(d,1)]
    if len(casos_cubiertos) > 0:
        cobertura = sum([caso["cantidad"] for caso in casos_cubiertos])
        vol_pond_bd = calcular_volumen_ponderado(b, d, h, hg, tp, theta )
        vol_pond_bd_total = cobertura * vol_pond_bd
        vol_pond_total = sum([calcular_volumen_ponderado(float(caso["b"]), float(caso["d"]), h, hg, tp, theta ) * caso["cantidad"] for caso in casos_cubiertos])
        sobrecosto = (vol_pond_bd_total - vol_pond_total) / vol_pond_total * 100
        if sobrecosto <= sobrecosto_max:
            return cobertura, sobrecosto, vol_pond_total, vol_pond_bd_total
        else:
            return 0, 0, 0, 0
    else:
        return 0, 0, 0, 0

def calcular_volumen_ponderado(b, d, h, hg, tp, theta ):
    vol_conc = b**2*h + tp**2*(d + hg - h)/math.cos(math.radians(theta))
    vol_rell = b**2*(d - h) - tp**2*(d - h)/math.cos(math.radians(theta))
    return (4 * vol_conc + vol_rell) / 5

def imprimir_casos(text_file, casos):
    text_file.write("casos:\n")
    for caso in casos:
        text_file.write("{}, {}, {}\n".format(caso["b"], caso["d"], caso["cantidad"]))

def imprimir_disenos(text_file, disenos):
    text_file.write("diseños:\n")
    for diseno in disenos:
        text_file.write("{}, {}\n".format(diseno[0], diseno[1]))

def imprimir_candidatos(text_file, candidatos):
    text_file.write("candidatos:\n")
    for candidato in candidatos:
        text_file.write("{}, {}, {}, {}\n".format(candidato[0][0], candidato[0][1], candidato[1], candidato[2]))

def imprimir_escogido(text_file, escogido):
    text_file.write("escogido:\n")
    text_file.write("{}, {}, {}, {}\n".format(escogido[0][0], escogido[0][1], escogido[1], escogido[2]))


if __name__ == "__main__":
    main()