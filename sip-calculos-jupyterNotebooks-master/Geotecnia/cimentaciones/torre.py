class Torre():
    """Clase que representa una torre
    Attributes:
        nombre {str} -- Nombre de la torre
        abscisa {float} -- Abscisa [m] 
        perfil {str} -- Nombre del perfil estratigráfico de la torre. Normalmente coincide con el nombre de la torre.
        tipo {str} -- Nombre del tipo de torre. Debe coincidir con el nombre utilizado en la consulta de cargas
        cuerpo {int} -- Número de cuerpos de la torre. Se requiere si las cargas a utilizar no son la envolvente 
        sumergido {boolean} -- Indica si la torre se encuentra en zona inundable
        inclinacion_terreno {float} -- Ángulo de inclinación del terreno en el sitio de torre [°]. Se asume 0 si está nulo.
        inclinacion_base_zapata {float} -- Ángulo de inclinación de la base de la zapata [°]
        recom_zapata {boolean} -- Indica si se recomienda zapata para la torre
        recom_micropilotes {boolean} -- Indica si se recomienda micropilotes para la torre
        recom_pilastra {boolean} -- Indica si se recomienda pilastra para la torre
        recom_especial {boolean} -- Indica si se recomienda cimentación especial para la torre
        ped_pata_a {float} -- Pedestal en la pata A. Se requiere si se desea incluir patas no estándares en el análisis (var parámetro 'hg_por_pata')
        ped_pata_b {float} -- Pedestal en la pata B. Se requiere si se desea incluir patas no estándares en el análisis (var parámetro 'hg_por_pata')
        ped_pata_c {float} -- Pedestal en la pata C. Se requiere si se desea incluir patas no estándares en el análisis (var parámetro 'hg_por_pata')
        ped_pata_d {float} -- Pedestal en la pata D. Se requiere si se desea incluir patas no estándares en el análisis (var parámetro 'hg_por_pata')
        f_carga_mp {float} -- Fracción de carga que tomarían los micropilotes en esta torre [0..1]
        prof_min_desplante {float} -- Profundidad mínima de desplante recomendada para zapata en suelo [m]
        gamma_r {float} -- Peso unitario del relleno en el suelo de la torre  [kN/m³]. #TODO Esto debería estar en perfil. Está aquí temporalmente porque es los más fácil dada la urgencia de la entrega
        zona_geotecnia {str} -- Zona geotécnica
        este {float} -- Coordenada este de la torre [m]
        norte {float} -- Coordenada norte de la torre [m]
        cota {float} -- Cota de la torre [m]
        fc {float} -- Resistencia mínima del concreto [MPa]
    """
    def __init__(self, nombre: str, abscisa: float, perfil: str, tipo: str, cuerpo: int, sumergido: bool, 
                inclinacion_terreno: float, inclinacion_base_zapata: float, recom_parrilla: bool,
                recom_zapata: bool, recom_micropilotes: bool, recom_pilastra: bool, recom_especial: bool,
                ped_pata_a: float, ped_pata_b: float, ped_pata_c: float, ped_pata_d: float,
                f_carga_mp: float, prof_min_desplante: float, gamma_r: float, zona_geotecnia: str,
                este: float = None, norte: float = None, cota: float = None, f_c = None, dv:float = None, dh:float = None
                ):
        self.nombre = nombre
        self.abscisa = abscisa
        self.perfil = perfil
        self.tipo = tipo
        self.cuerpo = cuerpo
        self.sumergido = sumergido
        self.inclinacion_terreno = inclinacion_terreno
        self.inclinacion_base_zapata = inclinacion_base_zapata
        self.recom_parrilla = recom_parrilla
        self.recom_zapata = recom_zapata
        self.recom_micropilotes = recom_micropilotes
        self.recom_pilastra = recom_pilastra
        self.recom_especial = recom_especial
        self.ped_pata_a = ped_pata_a
        self.ped_pata_b = ped_pata_b
        self.ped_pata_c = ped_pata_c
        self.ped_pata_d = ped_pata_d
        self.f_carga_mp = f_carga_mp
        self.prof_min_desplante = prof_min_desplante
        self.gamma_r = gamma_r
        self.zona_geotecnia = zona_geotecnia
        self.este = este
        self.norte = norte
        self.cota = cota
        self.f_c = f_c
        self.dv = dv
        self.dh = dh
        
        