from mof_data import get_data



years = [2022]
for year in years:
    # All of ministry
    df = get_data(year, 'total', 'total')
