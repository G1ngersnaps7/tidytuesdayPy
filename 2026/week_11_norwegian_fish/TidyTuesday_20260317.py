# TidyTuesday week 11 - March 17, 2026
## Salmonid Mortality Data 

# Question: Have any Norwegian counties seen a change in fish mortality trends?

# -- 1. Libraries ----
#from inspect import CO_VARKEYWORDS
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm      

# --2. Load TT data for week 11 ----
mort = pd.read_csv('https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2026/2026-03-17/monthly_mortality_data.csv')

# convert date to datetime
mort['date']=pd.to_datetime(mort['date'])

# create salmon-county df
sc = mort[(mort['geo_group']=='county') & (mort['species']=='salmon')].copy()


# --3. Fit linear region trend to a region to test --------
def get_trend(g):
    """Fit median ~ time for one region, return the fitted model.
    Newey-West (HAC) correction applied for potential month
    to month auto-correlation."""
    g = g.sort_values('date').copy()
    g['month_num'] = range(len(g))
    return smf.ols('median ~ month_num', data=g).fit(
        cov_type='HAC', cov_kwds={'maxlags': 4})

# one model per county, stored in a dict by region name
models = {region: get_trend(g) for region, g in sc.groupby('region')}

# set up the results summary df from each model (slope, p, and r^2)
results = pd.DataFrame({
    region: {
        'slope_yr': m.params['month_num'] * 12,
        'p': m.pvalues['month_num'],
        'r2': m.rsquared,
    }
    for region, m in models.items()
}).T.sort_values('slope_yr') # make region row instead of col


# --5. Make plots ------------------------------

# figure axes parameters (2 plots)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

## ---5.a. Plot 1 - bar chart showing slope (% change) by county, color
## coded by direction and significance ----------------------

# set custom bar colors based on slope/significance (p value)

# colours
inc = '#FF7E70' # positive slope with p<0.05
dec = '#BD685E' # negative slope, p<0.05
none = '#999999' # no change

# assign bar color based on slope or p value 
def bar_colors(slope, p):
    if p > 0.05:
        return none 
    return inc if slope > 0 else dec

# apply colors using bar_color fx - returning a list 
colors = [bar_colors(slope, p) for slope, p in zip(results['slope_yr'], results['p'])]
# add the horizontal bars with bar colors 
bars = ax1.barh(y=results.index, width=results['slope_yr'], color=colors)
# add the vertical zero line 
ax1.axvline(x=0, color='black', linewidth=0.8)
# add significance labels 
star_labels = ['*' if p<0.05 else '' for p in results['p']]
ax1.bar_label(bars, labels=star_labels, padding=4, fontsize=16, fontweight='bold')
# axes and plot titles
ax1.set_xlabel('Mortality trend (% points / year)')
ax1.set_title('A. Salmon mortality trend by county', fontweight='bold', loc='left')
ax1.grid(axis='x', alpha=0.25)

## ---5.b. Plot 2 - showing the trends over time (scatter) --------------------

# set colors for the two countries with significant trend 
sig_counties = {'Møre og Romsdal': '#E07A5F', 'Trøndelag': '#B5503A'}

# look up region, color and 
for region, color in sig_counties.items():
    g = sc[sc['region'] == region].sort_values('date').copy()
    g['month_num'] = range(len(g))
    m = models[region]            # <-- reuse, no refit

    ax2.scatter(g['date'], g['median'], color=color, s=20, alpha=0.45)
    slope_yr = m.params['month_num'] * 12
    ax2.plot(g['date'], m.fittedvalues, color=color, lw=2.6,
             label=f'{region} ({slope_yr:+.3f}/yr)')

# add titles
# axes and plot titles
ax2.set_ylabel('Mortality monthly mortality %')
ax2.set_xlabel("Year")
ax2.set_title('B. The two significant counties are rising', fontweight='bold', loc='left')
ax2.legend(frameon=True)
ax2.grid(alpha=0.25)

# full figure title
fig.suptitle('Norwegian salmon mortality trends diverge by county (2020–2025)',
             fontsize=14, fontweight='bold', y=0.99)
fig.text(0.5, 0.925,
         'In Møre og Romsdal and Trøndelag, the typical farm\u2019s monthly mortality '
         'has risen steadily from 2020\u20132025, though individual months vary widely',
         ha='center', fontsize=10.5, color='#555555')

# add the tidutuesday tag on the bottom
fig.text(0.99, 0.01, '#PydyTuesday \u2014 2026 Week 11',
         ha='right', fontsize=8, color='grey', style='italic')

plt.tight_layout(rect=[0, 0.03, 1, 0.9])

plt.savefig('2026/week_11_norwegian_fish/plots/norway_county_fish.png', dpi=300, bbox_inches="tight")