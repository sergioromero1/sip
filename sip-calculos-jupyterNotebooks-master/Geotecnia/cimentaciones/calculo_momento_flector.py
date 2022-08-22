import math
import numpy as np

# def calcular_longitud_camisa(L_b, D_p, f_c, paso, modulos_balastro, theta, d_h, d_v, limite):
#     momentos = calcular_momento_flector(L_b, D_p, f_c, paso, modulos_balastro, theta, d_h, d_v)
#     for momento in reversed(momentos):
#         if (abs(momento[1]) >= limite or abs(momento[2]) >= limite ):
#             return momento[0]
#     return 0.0

def calcular_longitud_camisa(momentos, limite):
    for momento in reversed(momentos):
        if (abs(momento[1]) >= limite or abs(momento[2]) >= limite ):
            return momento[0]
    return 0.0    

def calcular_momento_flector(L_b, D_p, f_c, paso, modulos_balastro, D_f, theta, d_h, d_v):
    d1 = d_h * math.cos(math.radians(theta)) + d_v * math.sin(math.radians(theta))
    R, r, r_ult, n = calcular_matriz_R(L_b, D_p, f_c, paso, modulos_balastro, D_f)

    ds_a = np.linalg.solve(R[1:,1:], -R[1:,0:1] * d1)
    ds_a = np.vstack((np.array([d1]), ds_a))

    ds_b = np.linalg.solve(R[2:,2:], -R[2:,0:2].dot(np.array([d1, 0])))
    ds_b = ds_b.reshape(ds_b.shape[0], 1)
    ds_b = np.vstack((np.array([0]), ds_b))
    ds_b = np.vstack((np.array([d1]), ds_b))

    curvas_momento = []
    curvas_cortante = []

    x = 0.0
    for k in range(n-1):
        ym_a = r.dot(ds_a[2*k:2*k+4])
        ym_b = r.dot(ds_b[2*k:2*k+4])
        curvas_momento.append((round(x,2), round(float(ym_a[1:2]),3), round(float(ym_b[1:2]),3) ))
        curvas_cortante.append((round(x,2), round(float(ym_a[0:1]),3), round(float(ym_b[0:1]),3) ))
        x += paso

    ym_a = r_ult.dot(ds_a[-4:])
    ym_b = r_ult.dot(ds_b[-4:])
    curvas_momento.append((L_b, round(float(ym_a[3:4]),3), round(float(ym_b[3:4]),3)  ))
    curvas_cortante.append((L_b, round(float(ym_a[2:3]),3), round(float(ym_b[2:3]),3)  ))

    return curvas_momento, curvas_cortante, d1

    # resultados = []
    
    # resultado = []
    # ds = np.linalg.solve(R[1:,1:], -R[1:,0:1] * d1)
    # print(ds.shape)
    # ds = np.vstack((np.array([d1]), ds))
    # x = 0.0
    # for k in range(n-1):
    #     ym = r.dot(ds[2*k:2*k+4])
    #     resultado.append((round(x,2), round(float(ym[0:1]),3), round(float(ym[1:2]),3) ))
    #     x += paso
    # ym = r_ult.dot(ds[-4:])
    # resultado.append((L_b, round(float(ym[2:3]),3), round(float(ym[3:4]),3) ))
    # resultados.append(resultado)

    # resultado = []
    # ds = np.linalg.solve(R[2:,2:], -R[2:,0:2].dot(np.array([d1, 0])))
    # ds = ds.reshape(ds.shape[0], 1)
    # print(ds.shape)
    # ds = np.vstack((np.array([0]), ds))
    # ds = np.vstack((np.array([d1]), ds))
    # x = 0.0
    # for k in range(n-1):
    #     ym = r.dot(ds[2*k:2*k+4])
    #     resultado.append((round(x,2), round(float(ym[0:1]),3), round(float(ym[1:2]),3) ))
    #     x += paso
    # ym = r_ult.dot(ds[-4:])
    # resultado.append((L_b, round(float(ym[2:3]),3), round(float(ym[3:4]),3) ))
    # resultados.append(resultado)

    # return resultados

def calcular_matriz_R(L_b, D_p, f_c, paso, modulos_balastro, D_f):
    # n: número de nodos
    n = math.ceil(L_b / paso) + 1
    ultimo_paso = L_b - (n - 2) * paso
    
    I = 1 / 4 * math.pi * (D_p / 2)**4
    E = 4700.0 * math.sqrt(max(f_c, 25)) * 1000.0
    
    r = calcular_matriz_r(I, E, paso)
    r_ult = calcular_matriz_r(I, E, ultimo_paso)
    # print(f"matriz r, Tipo: {r.dtype}, Shape: {r.shape}")

    R = np.zeros((2 * n, 2 * n), dtype='float64')
    # print(f"matriz R, Tipo: {R.dtype}, Shape: {R.shape}")
    
    for k in range(n-2):
        # R[2*k:2*k+4, 2*k:2*k+4] = R[2*k:2*k+4, 2*k:2*k+4] +  r
        R[2*k:2*k+4, 2*k:2*k+4] += r
    R[-4:,-4:] += r_ult
    
    # Adición de resortes
    b = encontrar_balastro(modulos_balastro, D_f + 0)
    # R[0:1, 0:1] = R[0:1, 0:1] + b * D_p * paso / 2.0
    R[0:1, 0:1] += b * D_p * paso / 2.0
    k = 1
    z = paso
    while z + paso < L_b:
        b = encontrar_balastro(modulos_balastro, D_f + z)
        # R[2*k:2*k+1, 2*k:2*k+1] = R[2*k:2*k+1, 2*k:2*k+1] + b * D_p * paso
        R[2*k:2*k+1, 2*k:2*k+1] += b * D_p * paso
        k += 1
        z += paso
    
    b = encontrar_balastro(modulos_balastro, D_f +z)
    # R[2*k:2*k+1, 2*k:2*k+1] = R[2*k:2*k+1, 2*k:2*k+1] + b * D_p * (paso + ultimo_paso) / 2.0
    R[2*k:2*k+1, 2*k:2*k+1] += b * D_p * (paso + ultimo_paso) / 2.0
    
    k += 1
    z += ultimo_paso
    b = encontrar_balastro(modulos_balastro, D_f + z)
    # R[2*k:2*k+1, 2*k:2*k+1] = R[2*k:2*k+1, 2*k:2*k+1] + b * D_p * ultimo_paso / 2.0
    R[2*k:2*k+1, 2*k:2*k+1] += b * D_p * ultimo_paso / 2.0

    return R, r, r_ult, n

def encontrar_balastro(modulos_balastro, z):
    H = 0.0
    for modulo_balastro in modulos_balastro:
        H += modulo_balastro[0]
        if H > z:
            return modulo_balastro[1]
    return modulos_balastro[-1][1]

def calcular_matriz_r(I, E, L):
    return np.array([
        [ +12*I*E/L**3,  +6*I*E/L**2,  -12*I*E/L**3,  +6*I*E/L**2  ],
        [ +6*I*E/L**2,   +4*I*E/L,     -6*I*E/L**2,   +2*I*E/L     ],
        [ -12*I*E/L**3,  -6*I*E/L**2,  +12*I*E/L**3,  -6*I*E/L**2  ],
        [ +6*I*E/L**2,   +2*I*E/L,     -6*I*E/L**2,   +4*I*E/L     ]
    ])

    