import pandas as pd

df = pd.read_csv("data/processed/AAPL.csv")

print(df.shape)
print(df.isnull().sum())