# TidyTuesday week 12 - March 24, 2026
## One Million Digits of Pi 

# Visualize the digits of pi via a pi walk - assign 
#  map each number to a direction representing cardinal 
# and intercardinal directions 
# Inspiration from seeing pi walk visualizations online. 
# References:
# - R-bloggers walkthrough (Venn's 1888 method): https://www.r-bloggers.com/2018/04/approximations-of-pi-a-random-walk-though-the-beauty-of-pi/
# - Aragón Artacho et al. 100 billion digit walk (visual): https://www.gigapan.com/gigapans/106803


# -- 1. Libraries ----
import pandas as pd
import numpy as np

pi_digits = pd.read_csv('https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2026/2026-03-24/pi_digits.csv')

# -- 2. Create directions ----

# 8 angles, 45 degrees apart in radians 
angles = np.linspace(0, 2*np.pi, 8, endpoint=False)

# create an 8 x 2 array with x/y movements
directions = np.column_stack([np.cos(angles), np.sin(angles)])  

# get remainder of each digit after dividing by 8 (to have 8 values to 
# match 8 directions)
digit_directions = pi_digits['digit'] % 8

# look up the actual (x,y) movement for each digit, using digit_directions
# as a row index in directions array to make one x,y step per
# digit in pi, in order
steps = directions[digit_directions]

# take each step and turn them into an array of moves to plot
# the path for the pi walk. Each position is just a sum of all 
# previous positions. 
path = np.cumsum(steps, axis=0) #axis=0 to sum row by row, down each col