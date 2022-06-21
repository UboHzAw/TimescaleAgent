from datetime import datetime
import psycopg2
from pgcopy import CopyManager
from configuration import * 

def make_hystogram(conn, table, col, search_id, min_val, max_val, n_bukets):
    cursor = conn.cursor()
    data = (min_val, max_val, n_bukets)
    cursor.execute("SELECT " + search_id + ", histogram(" + col + ", %s, %s, %s) FROM " + table + " GROUP BY " + search_id + ";", data)
    for row in cursor.fetchall():
        print(row)
    cursor.close()

def create_time_bucket(conn, table, interval):
    cursor = conn.cursor()
    cursor.execute("SELECT time_bucket('" + interval + "', time) AS five_min, avg(cpu) FROM " + table + " GROUP BY five_min ORDER BY five_min DESC LIMIT 10;")
    conn.commit()
    for row in cursor.fetchall():
        print(row)
    cursor.close()
    
def create_continuous_aggregation(conn, table, interval, select_param, metric_param, view_name):
    # interval definisce la dimensione del time_bucket
    # WITH NO DATA genera una view inizialmente vuota per non appesantirla con i dati storici
    # per aggregare anche quelli è necessario eseguire un refresh della view
    cursor = conn.cursor()
    cursor.execute("""CREATE MATERIALIZED VIEW """ + view_name + """
                        WITH (timescaledb.continuous) AS
                        SELECT """ + select_param + """,
                               time_bucket(INTERVAL '""" + interval + """', time) AS bucket,
                               AVG(""" + metric_param + """),
                               MAX(""" + metric_param + """),
                               MIN(""" + metric_param + """)
                        FROM """ + table + """
                        GROUP BY """ + select_param + """, bucket
                        WITH NO DATA;""")
    conn.commit()
    cursor.close()
    
def refresh_view(conn, table, start_date, end_date):
    # start_date definisce l'inizio dell'intervallo su cui fare il refresh della view
    # end_date definisce la fine dell'intervallo su cui fare il refresh della view
    cursor = conn.cursor()
    query = "CALL refresh_continuous_aggregate('" + table + "', '" + start_date + "', '" + end_date + "');"
    print(query)
    cursor.execute(query)
    conn.commit()
    cursor.close()  

def add_policy(conn, table, start_offset, end_offset, schedule_interval):
    # start_offset definisce la dimensione della view. impostando un mese si ha sempre una view dell'ultimo mese - end_offset
    # end_offset è solitamente pari alla dimensione del time_bucket
    # schedule_interval indica l'intervallo di tempo che intercorre tra ogni refresh della view
    cursor = conn.cursor()
    cursor.execute("""SELECT add_continuous_aggregate_policy('""" + table + """',
                  start_offset => INTERVAL '""" + start_offset + """',
                  end_offset   => INTERVAL '""" + end_offset + """',
                  schedule_interval => INTERVAL '""" + schedule_interval + """');""")
    conn.commit()
    cursor.close()  

