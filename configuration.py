# CONNECTION = "postgres://username:password@host:port/dbname"
CONNECTION = "postgres://postgres:Dinema22.@localhost:5432/arcadiainterloop"

# Query Tabelle Arcadia
query_create_stops_table = "CREATE TABLE stops (id SERIAL PRIMARY KEY, stopCode INTEGER, description VARCHAR(100));"

# Query di prova
query_create_sensors_table = "CREATE TABLE sensors (id SERIAL PRIMARY KEY, type VARCHAR(50), location VARCHAR(50));"
query_create_sensordata_table = """CREATE TABLE sensor_data (
                                           time TIMESTAMPTZ NOT NULL,
                                           sensor_id INTEGER,
                                           temperature DOUBLE PRECISION,
                                           cpu DOUBLE PRECISION,
                                           FOREIGN KEY (sensor_id) REFERENCES sensors (id)
                                           );"""
query_create_sensordata2_table = """CREATE TABLE sensor_data_2 (
                                           time TIMESTAMPTZ NOT NULL,
                                           sensor_id INTEGER,
                                           temperature DOUBLE PRECISION,
                                           cpu DOUBLE PRECISION,
                                           FOREIGN KEY (sensor_id) REFERENCES sensors (id)
                                           );"""
query_create_sensordata_small_table = """CREATE TABLE sensor_data_small (
                                           time TIMESTAMPTZ NOT NULL,
                                           sensor_id INTEGER,
                                           temperature DOUBLE PRECISION,
                                           cpu DOUBLE PRECISION,
                                           FOREIGN KEY (sensor_id) REFERENCES sensors (id)
                                           );"""
query_create_sensordata_hypertable = "SELECT create_hypertable('sensor_data_small', 'time');"
query_index = "CREATE UNIQUE INDEX idx_sensor_id_time ON sensor_data(sensor_id, time);"
query_create_partitoned_hypertable = """SELECT * FROM create_hypertable(
                                          'sensor_data_2',
                                          'time',
                                          partitioning_column => 'sensor_id',
                                          number_partitions => 3
                                        );"""
query_placeholder = """SELECT time_bucket('5 minutes', time) AS five_min, avg(cpu)
               FROM sensor_data
               JOIN sensors ON sensors.id = sensor_data.sensor_id
               WHERE sensors.location = %s AND sensors.type = %s
               GROUP BY five_min
               ORDER BY five_min DESC;
               """
query_drop = "DROP TABLE sensor_data_small"
query_select = """SELECT * FROM sensor_data_2 WHERE time > '2022-04-09 11:00:00'"""

# Definizione oggetti di prova
sensors = [('a', 'floor'), ('a', 'ceiling'), ('b', 'floor'), ('b', 'ceiling')]
stops = [(123, 'stop 1 '), (456, 'stop 2 '), (789, 'stop 3 '), (0, 'stop 4 ')]

query_create_schema = """CREATE TABLE stops_registry (
      message_code VARCHAR PRIMARY KEY, 
      type INTEGER NOT NULL,
      code INTEGER NOT NULL,
      offset_stop INTEGER NOT NULL,
      level_stop INTEGER NOT NULL,
      family INTEGER NOT NULL,
      stopMac BOOLEAN NOT NULL,
      stopCte BOOLEAN NOT NULL,
      message_ita TEXT NOT NULL,
      message_eng TEXT NOT NULL,
      message_loc TEXT NOT NULL,
      answers_ita TEXT[],
      answers_eng TEXT[],
      answers_loc TEXT[]
);

CREATE TABLE stops (
    stop_id INTEGER PRIMARY KEY,
    stop_code INTEGER,
    degree INTEGER NOT NULL,
    course INTEGER NOT NULL,
    step INTEGER NOT NULL,
    phase TEXT NOT NULL,
    revision TEXT NOT NULL,
    args TEXT[] NOT NULL,
    FOREIGN KEY (stop_code) REFERENCES stops_registry (message_code)
);

CREATE TABLE tamburini_info (
    tamburini_id VARCHAR PRIMARY KEY,
    machine_code VARCHAR NOT NULL,
    name TEXT NOT NULL,
    levels INTEGER NOT NULL,
    FOREIGN KEY (machine_code) REFERENCES machine_devices (machine_code)
);

CREATE TABLE tamburini_values (
    time TIMESTAMPTZ PRIMARY KEY,
    tamburini_id VARCHAR NOT NULL,
    count INTEGER NOT NULL,
    counter INTEGER NOT NULL,
    FOREIGN KEY (tamburini_id) REFERENCES tamburini_info (tamburini_id)
);
SELECT create_hypertable('tamburini_values', 'time');

CREATE TABLE electrovalve_info (
    electrovalve_id VARCHAR PRIMARY KEY,
    machine_code VARCHAR NOT NULL,
    name TEXT NOT NULL,
    max_shot INTEGER NOT NULL,
    FOREIGN KEY (machine_code) REFERENCES machine_devices (machine_code)
);

CREATE TABLE electrovalve_values (
    time TIMESTAMPTZ PRIMARY KEY,
    electrovalve_id VARCHAR NOT NULL,
    count INTEGER[] NOT NULL,
    counter INTEGER NOT NULL,
    FOREIGN KEY (electrovalve_id) REFERENCES electrovalve_info (electrovalve_id)
);
SELECT create_hypertable('electrovalve_values', 'time');

CREATE TABLE oc_motors_info (
    oc_motors_id VARCHAR PRIMARY KEY,
    machine_code VARCHAR NOT NULL,
    name TEXT NOT NULL,
    logic_trac INTEGER NOT NULL,
    FOREIGN KEY (machine_code) REFERENCES machine_devices (machine_code)
);

CREATE TABLE oc_motors_values (
    time TIMESTAMPTZ PRIMARY KEY,
    oc_motors_id VARCHAR NOT NULL,
    steps INTEGER NOT NULL,
    counter INTEGER NOT NULL,
    FOREIGN KEY (oc_motors_id) REFERENCES oc_motors_info (oc_motors_id)
);
SELECT create_hypertable('oc_motors_values', 'time');

CREATE TABLE cc_motors_info (
    cc_motors_id VARCHAR PRIMARY KEY,
    machine_code VARCHAR NOT NULL,
    name TEXT NOT NULL,
    logic_trac INTEGER NOT NULL,
    FOREIGN KEY (machine_code) REFERENCES machine_devices (machine_code)
);

CREATE TABLE cc_motors_values (
    time TIMESTAMPTZ PRIMARY KEY,
    cc_motors_id VARCHAR NOT NULL,
    power INTEGER NOT NULL,
    counter INTEGER NOT NULL,
    FOREIGN KEY (cc_motors_id) REFERENCES oc_motors_info (cc_motors_id)
);
SELECT create_hypertable('cc_motors_values', 'time');

CREATE TABLE azionamenti_info (
    azionamenti_id VARCHAR PRIMARY KEY,
    machine_code VARCHAR NOT NULL,
    name TEXT NOT NULL,
    FOREIGN KEY (machine_code) REFERENCES machine_devices (machine_code)
);

CREATE TABLE azionamenti_values (
    time TIMESTAMPTZ PRIMARY KEY,
    azionamenti_id VARCHAR NOT NULL,
    power INTEGER NOT NULL,
    counter INTEGER NOT NULL,
    FOREIGN KEY (azionamenti_id) REFERENCES azionamenti_info (azionamenti_id)
);
SELECT create_hypertable('azionamenti_values', 'time');

CREATE TABLE thread_power_supply_info (
    thread_power_supply_id VARCHAR PRIMARY KEY,
    machine_code VARCHAR NOT NULL,
    name TEXT NOT NULL,
    FOREIGN KEY (machine_code) REFERENCES machine_devices (machine_code)
);

CREATE TABLE thread_power_supply_values (
    time TIMESTAMPTZ PRIMARY KEY,
    thread_power_supply_id VARCHAR NOT NULL,
    consumption INTEGER NOT NULL,
    load INTEGER NOT NULL,
    counter INTEGER NOT NULL,
    FOREIGN KEY (thread_power_supply_id) REFERENCES thread_power_supply_info (thread_power_supply_id)
);
SELECT create_hypertable('thread_power_supply_values', 'time');

CREATE TABLE ps_power_supply_info (
    ps_power_supply_id VARCHAR PRIMARY KEY,
    machine_code VARCHAR NOT NULL,
    name TEXT NOT NULL,
    FOREIGN KEY (machine_code) REFERENCES machine_devices (machine_code)
);

CREATE TABLE ps_power_supply_values (
    time TIMESTAMPTZ PRIMARY KEY,
    ps_power_supply_id VARCHAR NOT NULL,
    power INTEGER NOT NULL,
    counter INTEGER NOT NULL,
    FOREIGN KEY (ps_power_supply_id) REFERENCES ps_power_supply_info (ps_power_supply_id)
);
SELECT create_hypertable('ps_power_supply_values', 'time');

CREATE TABLE article_values (
    time TIMESTAMPTZ PRIMARY KEY,
    machine_code VARCHAR NOT NULL,
    temperature FLOAT,
    oil FLOAT,
    pression FLOAT,
    counter INTEGER NOT NULL,
    FOREIGN KEY (machine_code) REFERENCES machine_devices (machine_code)
);
SELECT create_hypertable('article_values', 'time');

CREATE TABLE machine_devices (
    machine_code VARCHAR PRIMARY KEY,
    model VARCHAR NOT NULL
);

CREATE TABLE machine_parts (
    time TIMESTAMPTZ PRIMARY KEY,
    device_id VARCHAR NOT NULL,
    machine_code VARCHAR NOT NULL,
    description TEXT,
    tipology TEXT,
    intervenction TEXT,
    FOREIGN KEY (machine_code) REFERENCES machine_devices (machine_code)
);
SELECT create_hypertable('machine_parts', 'time');

CREATE TABLE implant (
    name VARCHAR PRIMARY KEY,
    language TEXT,
    business_company TEXT,
    country TEXT
);

CREATE TABLE machine_info (
    time TIMESTAMPTZ PRIMARY KEY,
    machine_code VARCHAR NOT NULL,
    plant_code VARCHAR,
    room_code VARCHAR,
    group_code VARCHAR,
    row_code VARCHAR,
    mac_number 
    needles INTEGER,
    system_version VARCHAR,
    custom_version VARCHAR,
    uboot_version VARCHAR,
    cdk_version VARCHAR,
    FOREIGN KEY (machine_code) REFERENCES machine_devices (machine_code)
);
SELECT create_hypertable('machine_info', 'time');"""