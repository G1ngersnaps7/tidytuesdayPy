# Tidytuesday 2026-01-20: NASA APOD 

# looking for the most commonly written about concepts by NASA
# using natural language processing 

import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# 1. Get data
apod_raw = pd.read_csv('https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2026/2026-01-20/apod.csv')

apod = apod_raw.copy()

# -- explore the data a bit --
print(apod.shape)
print(apod.dtypes)
print(apod.head())

print(apod['explanation'].isnull().sum()) # look for nulls
print(apod['explanation'].iloc[0]) # peek at an entry

