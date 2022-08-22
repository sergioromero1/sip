def get_parametros_default():
    parametros = {}
    
    parametros['D_p_min'] = 1.2                          # D_p_min {float} -- Valor mínimo para las iteraciones de diametro de la pila D_p [m]
    parametros['D_p_max'] = 2.0                          # D_p_max {float} -- Valor máximo para las iteraciones de diametro de la pila D_p [m]
    parametros['D_p_paso'] = 0.1                         # D_p_paso {float} -- Incremento para las iteraciones de diametro de la pila D_p [m] 
    
    parametros['H_min'] = 0.5                            # H_min {float} -- Valor mínimo para las iteraciones del espesor de la pila H [m]
    parametros['H_max'] = 5.0                            # H_max {float} -- Valor máximo para las iteraciones del espesor de la pila H [m]
    parametros['H_paso'] = 0.1                           # H_paso {float} -- Incremento para las iteraciones del espesor de la pila H [m]
    
    parametros['h_i_min'] = 0.5                          # h_i_min {float} -- Valor mínimo para las iteraciones de la profundidad de inicio de la pila [m]
    parametros['h_i_max'] = 1.5                          # h_i_max {float} -- Valor máximo para las iteraciones de la profundidad de inicio de la pila [m]
    parametros['h_i_paso'] = 0.1                         # h_i_paso {float} -- Incremento para las iteraciones de la profundidad de inicio de la pila [m]

    parametros['lista_hg'] = [0.25, 0.5, 1.0, 1.5, 2.0]  # Lista de altura de pedestales a evaluar [m] 
    
    parametros['gamma_c'] = 24.0                         # gamma_c {float} -- Peso unitario de la cimentación [kN/m³]
    parametros["E_p"] = 29492000                         # E_p {float} -- Modulo de elasticidad del material de la pila [kPa]
    
    parametros['campana'] = True                        # campana{bool} -- Boleano que define condicion de pila con o sin campana
    parametros['h_c'] = 0.50                             # h_c {float} -- altura de campana [m]
    parametros['h_con'] = 0.25                           # h_con {float} -- Altura de la sección conica de la campana[m]
    parametros['θ_c'] = 20                             # θ_c {float} --  Ángulo de la campana [°]

    parametros['d_agg'] = 0.01905                        # d_agg {float} -- Tamaño máximo nominal del agregado grueso [m]
    parametros['d_b_long'] = 0.01905                     # d_b_long {float} -- Diámetro de barras de refuerzo longitudinal [m]
    parametros['d_b_trans'] = 0.01905                    # d_b_trans {float} -- Diámetro de barras de refuerzo transversal [m]
    parametros['rec'] = 0.05                             # Longitud del recubrimiento del dado [m]
    parametros['rec_fondo_stub'] = 0.125                 # rec_fondo_stub {float} -- Recubrimiento vertical en el fondo de la pila para el stub [m]    

    parametros['usar_tp'] = False                        # usar_tp {bool} -- Indica si los cálculos deben usar el tp indicado o calcular el TP mínimo
    parametros['dict_tp'] = {"A100": 0.6,                # dict_tp {dict} --  Lado correspondiente a la sección transversal del pedestal por tipo de torre [m]
                            "AL100": 0.6, "AA100": 0.6, "B100": 0.6, 
                            "C100": 0.6, "D100": 0.6, "DT100": 0.6, "TR100": 0.6,
                            "A126": 0.6, "AA126": 0.6, "B126": 0.6, "C126": 0.6,
                            "D126": 0.6, "DT126": 0.6}

    parametros['fsc'] = 2.5                              # fsc {float} -- Factore de seguridad a compresión
    parametros['fst'] = 2                                # fst {float} -- Factor de seguridad a tensión suelo granular
    parametros['fsv'] = 1.5                              # fsv {float} -- Factor de seguridad para volcamiento
    parametros['fsll'] = 1.5                             # fsll {float} -- Factor de seguridad mínimo para cargas laterales
    parametros['fslc'] = 2                               # fslc {float} -- Factor de seguridad mínimo para cargas laterales
    parametros['s_max_adm_g'] = 0.0254                   # s_max_adm_g {float} -- Asentamiento máximo permitido suelos granulares [m]
    parametros['s_max_adm_c'] = 0.0508                   # s_max_adm_c {float} -- Asentamiento máximo permitido suelos cohesivos [m]
    parametros['s_max_adm_r'] = 0.0254                   # s_max_adm_r {float} -- Asentamiento máximo permitido roca [m]

    return parametros