# -*- coding: utf-8 -*-
"""
Created on Wed Jul 26 09:49:14 2023

@author: ONS2172
"""

import pyodbc 
import pandas as pd
import datetime


def select_driver():
    """Find least version of: ODBC Driver for SQL Server."""
    drv = sorted([drv for drv in pyodbc.drivers() if "SQL" in drv])
    if len(drv) == 0:
        raise Exception("No 'ODBC Driver XX for SQL Server' found.")
    return drv[0]

def get_sql_connection():

    conn = pyodbc.connect(
        'Driver={SQLServer};'
        'Server=mdzusvpcwapp200.krft.net;'
        'Database=Reporting_Global_DW;'
        'UID=S-CAT_Reporting;'
        'PWD=password1234;'
    )
    # conn = pyodbc.connect(
    #     # 'Driver={SQL Server};'
    #     'Driver={' + select_driver() + '};'
    #     'Server=mdzusvpcwapp200.krft.net;'
    #     'DBCName=Reporting_Global_DW;'
    #     'UID=S-CAT_Reporting;'
    #     'PWD=password1234;'
    # )
    cursor = conn.cursor()
    cursor.fast_executemany = True
    return conn, cursor

def close_sql_connection(conn):
    conn.close()
    
def genetate_query(df, table_name):
    col = len(df.columns)
    qm=""
    for i in range(col):
        qm = qm + "?, "
    qm = qm[:-2]
    
    dtlist = ['varchar', 'varchar', 'varchar', 'varchar', 'varchar', 'varchar', 'varchar', 'varchar', 'varchar', 'decimal', 'decimal', 'decimal', 'decimal', 'decimal', 'decimal', 'decimal', 'decimal', 'decimal', 'decimal', 'varchar', 'varchar', 'varchar', 'varchar', 'varchar', 'varchar', 'varchar']
    
    for i, col in enumerate(df.columns):
        if dtlist[i] == 'varchar' or dtlist[i] == 'date' :
            # print(col)
            df[col] = df[col].fillna('')
            df[col] = df[col].astype(object)
        elif dtlist[i] == 'decimal':
            # print(col)
            df[col] = df[col].astype(float)
            df[col] = df[col].round(decimals = 5)
            df[col] = df[col].fillna(0)
    
    # print(df.dtypes.value_counts())

    val = list(df.itertuples(index=False, name=None))
    sql_query = "INSERT INTO " + table_name + " VALUES " + "(" + qm + ")"
    return sql_query, val
    
def execute_query(conn, cursor, sql_query, val):
    today = datetime.datetime.now()
    print("Upload Start\t:\t"+today.strftime("%H:%M:%S"))
    cursor.executemany(sql_query, val)
    conn.commit()

    today = datetime.datetime.now()
    print("Upload End\t\t:\t"+today.strftime("%H:%M:%S"))
    
def fetch_data(conn, table_name, condition):

    query = 'SELECT * FROM ' + table_name + condition
    # print(query)
    today = datetime.datetime.now()
    print("Download Start\t:\t"+today.strftime("%H:%M:%S"))

    df = pd.read_sql_query(query, conn)
    # df.to_csv('sql.csv',index=False)

    today = datetime.datetime.now()
    print("Download End\t:\t"+today.strftime("%H:%M:%S"))
    # print(df.shape)
    return df

def delete_data(conn, cursor, table_name, condition):
    
    query = "Delete from " + table_name + condition
    print(query)
    
    cursor.execute(query)
    # conn.commit()
    
def get_condition(scenario):
    condition  = " where Scenario = '"+ scenario+"'"
    return condition

def upload_data(df, upload_table_name):
    conn, cursor = get_sql_connection()
    delete_data(conn, cursor, upload_table_name, '')
    sql_query, val = genetate_query(df, upload_table_name)
    execute_query(conn, cursor, sql_query, val)
    close_sql_connection(conn)

def download_data(download_table_name):
    # condition  = get_condition(scenario)
    condition = ''
    conn, cursor = get_sql_connection()
    df = fetch_data(conn, table_name=download_table_name , condition=condition)
    close_sql_connection(conn)
    # print(df)
    return df

# download_table_name = "Tbl_Dash_Test_v2"
# upload_table_name = "Tbl_Dash_Test_v2"

# df = download_data("Tbl_Dash_Test_v2_AC")
# df.to_csv('app/data/NPI_RCA.csv', index=False)
# df = pd.read_csv('app/data/NPI_RCA.csv')
# upload_data(df, "Tbl_Dash_Test_v2_AC")

def test():
    q1 = "delete from Tbl_Dash_Test_v2_AC"
    q2 = """insert into Tbl_Dash_Test_v2_AC values ('AMEA', 'AMEA', 2022, 12.8, 12.8, 12.8, 12.8, 12.8, 12.8, 12.8, 12.8, 12.8, 12.8, 12.8, 12.8, 12.8), ('ANZ', 'Australia', 2022, 9.3, 9.3, 9.3, 9.3, 9.3, 9.3, 9.3, 9.3, 9.3, 9.3, 9.3, 9.3, 9.3), ('ANZ', 'New Zealand', 2022, 9.3, 9.3, 9.3, 9.3, 9.3, 9.3, 9.3, 9.3, 9.3, 9.3, 9.3, 9.3, 9.3), ('ANZ', 'ANZ', 2022, 9.3, 9.3, 9.3, 9.3, 9.3, 9.3, 9.3, 9.3, 9.3, 9.3, 9.3, 9.3, 9.3), ('Greater China', 'China', 2022, 9.6, 9.6, 9.6, 9.6, 9.6, 9.6, 9.6, 9.6, 9.6, 9.6, 9.6, 9.6, 9.6), ('Greater China', 'Hong Kong', 2022, 9.6, 9.6, 9.6, 9.6, 9.6, 9.6, 9.6, 9.6, 9.6, 9.6, 9.6, 9.6, 9.6), ('Greater China', 'Taiwan', 2022, 9.6, 9.6, 9.6, 9.6, 9.6, 9.6, 9.6, 9.6, 9.6, 9.6, 9.6, 9.6, 9.6), ('Greater China', 'Greater China', 2022, 9.6, 9.6, 9.6, 9.6, 9.6, 9.6, 9.6, 9.6, 9.6, 9.6, 9.6, 9.6, 9.6), ('India', 'Bangladesh', 2022, 16.1, 16.1, 16.1, 16.1, 16.1, 16.1, 16.1, 16.1, 16.1, 16.1, 16.1, 16.1, 16.1), ('India', 'India', 2022, 16.1, 16.1, 16.1, 16.1, 16.1, 16.1, 16.1, 16.1, 16.1, 16.1, 16.1, 16.1, 16.1), ('India', 'India BU', 2022, 16.1, 16.1, 16.1, 16.1, 16.1, 16.1, 16.1, 16.1, 16.1, 16.1, 16.1, 16.1, 16.1), ('Japan', 'Japan', 2022, 50.9, 50.9, 50.9, 50.9, 50.9, 50.9, 50.9, 50.9, 50.9, 50.9, 50.9, 50.9, 50.9), ('MENAP', 'New Markets', 2022, 11.1, 11.1, 11.1, 11.1, 11.1, 11.1, 11.1, 11.1, 11.1, 11.1, 11.1, 11.1, 11.1), ('MENAP', 'Egypt', 2022, 11.1, 11.1, 11.1, 11.1, 11.1, 11.1, 11.1, 11.1, 11.1, 11.1, 11.1, 11.1, 11.1), ('MENAP', 'GCC', 2022, 11.1, 11.1, 11.1, 11.1, 11.1, 11.1, 11.1, 11.1, 11.1, 11.1, 11.1, 11.1, 11.1), ('MENAP', 'Lebanon', 2022, 11.1, 11.1, 
    11.1, 11.1, 11.1, 11.1, 11.1, 11.1, 11.1, 11.1, 11.1, 11.1, 11.1), ('MENAP', 'Morocco', 2022, 11.1, 11.1, 11.1, 11.1, 11.1, 11.1, 11.1, 11.1, 11.1, 11.1, 11.1, 11.1, 11.1), ('MENAP', 'Pakistan', 2022, 11.1, 11.1, 11.1, 11.1, 11.1, 11.1, 11.1, 11.1, 11.1, 11.1, 11.1, 11.1, 11.1), ('MENAP', 'Saudi Arabia', 2022, 11.1, 11.1, 11.1, 11.1, 11.1, 11.1, 
    11.1, 11.1, 11.1, 11.1, 11.1, 11.1, 11.1), ('MENAP', 'MENAP', 2022, 11.1, 11.1, 11.1, 11.1, 11.1, 11.1, 11.1, 11.1, 11.1, 11.1, 11.1, 11.1, 11.1), ('SEA', 'AMEA Exports', 2022, 14.2, 14.2, 14.2, 14.2, 14.2, 14.2, 14.2, 14.2, 14.2, 14.2, 14.2, 14.2, 14.2), ('SEA', 'Indonesia', 2022, 14.2, 14.2, 14.2, 14.2, 14.2, 14.2, 14.2, 14.2, 14.2, 14.2, 14.2, 14.2, 14.2), ('SEA', 'Malaysia', 2022, 14.2, 14.2, 14.2, 14.2, 14.2, 14.2, 14.2, 14.2, 14.2, 14.2, 14.2, 14.2, 14.2), ('SEA', 'Philippines', 2022, 14.2, 14.2, 14.2, 14.2, 14.2, 14.2, 14.2, 14.2, 14.2, 14.2, 14.2, 14.2, 14.2), ('SEA', 'Singapore', 2022, 14.2, 14.2, 14.2, 14.2, 14.2, 14.2, 14.2, 14.2, 14.2, 14.2, 14.2, 14.2, 14.2), ('SEA', 'Thailand', 2022, 14.2, 14.2, 14.2, 14.2, 14.2, 14.2, 14.2, 14.2, 14.2, 14.2, 14.2, 14.2, 14.2), ('SEA', 'Vietnam', 2022, 14.2, 14.2, 14.2, 14.2, 14.2, 14.2, 14.2, 14.2, 14.2, 14.2, 14.2, 14.2, 14.2), ('SEA', 'SEA', 2022, 14.2, 14.2, 14.2, 14.2, 14.2, 14.2, 14.2, 14.2, 14.2, 14.2, 14.2, 14.2, 14.2), ('SSA', 'CEA', 2022, 16.9, 16.9, 16.9, 16.9, 16.9, 16.9, 16.9, 16.9, 16.9, 16.9, 16.9, 16.9, 16.9), ('SSA', 'Ghana', 2022, 16.9, 16.9, 16.9, 16.9, 16.9, 16.9, 16.9, 16.9, 16.9, 16.9, 16.9, 16.9, 16.9), ('SSA', 'Nigeria', 2022, 16.9, 16.9, 16.9, 16.9, 16.9, 16.9, 16.9, 16.9, 16.9, 16.9, 16.9, 16.9, 16.9), ('SSA', 'South Africa', 2022, 16.9, 16.9, 16.9, 16.9, 16.9, 16.9, 16.9, 16.9, 16.9, 16.9, 16.9, 
    16.9, 16.9), ('SSA', 'SSA', 2022, 16.9, 16.9, 16.9, 16.9, 16.9, 16.9, 16.9, 16.9, 16.9, 16.9, 16.9, 16.9, 16.9), ('AMEA', 'AMEA', 2023, 14.0, 14.0, 14.0, 14.0, 14.0, 14.0, 14.0, 14.0, 14.0, 14.0, 14.0, 14.0, 14.0), ('ANZ', 'ANZ', 2023, 9.5, 9.5, 9.5, 9.5, 9.5, 9.5, 9.5, 9.5, 9.5, 9.5, 9.5, 9.5, 9.5), ('ANZ', 'New Zealand', 2023, 9.5, 9.5, 9.5, 9.5, 9.5, 9.5, 9.5, 9.5, 9.5, 9.5, 9.5, 9.5, 9.5), ('ANZ', 'Australia', 2023, 9.5, 9.5, 9.5, 9.5, 9.5, 9.5, 9.5, 9.5, 9.5, 9.5, 9.5, 9.5, 9.5), ('Greater China', 'Greater China', 2023, 9.8, 9.8, 9.8, 9.8, 9.8, 9.8, 9.8, 9.8, 9.8, 9.8, 9.8, 9.8, 9.8), ('Greater China', 'Taiwan', 2023, 9.8, 9.8, 9.8, 9.8, 9.8, 9.8, 9.8, 9.8, 9.8, 9.8, 9.8, 9.8, 9.8), ('Greater China', 'Hong Kong', 2023, 9.8, 9.8, 9.8, 9.8, 9.8, 9.8, 9.8, 9.8, 9.8, 9.8, 9.8, 9.8, 9.8), ('Greater China', 'China', 2023, 9.8, 9.8, 9.8, 9.8, 9.8, 9.8, 9.8, 9.8, 9.8, 9.8, 9.8, 9.8, 9.8), ('India', 'India BU', 2023, 16.3, 16.3, 16.3, 16.3, 16.3, 16.3, 16.3, 16.3, 16.3, 16.3, 16.3, 16.3, 16.3), ('India', 'India', 2023, 15.0, 15.0, 18.0, 15.0, 15.0, 15.0, 16.3, 16.3, 16.3, 16.3, 16.3, 16.3, 16.3), ('India', 'Bangladesh', 2023, 15.0, 15.0, 18.0, 15.0, 15.0, 15.0, 17.0, 16.3, 16.3, 16.3, 16.3, 16.3, 16.3), ('Japan', 'Japan', 2023, 51.1, 51.1, 51.1, 51.1, 51.1, 51.1, 51.1, 51.1, 51.1, 51.1, 51.1, 51.1, 51.1), ('MENAP', 'GCC', 2023, 11.3, 11.3, 11.3, 11.3, 11.3, 11.3, 11.3, 11.3, 11.3, 11.3, 11.3, 11.3, 11.3), ('MENAP', 'Lebanon', 2023, 11.3, 11.3, 11.3, 11.3, 11.3, 11.3, 11.3, 11.3, 11.3, 11.3, 11.3, 11.3, 11.3), ('MENAP', 'New Markets', 2023, 11.3, 11.3, 11.3, 11.3, 11.3, 11.3, 11.3, 11.3, 11.3, 11.3, 11.3, 11.3, 11.3), ('MENAP', 'Egypt', 2023, 11.3, 11.3, 11.3, 11.3, 11.3, 11.3, 11.3, 11.3, 11.3, 11.3, 11.3, 11.3, 11.3), ('MENAP', 'Pakistan', 2023, 11.3, 11.3, 11.3, 11.3, 11.3, 11.3, 11.3, 11.3, 11.3, 11.3, 11.3, 11.3, 11.3), ('MENAP', 'Saudi Arabia', 2023, 11.3, 11.3, 11.3, 11.3, 11.3, 
    11.3, 11.3, 11.3, 11.3, 11.3, 11.3, 11.3, 11.3), ('MENAP', 'MENAP', 2023, 11.3, 11.3, 11.3, 11.3, 11.3, 11.3, 11.3, 11.3, 11.3, 11.3, 11.3, 11.3, 11.3), ('MENAP', 'Morocco', 
    2023, 11.3, 11.3, 11.3, 11.3, 11.3, 11.3, 11.3, 11.3, 11.3, 11.3, 11.3, 11.3, 11.3), ('SEA', 'Thailand', 2023, 14.4, 14.4, 14.4, 14.4, 14.4, 14.4, 14.4, 14.4, 14.4, 14.4, 14.4, 14.4, 14.4), ('SEA', 'Singapore', 2023, 14.4, 14.4, 14.4, 14.4, 14.4, 14.4, 14.4, 14.4, 14.4, 14.4, 14.4, 14.4, 14.4), ('SEA', 'Malaysia', 2023, 14.4, 14.4, 14.4, 14.4, 14.4, 14.4, 14.4, 14.4, 14.4, 14.4, 14.4, 14.4, 14.4), ('SEA', 'SEA', 2023, 14.4, 14.4, 14.4, 14.4, 14.4, 14.4, 14.4, 14.4, 14.4, 14.4, 14.4, 14.4, 14.4), ('SEA', 'Vietnam', 2023, 14.4, 14.4, 14.4, 14.4, 14.4, 14.4, 14.4, 14.4, 14.4, 14.4, 14.4, 14.4, 14.4), ('SEA', 'Philippines', 2023, 14.4, 14.4, 14.4, 14.4, 14.4, 14.4, 14.4, 14.4, 14.4, 14.4, 14.4, 14.4, 14.4), ('SEA', 'Indonesia', 2023, 14.4, 14.4, 14.4, 14.4, 14.4, 14.4, 14.4, 14.4, 14.4, 14.4, 14.4, 14.4, 14.4), ('SEA', 'AMEA Exports', 2023, 14.4, 14.4, 14.4, 14.4, 14.4, 14.4, 14.4, 14.4, 14.4, 14.4, 14.4, 14.4, 14.4), ('SSA', 'Ghana', 2023, 17.1, 17.1, 17.1, 17.1, 17.1, 17.1, 17.1, 17.1, 17.1, 17.1, 17.1, 17.1, 17.1), ('SSA', 'CEA', 2023, 17.1, 17.1, 17.1, 17.1, 17.1, 17.1, 17.1, 17.1, 17.1, 17.1, 17.1, 17.1, 17.1), ('SSA', 'SSA', 2023, 17.1, 17.1, 17.1, 17.1, 17.1, 17.1, 17.1, 17.1, 17.1, 17.1, 17.1, 17.1, 17.1), ('SSA', 'Nigeria', 2023, 17.1, 17.1, 17.1, 17.1, 17.1, 17.1, 17.1, 17.1, 17.1, 17.1, 17.1, 17.1, 17.1), ('SSA', 'South Africa', 2023, 17.1, 17.1, 17.1, 17.1, 17.1, 17.1, 17.1, 17.1, 17.1, 17.1, 17.1, 17.1, 17.1)"""
    # q = q1+q2
    conn, cursor = get_sql_connection()
    try:
        cursor.execute(q1)
        # results = cursor.fetchone()
        # for result in results:
        #     print(result)

        cursor.execute(q2)
        # results = cursor.fetchone()
        # for result in results:
        #     print(result)
    except:
        print("Error")
    else:
        print("else")
        conn.commit()
# test()