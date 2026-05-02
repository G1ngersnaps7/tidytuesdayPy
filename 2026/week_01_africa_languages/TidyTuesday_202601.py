import pandas as pd

# Read directly from GitHub and assign to an object
df_raw = pd.read_csv('https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2026/2026-01-13/africa.csv')

# working df 
df = df_raw.copy()

#explore data
# Get a quick overview
print(df.shape)       # (rows, columns)
print(df.dtypes)      # column data types
print(df.head())

# Get several cutpoints 
cutpoints = df['native_speakers'].quantile([0.25, 0.50, 0.75, 0.90, 0.95])

# assign categories to the cutpoint
def speaker_tier(n):        
    if n >= cutpoints[0.90]:
        return 'major'
    elif n >= cutpoints[0.50]:
        return 'mid'
    else:
        return 'small'

# add the percentile cateogry to the df
df['tier'] = df['native_speakers'].apply(speaker_tier)  


