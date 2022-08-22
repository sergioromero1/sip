from .data_services import DataServices
from typing import List, Dict, Tuple, Any
DBFila = Dict[str, Any]

class CargasPorCuerpo:
    def __init__(self, data_service: DataServices):
        self.data_service = data_service
        self.cargas_maxima_compresion_cartesiano = data_service.listar_cargas_maxima_compresion_cartesiano_por_cuerpo()
        self.cargas_maxima_compresion_eds_cartesiano = data_service.listar_cargas_maxima_compresion_eds_cartesiano_por_cuerpo()
        self.cargas_maxima_tesion_cartesiano = data_service.listar_cargas_maxima_tesion_cartesiano_por_cuerpo()
        self.cargas_maxima_longitudinal_cartesiano = data_service.listar_cargas_maxima_longitudinal_cartesiano_por_cuerpo()
        self.cargas_maxima_transversal_cartesiano = data_service.listar_cargas_maxima_transversal_cartesiano_por_cuerpo()
        self.cargas_maxima_compresion_montante = data_service.listar_cargas_maxima_compresion_montante_por_cuerpo()
        self.cargas_maxima_tension_montante = data_service.listar_cargas_maxima_tension_montante_por_cuerpo()
        self.cargas_maxima_lateral_montante = data_service.listar_cargas_maxima_lateral_montante_por_cuerpo()

    def seleccionar_cargas(self, torre: DBFila, tipo_carga: str, caso_cargas: str, sistema_cargas: str, componentes: List[str]):
        if caso_cargas == "máxima carga a compresión" and sistema_cargas == "cartesiano":
            cargas = next(k for k in self.cargas_maxima_compresion_cartesiano if k["tipo_carga"] == tipo_carga and k["tipo_torre"] == torre["tipo"] and k["cuerpo"] == torre["cuerpo"])
        elif caso_cargas == "máxima carga a compresión eds" and sistema_cargas == "cartesiano":
            cargas = next(k for k in self.cargas_maxima_compresion_eds_cartesiano if k["tipo_carga"] == tipo_carga and k["tipo_torre"] == torre["tipo"] and k["cuerpo"] == torre["cuerpo"])        
        elif caso_cargas == "máxima carga a tensión" and sistema_cargas == "cartesiano":
            cargas = next(k for k in self.cargas_maxima_tesion_cartesiano if k["tipo_carga"] == tipo_carga and k["tipo_torre"] == torre["tipo"] and k["cuerpo"] == torre["cuerpo"])
        elif caso_cargas == "máxima carga longitudinal" and sistema_cargas == "cartesiano":
            cargas = next(k for k in self.cargas_maxima_longitudinal_cartesiano if k["tipo_carga"] == tipo_carga and k["tipo_torre"] == torre["tipo"] and k["cuerpo"] == torre["cuerpo"])
        elif caso_cargas == "máxima carga transversal" and sistema_cargas == "cartesiano":
            cargas = next(k for k in self.cargas_maxima_transversal_cartesiano if k["tipo_carga"] == tipo_carga and k["tipo_torre"] == torre["tipo"] and k["cuerpo"] == torre["cuerpo"])
        elif caso_cargas == "máxima carga a compresión" and sistema_cargas == "montante":
            cargas = next(k for k in self.cargas_maxima_compresion_montante if k["tipo_carga"] == tipo_carga and k["tipo_torre"] == torre["tipo"] and k["cuerpo"] == torre["cuerpo"])
        elif caso_cargas == "máxima carga a tensión" and sistema_cargas == "montante":
            cargas = next(k for k in self.cargas_maxima_tension_montante if k["tipo_carga"] == tipo_carga and k["tipo_torre"] == torre["tipo"] and k["cuerpo"] == torre["cuerpo"])
        elif caso_cargas == "máxima carga lateral" and sistema_cargas == "montante":
            cargas = next(k for k in self.cargas_maxima_lateral_montante if k["tipo_carga"] == tipo_carga and k["tipo_torre"] == torre["tipo"] and k["cuerpo"] == torre["cuerpo"])
        return [abs(cargas[componente]) for componente in componentes]
    
    def obtener_cargas_trabajo_maxima_compresion_cartesiano(self, torre: DBFila):
        tipo_carga = "TRABAJO"
        caso_cargas = "máxima carga a compresión"
        sistema_cargas = "cartesiano"
        componentes = ["compresion", "longitudinal", "transversal"]
        return self.seleccionar_cargas(torre, tipo_carga, caso_cargas, sistema_cargas, componentes)
        
    def obtener_cargas_trabajo_maxima_compresion_eds_cartesiano(self, torre: DBFila):
        tipo_carga = "TRABAJO"
        caso_cargas = "máxima carga a compresión eds"
        sistema_cargas = "cartesiano"
        componentes = ["compresion", "longitudinal", "transversal"]
        return self.seleccionar_cargas(torre, tipo_carga, caso_cargas, sistema_cargas, componentes)
        
    def obtener_cargas_trabajo_maxima_tesion_cartesiano(self, torre: DBFila):
        tipo_carga = "TRABAJO"
        caso_cargas = "máxima carga a tensión"
        sistema_cargas = "cartesiano"
        componentes = ["tension", "longitudinal", "transversal"]
        return self.seleccionar_cargas(torre, tipo_carga, caso_cargas, sistema_cargas, componentes)

    def obtener_cargas_trabajo_maxima_longitudinal_cartesiano(self, torre: DBFila):
        tipo_carga = "TRABAJO"
        caso_cargas = "máxima carga longitudinal"
        sistema_cargas = "cartesiano"
        componentes = ["axial", "longitudinal", "transversal"]
        return self.seleccionar_cargas(torre, tipo_carga, caso_cargas, sistema_cargas, componentes)

    def obtener_cargas_trabajo_maxima_transversal_cartesiano(self, torre: DBFila):
        tipo_carga = "TRABAJO"
        caso_cargas = "máxima carga transversal"
        sistema_cargas = "cartesiano"
        componentes = ["axial", "longitudinal", "transversal"]
        return self.seleccionar_cargas(torre, tipo_carga, caso_cargas, sistema_cargas, componentes)

    
    def obtener_cargas_trabajo_maxima_compresion_montante(self, torre: DBFila):
        tipo_carga = "TRABAJO"
        caso_cargas = "máxima carga a compresión"
        sistema_cargas = "montante"
        componentes = ["compresion", "lateral"]
        return self.seleccionar_cargas(torre, tipo_carga, caso_cargas, sistema_cargas, componentes)

    def obtener_cargas_trabajo_maxima_tension_montante(self, torre: DBFila):
        tipo_carga = "TRABAJO"
        caso_cargas = "máxima carga a tensión"
        sistema_cargas = "montante"
        componentes = ["tension", "lateral"]
        return self.seleccionar_cargas(torre, tipo_carga, caso_cargas, sistema_cargas, componentes)

    def obtener_cargas_trabajo_maxima_lateral_montante(self, torre: DBFila):
        tipo_carga = "TRABAJO"
        caso_cargas = "máxima carga lateral"
        sistema_cargas = "montante"
        componentes = ["axial", "lateral"]
        return self.seleccionar_cargas(torre, tipo_carga, caso_cargas, sistema_cargas, componentes)

    def obtener_cargas_as_dict(self, torre: DBFila):
        info_cargas = {}
        F_zc, F_xc, F_yc = self.obtener_cargas_trabajo_maxima_compresion_cartesiano(torre)
        info_cargas["CompresionMaxima"] = {"F_xc":  F_xc, "F_yc": F_yc, "F_zc": F_zc}
        # F_zc, F_xc, F_yc = self.obtener_cargas_trabajo_maxima_compresion_eds_cartesiano(torre)
        # info_cargas["CompresionMaximaEDS"] = {"F_xc":  F_xc, "F_yc": F_yc, "F_zc": F_zc}
        F_zc, F_xc, F_yc = self.obtener_cargas_trabajo_maxima_tesion_cartesiano(torre)
        info_cargas["TensionMaxima"] = {"F_xc":  F_xc, "F_yc": F_yc, "F_zc": F_zc}
        F_zc, F_xc, F_yc = self.obtener_cargas_trabajo_maxima_longitudinal_cartesiano(torre)
        info_cargas["LongitudinalMaxima"] = {"F_xc":  F_xc, "F_yc": F_yc, "F_zc": F_zc}
        F_zc, F_xc, F_yc = self.obtener_cargas_trabajo_maxima_transversal_cartesiano(torre)
        info_cargas["TransversalMaxima"] = {"F_xc":  F_xc, "F_yc": F_yc, "F_zc": F_zc}
        F_m, F_l = self.obtener_cargas_trabajo_maxima_compresion_montante(torre)
        info_cargas["CompresionMaximaMon"] = {"F_m":  F_m, "F_l": F_l}
        F_m, F_l = self.obtener_cargas_trabajo_maxima_tension_montante(torre)
        info_cargas["TensionMaximaMon"] = {"F_m":  F_m, "F_l": F_l}
        return info_cargas

    def get_angulo_inclinacion(self, torre: DBFila):
        angulos = {"A100" : 5.906892478, 	"AL100": 5.212115894, "AA100": 5.906892478, "B100": 6.807293875, "C100": 7.846555465, "D100": 9.914023378, "DT100": 9.914023378, "TR100": 9.914023378}
        return angulos[torre["tipo"]]
    
    def get_ancho_aleta_conector_cortante(self, torre: DBFila):
        anchos = {"A100" : 0.13, "AL100": 0.13, "AA100": 0.14, "B100": 0.18, "C100": 0.2, "D100": 0.2, "DT100": 0.2, "TR100": 0.2}
        return anchos[torre["tipo"]]

    def get_proyeccion_vertical_stub(self, torre: DBFila):
        proyecciones = {"A100" : 2.106, "AL100": 1.8, "AA100": 2.106, "B100": 2.159, "C100": 2.2, "D100": 2.5, "DT100": 2.5, "TR100": 2.5}
        return proyecciones[torre["tipo"]]
