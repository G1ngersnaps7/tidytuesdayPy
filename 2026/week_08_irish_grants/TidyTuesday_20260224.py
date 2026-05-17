# TidyTuesday week 8 - February 24, 2026
# Science Foundation Ireland Grants Commitments

# Goal: to make a Sankey chart to show where the total 
# grant amount from the Ireland Science foundation has been distributed 
# by research body (the top ones)

# --1. libraries ------
import pandas as pd
import plotly.graph_objects as go #for sankey diagrams

# --2. read in TT data for week 8 ---
sfi_grants_raw = pd.read_csv('https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2026/2026-02-24/sfi_grants.csv')

sfi_grants = sfi_grants_raw.copy()

# --3. Create tidy df for plotting -----
sfi_grants = sfi_grants[['funder_name','research_body','current_total_commitment']]

# total grant amount awarded
grant_total = sfi_grants['current_total_commitment'].sum()

# add up the total received grants by resarch body
sfi_totals = (
    sfi_grants
    .groupby(['research_body'])['current_total_commitment']
    .sum()
    .sort_values(ascending=False)
    .reset_index() 
)

# keep the top 10 research bodies by grant total separately
# and group the smaller ones into a single category and total

#top 10 and others grouped
top10 = sfi_totals.head(10)
others = pd.DataFrame({
    'research_body': ['Others combined'],
    'current_total_commitment':sfi_totals.loc[10:]['current_total_commitment'].sum()
})

#concat into one df
totals = pd.concat([top10, others]).reset_index(drop=True)
# add the funder col back in
totals['funder_name'] = 'Science Foundation Ireland'
