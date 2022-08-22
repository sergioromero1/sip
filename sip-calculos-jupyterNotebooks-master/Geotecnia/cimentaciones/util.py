import math
from typing import List, Dict, Tuple, Any

# Atajos para algunos tipos de datos usados
Memoria = Dict[str, Any]
DBFila = Dict[str, Any]

# π 
π = math.pi

# Peso unitario del agua [kN/m³]
γ_agua = 9.81

def sin_g(ang):
    """Función trigonométrica 'seno' con el ángulo en grados decimales
    
    Arguments:
        ang {float} -- Ángulo en grados decimales
    
    Returns:
        float -- seno del ángulo ang
    """
    return math.sin(math.radians(ang))

def cos_g(ang):
    """Función trigonométrica 'coseno' con el ángulo en grados decimales """
    return math.cos(math.radians(ang))

def tan_g(ang):
    """Función trigonométrica 'tangente' con el ángulo en grados decimales """
    return math.tan(math.radians(ang))

def cot_g(ang):
    """Función trigonométrica 'cotangente' con el ángulo en grados decimales """
    return 1/tan_g(ang)

def rad(ang):
    return ang * math.pi / 180.
    
def calcular_C_d(H:float, B:float) -> float:
    """
    Calcula C_d por interpolación cúbica, caso L/B = 1, ν = 0.50

    Arguments:
        H {float} -- Espesor del estrato [m]
        B {float} -- Ancho de la cimentación [m]

    Returns:
        float -- Valor de C_d interpolado [-]
    """
    H_B = H / B
    C_d = 0.0013 * H_B**3 - 0.0278 * H_B**2 + 0.1983 * H_B - 0.0167

    return C_d

def calcular_I_f(ν, Δz_B):
    dict = {(0.00, 0.35): [(0.2, 0.90),(0.4, 0.81),(0.6, 0.74),(1.0, 0.65)],
            (0.35, 0.45): [(0.2, 0.93),(0.4, 0.85),(0.6, 0.78),(1.0, 0.69)],
            (0.45, 0.51): [(0.2, 0.96),(0.4, 0.89),(0.6, 0.82),(1.0, 0.72)]}
    key = [key for key in dict.keys() if key[0] <= ν and key[1] >= ν][0]
    segmento = dict[key]
    if Δz_B < segmento[0][0]:
        Δz_B = segmento[0][0]
    elif Δz_B > segmento[-1][0]:
        Δz_B = segmento[-1][0]

    iter_izq = [pareja for pareja in segmento if pareja[0] <= Δz_B][-1]
    iter_der = [pareja for pareja in segmento if pareja[0] >= Δz_B][0]
    
    if iter_izq == iter_der:
        return iter_izq[1]
    else:
        return (iter_der[1] - iter_izq[1])/(iter_der[0] - iter_izq[0]) * (Δz_B - iter_der[0]) + iter_der[1]

def generar_serie(x_min, x_max, x_paso, decimales = 2):
    # if x_min > x_max:
    #     return []
    # return [round(x_min + k * x_paso, decimales) for k in range(0, math.floor((x_max - x_min) / x_paso) + 1)]
    if (x_min > x_max or x_paso <= 0 ):
        raise ValueError(f"Valores incorrectos para generar serie: x_min={x_min}, x_max={x_max}, x_paso={x_paso}, decimales={decimales}")
    serie = []
    x = round(x_min, decimales)
    while x <= x_max:
        serie.append(x)
        x = round(x + x_paso, decimales)
    return serie

def format_duracion(sec):
    mins = sec // 60
    sec = sec % 60
    hours = mins // 60
    mins = mins % 60
    return "Duración = {0}:{1}:{2}".format(int(hours),int(mins),sec)