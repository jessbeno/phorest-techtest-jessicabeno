#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 06:34:34 2024

@author: jessicabeno
"""

import os, sys
import pandas as pd
import sqlite3

def populate_table(db_name, data, col_names, table_name):
    '''
    This function inserts data into the specified table.
    
    args:
        db_name (str):      Name of the database
        data (list):        List of lists (each list is a row of the database)
        col_names (str):    Comma-delimited string of the column names
        table_name (str):   Name of the table to insert the data into
    '''
    
    # Create the database
    db_conn = sqlite3.connect(db_name)

    cur = db_conn.cursor()
    
    
    
    db_conn.close()


# User settings
db_name = 'client_data.db'
infile_clients = 'clients.csv'
infile_appts = 'appointments.csv'
infile_purch = 'purchases.csv'
infile_serv = 'services.csv'

# Obtain current directory
dir_main = os.getcwd()

# Define paths
path_clients = '%s/0_infiles/%s' % (dir_main, infile_clients)
path_appts = '%s/0_infiles/%s' % (dir_main, infile_appts)
path_purch = '%s/0_infiles/%s' % (dir_main, infile_purch)
path_serv = '%s/0_infiles/%s' % (dir_main, infile_serv)

# Create the database
db_conn = sqlite3.connect(db_name)

cur = db_conn.cursor()

# Drop table if it already exists
cur.execute('DROP TABLE IF EXISTS clients')
cur.execute('DROP TABLE IF EXISTS appointments')
cur.execute('DROP TABLE IF EXISTS purchases')
cur.execute('DROP TABLE IF EXISTS services')

# Create tables
db_conn.execute('''CREATE TABLE clients
(id VARCHAR(50) PRIMARY KEY,
first_name VARCHAR(50),
last_name VARCHAR(50),
email VARCHAR(50),
phone VARCHAR(50),
gender VARCHAR(50),
banned BOOL);''')

db_conn.execute('''CREATE TABLE appointments
(id VARCHAR(50) PRIMARY KEY,
client_id VARCHAR(50),
start_time DATETIME,
end_time DATETIME,
FOREIGN KEY (client_id) REFERENCES clients (id));''')

db_conn.execute('''CREATE TABLE purchases
(id VARCHAR(50) PRIMARY KEY,
appointment_id VARCHAR(50),
name VARCHAR(50),
price DECIMAL(10,2),
loyalty_points INT,
FOREIGN KEY (appointment_id) REFERENCES appointments (id));''')

db_conn.execute('''CREATE TABLE services
(id VARCHAR(50) PRIMARY KEY,
appointment_id VARCHAR(50),
name VARCHAR(50),
price DECIMAL(10,2),
loyalty_points INT,
FOREIGN KEY (appointment_id) REFERENCES appointments (id));''')

db_conn.close()

# Populate tables
