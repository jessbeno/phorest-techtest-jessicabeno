#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 06:34:34 2024

@author: jessicabeno
"""

import os, sys
import pandas as pd
import sqlite3
import json

def utility_parse_data(infile_path):
    '''
    Reads in data to pandas df. Iterates over rows. Stores rows into list.
    
    args:
        infile_path (str):  Path to the specified infile.
        
    returns:
        storage (list):     List of lists. Each row of infile is stored as a list.
    
    '''
    
    df = pd.read_csv(infile_path)
    
    storage = list()
    
    for idx, row in df.iterrows():
        storage.append(row)
        
    return storage


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
    
    # Add the data:
    #db_conn.executemany('INSERT INTO %s (%s) VALUES (?,?,?,?,?,?,?);' % (table_name,col_names),data)
    bindings_str = ','.join(['?' for i in col_names.split(',')])
    db_conn.executemany('INSERT INTO %s (%s) VALUES (%s);' % (table_name, col_names, bindings_str), data)

    db_conn.commit()
    
    
    db_conn.close()


# User settings
db_name = 'client_data.db'
infile_clients = 'clients.csv'
infile_appts = 'appointments.csv'
infile_purch = 'purchases.csv'
infile_serv = 'services.csv'

print('Enter top X number: ')
query_topxnumber = input()

print('Enter since date: (format as 2018-01-01)')
query_since_date = input()

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
# Populate clients table
col_names = 'id,first_name,last_name,email,phone,gender,banned'
storage = utility_parse_data(path_clients)
populate_table(db_name, storage, col_names, 'clients')

# Populate appointments table
col_names = 'id,client_id,start_time,end_time'
storage = utility_parse_data(path_appts)
populate_table(db_name, storage, col_names, 'appointments')

# Populate purchases table
col_names = 'id,appointment_id,name,price,loyalty_points'
storage = utility_parse_data(path_purch)
populate_table(db_name, storage, col_names, 'purchases')

# Populate services table
col_names = 'id,appointment_id,name,price,loyalty_points'
storage = utility_parse_data(path_serv)
populate_table(db_name, storage, col_names, 'services')

# Query - Top X number of clients that have accumulated the most loyalty points since Y date
db_conn = sqlite3.connect(db_name)

cur = db_conn.cursor()
            
parameters = (query_since_date, query_topxnumber)
query = '''SELECT clients.*, SUM(purchases.loyalty_points) AS total_loyalty_points
            FROM clients 
            JOIN appointments ON clients.id = appointments.client_id
            JOIN purchases ON appointments.id = purchases.appointment_id
            WHERE DATE(SUBSTR(appointments.end_time, 1, LENGTH(appointments.end_time) - 5)) >= ?
            GROUP BY clients.id
            ORDER BY total_loyalty_points DESC
            LIMIT ?;
            '''

query_store = db_conn.execute(query, parameters)
rows = query_store.fetchall()

db_conn.close()


# Convert to json compatible object

cols = [col[0] for col in query_store.description]

results = [dict(zip(cols, row)) for row in rows]

json_results = json.dumps(results)



