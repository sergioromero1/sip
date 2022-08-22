from cimentaciones.data_services import DataServices

# Esta rutina busca enontrar grupos en las torres
# que no tienen solución con la barra R38-550. Por lo tanto procesa solo
# un subconjunto de las soluciones de cll_dlt_gtc.m_micropilotes_corrida_integrada_2
# nombredo cll_dlt_gtc.m_micropilotes_corrida_integrada_2b, en donde solo
# están los resultados sin esta barra para las 13 torres que no tienen
# solución con la barra R38-550.

def main():
    conn_string = "host=localhost dbname=sip_db user=postgres password=Magnus64"
    esquema = "cll_dlt_gtc"
    data_services = DataServices(conn_string, esquema)
    
    torres_cubiertas = []
    grupos_seleccionados = []
    pocho = data_services.recuperar_mejor_grupo_micropilotes_2b(torres_cubiertas,grupos_seleccionados,20)
    while pocho:
        print(pocho["grupo"], "\t", pocho["cobertura"],"\t",pocho["tipo"],"\t",pocho["resistencia_min_conc"],"\t",pocho["proc_iny"],"\t",pocho["barra_nombre"])
        data_services.guardar_mp_grupo(pocho, "IGU-b")
        torres_cubiertas += pocho["torres_cubiertas"]
        if pocho["cobertura"] < 2:
            pocho = data_services.recuperar_mejor_grupo_micropilotes_2b(torres_cubiertas,grupos_seleccionados,1000)
        elif pocho["cobertura"] < 5:
            pocho = data_services.recuperar_mejor_grupo_micropilotes_2b(torres_cubiertas,grupos_seleccionados,60)
        else:
            pocho = data_services.recuperar_mejor_grupo_micropilotes_2b(torres_cubiertas,grupos_seleccionados,30)

if __name__ == "__main__":
    main()