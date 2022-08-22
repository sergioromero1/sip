import copy
from .util import γ_agua, π

class Estrato:
    """Clase que representa un estrato del suelo

    Attributes:
        H_0 {float} -- Espesor [m]
        γ_s {float} -- Peso unitario seco [kN/m³]
        E_s {float} -- Módulo de Young [kN/m²]
        c_u {float} -- Resistencia no drenada [kN/m²]
        φ_s {float} -- Ángulo de fricción [°]
        saturado {bool} -- Indica si el estrato está saturado
        tipo_mat {str} -- Tipo de materia ('c': Cohesivo, 'g': Granular, 'r': Roca)
        N {int} -- Número de golpes [-]
        ν {float} -- Relación de Poisson [-]g
        C_c {float} -- Coeficiente de compresibilidad [-]
        C_s {float} -- Coeficiente de descarga [-]
        c_p {float} -- Cohesión efectiva del suelo [kN/m²]
        ucs {float} -- Resistencia a la compresión simple para la roca [MPa]
        e_0 {float} -- Relación de vacíos inicial [-]
        σ_pp {float} -- Esfuerzo de preconsolidación [kN/m²]
        rechazo {bool} -- Indica si hubo rechazo en el número de golpes
    """
    def __init__(self, H_0: float, γ_s: float = None, E_s: float = None, c_u: float = None, φ_s: float = None, saturado: bool = None, tipo_mat: str = None,
                N: int = None, ν: float = None, C_c: float = None, C_s: float = None, c_p: float = None, ucs: float = None, e_0: float = None, σ_pp: float = None,
                rechazo: bool = False, roca_ν_rm: float = None, roca_a: float = None, roca_s: float = None, roca_m: float = None, roca_E_rm: float = None, 
                roca_φ_rm: float = None, roca_γ: float = None, roca_c_p_rm:float = None,RQD: float = None, suelo_micropilotes=None, origen=None, descripcion=None):
        self.prof_ini = None
        self.prof_fin = None
        self.H_0 = H_0
        self.γ_s = γ_s
        self.saturado = saturado
        self.E_s = E_s
        self.c_u = c_u
        self.φ_s = φ_s
        self.tipo_mat = tipo_mat
        self.N = N
        self.ν = ν
        self.C_c = C_c
        self.C_s = C_s
        self.c_p = c_p
        self.ucs = ucs
        self.e_0 = e_0
        self.σ_pp = σ_pp
        self.rechazo = rechazo
        self.roca_ν_rm = roca_ν_rm
        self.roca_a = roca_a
        self.roca_s = roca_s
        self.roca_m = roca_m
        self.roca_E_rm = roca_E_rm
        self.roca_φ_rm = roca_φ_rm
        self.roca_γ = roca_γ
        self.roca_c_p_rm = roca_c_p_rm
        self.RQD = RQD
        self.suelo_micropilotes = suelo_micropilotes
        self.origen = origen
        self.OCR = None
        self.descripcion = descripcion
        self.E_rs = E_s if tipo_mat != "r" else roca_E_rm
        self.ν_rs = ν if tipo_mat != "r" else roca_ν_rm
        self.γ_rs = (γ_s or roca_γ)
        self.γ_rse = (γ_s or roca_γ) - γ_agua if saturado else (γ_s or roca_γ)
        self.γ_se = (γ_s - γ_agua if saturado else γ_s) if γ_s is not None else None
        self.γ_re = (roca_γ - γ_agua if saturado else roca_γ) if roca_γ is not None else None


        #self.validar_atributos()

    def validar_atributos(self):
        # Valores numéricos positivos obligatorios
        for atributo in ["H_0", "γ_rse"]:
            if not isinstance(self.__dict__[atributo], (int, float)) or self.__dict__[atributo] <= 0:
                raise ValueError("Valor de '{}' no válido: {} ({})".format(atributo, self.__dict__[atributo], self.origen))

        # Valores numéricos positivos no obligatorios
        for atributo in ["ucs", "E_s", "roca_E_rm", "γ_s"]:
            if not isinstance(self.__dict__[atributo], (int, float, type(None))):
                raise ValueError("Valor de '{}' no válido: {} ({})".format(atributo, self.__dict__[atributo], self.origen))
            elif isinstance(self.__dict__[atributo], (int, float)) and self.__dict__[atributo] <= 0:
                raise ValueError("Valor de '{}' no válido: {} ({})".format(atributo, self.__dict__[atributo], self.origen))

        # Valores enteros positivos obligatorios
        for atributo in []:
            if not isinstance(self.__dict__[atributo], (int)) or self.__dict__[atributo] <= 0:
                raise ValueError("Valor de '{}' no válido: {} ({})".format(atributo, self.__dict__[atributo], self.origen))

        # Valores enteros positivos no obligatorios
        for atributo in ["N"]:
            if not isinstance(self.__dict__[atributo], (int, type(None))):
                raise ValueError("Valor de '{}' no válido: {} ({})".format(atributo, self.__dict__[atributo], self.origen))
            elif isinstance(self.__dict__[atributo], (int)) and self.__dict__[atributo] <= 0:
                raise ValueError("Valor de '{}' no válido: {} ({})".format(atributo, self.__dict__[atributo], self.origen))

        # Valores booleanos obligatorios
        for atributo in ["saturado"]:
            if not isinstance(self.__dict__[atributo], (bool)):
                raise ValueError("Valor de '{}' no válido: {} ({})".format(atributo, self.__dict__[atributo], self.origen))
        
        # Tipos de material
        if not self.tipo_mat in ["g", "c", "r"]:
            raise ValueError("Valor de 'tipo_mat' no válido: {} ({})".format(self.tipo_mat, self.origen))

        # Cohesivos deben tener c_u
        if self.tipo_mat == "c" and (not self.c_u or self.c_u == 0):
            raise ValueError("Estrato cohesivo con c_u = 0 ({})".format(self.origen))

        # 
        if self.tipo_mat == "g" and self.c_p is not None and self.c_p != 0:
            raise ValueError("Estrato granular con c_p <> 0 ({})".format(self.origen))

        # 
        if self.tipo_mat == "g" and (self.σ_pp or self.C_s or self.C_c):
            raise ValueError("Estrato granular con σ_pp o C_s o C_c no nulo ({})".format(self.origen))

        # Debe haber un φ_s para cohesivos y granulares
        if self.tipo_mat in ["g", "c"] and not self.φ_s:
            raise ValueError("Falta valor de φ_s para el suelo ({})".format(self.origen))

        # 
        if self.tipo_mat == "c" and self.σ_pp is None:
            raise ValueError("Estrato cohesivo sin valor de σ_pp ({})".format(self.origen))

class Perfil(list):
    """ Lista de estratos (Estrato) con métodos para cálculos sobre ellos
    """
    def __init__(self, estratos, nivel_freatico_exploracion = None, φ_r = None, γ_r = None, prof_lic_inicial = None, prof_lic_final = None):
        list.__init__(self, estratos)
        self.nivel_freatico_exploracion = nivel_freatico_exploracion
        self.φ_r = φ_r
        self.γ_r = γ_r
        self.prof_lic_inicial = prof_lic_inicial
        self.prof_lic_final = prof_lic_final
        self.calcular_profundidades()
        self.calcular_ocr()
        self.NF = self.calcular_NF()
        
        self.validar_datos()

    def validar_datos(self):
        pass

    def calcular_profundidades(self):
        prof = 0.0
        for estrato in self:
            estrato.prof_ini = prof
            estrato.prof_fin = prof + estrato.H_0
            prof += estrato.H_0

    def calcular_ocr(self):
        z_acum = 0.0
        for estrato in self:
            if estrato.tipo_mat == "c" and estrato.saturado:
                q_0 = self.calcular_q(z_acum + estrato.H_0 / 2)
                if estrato.σ_pp is not None:
                    estrato.OCR = estrato.σ_pp / q_0
            z_acum += estrato.H_0

    def calcular_NF(self):
        """Calcula el nivel freático a partir de los atributos 'H_0' y 'saturado' de los estratos"""
        
        if all(not estrato.saturado for estrato in self):
            return None

        return sum([estrato.H_0 for estrato in self if not estrato.saturado])
        
    def calcular_q(self, prof: float):
        """Calcula el esfuerzo en la profundidad prof
        
        Arguments:
            prof {float} -- Profundidad en donde se desea calcular el esfuerzo [m]
        
        Raises:
            ValueError: Profundidad del perfil es insuficiente para calcular el esfuerzo
        
        Returns:
            float -- Esfuerzo [kN/m²]
        """    
        if (sum([estrato.H_0 for estrato in self]) < prof):
            raise ValueError(f"Profundidad de perfil insuficiente ΣH = {sum([estrato.H_0 for estrato in self])}, prof = {prof}")
        
        d = 0.0 # Avance en profundidad
        i = 0   # Índice del estrato actual
        q = 0.0 # Esfuerzo acumulado
        
        while d + self[i].H_0 <= prof:
            q += self[i].H_0 * self[i].γ_rse
            d += self[i].H_0
            i += 1

        if d < prof:
            q += (prof - d) * self[i].γ_rse

        return q

    def calcular_q_con_γ_s(self, prof: float):
        """Calcula el esfuerzo en la profundidad prof, utilizando el γ seco
            aplicable a suelos cohesivos
        
        Arguments:
            prof {float} -- Profundidad en donde se desea calcular el esfuerzo [m]
        
        Raises:
            ValueError: Profundidad del perfil es insuficiente para calcular el esfuerzo
        
        Returns:
            float -- Esfuerzo [kN/m²]
        """    
        if (sum([estrato.H_0 for estrato in self]) < prof):
            raise ValueError(f"Profundidad de perfil insuficiente ΣH = {sum([estrato.H_0 for estrato in self])}, prof = {prof}")
        
        d = 0.0 # Avance en profundidad
        i = 0   # Índice del estrato actual
        q = 0.0 # Esfuerzo acumulado
        
        while d + self[i].H_0 <= prof:
            q += self[i].H_0 * self[i].γ_rs
            d += self[i].H_0
            i += 1

        if d < prof:
            q += (prof - d) * self[i].γ_rs

        return q        

    def estrato_en(self, prof: float):
        """Retorna el estrato que se encuentra en la profundidad prof
        
        Arguments:
            prof {float} -- Profundidad [m]
        
        Raises:
            ValueError: La profundidad D es mayor que la profundidad de los estratos
        
        Returns:
            Estrato -- Estrato en la profundidad D
        """ 

        if (sum([estrato.H_0 for estrato in self]) < prof):
            raise ValueError(f"Profundidad de perfil insuficiente ΣH = {sum([estrato.H_0 for estrato in self])}, prof = {prof}")

        d = 0.0   # Avance en profundidad
        i = 0     # Índice del estrato actual

        while d + self[i].H_0 < prof:
            d += self[i].H_0
            i += 1

        return self[i]

    def calcular_promedio_γ(self, prof: float):
        """Calcula el peso unitario promedio ponderado del suelo hasta la profundidad prof
        
        Arguments:
            prof {float} -- Profundidad [m]
        
        Raises:
            ValueError: La profundidad D es mayor que la profundidad del perfil
        
        Returns:
            float -- Peso unitario promedio del suelo hasta la profundidad D [kN/m³]
        """ 
        if (sum([estrato.H_0 for estrato in self]) < prof):
            raise ValueError(f"Profundidad de perfil insuficiente ΣH = {sum([estrato.H_0 for estrato in self])}, prof = {prof}")

        d = 0.0   # Avance en profundidad
        i = 0     # Índice del estrato actual
        sum_γH = 0.0   # Acumulado de los γ·H

        while d + self[i].H_0 < prof:
            sum_γH += self[i].γ_rse * self[i].H_0
            d += self[i].H_0
            i += 1
        
        if d < prof:
            sum_γH += self[i].γ_rse * (prof - d)

        return sum_γH / prof

    def calcular_promedio(self, prof_ini: float, prof_fin: float, atributo: str, tipo_mat: str = None):
        """Calcula el valor promedio ponderado por espesor del atributo 'atributo' de los estratos
        entre la profundidades 'prof_ini' y 'prof_fin. Si 'tipo_mat' <> None, solo se consideran
        los estratos con el tipo de material 'tipo_mat' para calcular el promedio. Si 'prof_fin'
        es mayor que la profundidad del perfil, el promedio se calcula hasta la profundidad del
        perfil
        
        Arguments:
            prof_ini {float} -- Profundidad inicial [m]
            prof_fin {float} -- Profundidad final [m]
            atributo {float} -- Nombre del atributo
        
        Keyword Arguments:
            tipo_mat {str} -- Tipo de material para filtrar - 'c': Cohesivo, 'g': Granular o 'r': Roca (default: {None})
        
        Returns:
            {float} -- Valor promedio del atributo
        """
        d = 0.0      # Avance en profundidad
        h_acum = 0.0 # Espesor acumulado
        acum = 0.0   # Valor de atributo por espesor acumulado
        for estrato in self:
            if tipo_mat == None or tipo_mat == estrato.tipo_mat:
                if d + estrato.H_0 > prof_ini and d < prof_fin:
                    if estrato.__dict__[atributo] is not None: 
                        if d < prof_ini:
                            if d + estrato.H_0 > prof_fin:
                                dH = prof_fin - prof_ini
                            else:
                                dH = d + estrato.H_0 - prof_ini
                        elif d + estrato.H_0 > prof_fin:
                            dH = prof_fin - d
                        else:
                            dH = estrato.H_0                    
                        acum += estrato.__dict__[atributo] * dH
                        h_acum += dH
                elif d >= prof_fin:
                    break
            d += estrato.H_0
            
        if h_acum == 0:
            return None
        else:
            return acum / h_acum
    
    def calcular_tipo_mat_predominante(self, prof_ini: float, prof_fin: float):
        """Calcula el tipo de material predominante desde prof_ini hasta el mínimo entre
        prof_fin y la profundidad del perfil"""

        d = 0.0 
        acum = {"c": 0, "g": 0, "r": 0}
        for estrato in self:
            if d + estrato.H_0 > prof_ini and d < prof_fin:
                if d < prof_ini:
                    if d + estrato.H_0 > prof_fin:
                        acum[estrato.tipo_mat] += prof_fin - prof_ini
                    else:
                        acum[estrato.tipo_mat] += d + estrato.H_0 - prof_ini
                elif d + estrato.H_0 > prof_fin:
                    acum[estrato.tipo_mat] += prof_fin - d
                else:
                    acum[estrato.tipo_mat] += estrato.H_0
            elif d >= prof_fin:
                break
            d += estrato.H_0
        return max(acum.keys(), key=(lambda key: acum[key]))

    def calcular_tipo_mat_distintos(self, prof_ini: float, prof_fin: float):
        """Retorna la lista de diferentes tipo_mat encontrados desde prof_ini hasta el mínimo entre
        prof_fin y la profundidad del perfil"""
        d = 0.0
        tipos_mat = []
        for estrato in self:
            if round(d + estrato.H_0,2) > prof_ini and d < prof_fin:
                if estrato.tipo_mat not in tipos_mat:
                    tipos_mat.append(estrato.tipo_mat)
            d += estrato.H_0
        return tipos_mat
    
    def calcular_porcentaje_tipo_mat(self, prof_ini: float, prof_fin: float):
        """Retorna el procentaje de tipo de material c, g, r entre las profundidades prof_ini y prof_fin del perfil"""
        d = 0.0
        porc = {"c": 0.0, "g": 0.0, "r": 0.0}
        for estrato in self:
            if d + estrato.H_0 > prof_ini and d < prof_fin:
                if d > prof_ini:
                    if d + estrato.H_0 < prof_fin:
                        porc[estrato.tipo_mat] += estrato.H_0
                    else:
                        porc[estrato.tipo_mat] += prof_fin - d
                else:
                    if d + estrato.H_0 < prof_fin:
                        porc[estrato.tipo_mat] += d + estrato.H_0 - prof_ini
                    else:
                        porc[estrato.tipo_mat] += prof_fin - prof_ini
            elif d >= prof_fin:
                break
            d += estrato.H_0
        
        total = porc["c"] + porc["g"] + porc["r"]
        if total == 0:
            raise ValueError("Error en 'calcular_porcentaje_tipo_mat'. Total porcentajes == 0. prof_ini={}, prof_fin={}".format(prof_ini, prof_fin))
        porc["c"] *= 100.0 / total
        porc["g"] *= 100.0 / total
        porc["r"] *= 100.0 / total

        return porc
    
    def calcular_profundidad_total(self):
        return sum([estrato.H_0 for estrato in self])

    def calcular_profundidad_hasta_roca(self):
        if any([estrato.tipo_mat == "r" for estrato in self]):
            return sum([estrato.H_0 for estrato in self if estrato.tipo_mat != 'r'])
        else:
            return None
    
    profundidad_roca = property(calcular_profundidad_hasta_roca)

    def calcular_material_relleno(self, prof: float):
        if prof == 0:
            return {"tipo_mat": None, "φ": None, "c_u": None, "γ": None}

        porcentajes = self.calcular_porcentaje_tipo_mat(0, prof)
        if porcentajes["r"] >= 70.0:
            tipo_mat = "r"
            φ = 27.0
            c_u = 20
        else:
            fraccion_cohesivo = porcentajes["c"] / (porcentajes["c"] + porcentajes["g"])
            if fraccion_cohesivo >= 0.3:
                tipo_mat = "c"
                φ = 0
                c_u = self.calcular_promedio(0, prof, "c_u", tipo_mat="c") / 2
            else:
                tipo_mat = "g"
                φ = 23.0
                c_u = 0

        NF = self.calcular_NF()
        if NF is not None and NF < prof:
            γ =  self.γ_r - γ_agua
        else:
            γ = self.γ_r
            
        return {"tipo_mat": tipo_mat, "φ": φ, "c_u": c_u, "γ": γ, "γ_total": self.γ_r}

    def clonar_saturado(self):
        nuevos_estratos = []
        for estrato in self:            
            nuevo_estrato = copy.deepcopy(estrato)
            nuevo_estrato.saturado = True
            nuevo_estrato.γ_rse = nuevo_estrato.γ_rs - γ_agua
            nuevo_estrato.γ_se = nuevo_estrato.γ_s - γ_agua if nuevo_estrato.γ_s is not None else None
            nuevo_estrato.γ_re = nuevo_estrato.roca_γ - γ_agua if nuevo_estrato.roca_γ is not None else None
            nuevos_estratos.append(nuevo_estrato)            
        return Perfil(nuevos_estratos, nivel_freatico_exploracion = self.nivel_freatico_exploracion, φ_r = self.φ_r, γ_r = self.γ_r)
        
    def set_nivel_freatico_exploracion(self, nivel_freatico: float):
        self.nivel_freatico_exploracion = nivel_freatico

    def get_nivel_freatico_exploracion(self):
        return self.nivel_freatico_exploracion

    def calcular_suelo_micropilotes(self, prof_ini, prof_fin):
        dict_jerarquia_por_facilidad = {"Suelos cohesivos": 1, "Arena": 2, "Gravas": 3, "Roca blanda": 4, "Roca dura": 5}
        suelos_incluidos = [estrato.suelo_micropilotes for estrato in self if estrato.prof_ini < prof_fin and estrato.prof_fin > prof_ini ]
        suelos_incluidos.sort(key= lambda s: dict_jerarquia_por_facilidad[s])
        return suelos_incluidos[-1]

    def calcular_derrumbabilidad(self, prof: float):
        c_u_derrum = 12.5
        d = 0.0 
        acum = 0.0
        for estrato in self:
            if estrato.tipo_mat == "g" or (estrato.tipo_mat == "c" and estrato.c_u <= c_u_derrum):
                if d + estrato.H_0 < prof:
                    acum += estrato.H_0
                else:
                    acum += prof - d
            d += estrato.H_0
            if d >= prof:
                break
        return acum

    def extender_suelo_a_roca(self, extension: float):
        estratos_a_eliminar = []
        estrato_ant = None
        estrato_suelo = None
        for estrato in self:
            if estrato.tipo_mat == "r":
                if estrato_suelo == None:
                    estrato_suelo = estrato_ant
                    estrato_suelo.prof_fin = round(estrato_suelo.prof_fin + extension, 2)
                    estrato_suelo.H_0 = round(estrato_suelo.H_0 + extension, 2)
                if estrato.H_0 > extension:
                    estrato.prof_ini = round(estrato.prof_ini + extension, 2)
                    estrato.H_0 = round(estrato.H_0 - extension, 2)
                    break
                else:
                    estratos_a_eliminar.append(estrato)
                    extension = round(extension - estrato.H_0, 2)
            estrato_ant = estrato
        for estrato_a_eliminar in estratos_a_eliminar:
            self.remove(estrato_a_eliminar)

    def calcular_modulos_balastro(self, D_p, f_c):
        return [(e.H_0, (0.65 * e.E_rs / D_p / (1.0 - e.ν_rs**2)*(64.0 * e.E_rs / π / 4700000 / max(f_c, 25)**0.5)**(1.0/12.0)) * 0.6) for e in self]

def obtener_perfil(data_services, torre):
    error_en_estratos = False
    mensaje_error = None

    info_estratos = data_services.listar_estratos(torre["perfil"])
    
    if not info_estratos:
        error_en_estratos = True
        mensaje_error = "Perfil no encontrado"
        return None, error_en_estratos, mensaje_error


    estratos = []
    for info_estrato in info_estratos:

        #
        # Validaciones no realizadas por el constructor de Estrato
        #
        if info_estrato["material"] != "ROCA" and not info_estrato["lab_w"]:
            mensaje_error = "Estrato sin valor de w (humedad) ({})".format(info_estrato["origen"])
            error_en_estratos = True
            break

        if info_estrato["material"] == "COHESIVO" and not info_estrato["lab_ip"] :
            mensaje_error =  "Estrato cohesivo sin valor de IP ({})".format(info_estrato["origen"])
            error_en_estratos = True
            break
        
        if info_estrato["material"] != "ROCA" and info_estrato["comp_e"] is None:
            mensaje_error = "Estrato sin valor de comp_e (E_s) ({})".format(info_estrato["origen"])
            error_en_estratos = True
            break

        if info_estrato["prof_ini"] is None or info_estrato["prof_fin"] is None:
            mensaje_error = "Estrato sin valores completos de prof_ini, prof_fin ({})".format(info_estrato["origen"])
            error_en_estratos = True
            break

        H_0 = round(info_estrato["prof_fin"] - info_estrato["prof_ini"], 2)
        γ_s = info_estrato["gamma"]
        E_s = info_estrato["comp_e"] * 1000 if info_estrato["comp_e"]  else None
        c_u = info_estrato["res_c_u"]

        if info_estrato["material"] == "COHESIVO":
            φ_s = info_estrato["res_phi_p_cohesivo"]
            tipo_mat = "c"
        elif info_estrato["material"] == "GRANULAR":
            φ_s = info_estrato["res_phi_p_granular"]
            tipo_mat = "g"
        elif info_estrato["material"] == "ROCA":
            φ_s = None
            tipo_mat = "r"

        if torre["sumergido"] or (info_estrato["nivel_freatico"] and info_estrato["prof_nivel_freatico"] <= info_estrato["prof_ini"]):
            saturado = True
        else:
            saturado = False

        N = info_estrato["n_campo"]
        ν = info_estrato["comp_nu"]
        C_c = info_estrato["comp_c_c"]
        C_s = info_estrato["comp_c_s"]
        c_p = info_estrato["res_c_p"]
        ucs = info_estrato["roca_ucs"]
        e_0 = info_estrato["comp_e_0"]
        σ_pp = info_estrato["comp_sigma_p_p"]
        rechazo = not info_estrato["n_campo"]
        roca_ν_rm = info_estrato["roca_nu"]
        roca_a = info_estrato["roca_a"]
        roca_s = info_estrato["roca_s"]
        roca_m = info_estrato["roca_m_b"]
        roca_E_rm = info_estrato["roca_e_rm"] * 1000 if info_estrato["roca_e_rm"]  else None
        roca_φ_rm = info_estrato["roca_phi_rm"] 
        roca_γ = info_estrato["roca_gamma"]
        roca_c_p_rm = info_estrato["c_p_rm"] * 1000 if info_estrato["c_p_rm"] else None
        RQD = info_estrato["roca_rqd"]
        suelo_micropilotes = info_estrato["suelo_micropilotes"]
        origen = info_estrato["origen"]
        descripcion = info_estrato["descripcion"]
        try:
            estratos.append(Estrato(H_0 = H_0,
                                    γ_s = γ_s,
                                    E_s = E_s,
                                    c_u = c_u,
                                    φ_s = φ_s,
                                    saturado = saturado,
                                    tipo_mat = tipo_mat,
                                    N = N,
                                    ν = ν,
                                    C_c = C_c,
                                    C_s = C_s,
                                    c_p = c_p,
                                    ucs = ucs,
                                    e_0 = e_0,
                                    σ_pp = σ_pp,
                                    rechazo = rechazo,
                                    roca_ν_rm = roca_ν_rm,
                                    roca_a = roca_a,
                                    roca_s = roca_s,
                                    roca_m = roca_m,
                                    roca_E_rm = roca_E_rm,
                                    roca_φ_rm = roca_φ_rm,
                                    roca_γ = roca_γ,
                                    roca_c_p_rm = roca_c_p_rm,
                                    RQD = RQD,
                                    suelo_micropilotes = suelo_micropilotes,
                                    origen = origen,
                                    descripcion= descripcion))
        except ValueError as err:
            error_en_estratos = True
            mensaje_error = str(err)
            break
    
    if error_en_estratos:
        return None, error_en_estratos, mensaje_error
    else:
        perfil = Perfil(estratos, info_estratos[0]["prof_nivel_freatico"], γ_r = torre["gamma_r"])
        return perfil, error_en_estratos, mensaje_error
