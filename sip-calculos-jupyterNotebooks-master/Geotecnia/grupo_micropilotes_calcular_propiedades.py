import math
import sys
import copy
import time
import json
from cimentaciones.data_services import DataServices
from cimentaciones.util import γ_agua, generar_serie,format_duracion
from cimentaciones.cargas import Cargas
from cimentaciones.barra import Barra
from cimentaciones.micropilotes import Micropilotes
from cimentaciones.parametros_micropilotes import get_parametros_default
from cimentaciones.perfil import Perfil, obtener_perfil
from cimentaciones.util import γ_agua, generar_serie, tan_g, π
from cimentaciones.evaluador_micropilotes import EvaluadorMicropilotes

def main():
    conn_string = "host=localhost dbname=sip_db user=postgres password=Magnus64"
    esquema = "cll_dlt_gtc"
    # conjunto = "IGU-c_cob-15%-i17a-r"
    # conjunto = "IGU-c_cob_lc-15%-i24a-r"
    # conjunto = 'IRS-c_cob-15%-i18'
    conjunto = "IGU-PED-ESP-200730"
    # conjunto = "IRS-PED-ESP-200801"
    usar_h_tp_de_grupo = False
    usar_tabla_α_exp = False
    α_exp = 1.0    
    parametros = get_parametros_default()
    # lista_HG = parametros["lista_hg"]
    lista_HG = [4.0, 5.0, 6.0, 7.0, 8.0]

    
    data_services = DataServices(conn_string, esquema)
    
    info_cargas = Cargas(data_services)

    torres = data_services.listar_torres_obj()

    evaluador = EvaluadorMicropilotes()

    grupos = data_services.listar_micropilotes_grupo(conjunto)
    for grupo in grupos:
        # if grupo["id"] != 2097:
        #     continue
        agregar_info_a_grupo(data_services, grupo, torres, info_cargas, parametros, usar_h_tp_de_grupo, lista_HG, usar_tabla_α_exp, α_exp, evaluador)
        data_services.actualizar_micropilotes_grupo(grupo)
        print(grupo["grupo"])
    print("Done")

def agregar_info_a_grupo(data_services, grupo, torres, info_cargas, parametros, usar_h_tp_de_grupo, lista_HG, usar_tabla_α_exp, α_exp, evaluador):
    info_barras = parametros["lista_barras"]              # lista_barras {List[Barra]} -- Lista de barras
    proc_iny = grupo["proc_iny"]
    nombre_barra = grupo["nombre_barra"]
    N_m = int(grupo["n_m"])
    D_p = float(grupo["d_p"])
    B = float(grupo["b"])
    D_f = float(grupo["d_f"])
    hs_grupo = (grupo["hs_grupos"])
    lista_barras = [Barra(b["nombre"], b["D"], b["D_int"], b["area"], b["f_y"], b["precio"], b["geoms"]) for b in info_barras]
    barra = next(b for b in lista_barras if b.nombre == nombre_barra)
    H_grupo = None if grupo["h_grupo"] is None else  float(grupo["h_grupo"])
    if usar_h_tp_de_grupo and H_grupo is None:
        h_min = grupo["h_min"]
        h_max = grupo["h_max"]
        if h_min == h_max:
            H_grupo = h_min
        else:
            raise ValueError(f"No puede establecer H de grupo. {grupo}")
    TP_grupo = None if grupo["tp_grupo"] is None else  float(grupo["tp_grupo"])
    if usar_h_tp_de_grupo and TP_grupo is None:
        raise ValueError(f"No puede establecer TP de grupo. {grupo['grupo']}")
    
    geometrias = {}
    maximos = {}
    for HG in lista_HG:
        maximos[HG] = {"Q_med_t": sys.float_info.min, "P_mp_comp_t": sys.float_info.min, "P_mp_tens_t": sys.float_info.min,
                        "Q_med_d": sys.float_info.min, "P_mp_comp_d": sys.float_info.min, "P_mp_tens_d": sys.float_info.min }
    TPs = []
    Hs = []
    S_m = grupo["s_m"]
    S_em = None
    materiales_relleno = []
    for nombre_torre in grupo["torres"].split(","):
        torre = next(iter([t for t in torres if t.nombre == nombre_torre]))        
        perfil, error_en_perfil, mensaje_error = obtener_perfil(data_services, vars(torre))
        print(torre.nombre)
        if error_en_perfil:
            raise ValueError(mensaje_error)
        for HG in lista_HG:
            anclaje_segun_barra = next(iter([geom["anclaje"] for geom in barra.geoms if geom["hg"]==HG]))
            anclaje_segun_grupo = float(grupo["anclaje"])
            L_b = float(grupo["l_b"]) + anclaje_segun_barra

            if hs_grupo is not None:
                H_grupo = hs_grupo[str(HG)]
            
            micropilotes = crear_micropilotes(torre, perfil, info_cargas, parametros, proc_iny, barra, N_m, D_p, L_b, B, D_f, HG, anclaje_segun_grupo, S_m, usar_h_tp_de_grupo, H_grupo, TP_grupo, usar_tabla_α_exp, α_exp)
            
            if not usar_h_tp_de_grupo:
                # Toca llamar al evaluador para para que ajuste el H del micropilote si es necesario
                H_min_barra = next(iter([geom["h_min"] for geom in barra.geoms if geom["hg"]==HG]))
                H_min = max(parametros["h_min"], H_min_barra)
                H_max = parametros["h_max"]
                H_paso = parametros["h_paso"]
                H_relleno_min = parametros["h_relleno_min"]  
                rec = parametros['rec']
                FSCD = parametros['fsc_d']                           
                FSC = parametros['fsc']                              
                FSL = parametros['fsl']                              
                FST = parametros['fst']                              
                k = parametros['k']                                  
                t = parametros['t']                                  
                S_max_adm_g = parametros['s_max_adm_g']              
                S_max_adm_c = parametros['s_max_adm_c']              
                S_max_adm_r = parametros['s_max_adm_r']              
                D_f_max = parametros['d_f_max']                      
                D_f_paso = parametros['d_f_paso']                    
                if usar_tabla_α_exp:
                    tabla_α_exp = parametros['tabla_alfa_exp']                       
                evaluacion=evaluador.evaluar(micropilotes, torre, perfil, info_cargas, H_min, H_max, H_paso, 0, 0, 0, H_relleno_min, FSC, FSCD, FST, k, t, S_max_adm_c, S_max_adm_g, S_max_adm_r, rec, FSL)

            if micropilotes:
                
                S_em = micropilotes.S_em

                if not micropilotes.TP in TPs:
                    TPs.append(micropilotes.TP)

                if not micropilotes.H in Hs:
                    Hs.append(micropilotes.H)
                
                materiales_relleno.append(micropilotes.perfil.calcular_material_relleno(micropilotes.D_f - micropilotes.H))

                # Q_med_d
                F_m, _, _, _ = info_cargas.obtener_cargas_diseno_maxima_compresion_montante(torre)
                Q_med_d = round(((1 - micropilotes.f_carga_mp) * F_m + micropilotes.peso_dado())/(micropilotes.B * micropilotes.L - micropilotes.N_m * π / 4 * micropilotes.D_s **2),2)
                if Q_med_d > maximos[HG]["Q_med_d"]:
                    maximos[HG]["Q_med_d"] = Q_med_d

                # Q_med_t
                F_m, _, _, _ = info_cargas.obtener_cargas_trabajo_maxima_compresion_montante(torre)
                Q_med_t = round(((1 - micropilotes.f_carga_mp) * F_m + micropilotes.peso_dado())/(micropilotes.B * micropilotes.L - micropilotes.N_m * π / 4 * micropilotes.D_s **2),2)
                if Q_med_t > maximos[HG]["Q_med_t"]:
                    maximos[HG]["Q_med_t"] = Q_med_t

                # P_mp_comp_d
                F_m, _, F_hl, F_ht = info_cargas.obtener_cargas_diseno_maxima_compresion_montante(torre)
                P_mp_comp_d = round(micropilotes.calculo_carga_maxima_micropilote(F_m, F_hl, F_ht),2)
                if P_mp_comp_d > maximos[HG]["P_mp_comp_d"]:
                    maximos[HG]["P_mp_comp_d"] = P_mp_comp_d
                    maximos[HG]["M_max"] = evaluacion["camisa"]["M_max"]
                F_m, _, F_hl, F_ht = info_cargas.obtener_cargas_diseno_maxima_lateral_montante(torre)
                P_mp_comp_d = micropilotes.calculo_carga_maxima_micropilote(F_m, F_hl, F_ht)
                if P_mp_comp_d > maximos[HG]["P_mp_comp_d"]:
                    maximos[HG]["P_mp_comp_d"] = P_mp_comp_d
                    maximos[HG]["M_max"] = evaluacion["camisa"]["M_max"]

                # P_mp_comp_t
                F_m, _, F_hl, F_ht = info_cargas.obtener_cargas_trabajo_maxima_compresion_montante(torre)
                P_mp_comp_t = round(micropilotes.calculo_carga_maxima_micropilote(F_m, F_hl, F_ht),2)
                if P_mp_comp_t > maximos[HG]["P_mp_comp_t"]:
                    maximos[HG]["P_mp_comp_t"] = P_mp_comp_t
                F_m, _, F_hl, F_ht = info_cargas.obtener_cargas_trabajo_maxima_lateral_montante(torre)
                P_mp_comp_t = micropilotes.calculo_carga_maxima_micropilote(F_m, F_hl, F_ht)
                if P_mp_comp_t > maximos[HG]["P_mp_comp_t"]:
                    maximos[HG]["P_mp_comp_t"] = P_mp_comp_t

                # P_mp_tens_d
                F_m, _, F_hl, F_ht = info_cargas.obtener_cargas_diseno_maxima_tension_montante(torre)
                P_mp_tens_d = round(micropilotes.calculo_carga_maxima_micropilote_tension(F_m, F_hl, F_ht),2)
                if P_mp_tens_d > maximos[HG]["P_mp_tens_d"]:
                    maximos[HG]["P_mp_tens_d"] = P_mp_tens_d

                # P_mp_tens_t
                F_m, _, F_hl, F_ht = info_cargas.obtener_cargas_trabajo_maxima_tension_montante(torre)
                P_mp_tens_t = round(micropilotes.calculo_carga_maxima_micropilote_tension(F_m, F_hl, F_ht),2)
                if P_mp_tens_t > maximos[HG]["P_mp_tens_t"]:
                    maximos[HG]["P_mp_tens_t"] = P_mp_tens_t
            else:
                raise ValueError("No pudo crear micropilote")

    # Material de relleno
    cohesivos = [mat for mat in materiales_relleno if mat["tipo_mat"] == "c"]
    granulares= [mat for mat in materiales_relleno if mat["tipo_mat"] == "g"]
    φ_r = 0 if len(granulares) == 0 else round(sum([mat["φ"] for mat in granulares]) / len(granulares),2)
    c_u_r = 0 if len(cohesivos) == 0 else round(sum([mat["c_u"] for mat in cohesivos]) / len(cohesivos),2)
    γ_r = 0 if len(materiales_relleno) == 0 else round(sum([mat["γ"] for mat in materiales_relleno]) / len(materiales_relleno),2)
    if usar_h_tp_de_grupo:
        grupo["maximos_grupo"] = json.dumps(maximos)
        grupo["maximos_propio"] = None if grupo["maximos_propio"] is None else json.dumps(grupo["maximos_propio"])
    else:
        grupo["maximos_grupo"] = None if grupo["maximos_grupo"] is None else json.dumps(grupo["maximos_grupo"])
        grupo["maximos_propio"] = json.dumps(maximos)

    grupo["geometrias"] = json.dumps({"TP_min" : min(TPs), "TP_max": max(TPs), "H_min": min(Hs), "H_max": max(Hs), "S_m": S_m, "S_em": S_em})
    grupo["relleno"] = json.dumps({"φ_r": φ_r, "c_u_r": c_u_r, "γ_r": γ_r})

def crear_micropilotes(torre, perfil, info_cargas, parametros, proc_iny, barra, N_m, D_p, L_b, B, D_f, HG, anclaje, S_m, usar_h_tp_de_grupo, H_grupo, TP_grupo, usar_tabla_α_exp, α_exp):
    #
    # Información de Parámetros
    #
    γ_c = parametros['gamma_c']                           # γ_c {float} -- Peso unitario de la cimentación [kN/m³]
    γ_l = parametros['gamma_l']                           # γ_l {float} -- Peso unitario de la lechada del micropilote [kN/m³]
    η = parametros["eta"]                                 # η {float} -- Eficiencia del grupo de micropilotes [-]
    f_pc = parametros["f_pc"]                             # f_pc {float} -- Resistencia a la compresión del concreto [kPa]
    f_py = parametros["f_py"]                             # f_py {float} -- Esfuerzo de fluencia de la barra de refuerzo [kPa]
    A_camisa = parametros["a_camisa"]                     # A_camisa {float} -- Área de la sección de la camisa [m²]
    
    # θ: Ángulo del pedestal con respecto a la vertical [°]
    θ = info_cargas.get_angulo_inclinacion(torre) 
    
    if usar_h_tp_de_grupo:
        TP = TP_grupo
        d_b_long = parametros['d_b_long']   # d_b_long {float} -- Diámetro de barras de refuerzo longitudinal [m]
    else:    
        # TP: Ancho mínimo del pedestal [m], calculado a partir de los parámetros geométricos del pedestal
        d_agg = parametros['d_agg']         # d_agg {float} -- Tamaño máximo nominal del agregado grueso [m]
        d_b_long = parametros['d_b_long']   # d_b_long {float} -- Diámetro de barras de refuerzo longitudinal [m]
        d_b_trans = parametros['d_b_trans'] # d_b_trans {float} -- Diámetro de barras de refuerzo transversal [m]
        rec = parametros['rec']             # rec {float} -- Espesor del recubrimiento [m]
        B_a = info_cargas.get_ancho_aleta_conector_cortante(torre)  # B_a: Ancho de la aleta del conector de cortante del stub [m]
        TP = 2 * (1.5 * B_a + d_agg + d_b_long + d_b_trans + rec)
        TP = math.ceil(TP * 10) / 10 # Aproximación a la décima por arriba

    # Nivel freático incluyendo inundabilidad
    NF = perfil.calcular_NF()

    # Inclinación del terreno
    ω = torre.inclinacion_terreno or 0        
    
    # Inclinación de la base de la zapata
    α = torre.inclinacion_base_zapata or 0        

    # f_carga_mp: Fracción de carga que toman los micropilotes [0..1]
    f_carga_mp = torre.f_carga_mp

    # Se satura todo el perfil si
    # el nivel freático esta por encima de
    # la profundidad de desplante
    if NF is not None and NF < D_f:
        perfil_ajustado = perfil.clonar_saturado()
    else:
        perfil_ajustado = perfil

    if usar_tabla_α_exp:
        tabla_α_exp = parametros['tabla_alfa_exp']        # tabla_α_exp {Dict} -- Diccionario para la evaluación de α_exp : Factor de expansión, con key: (tipo material, procedimiento de inyección)
        tipos_mat = perfil.calcular_tipo_mat_distintos(D_f, D_f + L_b)        
        α_exp = max([tabla_α_exp[(tipo_mat, proc_iny)] for tipo_mat in tipos_mat])                                

    if usar_h_tp_de_grupo:
        H = H_grupo
    else:
        barra_h_min = next(iter([geom["h_min"] for geom in barra.geoms if geom["hg"]==HG]))
        H = max(parametros["h_min"], barra_h_min)

    micropilotes = Micropilotes(D_f, 0.0, HG, H, TP, θ, γ_c, N_m, S_m, L_b - anclaje, barra, D_p, η, proc_iny, f_pc, f_py, A_camisa, d_b_long, perfil_ajustado, α, ω, f_carga_mp, α_exp, γ_l)

    return micropilotes

if __name__ == "__main__":
    main()