# Tidytuesday 2026-01-20: NASA APOD 

# looking for the most commonly written about concepts by NASA
# using natural language processing 

import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from collections import Counter # to count text token occurences

# -- 1. Get data --
apod_raw = pd.read_csv('https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2026/2026-01-20/apod.csv')

apod = apod_raw.copy()

# -- 2. explore the data a bit --
print(apod.shape)
print(apod.dtypes)
print(apod.head())

print(apod['explanation'].isnull().sum()) # look for nulls
print(apod['explanation'].iloc[0]) # peek at an entry

# -- 3. Analyze explanation text -- 
apod_clean = apod.dropna(subset=['explanation'])

# pull all the explanation text into one list
all_text = ' '.join(apod_clean['explanation'].tolist())

# convert all to lowercase and remove any non alphabet characters to 
# explanation text tokens
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

# count how often each word appears
word_counts = Counter(tokens)

# -- 4. Convert back to pd df for filtering --
# to be able to do more filtering on tokens
df_words = pd.DataFrame(
    word_counts.most_common(), #sort most common desc
    columns = ['word', 'count']
) 

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

# do some checking to ensure the top 30 words are meaningful before
# and ensure custom-stop set is good ahove 
# subsetting df to top 30 
df_top30 = df_words.head(30).copy()