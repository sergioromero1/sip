def get_parametros_default():
    parametros = {}
    parametros['d_f_max'] = 1.5                          # b_max {float} -- Profundida de desplante máxima [m]
    parametros['d_f_paso'] = 0.1                         # d_f_paso {float} -- Incremento para las iteraciones de profundidad de desplante [m]
    parametros['b_max'] = 2.8                            # b_max {float} -- Distancia máxima del lado de zapata [m]
    parametros['n_soluciones'] = 10                      # n_soluciones {int} -- Número de soluciones a conservar para reportes
    parametros['f_carga_por_torre'] = True               # f_carga_por_torre {bool} -- Indica si la fracción de carga que toma el mp se toma por cada torre
    parametros['f_carga_mp_fijo'] =  None                # f_carga_mp_fijo {float} -- Si 'f_carga_por_torre' == False, fracción de carga fija que toma el mp de todas las torres [0.0 - 1.0]
    parametros['d_agg'] = 0.01905                        # d_agg {float} -- Tamaño máximo nominal del agregado grueso [m]
    parametros['d_b_long'] = 0.01905                     # d_b_long {float} -- Diámetro de barras de refuerzo longitudinal [m]
    parametros['d_b_trans'] = 0.01905                    # d_b_trans {float} -- Diámetro de barras de refuerzo transversal [m]
    parametros['rec'] = 0.075                            # rec {float} -- Espesor del recubrimiento [m]
    parametros['gamma_c'] = 24                           # γ_c {float} -- Peso unitario de la cimentación [kN/m³]
    parametros['gamma_r'] = 17.1                         # γ_r {float} -- Peso unitario del relleno [kN/m³]
    parametros['gamma_l'] = 17                           # γ_l {float} -- Peso unitario de la lechada del micropilote [kN/m³]
    parametros['phi_r'] = 26                             # φ_r {float} -- Ángulo de fricción del relleno [°]
    parametros["eta"] = 1                                # η {float} -- Eficiencia del grupo de micropilotes [-]
    parametros["f_pc"] = 28000                           # f_pc {float} -- Resistencia a la compresión de la lechada del micropilote [kPa]
    parametros["f_py"] = 420000                          # f_py {float} -- Esfuerzo de fluencia de la barra de refuerzo [kPa]
    parametros["a_camisa"] = 0.0                         # a_camisa {float} -- Área de la sección de la camisa [m²]
    parametros["lista_N_m"] = [4, 8, 12, 16]             # lista_N_m {List[float]} -- Lista de valores posibles para el número de micropilotes
    parametros["lista_L_b"] = [4.5, 6.0, 7.5, 9.0, 10.5] # lista_L_b {List[float]} -- Lista de valores de longitudes de micropilotes a evaluar [m]
    parametros["proc_iny"] = "IGU"                       # proc_iny {str} -- Proceso de inyección, puede uno de "IGU" o "IRS"
    parametros["S_m_min"] = 0.76                          # S_m_min {float} --  [m] 0.76 según guía FHWA
    parametros["S_m_paso"] = 0.1
    parametros["lista_S_m"] = [0.7, 0.8, 0.9, 1.0,1.1, 1.2, 1.3, 1.4, 1.5]   # lista_S_m {List[float]} -- Lista de sepaaciones entre micropilotes [m]
    parametros["h_min"] = 0.5                            # h_min {float} -- Altura mínima de la zapata [m]
    parametros["h_max"] = 1.4                            # h_max {float} -- Altura máxima de la zapata [m]
    parametros["h_paso"] = 0.05                          # h_paso {float} -- Incremento en la altura de la zapata [m]
    parametros["d_d_min"] = 0.25                         # d_d_min {float} -- Altura mínima del dentellón [m]
    parametros["d_d_max"] = 0.5                          # d_d_max {float} -- Altura máxima del dentellón [m]
    parametros["d_d_paso"] = 0.05                        # d_d_paso {float} -- Incremento en la altura del dentellón [m]
    parametros["h_relleno_min"] = 0.3                    # h_relleno_min {float} -- Altura mínima del relleno [m]
    parametros["alfa_max"] = 1.5                         # alfa_max {float} -- Factor de expansión máximo
    parametros['fsc_d'] = 3                              # FSCD {float} -- Factor de seguridad mínimo para compresión del dado
    parametros['fsc'] = 2.5                              # FSC {float} -- Factor de seguridad mínimo para cargas a compresión
    parametros['fsl'] = 1.5                              # FSL {float} -- Factor de seguridad mínimo para cargas laterales
    parametros['fst'] = 2.5                              # FST {float} -- Factor de seguridad mínimo para cargas a tensión
    parametros['k'] = 80                                 # k {int} -- Número de segmentos para análisis de asentamiento       
    parametros['t'] = 50                                 # t {int} --  Número de años para corrección 'Creep'
    parametros['s_max_adm_g'] = 0.05                     # s_max_adm_g {float} -- Asentamiento máximo permitido suelos granulares [m]
    parametros['s_max_adm_c'] = 0.10                     # s_max_adm_c {float} -- Asentamiento máximo permitido suelos cohesivos [m]
    parametros['s_max_adm_r'] = 0.05                     # s_max_adm_r {float} -- Asentamiento máximo permitido roca [m]
    parametros['lista_hg'] = [1.0, 1.5, 2.0, 3.0]        # lista_HG {List[float]} -- Lista de altura de pedestales estándares a evaluar [m]
    parametros['lista_hg_esp'] = [4.0, 5.0, 6.0, 7.0, 8.0]    # lista_HG {List[float]} -- Lista de altura de pedestales especiales a evaluar [m]
    parametros["lista_barras"] = [                       # lista_barras {List[Dict]} -- Lista de barras
        {
            "nombre": "R38-500",
            "D": 0.0378 ,
            "D_int": 0.019,
            "area": 0.0007500,
            "f_y": 530000,
            "precio": 1.00, 
            "geoms": [
                {"hg": 1.0, "anclaje": 0.33, "h_min": 0.50},
                {"hg": 1.5, "anclaje": 0.33, "h_min": 0.50},
                {"hg": 2.0, "anclaje": 0.33, "h_min": 0.50},
                {"hg": 3.0, "anclaje": 0.33, "h_min": 0.50},
                {"hg": 4.0, "anclaje": 0.38, "h_min": 0.55},
                {"hg": 5.0, "anclaje": 0.38, "h_min": 0.55},
                {"hg": 6.0, "anclaje": 0.38, "h_min": 0.55},
                {"hg": 7.0, "anclaje": 0.38, "h_min": 0.55}
            ]
        },
        {
            "nombre": "R38-550",
            "D": 0.0378 ,
            "D_int": 0.017,
            "area": 0.0008000,
            "f_y": 560000,
            "precio": 1.05, 
            "geoms": [
                {"hg": 1.0, "anclaje": 0.33, "h_min": 0.50},
                {"hg": 1.5, "anclaje": 0.33, "h_min": 0.50},
                {"hg": 2.0, "anclaje": 0.33, "h_min": 0.50},
                {"hg": 3.0, "anclaje": 0.33, "h_min": 0.50},
                {"hg": 4.0, "anclaje": 0.38, "h_min": 0.55},
                {"hg": 5.0, "anclaje": 0.38, "h_min": 0.55},
                {"hg": 6.0, "anclaje": 0.38, "h_min": 0.55},
                {"hg": 7.0, "anclaje": 0.38, "h_min": 0.55},
                {"hg": 8.0, "anclaje": 0.38, "h_min": 0.55}
            ]
        },
        # {"nombre": "R51-550",          "D": 0.0498 , "area": 0.0008900, "f_y": 510000, "precio": 1.25, "anclaje": 0.38, "h_min": 0.55},
        # {"nombre": "R51-660",          "D": 0.0498 , "area": 0.0009700, "f_y": 560000, "precio": 1.35, "anclaje": 0.38, "h_min": 0.56},
        # {"nombre": "R51-800",          "D": 0.0498 , "area": 0.0011500, "f_y": 560000, "precio": 1.55, "anclaje": 0.39, "h_min": 0.57},
        # {"nombre": "R51-950",          "D": 0.0498 , "area": 0.0012250, "f_y": 640000, "precio": 2.00, "anclaje": 0.39, "h_min": 0.57},
        # {"nombre": "T76-1300",         "D": 0.0756 , "area": 0.0015900, "f_y": 630000, "precio": 3.10, "anclaje": 0.39, "h_min": 0.57},

        {
            "nombre": "DSI GEWI 28 PLUS", 
            "D": 0.0280 ,
            "D_int": 0.0,
            "area": 0.0006158, 
            "f_y": 670000, 
            "precio": 0.70, 
            "geoms": [
                {"hg": 1.0, "anclaje": 0.33, "h_min": 0.50},
                {"hg": 1.5, "anclaje": 0.33, "h_min": 0.50},
                {"hg": 2.0, "anclaje": 0.33, "h_min": 0.50},
                {"hg": 3.0, "anclaje": 0.33, "h_min": 0.50},
                {"hg": 4.0, "anclaje": 0.38, "h_min": 0.55},
                {"hg": 5.0, "anclaje": 0.38, "h_min": 0.55},
                {"hg": 6.0, "anclaje": 0.38, "h_min": 0.55},
                {"hg": 7.0, "anclaje": 0.38, "h_min": 0.55},
                {"hg": 8.0, "anclaje": 0.38, "h_min": 0.55}
            ]
        }
        # {"nombre": "DSI GEWI 40",      "D": 0.0400 , "area": 0.0012566, "f_y": 500000, "precio": 1.25, "anclaje": 0.41, "h_min": 0.60},
        # {"nombre": "DSI GEWI 50",      "D": 0.0500 , "area": 0.0019635, "f_y": 500000, "precio": 2.10, "anclaje": 0.40, "h_min": 0.57}
    ]

    parametros["suelo_diametro_barra"] = [               # suelo_diametro_barra {List[Dict]} -- Tabla de utilización de barras de acuerdo al proceso de inyección, suelo y diámetro de perforación
            {"proc_iny": "IGU", "suelo": "Suelos cohesivos", "D_p": 0.115, "barras": ['R38-550']},
            {"proc_iny": "IGU", "suelo": "Suelos cohesivos", "D_p": 0.130, "barras": ['R38-550']},

            {"proc_iny": "IGU", "suelo": "Arena",            "D_p": 0.115, "barras": ['R38-550']},
            {"proc_iny": "IGU", "suelo": "Arena",            "D_p": 0.130, "barras": ['R38-550']},

            {"proc_iny": "IGU", "suelo": "Gravas",           "D_p": 0.115, "barras": ['R38-550']},

            {"proc_iny": "IGU", "suelo": "Roca blanda",      "D_p": 0.115, "barras": ['R38-550']},

            {"proc_iny": "IGU", "suelo": "Roca dura",        "D_p": 0.115, "barras": ['R38-550']},

            {"proc_iny": "IRS", "suelo": "Suelos cohesivos", "D_p": 0.115, "barras": ['DSI GEWI 28 PLUS']},

            {"proc_iny": "IRS", "suelo": "Arena",            "D_p": 0.115, "barras": ['DSI GEWI 28 PLUS']},

            {"proc_iny": "IRS", "suelo": "Gravas",           "D_p": 0.115, "barras": ['DSI GEWI 28 PLUS']},

            {"proc_iny": "IRS", "suelo": "Roca blanda",      "D_p": 0.115, "barras": ['DSI GEWI 28 PLUS']},

            {"proc_iny": "IRS", "suelo": "Roca dura",        "D_p": 0.115, "barras": ['DSI GEWI 28 PLUS']}
    ]

    # parametros['tabla_alfa_exp'] = { ("g", "IRS") : 1.50, ("g", "IGU") : 1.15, # Diccionario para la evaluación de α_exp : Factor de expansión, con key: (tipo material, procedimiento de inyección)
    #                                 ("c", "IRS") : 1.40, ("c", "IGU") : 1.10, 
    #                                 ("r", "IRS") : 1.20, ("r", "IGU") : 1.00, }

    # parametros["suelo_diametro_barra"] = [               # suelo_diametro_barra {List[Dict]} -- Tabla de utilización de barras de acuerdo al proceso de inyección, suelo y diámetro de perforación
    #         {"proc_iny": "IGU", "suelo": "Suelos cohesivos", "D_p": 0.115, "barras": ['R38-550','R51-550','R51-800']},
    #         {"proc_iny": "IGU", "suelo": "Suelos cohesivos", "D_p": 0.130, "barras": ['R38-550','R51-550','R51-800']},
    #         {"proc_iny": "IGU", "suelo": "Suelos cohesivos", "D_p": 0.150, "barras": ['R51-550','R51-800']},

    #         {"proc_iny": "IGU", "suelo": "Arena",            "D_p": 0.115, "barras": ['R38-550','R51-550','R51-800']},
    #         {"proc_iny": "IGU", "suelo": "Arena",            "D_p": 0.130, "barras": ['R38-550','R51-550','R51-800']},
    #         {"proc_iny": "IGU", "suelo": "Arena",            "D_p": 0.150, "barras": ['R51-550','R51-800']},

    #         {"proc_iny": "IGU", "suelo": "Gravas",           "D_p": 0.115, "barras": ['R38-550','R51-550','R51-800']},
    #         {"proc_iny": "IGU", "suelo": "Gravas",           "D_p": 0.130, "barras": ['R51-550','R51-800']},

    #         {"proc_iny": "IGU", "suelo": "Roca blanda",      "D_p": 0.115, "barras": ['R38-550','R51-550','R51-800']},
    #         {"proc_iny": "IGU", "suelo": "Roca blanda",      "D_p": 0.130, "barras": ['R51-550','R51-800']},

    #         {"proc_iny": "IGU", "suelo": "Roca dura",        "D_p": 0.115, "barras": ['R38-550','R51-550','R51-800']},
    #         {"proc_iny": "IGU", "suelo": "Roca dura",        "D_p": 0.130, "barras": ['R51-550','R51-800']},

    #         {"proc_iny": "IRS", "suelo": "Suelos cohesivos", "D_p": 0.115, "barras": ['DSI GEWI 28 PLUS', 'DSI GEWI 50']},
    #         {"proc_iny": "IRS", "suelo": "Suelos cohesivos", "D_p": 0.130, "barras": ['DSI GEWI 50']},
    #         {"proc_iny": "IRS", "suelo": "Suelos cohesivos", "D_p": 0.150, "barras": ['DSI GEWI 50']},

    #         {"proc_iny": "IRS", "suelo": "Arena",            "D_p": 0.115, "barras": ['DSI GEWI 28 PLUS', 'DSI GEWI 50']},
    #         {"proc_iny": "IRS", "suelo": "Arena",            "D_p": 0.130, "barras": ['DSI GEWI 50']},
    #         {"proc_iny": "IRS", "suelo": "Arena",            "D_p": 0.150, "barras": ['DSI GEWI 50']},

    #         {"proc_iny": "IRS", "suelo": "Gravas",           "D_p": 0.115, "barras": ['DSI GEWI 28 PLUS', 'DSI GEWI 50']},
    #         {"proc_iny": "IRS", "suelo": "Gravas",           "D_p": 0.130, "barras": ['DSI GEWI 50']},
    #         {"proc_iny": "IRS", "suelo": "Gravas",           "D_p": 0.150, "barras": ['DSI GEWI 50']},

    #         {"proc_iny": "IRS", "suelo": "Roca blanda",      "D_p": 0.115, "barras": ['DSI GEWI 28 PLUS', 'DSI GEWI 50']},
    #         {"proc_iny": "IRS", "suelo": "Roca blanda",      "D_p": 0.130, "barras": ['DSI GEWI 50']},
    #         {"proc_iny": "IRS", "suelo": "Roca blanda",      "D_p": 0.150, "barras": ['DSI GEWI 50']},

    #         {"proc_iny": "IRS", "suelo": "Roca dura",        "D_p": 0.115, "barras": ['DSI GEWI 28 PLUS', 'DSI GEWI 50']},
    #         {"proc_iny": "IRS", "suelo": "Roca dura",        "D_p": 0.130, "barras": ['DSI GEWI 50']},
    #         {"proc_iny": "IRS", "suelo": "Roca dura",        "D_p": 0.150, "barras": ['DSI GEWI 50']}
    # ]
    parametros["costo_excavacion"] = 109302.8             # costo_excavacion [$/m³] -- Costo de excavación para optimización 
    parametros["costo_relleno"] = 45899.94                # costo_relleno [$/m³] -- Costo de excavación para optimización 
    parametros["costo_micropilote"] = 411016.59           # costo_micropilote [$/m] -- Costo de micropilote para optimización 
    parametros["costo_concreto"] = 814935.33              # costo_concreto [$/m³] -- Costo de concreto del dado para optimización 
    parametros["costo_camisa"] = 168978.16                # costo_concreto [$/m] -- Costo de la camisa para optimización 

    return parametros