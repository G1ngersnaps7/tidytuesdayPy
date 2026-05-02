import pandas as pd

# Read directly from GitHub and assign to an object
df = pd.read_csv('https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2026/2026-01-13/africa.csv')

#explore data
# Get a quick overview
print(df.shape)       # (rows, columns)
print(df.dtypes)      # column data types
print(df.head())