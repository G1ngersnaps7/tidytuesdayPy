# week 4 Tidy Tuesday - 2026-01-27
# Brazilian Companies - looking at business legal nature by captial stock

# libraries
# from itertools import count
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt

# -- 1. Read directly from GitHub --
companies_raw = pd.read_csv('https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2026/2026-01-27/companies.csv')

companies = companies_raw.copy()

# -- 2. calculate values --
# calculate count of companies, total and median capital, 
# proportion of total companies and proportion of total capital by legal type
summary = (
    companies
    .groupby('legal_nature')['capital_stock']
    .agg(
        count='count',
        total_capital='sum',
        median_capital='median'
    )
    .reset_index()
    .assign(
        share_of_companies=lambda x: x['count'] / x['count'].sum(),
        share_of_capital=lambda x: x['total_capital'] / x['total_capital'].sum()
    )
)

# create capital concentration ratio by legal nature (share of capital / share of companies)
# to visualize what company types hold more or less capital relative to their share of
# total companies 
summary['capital_concentration_ratio'] = (
    summary['share_of_capital'] / summary['share_of_companies']
)

# keep top 10 
top10 = (
    summary
    .sort_values('capital_concentration_ratio', ascending=False)
    .head(10)
)

# -- 3. Create bar plot --
fig, ax = plt.subplots(figsize=(10, 8))

# horizontal bar
ax.barh(top10['legal_nature'], top10['capital_concentration_ratio'], color='#390099')
# highlight 1 on x (i.e. if a company type makes up same percentage of total 
# companies as it does total capital)
ax.axvline(x=1, color='grey', linestyle='--', linewidth=1)
ax.set_xlabel('Capital concentration ratio')

# title 
ax.set_title("Who holds the most money? Capital concentration by Business Type in Brasil", 
loc = 'left', fontweight = 'bold', fontsize = 12, pad = 45)
# subtitle 
# subtitle positioned within axes
ax.text(0, 1.02, 
        "Capital concentration ratio = share of total capital ÷ share of total companies.\nA ratio of 8 means that business type controls 8x more capital than its prevalence alone would predict.",
        transform=ax.transAxes,
        fontsize=9, color='grey', va='bottom')
# add annotation (arrow pointing to index of 1)
ax.annotate('baseline: capital share = company share', xy=(1,5), xytext=(2, 5.5),
arrowprops=dict(facecolor='blue',shrink=0.05))

plt.savefig('2026/week_04_brazilian_companies/plots/braz_companies_ccr.png', 
            dpi=150, bbox_inches='tight')