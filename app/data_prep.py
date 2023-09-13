import pandas as pd
import numpy as np

rca_mapping = pd.read_csv('assets/rca_mapping.csv')
# rca_mapping = pd.read_csv('app/assets/rca_mapping.csv')


def npi_chart_1(df):
    # df['Date'] = pd.to_datetime(df['Month'], format="%b-%Y")
    # df1 = df.drop_duplicates(subset=['Date'])
    # df = df.sort_values(by='Week', ascending=False)
    # latest_month = df.iloc[0, 0]
    latest_month = df[df['Week']==df['Week'].unique().max()]['Month'].unique()[0]
    # print(latest_month)
    df = df[df['Month'] == latest_month]
    df = df[['BU', 'NPI Inv ($K)', 'Total Inv ($K)']]
    df = df.groupby(by='BU', as_index=False).sum()
    df['NPI %'] = df['NPI Inv ($K)']/df['Total Inv ($K)']*100
    df['NPI %'] = df['NPI %'].round(2)
    # print(df)
    return df

def npi_chart_2(df):
    df = df[['Month', 'Date', 'NPI Inv ($K)', 'Total Inv ($K)']]
    df = df.groupby(by=['Month', 'Date'], as_index=False).sum()
    df['NPI %'] = df['NPI Inv ($K)']/df['Total Inv ($K)']*100
    df['NPI %'] = df['NPI %'].round(2)
    df = df.sort_values(by='Date')
    return df

def npi_chart_3(df):
    df = df[['Blocked Inv ($K)', 'Excess Inv ($K)', 'IWND Inv ($K)']]
    df = pd.DataFrame(df.sum(), columns=['NPI Components'])
    return df

def npi_chart_4(df):
    # Old code - NPI Drivers
    # df = df[['Driver', 'NPI Inv ($K)']]
    # df = df.groupby(by='Driver', as_index=False).sum()

    df = df[['Global Category', 'SKU-Desc', 'Total Inv ($K)', 'NPI Inv ($K)']]
    df = df.groupby(by=['Global Category', 'SKU-Desc'], as_index=False).sum()
    df['NPI %'] = df['NPI Inv ($K)']/df['Total Inv ($K)']
    df = df.sort_values(by='NPI %', ascending=False)
    # df = df.iloc[:10,:]
    # print(df)
    return df

def npi_chart_5(df):
    df = df[['RCA', 'NPI Inv ($K)']]
    df['RCA'] = df['RCA'].fillna('BLANK')
    df = df.groupby(by='RCA', as_index=False).sum()
    df = df.sort_values(by='NPI Inv ($K)', ascending=False)
    df = df.iloc[:10,:]
    return df

def calculate(df):
    latest_month = df[df['Week']==df['Week'].unique().max()]['Month'].unique()[0]
    df = df[df['Month'] == latest_month]
    # print(rca_mapping)
    driver_map = rca_mapping.set_index('RCA')['Driver'].to_dict()
    dioh_map = rca_mapping.set_index('RCA')['DIOH Opp'].to_dict()
    df['Driver'] = df['RCA'].map(driver_map)
    df['DIOH Opp'] = df['RCA'].map(dioh_map)
    df['Driver'] = df['Driver'].fillna('')
    df['DIOH Opp'] = df['DIOH Opp'].fillna('')
    df['RCA'] = df['RCA'].fillna('')
    df.loc[df['NPI Inv ($K)']<=0, 'RCA Status'] = 'Not applicable'
    df.loc[df['NPI Inv ($K)']>0, 'RCA Status'] = 'RCA Available'
    df.loc[(df['NPI Inv ($K)']>0) & (df['RCA']==''), 'RCA Status'] = 'RCA Missing'
    # print(df)
    return df

def rca_status_summary(df):
    df['Count of Missing RCA Status'] = 1
    df = df[df['RCA Status'] == 'RCA Missing']
    if df['BU'].nunique() == 1:
        col = 'Country'
    else:
        col = 'BU'
    df = df[[col, 'Count of Missing RCA Status']]
    df_summary = df.groupby(by=col, as_index=False).sum()
    df_summary.loc['Total'] = df.sum()
    df_summary.loc[df_summary.index[-1], col] = 'Total'
    # print(df_summary)
    return df_summary

def rca_chart_1(df):
    df = df[(df['RCA'].isna()) | (df['RCA']=='')]
    df = df[df['RCA Status'] == 'RCA Missing']
    df = df[df['Month']=='Jul-2023']
    df = df[['BU', 'NPI Inv ($K)']]
    df['Count'] = 1
    df = df.groupby(by='BU', as_index=False).sum()
    return df

def rca_chart_2(df):
    df = df[(df['RCA'].isna()) | (df['RCA']=='')]
    df = df[df['RCA Status'] == 'RCA Missing']
    df = df[df['Month']=='Jul-2023']
    df = df[['Global Category', 'NPI Inv ($K)']]
    df['Count'] = 1
    df = df.groupby(by='Global Category', as_index=False).sum()
    return df

def rca_chart_3(df):
    df = df[(df['RCA'].isna()) | (df['RCA']=='')]
    df = df[df['RCA Status'] == 'RCA Missing']
    # df = df[df['Month']=='Jul-2023']
    df = df[['Month', 'NPI Inv ($K)']]
    df['Count'] = 1
    df = df.groupby(by='Month', as_index=False).sum()
    return df

def rca_chart_4(df):
    df = df[df['Month']=='Jul-2023']
    df = df[['RCA Status', 'NPI Inv ($K)']]
    df['Count'] = 1
    df = df.groupby(by='RCA Status', as_index=False).sum()
    return df

def rca_chart_5(df):
    df = df[df['RCA Status'] == 'RCA Available']
    df = df[df['Month']=='Jul-2023']
    df = df[['Driver', 'NPI Inv ($K)']]
    df['Count'] = 1
    df = df.groupby(by='Driver', as_index=False).sum()
    return df

def rca_chart_6(df):
    df = df[df['RCA Status'] == 'RCA Available']
    df = df[df['Month']=='Jul-2023']
    df = df[['RCA', 'NPI Inv ($K)']]
    df['Count'] = 1
    df = df.groupby(by='RCA', as_index=False).sum()
    return df

def get_data(df, id):
    df['Week'] = df['Week'].astype(str)
    df['Date'] = pd.to_datetime(df['Month'], format="%b-%Y")
    df['SKU Code'] = df['SKU Code'].astype(object)
    if id == 'npi-1':
        return npi_chart_1(df)
    elif id == 'npi-2':
        return npi_chart_2(df)
    elif id == 'npi-3':
        return npi_chart_3(df)
    elif id == 'npi-4':
        return npi_chart_4(df)
    elif id == 'npi-5':
        return npi_chart_5(df)
    elif id =='calculate':
        return calculate(df)
    elif id =='rca_status_summary':
        return rca_status_summary(df)
    elif id == 'rca-1':
        return rca_chart_1(df)
    elif id == 'rca-2':
        return rca_chart_2(df)
    elif id == 'rca-3':
        return rca_chart_3(df)
    elif id == 'rca-4':
        return rca_chart_4(df)
    elif id == 'rca-5':
        return rca_chart_5(df)
    elif id == 'rca-6':
        return rca_chart_6(df)
    
if __name__=='__main__':
    df = pd.read_csv('app/data/NPI_RCA_v2.csv')
    # print(df.dtypes)
    # print(get_data(df, 'npi-1'))
    get_data(df, 'npi-1')