import os
import sys
import pytz
import urllib3
import datetime
import numpy as np
import pandas as pd
import pyproj
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from dataretrieval import nwis
pd.options.mode.chained_assignment = None

def getSNOTELData(SiteName, SiteID, StateAbb, StartDate, EndDate, OutputFolder):
    #the api changed and we need to pull the site id out - 3-1-2026
    site_id = SiteID.split('_')[0]
    url1 = 'https://wcc.sc.egov.usda.gov/reportGenerator/view_csv/customMultiTimeSeriesGroupByStationReport/daily/start_of_period/'
    #url2 = f'{SiteID}:{StateAbb}:SNTL%7Cid=%22%22%7Cname/'
    url2 = f'{site_id}:{StateAbb}:SNTL%7Cid=%22%22%7Cname/'
    url3 = f'{StartDate},{EndDate}/'
    url4 = 'WTEQ::value?fitToScreen=false'
    url = url1+url2+url3+url4
    print(f'Start retrieving data for {SiteName}, {SiteID} \n {url}')

    http = urllib3.PoolManager()
    response = http.request('GET', url)
    data = response.data.decode('utf-8')
    i=0
    for line in data.split("\n"):
        if line.startswith("#"):
            i=i+1
    data = data.split("\n")[i:]

    df = pd.DataFrame.from_dict(data) 
    df = df[0].str.split(',', expand=True)
    df.rename(columns={0:df[0][0], 
                        1:df[1][0]}, inplace=True)
    df.drop(0, inplace=True)
    df.dropna(inplace=True)
    df.reset_index(inplace=True, drop=True)
    df["Date"] = pd.to_datetime(df["Date"])
    df.rename(columns={df.columns[1]:'Snow Water Equivalent (m) Start of Day Values'}, inplace=True)
    df.iloc[:, 1:] = df.iloc[:, 1:].apply(lambda x: pd.to_numeric(x) * 0.0254)  # convert in to m
    df['Water_Year'] = pd.to_datetime(df['Date']).map(lambda x: x.year+1 if x.month>9 else x.year)

    df.to_csv(f'./{OutputFolder}/df_{SiteID}_{StateAbb}_SNTL.csv', index=False)

def getCaliSNOTELData(SiteName, SiteID, StartDate, EndDate, OutputFolder):
    StateAbb = 'Ca'
    url1 = 'https://wcc.sc.egov.usda.gov/reportGenerator/view_csv/customMultiTimeSeriesGroupByStationReport/daily/start_of_period/'
    url2 = f'{SiteID}:CA:MSNT%257Cid=%2522%2522%257Cname/'
    url3 = f'{StartDate},{EndDate}/'
    url4 = 'WTEQ::value?fitToScreen=false'
    url = url1+url2+url3+url4
    print(f'Start retrieving data for {SiteName}, {SiteID}')
    print(url)
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Accept': 'text/csv,text/plain,application/csv',
        'Connection': 'keep-alive'
    }

    timeout = urllib3.Timeout(connect=2.0, read=10.0)
    retries = urllib3.Retry(total=3, backoff_factor=1, status_forcelist=[500, 502, 503, 504])

    http = urllib3.PoolManager(
        headers=headers,
        timeout=timeout,
        retries=retries,
        block=False
    )

    response = None

    try:
        response = http.request('GET', url, timeout=10.0)
        print(f"Status: {response.status}")
    except urllib3.exceptions.MaxRetryError:
        print("Error: The HPC network cannot reach the USDA server (Check Proxy).")
        return
    except urllib3.exceptions.TimeoutError:
        print("Error: The request timed out (The server or firewall is not responding).")
        return
    except Exception as e:
        print(f"Request failed: {e}")
        return

    if response is None:
        return

    data = response.data.decode('utf-8')
    print('Data decoded from bytes to string')
    i=0
    for line in data.split("\n"):
        if line.startswith("#"):
            i=i+1
    data = data.split("\n")[i:]

    df = pd.DataFrame.from_dict(data)
    df = df[0].str.split(',', expand=True)
    df.rename(columns={0:df[0][0], 
                        1:df[1][0]}, inplace=True)
    df.drop(0, inplace=True)
    df.dropna(inplace=True)
    df.reset_index(inplace=True, drop=True)
    df["Date"] = pd.to_datetime(df["Date"])
    df.rename(columns={df.columns[1]:'Snow Water Equivalent (m) Start of Day Values'}, inplace=True)
    df.iloc[:, 1:] = df.iloc[:, 1:].apply(lambda x: pd.to_numeric(x) * 0.0254)
    df['Water_Year'] = pd.to_datetime(df['Date']).map(lambda x: x.year+1 if x.month>9 else x.year)

    df.to_csv(f'./{OutputFolder}/df_{SiteID}_{StateAbb}_SNTL.csv', index=False)