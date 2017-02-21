from gensim import models
import nltk.data
import gensim.models.doc2vec
import multiprocessing
import ConstantStrings as cs
import unicodecsv as csv
import sys
import os

cores = multiprocessing.cpu_count()
assert gensim.models.doc2vec.FAST_VERSION > -1, "this will be painfully slow otherwise"

# Load the punkt tokenizer
tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')\

def CSV_to_list(date):
    # 1. Read aggregarted csv file to obtain entireText (list of lists)
    # 2. Return entireText - list of lists
    print "Inside CSV to list"
    entireText = []
    file_name = os.path.join(cs.path_aggr_five,date+cs.postfix_aggr_five)
    with open(file_name, 'rb') as f:
        for rec in csv.reader(f, delimiter=',', lineterminator='\n'):
            to_add = list(rec)
            to_add = filter(None, to_add)
            entireText.append(to_add)
    return entireText

def convertTextToVector(entireText,date,period):
    # 1. Train model using word2vec
    # 2. Save model in file
    # 3. Display output for "race", "crime", "criminal", "civil rights", "intellectual property"
    if period == "five":
        postfix = cs.postfix_models_five
        path = cs.path_models_five
    else:
        postfix = cs.postfix_models_decade
        path = cs.path_models_decade
    print "Inside word2Vec"
    print "No of lines: ",len(entireText)
    print "Start training.."
    model = models.Word2Vec(entireText, size=100, window=10, min_count=5, workers=cores)
    print "Done training.."
    model.save(os.path.join(path,date+postfix))
    print "Saved.."
    print "MODEL:\n",model
    print "RACE:\n",model.most_similar('race',topn=20)
    print "CRIME:\n",model.most_similar('crime',topn=20)
    print "CRIMINAL:\n",model.most_similar('criminal',topn=20)
    print "CIVIL RIGHTS:\n",model.most_similar(positive=['civil','rights'],topn=20)
    print "INTELLECTUAL PROPERTY:\n",model.most_similar(positive=['intellectual','property'],topn=20)

def loadWord2Vec(date,period):
    # 1. Load from model
    # 2. Display output for "race", "crime", "criminal", "civil rights", "intellectual property"
    if period == "five":
        postfix = cs.postfix_models_five
        path = cs.path_models_five
    else:
        postfix = cs.postfix_models_decade
        path = cs.path_models_decade
    print "Model: "
    model = models.Word2Vec.load(os.path.join(path,postfix))
    print "RACE:\n",model.most_similar('race',topn=20)
    print "CRIME:\n",model.most_similar('crime',topn=20)
    print "CRIMINAL:\n",model.most_similar('criminal',topn=20)
    print "CIVIL RIGHTS:\n",model.most_similar(positive=['civil','rights'],topn=20)
    print "INTELLECTUAL PROPERTY:\n",model.most_similar(positive=['intellectual','property'],topn=20)

if __name__ == '__main__':
    # Call options:
    # 1. python UseWord2Vec.py load 1950-01-01 five
    # 2. python UseWord2Vec.py load 1950-01-01 decade
    # 3. python UseWord2Vec.py save 1950-01-01 five
    # 4. python UseWord2Vec.py save 1950-01-01 decade 1955-01-01
    if len(sys.argv)>1:
        choice = sys.argv[1]
        date = sys.argv[2]
        period = sys.argv[3]
        if choice == "load":
            # Option 1 or 2
            loadWord2Vec(date,period)
        else:
            if period == "five":
                # Option 3
                print "Date: ",date
                entireText = CSV_to_list(date)
                convertTextToVector(entireText,date,period)
            else:
                # Option 4
                date2 = sys.argv[4]
                print "Date pair: ",date," and ",date2
                entireText = CSV_to_list(date)
                entireText += CSV_to_list(date2)
                convertTextToVector(entireText,date,period)
    else:
        print "Wrong number of arguments.\npython UseWord2Vec.py load/save date1 period [date2]"
