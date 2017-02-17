from bs4 import BeautifulSoup
import re
import nltk
from nltk.corpus import stopwords
import json
import ConstantStrings as cs
import unicodecsv as csv
import traceback
import sys
import os
from nltk import word_tokenize

tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

def content_to_wordlist(sentence, remove_stopwords=False, remove_non_words = False):
    # 1. Remove HTML
    # 2. Optionally remove non-letters
    # 3. Convert words to lower case (CHANGED: NO LOWER CASE) split them
    # 4. Optionally remove stop words (false by default)
    # 5. Return a list of words
    #sentence = BeautifulSoup(sentence).get_text()
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
    # 1. Use the NLTK tokenizer to split the paragraph into sentences
    # 2. Loop over each sentence
    # 3. Return the list of sentences (each sentence is a list of words, so this returns a list of lists
    html_content = html_content.strip().decode('iso8859_2')
    text = BeautifulSoup(html_content).get_text()
    try:
        #import chardet
        #print "Detected: ",chardet.detect(html_content)
        raw_sentences = tokenizer.tokenize(text)
    except UnicodeDecodeError:
        traceback.print_exc()
        print html_content.strip()
        raw_input()
    sentences = []
    for raw_sentence in raw_sentences:
        if len(raw_sentence) > 0:
            sentences.append(content_to_wordlist(raw_sentence, remove_stopwords, remove_non_words))
    return sentences

def aggregateTheText(date,data):
    '''
    # Writes list of list into file.
    filename = date+cs.postfix_json
    print "Filename: ",filename
    fileip = open(filename, "r")
    data = json.load(fileip)
    print "Data obtained."
    '''
    print "Pre-processing and aggregating.."
    entireText = []
    #print "Total: ", len(data.values())
    i = 0
    #for each in data.values():
    for text in data:
        #text = each["text"]
        #text = text.encode('utf-8') # Encodes text to utf-8
        #text = text.decode('string_escape') # Escapes the escape sequences. For eg. makes "\n" a new line
        #text = strip_tags(text)
        #text = text.translate(None, string.punctuation)  # makes !am.y? - amy . Basically removes all punctucation
        #text = text.split()
        entireText+= content_to_sentences(text,tokenizer)
        i+=1
        print "i: ",i
    print "Writing aggregated into .csv file.."
    f = open(os.path.join(cs.path_at_fifty,date+cs.postfix_aggr_fif), "wb")
    writer = csv.writer(f)
    writer.writerows(entireText)
    print "Written file."
    f.close()

def decerror():
    with open('decodeerror.txt','r') as f:
        f.seek(1900)
        m = f.read(5)
        print m
def tempCall():
    with open("tryAT.csv", 'rU') as f:
        #reader = csv.reader(f)
        data = list(list(rec) for rec in csv.reader(f, delimiter=','))
    print data
def readthejson():
    import mmap

    dates = [('2010-01-01',None)]
    p = re.compile('{')
    q = re.compile('}')
    print "inside"
    for d1,d2 in dates:
        with open(d1+'OP.json', 'r+') as f:
            print "Opened file",d1
            data = mmap.mmap(f.fileno(), 0)
            mo = p.findall(data)
            m1 = q.findall(data)
            print '{: ',len(mo),' }: ',len(m1)
if __name__ == '__main__':
    decerror()
    #readthejson()
    #aggregateTheText('1960-01-01')

'''
from HTMLParser import HTMLParser
class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()
'''