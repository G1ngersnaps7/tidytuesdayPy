# Tidytuesday 2026-01-20: NASA APOD 

# looking for the most commonly written about concepts by NASA
# using natural language processing 

import pandas as pd
import matplotlib.pyplot as plt
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from collections import Counter # to count text token occurences

# -- 1. Get data --
apod_raw = pd.read_csv('https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2026/2026-01-20/apod.csv')

apod = apod_raw.copy()

# make date column datetime class
apod['date'] = pd.to_datetime(apod['date'])
year_min = apod['date'].dt.year.min()
year_max = apod['date'].dt.year.max()

# -- 2. explore the data a bit --
print(apod.shape)
print(apod.dtypes)
print(apod.head())

print(apod['explanation'].iloc[0]) # peek at an entry

# -- 3. Analyze explanation text -- 
apod_clean = apod.dropna(subset=['explanation'])

# pull all the explanation text into one list
all_text = ' '.join(apod_clean['explanation'].tolist())

# convert all to lowercase and remove any non alphabet characters to 
# explanation text 
# py list comprehension - new learning concept: in general, 
# Create a new list by doing [this action] 
# to [every item] in this [old list] 
# if [a condition is met]
tokens = [
    word.lower() 
    for word in word_tokenize(all_text) 
    if word.lower().isalpha()
]

# get the english stop words set (to store unique words)
stop_words = set(stopwords.words('english'))

# Remove stop words from the tokens list
tokens = [word for word in tokens if word not in stop_words]

# use the nltk lemmatizer to reduce words to their base form (lemma)
lemmatizer = WordNetLemmatizer()
tokens = [lemmatizer.lemmatize(word) for word in tokens]

# dictionary: collapse very similar concepts into one for data visual
replacements = {
    'solar': 'sun', 
    'lunar': 'moon'
}

# replace in the token list
tokens = [replacements.get(word, word) for word in tokens]

# count how often each word appears - into dictionary
word_counts = Counter(tokens)

# -- 4. Convert back to pd df for filtering --
# to be able to do more filtering on tokens
df_words = pd.DataFrame(
    word_counts.most_common(), #sort most common desc
    columns = ['word', 'count']
) 

# -- 5. add custom stop words and filter out -- 
# look at the top 50 most common words and create custom stop words
# might need to do a few passes with custom stops to get a solid eventual top 20
print(df_words.head(50))

# create custom stop set to filter out of df 
custom_stops = {'image', 'near', 'years', 'known', 'one',
'seen', 'way', 'right', 'away', 'across', 'also',
'visible', 'years', 'seen', 'way', 'center', 'left', 'images',
'toward', 'view', 'taken', 'two', 'featured', 'large', 'year', 
'region', 'time', 'million', 'lie', 'show', 'captured', 
'central', 'small', 'last', 'like', 'color'}

# filter out (~) the custom stops from words
df_words = df_words[~df_words['word'].isin(custom_stops)]

# do some checking to ensure the top 20 words are meaningful before
# and ensure custom-stop set is good ahove 
# subsetting df to top 20 
df_top20 = df_words.head(20).copy()

# ensure df is sorted by count 
df_top20 = df_top20.sort_values('count', ascending=False)

# -- 6. make a horizontal lollipop plot --
fig, ax = plt.subplots()

# add hline (stem)
ax.hlines(df_top20['word'], xmin=0, xmax=df_top20['count'])
ax.scatter(df_top20['count'], df_top20['word'], color='blue', alpha=1)

# axis titles
ax.set_xlabel('Number of occurences')
ax.set_title(f"Top 20 most common concepts in NASA Astronomy Picture of the Day\n({year_min} to {year_max})", fontsize = 12)

plt.savefig('2026/week_03_nasa_apod/plots/apod_top20_concepts.png', 
            dpi=150, bbox_inches='tight')



