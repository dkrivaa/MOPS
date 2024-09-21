import json

import pandas as pd
import numpy as np
import requests
from io import BytesIO
from wix_requests import takanot_request
import os

from codes import budget_types, organization_codes, wage_codes


def get_data(year, organization, budget):

    # urls for Excel data from Finance Ministry 'https://www.gov.il/he/departments/policies/tableau'
    urls = {
        2024: 'https://www.gov.il/BlobFolder/policy/tableau/he/tableau_BudgetData2024.xls',
        2023: 'https://www.gov.il/BlobFolder/policy/tableau/he/tableau_BudgetData2023.xlsx',
        2022: 'https://www.gov.il/BlobFolder/policy/tableau/he/tableau_BudgetData2022.xlsx',
        2021: 'https://www.gov.il/BlobFolder/policy/tableau/he/tableau_tableau_BudgetData2021.xlsx',
        2020: 'https://www.gov.il/BlobFolder/policy/tableau/he/tableau_BudgetData2020.xlsx',
        2019: 'https://www.gov.il/BlobFolder/policy/tableau/he/tableau_BudgetData2019.xlsx',
        2018: 'https://www.gov.il/BlobFolder/policy/tableau/he/tableau_BudgetData2018.xlsx',
        2017: 'https://www.gov.il/BlobFolder/policy/tableau/he/tableau_BudgetData2017.xlsx',
        2016: 'https://www.gov.il/BlobFolder/policy/tableau/he/tableau_BudgetData2016.xlsx',
        2015: 'https://www.gov.il/BlobFolder/policy/tableau/he/tableau_BudgetData2015.xlsx'
    }
    # url20241 = 'before0710original2024.xlsx'

    # Access the URL using the year
    url = urls.get(year)  # Get the URL based on the provided year
    if url:
        response = requests.get(url)

        if response.status_code == 200:
            # Wrap the byte string in a BytesIO object
            excel_buffer = BytesIO(response.content)
            # Make dataframe
            df = pd.read_excel(excel_buffer)
            # Getting MOPS data
            org_dict = organization_codes()
            if organization == 'total':
                if budget == 'total':
                    df = df[df.iloc[:, 4] == 12]
                elif budget == 'wages':
                    df = df[(df.iloc[:, 4] == 12) & (df.iloc[:, 21] == 1)]
                elif budget == 'other':
                    df = df[(df.iloc[:, 4] == 12) & (df.iloc[:, 21] != 1)]

            else :
                if budget == 'total':
                    df = df[(df.iloc[:, 4] == 12) & (df.iloc[:, 12].isin(org_dict[organization]))]
                elif budget == 'wages':
                    df = df[(df.iloc[:, 4] == 12) & (df.iloc[:, 12].isin(org_dict[organization])) &
                            (df.iloc[:, 21] == 1)]
                elif budget == 'other':
                    df = df[(df.iloc[:, 4] == 12) & (df.iloc[:, 12].isin(org_dict[organization])) &
                            (df.iloc[:, 21] != 1)]
            return df


def get_annual_total(df, organization, budget):
    budget_dict = budget_types()

    year = df.iloc[0, 0]
    # Filter DataFrames for original, approved, and executed budget types
    df_original = df[
        df.iloc[:, 29] == budget_dict['original']].copy()  # Use .copy() to avoid SettingWithCopyWarning
    df_approved = df[df.iloc[:, 29] == budget_dict['approved']].copy()
    df_executed = df[df.iloc[:, 29] == budget_dict['executed']].copy()

    original_budget = df_original.iloc[:, 30].sum()
    approved_budget = df_approved.iloc[:, 30].sum()
    executed_budget = df_executed.iloc[:, 30].sum()

    original_manpower = df_original.iloc[:, 34].sum() + (df_original.iloc[:, 35].sum() / 12)
    approved_manpower = df_approved.iloc[:, 34].sum() + (df_approved.iloc[:, 35].sum() / 12)
    executed_manpower = df_executed.iloc[:, 34].sum() + (df_executed.iloc[:, 35].sum() / 12)

    temp_dict = {
        'organization': organization,
        'budget': budget,
        'year': year,
        'original_budget': original_budget,
        'approved_budget': approved_budget,
        'executed_budget': executed_budget,
        'original_manpower': original_manpower,
        'approved_manpower': approved_manpower,
        'executed_manpower': executed_manpower,
    }

    # Convert NumPy float64 and int64 to Python float and int
    final_dict = {key: float(value) if isinstance(value, np.float64) else int(value) if isinstance(value, np.int64) else value
                  for key, value in temp_dict.items()}

    return final_dict


def drop_columns(df):
    columns_to_drop = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 20,
                       21, 22, 23, 24, 25, 26, 27, 28, 29, 31, 32, 33, 34, 35, 36, 37]
    df = df.drop(df.columns[columns_to_drop], axis=1)
    return df


def get_takanot(df):
    budget_dict = budget_types()

    year = df.iloc[0, 0]
    # Filter DataFrames for original, approved, and executed budget types
    df_original = df[
        df.iloc[:, 29] == budget_dict['original']].copy()  # Use .copy() to avoid SettingWithCopyWarning
    df_original = drop_columns(df_original)
    df_original = df_original.rename(columns={'הוצאה נטו': 'original'})

    df_approved = df[df.iloc[:, 29] == budget_dict['approved']].copy()
    df_approved = drop_columns(df_approved)
    df_approved = df_approved.rename(columns={'הוצאה נטו': 'approved'})

    df_executed = df[df.iloc[:, 29] == budget_dict['executed']].copy()
    df_executed = drop_columns(df_executed)
    df_executed = df_executed.rename(columns={'הוצאה נטו': 'executed'})

    df = df_original.merge(df_approved[['קוד תקנה', 'approved']], on='קוד תקנה', how='outer')
    df = df.merge(df_executed[['קוד תקנה', 'executed']], on='קוד תקנה', how='outer')

    df = df.rename(columns={
        'שנה': 'year',
        'קוד תקנה': 'code',
        'שם תקנה': 'name'
    })

    for x in range(0, len(df), 50):
        y = x + 50
        print(x, y)
        df_temp = df[x:y]
        df_json = df_temp.to_json(orient='records', force_ascii=False)
        json_obj = json.loads(df_json)
        takanot_request(json_obj)






