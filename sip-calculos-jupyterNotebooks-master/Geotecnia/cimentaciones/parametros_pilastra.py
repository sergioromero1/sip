def get_parametros_default():
    parametros = {}
    parametros['n_soluciones'] = 10                      # n_soluciones {int} -- Número de soluciones a conservar para reportes
    parametros['hg_por_pata'] = False                    # Indica si aparte de la lista de hgs a evaluar, se debe incluir el hg de cada pata
    parametros['D_p_min'] = 1.2                          # D_p_min {float} -- Valor mínimo para las iteraciones de diametro de la pilastra D_p [m]
    parametros['D_p_max'] = 2.0                          # D_p_max {float} -- Valor máximo para las iteraciones de diametro de la pilastra D_p [m]
    parametros['D_p_paso'] = 0.1                         # D_p_paso {float} -- Incremento para las iteraciones de diametro de la pilastra D_p [m]
    parametros['H_min'] = 0.5                            # H_min {float} -- Valor mínimo para las iteraciones del espesor de la pilastra H [m]
    parametros['H_max'] = 5.0                            # H_max {float} -- Valor máximo para las iteraciones del espesor de la pilastra H [m]
    parametros['H_paso'] = 0.1                           # H_paso {float} -- Incremento para las iteraciones del espesor de la pilastra H [m]
    parametros['h_is'] = [1.0, 1.5]                      # h_ps {float} -- Lista de profundidad de inicio de la pilastra [m]
    parametros['lista_hg'] = [0.25, 0.5, 1.0, 1.5, 2.0]  # Lista de altura de pedestales a evaluar [m] 
    parametros['gamma_c'] = 24.0                         # Peso unitario de la cimentación [kN/m³]
    parametros['d_agg'] = 0.01905                        # d_agg {float} -- Tamaño máximo nominal del agregado grueso [m]
    parametros['d_b_long'] = 0.01905                     # d_b_long {float} -- Diámetro de barras de refuerzo longitudinal [m]
    parametros['d_b_trans'] = 0.01905                    # d_b_trans {float} -- Diámetro de barras de refuerzo transversal [m]
    parametros['rec'] = 0.05                             # Longitud del recubrimiento del dado [m]
    parametros['rec_fondo_stub'] = 0.125                 # rec_fondo_stub {float} -- Recubrimiento vertical en el fondo de la pilastra para el stub [m]    
    parametros['dict_tp'] = {"A100": 0.6,                # Lado correspondiente a la sección transversal del pedestal [m]
                            "AL100": 0.6, "AA100": 0.6, "B100": 0.6, 
                            "C100": 0.6, "D100": 0.6, "DT100": 0.6, "TR100": 0.6,
                            "A126": 0.6, "AA126": 0.6, "B126": 0.6, "C126": 0.6,
                            "D126": 0.6, "DT126": 0.6}
    parametros['usar_tp'] = False                        # Indica si los cálculos deben usar el tp indicado o calcular el TP mínimo
    parametros['fsc'] = 1.0                              # fsc: Factore de seguridad a compresión
    parametros['fst'] = 1.0                              # fst: Factor de seguridad a tensión suelo granular
    parametros['fsv'] = 1.5                              # fsv: Factor de seguridad para volcamiento
    parametros['fsl'] = 1.5                              # fsl: Factor de seguridad para cargas laterales

    return parametros