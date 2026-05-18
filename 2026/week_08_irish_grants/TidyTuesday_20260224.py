# TidyTuesday week 8 - February 24, 2026
# Science Foundation Ireland Grants Commitments

# Goal: to make a Sankey chart to show where the total 
# grant amount from the Ireland Science foundation has been distributed 
# by research body (the top ones)

# --- 1. libraries ------
import pandas as pd
import plotly.graph_objects as go #for sankey diagrams

# --2. read in TT data for week 8 ---
sfi_grants_raw = pd.read_csv('https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2026/2026-02-24/sfi_grants.csv')

sfi_grants = sfi_grants_raw.copy()

# --- 3. Create tidy df for plotting -----
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

# --- 4. Create the sankey diagram using plotly -----

grant_total=totals['current_total_commitment'].sum()

# create the plot labels
source_label = f"Science Foundation Ireland<br>€{grant_total/1e9:.2f}B"
target_labels = [
    f"{row['research_body']}<br>€{row['current_total_commitment']/1e6:.0f}M"
    for _, row in totals.iterrows()
]
labels = [source_label]+target_labels

# links: all flow from node 0 to each research body node
sources = [0] * len(totals)
targets = list(range(1, len(totals) + 1))
values = totals["current_total_commitment"].tolist()

#plotly Sankey 
fig = go.Figure(data=go.Sankey(
    node = dict(
        label=labels, 
        pad=30, 
        thickness=20, 
        color=["#06402B"] + ["#1D9E75"] * (len(totals) - 1) + ["#B4B2A9"],
    ),
    link = dict(
        source=sources, 
        target=targets, 
        value=values, 
        color="rgba(136, 231, 136, 0.49)",
    ),
))

# add a title
fig.update_layout(title_text="Science Foundation Ireland - grant commitments by insitution (2001-2024)",
 font_size=12)

#save the plot as png. 
# note there appears to be an issue with the latest version of 
#plotly and kaleido when saving static images. 
# had to use versions: plotly==5.24.0 kaleido==0.2.1
fig.write_image("2026/week_08_irish_grants/plots/sfi_sankey.png")
