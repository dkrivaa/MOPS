from mof_data import get_data, get_data_special, get_takanot, get_takanot_special
from wix_requests import takanot_request, takanot_request_special


def update_takanot():
    years = [2022, 2023, 2024]
    for year in years:
        # All of ministry
        df = get_data(year, 'total', 'total')

        df_json = get_takanot(df)


def update_takanot_special():
    years = [2024, 20241]
    for year in years:
        # All of ministry
        if year == 2024:
            df = get_data(year, 'total', 'total')

            df_json = get_takanot_special(df)

        if year == 20241:
            df = get_data_special(year, 'total', 'total')
            df['שנה'] = 20241
            print(df.iloc[0,0])
            # df_json = get_takanot_special(df)

