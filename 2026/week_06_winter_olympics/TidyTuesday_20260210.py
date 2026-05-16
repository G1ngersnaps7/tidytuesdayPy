# TidyTuesday week 6 - February 10, 2026
# Winter Olympics
# create an at a glance chart for disciples and days for medal events

# --1. libraries --
import pandas as pd
#import numpy as np
import matplotlib.pyplot as plt
#import matplotlib.dates as mdates
#import matplotlib.font_manager as fm
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from datetime import date

# --2. Get Data --
olympic_raw = pd.read_csv('https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2026/2026-02-10/schedule.csv')
olympic = olympic_raw.copy()

# --3. Prep data --------------------------------

# remove the training sessions
olympic= olympic[olympic['is_training'] == False]

# use local event end_datetime for event date
olympic['end_datetime_local'] = pd.to_datetime(olympic['end_datetime_local']).dt.date

# create a column for if a discipline has a medal event or not 
# on a given day 
day_types = (
    olympic
    .groupby(['discipline_name', 'end_datetime_local'])['is_medal_event']
    .any()
    .reset_index()
    .rename(columns={'is_medal_event':'has_medal_event'})
)

# --4. Create plot to show schedule ----------------
# disciplines
disciplines = sorted(day_types['discipline_name'].unique())
# unique dates
dates = sorted(day_types['end_datetime_local'].unique())

# create the figure and axes
fig, ax = plt.subplots()

# fontface for plot
plt.rcParams['font.family'] = 'Osaka'

# add the February xaxis title top left
ax.text(-1.5, -1.5, 'February', 
        transform=ax.transData,
        fontsize=12, fontweight='bold',
        ha='right', va='center')

# create x-axis ticks (each day of Olympics and labels)
# and put on top of plot
xlabs = [d.strftime('%d') for d in dates]
ax.set_xticks(range(len(dates)), labels=xlabs)
ax.tick_params(axis='x', top=True, labeltop=True, bottom=False, labelbottom=False)
ax.set_xlim(-1, len(dates))

# set yaxis labels and have white space at edges
ax.set_yticks(range(len(disciplines)), labels=disciplines)
ax.set_ylim(len(disciplines), -1)

# plot title
ax.set_title(
    "Milano Cortina 2026 Winter Olympics Schedule", 
    pad=10, 
    fontdict={'fontweight': 'bold', 'fontsize': 14})

# read in the custom emojis to use in the plot
medal_img = plt.imread('2026/week_06_winter_olympics/images/medal.png')
square_img = plt.imread('2026/week_06_winter_olympics/images/red_square.png')

# create zebra striping (color on even rows)
for i in range(len(disciplines)):
    if i % 2 == 0: 
        ax.axhspan(i - 0.5, i + 0.5, color='lightgrey', alpha=0.3, zorder=0)

# add the correct emoji icon for event event by medal or not medal event 
for _, row in day_types.iterrows():
    x = dates.index(row['end_datetime_local'])
    y = disciplines.index(row['discipline_name'])
    
    img = medal_img if row['has_medal_event'] else square_img
    
    imagebox = OffsetImage(img, zoom=0.05)
    ab = AnnotationBbox(imagebox, (x, y), frameon=False)
    ax.add_artist(ab)

# -- 5. Plot footnote ----------------------------------
# adding foot note with emojis using annotation boxes

# add medal image to footnote
medal_legend = OffsetImage(medal_img, zoom=0.03)
ab_medal = AnnotationBbox(medal_legend, 
                          xy=(0, -0.04),
                          xycoords='axes fraction',
                          frameon=False)
ax.add_artist(ab_medal)

# add text next to medal image
ax.annotate('= medal event day',
            xy=(0.02, -0.04),
            xycoords='axes fraction',
            fontsize=8,
            color='grey',
            va='center')

# add square image to footnote
square_legend = OffsetImage(square_img, zoom=0.03)
ab_square = AnnotationBbox(square_legend,
                           xy=(0.28, -0.04),
                           xycoords='axes fraction',
                           frameon=False)
ax.add_artist(ab_square)

# add text next to square image
ax.annotate('= competition day (no medal)',
            xy=(0.30, -0.04),
            xycoords='axes fraction',
            fontsize=8,
            color='grey',
            va='center')

plt.savefig('2026/week_06_winter_olympics/plots/olympic2026_schedule.png', 
            dpi=150, bbox_inches='tight')