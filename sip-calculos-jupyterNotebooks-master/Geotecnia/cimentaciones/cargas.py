from .data_services import DataServices
from .torre import Torre
from typing import List, Dict, Tuple, Any
DBFila = Dict[str, Any]

class Cargas:
    def __init__(self, data_service: DataServices):
        self.data_service = data_service
        self.cargas_maxima_compresion_cartesiano = data_service.listar_cargas_maxima_compresion_cartesiano()
        self.cargas_maxima_compresion_eds_cartesiano = data_service.listar_cargas_maxima_compresion_eds_cartesiano()
        self.cargas_maxima_tesion_cartesiano = data_service.listar_cargas_maxima_tesion_cartesiano()
        self.cargas_maxima_longitudinal_cartesiano = data_service.listar_cargas_maxima_longitudinal_cartesiano()
        self.cargas_maxima_transversal_cartesiano = data_service.listar_cargas_maxima_transversal_cartesiano()
        self.cargas_maxima_compresion_montante = data_service.listar_cargas_maxima_compresion_montante()
        self.cargas_maxima_tension_montante = data_service.listar_cargas_maxima_tension_montante()
        self.cargas_maxima_lateral_montante = data_service.listar_cargas_maxima_lateral_montante()
        self.cargas_maxima_horz_long_montante = data_service.listar_cargas_maxima_horz_long_montante()
        self.cargas_maxima_horz_tran_montante = data_service.listar_cargas_maxima_horz_tran_montante()

    def seleccionar_cargas(self, torre: Torre, tipo_carga: str, caso_cargas: str, sistema_cargas: str, componentes: List[str]):
        if caso_cargas == "máxima carga a compresión" and sistema_cargas == "cartesiano":
            cargas = next(k for k in self.cargas_maxima_compresion_cartesiano if k["tipo_carga"] == tipo_carga and k["tipo_torre"] == torre.tipo)
        elif caso_cargas == "máxima carga a compresión eds" and sistema_cargas == "cartesiano":
            cargas = next(k for k in self.cargas_maxima_compresion_eds_cartesiano if k["tipo_carga"] == tipo_carga and k["tipo_torre"] == torre.tipo)
        elif caso_cargas == "máxima carga a tensión" and sistema_cargas == "cartesiano":
            cargas = next(k for k in self.cargas_maxima_tesion_cartesiano if k["tipo_carga"] == tipo_carga and k["tipo_torre"] == torre.tipo)
        elif caso_cargas == "máxima carga longitudinal" and sistema_cargas == "cartesiano":
            cargas = next(k for k in self.cargas_maxima_longitudinal_cartesiano if k["tipo_carga"] == tipo_carga and k["tipo_torre"] == torre.tipo)
        elif caso_cargas == "máxima carga transversal" and sistema_cargas == "cartesiano":
            cargas = next(k for k in self.cargas_maxima_transversal_cartesiano if k["tipo_carga"] == tipo_carga and k["tipo_torre"] == torre.tipo)
        elif caso_cargas == "máxima carga a compresión" and sistema_cargas == "montante":
            cargas = next(k for k in self.cargas_maxima_compresion_montante if k["tipo_carga"] == tipo_carga and k["tipo_torre"] == torre.tipo)
        elif caso_cargas == "máxima carga a tensión" and sistema_cargas == "montante":
            cargas = next(k for k in self.cargas_maxima_tension_montante if k["tipo_carga"] == tipo_carga and k["tipo_torre"] == torre.tipo)
        elif caso_cargas == "máxima carga lateral" and sistema_cargas == "montante":
            cargas = next(k for k in self.cargas_maxima_lateral_montante if k["tipo_carga"] == tipo_carga and k["tipo_torre"] == torre.tipo)
        elif caso_cargas == "máxima carga horz long" and sistema_cargas == "montante":
            cargas = next(k for k in self.cargas_maxima_horz_long_montante if k["tipo_carga"] == tipo_carga and k["tipo_torre"] == torre.tipo)
        elif caso_cargas == "máxima carga horz tran" and sistema_cargas == "montante":
            cargas = next(k for k in self.cargas_maxima_horz_tran_montante if k["tipo_carga"] == tipo_carga and k["tipo_torre"] == torre.tipo)
        return [abs(cargas[componente]) for componente in componentes]
    
    def obtener_cargas_trabajo_maxima_compresion_cartesiano(self, torre: Torre):
        tipo_carga = "TRABAJO"
        caso_cargas = "máxima carga a compresión"
        sistema_cargas = "cartesiano"
        componentes = ["compresion", "longitudinal", "transversal"]
        return self.seleccionar_cargas(torre, tipo_carga, caso_cargas, sistema_cargas, componentes)
        
    def obtener_cargas_trabajo_maxima_compresion_eds_cartesiano(self, torre: Torre):
        tipo_carga = "TRABAJO"
        caso_cargas = "máxima carga a compresión eds"
        sistema_cargas = "cartesiano"
        componentes = ["compresion", "longitudinal", "transversal"]
        return self.seleccionar_cargas(torre, tipo_carga, caso_cargas, sistema_cargas, componentes)
        
    def obtener_cargas_trabajo_maxima_tesion_cartesiano(self, torre: Torre):
        tipo_carga = "TRABAJO"
        caso_cargas = "máxima carga a tensión"
        sistema_cargas = "cartesiano"
        componentes = ["tension", "longitudinal", "transversal"]
        return self.seleccionar_cargas(torre, tipo_carga, caso_cargas, sistema_cargas, componentes)

    def obtener_cargas_trabajo_maxima_longitudinal_cartesiano(self, torre: Torre):
        tipo_carga = "TRABAJO"
        caso_cargas = "máxima carga longitudinal"
        sistema_cargas = "cartesiano"
        componentes = ["axial", "longitudinal", "transversal"]
        return self.seleccionar_cargas(torre, tipo_carga, caso_cargas, sistema_cargas, componentes)

    def obtener_cargas_trabajo_maxima_transversal_cartesiano(self, torre: Torre):
        tipo_carga = "TRABAJO"
        caso_cargas = "máxima carga transversal"
        sistema_cargas = "cartesiano"
        componentes = ["axial", "longitudinal", "transversal"]
        return self.seleccionar_cargas(torre, tipo_carga, caso_cargas, sistema_cargas, componentes)
    
    def obtener_cargas_trabajo_maxima_compresion_montante(self, torre: Torre):
        tipo_carga = "TRABAJO"
        caso_cargas = "máxima carga a compresión"
        sistema_cargas = "montante"
        componentes = ["compresion", "lateral", "horz_long", "horz_tran"]
        return self.seleccionar_cargas(torre, tipo_carga, caso_cargas, sistema_cargas, componentes)

    def obtener_cargas_trabajo_maxima_tension_montante(self, torre: Torre):
        tipo_carga = "TRABAJO"
        caso_cargas = "máxima carga a tensión"
        sistema_cargas = "montante"
        componentes = ["tension", "lateral", "horz_long", "horz_tran"]
        return self.seleccionar_cargas(torre, tipo_carga, caso_cargas, sistema_cargas, componentes)

    def obtener_cargas_trabajo_maxima_lateral_montante(self, torre: Torre):
        tipo_carga = "TRABAJO"
        caso_cargas = "máxima carga lateral"
        sistema_cargas = "montante"
        componentes = ["axial", "lateral", "horz_long", "horz_tran"]
        return self.seleccionar_cargas(torre, tipo_carga, caso_cargas, sistema_cargas, componentes)

    def obtener_cargas_trabajo_maxima_horz_long_montante(self, torre: Torre):
        tipo_carga = "TRABAJO"
        caso_cargas = "máxima carga horz long"
        sistema_cargas = "montante"
        componentes = ["axial", "lateral", "horz_long", "horz_tran"]
        return self.seleccionar_cargas(torre, tipo_carga, caso_cargas, sistema_cargas, componentes)    
    
    def obtener_cargas_trabajo_maxima_horz_trans_montante(self, torre: Torre):
        tipo_carga = "TRABAJO"
        caso_cargas = "máxima carga horz tran"
        sistema_cargas = "montante"
        componentes = ["axial", "lateral", "horz_long", "horz_tran"]
        return self.seleccionar_cargas(torre, tipo_carga, caso_cargas, sistema_cargas, componentes)    
    
    def obtener_cargas_diseno_maxima_compresion_cartesiano(self, torre: Torre):
        tipo_carga = "DISEÑO"
        caso_cargas = "máxima carga a compresión"
        sistema_cargas = "cartesiano"
        componentes = ["compresion", "longitudinal", "transversal"]
        return self.seleccionar_cargas(torre, tipo_carga, caso_cargas, sistema_cargas, componentes)
        
    def obtener_cargas_diseno_maxima_compresion_eds_cartesiano(self, torre: Torre):
        tipo_carga = "DISEÑO"
        caso_cargas = "máxima carga a compresión eds"
        sistema_cargas = "cartesiano"
        componentes = ["compresion", "longitudinal", "transversal"]
        return self.seleccionar_cargas(torre, tipo_carga, caso_cargas, sistema_cargas, componentes)
        
    def obtener_cargas_diseno_maxima_tesion_cartesiano(self, torre: Torre):
        tipo_carga = "DISEÑO"
        caso_cargas = "máxima carga a tensión"
        sistema_cargas = "cartesiano"
        componentes = ["tension", "longitudinal", "transversal"]
        return self.seleccionar_cargas(torre, tipo_carga, caso_cargas, sistema_cargas, componentes)

    def obtener_cargas_diseno_maxima_longitudinal_cartesiano(self, torre: Torre):
        tipo_carga = "DISEÑO"
        caso_cargas = "máxima carga longitudinal"
        sistema_cargas = "cartesiano"
        componentes = ["axial", "longitudinal", "transversal"]
        return self.seleccionar_cargas(torre, tipo_carga, caso_cargas, sistema_cargas, componentes)

    def obtener_cargas_diseno_maxima_transversal_cartesiano(self, torre: Torre):
        tipo_carga = "DISEÑO"
        caso_cargas = "máxima carga transversal"
        sistema_cargas = "cartesiano"
        componentes = ["axial", "longitudinal", "transversal"]
        return self.seleccionar_cargas(torre, tipo_carga, caso_cargas, sistema_cargas, componentes)
    
    def obtener_cargas_diseno_maxima_compresion_montante(self, torre: Torre):
        tipo_carga = "DISEÑO"
        caso_cargas = "máxima carga a compresión"
        sistema_cargas = "montante"
        componentes = ["compresion", "lateral", "horz_long", "horz_tran"]
        return self.seleccionar_cargas(torre, tipo_carga, caso_cargas, sistema_cargas, componentes)

    def obtener_cargas_diseno_maxima_tension_montante(self, torre: Torre):
        tipo_carga = "DISEÑO"
        caso_cargas = "máxima carga a tensión"
        sistema_cargas = "montante"
        componentes = ["tension", "lateral", "horz_long", "horz_tran"]
        return self.seleccionar_cargas(torre, tipo_carga, caso_cargas, sistema_cargas, componentes)

    def obtener_cargas_diseno_maxima_lateral_montante(self, torre: Torre):
        tipo_carga = "DISEÑO"
        caso_cargas = "máxima carga lateral"
        sistema_cargas = "montante"
        componentes = ["axial", "lateral", "horz_long", "horz_tran"]
        return self.seleccionar_cargas(torre, tipo_carga, caso_cargas, sistema_cargas, componentes)

    def obtener_cargas_as_dict(self, torre: Torre):
        info_cargas = {}
        F_zc, F_xc, F_yc = self.obtener_cargas_trabajo_maxima_compresion_cartesiano(torre)
        info_cargas["CompresionMaxima"] = {"F_xc":  F_xc, "F_yc": F_yc, "F_zc": F_zc}
        F_zc, F_xc, F_yc = self.obtener_cargas_trabajo_maxima_compresion_eds_cartesiano(torre)
        info_cargas["CompresionMaximaEDS"] = {"F_xc":  F_xc, "F_yc": F_yc, "F_zc": F_zc}
        F_zc, F_xc, F_yc = self.obtener_cargas_trabajo_maxima_tesion_cartesiano(torre)
        info_cargas["TensionMaxima"] = {"F_xc":  F_xc, "F_yc": F_yc, "F_zc": F_zc}
        F_zc, F_xc, F_yc = self.obtener_cargas_trabajo_maxima_longitudinal_cartesiano(torre)
        info_cargas["LongitudinalMaxima"] = {"F_xc":  F_xc, "F_yc": F_yc, "F_zc": F_zc}
        F_zc, F_xc, F_yc = self.obtener_cargas_trabajo_maxima_transversal_cartesiano(torre)
        info_cargas["TransversalMaxima"] = {"F_xc":  F_xc, "F_yc": F_yc, "F_zc": F_zc}
        F_m, F_l, F_hl, F_ht = self.obtener_cargas_trabajo_maxima_compresion_montante(torre)
        info_cargas["CompresionMaximaMon"] = {"F_m":  F_m, "F_l": F_l, "F_hl": F_hl, "F_ht": F_ht}
        F_m, F_l, F_hl, F_ht = self.obtener_cargas_trabajo_maxima_tension_montante(torre)
        info_cargas["TensionMaximaMon"] = {"F_m":  F_m, "F_l": F_l, "F_hl": F_hl, "F_ht": F_ht}
        F_m, F_l, F_hl, F_ht = self.obtener_cargas_trabajo_maxima_horz_long_montante(torre)
        info_cargas["HorizontalLongitudinalMaximaMon"] = {"F_m":  F_m, "F_l": F_l, "F_hl": F_hl, "F_ht": F_ht}
        F_m, F_l, F_hl, F_ht = self.obtener_cargas_trabajo_maxima_horz_trans_montante(torre)
        info_cargas["HorizontalTransversalMaximaMon"] = {"F_m":  F_m, "F_l": F_l, "F_hl": F_hl, "F_ht": F_ht}
        return info_cargas

    def get_angulo_inclinacion(self, torre: Torre):
        angulos = {"A100": 5.906892478, "AL100": 5.212115894, "AA100": 5.906892478, "B100": 6.807293875, "C100": 7.846555465, "D100": 9.914023378, "DT100": 9.914023378, "TR100": 5.864982621, 
                "A126": 5.906892478, "AA126": 5.906892478,  "B126": 6.807293875, "C126": 7.846555465, "D126": 9.914023378, "DT126": 9.914023378}
        return angulos[torre.tipo]
    
    def get_ancho_aleta_conector_cortante(self, torre: Torre):
        anchos = {"A100": 0.13, "AL100": 0.13, "AA100": 0.14, "B100": 0.18, "C100": 0.2, "D100": 0.2, "DT100": 0.2, "TR100": 0.2, 
                "A126": 0.15, "AA126": 0.15, "B126": 0.2, "C126": 0.2, "D126": 0.2, "DT126": 0.2}

        return anchos[torre.tipo]

    def get_proyeccion_vertical_stub(self, torre: Torre):
        proyecciones = {"A100": 2.106, "AL100": 1.8, "AA100": 2.106, "B100": 2.159, "C100": 2.2, "D100": 2.5, "DT100": 2.5, "TR100": 2.171, 
                        "A126": 2.106, "AA126": 2.106, "B126": 2.159, "C126": 2.2, "D126": 2.5, "DT126": 2.5}

        return proyecciones[torre.tipo]
