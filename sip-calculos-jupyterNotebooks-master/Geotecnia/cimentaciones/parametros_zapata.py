def get_parametros_default():
    parametros = {}
    parametros['n_soluciones'] = 10                     # n_soluciones {int} -- Número de soluciones a conservar para reportes
    parametros['hg_por_pata'] = False                   # hg_por_pata {bool} -- Indica si aparte de la lista de hgs a evaluar, se debe incluir el hg de cada pata
    parametros['b_min'] = 2.0                           # b_min {float} -- Valor mínimo para las iteraciones de ancho de la zapata B [m]
    parametros['b_max'] = 4.5                           # b_max {float} -- Valor máximo para las iteraciones de ancho de la zapata B [m]
    parametros['b_extra'] = None                        # b_extra {float} -- Valor extra de búsqueda para el ancho de la zapata B si no encuentra solución con b_max [m]
    parametros['b_paso'] = 0.1                          # b_paso {float} -- Incremento para las iteraciones de ancho de la zapata B [m]
    parametros['d_min'] = 2.0                           # d_min {float} -- Valor mínimo para las iteraciones de la profundidad de la zapata B [m]
    parametros['d_max'] = 4.0                           # d_max {float} -- Valor máximo para las iteraciones de la profundidad de la zapata B [m]
    parametros['d_paso'] = 0.1                          # d_paso {float} -- Incremento para las iteraciones de la profundidad de la zapata B [m]
    parametros['usar_prof_min_desp_por_torre'] = True   # usar_prof_min_desp_por_torre {bool} -- Indica si se debe tener en cuenta la profundidad mínima de desplante por torre
    parametros['lista_hg'] = [0.25, 0.5, 1.0, 1.5, 2.0] # lista_hg {list} -- Lista de altura de pedestales convencionales a evaluar [m] 
    parametros['lista_hg_esp'] = [3.0, 4.0, 5.0, 6.0, 7.0] # lista_hg_esp {list} -- Lista de altura de pedestales especiales a evaluar [m] 
    parametros['d_agg'] = 0.01905                       # d_agg {float} -- Tamaño máximo nominal del agregado grueso [m]
    parametros['d_b_long'] = 0.01905                    # d_b_long {float} -- Diámetro de barras de refuerzo longitudinal [m]
    parametros['d_b_trans'] = 0.01905                   # d_b_trans {float} -- Diámetro de barras de refuerzo transversal [m]
    parametros['rec'] = 0.05                            # rec {float} -- Longitud del recubrimiento del dado [m]
    parametros['rec_fondo_stub'] = 0.125                # rec_fondo_stub {float} -- Recubrimiento vertical en el fondo de la zapata para el stub [m]    
    parametros['h'] = 0.4                               # h {float} -- Espesor de la zapata [m]
    parametros['usar_h'] = False                        # usar_h {bool} -- Indica si los cálculos deben usar el h indicado o calcular el H mínimo
    parametros['dict_tp'] = {"A100": 0.6,               # dict_tp {dict} -- Lado correspondiente a la sección transversal del pedestal [m]
                            "AL100": 0.6, "AA100": 0.6, "B100": 0.6, 
                            "C100": 0.6, "D100": 0.6, "DT100": 0.6, "TR100": 0.6,
                            "A126": 0.6, "AA126": 0.6, "B126": 0.6, "C126": 0.6,
                            "D126": 0.6, "DT126": 0.6}
    parametros['usar_tp'] = False                        # usar_tp {bool} -- Indica si los cálculos deben usar el tp indicado o calcular el TP mínimo
    parametros['gamma_c'] = 24.0                         # gamma_c {float} -- Peso unitario de la cimentación seco [kN/m³]
    parametros['fsc'] =  3.0                             # fsc {float} -- Factor de seguridad a compresión
    parametros['fst_g'] = 1.5                            # fst_g {float} -- Factor de seguridad a tensión suelo granular
    parametros['fst_c'] = 2.0                            # fst_c {float} -- Factor de seguridad a tensión suelo cohesivo
    parametros['k'] = 80                                 # k {int} -- Número de segmentos para análisis de asentamiento       
    parametros['t'] = 50                                 # t {int} -- Número de años para corrección 'Creep'
    parametros['s_max_adm_g'] = 0.05                     # s_max_adm_g {float} -- Asentamiento máximo permitido suelos granulares [m]
    parametros['s_max_adm_c'] = 0.10                     # s_max_adm_c {float} -- Asentamiento máximo permitido suelos cohesivos [m]
    parametros['fsv'] = 1.5                              # fsv {float} -- Factor de seguridad para volcamiento
    parametros['fsl'] = 1.5                              # fsl {float} -- Factor de seguridad para cargas laterales
    parametros["optimo_por_profundidad"] = True          # optimo_por_profundidad {bool} -- Determina si se quiere optener un solo óptimo por profundidad
    parametros["perf_roca_min"] = 0.2                    # perf_roca_min {float} -- Perforación mínima de la zapata a la roca [m]
    parametros["perf_roca_max"] = 0.5                    # perf_roca_max {float} -- Perforación máxima de la zapata a la roca [m]
    parametros["dist_atraccion_roca"] = 0.2              # dist_atraccion_roca {float} -- Distancia a la roca, a partir de la cual debe penetrar la zapata [m]

    return parametros