def get_parametros_default():
    parametros = {}
    parametros['d_f_max'] = 1.5                          # b_max {float} -- Profundida de desplante máxima [m]
    parametros['d_f_paso'] = 0.1                         # d_f_paso {float} -- Incremento para las iteraciones de profundidad de desplante [m]
    parametros['b_max'] = 2.8                            # b_max {float} -- Distancia máxima del lado de zapata [m]
    parametros['n_soluciones'] = 10                      # n_soluciones {int} -- Número de soluciones a conservar para reportes
    parametros['d_agg'] = 0.01905                        # d_agg {float} -- Tamaño máximo nominal del agregado grueso [m]
    parametros['d_b_long'] = 0.01905                     # d_b_long {float} -- Diámetro de barras de refuerzo longitudinal [m]
    parametros['d_b_trans'] = 0.01905                    # d_b_trans {float} -- Diámetro de barras de refuerzo transversal [m]
    parametros['rec'] = 0.075                            # rec {float} -- Espesor del recubrimiento [m]
    parametros['gamma_c'] = 24                           # γ_c {float} -- Peso unitario de la cimentación [kN/m³]
    parametros["lista_n"] = [4, 5, 8, 9]                 # lista_n {List[float]} -- Lista de valores posibles para el número de pilotes
    parametros["lista_H"] = [3.0, 4.0, 5.0, 6.0, 7.0,    # lista_H {List[float]} -- Lista de valores de longitudes de pilotes a evaluar [m]
                            8.0, 9.0, 10.5]
    parametros["factor_s_p"] = 3                         # factor_S_p {float} -- Factor de separación de los pilotes respecto a su diámetro [-]
    parametros['campana'] = False                        # campana{bool} -- Boleano que define condicion del pilote con o sin campana
    parametros['h_c'] = None                             # h_c {float} -- altura de campana [m]
    parametros['h_con'] = None                           # h_con {float} -- Altura de la sección conica de la campana[m]
    parametros['θ_c'] = None                             # θ_c {float} --  Ángulo de la campana [°]
    parametros['d_bor'] = 0.30                           # d_bor {float -- Distancia del pilote al borde del dado [m]
    parametros['f_carga_por_torre'] =False               # f_carga_por_torre {bool} -- Indica si la fracción de carga que toma el p se toma por cada torre
    parametros['f_carga_p_fijo'] = 1                     # f_carga_p_fijo {float} -- Fracción de carga que toman los pilotes [-]
    parametros['hincado'] = False                        # hincado {bool} -- Boleano que define condicion del pilote hincado o preexcavado
    parametros['k'] = 80                                 # k {int} -- Número de segmentos para análisis de asentamiento       
    parametros['t'] = 50                                 # t {int} --  Número de años para corrección 'Creep'
    parametros['s_max_adm_g'] = 0.0254                   # s_max_adm_g {float} -- Asentamiento máximo permitido suelos granulares [m]
    parametros['s_max_adm_c'] = 0.0508                   # s_max_adm_c {float} -- Asentamiento máximo permitido suelos cohesivos [m]
    parametros['s_max_adm_r'] = 0.0254                   # s_max_adm_r {float} -- Asentamiento máximo permitido roca [m]
    parametros['lista_hg'] = [1.0, 1.5, 2.0, 3.0]        # lista_HG {List[float]} -- Lista de altura de pedestales a evaluar [m]
    parametros['hg_por_pata'] = False                    # Indica si aparte de la lista de hgs a evaluar, se debe incluir el hg de cada pata
    # parametros['D_p_min'] = 0.3                        # D_p_min {float} -- Valor mínimo para las iteraciones de diámetro del pilote D_p [m]
    # parametros['D_p_max'] = 1.2                        # D_p_max {float} -- Valor máximo para las iteraciones de diámetro del pilote D_p [m]
    # parametros['D_p_paso'] = 0.1                       # D_p_paso {float} -- Incremento para las iteraciones de diámetro del pilote D_p [m]
    parametros['lista_D_p'] = [0.3, 0.4, 0.5, 0.6, 0.7,
                            0.8, 0.9, 1.0, 1.1, 1.2]
    parametros['lista_H_z_min'] = [0.3, 0.3, 0.35, 0.35, 0.35,
                            0.35, 0.35, 0.35, 0.35, 0.35 ]
    parametros['rec_fondo_stub'] = 0.125                 # rec_fondo_stub {float} -- Recubrimiento vertical en el fondo de la pilastra para el stub [m]    
    parametros['dict_tp'] = {"A100": 0.6,                # Lado correspondiente a la sección transversal del pedestal [m]
                            "AL100": 0.6, "AA100": 0.6, "B100": 0.6, 
                            "C100": 0.6, "D100": 0.6, "DT100": 0.6, "TR100": 0.6,
                            "A126": 0.6, "AA126": 0.6, "B126": 0.6, "C126": 0.6,
                            "D126": 0.6, "DT126": 0.6}
    parametros['usar_tp'] = False                        # Indica si los cálculos deben usar el tp indicado o calcular el TP mínimo
    parametros["h_relleno_min"] = 0.3                    # h_relleno_min {float} -- Altura mínima del relleno [m]
    # parametros["h_z_min"] = 0.5                        # h_min {float} -- Altura mínima de la zapata [m]
    # parametros["h_z_max"] = 0.9                        # h_max {float} -- Altura máxima de la zapata [m]
    parametros["E_p"] = 29492000                         # E_p {float} -- Modulo de elasticidad del material de los pilotes [kPa]
    parametros['fsc'] = 2.5                              # FSC {float} -- Factor de seguridad mínimo para cargas a compresión
    parametros['fsll'] = 1.5                             # FSL {float} -- Factor de seguridad mínimo para cargas laterales
    parametros['fslc'] = 2                               # FSL {float} -- Factor de seguridad mínimo para cargas laterales
    parametros['fst'] = 2                                # FST {float} -- Factor de seguridad mínimo para cargas a tensión
    parametros['fsc_p'] = 1.0                            # FSCp {float} -- Factor de seguridad mínimo para cargas a compresión de un pilote

    return parametros