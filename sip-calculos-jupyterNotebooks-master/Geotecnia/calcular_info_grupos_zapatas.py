import math
import sys
from cimentaciones.data_services import DataServices
from cimentaciones.perfil import Perfil, obtener_perfil
from cimentaciones.cargas import Cargas
from cimentaciones.zapata import Zapata
from cimentaciones.util import γ_agua, generar_serie
from cimentaciones.parametros_zapata import get_parametros_default

def main():
    #conn_string = "host=p1378.concol.com dbname=sip_db user=test_user password=test_user"
    conn_string = "host=localhost dbname=sip_db user=postgres password=Magnus64"
    esquema = "cll_dlt_gtc"
    corrida_id = 183
    parametros = get_parametros_default()
    lista_HG = parametros["lista_hg"]
    data_services = DataServices(conn_string, esquema) 
    info_cargas = Cargas(data_services)
    torres = data_services.listar_torres_obj()
    agrupaciones = data_services.listar_grupos_zapatas()    
    for grupo in agrupaciones:
        tipo = grupo["tipo"]
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

        grupo_info = {}
        grupo_info["zapata_corrida_id"] = corrida_id
        grupo_info["tipo"] = tipo
        grupo_info["concreto"] = grupo["concreto"]
        grupo_info["orden"] = None
        grupo_info["b"] = B
        grupo_info["d"] = D
        grupo_info["cantidad"] = len(grupo["torres"])
        grupo_info["porc_sobrecosto"] = None
        grupo_info["vol_optimos"] = None
        grupo_info["vol_grupo"] = None
        grupo_info["porc_sobrecosto_max"] = None
        grupo_info["qs"] = qs
        grupo_info["relleno"] = {"φ_r": φ_r, "c_u_r": c_u_r, "γ_r": γ_r}
        grupo_info["geometrias"] = {"TP_min" : min(TPs), "TP_max": max(TPs), "H_min": min(Hs), "H_max": max(Hs)}
        grupo_info["torres_cubiertas"] = [{"nombre": nombre } for nombre in grupo["torres"]]
        data_services.guardar_zapata_corrida_grupo(grupo_info)

        print(grupo_info["tipo"], grupo_info["b"], grupo_info["d"], "->", grupo_info["cantidad"])
        #input("...")





def crear_zapata(torre, perfil, info_cargas, parametros, B, D, HG):
    profundidad_roca = perfil.calcular_profundidad_hasta_roca()    
    if profundidad_roca and D > profundidad_roca:
        return None

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
        perfil_ajustado = perfil.clonar_saturado()
        γ_c_ajustado = γ_c - γ_agua
    else:
        perfil_ajustado = perfil
        γ_c_ajustado = γ_c

    # Inclinación del terreno
    ω = torre.inclinacion_terreno or 0        
    
    # Inclinación de la base de la zapata
    α = torre.inclinacion_base_zapata or 0        

    return   Zapata(B, B, D, H, C, TP, θ, γ_c_ajustado, perfil_ajustado, α, ω)


if __name__ == "__main__":
    main()