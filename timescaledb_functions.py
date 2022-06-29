from datetime import datetime
import psycopg2
from pgcopy import CopyManager
from configuration import * 

def print__message(conn):
    cursor = conn.cursor()
    # use the cursor to interact with your database
    cursor.execute("SELECT 'hello world'")
    print(cursor.fetchone())
    cursor.close()

def normal_insert(conn, table, columns, values):
    cursor = conn.cursor()
    conn.commit()
    str_col = ""
    for col in columns:
        str_col += col + ", "
    for val in values:
        str_val = ""
        for i in range(0, len(val)):
            str_val += "%s, "
        cursor.execute("INSERT INTO " + table + " (" + str_col[:-2] + ") VALUES (" + str_val[:-2] + ");", val)
    conn.commit()
    cursor.close()

def print_table_values(conn, table, funct, param):
    cursor = conn.cursor()
    if funct == 'first':
        cursor.execute("SELECT " + param[0] + ", first(" + param[1] + ", time) FROM " + table + " GROUP BY " + param[0] + ";")
    elif funct == 'last':
        cursor.execute("SELECT " + param[0] + ", last(" + param[1] + ", time) FROM " + table + " GROUP BY " + param[0] + ";")
    elif funct == 'all':
        cursor.execute("SELECT * FROM " + table + ";")
    elif funct == 'count':
        cursor.execute("ANALYZE " + table + "; SELECT * FROM approximate_row_count('" + table + "');")
    for row in cursor.fetchall():
        print(row)
    cursor.close()

# insert using pgcopy
def fast_insert(conn, table, columns, id_min, id_max):
    cursor = conn.cursor()
    for id in range(id_min, id_max):
        data = (id,)
        query = """SELECT generate_series(now() - interval '2 days', now(), interval '60 seconds') AS time,
                    %s as sensor_id, random()*100 AS temperature, random() AS cpu
                """
        cursor.execute(query, data)
        values = cursor.fetchall()
        # create copy manager with the target table and insert
        mgr = CopyManager(conn, table, columns)
        mgr.copy(values)
    conn.commit()
    cursor.close()

# query with placeholders
def select_query_placeholder(conn, query):
    cursor = conn.cursor()
    location = "floor"
    sensor_type = "a"
    data = (location, sensor_type)
    cursor.execute(query, data)
    results = cursor.fetchall()
    for row in results:
        print(row)

def alter_table(conn, table, funct, param):
    cursor = conn.cursor()
    if funct == 'add':
        cursor.execute("ALTER TABLE " + table + " ADD COLUMN " + param[0] + " " + param[1] + ";")
    elif funct == 'drop':
        cursor.execute("ALTER TABLE " + table + " DROP COLUMN " + param[0] + ";")
    conn.commit()
    cursor.close()

def update_row(conn, table, columns, values, search_id):
    cursor = conn.cursor()
    query = "UPDATE " + table + " SET "
    for col in columns:
        query += col + " = %s, "
    query = query[:-2] + " WHERE " + search_id + ' = %s;'
    print(query)
    cursor.execute(query, values)
    conn.commit()
    cursor.close()
    
def delete_row(conn, table, col, val):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM " + table + " WHERE " + col + " = %s;", val)
    conn.commit()
    cursor.close()  
    
def get_last_timestamp(conn, table, param, value):
    cursor = conn.cursor()
    cursor.execute("SELECT last(time, time) FROM " + table + " WHERE " + param + " = %s;", (value,))
    results = cursor.fetchall()
    cursor.close()
    return results[0]

def update_last_element(conn, table, columns, values, param):
    last_timestamp = get_last_timestamp(conn, table, param, values[1])
    #print(param[1])
    cursor = conn.cursor()
    query = "UPDATE " + table + " SET "
    for col in columns:
        query += col + " = %s, "
    query = query[:-2] + " WHERE time = %s AND " + param + ' = %s;'
    print(query)
    cursor.execute(query, (values[0], last_timestamp, values[1]))
    conn.commit()
    cursor.close()

def executeQuery(conn, query):
    cursor = conn.cursor()
    #query = "CALL refresh_continuous_aggregate('temperature_summary_hourly', NULL, localtimestamp - INTERVAL '1 day');"
    #query = """SELECT add_continuous_aggregate_policy('temperature_summary_view2',
                  #start_offset => INTERVAL '1 week',
                  #end_offset   => INTERVAL '1 hour',
                  #schedule_interval => INTERVAL '30 minutes');"""
    
    cursor.execute(query)
    #results = cursor.fetchall()
    #for row in results:
        #print(row)
    conn.commit()
    cursor.close()

