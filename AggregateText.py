from bs4 import BeautifulSoup
import re
import nltk
from nltk.corpus import stopwords
import ConstantStrings as cs
import unicodecsv as csv
import traceback
import os
from nltk import word_tokenize
import connectDB as cdb

tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

def content_to_wordlist(sentence, remove_stopwords=False, remove_non_words = False):
    # 1. Optionally remove non-letters
    # 2. Tokenize sentence into terms and remove terms that are only made of characters
    # 3. Optionally remove stop words (false by default)
    # 4. Return the list of words
    if remove_non_words:
        sentence = re.sub("[^a-zA-Z]"," ", sentence)
    words = word_tokenize(sentence)
    words = [re.sub('^\W+$', '', e) for e in words]
    words = [s for s in words if s]
    if remove_stopwords:
        stops = set(stopwords.words("english"))
        words = [w for w in words if not w in stops]
    return(words)

def content_to_sentences( html_content, tokenizer, remove_stopwords=False, remove_non_words = False ):
    # 1. Decode HTML content
    # 2. Parse content to remove tags (i.e. extract required text)
    # 3. Use the NLTK tokenizer to split the paragraph into sentences
    # 4. Loop over each sentence - call convert_to_wordlist
    # 5. Return the list of sentences (each sentence is a list of words, so this returns a list of lists)
    html_content = html_content.strip().decode('iso8859_2')
    text = BeautifulSoup(html_content).get_text()
    try:
        raw_sentences = tokenizer.tokenize(text)
    except UnicodeDecodeError:
        traceback.print_exc()
        print html_content.strip()
    sentences = []
    for raw_sentence in raw_sentences:
        if len(raw_sentence) > 0:
            sentences.append(content_to_wordlist(raw_sentence, remove_stopwords, remove_non_words))
    return sentences

def aggregateTheText(date,data):
    # 1. Aggregate the text from each case in time period into entiretext - in the form of list of lists
    # 2. Write the aggregated entireText into a csv file
    print "Pre-processing and aggregating.."
    entireText = []
    i = 0
    for text in data:
        entireText+= content_to_sentences(text,tokenizer)
        i+=1
        if i%100:
            print "i: ",i
    print "Writing aggregated into .csv file.."
    f = open(os.path.join(cs.path_aggr_five,date+cs.postfix_aggr_five), "wb")
    writer = csv.writer(f)
    writer.writerows(entireText)
    print "Written file."
    f.close()

if __name__ == '__main__':
    # Call options:
    # 1. python AggregateText.py 1950-01-01 1955-01-01
    # 2. python AggregateText.py 1950-01-01 1955-01-01
    if len(sys.argv)>1:
        date = sys.argv[1]
        period = sys.argv[3]
        date2 = sys.argv[2]
        print "Arguments given: ",date,period,date2
        db = cdb.connect()
        allCases = cdb.extractCases(db,date,date2)
        at.aggregateTheText(date,allCases)

    else:
        print "Wrong number of arguments.\npython mainTopicChange.py date1 date2"
