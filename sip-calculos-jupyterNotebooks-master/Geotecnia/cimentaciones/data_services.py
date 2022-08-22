import psycopg2
import psycopg2.extras
from configparser import ConfigParser
from typing import List, Dict, Tuple, Any
from .util import DBFila, generar_serie
from .perfil import Perfil
from .torre import Torre
import json

class DataServices():

    def __init__(self, conn_string: str, esquema: str):
        self.conn_string = conn_string
        self.esquema = esquema

    def listar_torres(self) -> List[DBFila]:
        """
        Consulta las torres de la base de datos. Las columnas requeridas son:
            nombre {varchar}                 -- Nombre de la torre
            abscisa {float8}                 -- Abscisa [m] 
            perfil {varchar}                 -- Nombre del perfil estratigráfico de la torre. Normalmente coincide con el nombre de la torre.
            tipo {varchar}                   -- Nombre del tipo de torre. Debe coincidir con el nombre utilizado en la consulta de cargas
            cuerpo {int}                     -- Número de cuerpos de la torre. Se requiere si las cargas a utilizar no son la envolvente 
            sumergido {boolean}              -- Indica si la torre se encuentra en zona inundable
            inclinacion_terreno {float8}     -- Ángulo de inclinación del terreno en el sitio de torre [°]. Se asume 0 si está nulo.
            inclinacion_base_zapata {float8} -- Ángulo de inclinación de la base de la zapata [°]
            recom_zapata {boolean}           -- Indica si se recomienda zapata para la torre
            recom_micropilotes {boolean}     -- Indica si se recomienda micropilotes para la torre
            recom_pilastra {boolean}         -- Indica si se recomienda pilastra para la torre
            ped_pata_a {float8}              -- Pedestal en la pata A. Se requiere si se desea incluir patas no estándares en el análisis (var parámetro 'hg_por_pata')
            ped_pata_b {float8}              -- Pedestal en la pata B. Se requiere si se desea incluir patas no estándares en el análisis (var parámetro 'hg_por_pata')
            ped_pata_c {float8}              -- Pedestal en la pata C. Se requiere si se desea incluir patas no estándares en el análisis (var parámetro 'hg_por_pata')
            ped_pata_d {float8}              -- Pedestal en la pata D. Se requiere si se desea incluir patas no estándares en el análisis (var parámetro 'hg_por_pata')
            f_carga_mp {float8}              -- Fracción de carga que tomarían los micropilotes en esta torre [0..1]
            prof_min_desplante {float8}      -- Profundidad mínima de desplante recomendada para zapata en suelo [m]
            gamma_r {float}                  -- Peso unitario del relleno en el suelo de la torre [kN/m³].
        
        Arguments:
            esquema {str} -- Nombre del esquema de la línea de transmisión
        
        Returns:
            List[DBFila] -- Lista de diccionarios que representan cada torre
        """        
        try:
            conn = psycopg2.connect(self.conn_string)
            dict_cur: psycopg2.extras.DictCursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            sql = "select * from {}.v_torre order by abscisa".format(self.esquema)
            dict_cur.execute(sql)
            return dict_cur.fetchall()
        except (Exception, psycopg2.Error) as error :
            print ("Error en base de datos", error)
            return None
        
        finally:
            if(conn):
                dict_cur.close()
                conn.close()

    def listar_torres_obj(self) -> List[DBFila]:
        """
        Retorna la lista de torres

        Arguments:
            esquema {str} -- Nombre del esquema de la línea de transmisión
        
        Returns:
            List[Torre] -- Lista de diccionarios que representan cada torre
        """        
        torres = []
        lista_torres = self.listar_torres()
        for info_torre in lista_torres:
            torres.append(Torre(
                info_torre["nombre"],
                info_torre["abscisa"],
                info_torre["perfil"],
                info_torre["tipo"],
                info_torre["cuerpo"],
                info_torre["sumergido"],
                info_torre["inclinacion_terreno"],
                info_torre["inclinacion_base_zapata"],
                info_torre["recom_parrilla"],
                info_torre["recom_zapata"],
                info_torre["recom_micropilotes"],
                info_torre["recom_pilastra"],
                info_torre["recom_especial"],
                info_torre["ped_pata_a"],
                info_torre["ped_pata_b"],
                info_torre["ped_pata_c"],
                info_torre["ped_pata_d"],
                info_torre["f_carga_mp"],
                info_torre["prof_min_desplante"],
                info_torre["gamma_r"],
                info_torre["zona_geotecnia"],
                None, # este
                None, # norte
                None, # cota
                info_torre["resistencia_min_conc"],
                -info_torre["dv"]/1000.0 if info_torre["dv"] is not None else None,
                info_torre["dh"]/1000.0 if info_torre["dh"] is not None else None
            ))
        return torres

    def listar_cargas(self) -> List[DBFila]:
        """
        Consulta las cargas de la base de datos
        
        Arguments:
            esquema {str} -- Nombre del esquema de la línea de transmisión
        
        Returns:
            List[DBFila] -- Lista de diccionarios que representan cada carga
        """        
        try:
            conn = psycopg2.connect(self.conn_string)
            #conn = psycopg2.connect(host = host, dbname = dbname, user = user, password = password)
            dict_cur: psycopg2.extras.DictCursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            sql = (
                    "select tt.nombre as tipo_torre, "
                    "       rc.cuerpo_min, "
                    "       rc.cuerpo_max, "
                    "       gc.nombre as grupo_cargas, "
                    "       tc.nombre as tipo_cargas, "
                    "       c.nombre as componente, "
                    "       vc.valor "
                    "from {}.t_grupo_cargas gc "
                    "join {}.t_tipo_cargas tc on tc.grupo_cargas_id = gc.id "
                    "join {}.t_carga c on c.tipo_cargas_id = tc.id "
                    "join {}.t_valor_carga vc on vc.carga_id = c.id "
                    "join {}.t_rango_cuerpos rc on rc.id = vc.rango_cuerpos_id "
                    "join {}.t_tipo_torre tt on tt.id = rc.tipo_torre_id "
                    "join {}.t_familia_torre ft on ft.id = tt.familia_torre_id "
                    "order by 1,2,4,5,6"
            ).format(*(self.esquema,)*7)
            dict_cur.execute(sql)
            return dict_cur.fetchall()
        
        except (Exception, psycopg2.Error) as error :
            print ("Error en base de datos", error)
            return None
        
        finally:
            if(conn):
                dict_cur.close()
                conn.close()

    def listar_estratos(self, torre: str):
        try:
            conn = psycopg2.connect(self.conn_string)
            dict_cur: psycopg2.extras.DictCursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            sql = """select * 
                    from {}.v_estrato_final
                    where torre = %s 
                    order by prof_ini""".format(self.esquema)
            dict_cur.execute(sql, (torre,))
            recs = dict_cur.fetchall()
            return recs
        
        except (Exception, psycopg2.Error) as error :
            print ("Error en base de datos", error)
            return None
        
        finally:
            if(conn):
                dict_cur.close()
                conn.close()

    def recuperar_sitio(self, torre: str):
        try:
            conn = psycopg2.connect(self.conn_string)
            dict_cur: psycopg2.extras.DictCursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            sql = """select * 
                    from {}.t_sitio_suelos_x
                    where nombre = %s """.format(self.esquema)
            dict_cur.execute(sql, (torre,))
            recs = dict_cur.fetchone()
            return recs
        
        except (Exception, psycopg2.Error) as error :
            print ("Error en base de datos", error)
            return None
        
        finally:
            if(conn):
                dict_cur.close()
                conn.close()

    def listar_cargas_maxima_compresion_cartesiano(self):
        try:
            conn = psycopg2.connect(self.conn_string)
            dict_cur: psycopg2.extras.DictCursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            sql = """
                select distinct on (tt.nombre, tc.nombre) tt.nombre as tipo_torre, tc.nombre as tipo_carga, 'máxima carga a compresión' as caso_carga, 'cartesiano' as sistema, 
                r.load_case, r.total_vert_force as compresion, r.total_long_force as longitudinal, r.total_tran_force as transversal, r.id
                from {}.t_reaccion r
                join {}.t_reaccion_archivo a on a.id= r.reaccion_archivo_id
                join {}.t_reaccion_tipo_torre tt on tt.id = a.reaccion_tipo_torre_id
                join {}.t_reaccion_tipo_carga tc on tc.id = a.reaccion_tipo_carga_id
                where r.total_vert_force < 0
                order by tt.nombre, tc.nombre, abs(r.total_vert_force) desc        
            """.format(*(self.esquema,)*4)
            dict_cur.execute(sql)
            return dict_cur.fetchall()
        
        except (Exception, psycopg2.Error) as error :
            print ("Error en base de datos", error)
            return None
        
        finally:
            if(conn):
                dict_cur.close()
                conn.close()

    def listar_cargas_maxima_compresion_cartesiano_por_cuerpo(self):
        try:
            conn = psycopg2.connect(self.conn_string)
            dict_cur: psycopg2.extras.DictCursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            sql = """
                select *
                from {}.v_cargas_maximas_compresion_cartesiano
            """.format(self.esquema)
            dict_cur.execute(sql)
            return dict_cur.fetchall()
        
        except (Exception, psycopg2.Error) as error :
            print ("Error en base de datos", error)
            return None
        
        finally:
            if(conn):
                dict_cur.close()
                conn.close()                

    def listar_cargas_maxima_compresion_eds_cartesiano(self):
        try:
            conn = psycopg2.connect(self.conn_string)
            dict_cur: psycopg2.extras.DictCursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            sql = """
                select distinct on (tt.nombre, tc.nombre) tt.nombre as tipo_torre, tc.nombre as tipo_carga, 'máxima carga a compresión eds' as caso_carga, 'cartesiano' as sistema, 
                r.load_case, r.total_vert_force as compresion, r.total_long_force as longitudinal, r.total_tran_force as transversal, r.id
                from {}.t_reaccion r
                join {}.t_reaccion_archivo a on a.id= r.reaccion_archivo_id
                join {}.t_reaccion_tipo_torre tt on tt.id = a.reaccion_tipo_torre_id
                join {}.t_reaccion_tipo_carga tc on tc.id = a.reaccion_tipo_carga_id
                where r.total_vert_force < 0
                and load_case ~ 'EDS'
                order by tt.nombre, tc.nombre, abs(r.total_vert_force) desc        
            """.format(*(self.esquema,)*4)
            dict_cur.execute(sql)
            return dict_cur.fetchall()
        
        except (Exception, psycopg2.Error) as error :
            print ("Error en base de datos", error)
            return None
        
        finally:
            if(conn):
                dict_cur.close()
                conn.close()

    def listar_cargas_maxima_compresion_eds_cartesiano_por_cuerpo(self):
        try:
            conn = psycopg2.connect(self.conn_string)
            dict_cur: psycopg2.extras.DictCursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            sql = """
                select *
                from {}.v_cargas_maximas_compresion_eds_cartesiano
            """.format(self.esquema)
            dict_cur.execute(sql)
            return dict_cur.fetchall()
        
        except (Exception, psycopg2.Error) as error :
            print ("Error en base de datos", error)
            return None
        
        finally:
            if(conn):
                dict_cur.close()
                conn.close()                

    def listar_cargas_maxima_tesion_cartesiano(self):
        try:
            conn = psycopg2.connect(self.conn_string)
            dict_cur: psycopg2.extras.DictCursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            sql = """
                select distinct on (tt.nombre, tc.nombre) tt.nombre as tipo_torre, tc.nombre as tipo_carga, 'máxima carga a tensión' as caso_carga, 'cartesiano' as sistema, 
                r.load_case, r.total_vert_force as tension, r.total_long_force as longitudinal, r.total_tran_force as transversal, r.id
                from {}.t_reaccion r
                join {}.t_reaccion_archivo a on a.id= r.reaccion_archivo_id
                join {}.t_reaccion_tipo_torre tt on tt.id = a.reaccion_tipo_torre_id
                join {}.t_reaccion_tipo_carga tc on tc.id = a.reaccion_tipo_carga_id
                where r.total_vert_force > 0
                order by tt.nombre, tc.nombre, abs(r.total_vert_force) desc       
            """.format(*(self.esquema,)*4)
            dict_cur.execute(sql)
            return dict_cur.fetchall()
        
        except (Exception, psycopg2.Error) as error :
            print ("Error en base de datos", error)
            return None
        
        finally:
            if(conn):
                dict_cur.close()
                conn.close()

    def listar_cargas_maxima_tesion_cartesiano_por_cuerpo(self):
        try:
            conn = psycopg2.connect(self.conn_string)
            dict_cur: psycopg2.extras.DictCursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            sql = """
                select *
                from {}.v_cargas_maximas_tension_cartesiano
            """.format(self.esquema)
            dict_cur.execute(sql)
            return dict_cur.fetchall()
        
        except (Exception, psycopg2.Error) as error :
            print ("Error en base de datos", error)
            return None
        
        finally:
            if(conn):
                dict_cur.close()
                conn.close()         

    def listar_cargas_maxima_longitudinal_cartesiano(self):
        try:
            conn = psycopg2.connect(self.conn_string)
            dict_cur: psycopg2.extras.DictCursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            sql = """
                select distinct on (tt.nombre, tc.nombre) tt.nombre as tipo_torre, tc.nombre as tipo_carga, 'máxima carga longitudinal' as caso_carga, 'cartesiano' as sistema, 
                r.load_case, r.total_vert_force as axial, r.total_long_force as longitudinal, r.total_tran_force as transversal, r.id
                from {}.t_reaccion r
                join {}.t_reaccion_archivo a on a.id= r.reaccion_archivo_id
                join {}.t_reaccion_tipo_torre tt on tt.id = a.reaccion_tipo_torre_id
                join {}.t_reaccion_tipo_carga tc on tc.id = a.reaccion_tipo_carga_id
                --order by tt.nombre, tc.nombre, sqrt(r.total_tran_force^2 + r.total_long_force^2) desc, abs(r.total_long_force) desc    
                order by tt.nombre, tc.nombre, abs(r.total_long_force) desc 
            """.format(*(self.esquema,)*4)
            dict_cur.execute(sql)
            return dict_cur.fetchall()
        
        except (Exception, psycopg2.Error) as error :
            print ("Error en base de datos", error)
            return None
        
        finally:
            if(conn):
                dict_cur.close()
                conn.close()

    def listar_cargas_maxima_longitudinal_cartesiano_por_cuerpo(self):
        try:
            conn = psycopg2.connect(self.conn_string)
            dict_cur: psycopg2.extras.DictCursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            sql = """
                select *
                from {}.v_cargas_maximas_longitudinal_cartesiano
            """.format(self.esquema)
            dict_cur.execute(sql)
            return dict_cur.fetchall()
        
        except (Exception, psycopg2.Error) as error :
            print ("Error en base de datos", error)
            return None
        
        finally:
            if(conn):
                dict_cur.close()
                conn.close()          

    def listar_cargas_maxima_transversal_cartesiano(self):
        try:
            conn = psycopg2.connect(self.conn_string)
            dict_cur: psycopg2.extras.DictCursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            sql = """
                select distinct on (tt.nombre, tc.nombre) tt.nombre as tipo_torre, tc.nombre as tipo_carga, 'máxima carga transversal' as caso_carga, 'cartesiano' as sistema, 
                r.load_case, r.total_vert_force as axial, r.total_long_force as longitudinal, r.total_tran_force as transversal, r.id
                from {}.t_reaccion r
                join {}.t_reaccion_archivo a on a.id= r.reaccion_archivo_id
                join {}.t_reaccion_tipo_torre tt on tt.id = a.reaccion_tipo_torre_id
                join {}.t_reaccion_tipo_carga tc on tc.id = a.reaccion_tipo_carga_id
                --order by tt.nombre, tc.nombre, sqrt(r.total_tran_force^2 + r.total_long_force^2) desc, abs(r.total_tran_force) desc  
                order by tt.nombre, tc.nombre, abs(r.total_tran_force) desc  
            """.format(*(self.esquema,)*4)
            dict_cur.execute(sql)
            return dict_cur.fetchall()
        
        except (Exception, psycopg2.Error) as error :
            print ("Error en base de datos", error)
            return None
        
        finally:
            if(conn):
                dict_cur.close()
                conn.close()

    def listar_cargas_maxima_transversal_cartesiano_por_cuerpo(self):
        try:
            conn = psycopg2.connect(self.conn_string)
            dict_cur: psycopg2.extras.DictCursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            sql = """
                select *
                from {}.v_cargas_maximas_transversal_cartesiano
            """.format(self.esquema)
            dict_cur.execute(sql)
            return dict_cur.fetchall()
        
        except (Exception, psycopg2.Error) as error :
            print ("Error en base de datos", error)
            return None
        
        finally:
            if(conn):
                dict_cur.close()
                conn.close()           

    def listar_cargas_maxima_compresion_montante(self):
        try:
            conn = psycopg2.connect(self.conn_string)
            dict_cur: psycopg2.extras.DictCursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            sql = """
                select distinct on (tt.nombre, tc.nombre) tt.nombre as tipo_torre, tc.nombre as tipo_carga, 'máxima carga a compresión' as caso_carga, 'montante' as sistema, 
                r.load_case, r.force_in_leg_dir as compresion, r.residual_shear_perp_to_leg as lateral, r.residual_shear_hor_to_leg_long as horizontal_long,
                r.residual_shear_hor_to_leg_tran as horizontal_trans,
                r.residual_shear_hor_to_leg_long as horz_long, 
                r.residual_shear_hor_to_leg_tran as horz_tran, 
                r.id
                from {}.t_reaccion r
                join {}.t_reaccion_archivo a on a.id= r.reaccion_archivo_id
                join {}.t_reaccion_tipo_torre tt on tt.id = a.reaccion_tipo_torre_id
                join {}.t_reaccion_tipo_carga tc on tc.id = a.reaccion_tipo_carga_id
                where r.force_in_leg_dir > 0
                order by tt.nombre, tc.nombre, abs(r.force_in_leg_dir) desc
            """.format(*(self.esquema,)*4)
            dict_cur.execute(sql)
            return dict_cur.fetchall()
        
        except (Exception, psycopg2.Error) as error :
            print ("Error en base de datos", error)
            return None
        
        finally:
            if(conn):
                dict_cur.close()
                conn.close()

    def listar_cargas_maxima_compresion_montante_por_cuerpo(self):
        try:
            conn = psycopg2.connect(self.conn_string)
            dict_cur: psycopg2.extras.DictCursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            sql = """
                select *
                from {}.v_cargas_maximas_compresion_montante
            """.format(self.esquema)
            dict_cur.execute(sql)
            return dict_cur.fetchall()
        
        except (Exception, psycopg2.Error) as error :
            print ("Error en base de datos", error)
            return None
        
        finally:
            if(conn):
                dict_cur.close()
                conn.close()          

    def listar_cargas_maxima_tension_montante(self):
        try:
            conn = psycopg2.connect(self.conn_string)
            dict_cur: psycopg2.extras.DictCursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            sql = """
                select distinct on (tt.nombre, tc.nombre) tt.nombre as tipo_torre, tc.nombre as tipo_carga, 'máxima carga a tensión' as caso_carga, 'montante' as sistema, 
                r.load_case, r.force_in_leg_dir as tension, r.residual_shear_perp_to_leg as lateral, 
                r.residual_shear_hor_to_leg_long as horz_long, 
                r.residual_shear_hor_to_leg_tran as horz_tran, 
                r.id
                from {}.t_reaccion r
                join {}.t_reaccion_archivo a on a.id= r.reaccion_archivo_id
                join {}.t_reaccion_tipo_torre tt on tt.id = a.reaccion_tipo_torre_id
                join {}.t_reaccion_tipo_carga tc on tc.id = a.reaccion_tipo_carga_id
                where r.total_vert_force > 0
                order by tt.nombre, tc.nombre, abs(r.total_vert_force) desc
            """.format(*(self.esquema,)*4)
            dict_cur.execute(sql)
            return dict_cur.fetchall()
        
        except (Exception, psycopg2.Error) as error :
            print ("Error en base de datos", error)
            return None
        
        finally:
            if(conn):
                dict_cur.close()
                conn.close()

    def listar_cargas_maxima_tension_montante_por_cuerpo(self):
        try:
            conn = psycopg2.connect(self.conn_string)
            dict_cur: psycopg2.extras.DictCursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            sql = """
                select *
                from {}.v_cargas_maximas_tension_montante
            """.format(self.esquema)
            dict_cur.execute(sql)
            return dict_cur.fetchall()
        
        except (Exception, psycopg2.Error) as error :
            print ("Error en base de datos", error)
            return None
        
        finally:
            if(conn):
                dict_cur.close()
                conn.close()           

    def listar_cargas_maxima_lateral_montante(self):
        try:
            conn = psycopg2.connect(self.conn_string)
            dict_cur: psycopg2.extras.DictCursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            sql = """
                select distinct on (tt.nombre, tc.nombre) tt.nombre as tipo_torre, tc.nombre as tipo_carga, 'máxima carga lateral' as caso_carga, 'montante' as sistema, 
                r.load_case, r.force_in_leg_dir as axial, r.residual_shear_perp_to_leg as lateral, 
                r.residual_shear_hor_to_leg_long as horz_long, 
                r.residual_shear_hor_to_leg_tran as horz_tran,                 
                r.id
                from {}.t_reaccion r
                join {}.t_reaccion_archivo a on a.id= r.reaccion_archivo_id
                join {}.t_reaccion_tipo_torre tt on tt.id = a.reaccion_tipo_torre_id
                join {}.t_reaccion_tipo_carga tc on tc.id = a.reaccion_tipo_carga_id
                order by tt.nombre, tc.nombre, abs(r.residual_shear_perp_to_leg) desc
            """.format(*(self.esquema,)*4)
            dict_cur.execute(sql)
            return dict_cur.fetchall()
        
        except (Exception, psycopg2.Error) as error :
            print ("Error en base de datos", error)
            return None
        
        finally:
            if(conn):
                dict_cur.close()
                conn.close()  

    def listar_cargas_maxima_horz_long_montante(self):
        try:
            conn = psycopg2.connect(self.conn_string)
            dict_cur: psycopg2.extras.DictCursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            sql = """
                select distinct on (tt.nombre, tc.nombre) tt.nombre as tipo_torre, tc.nombre as tipo_carga, 'máxima carga horz long' as caso_carga, 'montante' as sistema, 
                r.load_case, r.force_in_leg_dir as axial, r.residual_shear_perp_to_leg as lateral, 
                r.residual_shear_hor_to_leg_long as horz_long, 
                r.residual_shear_hor_to_leg_tran as horz_tran, 
                r.id
                from {}.t_reaccion r
                join {}.t_reaccion_archivo a on a.id= r.reaccion_archivo_id
                join {}.t_reaccion_tipo_torre tt on tt.id = a.reaccion_tipo_torre_id
                join {}.t_reaccion_tipo_carga tc on tc.id = a.reaccion_tipo_carga_id
                order by tt.nombre, tc.nombre, abs(r.residual_shear_hor_to_leg_long) desc
            """.format(*(self.esquema,)*4)
            dict_cur.execute(sql)
            return dict_cur.fetchall()
        
        except (Exception, psycopg2.Error) as error :
            print ("Error en base de datos", error)
            return None
        
        finally:
            if(conn):
                dict_cur.close()
                conn.close() 
    
    def listar_cargas_maxima_horz_tran_montante(self):
        try:
            conn = psycopg2.connect(self.conn_string)
            dict_cur: psycopg2.extras.DictCursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            sql = """
                select distinct on (tt.nombre, tc.nombre) tt.nombre as tipo_torre, tc.nombre as tipo_carga, 'máxima carga horz tran' as caso_carga, 'montante' as sistema, 
                r.load_case, r.force_in_leg_dir as axial, r.residual_shear_perp_to_leg as lateral, 
                r.residual_shear_hor_to_leg_long as horz_long, 
                r.residual_shear_hor_to_leg_tran as horz_tran, 
                r.id
                from {}.t_reaccion r
                join {}.t_reaccion_archivo a on a.id= r.reaccion_archivo_id
                join {}.t_reaccion_tipo_torre tt on tt.id = a.reaccion_tipo_torre_id
                join {}.t_reaccion_tipo_carga tc on tc.id = a.reaccion_tipo_carga_id
                order by tt.nombre, tc.nombre, abs(r.residual_shear_hor_to_leg_tran) desc
            """.format(*(self.esquema,)*4)
            dict_cur.execute(sql)
            return dict_cur.fetchall()
        
        except (Exception, psycopg2.Error) as error :
            print ("Error en base de datos", error)
            return None
        
        finally:
            if(conn):
                dict_cur.close()
                conn.close() 

    def listar_cargas_maxima_lateral_montante_por_cuerpo(self):
        try:
            conn = psycopg2.connect(self.conn_string)
            dict_cur: psycopg2.extras.DictCursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            sql = """
                select *
                from {}.v_cargas_maximas_lateral_montante
            """.format(self.esquema)
            dict_cur.execute(sql)
            return dict_cur.fetchall()
        
        except (Exception, psycopg2.Error) as error :
            print ("Error en base de datos", error)
            return None
        
        finally:
            if(conn):
                dict_cur.close()
                conn.close()         


    def guardar_corrida_zapata(self, corrida, parametros):
        try:
            conn = psycopg2.connect(self.conn_string)
            cur = conn.cursor()
            sql = "insert into {}.t_zapata_corrida(nombre, parametros) values(%s, %s) returning id".format(self.esquema)
            json_parametros = json.dumps(parametros)
            cur.execute(sql, (corrida["nombre"], json_parametros ))
            return cur.fetchone()[0]
        
        except (Exception, psycopg2.Error) as error :
            print ("Error en base de datos", error)
            return None
        
        finally:
            if(conn):
                cur.close()
                conn.commit()
                conn.close()

    def guardar_corrida_zapata_torre(self, corrida_id: int, torre: Torre, perfil: Perfil, info_cargas: Dict, error_en_perfil: bool, mensaje_error: str, resultados):
        try:
            conn = psycopg2.connect(self.conn_string)
            cur = conn.cursor()
            sql = "insert into {}.t_zapata_corrida_torre(zapata_corrida_id, torre, perfil, cargas, error_en_perfil, mensaje_error, resultados, torre_info) values(%s,%s,%s,%s,%s,%s,%s, %s) returning id".format(self.esquema)
            json_torre_info = json.dumps(vars(torre))
            if error_en_perfil:
                cur.execute(sql, (corrida_id, torre.nombre, None, None, error_en_perfil, mensaje_error, None, json_torre_info))
            else:
                #json_perfil = json.dumps([vars(estrato) for estrato in perfil])
                json_perfil = json.dumps({ "nivel_freatico_exploracion": perfil.nivel_freatico_exploracion, "estratos": [vars(estrato) for estrato in perfil]})
                json_info_cargas = json.dumps(info_cargas)
                json_resultados = json.dumps(resultados)
                cur.execute(sql, (corrida_id, torre.nombre, json_perfil , json_info_cargas, error_en_perfil, None, json_resultados, json_torre_info))
            return cur.fetchone()[0]
        
        except (Exception, psycopg2.Error) as error :
            print ("Error en base de datos", error)
            return None
        
        finally:
            if(conn):
                cur.close()
                conn.commit()
                conn.close()


    def guardar_corrida_parrilla(self, corrida, parametros):
        try:
            conn = psycopg2.connect(self.conn_string)
            cur = conn.cursor()
            sql = "insert into {}.t_parrilla_corrida(nombre, parametros) values(%s, %s) returning id".format(self.esquema)
            json_parametros = json.dumps(parametros)
            cur.execute(sql, (corrida["nombre"], json_parametros ))
            return cur.fetchone()[0]
        
        except (Exception, psycopg2.Error) as error :
            print ("Error en base de datos", error)
            return None
        
        finally:
            if(conn):
                cur.close()
                conn.commit()
                conn.close()

    def guardar_corrida_parrilla_torre(self, corrida_id: int, torre: Torre, perfil: Perfil, info_cargas: Dict, error_en_perfil: bool, mensaje_error: str, resultados):
        try:
            conn = psycopg2.connect(self.conn_string)
            cur = conn.cursor()
            sql = "insert into {}.t_parrilla_corrida_torre(parrilla_corrida_id, torre, perfil, cargas, error_en_perfil, mensaje_error, resultados, torre_info) values(%s,%s,%s,%s,%s,%s,%s, %s) returning id".format(self.esquema)
            json_torre_info = json.dumps(vars(torre))
            if error_en_perfil:
                cur.execute(sql, (corrida_id, torre.nombre, None, None, error_en_perfil, mensaje_error, None, json_torre_info))
            else:
                #json_perfil = json.dumps([vars(estrato) for estrato in perfil])
                json_perfil = json.dumps({ "nivel_freatico_exploracion": perfil.nivel_freatico_exploracion, "estratos": [vars(estrato) for estrato in perfil]})
                json_info_cargas = json.dumps(info_cargas)
                json_resultados = json.dumps(resultados)
                cur.execute(sql, (corrida_id, torre.nombre, json_perfil , json_info_cargas, error_en_perfil, None, json_resultados, json_torre_info))
            return cur.fetchone()[0]
        
        except (Exception, psycopg2.Error) as error :
            print ("Error en base de datos", error)
            return None
        
        finally:
            if(conn):
                cur.close()
                conn.commit()
                conn.close()


    def guardar_corrida_pilastra(self, corrida, parametros):
        try:
            conn = psycopg2.connect(self.conn_string)
            cur = conn.cursor()
            sql = "insert into {}.t_pilastra_corrida(nombre, parametros) values(%s, %s) returning id".format(self.esquema)
            json_parametros = json.dumps(parametros)
            cur.execute(sql, (corrida["nombre"], json_parametros ))
            return cur.fetchone()[0]
        
        except (Exception, psycopg2.Error) as error :
            print ("Error en base de datos", error)
            return None
        
        finally:
            if(conn):
                cur.close()
                conn.commit()
                conn.close()

    def guardar_corrida_pilastra_torre(self, corrida_id: int, torre: Torre, perfil: Perfil, info_cargas: Dict, error_en_perfil: bool, mensaje_error: str, resultados):
        try:
            conn = psycopg2.connect(self.conn_string)
            cur = conn.cursor()
            sql = "insert into {}.t_pilastra_corrida_torre(pilastra_corrida_id, torre, perfil, cargas, error_en_perfil, mensaje_error, resultados, torre_info) values(%s,%s,%s,%s,%s,%s,%s, %s) returning id".format(self.esquema)
            json_torre_info = json.dumps(vars(torre))
            if error_en_perfil:
                cur.execute(sql, (corrida_id, torre.nombre, None, None, error_en_perfil, mensaje_error, None, json_torre_info))
            else:
                #json_perfil = json.dumps([estrato.__dict__ for estrato in perfil])
                json_perfil = json.dumps({ "nivel_freatico_exploracion": perfil.nivel_freatico_exploracion, "estratos": [vars(estrato) for estrato in perfil]})
                json_info_cargas = json.dumps(info_cargas)
                json_resultados = json.dumps(resultados)
                cur.execute(sql, (corrida_id, torre.nombre, json_perfil , json_info_cargas, error_en_perfil, None, json_resultados, json_torre_info))
            return cur.fetchone()[0]
        
        except (Exception, psycopg2.Error) as error :
            print ("Error en base de datos", error)
            return None
        
        finally:
            if(conn):
                cur.close()
                conn.commit()
                conn.close()


    def guardar_corrida_micropilotes(self, corrida):
        try:
            conn = psycopg2.connect(self.conn_string)
            cur = conn.cursor()
            sql = "insert into {}.t_micropilotes_corrida(nombre, parametros) values(%s, %s) returning id".format(self.esquema)
            cur.execute(sql, (corrida["nombre"], corrida["parametros"]))
            return cur.fetchone()[0]
        
        except (Exception, psycopg2.Error) as error :
            print ("Error en base de datos", error)
            return None
        
        finally:
            if(conn):
                cur.close()
                conn.commit()
                conn.close()

    def guardar_corrida_micropilotes_torre(self, corrida_id: int, torre: Torre, perfil: Perfil, info_cargas: Dict, error_en_perfil: bool, mensaje_error: str, resultados, observaciones: str):
        try:
            conn = psycopg2.connect(self.conn_string)
            cur = conn.cursor()
            sql = "insert into {}.t_micropilotes_corrida_torre(micropilotes_corrida_id, torre, perfil, cargas, error_en_perfil, mensaje_error, resultados, observaciones) values(%s,%s,%s,%s,%s,%s,%s,%s) returning id".format(self.esquema)
            if error_en_perfil:
                cur.execute(sql, (corrida_id, torre.nombre, None, None, error_en_perfil, mensaje_error, None, None))
            else:
                #json_perfil = json.dumps([vars(estrato) for estrato in perfil])
                json_perfil = json.dumps({ "nivel_freatico_exploracion": perfil.nivel_freatico_exploracion, "estratos": [vars(estrato) for estrato in perfil]})
                json_info_cargas = json.dumps(info_cargas)
                json_resultados = json.dumps(resultados)
                cur.execute(sql, (corrida_id, torre.nombre, json_perfil , json_info_cargas, error_en_perfil, None, json_resultados, observaciones))
            return cur.fetchone()[0]
        
        except (Exception, psycopg2.Error) as error :
            print ("Error en base de datos", error)
            raise error
        
        finally:
            if(conn):
                cur.close()
                conn.commit()
                conn.close()


    def guardar_resultado_micropilotes(self, corrida_id:int, torre, resultado):
        try:
            print(len(resultado), " resultados")
            conn = psycopg2.connect(self.conn_string)
            cur = conn.cursor()
            
            sql = """insert into {}.t_micropilotes_result
                    (micropilotes_corrida_id,torre,hg,d_f,f_carga_mp,tp,proc_iny,barra_diam,barra_area,barra_fy,d_p,n_m,s_m,b,h,d_d,e_d,l_b,
                    lateral_q_long,lateral_q_long_fs,lateral_q_trans,lateral_q_trans_fs,lateral_q_pasa,lateral_c_remanente,
                    micropilote_p_g,micropilote_fs_pg,micropilote_p_t,micropilote_fs_pt,micropilote_p_c,micropilote_fs_pc,micropilote_p_br_gr,micropilote_fs_p_br_gr,micropilote_p_mp,micropilote_pasa,
                    compresion_dado_q_ult,compresion_dado_fs,compresion_dado_pasa,
                    compresion_micropilotes_p_perms,compresion_micropilotes_fs,compresion_micropilotes_pasa,
                    asentamiento_s,asentamiento_holgura,asentamiento_pasa,
                    tension_material,tension_q_ug,tension_fs,tension_pasa,
                    pasa,observaciones, dist_bor)
                    values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""".format(self.esquema)

            for caso in resultado:
                HG, D_f, f_carga_mp, TP, proc_iny, barra, D_p, N_m, S_m = caso
                r = resultado[caso]

                lateral_q_long,lateral_q_trans,lateral_q_long_fs,lateral_q_trans_fs,lateral_c_remanente,lateral_q_pasa,_,_ = r["lateral"]
                micropilote_p_g,micropilote_fs_pg,micropilote_p_t,micropilote_fs_pt,micropilote_p_c,micropilote_fs_pc,micropilote_p_br_gr,micropilote_fs_p_br_gr,micropilote_p_mp,micropilote_pasa,_ = r["micropilote"]
                compresion_dado_q_ult,compresion_dado_fs,compresion_dado_pasa, _ = r["compresion_dado"]
                compresion_micropilotes_p_perms,compresion_micropilotes_fs,compresion_micropilotes_pasa, _ = r["compresion_micropilotes"]
                asentamiento_s,asentamiento_holgura,asentamiento_pasa, _ = r["asentamientos"]
                tension_q_ug, tension_fs,tension_pasa, _ = r["tension"]
                b, h, d_d, e_d, l_b, dist_bor = r["adicionales"]
                pasa = lateral_q_pasa and micropilote_pasa and compresion_dado_pasa and compresion_micropilotes_pasa and asentamiento_pasa and tension_pasa

                observaciones = None

                cur.execute(sql, (corrida_id, torre["nombre"], HG, D_f, f_carga_mp, TP, proc_iny, barra.D, barra.area, barra.f_y, D_p, N_m, S_m, b, h, d_d, e_d, l_b,
                lateral_q_long,lateral_q_long_fs,lateral_q_trans,lateral_q_trans_fs,lateral_q_pasa,lateral_c_remanente,
                micropilote_p_g,micropilote_fs_pg,micropilote_p_t,micropilote_fs_pt,micropilote_p_c,micropilote_fs_pc,micropilote_p_br_gr,micropilote_fs_p_br_gr,micropilote_p_mp,micropilote_pasa,
                compresion_dado_q_ult,compresion_dado_fs,compresion_dado_pasa,
                compresion_micropilotes_p_perms,compresion_micropilotes_fs,compresion_micropilotes_pasa,
                asentamiento_s,asentamiento_holgura,asentamiento_pasa,
                None,tension_q_ug,tension_fs,tension_pasa,
                pasa, observaciones, dist_bor))
        
        except (Exception, psycopg2.Error) as error :
            print ("Error en base de datos", error)
            return None
        
        finally:
            if(conn):
                cur.close()
                conn.commit()
                conn.close()

    def guardar_resultado_micropilotes_error(self, corrida_id:int, torre, observaciones):
        try:
            conn = psycopg2.connect(self.conn_string)
            cur = conn.cursor()
            
            sql = """insert into {}.t_micropilotes_result
                    (micropilotes_corrida_id, torre, observaciones)
                    values(%s,%s,%s)""".format(self.esquema)

            cur.execute(sql, (corrida_id, torre["nombre"], observaciones))
        
        except (Exception, psycopg2.Error) as error :
            print ("Error en base de datos", error)
            return None
        
        finally:
            if(conn):
                cur.close()
                conn.commit()
                conn.close()


    def guardar_corrida_pilotes(self, corrida, parametros):
        try:
            conn = psycopg2.connect(self.conn_string)
            cur = conn.cursor()
            sql = "insert into {}.t_pilotes_corrida(nombre, parametros) values(%s, %s) returning id".format(self.esquema)
            json_parametros = json.dumps(parametros)
            cur.execute(sql, (corrida["nombre"], json_parametros ))
            return cur.fetchone()[0]
        
        except (Exception, psycopg2.Error) as error :
            print ("Error en base de datos", error)
            return None
        
        finally:
            if(conn):
                cur.close()
                conn.commit()
                conn.close()

    def guardar_corrida_pilotes_torre(self, corrida_id: int, torre: Torre, perfil: Perfil, info_cargas: Dict, error_en_perfil: bool, mensaje_error: str, resultados):
        try:
            conn = psycopg2.connect(self.conn_string)
            cur = conn.cursor()
            sql = "insert into {}.t_pilotes_corrida_torre(pilotes_corrida_id, torre, perfil, cargas, error_en_perfil, mensaje_error, resultados, torre_info) values(%s,%s,%s,%s,%s,%s,%s, %s) returning id".format(self.esquema)
            json_torre_info = json.dumps(vars(torre))
            if error_en_perfil:
                cur.execute(sql, (corrida_id, torre.nombre, None, None, error_en_perfil, mensaje_error, None, json_torre_info))
            else:
                #json_perfil = json.dumps([estrato.__dict__ for estrato in perfil])
                json_perfil = json.dumps({ "nivel_freatico_exploracion": perfil.nivel_freatico_exploracion, "estratos": [vars(estrato) for estrato in perfil]})
                json_info_cargas = json.dumps(info_cargas)
                json_resultados = json.dumps(resultados)
                cur.execute(sql, (corrida_id, torre.nombre, json_perfil , json_info_cargas, error_en_perfil, None, json_resultados, json_torre_info))
            return cur.fetchone()[0]
        
        except (Exception, psycopg2.Error) as error :
            print ("Error en base de datos", error)
            return None
        
        finally:
            if(conn):
                cur.close()
                conn.commit()
                conn.close()


    def guardar_corrida_pila(self, corrida, parametros):
        try:
            conn = psycopg2.connect(self.conn_string)
            cur = conn.cursor()
            sql = "insert into {}.t_pila_corrida(nombre, parametros) values(%s, %s) returning id".format(self.esquema)
            json_parametros = json.dumps(parametros)
            cur.execute(sql, (corrida["nombre"], json_parametros ))
            return cur.fetchone()[0]
        
        except (Exception, psycopg2.Error) as error :
            print ("Error en base de datos", error)
            return None
        
        finally:
            if(conn):
                cur.close()
                conn.commit()
                conn.close()
    
    def guardar_corrida_pila_torre(self, corrida_id: int, torre: Torre, perfil: Perfil, info_cargas: Dict, error_en_perfil: bool, mensaje_error: str, resultados):
        try:
            conn = psycopg2.connect(self.conn_string)
            cur = conn.cursor()
            sql = "insert into {}.t_pila_corrida_torre(pila_corrida_id, torre, perfil, cargas, error_en_perfil, mensaje_error, resultados, torre_info) values(%s,%s,%s,%s,%s,%s,%s, %s) returning id".format(self.esquema)
            json_torre_info = json.dumps(vars(torre))
            if error_en_perfil:
                cur.execute(sql, (corrida_id, torre.nombre, None, None, error_en_perfil, mensaje_error, None, json_torre_info))
            else:
                #json_perfil = json.dumps([estrato.__dict__ for estrato in perfil])
                json_perfil = json.dumps({ "nivel_freatico_exploracion": perfil.nivel_freatico_exploracion, "estratos": [vars(estrato) for estrato in perfil]})
                json_info_cargas = json.dumps(info_cargas)
                json_resultados = json.dumps(resultados)
                cur.execute(sql, (corrida_id, torre.nombre, json_perfil , json_info_cargas, error_en_perfil, None, json_resultados, json_torre_info))
            return cur.fetchone()[0]
        
        except (Exception, psycopg2.Error) as error :
            print ("Error en base de datos", error)
            return None
        
        finally:
            if(conn):
                cur.close()
                conn.commit()
                conn.close()


    def listar_agrupacion_soluciones_corrida_zapata_por_pedestal_b_d(self, corrida_id: int, tipo: str, hg: float):
        """
        Consulta las soluciones de una corrida de zapatas agrupada por b,d
        y filtrada por corrida, pedestal y tipo de torre
        
        Arguments:
            ToDo
        
        Returns:
            List[DBFila] -- Lista de diccionarios que representan las soluciones
        """        
        try:
            conn = psycopg2.connect(self.conn_string)
            dict_cur: psycopg2.extras.DictCursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            sql = (
                    "with datos as "
                    "( "
                    "   select distinct on (ct.torre, (r->>'HG')::numeric) "
                    "		   ct.torre, "
                    "	  	   vt.tipo, "
                    "	       (r->>'HG')::numeric as hg, "
                    "	       (r->>'B')::numeric as b, "
                    "	       (r->>'D')::numeric as d, "
                    "	       (r->>'volumen_ponderado')::numeric as volumen_ponderado "
                    "	from cll_dlt_gtc.t_zapata_corrida_torre ct "
                    "	cross join jsonb_array_elements(ct.resultados ) r "
                    "	join cll_dlt_gtc.v_torre vt on vt.nombre= ct.torre "
                    "	where ct.zapata_corrida_id = %s "
                    "	and (r->>'HG')::numeric = %s "
                    "	and vt.tipo = %s "
                    "	order by ct.torre, (r->>'HG')::numeric, (R->>'volumen_ponderado')::numeric "
                    ") "
                    "select d.tipo, "
                    "       d.hg,  "
                    "	   round(d.b,1) as b, "
                    "	   round(d.d,1) as d,  "
                    "	   count(*) as cantidad  "
                    "from datos d "
                    "group by d.tipo, d.hg, d.b, d.d "
                    "order by d.tipo, d.hg, d.b, d.d "
            )
            dict_cur.execute(sql, (corrida_id, hg, tipo))
            return dict_cur.fetchall()

        except (Exception, psycopg2.Error) as error :
            print ("Error en base de datos", error)
            raise error

        finally:
            if(conn):
                dict_cur.close()
                conn.close()

    def listar_agrupacion_soluciones_corrida_zapata_por_b_d(self, corrida_id: int, tipo: str, resistencia_concreto: float, relacion_agua_cemento: float):
        """
        Consulta las soluciones de una corrida de zapatas
        filtrada por tipo de torre, resistencia del concreto y relación agua cemento
        y las agrupa por b y d para la búsqueda de la agrupacines óptimas para diseño
        
        Arguments:
            ToDo
        
        Returns:
            List[DBFila] -- Lista de agrupaciones: [{tipo, b, d, cantidad, [torres]}]
        """        
        try:
            conn = psycopg2.connect(self.conn_string)
            dict_cur: psycopg2.extras.DictCursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            sql = (
                    "with datos as "
                    "( "
                    "   select ct.torre, "
                    "	  	   vt.tipo, "
                    "	       (ct.resultados->0->>'B')::numeric as b, "
                    "	       (ct.resultados->0->>'D')::numeric as d, "
                    "	       (ct.resultados->0->>'volumen_ponderado')::numeric as volumen_ponderado "
                    "	from cll_dlt_gtc.t_zapata_corrida_torre ct "
                    "	join cll_dlt_gtc.v_torre vt on vt.nombre= ct.torre "
                    "	where ct.zapata_corrida_id = %s	"
                    "	and vt.tipo ~ %s "
                    "   and vt.resistencia_min_conc = %s"
                    "   and coalesce(vt.relacion_a_mc_max, '') = coalesce(%s, '')"
                    "	and (ct.resultados->0->>'cumple')::bool"
                    "	order by ct.torre "
                    ") "
                    "select d.tipo, "
                    "	   round(d.b,1) as b, "
                    "	   round(d.d,1) as d, "
                    "	   count(*) as cantidad, "
                    "	   array_agg(d.torre) as torres "
                    "from datos d "
                    "group by d.tipo, d.b, d.d "
                    "order by d.tipo, d.b, d.d"
            )
            dict_cur.execute(sql, (corrida_id, tipo, resistencia_concreto, relacion_agua_cemento))
            return dict_cur.fetchall()

        except (Exception, psycopg2.Error) as error :
            print ("Error en base de datos", error)
            raise error

        finally:
            if(conn):
                dict_cur.close()
                conn.close()

    def listar_torres_corrida_zapata(self, corrida_id: int, tipo: str, resistencia_concreto: float, relacion_agua_cemento: float):
        """
        Consulta las soluciones de una corrida de zapatas
        filtrada por tipo de torre, resistencia del concreto y relación agua cemento
        
        Arguments:
            ToDo
        
        Returns:
            List[DBFila] -- Lista de diccionarios con infomación de tabla de torres más su punto de diseño b, d
        """        
        try:
            conn = psycopg2.connect(self.conn_string)
            dict_cur: psycopg2.extras.DictCursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            sql = (
                    "select vt.*, "
                    "       round((ct.resultados->0->>'B')::numeric,1) as b, "
                    "       round((ct.resultados->0->>'D')::numeric,1) as d "
                    "from cll_dlt_gtc.t_zapata_corrida_torre ct "
                    "join cll_dlt_gtc.v_torre vt on vt.nombre= ct.torre "
                    "where ct.zapata_corrida_id = %s	"
                    "and vt.tipo ~ %s "
                    "and vt.resistencia_concreto = %s "
                    "and coalesce(vt.relacion_agua_cemento, 0) = coalesce(%s, 0) "
                    "and (ct.resultados->0->>'cumple')::bool "
                    "order by ct.torre "
            )
            dict_cur.execute(sql, (corrida_id, tipo, resistencia_concreto, relacion_agua_cemento))
            return dict_cur.fetchall()

        except (Exception, psycopg2.Error) as error :
            print ("Error en base de datos", error)
            raise error

        finally:
            if(conn):
                dict_cur.close()
                conn.close()

    def listar_grupos_zapatas(self):
        """
        Consulta las soluciones de una corrida de zapatas agrupada por b,d
        y filtrada por corrida, pedestal y tipo de torre
        
        Arguments:
            ToDo
        
        Returns:
            List[DBFila] -- Lista de diccionarios que representan las soluciones
        """        
        try:
            conn = psycopg2.connect(self.conn_string)
            dict_cur: psycopg2.extras.DictCursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            sql = (
                "select sz.tipo, tt.sumergido, case when tt.sumergido then '28MPa' else '21MPa' end as concreto, sz.b, sz.d, array_agg(tt.nombre) as torres "
                "from {}.seleccion_zapatas sz "
                "join {}.v_torre tt on tt.nombre=sz.torre "
                "where b is not null "
                "group by 1,2,3,4,5 "
                "order by 1,2,3,4,5 "                
            ).format(*(self.esquema,)*2)
            dict_cur.execute(sql)
            return dict_cur.fetchall()

        except (Exception, psycopg2.Error) as error :
            print ("Error en base de datos", error)
            raise error

        finally:
            if(conn):
                dict_cur.close()
                conn.close()

    def guardar_zapata_corrida_grupo(self, solucion: Dict):
        try:
            conn = psycopg2.connect(self.conn_string)
            cur = conn.cursor()
            sql = "insert into {}.t_zapata_corrida_grupo(zapata_corrida_id, tipo, concreto, orden, b, d, cantidad, porc_sobrecosto, vol_optimos, vol_grupo, qs, relleno, geometrias, porc_sobrecosto_max, torres) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) returning id".format(self.esquema)
            json_qs = json.dumps(solucion["qs"])
            json_relleno = json.dumps(solucion["relleno"])
            json_geometrias = json.dumps(solucion["geometrias"])
            nombres_torres = [torre["nombre"] for torre in solucion["torres_cubiertas"]]
            cur.execute(sql, (
                solucion["zapata_corrida_id"],
                solucion["tipo"],
                solucion["concreto"],
                solucion["orden"],
                solucion["b"],
                solucion["d"],
                solucion["cantidad"],
                solucion["porc_sobrecosto"],
                solucion["vol_optimos"],
                solucion["vol_grupo"],
                json_qs,
                json_relleno,
                json_geometrias,
                solucion["porc_sobrecosto_max"],
                nombres_torres ))
        
        except (Exception, psycopg2.Error) as error :
            print ("Error en base de datos", error)
            return None
        
        finally:
            if(conn):
                cur.close()
                conn.commit()
                conn.close()

    def listar_geometrias_zapata_por_tipo_torre(self, tipo: str):
        """
        ?
        
        Arguments:
            ToDo
        
        Returns:
            List[DBFila] -- Lista de diccionarios que representan las geometrías
        """        
        try:
            conn = psycopg2.connect(self.conn_string)
            dict_cur: psycopg2.extras.DictCursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            sql = (
                    "with geomes(tipo, tp, h, theta) as "
                    "( "
                    "	values "
                    "	('A100',0.6043,0.4,5.906892478), "
                    "	('AA100',0.6343,0.4,5.906892478), "
                    "	('B100',0.7543,0.4,6.807293875), "
                    "	('C100',0.8143,0.40715,7.846555465), "
                    "	('D100',0.8143,0.40715,9.914023378), "
                    "	('DT100',0.8143,0.40715,9.914023378), "
                    "	('(D100|DT100)',0.8143,0.40715,9.914023378), "
                    "	('TR100',0.8143,0.40715,9.914023378) "
                    ") "
                    "select * "
                    "from geomes "
                    "where tipo = %s "
            )
            dict_cur.execute(sql, (tipo, ))
            return dict_cur.fetchone()

        except (Exception, psycopg2.Error) as error :
            print ("Error en base de datos", error)
            raise error

        finally:
            if(conn):
                dict_cur.close()
                conn.close()
                
    def listar_conjuntos_zapatas_a_agrupar(self, corrida_id):
        """
        Consulta los conjuntos que se forman de una corrida
        de zapatas, basado en el tipo y el concreto para
        encontrar sus grupos de diseño
        
        Arguments:
            TODO
        
        Returns:
            List[DBFila] -- Lista de diccionarios que representan los conjuntos
        """        
        try:
            conn = psycopg2.connect(self.conn_string)
            dict_cur: psycopg2.extras.DictCursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            sql = (
                "select torre_info->>'tipo' as tipo, d.resistencia_min_conc, d.relacion_a_mc_max, count(*) as cant "
                "from {}.t_zapata_corrida_torre ct "
                "join {}.v_torre d on ln_dlt_gtc.torre_norm(d.nombre)=ln_dlt_gtc.torre_norm(ct.torre) "
                "where zapata_corrida_id = %s "
                "and (resultados->0->>'cumple')::bool "
                "group by 1,2,3 "
                "order by 1,2,3 "             
            ).format(*(self.esquema,)*2)
            dict_cur.execute(sql, (corrida_id,))
            return dict_cur.fetchall()

        except (Exception, psycopg2.Error) as error :
            print ("Error en base de datos", error)
            raise error

        finally:
            if(conn):
                dict_cur.close()
                conn.close()

    def listar_resultados_en_conjunto_zapatas(self, corrida_id, tipo, resistencia_min_conc, relacion_a_mc_max):
        """
        Consulta los resultados que cumplen de un corrida
        de zapatas y que están en un conjunto tipo torre, concreto
        para encontrar sus grupos de diseño
        
        Arguments:
            TODO
        
        Returns:
            List[DBFila] -- Lista de diccionarios que representan los resultados  [{"torre":., "b":., "d":., "volumen_ponderado":., "sobrecosto":.},]
        """        
        try:
            conn = psycopg2.connect(self.conn_string)
            dict_cur: psycopg2.extras.DictCursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            sql = (
                "select ct.torre, (r->>'B')::numeric as b, (r->>'D')::numeric as d, "
                "(r->>'volumen_ponderado')::numeric as costo, "
                "min((r->>'volumen_ponderado')::numeric) over(partition by ct.torre) as costo_optimo "
                "from {}.t_zapata_corrida_torre ct "
                "join {}.v_torre d on ln_dlt_gtc.torre_norm(d.nombre) =ln_dlt_gtc.torre_norm(ct.torre) "
                "cross join lateral jsonb_array_elements(ct.resultados) r(value) "
                "where zapata_corrida_id = %s "
                "and (r->>'cumple')::bool "
                "and torre_info->>'tipo' = %s "
                "and d.resistencia_min_conc = %s "
                "and d.relacion_a_mc_max = %s "
                "and (ct.torre, (r->>'B')::numeric, (r->>'D')::numeric) not in "
                "( "
                "	select torre, b, d "
                "	from cll_dlt_gtc.t_torre_zapata_prohibida_exp "
                ") "
            ).format(*(self.esquema,)*2)
            dict_cur.execute(sql, (corrida_id, tipo, resistencia_min_conc, relacion_a_mc_max))
            return dict_cur.fetchall()

        except (Exception, psycopg2.Error) as error :
            print ("Error en base de datos", error)
            raise error

        finally:
            if(conn):
                dict_cur.close()
                conn.close()

    def listar_zapatas_prohibidas(self):
        """
        Consulta las zapatas prohibidas por torre
        debido a confiabilidad de la zona B,D
        
        Arguments:
            TODO
        
        Returns:
            List[DBFila] -- Lista de diccionarios que representan las prohibiciones [{"torre":., "b_min":., "d_max":., "b_max":., "d_max":.},]
        """        
        try:
            conn = psycopg2.connect(self.conn_string)
            dict_cur: psycopg2.extras.DictCursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            sql = (
                "select * "
                "from {}.t_torre_zapata_prohibida "
            ).format(self.esquema)
            dict_cur.execute(sql)
            return dict_cur.fetchall()

        except (Exception, psycopg2.Error) as error :
            print ("Error en base de datos", error)
            raise error

        finally:
            if(conn):
                dict_cur.close()
                conn.close()

    def guardar_resultados_zapatas_en_temp(self, corrida_id, tipo, resistencia_min_conc, relacion_a_mc_max):
        try:
            conn = psycopg2.connect(self.conn_string)
            cur = conn.cursor()
            sql = "delete from {}.resultados_temp".format(self.esquema)
            cur.execute(sql)
            sql = (
                "insert into {}.resultados_temp(torre, b, d, costo, costo_optimo) "
                "select ct.torre, (r->>'B')::numeric as b, (r->>'D')::numeric as d,  "
                "       (r->>'volumen_ponderado')::numeric as costo,  "
                "       min((r->>'volumen_ponderado')::numeric) over(partition by ct.torre) as costo_optimo "
                "from {}.t_zapata_corrida_torre ct "
                "join {}.v_torre d on ln_dlt_gtc.torre_norm(d.nombre) =ln_dlt_gtc.torre_norm(ct.torre) "
                "cross join lateral jsonb_array_elements(ct.resultados) r(value) "
                "where zapata_corrida_id = %s "
                "and (r->>'cumple')::bool "
                "and torre_info->>'tipo' = %s "
                "and d.resistencia_min_conc = %s "
                "and d.relacion_a_mc_max = %s "
                "and (ct.torre, (r->>'B')::numeric, (r->>'D')::numeric) not in "
                "( "
                "	select torre, b, d "
                "	from {}.t_torre_zapata_prohibida_exp  "
                "); "                
            ).format(self.esquema,self.esquema,self.esquema,self.esquema)
            cur.execute(sql, (corrida_id, tipo, resistencia_min_conc, relacion_a_mc_max))
        except (Exception, psycopg2.Error) as error :
            print ("Error en base de datos", error)
            return None
        
        finally:
            if(conn):
                cur.close()
                conn.commit()
                conn.close()

    def calcular_grupo_zapatas_cobertura_sobrecosto(self, b, d, porc_sobrecosto_max, torres_cubiertas):
        """
        TODO
        
        Arguments:
            TODO
        
        Returns:
            TODO
        """        
        try:
            conn = psycopg2.connect(self.conn_string)
            dict_cur: psycopg2.extras.DictCursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            if len(torres_cubiertas) > 0:
                sql = (
                    "select count(*) as cobertura, sum(costo) as costo, sum(costo_optimo) as costo_optimo, sum(costo - costo_optimo) as sobrecosto, array_agg(torre) as torres "
                    "from {}.resultados_temp "
                    "where b=%s and d=%s "
                    "and (costo - costo_optimo)/costo_optimo*100 < %s "
                    "and not torre = any(%s) "
                ).format(self.esquema)
                dict_cur.execute(sql, (b, d, porc_sobrecosto_max, torres_cubiertas))
                return dict_cur.fetchone()
            else:
                sql = (
                    "select count(*) as cobertura, sum(costo) as costo, sum(costo_optimo) as costo_optimo, sum(costo - costo_optimo) as sobrecosto, array_agg(torre) as torres "
                    "from {}.resultados_temp "
                    "where b=%s and d=%s "
                    "and (costo - costo_optimo)/costo_optimo*100 < %s "
                ).format(self.esquema)
                dict_cur.execute(sql, (b, d, porc_sobrecosto_max))
                return dict_cur.fetchone()

        except (Exception, psycopg2.Error) as error :
            print ("Error en base de datos", error)
            raise error

        finally:
            if(conn):
                dict_cur.close()
                conn.close()

    def listar_grupos_zapata_posibles(self, torres_cubiertas):
        """
        TODO
        
        Arguments:
            TODO
        
        Returns:
            TODO
        """        
        try:
            conn = psycopg2.connect(self.conn_string)
            dict_cur: psycopg2.extras.DictCursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            if len(torres_cubiertas) > 0:
                sql = (
                    "select distinct b, d "
                    "from {}.resultados_temp "
                    "where not torre = any(%s) "
                    "order by b,d "
                ).format(self.esquema)
                dict_cur.execute(sql, (torres_cubiertas,))
                return dict_cur.fetchall()
            else:
                sql = (
                    "select distinct b, d "
                    "from {}.resultados_temp "
                    "order by b,d "
                ).format(self.esquema)
                dict_cur.execute(sql)
                return dict_cur.fetchall()

        except (Exception, psycopg2.Error) as error :
            print ("Error en base de datos", error)
            raise error

        finally:
            if(conn):
                dict_cur.close()
                conn.close()        

    def guardar_zapata_corrida_grupo2(self, grupo: Dict, escenario: str):
        try:
            conn = psycopg2.connect(self.conn_string)
            cur = conn.cursor()
            sql = "insert into {}.t_zapata_corrida_grupo(zapata_corrida_id, tipo, concreto, orden, b, d, cantidad, porc_sobrecosto, vol_optimos, vol_grupo, qs, relleno, geometrias, porc_sobrecosto_max, torres, escenario) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) returning id".format(self.esquema)
            json_qs = json.dumps(grupo["qs"])
            json_relleno = json.dumps(grupo["relleno"])
            json_geometrias = json.dumps(grupo["geometrias"])
            torres = ','.join(grupo["torres"])
            cur.execute(sql, (
                grupo["zapata_corrida_id"],
                grupo["tipo"],
                grupo["concreto"],
                grupo["orden"],
                grupo["b"],
                grupo["d"],
                grupo["cobertura"],
                grupo["porc_sobrecosto"],
                grupo["costo_optimo"],
                grupo["costo"],
                json_qs,
                json_relleno,
                json_geometrias,
                grupo["porc_sobrecosto_max"],
                torres,
                escenario ))
        
        except (Exception, psycopg2.Error) as error :
            print ("Error en base de datos", error)
            return None
        
        finally:
            if(conn):
                cur.close()
                conn.commit()
                conn.close()

    def listar_grupos_zapatas_finales(self, corrida_id):
        """
        TODO
        
        Arguments:
            TODO
        
        Returns:
            TODO
        """        
        try:
            conn = psycopg2.connect(self.conn_string)
            dict_cur: psycopg2.extras.DictCursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            sql = (
                " with grupos as "
                " ( "
                "	select * "
                "	from {}.t_zapata_corrida_grupo_final "
                "	where zapata_corrida_id=%s "
                "	order by tipo, concreto "
                " ) "
                " select g.*, h.h "
                " from grupos g "
                " join {}.t_zapata_grupo_final_h h on h.tipo=g.tipo  "
                "												and h.concreto=g.concreto "
                "												and h.b=g.b "
                "												and h.d=g.d "
                " order by g.tipo, g.concreto, g.cantidad desc "
            ).format(self.esquema, self.esquema)
            dict_cur.execute(sql, (corrida_id,))
            return dict_cur.fetchall()

        except (Exception, psycopg2.Error) as error :
            print ("Error en base de datos", error)
            raise error

        finally:
            if(conn):
                dict_cur.close()
                conn.close()            

    def listar_zapata_grupo(self, conjunto):
        """
        TODO
        
        Arguments:
            TODO
        
        Returns:
            TODO
        """        
        try:
            conn = psycopg2.connect(self.conn_string)
            dict_cur: psycopg2.extras.DictCursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            sql = (
                "select * "
                "from {}.t_zapata_grupo "
                "where conjunto = %s "
            ).format(self.esquema, self.esquema)
            dict_cur.execute(sql, (conjunto,))
            return dict_cur.fetchall()

        except (Exception, psycopg2.Error) as error :
            print ("Error en base de datos", error)
            raise error

        finally:
            if(conn):
                dict_cur.close()
                conn.close()            




    def actualizar_grupo_zapatas_finales(self, grupo):
        try:
            conn = psycopg2.connect(self.conn_string)
            cur = conn.cursor()
            sql = (
                "update {}.t_zapata_corrida_grupo_final set "
                "qs = %s, "
                "relleno = %s, "
                "geometrias = %s, "
                "qs_con_h_grupo = %s "
                "where id=%s "
            ).format(self.esquema)
            json_qs = json.dumps(grupo["qs"])
            json_relleno = json.dumps(grupo["relleno"])
            json_geometrias = json.dumps(grupo["geometrias"])
            cur.execute(sql, (
                json_qs,
                json_relleno,
                json_geometrias,
                grupo["qs_con_h_grupo"],
                grupo["id"] ))
        
        except (Exception, psycopg2.Error) as error :
            print ("Error en base de datos", error)
            return None
        
        finally:
            if(conn):
                cur.close()
                conn.commit()
                conn.close()

    def listar_grupos_zapatas_por_torre(self, corrida_id):
        """
        TODO
        
        Arguments:
            TODO
        
        Returns:
            TODO
        """        
        try:
            conn = psycopg2.connect(self.conn_string)
            dict_cur: psycopg2.extras.DictCursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            sql = (
                " select tipo, concreto, b, d, h_est, unnest(string_to_array(torres,',')) as torre "
                " from {}.t_zapata_corrida_grupo_final "
                " where zapata_corrida_id = %s "
            ).format(self.esquema)
            dict_cur.execute(sql, (corrida_id,))
            return dict_cur.fetchall()

        except (Exception, psycopg2.Error) as error :
            print ("Error en base de datos", error)
            raise error

        finally:
            if(conn):
                dict_cur.close()
                conn.close()          

    def listar_zapata_grupo(self, conjunto):
        """
        ToDo
        
        Arguments:
            ToDo
        
        Returns:
            List[DBFila] -- 
        """        
        try:
            conn = psycopg2.connect(self.conn_string)
            dict_cur: psycopg2.extras.DictCursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            sql = (
                "select * "
                "from {}.t_zapata_grupo "
                "where conjunto = %s "
            ).format(self.esquema)
            dict_cur.execute(sql, (conjunto,))
            return dict_cur.fetchall()

        except (Exception, psycopg2.Error) as error :
            print ("Error en base de datos", error)
            raise error

        finally:
            if(conn):
                dict_cur.close()
                conn.close()

    def actualizar_zapata_grupo(self, grupo):
        try:
            conn = psycopg2.connect(self.conn_string)
            cur = conn.cursor()
            sql = (
                "update {}.t_zapata_grupo set "
                "qs_h_propio = %s, "
                "qs_h_grupo = %s, "
                "relleno = %s, "
                "geometrias = %s "
                "where id=%s "
            ).format(self.esquema)
            cur.execute(sql, (
                grupo["qs_h_propio"],
                grupo["qs_h_grupo"],
                grupo["relleno"],
                grupo["geometrias"],
                grupo["id"] ))
        
        except (Exception, psycopg2.Error) as error :
            print ("Error en base de datos", error)
            return None
        
        finally:
            if(conn):
                cur.close()
                conn.commit()
                conn.close()

    def listar_micropilotes_grupo(self, conjunto):
        """
        ToDo
        
        Arguments:
            ToDo
        
        Returns:
            List[DBFila] -- 
        """        
        try:
            conn = psycopg2.connect(self.conn_string)
            dict_cur: psycopg2.extras.DictCursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            sql = (
                "select * "
                "from {}.grupos_mp_finales "
                "where conjunto = %s "
            ).format(self.esquema)
            dict_cur.execute(sql, (conjunto,))
            return dict_cur.fetchall()

        except (Exception, psycopg2.Error) as error :
            print ("Error en base de datos", error)
            raise error

        finally:
            if(conn):
                dict_cur.close()
                conn.close()

    def actualizar_micropilotes_grupo(self, grupo):
        try:
            conn = psycopg2.connect(self.conn_string)
            cur = conn.cursor()
            sql = (
                "update {}.grupos_mp_finales set "
                "maximos_propio = %s, "
                "maximos_grupo = %s, "
                "relleno = %s, "
                "geometrias = %s "
                "where id=%s "
            ).format(self.esquema)
            cur.execute(sql, (
                grupo["maximos_propio"],
                grupo["maximos_grupo"],
                grupo["relleno"],
                grupo["geometrias"],
                grupo["id"] ))
        
        except (Exception, psycopg2.Error) as error :
            print ("Error en base de datos", error)
            return None
        
        finally:
            if(conn):
                cur.close()
                conn.commit()
                conn.close()

    def guardar_micropilotes_suelo(self, torre, resultados):
        try:
            conn = psycopg2.connect(self.conn_string)
            cur = conn.cursor()
            sql = "insert into {}.mp_suelo(torre, resultados) values(%s,%s)".format(self.esquema)
            json_resultados = json.dumps(resultados)
            cur.execute(sql, (torre, json_resultados))
        
        except (Exception, psycopg2.Error) as error :
            print ("Error en base de datos", error)
            return None
        
        finally:
            if(conn):
                cur.close()
                conn.commit()
                conn.close()
    
    def listar_micropilotes_grupos_optimos(self):
        try:
            conn = psycopg2.connect(self.conn_string)
            dict_cur: psycopg2.extras.DictCursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            sql = """
                with optimos as
                (
                    select distinct on(torre) *
                    from {}.m_micropilotes_corrida_integrada_1
                    order by torre, calificacion
                )
                select o.tipo, t.resistencia_min_conc, proc_iny, barra_nombre, n_m, d_p, l_b, b, d_f, count(*) as cantidad, array_agg(o.torre) as torres   
                from optimos o
                join {}.v_torre t on t.nombre=o.torre
                where o.cumple
                group by o.tipo, t.resistencia_min_conc, proc_iny, barra_nombre, n_m, d_p, l_b, b, d_f
            """.format(self.esquema, self.esquema)
            dict_cur.execute(sql)
            return dict_cur.fetchall()
        
        except (Exception, psycopg2.Error) as error :
            print ("Error en base de datos", error)
            return None
        
        finally:
            if(conn):
                dict_cur.close()
                conn.close()             

    def recuperar_mejor_grupo_micropilotes_back(self, torres_excluir, grupos_excluir, porc_sobrecosto):
        try:
            conn = psycopg2.connect(self.conn_string)
            dict_cur: psycopg2.extras.DictCursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            sql = """
                with optimos as
                (
                    select distinct on (torre) ci.*
                    from {}.m_micropilotes_corrida_integrada_1 ci
                    where ci.cumple
                    order by torre, ci.calificacion
                ), pochos as
                (
                    select ci.grupo, ci.tipo, ci.resistencia_min_conc, ci.proc_iny, ci.barra_nombre, ci.n_m, ci.d_p, ci.l_b, ci.b, ci.d_f, count(*) as cobertura, array_agg(ci.torre) as torres, sum(ci.calificacion[2] - op.calificacion[2]) as sobrecosto
                    from {}.m_micropilotes_corrida_integrada_1 ci
                    join optimos op on ci.torre=op.torre
                    where ci.cumple
                    and not ci.torre = any(%s) 
                    and not ci.grupo = any(%s)
                    and abs((ci.calificacion[2] - op.calificacion[2])/op.calificacion[2]*100) <= %s
                    group by ci.grupo,ci.tipo, ci.resistencia_min_conc, ci.proc_iny, ci.barra_nombre, ci.n_m, ci.d_p, ci.l_b, ci.b, ci.d_f
                )
                select *
                from pochos
                order by cobertura desc, sobrecosto
                limit 1
            """.format(self.esquema, self.esquema)
            dict_cur.execute(sql, (torres_excluir,grupos_excluir,porc_sobrecosto))
            recs = dict_cur.fetchone()
            return recs
        
        except (Exception, psycopg2.Error) as error :
            print ("Error en base de datos", error)
            return None
        
        finally:
            if(conn):
                dict_cur.close()
                conn.close() 

    def recuperar_mejor_grupo_micropilotes_2(self, torres_excluir, grupos_excluir, porc_sobrecosto):
        try:
            conn = psycopg2.connect(self.conn_string)
            dict_cur: psycopg2.extras.DictCursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            sql = """
                with optimos as
                (
                    select distinct on (torre) ci.*
                    from {}.m_micropilotes_corrida_integrada_2x ci
                    where ci.cumple
                    order by torre, ci.calificacion
                ), pochos as
                (
                    select ci.grupo, ci.tipo, ci.resistencia_min_conc, ci.proc_iny, ci.barra_nombre, ci.n_m, ci.d_p, ci.l_b, ci.b, ci.d_f, count(*) as cobertura, 
                    array_agg(ci.torre) as torres_cubiertas, array_to_string(array_agg(ci.torre),',') as torres, sum(ci.calificacion[2] - op.calificacion[2]) as sobrecosto,
                    min(ci.h) as h_min, max(ci.h) as h_max, min(ci.tp) as tp_min, max(ci.tp) as tp_max
                    from {}.m_micropilotes_corrida_integrada_2x ci
                    join optimos op on ci.torre=op.torre
                    where ci.cumple
                    and not ci.torre = any(%s) 
                    and not ci.grupo = any(%s)
                    and abs((ci.calificacion[2] - op.calificacion[2])/op.calificacion[2]*100) <= %s
                    group by ci.grupo,ci.tipo, ci.resistencia_min_conc, ci.proc_iny, ci.barra_nombre, ci.n_m, ci.d_p, ci.l_b, ci.b, ci.d_f
                )
                select *
                from pochos
                order by cobertura desc, sobrecosto
                limit 1
            """.format(self.esquema, self.esquema)
            dict_cur.execute(sql, (torres_excluir,grupos_excluir,porc_sobrecosto))
            recs = dict_cur.fetchone()
            return recs
        
        except (Exception, psycopg2.Error) as error :
            print ("Error en base de datos", error)
            return None
        
        finally:
            if(conn):
                dict_cur.close()
                conn.close() 

    def recuperar_mejor_grupo_micropilotes_3(self, torres_excluir, grupos_excluir, porc_sobrecosto):
        try:
            conn = psycopg2.connect(self.conn_string)
            dict_cur: psycopg2.extras.DictCursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            sql = """
                with optimos as
                (
                    select distinct on (torre) ci.*
                    from {}.m_micropilotes_corrida_integrada_3 ci
                    where ci.cumple
                    order by torre, ci.calificacion
                ), pochos as
                (
                    select ci.grupo, ci.tipo, ci.resistencia_min_conc, ci.proc_iny, ci.barra_nombre, ci.n_m, ci.d_p, ci.l_b, ci.b, ci.d_f, count(*) as cobertura, 
                            array_agg(ci.torre) as torres_cubiertas, array_to_string(array_agg(ci.torre),',') as torres, sum(ci.calificacion[2] - op.calificacion[2]) as sobrecosto,
                            min(ci.h) as h_min, max(ci.h) as h_max, min(ci.tp) as tp_min, max(ci.tp) as tp_max
                    from {}.m_micropilotes_corrida_integrada_3 ci
                    join optimos op on ci.torre=op.torre
                    where ci.cumple
                    and not ci.torre = any(%s) 
                    and not ci.grupo = any(%s)
                    and abs((ci.calificacion[2] - op.calificacion[2])/op.calificacion[2]*100) <= %s
                    group by ci.grupo,ci.tipo, ci.resistencia_min_conc, ci.proc_iny, ci.barra_nombre, ci.n_m, ci.d_p, ci.l_b, ci.b, ci.d_f
                )
                select *
                from pochos
                order by cobertura desc, sobrecosto
                limit 1
            """.format(self.esquema, self.esquema)
            dict_cur.execute(sql, (torres_excluir,grupos_excluir,porc_sobrecosto))
            recs = dict_cur.fetchone()
            return recs
        
        except (Exception, psycopg2.Error) as error :
            print ("Error en base de datos", error)
            return None
        
        finally:
            if(conn):
                dict_cur.close()
                conn.close() 

    def recuperar_mejor_grupo_micropilotes_2a(self, torres_excluir, grupos_excluir, porc_sobrecosto):
        try:
            conn = psycopg2.connect(self.conn_string)
            dict_cur: psycopg2.extras.DictCursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            sql = """
                with optimos as
                (
                    select distinct on (torre) ci.*
                    from {}.m_micropilotes_corrida_integrada_2a ci
                    where ci.cumple
                    order by torre, ci.calificacion
                ), pochos as
                (
                    select ci.grupo, ci.tipo, ci.resistencia_min_conc, ci.proc_iny, ci.barra_nombre, ci.n_m, ci.d_p, ci.l_b, ci.b, ci.d_f, count(*) as cobertura, 
                    array_agg(ci.torre) as torres_cubiertas, array_to_string(array_agg(ci.torre),',') as torres, sum(ci.calificacion[2] - op.calificacion[2]) as sobrecosto,
                    min(ci.h) as h_min, max(ci.h) as h_max, min(ci.tp) as tp_min, max(ci.tp) as tp_max
                    from {}.m_micropilotes_corrida_integrada_2a ci
                    join optimos op on ci.torre=op.torre
                    where ci.cumple
                    and not ci.torre = any(%s) 
                    and not ci.grupo = any(%s)
                    and abs((ci.calificacion[2] - op.calificacion[2])/op.calificacion[2]*100) <= %s
                    group by ci.grupo,ci.tipo, ci.resistencia_min_conc, ci.proc_iny, ci.barra_nombre, ci.n_m, ci.d_p, ci.l_b, ci.b, ci.d_f
                )
                select *
                from pochos
                order by cobertura desc, sobrecosto
                limit 1
            """.format(self.esquema, self.esquema)
            dict_cur.execute(sql, (torres_excluir,grupos_excluir,porc_sobrecosto))
            recs = dict_cur.fetchone()
            return recs
        
        except (Exception, psycopg2.Error) as error :
            print ("Error en base de datos", error)
            return None
        
        finally:
            if(conn):
                dict_cur.close()
                conn.close() 

    def recuperar_mejor_grupo_micropilotes_2b(self, torres_excluir, grupos_excluir, porc_sobrecosto):
        try:
            conn = psycopg2.connect(self.conn_string)
            dict_cur: psycopg2.extras.DictCursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            sql = """
                with optimos as
                (
                    select distinct on (torre) ci.*
                    from {}.m_micropilotes_corrida_integrada_2b ci
                    where ci.cumple
                    order by torre, ci.calificacion
                ), pochos as
                (
                    select ci.grupo, ci.tipo, ci.resistencia_min_conc, ci.proc_iny, ci.barra_nombre, ci.n_m, ci.d_p, ci.l_b, ci.b, ci.d_f, count(*) as cobertura, 
                    array_agg(ci.torre) as torres_cubiertas, array_to_string(array_agg(ci.torre),',') as torres, sum(ci.calificacion[2] - op.calificacion[2]) as sobrecosto,
                    min(ci.h) as h_min, max(ci.h) as h_max, min(ci.tp) as tp_min, max(ci.tp) as tp_max
                    from {}.m_micropilotes_corrida_integrada_2b ci
                    join optimos op on ci.torre=op.torre
                    where ci.cumple
                    and not ci.torre = any(%s) 
                    and not ci.grupo = any(%s)
                    and abs((ci.calificacion[2] - op.calificacion[2])/op.calificacion[2]*100) <= %s
                    group by ci.grupo,ci.tipo, ci.resistencia_min_conc, ci.proc_iny, ci.barra_nombre, ci.n_m, ci.d_p, ci.l_b, ci.b, ci.d_f
                )
                select *
                from pochos
                order by cobertura desc, sobrecosto
                limit 1
            """.format(self.esquema, self.esquema)
            dict_cur.execute(sql, (torres_excluir,grupos_excluir,porc_sobrecosto))
            recs = dict_cur.fetchone()
            return recs
        
        except (Exception, psycopg2.Error) as error :
            print ("Error en base de datos", error)
            return None
        
        finally:
            if(conn):
                dict_cur.close()
                conn.close() 

    def recuperar_mejor_grupo_micropilotes_4(self, torres_excluir, grupos_excluir, porc_sobrecosto):
        try:
            conn = psycopg2.connect(self.conn_string)
            dict_cur: psycopg2.extras.DictCursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            sql = """
                with optimos as
                (
                    select distinct on (torre) ci.*
                    from {}.m_micropilotes_corrida_integrada_4 ci
                    where ci.cumple
                    order by torre, ci.calificacion
                ), pochos as
                (
                    select ci.grupo, ci.tipo, ci.resistencia_min_conc, ci.proc_iny, ci.barra_nombre, ci.n_m, ci.d_p, ci.l_b, ci.b, ci.d_f, count(*) as cobertura, 
                            array_agg(ci.torre) as torres_cubiertas, array_to_string(array_agg(ci.torre),',') as torres, sum(ci.calificacion[2] - op.calificacion[2]) as sobrecosto,
                            min(ci.h) as h_min, max(ci.h) as h_max, min(ci.tp) as tp_min, max(ci.tp) as tp_max
                    from {}.m_micropilotes_corrida_integrada_4 ci
                    join optimos op on ci.torre=op.torre
                    where ci.cumple
                    and not ci.torre = any(%s) 
                    and not ci.grupo = any(%s)
                    and abs((ci.calificacion[2] - op.calificacion[2])/op.calificacion[2]*100) <= %s
                    group by ci.grupo,ci.tipo, ci.resistencia_min_conc, ci.proc_iny, ci.barra_nombre, ci.n_m, ci.d_p, ci.l_b, ci.b, ci.d_f
                )
                select *
                from pochos
                order by cobertura desc, sobrecosto
                limit 1
            """.format(self.esquema, self.esquema)
            dict_cur.execute(sql, (torres_excluir,grupos_excluir,porc_sobrecosto))
            recs = dict_cur.fetchone()
            return recs
        
        except (Exception, psycopg2.Error) as error :
            print ("Error en base de datos", error)
            return None
        
        finally:
            if(conn):
                dict_cur.close()
                conn.close() 

    def recuperar_mejor_grupo_micropilotes_5(self, torres_excluir, grupos_excluir, porc_sobrecosto):
        try:
            conn = psycopg2.connect(self.conn_string)
            dict_cur: psycopg2.extras.DictCursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            sql = """
                with optimos as
                (
                    select distinct on (torre) ci.*
                    from {}.m_micropilotes_corrida_integrada_5 ci
                    where ci.cumple
                    order by torre, ci.calificacion
                ), pochos as
                (
                    select ci.grupo, ci.tipo, ci.resistencia_min_conc, ci.proc_iny, ci.barra_nombre, ci.n_m, ci.d_p, ci.l_b, ci.b, ci.d_f, count(*) as cobertura, 
                            array_agg(ci.torre) as torres_cubiertas, array_to_string(array_agg(ci.torre),',') as torres, sum(ci.calificacion[2] - op.calificacion[2]) as sobrecosto,
                            min(ci.h) as h_min, max(ci.h) as h_max, min(ci.tp) as tp_min, max(ci.tp) as tp_max
                    from {}.m_micropilotes_corrida_integrada_5 ci
                    join optimos op on ci.torre=op.torre
                    where ci.cumple
                    and not ci.torre = any(%s) 
                    and not ci.grupo = any(%s)
                    and abs((ci.calificacion[2] - op.calificacion[2])/op.calificacion[2]*100) <= %s
                    group by ci.grupo,ci.tipo, ci.resistencia_min_conc, ci.proc_iny, ci.barra_nombre, ci.n_m, ci.d_p, ci.l_b, ci.b, ci.d_f
                )
                select *
                from pochos
                order by cobertura desc, sobrecosto
                limit 1
            """.format(self.esquema, self.esquema)
            dict_cur.execute(sql, (torres_excluir,grupos_excluir,porc_sobrecosto))
            recs = dict_cur.fetchone()
            return recs
        
        except (Exception, psycopg2.Error) as error :
            print ("Error en base de datos", error)
            return None
        
        finally:
            if(conn):
                dict_cur.close()
                conn.close() 

    def recuperar_mejor_grupo_micropilotes_6(self, torres_excluir, grupos_excluir, porc_sobrecosto):
        try:
            conn = psycopg2.connect(self.conn_string)
            dict_cur: psycopg2.extras.DictCursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            sql = """
                with optimos as
                (
                    select distinct on (torre) ci.*
                    from {}.m_micropilotes_corrida_integrada_6 ci
                    where ci.cumple
                    order by torre, ci.calificacion
                ), pochos as
                (
                    select ci.grupo, ci.tipo, ci.resistencia_min_conc, ci.proc_iny, ci.barra_nombre, ci.n_m, ci.d_p, ci.l_b, ci.b, ci.d_f, ci.s_m, count(*) as cobertura, 
                            array_agg(ci.torre) as torres_cubiertas, array_to_string(array_agg(ci.torre),',') as torres, sum(ci.calificacion[2] - op.calificacion[2]) as sobrecosto,
                            min(ci.h) as h_min, max(ci.h) as h_max, min(ci.tp) as tp_min, max(ci.tp) as tp_max
                    from {}.m_micropilotes_corrida_integrada_6 ci
                    join optimos op on ci.torre=op.torre
                    where ci.cumple
                    and not ci.torre = any(%s) 
                    and not ci.grupo = any(%s)
                    and abs((ci.calificacion[2] - op.calificacion[2])/op.calificacion[2]*100) <= %s
                    group by ci.grupo,ci.tipo, ci.resistencia_min_conc, ci.proc_iny, ci.barra_nombre, ci.n_m, ci.d_p, ci.l_b, ci.b, ci.d_f, ci.s_m
                )
                select *
                from pochos
                order by cobertura desc, sobrecosto
                limit 1
            """.format(self.esquema, self.esquema)
            dict_cur.execute(sql, (torres_excluir,grupos_excluir,porc_sobrecosto))
            recs = dict_cur.fetchone()
            return recs

        except (Exception, psycopg2.Error) as error :
            print ("Error en base de datos", error)
            return None
        
        finally:
            if(conn):
                dict_cur.close()
                conn.close() 

    def recuperar_mejor_grupo_micropilotes_7(self, torres_excluir, grupos_excluir, porc_sobrecosto):
        try:
            conn = psycopg2.connect(self.conn_string)
            dict_cur: psycopg2.extras.DictCursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            sql = """
                with optimos as
                (
                    select distinct on (torre) ci.*
                    from {}.m_micropilotes_corrida_integrada_7 ci
                    where ci.cumple
                    order by torre, ci.calificacion
                ), pochos as
                (
                    select ci.grupo, ci.tipo, ci.resistencia_min_conc, ci.proc_iny, ci.barra_nombre, ci.n_m, ci.d_p, ci.l_b, ci.b, ci.d_f, count(*) as cobertura, 
                            array_agg(ci.torre) as torres_cubiertas, array_to_string(array_agg(ci.torre),',') as torres, sum(ci.calificacion[2] - op.calificacion[2]) as sobrecosto,
                            min(ci.h) as h_min, max(ci.h) as h_max, min(ci.tp) as tp_min, max(ci.tp) as tp_max
                    from {}.m_micropilotes_corrida_integrada_7 ci
                    join optimos op on ci.torre=op.torre
                    where ci.cumple
                    and not ci.torre = any(%s) 
                    and not ci.grupo = any(%s)
                    and abs((ci.calificacion[2] - op.calificacion[2])/op.calificacion[2]*100) <= %s
                    group by ci.grupo,ci.tipo, ci.resistencia_min_conc, ci.proc_iny, ci.barra_nombre, ci.n_m, ci.d_p, ci.l_b, ci.b, ci.d_f
                )
                select *
                from pochos
                order by cobertura desc, sobrecosto
                limit 1
            """.format(self.esquema, self.esquema)
            dict_cur.execute(sql, (torres_excluir,grupos_excluir,porc_sobrecosto))
            recs = dict_cur.fetchone()
            return recs
        
        except (Exception, psycopg2.Error) as error :
            print ("Error en base de datos", error)
            return None
        
        finally:
            if(conn):
                dict_cur.close()
                conn.close() 

    def recuperar_mejor_grupo_micropilotes_8(self, torres_excluir, grupos_excluir, porc_sobrecosto):
        try:
            conn = psycopg2.connect(self.conn_string)
            dict_cur: psycopg2.extras.DictCursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            sql = """
                with optimos as
                (
                    select distinct on (torre) ci.*
                    from {}.m_micropilotes_corrida_integrada_8 ci
                    where ci.cumple
                    order by torre, ci.calificacion
                ), pochos as
                (
                    select ci.grupo, ci.tipo, ci.resistencia_min_conc, ci.proc_iny, ci.barra_nombre, ci.n_m, ci.d_p, ci.l_b, ci.b, ci.d_f, count(*) as cobertura, 
                            array_agg(ci.torre) as torres_cubiertas, array_to_string(array_agg(ci.torre),',') as torres, sum(ci.calificacion[2] - op.calificacion[2]) as sobrecosto,
                            min(ci.h) as h_min, max(ci.h) as h_max, min(ci.tp) as tp_min, max(ci.tp) as tp_max
                    from {}.m_micropilotes_corrida_integrada_8 ci
                    join optimos op on ci.torre=op.torre
                    where ci.cumple
                    and not ci.torre = any(%s) 
                    and not ci.grupo = any(%s)
                    and abs((ci.calificacion[2] - op.calificacion[2])/op.calificacion[2]*100) <= %s
                    group by ci.grupo,ci.tipo, ci.resistencia_min_conc, ci.proc_iny, ci.barra_nombre, ci.n_m, ci.d_p, ci.l_b, ci.b, ci.d_f
                )
                select *
                from pochos
                order by cobertura desc, sobrecosto
                limit 1
            """.format(self.esquema, self.esquema)
            dict_cur.execute(sql, (torres_excluir,grupos_excluir,porc_sobrecosto))
            recs = dict_cur.fetchone()
            return recs
        
        except (Exception, psycopg2.Error) as error :
            print ("Error en base de datos", error)
            return None
        
        finally:
            if(conn):
                dict_cur.close()
                conn.close() 

    def recuperar_mejor_grupo_micropilotes_9(self, torres_excluir, grupos_excluir, porc_sobrecosto):
        try:
            conn = psycopg2.connect(self.conn_string)
            dict_cur: psycopg2.extras.DictCursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            sql = """
                with optimos as
                (
                    select distinct on (torre) ci.*
                    from {}.m_micropilotes_corrida_integrada_9 ci
                    where ci.cumple
                    order by torre, ci.calificacion
                ), pochos as
                (
                    select ci.grupo, ci.tipo, ci.resistencia_min_conc, ci.proc_iny, ci.barra_nombre, ci.n_m, ci.d_p, ci.l_b, ci.b, ci.d_f, count(*) as cobertura, 
                            array_agg(ci.torre) as torres_cubiertas, array_to_string(array_agg(ci.torre),',') as torres, sum(ci.calificacion[2] - op.calificacion[2]) as sobrecosto,
                            min(ci.h) as h_min, max(ci.h) as h_max, min(ci.tp) as tp_min, max(ci.tp) as tp_max
                    from {}.m_micropilotes_corrida_integrada_9 ci
                    join optimos op on ci.torre=op.torre
                    where ci.cumple
                    and not ci.torre = any(%s) 
                    and not ci.grupo = any(%s)
                    and abs((ci.calificacion[2] - op.calificacion[2])/op.calificacion[2]*100) <= %s
                    group by ci.grupo,ci.tipo, ci.resistencia_min_conc, ci.proc_iny, ci.barra_nombre, ci.n_m, ci.d_p, ci.l_b, ci.b, ci.d_f
                )
                select *
                from pochos
                order by cobertura desc, sobrecosto
                limit 1
            """.format(self.esquema, self.esquema)
            dict_cur.execute(sql, (torres_excluir,grupos_excluir,porc_sobrecosto))
            recs = dict_cur.fetchone()
            return recs
        
        except (Exception, psycopg2.Error) as error :
            print ("Error en base de datos", error)
            return None
        
        finally:
            if(conn):
                dict_cur.close()
                conn.close() 

    def recuperar_mejor_grupo_micropilotes_12(self, torres_excluir, grupos_excluir, porc_sobrecosto):
        try:
            conn = psycopg2.connect(self.conn_string)
            dict_cur: psycopg2.extras.DictCursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            sql = """
                with optimos as
                (
                    select distinct on (torre) ci.*
                    from {}.m_micropilotes_corrida_integrada_12 ci
                    where ci.cumple
                    order by torre, ci.calificacion
                ), pochos as
                (
                    select ci.grupo, ci.tipo, ci.resistencia_min_conc, ci.proc_iny, ci.barra_nombre, ci.n_m, ci.d_p, ci.l_b, ci.b, ci.d_f, ci.s_m, count(*) as cobertura, 
                            array_agg(ci.torre) as torres_cubiertas, array_to_string(array_agg(ci.torre),',') as torres, sum(ci.calificacion[2] - op.calificacion[2]) as sobrecosto,
                            min(ci.h) as h_min, max(ci.h) as h_max, min(ci.tp) as tp_min, max(ci.tp) as tp_max
                    from {}.m_micropilotes_corrida_integrada_12 ci
                    join optimos op on ci.torre=op.torre
                    where ci.cumple
                    and not ci.torre = any(%s) 
                    and not ci.grupo = any(%s)
                    and abs((ci.calificacion[2] - op.calificacion[2])/op.calificacion[2]*100) <= %s
                    group by ci.grupo,ci.tipo, ci.resistencia_min_conc, ci.proc_iny, ci.barra_nombre, ci.n_m, ci.d_p, ci.l_b, ci.b, ci.d_f, ci.s_m
                )
                select *
                from pochos
                order by cobertura desc, sobrecosto
                limit 1
            """.format(self.esquema, self.esquema)
            dict_cur.execute(sql, (torres_excluir,grupos_excluir,porc_sobrecosto))
            recs = dict_cur.fetchone()
            return recs

        except (Exception, psycopg2.Error) as error :
            print ("Error en base de datos", error)
            return None
        
        finally:
            if(conn):
                dict_cur.close()
                conn.close() 

    def recuperar_mejor_grupo_micropilotes_12x(self, torres_excluir, grupos_excluir, porc_sobrecosto):
        try:
            conn = psycopg2.connect(self.conn_string)
            dict_cur: psycopg2.extras.DictCursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            sql = """
                with optimos as
                (
                    select distinct on (torre) ci.*
                    from {}.m_micropilotes_corrida_integrada_12 ci
                    where ci.cumple
                    order by torre, ci.calificacion
                ), pochos as
                (
                    select ci.grupo, ci.tipo, ci.resistencia_min_conc, ci.proc_iny, ci.barra_nombre, ci.n_m, ci.d_p, ci.l_b, ci.b, ci.d_f, ci.s_m, count(*) as cobertura, 
                            array_agg(ci.torre) as torres_cubiertas, array_to_string(array_agg(ci.torre),',') as torres, sum(ci.calificacion[2] - op.calificacion[2]) as sobrecosto,
                            min(ci.h) as h_min, max(ci.h) as h_max, min(ci.tp) as tp_min, max(ci.tp) as tp_max
                    from {}.m_micropilotes_corrida_integrada_12 ci
                    join optimos op on ci.torre=op.torre
                    where ci.cumple
                    and not ci.torre = any(%s) 
                    and not ci.grupo = any(%s)
                    and abs((    
                        cll_dlt_gtc.costo_micropilotes(ci.resultado) - cll_dlt_gtc.costo_micropilotes(op.resultado)
                    )/cll_dlt_gtc.costo_micropilotes(op.resultado)*100) <= %s
                    group by ci.grupo,ci.tipo, ci.resistencia_min_conc, ci.proc_iny, ci.barra_nombre, ci.n_m, ci.d_p, ci.l_b, ci.b, ci.d_f, ci.s_m
                )
                select *
                from pochos
                order by cobertura desc, sobrecosto
                limit 1
            """.format(self.esquema, self.esquema)
            dict_cur.execute(sql, (torres_excluir,grupos_excluir,porc_sobrecosto))
            recs = dict_cur.fetchone()
            return recs

        except (Exception, psycopg2.Error) as error :
            print ("Error en base de datos", error)
            return None
        
        finally:
            if(conn):
                dict_cur.close()
                conn.close() 

    def recuperar_mejor_grupo_micropilotes_13(self, torres_excluir, grupos_excluir, porc_sobrecosto):
        try:
            conn = psycopg2.connect(self.conn_string)
            dict_cur: psycopg2.extras.DictCursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            sql = """
                with optimos as
                (
                    select distinct on (torre) ci.*
                    from {}.m_micropilotes_corrida_integrada_13 ci
                    where ci.cumple
                    order by torre, ci.calificacion
                ), pochos as
                (
                    select ci.grupo, ci.tipo, ci.resistencia_min_conc, ci.proc_iny, ci.barra_nombre, ci.n_m, ci.d_p, ci.l_b, ci.b, ci.d_f, ci.s_m, count(*) as cobertura, 
                            array_agg(ci.torre) as torres_cubiertas, array_to_string(array_agg(ci.torre),',') as torres, sum(ci.calificacion[2] - op.calificacion[2]) as sobrecosto,
                            min(ci.h) as h_min, max(ci.h) as h_max, min(ci.tp) as tp_min, max(ci.tp) as tp_max
                    from {}.m_micropilotes_corrida_integrada_13 ci
                    join optimos op on ci.torre=op.torre
                    where ci.cumple
                    and not ci.torre = any(%s) 
                    and not ci.grupo = any(%s)
                    and abs((ci.calificacion[2] - op.calificacion[2])/op.calificacion[2]*100) <= %s
                    group by ci.grupo,ci.tipo, ci.resistencia_min_conc, ci.proc_iny, ci.barra_nombre, ci.n_m, ci.d_p, ci.l_b, ci.b, ci.d_f, ci.s_m
                )
                select *
                from pochos
                order by cobertura desc, sobrecosto
                limit 1
            """.format(self.esquema, self.esquema)
            dict_cur.execute(sql, (torres_excluir,grupos_excluir,porc_sobrecosto))
            recs = dict_cur.fetchone()
            return recs

        except (Exception, psycopg2.Error) as error :
            print ("Error en base de datos", error)
            return None
        
        finally:
            if(conn):
                dict_cur.close()
                conn.close() 

    def recuperar_mejor_grupo_micropilotes_14(self, torres_excluir, grupos_excluir, porc_sobrecosto):
        try:
            conn = psycopg2.connect(self.conn_string)
            dict_cur: psycopg2.extras.DictCursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            sql = """
                with optimos as
                (
                    select distinct on (torre) ci.*
                    from {}.m_micropilotes_corrida_integrada_14 ci
                    where ci.cumple
                    order by torre, ci.calificacion
                ), pochos as
                (
                    select ci.grupo, ci.tipo, ci.resistencia_min_conc, ci.proc_iny, ci.barra_nombre, ci.n_m, ci.d_p, ci.l_b, ci.b, ci.d_f, ci.s_m, count(*) as cobertura, 
                            array_agg(ci.torre) as torres_cubiertas, array_to_string(array_agg(ci.torre),',') as torres, sum(ci.calificacion[2] - op.calificacion[2]) as sobrecosto,
                            min(ci.h) as h_min, max(ci.h) as h_max, min(ci.tp) as tp_min, max(ci.tp) as tp_max
                    from {}.m_micropilotes_corrida_integrada_14 ci
                    join optimos op on ci.torre=op.torre
                    where ci.cumple
                    and not ci.torre = any(%s) 
                    and not ci.grupo = any(%s)
                    and abs((ci.calificacion[2] - op.calificacion[2])/op.calificacion[2]*100) <= %s
                    group by ci.grupo,ci.tipo, ci.resistencia_min_conc, ci.proc_iny, ci.barra_nombre, ci.n_m, ci.d_p, ci.l_b, ci.b, ci.d_f, ci.s_m
                )
                select *
                from pochos
                order by cobertura desc, sobrecosto
                limit 1
            """.format(self.esquema, self.esquema)
            dict_cur.execute(sql, (torres_excluir,grupos_excluir,porc_sobrecosto))
            recs = dict_cur.fetchone()
            return recs

        except (Exception, psycopg2.Error) as error :
            print ("Error en base de datos", error)
            return None
        
        finally:
            if(conn):
                dict_cur.close()
                conn.close() 

    def recuperar_mejor_grupo_micropilotes_15(self, torres_excluir, grupos_excluir, porc_sobrecosto):
        try:
            conn = psycopg2.connect(self.conn_string)
            dict_cur: psycopg2.extras.DictCursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            sql = """
                with optimos as
                (
                    select distinct on (torre) ci.*
                    from {}.m_micropilotes_corrida_integrada_15 ci
                    where ci.cumple
                    order by torre, ci.calificacion
                ), pochos as
                (
                    select ci.grupo, ci.tipo, ci.resistencia_min_conc, ci.proc_iny, ci.barra_nombre, ci.n_m, ci.d_p, ci.l_b, ci.b, ci.d_f, ci.s_m, count(*) as cobertura, 
                            array_agg(ci.torre) as torres_cubiertas, array_to_string(array_agg(ci.torre),',') as torres, sum(ci.calificacion[2] - op.calificacion[2]) as sobrecosto,
                            min(ci.h) as h_min, max(ci.h) as h_max, min(ci.tp) as tp_min, max(ci.tp) as tp_max
                    from {}.m_micropilotes_corrida_integrada_15 ci
                    join optimos op on ci.torre=op.torre
                    where ci.cumple
                    and not ci.torre = any(%s) 
                    and not ci.grupo = any(%s)
                    and abs((ci.calificacion[2] - op.calificacion[2])/op.calificacion[2]*100) <= %s
                    group by ci.grupo,ci.tipo, ci.resistencia_min_conc, ci.proc_iny, ci.barra_nombre, ci.n_m, ci.d_p, ci.l_b, ci.b, ci.d_f, ci.s_m
                )
                select *
                from pochos
                order by cobertura desc, sobrecosto
                limit 1
            """.format(self.esquema, self.esquema)
            dict_cur.execute(sql, (torres_excluir,grupos_excluir,porc_sobrecosto))
            recs = dict_cur.fetchone()
            return recs

        except (Exception, psycopg2.Error) as error :
            print ("Error en base de datos", error)
            return None
        
        finally:
            if(conn):
                dict_cur.close()
                conn.close() 

    def recuperar_mejor_grupo_micropilotes_16(self, torres_excluir, grupos_excluir, porc_sobrecosto):
        try:
            conn = psycopg2.connect(self.conn_string)
            dict_cur: psycopg2.extras.DictCursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            sql = """
                with optimos as
                (
                    select distinct on (torre) ci.*
                    from {}.m_micropilotes_corrida_integrada_16 ci
                    where ci.cumple
                    order by torre, ci.calificacion
                ), pochos as
                (
                    select ci.grupo, ci.tipo, ci.resistencia_min_conc, ci.proc_iny, ci.barra_nombre, ci.n_m, ci.d_p, ci.l_b, ci.b, ci.d_f, ci.s_m, count(*) as cobertura, 
                            array_agg(ci.torre) as torres_cubiertas, array_to_string(array_agg(ci.torre),',') as torres, sum(ci.calificacion[2] - op.calificacion[2]) as sobrecosto,
                            min(ci.h) as h_min, max(ci.h) as h_max, min(ci.tp) as tp_min, max(ci.tp) as tp_max
                    from {}.m_micropilotes_corrida_integrada_16 ci
                    join optimos op on ci.torre=op.torre
                    where ci.cumple
                    and not ci.torre = any(%s) 
                    and not ci.grupo = any(%s)
                    and abs((ci.calificacion[2] - op.calificacion[2])/op.calificacion[2]*100) <= %s
                    group by ci.grupo,ci.tipo, ci.resistencia_min_conc, ci.proc_iny, ci.barra_nombre, ci.n_m, ci.d_p, ci.l_b, ci.b, ci.d_f, ci.s_m
                )
                select *
                from pochos
                order by cobertura desc, sobrecosto
                limit 1
            """.format(self.esquema, self.esquema)
            dict_cur.execute(sql, (torres_excluir,grupos_excluir,porc_sobrecosto))
            recs = dict_cur.fetchone()
            return recs

        except (Exception, psycopg2.Error) as error :
            print ("Error en base de datos", error)
            return None
        
        finally:
            if(conn):
                dict_cur.close()
                conn.close() 

    def recuperar_mejor_grupo_micropilotes_b_cob(self, torres_excluir, grupos_excluir, porc_sobrecosto, corrida_integrada_id):
        try:
            conn = psycopg2.connect(self.conn_string)
            dict_cur: psycopg2.extras.DictCursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            sql = """
                with optimos as
                (
                    select distinct on (torre) ci.*
                    from {}.m_micropilotes_corrida_integrada_{} ci
                    where ci.cumple
                    order by torre, ci.calificacion
                ), pochos as
                (
                    select ci.grupo, ci.tipo, ci.resistencia_min_conc, ci.proc_iny, ci.barra_nombre, ci.n_m, ci.d_p, ci.l_b, ci.con_camisa, ci.b, ci.d_f, ci.s_m, count(*) as cobertura, 
                            array_agg(ci.torre) as torres_cubiertas, array_to_string(array_agg(ci.torre),',') as torres, sum(ci.calificacion[2] - op.calificacion[2]) as sobrecosto,
                            min(ci.h) as h_min, max(ci.h) as h_max, min(ci.tp) as tp_min, max(ci.tp) as tp_max
                    from {}.m_micropilotes_corrida_integrada_{} ci
                    join optimos op on ci.torre=op.torre
                    where ci.cumple
                    and not ci.torre = any(%s) 
                    and not ci.grupo = any(%s)
                    and abs((ci.calificacion[2] - op.calificacion[2])/op.calificacion[2]*100) <= %s -- Se restringe desviación en costo, no en B
                    group by ci.grupo,ci.tipo, ci.resistencia_min_conc, ci.proc_iny, ci.barra_nombre, ci.n_m, ci.d_p, ci.l_b, ci.con_camisa, ci.b, ci.d_f, ci.s_m
                )
                select *
                from pochos
                order by cobertura desc, sobrecosto
                limit 1
            """.format(self.esquema, corrida_integrada_id, self.esquema, corrida_integrada_id)
            dict_cur.execute(sql, (torres_excluir,grupos_excluir,porc_sobrecosto))
            recs = dict_cur.fetchone()
            return recs

        except (Exception, psycopg2.Error) as error :
            print ("Error en base de datos", error)
            return None
        
        finally:
            if(conn):
                dict_cur.close()
                conn.close() 

    def recuperar_mejor_grupo_micropilotes_c_cob(self, torres_excluir, grupos_excluir, porc_sobrecosto, corrida_integrada_id):
        try:
            conn = psycopg2.connect(self.conn_string)
            dict_cur: psycopg2.extras.DictCursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            sql = """
                with optimos as
                (
                    select distinct on (torre) ci.*
                    from {}.m_micropilotes_corrida_integrada_{} ci
                    where ci.cumple
                    order by torre, ci.calificacion
                ), pochos as
                (
                    select ci.grupo, ci.tipo, ci.resistencia_min_conc, ci.proc_iny, ci.barra_nombre, ci.n_m, ci.d_p, ci.l_b, ci.con_camisa, ci.b, ci.d_f, ci.s_m, count(*) as cobertura, 
                            array_agg(ci.torre) as torres_cubiertas, array_to_string(array_agg(ci.torre),',') as torres, sum(ci.calificacion[2] - op.calificacion[2]) as sobrecosto,
                            min(ci.h) as h_min, max(ci.h) as h_max, min(ci.tp) as tp_min, max(ci.tp) as tp_max
                    from {}.m_micropilotes_corrida_integrada_{} ci
                    join optimos op on ci.torre=op.torre
                    where ci.cumple
                    and not ci.torre = any(%s) 
                    and not ci.grupo = any(%s)
                    and abs((ci.calificacion[3] - op.calificacion[3])/op.calificacion[3]*100) <= %s -- Se restringe desviación en costo, no en B
                    group by ci.grupo,ci.tipo, ci.resistencia_min_conc, ci.proc_iny, ci.barra_nombre, ci.n_m, ci.d_p, ci.l_b, ci.con_camisa, ci.b, ci.d_f, ci.s_m
                )
                select *
                from pochos
                order by cobertura desc, sobrecosto
                limit 1
            """.format(self.esquema, corrida_integrada_id, self.esquema, corrida_integrada_id)
            dict_cur.execute(sql, (torres_excluir,grupos_excluir,porc_sobrecosto))
            recs = dict_cur.fetchone()
            return recs

        except (Exception, psycopg2.Error) as error :
            print ("Error en base de datos", error)
            return None
        
        finally:
            if(conn):
                dict_cur.close()
                conn.close() 

    def recuperar_mejor_grupo_micropilotes_b_nm(self, torres_excluir, grupos_excluir, porc_sobrecosto, corrida_integrada_id):
        try:
            conn = psycopg2.connect(self.conn_string)
            dict_cur: psycopg2.extras.DictCursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            sql = """
                with optimos as
                (
                    select distinct on (torre) ci.*
                    from {}.m_micropilotes_corrida_integrada_{} ci
                    where ci.cumple
                    order by torre, ci.calificacion
                ), pochos as
                (
                    select ci.grupo, ci.tipo, ci.resistencia_min_conc, ci.proc_iny, ci.barra_nombre, ci.n_m, ci.d_p, ci.l_b, ci.con_camisa, ci.b, ci.d_f, ci.s_m, count(*) as cobertura, 
                            array_agg(ci.torre) as torres_cubiertas, array_to_string(array_agg(ci.torre),',') as torres, sum(ci.calificacion[2] - op.calificacion[2]) as sobrecosto,
                            min(ci.h) as h_min, max(ci.h) as h_max, min(ci.tp) as tp_min, max(ci.tp) as tp_max
                    from {}.m_micropilotes_corrida_integrada_{} ci
                    join optimos op on ci.torre=op.torre
                    where ci.cumple
                    and not ci.torre = any(%s) 
                    and not ci.grupo = any(%s)
                    and abs((ci.calificacion[2] - op.calificacion[2])/op.calificacion[2]*100) <= %s -- Se restringe desviación en costo, no en B
                    group by ci.grupo,ci.tipo, ci.resistencia_min_conc, ci.proc_iny, ci.barra_nombre, ci.n_m, ci.d_p, ci.l_b, ci.con_camisa, ci.b, ci.d_f, ci.s_m
                )
                select *
                from pochos
                order by n_m, cobertura desc, sobrecosto
                limit 1
            """.format(self.esquema, corrida_integrada_id, self.esquema, corrida_integrada_id)
            dict_cur.execute(sql, (torres_excluir,grupos_excluir,porc_sobrecosto))
            recs = dict_cur.fetchone()
            return recs

        except (Exception, psycopg2.Error) as error :
            print ("Error en base de datos", error)
            return None
        
        finally:
            if(conn):
                dict_cur.close()
                conn.close() 

    def recuperar_mejor_grupo_micropilotes_c_cob_lc(self, torres_excluir, grupos_excluir, porc_sobrecosto, corrida_integrada_id):
        try:
            conn = psycopg2.connect(self.conn_string)
            dict_cur: psycopg2.extras.DictCursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            sql = """
                with optimos as
                (
                    select distinct on (torre) ci.*
                    from {}.m_micropilotes_corrida_integrada_{} ci
                    where ci.cumple
                    order by torre, ci.calificacion
                ), pochos as
                (
                    select ci.grupo, ci.tipo, ci.resistencia_min_conc, ci.proc_iny, ci.barra_nombre, ci.n_m, ci.d_p, ci.l_b, ci.con_camisa, ci.l_c, ci.b, ci.d_f, ci.s_m, count(*) as cobertura, 
                            array_agg(ci.torre) as torres_cubiertas, array_to_string(array_agg(ci.torre),',') as torres, sum(ci.calificacion[2] - op.calificacion[2]) as sobrecosto,
                            min(ci.h) as h_min, max(ci.h) as h_max, min(ci.tp) as tp_min, max(ci.tp) as tp_max
                    from {}.m_micropilotes_corrida_integrada_{} ci
                    join optimos op on ci.torre=op.torre
                    where ci.cumple
                    and not ci.torre = any(%s) 
                    and not ci.grupo = any(%s)
                    and abs((ci.calificacion[3] - op.calificacion[3])/op.calificacion[3]*100) <= %s -- Se restringe desviación en costo, no en B
                    group by ci.grupo,ci.tipo, ci.resistencia_min_conc, ci.proc_iny, ci.barra_nombre, ci.n_m, ci.d_p, ci.l_b, ci.con_camisa, ci.l_c, ci.b, ci.d_f, ci.s_m
                )
                select *
                from pochos
                order by cobertura desc, sobrecosto
                limit 1
            """.format(self.esquema, corrida_integrada_id, self.esquema, corrida_integrada_id)
            dict_cur.execute(sql, (torres_excluir,grupos_excluir,porc_sobrecosto))
            recs = dict_cur.fetchone()
            return recs

        except (Exception, psycopg2.Error) as error :
            print ("Error en base de datos", error)
            return None
        
        finally:
            if(conn):
                dict_cur.close()
                conn.close() 

    def listar_micropilote_en_grupo(self, conjunto):
        """       
        Arguments:
            ToDo
        
        Returns:
            List[DBFila] -- Lista de diccionarios
        """        
        try:
            conn = psycopg2.connect(self.conn_string)
            dict_cur: psycopg2.extras.DictCursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            sql = (r"""
                    select
                        id, 
                        grupo, 
                        tipo,
                        resistencia_min_conc,
                        proc_iny,
                        nombre_barra,
                        n_m,
                        d_p,
                        l_b,
                        b,
                        d_f,
                        s_m,
                        hs_grupos,
                        anc_grupos,
                        tps_grupos,
                        unnest(string_to_array(torres,',')) as torre
                    from {}.grupos_mp_finales g
                    where conjunto = %s
            """).format(self.esquema)
            dict_cur.execute(sql, (conjunto,))
            return dict_cur.fetchall()

        except (Exception, psycopg2.Error) as error :
            print ("Error en base de datos", error)
            raise error

        finally:
            if(conn):
                dict_cur.close()
                conn.close()        

    def listar_zapatas_en_grupo(self, conjunto):
        """       
        Arguments:
            ToDo
        
        Returns:
            List[DBFila] -- Lista de diccionarios
        """        
        try:
            conn = psycopg2.connect(self.conn_string)
            dict_cur: psycopg2.extras.DictCursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            sql = ("""
                    select id, conjunto, tipo, concreto, b, d, h_grupo, tp_grupo, hgs, unnest(string_to_array(torres,',')) as torre, hs_grupo, tps_grupo
                    from {}.t_zapata_grupo
                    where conjunto = %s
            """).format(self.esquema)
            dict_cur.execute(sql, (conjunto,))
            return dict_cur.fetchall()

        except (Exception, psycopg2.Error) as error :
            print ("Error en base de datos", error)
            raise error

        finally:
            if(conn):
                dict_cur.close()
                conn.close()        

    def listar_pilastras_en_grupo(self, conjunto):
        """       
        Arguments:
            ToDo
        
        Returns:
            List[DBFila] -- Lista de diccionarios
        """        
        try:
            conn = psycopg2.connect(self.conn_string)
            dict_cur: psycopg2.extras.DictCursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            sql = ("""
                    select id, conjunto, tipo, concreto, d_p, h_p, h_i, hgs, unnest(string_to_array(torres,',')) as torre
                    from {}.t_pilastra_grupo
                    where conjunto = %s
            """).format(self.esquema)
            dict_cur.execute(sql, (conjunto,))
            return dict_cur.fetchall()

        except (Exception, psycopg2.Error) as error :
            print ("Error en base de datos", error)
            raise error

        finally:
            if(conn):
                dict_cur.close()
                conn.close()        

    def guardar_mp_grupo(self, pocho, conjunto):
        try:
            conn = psycopg2.connect(self.conn_string)
            cur = conn.cursor()
            sql = """
                insert into {}.grupos_mp_finales(grupo, cantidad, torres, tipo, resistencia_min_conc, proc_iny, nombre_barra, n_m, d_p, l_b, b, d_f, conjunto, h_min, h_max, tp_min, tp_max, s_m, con_camisa)
                values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """.format(self.esquema)
            cur.execute(sql, (pocho["grupo"], pocho["cobertura"], pocho["torres"], pocho["tipo"], pocho["resistencia_min_conc"], pocho["proc_iny"], pocho["barra_nombre"], 
            pocho["n_m"], pocho["d_p"], pocho["l_b"], pocho["b"], pocho["d_f"], conjunto, pocho["h_min"], pocho["h_max"], pocho["tp_min"], pocho["tp_max"], pocho["s_m"], pocho["con_camisa"]))
        
        except (Exception, psycopg2.Error) as error :
            print ("Error en base de datos", error)
            return None
        
        finally:
            if(conn):
                cur.close()
                conn.commit()
                conn.close()

    def guardar_mp_grupo_lc(self, pocho, conjunto):
        try:
            conn = psycopg2.connect(self.conn_string)
            cur = conn.cursor()
            sql = """
                insert into {}.grupos_mp_finales(grupo, cantidad, torres, tipo, resistencia_min_conc, proc_iny, nombre_barra, n_m, d_p, l_b, b, d_f, conjunto, h_min, h_max, tp_min, tp_max, s_m, con_camisa, l_c)
                values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """.format(self.esquema)
            cur.execute(sql, (pocho["grupo"], pocho["cobertura"], pocho["torres"], pocho["tipo"], pocho["resistencia_min_conc"], pocho["proc_iny"], pocho["barra_nombre"], 
            pocho["n_m"], pocho["d_p"], pocho["l_b"], pocho["b"], pocho["d_f"], conjunto, pocho["h_min"], pocho["h_max"], pocho["tp_min"], pocho["tp_max"], pocho["s_m"], pocho["con_camisa"], pocho["l_c"]))
        
        except (Exception, psycopg2.Error) as error :
            print ("Error en base de datos", error)
            return None
        
        finally:
            if(conn):
                cur.close()
                conn.commit()
                conn.close()

    def guardar_memoria_calculo_zapata_qs(self, grupo, dato):
        try:
            conn = psycopg2.connect(self.conn_string)
            cur = conn.cursor()
            sql = """
                insert into {}.memoria_calculo_zapata_qs
                (grupo_id, tipo, concreto, b, d, torre, hg, caso_cargas, f_xc, f_yc, f_zc, q_max, q_min, memoria, h, tp, relleno)
                values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            """.format(self.esquema)
            json_memoria = json.dumps(dato["memoria"])
            json_relleno = json.dumps(dato["relleno"])
            cur.execute(sql, (grupo["id"],grupo["tipo"], grupo["concreto"], grupo["b"], grupo["d"], dato["torre"], 
                            dato["hg"], dato["caso_cargas"], dato["f_xc"], dato["f_yc"], dato["f_zc"], dato["q_max"],
                            dato["q_min"], json_memoria, grupo["h_grupo"], grupo["tp_grupo"], json_relleno))
            print()        

        except (Exception, psycopg2.Error) as error :
            print ("Error en base de datos", error)
            return None
        
        finally:
            if(conn):
                cur.close()
                conn.commit()
                conn.close()

    def listar_datos_parrillas(self, tipo):
        """       
        Arguments:
            ToDo
        
        Returns:
            List[DBFila] -- Lista de diccionarios
        """        
        try:
            conn = psycopg2.connect(self.conn_string)
            dict_cur: psycopg2.extras.DictCursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            sql = ("""
                    select vt.nombre as torre, dp.tipo as tipo_parrilla, dp.b, dp.d, dp.peso, dp.esf_act_ingedisa, dp.h, dp.tp, dp.mv_ingedisa
                    from cll_dlt_gtc.v_torre vt
                    join cll_dlt_gtc.diseno_parrilla dp on dp.tipo_torre=vt.tipo
                    where vt.recom_parrilla
                    and dp.tipo = %s
                    order by vt.abscisa            
            """).format(self.esquema)
            dict_cur.execute(sql, (tipo,))
            return dict_cur.fetchall()

        except (Exception, psycopg2.Error) as error :
            print ("Error en base de datos", error)
            raise error

        finally:
            if(conn):
                dict_cur.close()
                conn.close()        
