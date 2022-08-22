import math
from scipy import optimize
from .util import *

##########################################
# Utilitarios
##########################################
def peso_pila(D_p, B_p, B_c, h_c, θ_c, C, TP, θ, γ_c):
    """
    Calcula del peso de la pila .

    Parameters:
        D_p: Longitud la pila [m]
        B_p: Diámetro de la pila [m]
        B_c: Diámetro de la campana de la pila [m]. Si es pila recta B_c == B_p
        h_c: Altura de la base campana [m]
        θ_c: Ángulo de la campana [°]
        C:   Altura total del pedestal [m]
        TP:  Lado correspondiente a la sección transversal del pedestal [m]
        θ:   Ángulo del pedestal respecto a la vertical [°]
        γ_c: Peso unitario de la cimentación [kN/m³]

    Returns:
        W_p:  Peso de la cimentación [kN]

    Problemas/dudas:
        Agregar el peso de la campana
    """

    # W_p:  Peso de la cimentación, sección recta [kN]
    W_p = (D_p * π * B_p**2 / 4 + TP**2 * C / cos_g(θ)) * γ_c

    # Ajuste del peso por la campana [kN]
    if B_c != B_p:
        h = (B_c - B_p) / 2 / tan_g(θ_c)              # Altura de la sección cónica
        V1 = h * π / 3 *(B_c**2 + B_p**2 + B_c * B_p) # Volumen de la sección cónica
        V2 = π / 4 * B_c ** 2 * (h_c - h)             # Volumen de la sección cilíndrica
        V3 = π / 4 * B_p ** 2 * h_c                   # Volumen de la sección cilíndrica de la pila recta
        W_p += (V1 + V2 - V3) * γ_c

    return W_p

##########################################
# Cálculos capacidad portante
##########################################
def calculos_capacidad_portante_suelos_granulares(B_p, B_c, γ_p, condicion_de_saturacion, ϕ, σ_p):
    """
    Calcula las capacidad portante última para suelos granulares.

    Parameters:
        B_p: Diámetro de la pila [m]
        B_c:  Diámetro de la campana de la pila [m] = B_p si pila recta
        γ_p: Peso unitario del suelo, bajo la condicón de saturación encontrado [kN/m³]
        condicion_de_saturacion: 'seco' o 'sumergido'
        ϕ:   Ángulo de fricción interna del suelo [°]
        σ_p: Esfuerzo efectivo vertical en la punta de la pila [kN/m²]

    Returns:
        Q_u:  Capacidad portante última [kN]

    Problemas/dudas:
        ¿Se necesita el parámetro 'condicion_de_saturacion' para sumergencia? ¿Tiene que ver con el NF (nivel freático)?
    """

    # Calcula γ_p efectivo si está en condición de sumergencia
    if condicion_de_saturacion == "sumergido":
        γ_p = γ_p - γ_agua

    # S_q: Factor de forma debido a la sobrecarga para círculo [-]
    S_q = 1.2

    # S_γ: Factor de forma debido al peso unitario del suelo para círculo [-]
    S_γ = 0.6

    # N_q: Factor de capacidad portante debido a la sobrecarga. [-]
    N_q = math.exp(π * tan_g(ϕ)) * tan_g(45 + ϕ / 2)**2

    # N_γ: Factor de capacidad portante debido al peso unitario del suelo de fundación. [-]
    N_γ = 2 * (N_q + 1) * tan_g(ϕ)

    # A_p: Área de la pila en la punta [m²]
    A_p = π / 4 * B_c ** 2

    # Q_p: Capacidad portante última por punta de la pila [kN]
    Q_p = (0.5 * γ_p * B_p * N_γ * S_γ + σ_p * N_q * S_q) * A_p

    # K: Coeficiente de presión lateral de tierras [-] 
    K = 1 - sin_g(ϕ) 
    
    # δ: Fricción entre el suelo y la pila [-]
    δ = 2 * ϕ / 3

    # A_s: Área del fuste de la pila [m²]
    A_s = π / 4 * B_p ** 2

    # Q_s: Capacidad portante por fuste [kN]
    Q_s = K * σ_p * A_s * tan_g(δ)

    # Q_u: Capacidad portante última [kN]
    Q_u = Q_p + Q_s 

    return Q_u

def calculos_capacidad_portante_suelos_cohesivos(B_p, B_c, c_u, C_avg):
    """
    Calcula la capacidad portante última para suelos cohesivos.

    Parameters:
        B_p: Diámetro de la pila [m]
        B_c: Diámetro de la campana de la pila [m] = B_p si pila recta

        c_u: Resistencia al corte no drenada [kN/m²]
        C_avg: Resistencia no drenada promedio del suelo a lo largo de la pila [kN/m²]

    Returns:
        Q_u:  Capacidad portante última [kN]
    """    
    # A_p: Área de la pila en la punta [m²]
    A_p = π / 4 * B_c ** 2

    # q_0: Valor unitario de capacidad portante por punta [kN/m²]
    q_0 = 9 * c_u

    # Q_p: Capacidad portante última por punta de la pila [kN]
    Q_p = q_0 * A_p

    # A_s: Área del fuste de la pila [m²]
    A_s = π / 4 * B_p ** 2

    # α: Factor de adhesión suelo–pila que se encuentra en función de la resistencia al corte no drenada del suelo, c_u [-]
    α = 18.03 * c_u ** (-0.77)

    # Q_s: Capacidad portante por fuste [kN]
    Q_s = α * C_avg * A_s

    # Q_u: Capacidad portante última [kN]
    Q_u = Q_p + Q_s 

    return Q_u

##########################################
# Cálculos tensión
##########################################
def calculos_tension_falla_vertical_pila_recta_suelos_granulares(D_p, p, C, TP, θ, γ_c, e, ϕ, σ):
    """
    Calcula las capacidad a la tensión para pila recta con modelo de falla vertical y suelos granulares.

    Parameters:
        D_p: Longitud efectiva de la pila [m]
        p:   Perímetro de la pila [m]
        C:   Altura total del pedestal [m]
        TP:  Lado correspondiente a la sección transversal del pedestal [m]
        θ:   Ángulo del montante con respecto a la vertical [°]
        γ_c: Peso unitario de la cimentación [kN/m³]
        e:   Excentricidad de la pila [m]

        ϕ:   Ángulo de fricción interna del suelo [°]
        σ:   Esfuerzo efectivo vertical promedio en la longitud de la pila [kN/m²]

    Returns:
        T_u: Capacidad a la tensión última [kN]    
    """
    # K_s: Coeficiente de presión lateral de tierras [-]
    K_s = 1 - sin_g(ϕ)

    # W_p: Peso efectivo de la pila [kN]
    B_p = p / π # Diámetro de la pila
    W_p = peso_pila(D_p + e, B_p, B_p, 0, 0,C, TP, θ, γ_c)

    # δ: Ángulo de fricción entre el suelo y la pila [°]
    δ = 2 * ϕ / 3

    # Q_fs: Resistencia última por fricción [kN] 
    Q_fs = p * K_s * tan_g(δ) * σ * D_p

    # T_u: Capacidad a la tensión última [kN]
    T_ug = Q_fs + W_p
    
    return T_ug

def calculos_tension_falla_vertical_pila_recta_suelos_cohesivos(D_p, p, B_c, h_c, θ_c, C, TP, θ, γ_c, c_u):
    """
    Calcula las capacidad a la tensión para pila recta con modelo de falla vertical y suelos cohesivos.

    Parameters:
        D_p:  Longitud de la pila [m]
        p:    Perímetro de la pila [m]
        B_c: Diámetro de la campana de la pila [m]. Si es pila recta B_c == B_p
        h_c: Altura de la base campana [m]
        θ_c: Ángulo de la campana [°]
        C:   Altura total del pedestal [m]
        TP:  Lado correspondiente a la sección transversal del pedestal [m]
        θ:   Ángulo del montante con respecto a la vertical [°]
        γ_c: Peso unitario de la cimentación [kN/m³]

        c_u:  Resistencia al corte no drenada [kN/m²]
    Returns:
        T_u:  Capacidad última a la tensión [kN]
    """
    # W_p: Peso efectivo de la pila [kN]
    B_p = p / π # Diámetro de la pila    
    W_p = peso_pila(D_p, B_p, B_c, h_c, θ_c, C, TP, θ, γ_c)

    # α: Factor de adhesión suelo–pila que se encuentra en función de la resistencia al corte no drenada del suelo, c_u [-]
    α = 18.03 * (c_u / 9.8)** (-0.77)

    # δ: Ángulo de fricción entre el suelo y la pila [°]
    c_a = α * c_u

    # Q_fs: Resistencia última por fricción [kN] 
    Q_fs = p * c_a * D_p

    # T_u: Capacidad última a la tensión [kN]
    T_ug = Q_fs + W_p
    
    return T_ug

def calculos_tension_falla_vertical_pila_campana_suelos_cohesivos(D_p, B_p, B_c, C, TP, θ, γ_c, c_u):
    """
    Calcula las capacidad a la tensión para pila ensanchada en la base con modelo de falla vertical y suelos cohesivos.

    Parameters:
        D_p:  Longitud efectiva de la pila [m]
        B_p:  Diámetro de la pila [m]
        B_c:  Diámetro de la campana de la pila [m]
        γ_c: Peso unitario de la cimentación [kN/m³]

        c_u:  Resistencia al corte no drenada [kN/m²]

    Returns:
        T_u:  Capacidad última a la tensión [kN]    
    """

    # W_p: Peso efectivo de la pila [kN]
    W_p = peso_pila(D_p, B_p, B_c, 0, 0, C, TP, θ, γ_c)

    # N_c:  Constante de capacidad a la tensión, para el caso de suelos cohesivos en cimentaciones profundas es igual a 9 [-]
    N_c = 9

    # T_u:  Capacidad última a la tensión [kN]
    T_ug = min( π / 4 * (B_c**2 - B_p**2) * c_u * N_c + W_p, π / 2 * (B_c + B_p) * c_u * D_p + W_p)

    return T_ug

def interpolar_ku(ϕ):
    """
    Interpola la curva lineal a trozos de Ku(ϕ)
    """
    ϕs = [20, 25, 30, 35, 40, 45]
    kus = [0.856, 0.888, 0.920, 0.936, 0.960, 0.960]

    if ϕ < ϕs[0] or ϕ > ϕs[-1]:
        raise ValueError("Valor ϕ fuera de rango [20 - 45]: " + str(ϕ))

    i1 = [i for i in range(len(ϕs)) if ϕs[i] <= ϕ ][-1] 
    i2 = [i for i in range(len(ϕs)) if ϕs[i] >= ϕ ][0]

    if i1 == i2:
        return kus[i1]
    else:
        return (kus[i2] - kus[i1]) / (ϕs[i2] - ϕs[i1]) * (ϕ - ϕs[i1])   + kus[i1] 

def interpolar_m(ϕ):
    """
    Interpola la curva lineal a trozos de m(ϕ)
    """
    ϕs = [20, 25, 30, 35, 40, 45]
    ms = [0.05, 0.10, 0.15, 0.25, 0.35, 0.50]

    if ϕ < ϕs[0] or ϕ > ϕs[-1]:
        raise ValueError("Valor ϕ fuera de rango [20 - 45]: " + str(ϕ))

    i1 = [i for i in range(len(ϕs)) if ϕs[i] <= ϕ ][-1] 
    i2 = [i for i in range(len(ϕs)) if ϕs[i] >= ϕ ][0]

    if i1 == i2:
        return ms[i1]
    else:
        return (ms[i2] - ms[i1]) / (ϕs[i2] - ϕs[i1]) * (ϕ - ϕs[i1])   + ms[i1] 

def calculos_tension_falla_tronco_piramidal_suelos_granulares(D_p, B_p, B_c, h_c, θ_c, C, TP, θ, γ_c, e, γ_s, ϕ):
    """
    Calcula las capacidad total última a la tensión para pila falla tronco piramidal para suelos granulares.

    Parameters:
        D_p: Longitud efectiva de la pila [m]
        B_p: Diámetro de la pila [m]
        B_c: Diámetro de la campana de la pila [m] = B_p si pila recta
        h_c: Altura de la base campana [m]
        θ_c: Ángulo de la campana [°]
        C:   Altura total del pedestal [m]
        TP:  Lado correspondiente a la sección transversal del pedestal [m]
        θ:   Ángulo del montante con respecto a la vertical [°]
        γ_c: Peso unitario de la cimentación [kN/m³]
        e:   Excentricidad de la pila [m]

        γ_s: Peso unitario del suelo [kN/m³]
        ϕ:   Ángulo de fricción interna del suelo [°]

    Returns:
        T_ug:  Capacidad total última a la tensión [kN]    
    """    
    # Área de la base de la pila (Si es pila recta B_c = B_p)
    A_p = π / 4 * B_c ** 2

    # K_u: Coeficiente nominal de levantamiento [-]
    K_u = interpolar_ku(ϕ)

    # m: Coeficiente de factor de forma [-]
    m = interpolar_m(ϕ)

    # Factor de arrancamiento [-]
    B_q = 2 * D_p / B_c * K_u * tan_g(ϕ) *(m * D_p / B_c + 1) + 1
    
    # T_ug: Capacidad a la tensión [kN]
    T_un = B_q * A_p * γ_s * D_p
    
    # W_p: Peso efectivo de la pila [kN]
    W_p = peso_pila(D_p + e, B_p, B_c, h_c, θ_c, C, TP, θ, γ_c)

    # T_ug: Capacidad total última a la tensión [kN]
    T_ug = T_un + W_p
    
    return T_ug

def calculos_tension_falla_tronco_piramidal_suelos_cohesivos(D_p, B_p, B_c, h_c, θ_c, C, TP, θ, γ_c, γ_s, ϕ, c_u):
    """
    Calcula las capacidad total última a la tensión para pila falla tronco piramidal para suelos cohesivos.

    Parameters:
        D_p: Longitud efectiva de la pila [m]
        B_p: Diámetro de la pila [m]
        B_c: Diámetro de la campana de la pila [m]
        h_c: Altura de la base campana [m]
        θ_c: Ángulo de la campana [°]
        C:   Altura total del pedestal [m]
        TP:  Lado correspondiente a la sección transversal del pedestal [m]
        θ:   Ángulo del montante con respecto a la vertical [°]
        γ_c: Peso unitario de la cimentación [kN/m³]

        γ_s: Peso unitario del suelo [kN/m³]
        ϕ:   Ángulo de fricción interna del suelo [°]
        c_u: Resistencia al corte no drenada [kN/m²]

    Returns:
        T_ug:  Capacidad total última a la tensión [kN]

    Problemas/dudas:
    """    
    # Área de la base de la pila (Si es pila recta B_c = B_p)
    A_p = π / 4 * B_c ** 2

    # K_u = coeficiente nominal de levantamiento [-]
    K_u = interpolar_ku(ϕ)

    # m = coeficiente de factor de forma [-]
    m = interpolar_ku(ϕ)
    
    # β: Factor de desconexión [-]
    β = 2 * D_p / B_c * K_u * tan_g(ϕ) * (m * D_p / B_c + 1) + 1
    
    # T_un: Capacidad a la tensión [kN]
    T_un = (c_u * β + γ_s * D_p) * A_p

    # W_p: Peso efectivo de la pila [kN]
    W_p = peso_pila(D_p, B_p, B_c, h_c, θ_c, C, TP, θ, γ_c)

    # T_ug: Capacidad total última a la tensión [kN]
    T_ug = T_un + W_p

    return T_ug
    
##########################################
# Cálculos cargas laterales
##########################################
def calculos_carga_lateral_pilas_cortas_suelos_granulares(D_p, B_p, e, ϕ, γ_p):
    """
    Calcula resistencia última a la carga lateral para pilas cortas en suelos granulares.

    Parameters:
        D_p: Longitud de la pila [m]
        B_p: Diámetro de la pila [m]
        e:   Excentricidad del pedestal [m]

        ϕ:   Ángulo de fricción interna del suelo [°]
        γ_p: Peso unitario del suelo, si existe condición de sugerencia se usará el peso unitario efectivo [kN/m³]

    Returns:
        H_u:  Resistencia última a la carga lateral [kN]

    Problemas/dudas:
        ¿Cómo se calcula el γ_p peso unitario efectivo en caso de sumergencia?
    """

    # K_p: Coeficiente de presión pasiva de tierras [-]
    K_p = tan_g(45 + ϕ / 2)**2

    # H_u:  Resistencia última a la carga lateral [kN]
    H_u = 0.5 * γ_p * D_p**3 * B_p * K_p / (e + D_p)

    return H_u

def calculos_carga_lateral_pilas_cortas_suelos_cohesivos(D_p, B_p, e, c_u):
    """
    Calcula resistencia última a la carga lateral para pilas cortas en suelos cohesivos.

    Parameters:
        D_p: Longitud de la pila [m]
        B_p: Diámetro de la pila [m]
        
        e:   Excentricidad del pedestal [m]
        c_u: Resistencia no drenada del suelo [kN/m²]

    Returns:
        H_u:  Resistencia última a la carga lateral [kN]

    Problemas/dudas:
        ¿Se entendió bien la solución... resolver la cuadrática (escoger solución positiva) o encontrar ceros de la expresión del libro pag. 58?
    """ 
    # H_u: Resistencia última a la carga lateral [kN]
    x = e + 1.5 * B_p + 0.5 * D_p
    H_u = (math.sqrt(x**2 + D_p **2 / 4) - x) * 18 * c_u * B_p

    return H_u

    # try:
    #     # H_u: Resistencia última a la carga lateral [kN]
    #     H_u = optimize.newton(func= zero_hu_suelos_cohesivos, x0= 0, fprime= d_zero_hu_suelos_cohesivos , args= (D_p, B_p, e, c_u))

    #     return H_u
    # except:
    #     raise ValueError("No encontró cero para H_u: Resistencia última a la carga lateral para pila, suelos cohesivos")

# def zero_hu_suelos_cohesivos(H_u, D_p, B_p, e, c_u):
#     return H_u * (e + 1.5 * B_p + 0.5 * H_u / 9 / c_u / B_p) - 2.25 * B_p * c_u * (D_p - H_u / 9 / c_u / B_p)**2

# def d_zero_hu_suelos_cohesivos(H_u, D_p, B_p, e, c_u):
#     return e + 1.5 * B_p + 0.5 * D_p + H_u / 9 / c_u / B_p

def calculos_carga_lateral_pilas_largas_suelos_granulares(B_p, e, γ_p, condicion_de_saturacion, K_p, M_y):
    """
    Calcula resistencia última a la carga lateral para pilas largas en suelos granulares.

    Parameters:
        B_p: Diámetro de la pila [m]
        
        e: Excentricidad del pedestal [m]
        γ_p: Peso unitario del suelo, si existe condición de sugerencia se usará el peso unitario efectivo [kN/m³]
        K_p: Coeficiente de presión pasiva de tierras [-]

        M_y: Momento de fluencia para la pila [kN·m] 

    Returns:
        H_u:  Resistencia última a la carga lateral [kN]

    Problemas/dudas:
        ¿Se entendió bien la solución... encontrar ceros de la expresión del libro pag. 58?
        ¿Cómo se calcula el γ_p peso unitario efectivo en caso de sumergencia?
        ¿El coeficiente de presión pasiva de tierras K_p es input o se calcula?
    """     
    try:
        # H_u: Resistencia última a la carga lateral [kN]
        H_u = optimize.newton(func= zero_hu_pilas_largas_suelos_granulares, x0= 0, fprime= d_zero_hu_pilas_largas_suelos_granulares , args= (B_p, e, γ_p, K_p, M_y))

        return H_u
    except:
        raise ValueError("No encontró cero para H_u: Resistencia última a la carga lateral para pila, suelos granulares")

def zero_hu_pilas_largas_suelos_granulares(H_u, B_p, e, γ_p, K_p, M_y):
    return H_u - M_y / (e + 0.54 * (H_u / γ_p / B_p / K_p)**0.5)

def d_zero_hu_pilas_largas_suelos_granulares(H_u, B_p, e, γ_p, K_p, M_y):
    x = H_u / H_u / γ_p / B_p / K_p
    return 1 + 0.27 * M_y * γ_p * B_p * K_p / (e**2 * x**0.5 + 1.08 * x + 0.2916 * x**1.5)

def modulo_reaccion_horizontal(B_p, E_p, I_p, E_s, ν_s, d):
    """
    Calcula el módulo de racción horizontal.

    Parameters:
        B_p: Diámetro de la pila [m]
        E_p: Módulo de elasticidad del material de la pila [kN/m²]
        I_p: Momento de inercia de la sección [m4]
        
        E_s: Módulo elástico del suelo [kN/m²]
        ν_s: Relación del Poisson del suelo
        d: ?????

    Returns:
        k: Módulo de racción horizontal [?]

    Problemas/dudas:
        ¿Qué es d?
    """
    k = 0.65 / B_p *(E_s * d**4 / E_p / I_p)**(1/12) * E_s / (1 - ν_s**2)

    return k

##########################################
# Cálculos volcamiento
##########################################
def calculos_volcamiento_pilas_cortas(Hs, D_p, HG, α, h, γ, f_s, K_p, CV, F_v, F_h):
    """
    Calcula la longitud de la pila y la longitud requerida para evitar el volcamiento.

    Parameters:
        Hs:  Longitud de la pila [m]
        D_p: Diámetro de la pila [m]
        HG:  Altura del pedestal que sobresale del terreno [m]
        α:   Ángulo entre el montante y la vertical [°]

        h: Profundidad de suelo no competente [m]
        γ: Peso unitario del suelo [kN/m³]

        M_y: Momento de fluencia para la pila [kN·m] 

    Returns:
        Tupla (L_req, Hs)

    Problemas/dudas:
        La figura 2.13 (pag 72) muestra a F_v hacia arriba. 
        ¿Cómo se calcula CV, CV = P_p (Peso propio de la pila) o es input?
        El documento dice que es necesario un método iterativo para calcular L_req, pero no parece necesario... se puede despejar L_req (lineal)
        ¿Qué pasa con pilas largas?
    """        
    # R_p: Fuerza resultante del empuje pasivo [kN]
    R_p = 1 / 2 * γ * Hs * K_p * D_p

    # L_req: Longitud requerida para evitar el volcamiento [m]
    L_req = (F_v * D_p / 2 - CV * D_p / 2 - F_h * tan_g(α) * (HG + h)) / (R_p / 3 + π / 3 * D_p**2 * f_s - F_h)

    return (Hs, L_req)

##########################################
# Cálculos asentamientos
##########################################
def calculos_asentamiento_metodo_transferencia_carga(D_p, B_p, B_c, I_p, E_p, E_s, ν, Q_ws, Q_wp):
    """
    Calcula el asentamiento en pilas por el método de transferencia de carga

    Parameters:
        D_p: Longitud efectiva de la pila [m]
        B_p: Diámetro de la pila [m]
        B_c: Diámetro de la campana [m]
        I_p: Factor de influencia dependiente de la relación D_p/B [-]
        E_p: Módulo de Young del material de la pila [kN/m²]
        E_s: Módulo de Young del suelo bajo la pila [kN/m²]
        ν:   Relación de Poisson de suelo [-]
        Q_ws:Carga de trabajo por fuste [kN]
        Q_wp:Carga de trabajo por punta [kN]
    
    Returns:
        ρ: Asentamiento [m]

    Problemas/dudas:
        ¿I_p se calcula o es input?
        ¿ Se calcula ν según la fórmula en:
                # ϕ_rel: Ángulo de fricción relativo [-]
                ϕ_rel = (ϕ - 25) / 20
                
                # ν: Relación de Poisson [-]
                ν = 0.1 + 0.3 * ϕ_rel?
        ¿Q_ws y Q_wp ?
    """
    # A_s: Área del fuste de la pila [m²]
    A_s = π / 4 * B_p ** 2     

    # A_p: Área de la pila en la punta [m²]
    A_p = π / 4 * B_c ** 2

    # ρ: Asentamiento [m]
    ρ = (Q_ws + 2 * Q_wp) * D_p /2 /A_s / E_p + π * Q_wp * B_p * (1 - ν**2) * I_p / 4 / A_p / E_s

    return ρ

def calculos_asentamiento_metodo_empirico_vesic(D_p, B_p, B_c, E_p, Q_w):
    """
    Calcula el asentamiento en pilas por el método empirico de Vesic

    Parameters:
        D_p: Longitud efectiva de la pila [pulg]
        B_p: Diámetro de la pila [pulg]
        B_c: Diámetro de la campana [pulg]
        E_p: Módulo de Young del material de la pila [lb/pulg²]
        Q_w: Carga de trabajo[lb]
    
    Returns:
        ρ: Asentamiento [pulg]

    Problemas/dudas:
        Sistema de unidades !!!
    """
    
    # A_p: Área de la pila en la punta [m²]
    A_p = π / 4 * B_c ** 2
    
    # ρ: Asentamiento [m]
    ρ = B_p / 100 + Q_w * D_p / A_p / E_p

    return ρ