import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# -- 1. Get the data --
# Read directly from GitHub for 2026-01
df_raw = pd.read_csv('https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2026/2026-01-13/africa.csv')

# working df 
df = df_raw.copy()

# -- 2. look at it --
# Get a quick overview
print(df.shape)       # (rows, columns)
print(df.dtypes)      # column data types
print(df.head())

# -- 3. Create language groupings by quantiles -- 
# Create quantile breakpoints
breakpoints = df['native_speakers'].quantile([0.25, 0.50, 0.90])

# assign categories to the breakpoint
def speaker_tier(n):        
    if n >= breakpoints[0.90]:
        return 'major (90pct)'
    elif n >= breakpoints[0.50]:
        return 'mid (50-89pct)'
    else:
        return 'small (50pct)'

# add the quantile category to the df
df['tier'] = df['native_speakers'].apply(speaker_tier) 

# ensure only one row per language (i.e. drop country dupes)
df = df.drop_duplicates('language')

# log transform that native speaker values (since data is 
# right-skewed)
df['log_speakers'] = np.log10(df['native_speakers'])

# -- 4. Assign colors --
tier_colours = {
    'small (50pct)': '#F67E7D',
    'mid (50-89pct)':   '#843B62',
    'major (90pct)': '#0B032D',
}

# -- 3: set up the figure --
fig, ax = plt.subplots(figsize=(10, 6))

# -- 4. Create plot --
sns.histplot(
    data = df,
    x ='log_speakers',
    hue='tier',
    palette=tier_colours,   # pass the dictionary directly
    bins = 20,
    multiple='stack', 
    ax = ax
)

# -- 5: fix the x axis labels --
# we want to show the real numbers (1k, 10k, 100k...) instead of log vals
ax.set_xticks([2, 3, 4, 5, 6, 7, 8])
ax.set_xticklabels(['100', '1k', '10k', '100k', '1M', '10M', '100M'])

# -- 6: labels and legend --
ax.set_xlabel('Native speakers (log scale)', fontsize=12)
ax.set_ylabel('Number of languages', fontsize=12)
ax.set_title('Distribution of African languages by native speaker count', fontsize=14)

plt.tight_layout()
plt.savefig('plots/africa_languages_histogram.png', dpi=150, bbox_inches='tight')

