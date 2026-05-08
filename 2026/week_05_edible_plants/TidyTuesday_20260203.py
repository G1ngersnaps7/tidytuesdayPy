# TidyTuesday 2026 Week 4: Edible Plants

# Plan: What plants are 'least demanding' overall to grow - for the 
# green-thumb challenged people. 

# -- 1. Load libraries --
import pandas as pd
import numpy as np

# -- 2. Get TT data from GitHub --
edible_plants_raw = pd.read_csv('https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2026/2026-02-03/edible_plants.csv')

edible_plants = edible_plants_raw.copy()

# -- 3. Explore data and create a "easiness score" based on:
# water needs 
# ph range 
# hardiness
# nutrient needs 
# and group by sunlight requirements 

# convert needed cols to lowercase to standardize 
to_lower = ['sunlight', 'water', 'temperature_class', 'nutrients']
for col in to_lower:
    edible_plants[col] = edible_plants[col].str.lower()

# 3.a. create sunlight groups (collapse sparse into 3 major)
sunlight_grps = {
    'full sun':'Full sun', 
    'full sun/partial shade':'full sun/partial shade',
    'partial shade': 'partial shade',
    'full sun/partial shade/full shade':'full sun/partial shade',
    'full sun/partial shade/ full shade': 'full sun/partial shade',
}

# 3.b. create water grouping (collapse a few) and create scoring 
# high number = low watering 
water_grps = {
    'high':0, 'very high':0, 
    'medium':0.5,
    'low':1.0, 'very low':1.0
}
# 3.c. create hardiness scores (higher score is easier)
hardiness_grps = {
    'very tender':0, 
    'tender':0.25,
    'half hardy':0.5,
    'hardy':0.75, 
    'very hard':1, 'very hardy':1
}

# 3.d. create the nutrient scores
nutrient_grps = {
    'high': 0, 
    'high potassium fertilizer every 2 weeks': 0, 
    'medium': 0.5, 
    'medium to high': 0.5, 
    'low': 0
}

# 3.d. create a ph range score (wider range is easier)
def ph_score(val):
    if pd.isnull(val): 
        return(np.nan)
    if val < 1: 
        return(0)
    elif val <= 2: 
        return(0.5)
    else: 
        return 1

# 3.e. calculate the ph range max values, assing ph score, 
# add water and hardiness scores. 
# Calculate overall ease_score (water+hard+ph scores)
# keep needed cols for plot
edible_plants_plot = (
    edible_plants
    .assign(ph_range = lambda x: x.preferred_ph_upper - x.preferred_ph_lower)
    .assign(ph_score = lambda x: x.ph_range.apply(ph_score))
    .assign(sun_clean = lambda x: x.sunlight.map(sunlight_grps))
    .assign(hard_score = lambda x: x.temperature_class.map(hardiness_grps))
    .assign(nutrient_score = lambda x: x.nutrients.map(nutrient_grps))
    .assign(water_score = lambda x: x.water.map(water_grps))
    .assign(ease_score = lambda x: x[['ph_score', 'water_score', 'nutrient_score', 'hard_score']].sum(axis=1))
    .filter(items=['common_name', 'sun_clean', 'ph_score', 
    'water_score', 'nutrient_score', 'hard_score', 'ease_score'])
)


