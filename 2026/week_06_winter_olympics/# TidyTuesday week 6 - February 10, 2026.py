# TidyTuesday week 6 - February 10, 2026
# Winter Olympics
# create an at a glance chart for disciples and days for medal events

# --1. libraries --
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np

# --2. Get Data --
olympic_raw = pd.read_csv('https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2026/2026-02-10/schedule.csv')
olympic = olympic_raw.copy()

# --3. Prep data --

# remove the training sessions
olympic= olympic[olympic['is_training'] == False]

# create a column for if a discipline has a medal event or not 
# on a given day 
day_types = (
    olympic
    .groupby(['discipline_name', 'date'])['is_medal_event']
    .any()
    .reset_index()
    .rename(columns={'is_medal_event':'has_medal_event'})
)