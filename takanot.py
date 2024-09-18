from mof_data import get_data, get_takanot



years = [2022]
for year in years:
    # All of ministry
    df = get_data(year, 'total', 'total')

    get_takanot(df)
