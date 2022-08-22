from cimentaciones.data_services import DataServices

def main():
    conn_string = "host=localhost dbname=sip_db user=postgres password=Magnus64"
    esquema = "cll_dlt_gtc"
    data_services = DataServices(conn_string, esquema)
    
    torres_cubiertas = []
    grupos_seleccionados = []
    pocho = data_services.recuperar_mejor_grupo_micropilotes_7(torres_cubiertas,grupos_seleccionados,20)
    while pocho:
        print(pocho["grupo"], "\t", pocho["cobertura"],"\t",pocho["tipo"],"\t",pocho["resistencia_min_conc"],"\t",pocho["proc_iny"],"\t",pocho["barra_nombre"])
        data_services.guardar_mp_grupo(pocho, "IRS")
        torres_cubiertas += pocho["torres_cubiertas"]
        if pocho["cobertura"] < 2:
            pocho = data_services.recuperar_mejor_grupo_micropilotes_7(torres_cubiertas,grupos_seleccionados,1000)
        elif pocho["cobertura"] < 5:
            pocho = data_services.recuperar_mejor_grupo_micropilotes_7(torres_cubiertas,grupos_seleccionados,60)
        else:
            pocho = data_services.recuperar_mejor_grupo_micropilotes_7(torres_cubiertas,grupos_seleccionados,30)

if __name__ == "__main__":
    main()