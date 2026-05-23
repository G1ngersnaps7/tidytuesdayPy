# TidyTuesday week 9 - March 03, 2026
# Golem Grad Island Tortoises

# Question: Does body condition differ between sexes, 
# and does that difference vary by locality? Has proportion of m/f 
# changed by locality over time? 

# --- 1. libraries ------
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# --2. read in TT data for week 9 ---
clutch_size_cleaned = pd.read_csv('https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2026/2026-03-03/clutch_size_cleaned.csv')
tortoise_body_condition_cleaned = pd.read_csv('https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2026/2026-03-03/tortoise_body_condition_cleaned.csv')

clutch = clutch_size_cleaned.copy()
condition = tortoise_body_condition_cleaned.copy()

# --3. wrangle data ---

#get individual tortoise body condition index mean values (since 
# some have repeated measures)
individual_means = (
    condition
    .groupby(['individual', 'sex', 'locality'])['body_condition_index']
    .mean()
    .reset_index()
)

# get sex proportions to show changes over time by locality. 
# get sex counts by year and locality
sex_counts = (
    condition
    .groupby(["year", "locality", "sex"])
    .size()
    .reset_index(name="count")
)

# calculate proportions by sex, locality and year
sex_props = (
    sex_counts
    .pivot_table(
        index=["year", "locality"], 
        columns="sex", 
        values="count", 
        fill_value=0
    )
    .reset_index()
)

# add proportion (as %) of females col
sex_props["prop_female"] = sex_props["f"] / (sex_props["f"] + sex_props["m"]) * 100

# --4. Plotting set-up ---

# locality orders
locality_order = ['Beach', 'Plateau', 'Konjsko']

#locality cols 
locality_colors = {
    'Beach': '#CBBD93', #sandy color
    'Plateau': '#BC815F', #earthy brown
    'Konjsko': '#276221' #plant green
}
# sex cols 
sex_colors = {
    'f': '#B7410E',
    'm': '658B38'
}

#plot theme
sns.set_style('whitegrid')

# --5. Plots ----

# set up 2-plot figure 
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10))

# plot 1 (ax1)

sns.lineplot(
    data=sex_props, 
    x = 'year', 
    y = 'prop_female', 
    hue = 'locality',
    hue_order = locality_order,
    palette = locality_colors, 
    linewidth=2,
    ax = ax1
)
