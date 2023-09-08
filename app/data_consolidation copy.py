# -*- coding: utf-8 -*-
"""
Created on Fri Aug 18 12:02:26 2023

@author: ONS2172
"""

import os
import pandas as pd

ROOT_FOLDER_PATH = "C:\\AMEA NPI RCA Automation\\"
# ROOT_FOLDER_PATH = "C:\\Dash\AMEA NPI RCA Automation\\app\\data"

folder_path = ROOT_FOLDER_PATH + "Inputs\\"
conso_file_path = ROOT_FOLDER_PATH + "YTD Template\\NPI_RCA.csv"

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
        columns = ['Month', 'Week', 'BU', 'Country', 'Global Category', 'SKU Code', 'SKU-Desc', 'Location Code', 'Location Desc', 'Total Inv ($K)', 'Active Inv ($K)', 'Blocked Inv ($K)', 'Excess Inv ($K)', 'IWND Inv ($K)', 'Low Inv ($K)', 'NPI Inv ($K)', 'DIFC', 'Min Bnd Days', 'Max Bnd Days', 'RCA', 'Driver', 'DIOH Opp', 'Comments', 'Included in Provision', 'Timing of resolution (M)', 'RCA Status']
        df[columns]=''
        months_available=[]
        
    return df, months_available

def generate_consolidated_file():

    df, months_available = get_existing_data()
    
    for folder in os.listdir(folder_path):
        if folder not in months_available:
            print(folder)
            df_new = pd.read_excel(folder_path+folder+"\\"+"NPI Data Model.xlsx", sheet_name='Sheet 1')
            df_new.insert(loc=0, column='Month', value=folder.replace(' ', '-'))
            df_new.columns = ['Month', 'Week', 'BU', 'Country', 'Global Category', 'SKU Code', 'SKU-Desc', 'Location Code', 'Location Desc', 'Total Inv ($K)', 'Active Inv ($K)', 'Blocked Inv ($K)', 'Excess Inv ($K)', 'IWND Inv ($K)', 'Low Inv ($K)', 'NPI Inv ($K)', 'DIFC', 'Min Bnd Days', 'Max Bnd Days']
            if test_mode:
                for filter in test_filters:
                    df_new = df_new[df_new[filter].isin(test_filters[filter])]
            df = pd.concat([df, df_new])

    df.to_csv(conso_file_path, index=False)
    return df
    
if __name__ == "__main__":
    generate_consolidated_file()