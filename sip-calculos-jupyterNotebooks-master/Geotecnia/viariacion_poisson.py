from cimentaciones.data_services import DataServices
from cimentaciones.perfil import Perfil, Estrato, obtener_perfil
from cimentaciones.cargas import Cargas
from cimentaciones.evaluador_zapatas import EvaluadorZapatas
from cimentaciones.optimizador_zapatas_por_pedestal import OptimizadorZapatasPorPedestal

def main():
    conn_string = "host=p1378.concol.com dbname=sip_db user=test_user password=test_user"
    esquema = "cll_dlt_gtc"
    data_services = DataServices(conn_string, esquema)
    parametros = data_services.listar_parametros("zapata")
    info_cargas = Cargas(data_services)
    lista_torres = data_services.listar_torres()
    torre = [t for t in lista_torres if t["nombre"] == 'TCLL252'][0]
    perfil, _, _ = obtener_perfil(data_services, torre)
    evaluador = EvaluadorZapatas()
    optimizador = OptimizadorZapatasPorPedestal(evaluador)
    resultados = optimizador.optimizar(parametros, torre, perfil, info_cargas, False, 1)
    print("HG={}, S_e={}".format(resultados[3]["HG"], resultados[3]["asentamiento-comp_max"]["S_e"]))
    for ν in [0.3, 0.35, 0.4, 0.45, 0.5]:
        for estrato in perfil:
            estrato.ν = ν
        resultados = optimizador.optimizar(parametros, torre, perfil, info_cargas, False, 1)
        print("ν={}, S_e={}".format(ν, resultados[3]["asentamiento-comp_max"]["S_e"]))

if __name__ == "__main__":
    main()
    