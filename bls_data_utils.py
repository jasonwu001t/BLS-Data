"""
API Key is optional, but limits your calls, you can register for free at : https://www.bls.gov/developers/api_signature_v2.htm

# HTTP Type:	POST
# URL (JSON):	https://api.bls.gov/publicAPI/v2/timeseries/data/
# URL (Excel):	https://api.bls.gov/publicAPI/v2/timeseries/data.xlsx
# Header:	Content-Type= application/json
# Payload (JSON):	{"seriesid":["Series1",..., "SeriesN"], "startyear":"yearX", "endyear":"yearY",
# "catalog":true|false, "calculations":true|false, "annualaverage":true|false,"aspects":true|false,
# "registrationkey":"XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX" }
"""


import requests
import json
import pandas as pd
from datetime import datetime

def fetch_bls_data(series_ids, start_year, end_year):
    headers = {'Content-type': 'application/json'}
    data = json.dumps({
        "seriesid": series_ids,
        "startyear": str(start_year),
        "endyear": str(end_year),
        "registrationkey": ''  # Optional
    })
    response = requests.post('https://api.bls.gov/publicAPI/v2/timeseries/data/', data=data, headers=headers)
    json_data = json.loads(response.text)
    all_data = []
    for series in json_data['Results']['series']:
        series_id = series['seriesID']
        for item in series['data']:
            all_data.append({
                "series_id": series_id,
                "year": item['year'],
                "period": item['period'],
                "value": float(item['value']),
            })
    df = pd.DataFrame(all_data)
    df['date'] = pd.to_datetime(df['year'] + df['period'].str.replace('M', '-'), format='%Y-%m')
    df.sort_values(by=['series_id', 'date'], inplace=True)
    return df

def calculate_mom_changes(df):
    df.sort_values(by=['series_id', 'year', 'period'], inplace=True)
    df['mom_change'] = df.groupby('series_id')['value'].diff()
    return df
