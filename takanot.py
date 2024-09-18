from mof_data import get_data, get_takanot


years = [2023]
for year in years:
    # All of ministry
    df = get_data(year, 'total', 'total')

    df_json = get_takanot(df)

