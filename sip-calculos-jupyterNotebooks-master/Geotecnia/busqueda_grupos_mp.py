from cimentaciones.data_services import DataServices

def main():
    conn_string = "host=localhost dbname=sip_db user=postgres password=Magnus64"
    esquema = "cll_dlt_gtc"
    data_services = DataServices(conn_string, esquema)
    
    pefijo_conjunto = "IRS"
    # estrategia = "c_cob_lc"
    # corrida_integrada_id = '25a'
    estrategia = "c_cob"
    corrida_integrada_id = '25'
    porcentaje_sobrecosto = 15
    torres_cubiertas = []
    grupos_seleccionados = []

    if estrategia == "b_cob":
        recuperar_mejor_grupo_micropilotes = data_services.recuperar_mejor_grupo_micropilotes_b_cob
    elif estrategia == "c_cob":
        recuperar_mejor_grupo_micropilotes = data_services.recuperar_mejor_grupo_micropilotes_c_cob
    elif estrategia == "c_cob_lc":
        recuperar_mejor_grupo_micropilotes = data_services.recuperar_mejor_grupo_micropilotes_c_cob_lc
    elif estrategia == "b_nm":
        recuperar_mejor_grupo_micropilotes = data_services.recuperar_mejor_grupo_micropilotes_b_nm

    pocho = recuperar_mejor_grupo_micropilotes(torres_cubiertas,grupos_seleccionados,porcentaje_sobrecosto, corrida_integrada_id)
    while pocho:
        print(pocho["grupo"], "\t", pocho["cobertura"],"\t",pocho["tipo"],"\t",pocho["resistencia_min_conc"],"\t",pocho["proc_iny"],"\t",pocho["barra_nombre"])
        if estrategia == 'c_cob_lc':
            data_services.guardar_mp_grupo_lc(pocho, f"{pefijo_conjunto}-{estrategia}-{porcentaje_sobrecosto}%-i{str(corrida_integrada_id)}")
        else:
            data_services.guardar_mp_grupo(pocho, f"{pefijo_conjunto}-{estrategia}-{porcentaje_sobrecosto}%-i{str(corrida_integrada_id)}")
        torres_cubiertas += pocho["torres_cubiertas"]
        grupos_seleccionados.append(pocho["grupo"])
        if pocho["cobertura"] < 2:
            pocho = recuperar_mejor_grupo_micropilotes(torres_cubiertas,grupos_seleccionados,100, corrida_integrada_id)
        elif pocho["cobertura"] < 5:
            pocho = recuperar_mejor_grupo_micropilotes(torres_cubiertas,grupos_seleccionados,60, corrida_integrada_id)
        else:
            pocho = recuperar_mejor_grupo_micropilotes(torres_cubiertas,grupos_seleccionados,porcentaje_sobrecosto, corrida_integrada_id)

if __name__ == "__main__":
    main()