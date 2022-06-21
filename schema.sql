# -*- coding: utf-8 -*-
"""
Created on Thu Jun 16 15:24:43 2022

@author: dinema
"""

CREATE TABLE stops_registry (
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
      answers_loc TEXT[],
      component
      UNIQUE(message_code)
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
    FOREIGN KEY (stop_code) REFERENCES stops_registry (message_code),
    UNIQUE(stop_id)
);

CREATE TABLE tamburini_info (
    tamburini_id VARCHAR PRIMARY KEY,
    machine_code VARCHAR NOT NULL,
    name TEXT NOT NULL,
    levels INTEGER NOT NULL,
    FOREIGN KEY (machine_code) REFERENCES machine_devices (machine_code),
    UNIQUE(tamburini_id)
);

CREATE TABLE tamburini_values (
    time TIMESTAMPTZ PRIMARY KEY,
    tamburini_id VARCHAR NOT NULL,
    count INTEGER NOT NULL,
    counter INTEGER NOT NULL,
    FOREIGN KEY (tamburini_id) REFERENCES tamburini_info (tamburini_id),
    UNIQUE(time)
);
SELECT create_hypertable('tamburini_values', 'time');

CREATE TABLE electrovalve_info (
    electrovalve_id VARCHAR PRIMARY KEY,
    machine_code VARCHAR NOT NULL,
    name TEXT NOT NULL,
    max_shot INTEGER NOT NULL,
    FOREIGN KEY (machine_code) REFERENCES machine_devices (machine_code),
    UNIQUE(electrovalve_id)
);

CREATE TABLE electrovalve_values (
    time TIMESTAMPTZ PRIMARY KEY,
    electrovalve_id VARCHAR NOT NULL,
    count INTEGER[] NOT NULL,
    counter INTEGER NOT NULL,
    time_max 
    FOREIGN KEY (electrovalve_id) REFERENCES electrovalve_info (electrovalve_id),
    UNIQUE(time)
);
SELECT create_hypertable('electrovalve_values', 'time');

CREATE TABLE oc_motors_info (
    oc_motors_id VARCHAR PRIMARY KEY,
    machine_code VARCHAR NOT NULL,
    name TEXT NOT NULL,
    logic_trac INTEGER NOT NULL,
    FOREIGN KEY (machine_code) REFERENCES machine_devices (machine_code),
    UNIQUE(oc_motors_id)
);

CREATE TABLE oc_motors_values (
    time TIMESTAMPTZ PRIMARY KEY,
    oc_motors_id VARCHAR NOT NULL,
    steps INTEGER NOT NULL,
    counter INTEGER NOT NULL,
    FOREIGN KEY (oc_motors_id) REFERENCES oc_motors_info (oc_motors_id),
    UNIQUE(time)
);
SELECT create_hypertable('oc_motors_values', 'time');

CREATE TABLE cc_motors_info (
    cc_motors_id VARCHAR PRIMARY KEY,
    machine_code VARCHAR NOT NULL,
    name TEXT NOT NULL,
    logic_trac INTEGER NOT NULL,
    FOREIGN KEY (machine_code) REFERENCES machine_devices (machine_code),
    UNIQUE(cc_motors_id)
);

CREATE TABLE cc_motors_values (
    time TIMESTAMPTZ PRIMARY KEY,
    cc_motors_id VARCHAR NOT NULL,
    power INTEGER NOT NULL,
    counter INTEGER NOT NULL,
    FOREIGN KEY (cc_motors_id) REFERENCES oc_motors_info (cc_motors_id),
    UNIQUE(time)
);
SELECT create_hypertable('cc_motors_values', 'time');

CREATE TABLE azionamenti_info (
    azionamenti_id VARCHAR PRIMARY KEY,
    machine_code VARCHAR NOT NULL,
    name TEXT NOT NULL,
    FOREIGN KEY (machine_code) REFERENCES machine_devices (machine_code),
    UNIQUE(azionamenti_id)
);

CREATE TABLE azionamenti_values (
    time TIMESTAMPTZ PRIMARY KEY,
    azionamenti_id VARCHAR NOT NULL,
    power INTEGER NOT NULL,
    counter INTEGER NOT NULL,
    FOREIGN KEY (azionamenti_id) REFERENCES azionamenti_info (azionamenti_id),
    UNIQUE(time)
);
SELECT create_hypertable('azionamenti_values', 'time');

CREATE TABLE thread_power_supply_info (
    thread_power_supply_id VARCHAR PRIMARY KEY,
    machine_code VARCHAR NOT NULL,
    name TEXT NOT NULL,
    FOREIGN KEY (machine_code) REFERENCES machine_devices (machine_code),
    UNIQUE(thread_power_supply_id)
);

CREATE TABLE thread_power_supply_values (
    time TIMESTAMPTZ PRIMARY KEY,
    thread_power_supply_id VARCHAR NOT NULL,
    consumption INTEGER NOT NULL,
    load INTEGER NOT NULL,
    counter INTEGER NOT NULL,
    FOREIGN KEY (thread_power_supply_id) REFERENCES thread_power_supply_info (thread_power_supply_id),
    UNIQUE(time)
);
SELECT create_hypertable('thread_power_supply_values', 'time');

CREATE TABLE ps_power_supply_info (
    ps_power_supply_id VARCHAR PRIMARY KEY,
    machine_code VARCHAR NOT NULL,
    name TEXT NOT NULL,
    FOREIGN KEY (machine_code) REFERENCES machine_devices (machine_code),
    UNIQUE(ps_power_supply_id)
);

CREATE TABLE ps_power_supply_values (
    time TIMESTAMPTZ PRIMARY KEY,
    ps_power_supply_id VARCHAR NOT NULL,
    power INTEGER NOT NULL,
    counter INTEGER NOT NULL,
    FOREIGN KEY (ps_power_supply_id) REFERENCES ps_power_supply_info (ps_power_supply_id),
    UNIQUE(time)
);
SELECT create_hypertable('ps_power_supply_values', 'time');

CREATE TABLE article_values (
    time TIMESTAMPTZ PRIMARY KEY,
    machine_code VARCHAR NOT NULL,
    temperature FLOAT,
    oil FLOAT,
    pression FLOAT,
    counter INTEGER NOT NULL,
    FOREIGN KEY (machine_code) REFERENCES machine_devices (machine_code),
    UNIQUE(time)
);
SELECT create_hypertable('article_values', 'time');

CREATE TABLE machine_devices (
    machine_code VARCHAR PRIMARY KEY,
    model VARCHAR NOT NULL,
    UNIQUE(machine_code)
);

CREATE TABLE machine_parts (
    time TIMESTAMPTZ PRIMARY KEY,
    device_id VARCHAR NOT NULL,
    machine_code VARCHAR NOT NULL,
    description TEXT,
    tipology TEXT,
    intervenction TEXT,
    FOREIGN KEY (machine_code) REFERENCES machine_devices (machine_code),
    UNIQUE(machine_code, device_id)
);
SELECT create_hypertable('machine_parts', 'time');

CREATE TABLE implant (
    name VARCHAR PRIMARY KEY,
    language TEXT,
    business_company TEXT,
    country TEXT,
    UNIQUE(name)
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
    FOREIGN KEY (machine_code) REFERENCES machine_devices (machine_code),
    UNIQUE(machine_code, device_id)
);
SELECT create_hypertable('machine_info', 'time');










