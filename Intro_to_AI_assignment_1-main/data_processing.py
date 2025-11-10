import pandas as pd
import numpy as np

#Concatenate scores files
scores_20 = 'Data/Challenge_1/scores_20.csv'
scores_21 = 'Data/Challenge_1/scores_21.csv'
scores_22 = 'Data/Challenge_1/scores_22.csv'
scores_23 = 'Data/Challenge_1/scores_23.csv'
def concat_scores():
    dfs = []
    dfs.append(pd.read_csv(scores_20))
    dfs.append(pd.read_csv(scores_21))
    dfs.append(pd.read_csv(scores_22))
    dfs.append(pd.read_csv(scores_23))
    data_scores = pd.concat(dfs, ignore_index=True)
    return data_scores

# Load datasets
data_budget = pd.read_excel('Data/Challenge_1/budget_units.xlsx')
data_funnel = pd.read_csv('Data/Challenge_1/transactions.csv')
data_analysis = pd.read_csv('Data/Challenge_1/analytics_data.csv')
data_scores = concat_scores()

# Data Pre-Processing
def pre_processing():
    data = {
        "data_budget": data_budget,
        "data_funnel": data_funnel,
        "data_analysis": data_analysis,
        "data_scores": data_scores,
    }
    for name, df in data.items():
        if df.duplicated().any() or df.isnull().values.any():
            print("\n-----------------------------------\n")
            print(f"Dataset: {name}")
            #print("Data information and description:")
            #f.info()
            #f.describe(include='all')

            print("\nCheck duplicates:")
            print(df.duplicated().sum())

            print("\nCheck missing or null:")
            print(df.isnull().sum())
            print("\nPercentage of missing values:")
            print(df.isnull().mean() * 100)

            print("\n-----------------------------------\n")
        else:
            print(f"\n{name} - No duplicates or missing values found.")
#pre_processing()

#After the pre-processing, we can come to the conclusion to remove 'period_24' from data_budget as it is Null.
data_budget.drop(columns=['period_24'], inplace=True)

#Next: Check that data types, date format, trip names match across datasets.
