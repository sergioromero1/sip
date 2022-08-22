def get_parametros_default():
    parametros = {}
    parametros['fsc'] =  3.0                             # fsc {float} -- Factor de seguridad a compresión
    parametros['fst_g'] = 1.5                            # fst_g {float} -- Factor de seguridad a tensión suelo granular
    parametros['fst_c'] = 2.0                            # fst_c {float} -- Factor de seguridad a tensión suelo cohesivo
    parametros['k'] = 80                                 # k {int} -- Número de segmentos para análisis de asentamiento       
    parametros['t'] = 50                                 # t {int} -- Número de años para corrección 'Creep'
    parametros['s_max_adm_g'] = 0.05                     # s_max_adm_g {float} -- Asentamiento máximo permitido suelos granulares [m]
    parametros['s_max_adm_c'] = 0.10                     # s_max_adm_c {float} -- Asentamiento máximo permitido suelos cohesivos [m]
    parametros['fsv'] = 1.5                              # fsv {float} -- Factor de seguridad para volcamiento
    parametros['fsl'] = 1.5                              # fsl {float} -- Factor de seguridad para cargas laterales

    return parametros