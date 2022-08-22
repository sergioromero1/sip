import numpy as np
from cimentaciones.calculo_momento_flector import calcular_momento_flector, calcular_matriz_R, calcular_matriz_r, calcular_longitud_camisa

def main():
    L_b = 4.5
    D_p = 0.115
    f_c = 28
    paso = 0.01
    theta = 5.906892478
    d_h =  0.0045
    d_v = -0.003
    modulos_balastro = [(1.3, 18853.134),(1, 22789.5),(1, 24146.388),(1, 69522.18),(2, 63997.86),(3.7, 78342.96)]
    # # R, r, r_ult, n = calcular_matriz_R(L_b, D_p, f_c, paso, modulos_balastro)
    # #np.savetxt('m_R.txt', R, delimiter=',')
    # # np.savetxt('m_r_.txt', r, delimiter=',')
    # resultado = calcular_momento_flector(L_b, D_p, f_c, paso, modulos_balastro, theta, d_h, d_v)
    # #np.savetxt('x.txt', x, delimiter=',')
    # file1 = open(r"F:\WSP\Proyectos\1378\Mariella\momento_flector\result.txt", "w")
    # file1.write(str(resultado))
    # #print(resultado)
    # print("Done")
    # # calcular_momento_flector(L_b, D_p, f_c, paso, modulos_balastro, θ, δ_h, δ_v)
    longitud_camisa = calcular_longitud_camisa(L_b, D_p, f_c, paso, modulos_balastro, theta, d_h, d_v, 4)
    print(longitud_camisa)


if __name__ == "__main__":
    main()    
