from gensim import models
import nltk.data
#nltk.download()
import gensim.models.doc2vec
import multiprocessing
import ConstantStrings as cs
import unicodecsv as csv
import sys
import os

cores = multiprocessing.cpu_count()
assert gensim.models.doc2vec.FAST_VERSION > -1, "this will be painfully slow otherwise"
# assertion meaning? variable^ meaning? why low vocab? Is cython working?
# try on ubuntu? try with C? email hao if questions

# Load the punkt tokenizer
tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')\


def CSV_to_list(date):
    #Read CSV file and return list of lists
    print "Inside CSV to list"
    entireText = []
    file_name = os.path.join(cs.path_at_fifty,date+cs.postfix_aggr_fif)
    with open(file_name, 'rb') as f:  # opens PW file
        for rec in csv.reader(f, delimiter=',', lineterminator='\n'):
            to_add = list(rec)
            to_add = filter(None, to_add)
            entireText.append(to_add)
    return entireText

def convertTextToVector(entireText,period):
    if period == "fifty":
        path = cs.path_models_fifty
    else:
        path = cs.path_models_decade
    print "inside word2Vec"
    print "No of lines: ",len(entireText)
    #d1 = datetime.date.today().ctime()
    #print d1
    print "Start training.."
    model = models.Word2Vec(entireText, size=100, window=10, min_count=5, workers=cores)
    print "Done training.."
    #d2 = datetime.date.today().ctime()
    #print d2
    #raw_input()
    model.save(os.path.join(path,date+'_'+period+'_model'))
    print "Saved.."
    #raw_input()
    
    print "Model: "
    model = models.Word2Vec.load(os.path.join(path,date+'_'+period+'_model'))
    print model
    #print model['patent']
    print "RACE:\n",model.most_similar('race',topn=20)
    print "CRIME:\n",model.most_similar('crime',topn=20)
    print "CRIMINAL:\n",model.most_similar('criminal',topn=20)
    print "CIVIL RIGHTS:\n",model.most_similar(positive=['civil','rights'],topn=20)
    print "INTELLECTUAL PROPERTY:\n",model.most_similar(positive=['intellectual','property'],topn=20)
    #diff = d2-d1
    #print "Time taken: ",diff.total_seconds()
    #model = word2vec.load(date+'model')
    #print "Model vocab: "
    #print model.vocab
    '''
    fo = open("newText.txt","w")
    raw_sentences = tokenizer.tokenize(fo.read().strip())
    for each in raw_sentences:
        each = each.strip("\n\t ")
        if each == "":
            continue
        #print each
        fo.write(each)
        fo.write("\n")
    f.close()
    fo.close()
    print "Done"
    raw_input()
    w = models.Word2Vec()
    w.load_word2vec_format('GoogleNews-vectors-negative300.bin', binary=True)
    print w["queen"]
    word2vec.word2vec("newText.txt", "aggregatedText.bin", size=5,verbose=True)
    sentences = [['first', 'sentence'], ['second', 'sentence']]
    f = open("newText.txt","r")
    raw_sentences = tokenizer.tokenize(f.read().strip())
    print len(f.readlines())
    '''

if __name__ == '__main__':
    # First call for every fifty years:
    #'1950-01-01','1955-01-01','1960-01-01','1965-01-01','1970-01-01','1975-01-01','1980-01-01','1985-01-01','1990-01-01','1995-01-01',
    #fif_year_date_string = ['2000-01-01','2005-01-01','2010-01-01','2015-01-01']
    #for date in fif_year_date_string:
    #convertTextToVector('1985-01-01','fifty')
    #raw_input()
    date = sys.argv[1]
    period = sys.argv[2]
    date2 = sys.argv[3]
    if period == "fifty":
        print "Date: ",date
        entireText = CSV_to_list(date)
        convertTextToVector(entireText,"fifty")
    else:
        print "Date pair: ",date," and ",date2
        entireText = CSV_to_list(date)
        entireText += CSV_to_list(date2)
        convertTextToVector(entireText,"decade")
    #convertTextToVector('try')
