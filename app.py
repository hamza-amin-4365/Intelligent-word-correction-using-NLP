# importing main libraries
from flask import Flask, render_template,request
import numpy as np
import pandas as pd
import textdistance
from collections import Counter
import re


app = Flask(__name__)

# File opening and cleaning our txt file
words = []
with open('Oxford English Dictionary.txt', 'r', encoding='utf-8') as f:
    data = f.read().lower()
    words = re.findall('\w+', data)
    words += words


#  Make vocabulary
V = set(words) # gives unique words

#build frequency of all words
words_freq_dict = Counter(words)


# RELATIVE FREQUENCY OF WORDS
# Now we want to get probability of occurance of each word, this equals relative frequency
# the formula is:
# probability(word) = Frequency(word)/Total words
total_words_freq = sum(words_freq_dict.values()) # sum of all total words
probs = {}
for k in words_freq_dict.keys():
  probs[k] = words_freq_dict[k] / total_words_freq


@app.route('/')
def index():
    return render_template('index.html', suggestions=None)


# FINDING SIMILAR WORDS
# Now we will sort similar words according to Jaccard distance fr by calculating 2 grams Q of the words. 
# Next, we will return 5 most similar words ordered by similarity and probability.
# Jaccard distance measures the dissimilarity b/w two sets by comparing their intersection and union 
@app.route('/suggest', methods=['POST'])
def suggest():
    keyword = request.form['keyword'].lower()
    if keyword:
        similarities = [1 - textdistance.Jaccard(qval=2).distance(v, keyword) for v in words_freq_dict.keys()]
        df = pd.DataFrame.from_dict(probs, orient='index').reset_index()
        df.columns = ['Word', 'Prob']
        df['Similarity'] = similarities
         # Filter words with similarity greater than 0
        df = df[df['Similarity'] > 0]
        suggestions = df.sort_values(['Similarity', 'Prob'], ascending=False)[['Word', 'Similarity']]
        suggestions_list = suggestions.to_dict('records')  # Convert DataFrame to list of dictionaries
        return render_template('index.html', suggestions=suggestions_list)

if __name__ == '__main__':
    app.run(debug=True)