from gensim import models
import gensim.models.doc2vec
import multiprocessing
import constant_strings as cs
import unicodecsv as csv
import sys
import os
import numpy

cores = multiprocessing.cpu_count()
assert gensim.models.doc2vec.FAST_VERSION > -1, "this will be painfully slow otherwise"

CHECK_WORDS = ['race','crime','criminal','civil rights','intellectual property','business','startup','entrepreneur','entrepreneurial','merger','acquisition','technology','competition']

def CSV_to_list(date):
    # 1. Read aggregated csv file to obtain entire_text (list of lists)
    # 2. Return entire_text - list of lists
    print "Inside CSV to list"
    entire_text = []
    file_name = os.path.join(cs.path_aggr_five,date+cs.postfix_aggr_five)
    with open(file_name, 'rb') as f:
        for rec in csv.reader(f, delimiter=',', lineterminator='\n'):
            to_add = list(rec)
            to_add = filter(None, to_add)
            to_add = [ch.lower() for ch in to_add]
            entire_text.append(to_add)
    return entire_text

def convert_text_to_vector(entire_text,date,period):
    # 1. Train model using word2vec
    # 2. Save model in file
    # 3. Write the top 20 most similar words for each word in CHECK_WORDS into file
    if period == "five":
        postfix = cs.postfix_models_five
        path = cs.path_models_five
    else:
        postfix = cs.postfix_models_decade
        path = cs.path_models_decade
    print "Inside word2vec"
    print "No of lines: ",len(entire_text)
    print "Start training.."
    model = models.Word2Vec(entire_text, size=100, window=10, min_count=5, workers=cores)
    print "Done training.."
    model.save(os.path.join(path,date+postfix))
    print "Saved.."
    print "MODEL:\n",model
    for term in CHECK_WORDS:
        print term.upper(),":\n"
        for t,p in model.most_similar(positive=term.split(' '),topn=20):
            print t,":",str(round(p,3))
        print ""

def load_word2vec(date,period):
    # Load model from file and return it
    if period == "five":
        postfix = cs.postfix_models_five
        path = cs.path_models_five
    else:
        postfix = cs.postfix_models_decade
        path = cs.path_models_decade
    model = models.Word2Vec.load(os.path.join(path,date+postfix))
    return model

def output_model_to_file(model,period):
    # 1. Get top 20 most similar words for each word in CHECK_WORDS
    # 2. Write top 20 for all words into file
    if period == "five":
        op_postfix = cs.postfix_similar_five
        op_path = cs.path_similar_five
    else:
        op_postfix = cs.postfix_similar_decade
        op_path = cs.path_similar_decade
    f = open(os.path.join(op_path,date+op_postfix),"wb")
    writer = csv.writer(f)
    for term in CHECK_WORDS:
        if term not in model.vocab:
            continue
        writer.writerow([term.upper()])
        similar_list = []
        similar_terms = model.most_similar(positive=term.split(' '),topn=20)
        for t,p in similar_terms:
            similar_list.append([t,str(round(p,3))])
        writer.writerows(similar_list)
    f.close()
    print "Done"

if __name__ == '__main__':
    # Call options:
    # 1. python use_word2vec.py load 1950-01-01 five
    # 2. python use_word2vec.py load 1950-01-01 decade
    # 3. python use_word2vec.py save 1950-01-01 five
    # 4. python use_word2vec.py save 1950-01-01 decade 1955-01-01
    if len(sys.argv)>1:
        choice = sys.argv[1]
        date = sys.argv[2]
        period = sys.argv[3]
        if choice == "load":
            # Option 1 or 2
            model = load_word2vec(date,period)
            output_model_to_file(model,period)
        else:
            if period == "five":
                # Option 3
                print "Date: ",date
                entire_text = CSV_to_list(date)
                convert_text_to_vector(entire_text,date,period)
            else:
                # Option 4
                date2 = sys.argv[4]
                print "Date pair: ",date," and ",date2
                entire_text = CSV_to_list(date)
                entire_text += CSV_to_list(date2)
                convert_text_to_vector(entire_text,date,period)
    else:
        print "Wrong number of arguments.\npython use_word2vec.py load/save date1 period [date2]"