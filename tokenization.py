import nltk
import pprint
from bs4 import BeautifulSoup
from nltk import word_tokenize
import re

def remove_puncts(a):
	return re.search('\W+',a)


tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
with open("testTextInter.txt",'r') as f:
	text = f.read()
	text = text.decode('iso8859_2')
	text = BeautifulSoup(text).get_text()
	tok_text = tokenizer.tokenize(text)
	#pprint.pprint(tok_text)
	fop = open("testTextTokenized.txt",'w')
	#fop.write(text)
	for each in tok_text:
		#print "Each: ",each
		fop.write(each)
		fop.write("\n")
		each_list = word_tokenize(each)
		#each_list = filter(remove_puncts,each_list)
		each_list = [re.sub('^\W+$', '', e) for e in each_list]
		each_list = [s for s in each_list if s]
		print each_list
	fop.close()