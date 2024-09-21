from mof_data import get_data, get_takanot
from wix_requests import takanot_request


def update_takanot():
    years = [2022, 2023, 2024]
    for year in years:
        # All of ministry
        df = get_data(year, 'total', 'total')

        df_json = get_takanot(df)

