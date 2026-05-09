# TidyTuesday 2026 Week 4: Edible Plants

# Plan: What plants are 'least demanding' overall to grow - for the 
# green-thumb challenged people. 

# -- 1. Load libraries --
import pandas as pd
import numpy as np
from great_tables import GT, style, loc, md # tables
import emoji 

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
    'full sun/partial shade':'Full sun/partial shade',
    'partial shade': 'Partial shade',
    'full sun/partial shade/full shade':'Full sun/partial shade',
    'full sun/partial shade/ full shade': 'Full sun/partial shade',
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
    'low': 1
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
# add water, nutrient, and hardiness scores. 
# Calculate overall ease_score (water+hard+ph+nutrient scores)
edible_plants_scored = (
    edible_plants
    .assign(ph_range = lambda x: x.preferred_ph_upper - x.preferred_ph_lower)
    .assign(ph_score = lambda x: x.ph_range.apply(ph_score))
    .assign(sun_clean = lambda x: x.sunlight.map(sunlight_grps))
    .assign(hard_score = lambda x: x.temperature_class.map(hardiness_grps))
    .assign(nutrient_score = lambda x: x.nutrients.map(nutrient_grps))
    .assign(water_score = lambda x: x.water.map(water_grps))
    .assign(ease_score = lambda x: x[['ph_score', 'water_score', 'nutrient_score', 'hard_score']].sum(axis=1))
)

# 3.f. table df with top scoring plants per sun category 
edible_plants_tbl = (
    edible_plants_scored
    .sort_values('ease_score', ascending=False)
    .groupby('sun_clean', group_keys=False)
    .head(10)
    .reset_index(drop=True)
    .filter(items=['common_name', 'sun_clean', 'ph_score', 
    'water_score', 'nutrient_score', 'hard_score', 'ease_score'])
)

# 3.g. Add emojis for the sunlight categories
sun_emojis = {
    'Full sun': emoji.emojize(':sun:') + 'Full sun',
    'Full sun/partial shade': emoji.emojize(':sun_behind_small_cloud:') + ' Full sun/partial shade', 
    'Partial shade': emoji.emojize(':sun_behind_large_cloud:') + ' Partial shade'
}

edible_plants_tbl['sun_clean']=edible_plants_tbl['sun_clean'].map(sun_emojis)

# --4. Visualize top plants by sunlight category in a pretty table

tbl = (
    GT(edible_plants_tbl, 
    rowname_col='common_name',
    groupname_col='sun_clean')
    .tab_header(
        title=md("**Easiest plants to grow by sunlight need**"), 
        subtitle="Plants scored 0–1 on water needs, hardiness, pH tolerance, and nutrient needs — higher is easier to grow.")
    .cols_label(
        common_name = 'Plant', 
        ph_score = 'pH Score', 
        water_score = 'Water score', 
        nutrient_score = 'Nutrient score', 
        hard_score = 'Hardiness score', 
        ease_score = 'Easiness score'
        )
    # style
    .opt_row_striping() # zebra striping
    .tab_style(
        style=style.text(weight="bold"),
        locations=loc.row_groups()
    )
    .tab_style(
    style=style.text(weight="bold", color = "green"),
    locations=loc.stub()
    )
    .tab_style(
        style=style.fill(color="#90EE90"),
        locations=loc.body(columns='ease_score')
    )
)



# --5. Save the output table as html
html = tbl.as_raw_html()
html = html.replace('<head>', '<head>\n<meta http-equiv="Content-Type" content="text/html; charset=utf-8">')

with open("2026/week_05_edible_plants/outputs/plant_table.html", "w", encoding="utf-8") as f:
    f.write(html)