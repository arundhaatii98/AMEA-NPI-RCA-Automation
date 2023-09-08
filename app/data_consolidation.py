# -*- coding: utf-8 -*-
"""
Created on Fri Aug 18 12:02:26 2023

@author: ONS2172
"""

import os
import pandas as pd

# ROOT_FOLDER_PATH = "C:\\AMEA NPI RCA Automation\\"
ROOT_FOLDER_PATH = "C:\\Users\\ONS2172\MDLZ\\CAT Reporting Site - AMEA NPI RCA Automation\\"

folder_path = ROOT_FOLDER_PATH + "Inputs\\"
conso_file_path = ROOT_FOLDER_PATH + "YTD Template\\NPI_RCA.csv"

column_list = ['Month', 'Week', 'BU', 'Country', 'Global Category', 'SKU Code', 'SKU-Desc', 'Location Code', 'Location Desc', 'Total Inv ($K)', 'Active Inv ($K)', 'Blocked Inv ($K)', 'Excess Inv ($K)', 'IWND Inv ($K)', 'Low Inv ($K)', 'NPI Inv ($K)', 'DIFC', 'Min Bnd Days', 'Max Bnd Days', 'RCA', 'Driver', 'DIOH Opp', 'Comments', 'Included in Provision', 'Timing of resolution (M)', 'RCA Status']

test_mode = False
test_filters={
    'BU':['ANZ']
}

def get_existing_data():
    
    if os.path.isfile(conso_file_path):
        df = pd.read_csv(conso_file_path)
        months_available = df['Month'].unique()
        months_available = [month.replace('-', ' ') for month in months_available]
    else:
        df = pd.DataFrame()
        df[column_list]=''
        months_available=[]
        
    return df, months_available

def generate_consolidated_file():

    df, months_available = get_existing_data()
    # df = pd.DataFrame()
    # months_available=[]
    for folder in os.listdir(folder_path):
        if folder not in months_available:
            print(folder)
            df_new = pd.read_excel(folder_path+folder+"\\"+"NPI Data Model.xlsx", sheet_name='Sheet 1')
            df_new['Month'] = df_new['Month'].dt.strftime('%b-%Y')
            df_new.columns = ['Month', 'Week', 'BU', 'Country', 'Global Category', 'SKU Code', 'SKU-Desc', 'Location Code', 'Location Desc', 'Total Inv ($K)', 'Active Inv ($K)', 'Blocked Inv ($K)', 'Excess Inv ($K)', 'IWND Inv ($K)', 'Low Inv ($K)', 'NPI Inv ($K)', 'DIFC', 'Min Bnd Days', 'Max Bnd Days']
            if test_mode:
                for filter in test_filters:
                    df_new = df_new[df_new[filter].isin(test_filters[filter])]
            df = pd.concat([df, df_new])
    
    df = df.fillna('')

    df = df.sort_values(by=['Week', 'Location Code', 'SKU Code'], ascending=True)
    df.to_csv(conso_file_path, index=False)
    return df
    
def save_consolidated_file(df):
    df = df[column_list]
    df.to_csv(conso_file_path, index=False)

if __name__ == "__main__":
    df = generate_consolidated_file()
    print(df)