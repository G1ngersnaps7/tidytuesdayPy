# week 4 Tidy Tuesday - 2026-01-27
# Brazilian Companies - looking at business legal nature by captial stock

# libraries
from itertools import count
import pandas as pd 

# 1. Read directly from GitHub
companies_raw = pd.read_csv('https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2026/2026-01-27/companies.csv')

companies = companies_raw.copy()

# 2. calculate total capital stock, median stock 
summary = (
    companies
    .groupby('legal_nature')['capital_stock'] 
    .agg(
        count='count', # count by legal nature
        total_capital='sum', #total capital by legal sype
        median_capital='median' #median capital by legal type
    )
    .reset_index() #keep legal_nature as column 
)