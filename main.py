from datetime import datetime
import psycopg2
from pgcopy import CopyManager
from configuration import *
from timescaledb_functions import *
from view_functions import *
import json
import glob
import pandas as pd
import numpy as np
from psycopg2.extensions import register_adapter, AsIs
import math

psycopg2.extensions.register_adapter(np.int64, AsIs)
psycopg2.extensions.register_adapter(np.bool_, AsIs)

directory = "new Lonati Giugno/"
files = glob.glob(directory + "*.csv")

if __name__ == '__main__':
    # eseguo la connessione e creo un cursore
    conn = psycopg2.connect(CONNECTION)

    inizio = datetime.now()
    # executeQuery(conn, "DROP MATERIALIZED VIEW sensor_data_small_view_temperature_hour")
    # executeQuery(conn, "DELETE FROM stops")
    # executeQuery(conn, "ALTER TABLE electrovalve_values DROP CONSTRAINT electrovalve_values_pkey;")
    # executeQuery(conn,  "ALTER TABLE electrovalve_values ADD PRIMARY KEY (time, machine_code, electrovalve_id);")
    # executeQuery(conn, "ALTER TABLE motors_values ALTER COLUMN i2t TYPE BIGINT;")
    # executeQuery(conn, query_drop)
    # executeQuery(conn, query_db_diag)
    # executeQuery(conn, "ALTER TABLE tamburini_values ALTER COLUMN count TYPE VARCHAR;")
    # executeQuery(conn, query_create_sensordata_hypertable)
    # create_continuous_aggregation(conn, 'sensor_data_small', '1 hour', 'sensor_id', 'temperature', 'sensor_data_small_view_temperature_hour')
    # add_policy(conn, 'sensor_data_small_view_temperature_hour', '1 day', '1 hour', '1 hour')
    # fast_insert(conn, 'sensor_data_small', ['time', 'sensor_id', 'temperature', 'cpu'], 1, 8)
    # print_table_values(conn, 'programs', 'count', ['program_name'])
    # update_last_element(conn, 'sensor_data_2', ['cpu'], (0.9999, 5), 'sensor_id')
    # refresh_view(conn, 'temperature_summary_view2', '2022-06-10', '2022-06-22')

    # normal_insert(conn, 'sensors', ['type', 'location'], [('d', 'floor'), ('d', 'ceiling')])
    # normal_insert(conn, 'sensor_data', ['time', 'sensor_id', 'temperature', 'cpu'], [(datetime.now(), 5, 72, 0.15)])

    # alter_table(conn, 'sensors', 'drop', ['prova', 'INTEGER'])

    # update_row(conn, 'sensors', ['type', 'location'], ('c', 'ceiling', 1), 'id')
    # delete_row(conn, 'sensors', 'id', (8,))

    # make_hystogram(conn, 'sensor_data', 'temperature', 'sensor_id', 0, 100, 5)
    # create_time_bucket(conn, 'sensor_data', '10 minutes')

    for file in files:
        fileReader = open(file, 'r', encoding='utf-8')
        print("Elaboro: " + file)
        for line in fileReader.readlines():

            if """ "INFO",""" in line:
                data = json.loads(line[21:])
                df_nested_list = pd.json_normalize(
                    data,
                    record_path=['events'],
                    meta=['timestamp', 'machine_id']
                )
                try:
                    values = (str(df_nested_list['machine_id'][0]), str(df_nested_list['model'][0]),
                                   str(df_nested_list['family'][0]), df_nested_list['needles'][0], df_nested_list['diameter'][0],
                                   str(df_nested_list['eth_address'][0]), str(df_nested_list['wlan_address'][0]),
                                   str(df_nested_list['eth_ip_address'][0]), str(df_nested_list['wlan_ip_address'][0]))
                    normal_insert(conn, 'machine_devices', ['machine_code', 'model', 'family', 'needles', 'diameter',
                                                                'eth_address', 'wlan_address', 'eth_ip_address', 'wlan_ip_address'], [values])
                    print("Macchina " + str(df_nested_list['machine_id'][0]) + " inserita correttamente in machine_devices")
                except Exception as e:
                    print(e)

            if "PROGRAM" in line:
                data = json.loads(line[21:])
                df_nested_list = pd.json_normalize(
                    data,
                    record_path=['events', 'programs'],
                    meta=['timestamp', 'machine_id']
                )
                try:
                    values = (str(df_nested_list['program'][0]))
                    normal_insert(conn, 'programs', ['program_name'], [(values,)])
                    print("Programma " + str(df_nested_list['program'][0]) + " inserito correttamente in programs")
                except Exception as e:
                    print(e)
                try:
                    values = (df_nested_list['timestamp'][0], str(df_nested_list['machine_id'][0]), str(df_nested_list['program'][0]))
                    normal_insert(conn, 'machine_status', ['time', 'machine_code', 'program_name'], [values])
                except Exception as e:
                    print(e)

            if "STOP" in line:
                data = json.loads(line[21:])
                df_nested_list = pd.json_normalize(
                    data,
                    record_path=['events'],
                    meta=['timestamp', 'machine_id']
                )
                try:
                    message_code = str(df_nested_list['type'][0]) + '_' + str(df_nested_list['code'][0]) + '_' + str(df_nested_list['offset'][0])
                    values = (message_code, df_nested_list['type'][0], df_nested_list['code'][0],
                              df_nested_list['offset'][0], df_nested_list['level'][0], df_nested_list['family'][0],
                              df_nested_list['stop_mac'][0], df_nested_list['stop_cte'][0], str(df_nested_list['msg_base'][0]))
                    normal_insert(conn, 'stops', ['message_code', 'type', 'code', 'offset_stop', 'level_stop', 'family', 'stopMac', 'stopCte', 'message_base'], [values])
                    print("Stop " + str(df_nested_list['message_code'][0]) + " inserito correttamente in stops")
                except Exception as e:
                    print(e)
                try:
                    message_code = str(df_nested_list['type'][0]) + '_' + str(df_nested_list['code'][0]) + '_' + str(df_nested_list['offset'][0])
                    values = (df_nested_list['timestamp'][0], df_nested_list['machine_id'][0], message_code,
                              df_nested_list['degree'][0], df_nested_list['course'][0], df_nested_list['step'][0],
                              df_nested_list['phase'][0], df_nested_list['revision'][0])
                    normal_insert(conn, 'machine_status', ['time', 'machine_code', 'message_code', 'degree', 'course', 'step', 'phase', 'revision'], [values])
                except Exception as e:
                    print(e)

            if "POWERON" in line:
                data = json.loads(line[21:])
                df_nested_list = pd.json_normalize(
                    data,
                    record_path=['events'],
                    meta=['timestamp', 'machine_id']
                )
                try:
                    values_off = (df_nested_list['power_off'][0], df_nested_list['machine_id'][0], False)
                    values_on = (df_nested_list['power_on'][0], df_nested_list['machine_id'][0], True)
                    normal_insert(conn, 'machine_status', ['time', 'machine_code', 'power_machine'], [values_off])
                    normal_insert(conn, 'machine_status', ['time', 'machine_code', 'power_machine'], [values_on])
                except Exception as e:
                    print(e)

            if "COUNTERS" in line:
                data = json.loads(line[21:])
                df_nested_list = pd.json_normalize(
                    data,
                    record_path=['events'],
                    meta=['timestamp', 'machine_id']
                )
                try:
                    program_index = df_nested_list['program_index'][0] if 'program_index' in df_nested_list.columns else -1
                    pieces = df_nested_list['pieces'][0] if 'pieces' in df_nested_list.columns else -1
                    order_pieces = df_nested_list['order_pieces'][0] if 'order_pieces' in df_nested_list.columns else -1
                    order_target = df_nested_list['order_target'][0] if 'order_target' in df_nested_list.columns else -1
                    bag_pieces = df_nested_list['bag_pieces'][0] if 'bag_pieces' in df_nested_list.columns else -1
                    bag_target = df_nested_list['bag_target'][0] if 'bag_target' in df_nested_list.columns else -1
                    cycle_time = df_nested_list['cycle_time'][0] if 'cycle_time' in df_nested_list.columns else -1
                    values = (df_nested_list['timestamp'][0], df_nested_list['machine_id'][0], df_nested_list['sub_code'][0],
                              df_nested_list['reason'][0], program_index, pieces, order_pieces, order_target,
                              bag_pieces, bag_target, cycle_time)
                    normal_insert(conn, 'machine_status', ['time', 'machine_code', 'sub_code', 'reason', 'program_index',
                                                           'pieces', 'order_pieces', 'order_target', 'bag_pieces', 'bag_target', 'cycle_time'], [values])
                except Exception as e:
                    print(e)

            if "STATUS" in line:
                data = json.loads(line[21:])
                df_nested_list = pd.json_normalize(
                    data,
                    record_path=['events'],
                    meta=['timestamp', 'machine_id']
                )
                try:
                    key_reset = df_nested_list['key_reset'][0] if 'key_reset' in df_nested_list.columns else False
                    key_chain_stop = df_nested_list['key_chain_stop'][0] if 'key_chain_stop' in df_nested_list.columns else False
                    key_econ_stop = df_nested_list['key_econ_stop'][0] if 'key_econ_stop' in df_nested_list.columns else False
                    key_stop_end_cycle = df_nested_list['key_stop_end_cycle'][0] if 'key_stop_end_cycle' in df_nested_list.columns else False
                    key_prg_stop = df_nested_list['key_prg_stop'][0] if 'key_prg_stop' in df_nested_list.columns else False
                    key_low_speed = df_nested_list['key_low_speed'][0] if 'key_low_speed' in df_nested_list.columns else False
                    key_middle_speed = df_nested_list['key_middle_speed'][0] if 'key_middle_speed' in df_nested_list.columns else False
                    running = df_nested_list['running'][0] if 'running' in df_nested_list.columns else False
                    mechanical_reset = df_nested_list['mechanical_reset'][0] if 'mechanical_reset' in df_nested_list.columns else False
                    resetting = df_nested_list['resetting'][0] if 'resetting' in df_nested_list.columns else False
                    next_bag = df_nested_list['next_bag'][0] if 'next_bag' in df_nested_list.columns else False
                    queue_full = df_nested_list['queue_full'][0] if 'queue_full' in df_nested_list.columns else False
                    limits = df_nested_list['limits'][0] if 'limits' in df_nested_list.columns else -1
                    manual_stop = df_nested_list['manual_stop'][0] if 'manual_stop' in df_nested_list.columns else -1
                    values = (df_nested_list['timestamp'][0], df_nested_list['machine_id'][0], key_reset, key_chain_stop,
                              key_econ_stop, key_stop_end_cycle, key_prg_stop, key_low_speed, key_middle_speed,
                              running, mechanical_reset, resetting, next_bag, queue_full, limits, manual_stop)
                    normal_insert(conn, 'machine_status', ['time', 'machine_code', 'key_reset', 'key_chain_stop', 'key_econ_stop',
                                                           'key_stop_end_cycle', 'key_prg_stop', 'key_low_speed', 'key_middle_speed',
                                                           'running', 'mechanical_reset', 'resetting', 'next_bag',
                                                           'queue_full', 'limits', 'manual_stop'], [values])
                except Exception as e:
                    print(e)

            if "INFO_MPP" in line:
                data = json.loads(line[21:])
                df_nested_list = pd.json_normalize(
                    data,
                    record_path=['messages', 'actuators'],
                    meta=['timestamp', 'machine_id']
                )
                try:
                    for row in df_nested_list.iterrows():
                        id = row[1]['id']
                        name = row[1]['info.name']
                        logic_trac = row[1]['info.logic_trac']
                        values = (id, name, logic_trac)
                        normal_insert(conn, 'motors_info', ['motors_id', 'name', 'logic_trac'], [values])
                        print("MPP " + str(id) + " inserito con successo")
                except Exception as e:
                    print(e)
            if "DIAG_MPP" in line:
                data = json.loads(line[21:])
                df_nested_list = pd.json_normalize(
                    data,
                    record_path=['messages', 'actuators'],
                    meta=['timestamp', 'machine_id']
                )
                # TODO: da verificare il corretto funzionamento
                df_nested_list = df_nested_list.groupby(['timestamp', 'machine_id', 'id']).max().reset_index()
                try:
                    for row in df_nested_list.iterrows():
                        # TODO: aggiungere la selezione del logic_trac
                        motor_id = row[1]['id']
                        timestamp = row[1]['timestamp']
                        machine_id = row[1]['machine_id']
                        steps = row[1]['value.stepsPullOver'] if 'stepsPullOver' in str(row[1]) else -1111
                        i2t = row[1]['value.I2T'] if 'I2T' in str(row[1]) and math.isnan(row[1]['value.I2T']) == False else -1
                        round = row[1]['value.round'] if 'round' in str(row[1]) else -1
                        time_move = row[1]['value.timeMove'] if 'timeMove' in str(row[1]) else -1
                        if i2t != -1:
                            values = (motor_id, timestamp, machine_id, i2t, time_move)
                            normal_insert(conn, 'motors_values', ['motors_id', 'time', 'machine_code', 'I2T', 'timeMove'], [values])
                        elif steps != -1111:
                            values = (motor_id, timestamp, machine_id, steps)
                            normal_insert(conn, 'motors_values', ['motors_id', 'time', 'machine_code', 'stepsPullOver'], [values])
                        else:
                            values = (motor_id, timestamp, machine_id, round)
                            normal_insert(conn, 'motors_values', ['motors_id', 'time', 'machine_code', 'round'], [values])
                except Exception as e:
                    print(e)

            if "INFO_AZ" in line:
                data = json.loads(line[21:])
                df_nested_list = pd.json_normalize(
                    data,
                    record_path=['messages', 'actuators'],
                    meta=['timestamp', 'machine_id']
                )
                try:
                    for row in df_nested_list.iterrows():
                        id = row[1]['id']
                        name = row[1]['info.name']
                        values = (id, name)
                        normal_insert(conn, 'azionamenti_info', ['azionamenti_id', 'name'], [values])
                        print("Azionamento " + str(id) + " inserito con successo")
                except Exception as e:
                    print(e)
            if "DIAG_AZ" in line:
                data = json.loads(line[21:])
                df_nested_list = pd.json_normalize(
                    data,
                    record_path=['messages', 'actuators'],
                    meta=['timestamp', 'machine_id']
                )
                # TODO: da verificare il corretto funzionamento
                df_nested_list = df_nested_list.groupby(['timestamp', 'machine_id', 'id']).max().reset_index()
                try:
                    for row in df_nested_list.iterrows():
                        azionamenti_id = row[1]['id']
                        timestamp = row[1]['timestamp']
                        machine_id = row[1]['machine_id']
                        power = row[1]['value.power']
                        values = (azionamenti_id, timestamp, machine_id, power)
                        normal_insert(conn, 'azionamenti_values', ['azionamenti_id', 'time', 'machine_code', 'power'], [values])
                except Exception as e:
                    print(e)

            if "INFO_GRYF" in line:
                data = json.loads(line[21:])
                df_nested_list = pd.json_normalize(
                    data,
                    record_path=['messages', 'actuators'],
                    meta=['timestamp', 'machine_id']
                )
                try:
                    for row in df_nested_list.iterrows():
                        id = row[1]['id']
                        name = row[1]['info.name']
                        values = (id, name)
                        normal_insert(conn, 'thread_power_supply_info', ['thread_power_supply_id', 'name'], [values])
                        print("GRYF " + str(id) + " inserito con successo")
                except Exception as e:
                    print(e)
            if "DIAG_GRYF" in line:
                data = json.loads(line[21:])
                df_nested_list = pd.json_normalize(
                    data,
                    record_path=['messages', 'actuators'],
                    meta=['timestamp', 'machine_id']
                )
                # TODO: da verificare il corretto funzionamento
                df_nested_list = df_nested_list.groupby(['timestamp', 'machine_id', 'id']).max().reset_index()
                try:
                    for row in df_nested_list.iterrows():
                        thread_power_supply_id = row[1]['id']
                        timestamp = row[1]['timestamp']
                        machine_id = row[1]['machine_id']
                        load = row[1]['value.load'] if 'load' in str(row[1]) and math.isnan(row[1]['value.load']) == False else 0
                        consumption = row[1]['value.consumption'] if 'consumption' in str(row[1]) and math.isnan(row[1]['value.consumption']) == False else 0
                        values = (thread_power_supply_id, timestamp, machine_id, load, consumption)
                        normal_insert(conn, 'thread_power_supply_values', ['thread_power_supply_id', 'time', 'machine_code', 'load', 'consumption'], [values])
                        print("-.-.-.-.-.-.-.-.-.-")
                except Exception as e:
                    print(e)

            if "INFO_TAMB" in line:
                data = json.loads(line[21:])
                df_nested_list = pd.json_normalize(
                    data,
                    record_path=['messages', 'actuators'],
                    meta=['timestamp', 'machine_id']
                )
                try:
                    for row in df_nested_list.iterrows():
                        id = row[1]['id']
                        name = row[1]['info.name']
                        levels = row[1]['info.levels'] if 'levels' in str(row[1]) and math.isnan(row[1]['info.levels']) == False else 0
                        values = (id, name, levels)
                        normal_insert(conn, 'tamburini_info', ['tamburini_id', 'name', 'levels'], [values])
                        print("tamburino " + str(id) + " inserito con successo")
                except Exception as e:
                    print(e)
            if "DIAG_TAMB" in line:
                data = json.loads(line[21:])
                df_nested_list = pd.json_normalize(
                    data,
                    record_path=['messages', 'actuators'],
                    meta=['timestamp', 'machine_id']
                )
                # TODO: da verificare il corretto funzionamento
                df_nested_list = df_nested_list.groupby(['timestamp', 'machine_id', 'id']).max().reset_index()
                for row in df_nested_list.iterrows():
                    try:
                        tamburini_id = row[1]['id']
                        timestamp = row[1]['timestamp']
                        machine_id = row[1]['machine_id']
                        count = row[1]['value.count'] if 'count' in str(row[1]) else ""
                        values = (tamburini_id, timestamp, machine_id, count)
                        normal_insert(conn, 'tamburini_values', ['tamburini_id', 'time', 'machine_code', 'count'], [values])
                    except Exception as e:
                        print(e)

            if "INFO_EV" in line:
                data = json.loads(line[21:])
                df_nested_list = pd.json_normalize(
                    data,
                    record_path=['messages', 'actuators'],
                    meta=['timestamp', 'machine_id']
                )
                for row in df_nested_list.iterrows():
                    try:
                        id = row[1]['id']
                        name = row[1]['info.name']
                        max_shot = row[1]['info.max_shot'] if 'max_shot' in str(row[1]) and math.isnan(
                            row[1]['info.max_shot']) == False else -1
                        values = (id, name, max_shot)
                        normal_insert(conn, 'electrovalve_info', ['electrovalve_id', 'name', 'max_shot'], [values])
                        print("elettrovalvola " + str(id) + " inserita con successo")
                    except Exception as e:
                        print(e)
            if "DIAG_EV" in line:
                data = json.loads(line[21:])
                df_nested_list = pd.json_normalize(
                    data,
                    record_path=['messages', 'actuators'],
                    meta=['timestamp', 'machine_id']
                )
                # TODO: da verificare il corretto funzionamento
                df_nested_list = df_nested_list.groupby(['timestamp', 'machine_id', 'id']).max().reset_index()
                for row in df_nested_list.iterrows():
                    try:
                        tamburini_id = row[1]['id']
                        timestamp = row[1]['timestamp']
                        machine_id = row[1]['machine_id']
                        count = row[1]['value.count'] if 'count' in str(row[1]) else ""
                        values = (tamburini_id, timestamp, machine_id, count)
                        normal_insert(conn, 'electrovalve_values', ['electrovalve_id', 'time', 'machine_code', 'count'],
                                      [values])
                    except Exception as e:
                        print(e)
        fileReader.close()

    fine = datetime.now()
    tempo_INSERT = fine - inizio
    print("L'operazione ha richiesto " + str(tempo_INSERT) + " secondi")

