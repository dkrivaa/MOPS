from mof_data import get_data, get_annual_total
from wix_requests import annual_request

# Lists to hold data
total_data = []
ministry_data = []
witness_data = []
fire_data = []
prison_data = []
police_data = []

years = [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024]
budgets = ['total', 'wages', 'other']
for year in years:
    for budget in budgets:
        # All of ministry
        df = get_data(year, 'total', budget)
        data = get_annual_total(df, 'total', budget)
        total_data.append(data)

        organizations = ['ministry', 'witness', 'fire', 'prison', 'police']
        for organization in organizations:
            df = get_data(year, organization, budget)
            data = get_annual_total(df, organization, budget)
            # Append data to the appropriate list
            if organization == 'ministry':
                ministry_data.append(data)
            elif organization == 'witness':
                witness_data.append(data)
            elif organization == 'fire':
                fire_data.append(data)
            elif organization == 'prison':
                prison_data.append(data)
            elif organization == 'police':
                police_data.append(data)

data_lists = [total_data, ministry_data, witness_data, fire_data, prison_data, police_data]
for d_list in data_lists:
    annual_request(d_list)
