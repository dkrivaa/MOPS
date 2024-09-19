from mof_data import get_data, get_takanot
from wix_requests import takanot_request


years = [2022]
for year in years:
    # All of ministry
    df = get_data(year, 'total', 'total')

    df_json = get_takanot(df)
    # takanot_request(df_json)

