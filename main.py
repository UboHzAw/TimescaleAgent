from datetime import datetime
import psycopg2
from pgcopy import CopyManager
from configuration import *
from timescaledb_functions import *
from view_functions import *

if __name__ == '__main__':
    # eseguo la connessione e creo un cursore
    conn = psycopg2.connect(CONNECTION)

    inizio = datetime.now()
    # executeQuery(conn, "DROP MATERIALIZED VIEW sensor_data_small_view_temperature_hour")
    # executeQuery(conn, query_drop)
    # executeQuery(conn, query_create_sensordata_small_table)
    # executeQuery(conn, query_create_sensordata_hypertable)
    # create_continuous_aggregation(conn, 'sensor_data_small', '1 hour', 'sensor_id', 'temperature', 'sensor_data_small_view_temperature_hour')
    # add_policy(conn, 'sensor_data_small_view_temperature_hour', '1 day', '1 hour', '1 hour')
    # fast_insert(conn, 'sensor_data_small', ['time', 'sensor_id', 'temperature', 'cpu'], 1, 8)
    print_table_values(conn, 'sensor_data_small', 'count', ['sensor_id', 'cpu'])
    # update_last_element(conn, 'sensor_data_2', ['cpu'], (0.9999, 5), 'sensor_id')
    # refresh_view(conn, 'temperature_summary_view2', '2022-06-10', '2022-06-22')

    # normal_insert(conn, 'sensors', ['type', 'location'], [('d', 'floor'), ('d', 'ceiling')])
    # normal_insert(conn, 'sensor_data', ['time', 'sensor_id', 'temperature', 'cpu'], [(datetime.now(), 5, 72, 0.15)])

    # alter_table(conn, 'sensors', 'drop', ['prova', 'INTEGER'])

    # update_row(conn, 'sensors', ['type', 'location'], ('c', 'ceiling', 1), 'id')
    # delete_row(conn, 'sensors', 'id', (8,))

    # make_hystogram(conn, 'sensor_data', 'temperature', 'sensor_id', 0, 100, 5)
    # create_time_bucket(conn, 'sensor_data', '10 minutes')

    fine = datetime.now()
    tempo_INSERT = fine - inizio
    print("L'operazione ha richiesto " + str(tempo_INSERT) + " secondi")

