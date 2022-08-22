import sys
import math
import copy
import json
from cimentaciones.parametros_zapata import get_parametros_default
from cimentaciones.data_services import DataServices
from cimentaciones.evaluador_zapatas import EvaluadorZapatas
from cimentaciones.util import γ_agua, generar_serie,format_duracion
from cimentaciones.cargas import Cargas
from cimentaciones.zapata import Zapata
from cimentaciones.perfil import Perfil, obtener_perfil

def main():
    conn_string = "host=localhost dbname=sip_db user=postgres password=Magnus64"
    esquema = "cll_dlt_gtc"
    parametros = get_parametros_default()
    
    # conjunto = "200630-PED-ESP"
    # lista_HG = [3.0, 4.0, 5.0, 6.0, 7.0]
    
    conjunto = "200716"
    lista_HG = parametros["lista_hg"] 
    
    data_services = DataServices(conn_string, esquema)
    info_cargas = Cargas(data_services)
    torres = data_services.listar_torres_obj()
    grupos = data_services.listar_zapata_grupo(conjunto)
    evaluador = EvaluadorZapatas()
    guardar_corrida = True

    γ_r = 16.4

    nombre_corrida = "Validación del conjunto " + conjunto
    corrida_id = None
    if guardar_corrida:
        corrida_id = data_services.guardar_corrida_zapata({"nombre": nombre_corrida}, parametros)
    print(f"Corrida creada. id: {corrida_id} - {nombre_corrida}", flush=True )

    for grupo in grupos:
        validar_grupo(data_services, grupo, torres, info_cargas, parametros, γ_r, evaluador, lista_HG, guardar_corrida, corrida_id)

def validar_grupo(data_services, grupo, torres, info_cargas, parametros, γ_r, evaluador, lista_HG, guardar_corrida, corrida_id ):
    # Factores de seguridad y restricciones
    FSC = parametros['fsc']                  # FSC {float} -- Factore de seguridad a compresión
    FST_g = parametros['fst_g']              # FST_g {float} -- Factor de seguridad a tensión suelo granular
    FST_c = parametros['fst_c']              # FST_c {float} -- Factor de seguridad a tensión suelo cohesivo
    FSV = parametros['fsv']                  # FSV {float} -- Factor de seguridad para volcamiento
    FSL = parametros['fsl']                  # FSL {float} -- Factor de seguridad para cargas laterales
    k = parametros['k']                      # k {int} -- Número de segmentos para análisis de asentamiento  
    t = parametros['t']                      # t {int} -- Número de años para corrección 'Creep'
    S_max_adm_c = parametros['s_max_adm_c']  # S_max_adm_c {float} -- Asentamiento máximo permitido suelos granulares [m]
    S_max_adm_g = parametros['s_max_adm_g']  # S_max_adm_g {float} -- Asentamiento máximo permitido suelos cohesivos [m]

    B = grupo["b"]
    D = grupo["d"]
    H = grupo["h_grupo"]
    TP = grupo["tp_grupo"]

    print("id:", grupo["id"], "tipo:", grupo["tipo"], "concreto:", grupo["concreto"], "B:", grupo["b"], "D:", grupo["d"], "cantidad:", grupo["cantidad"])

    for nombre_torre in grupo["torres"].split(","):
        print(nombre_torre)
        torre = next(iter([t for t in torres if t.nombre == nombre_torre]))

        torre.gamma_r = γ_r

        # valida profundidad mínima de desplante
        if torre.prof_min_desplante and D < torre.prof_min_desplante:
            print("\t", torre.nombre, "No cumple")
            print(f"\t\tD: {D} del grupo es menor que la profundidad mínima de desplante de la torre: {torre.prof_min_desplante}")

        perfil, error_en_perfil, mensaje_error = obtener_perfil(data_services, vars(torre))
        if error_en_perfil:
            raise ValueError(mensaje_error)

        cargas = info_cargas.obtener_cargas_as_dict(torre)

        for HG in lista_HG:
            zapata = crear_zapata(torre, perfil, info_cargas, parametros, B, D, HG, H, TP)
            if zapata:
                try:
                    evaluacion = evaluador.evaluar(zapata, torre, zapata.perfil, info_cargas, FSC, FST_g, FST_c, k, t, S_max_adm_c, S_max_adm_g, FSV, FSL)
                    if guardar_corrida:
                        resultado = {"B": zapata.B, "D": zapata.D, "HG": round(zapata.HG,2), "TP": zapata.TP, "θ": zapata.θ, "α": zapata.α, "ω": zapata.ω, "error": False, "mensaje_error": None}  
                        resultado["cumple"] = all([evaluacion[key]["cumple"] for key in evaluacion])
                        resultado["evaluacion"] = evaluacion
                        resultado["H"] = zapata.H
                        resultado["volumen_zapata"] = zapata.volumen()
                        resultado["volumen_relleno"] = zapata.volumen_relleno()
                        resultado["volumen_ponderado"] = (zapata.volumen() * 4 + zapata.volumen_relleno())/5
                        resultado["esbeltez"] = zapata.D / zapata.B
                        resultado["relleno"] = perfil.calcular_material_relleno(zapata.D - zapata.H)
                        #resultado["parametros_suelo"] = self.calcular_parametros_generales_suelo(resultado["evaluacion"])
                        data_services.guardar_corrida_zapata_torre(corrida_id, torre, perfil, cargas, error_en_perfil, mensaje_error,  [resultado])
                    cumple = all([evaluacion[key]["cumple"] for key in evaluacion])
                    
                    # mt = evaluacion["cap_port-comp_max"]["memoria_Q"]["MT"]
                    # mt_o = evaluacion["cap_port-comp_max"]["memoria_Q"]["MT_o"]
                    # ml = evaluacion["cap_port-comp_max"]["memoria_Q"]["ML"]
                    # ml_o = evaluacion["cap_port-comp_max"]["memoria_Q"]["ML_o"]                    
                    # print("cap_port-comp_max", mt, mt_o, ml, ml_o)

                    # mt = evaluacion["cap_port-long_max"]["memoria_Q"]["MT"]
                    # mt_o = evaluacion["cap_port-long_max"]["memoria_Q"]["MT_o"]
                    # ml = evaluacion["cap_port-long_max"]["memoria_Q"]["ML"]
                    # ml_o = evaluacion["cap_port-long_max"]["memoria_Q"]["ML_o"]                    
                    # print("cap_port-long_max", mt, mt_o, ml, ml_o)

                    if not cumple:
                        #print(json.dumps(evaluacion))
                        #input("...")
                        print("\t", torre.nombre, HG, "No cumple")
                        for eval_key in evaluacion:
                            if not evaluacion[eval_key]["cumple"]:
                                # print("\t\t", eval_key, evaluacion[eval_key]["fs_Q_max"])
                                if eval_key.find("cap_port") != -1:
                                    print("\t\t", eval_key, evaluacion[eval_key]["fs_Q_max"])
                                else:
                                    print("\t\t", eval_key, evaluacion[eval_key]["fs"])
                except Exception as ex:
                    print(str(ex))
                        
def crear_zapata(torre, perfil, info_cargas, parametros, B, D, HG, H, TP):
    perf_roca_min = parametros["perf_roca_min"]                    # perf_roca_min {float} -- Perforación mínima de la zapata a la roca [m]
    perf_roca_max = parametros["perf_roca_max"]                    # perf_roca_max {float} -- Perforación máxima de la zapata a la roca [m]
    dist_atraccion_roca = parametros["dist_atraccion_roca"]        # dist_atraccion_roca {float} -- Distancia a la roca, a partir de la cual debe penetrar la zapata [m]    
    perfil_ajustado = perfil
    profundidad_roca = perfil.calcular_profundidad_hasta_roca()   
    if profundidad_roca:
        perf_roca = round(D - profundidad_roca, 2)
        if perf_roca > perf_roca_max:
            raise ValueError(f"Zapata sobrepasa la perforación máxima en roca. D: {D}. profundidad roca: {profundidad_roca}, perforación máxima permitida: {perf_roca_max}")
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
    if NF and NF < D:
        perfil_ajustado = perfil_ajustado.clonar_saturado()
        γ_c_ajustado = γ_c - γ_agua
        ajuste_saturacion_perfil = True
    else:
        γ_c_ajustado = γ_c
        ajuste_saturacion_perfil = False

    # Ángulo del pedestal con respecto a la vertical [°]                        
    θ = info_cargas.get_angulo_inclinacion(torre)    


    # TP: Lado correspondiente a la sección transversal del pedestal [m]    
    if TP is None:
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
    if H is None:
        H = parametros['h']
        usar_H = parametros['usar_h']
        if not usar_H:
            H = max(H, TP / 2)


    # Proyección vertical del stub
    pvs = info_cargas.get_proyeccion_vertical_stub(torre)

    rec_fondo_stub = parametros['rec_fondo_stub']     
    
    C = D + HG - H

    if C < pvs + rec_fondo_stub - H:
        raise ValueError(f"Falla por stub")    
    
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

    return  Zapata(B, B, D, H, C, TP, θ, γ_c_ajustado, perfil_ajustado, α, ω)

if __name__ == "__main__":
    main()