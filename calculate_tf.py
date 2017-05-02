import re
#from nltk.corpus import stopwords
import constant_strings as cs
import unicodecsv as csv
import sys
import os


def CSV_to_list(date):
    # 1. Read aggregated csv file to obtain entire_text (list of words)
    # 2. Return entire_text (list of words)
    print "Inside CSV_to_list"
    entire_text = []
    file_name = os.path.join(cs.path_aggr_five,date+cs.postfix_aggr_five)
    with open(file_name, 'rb') as f:
        for rec in csv.reader(f, delimiter=',', lineterminator='\n'):
            to_add = list(rec)
            to_add = filter(None, to_add)
            entire_text.extend(to_add)
    print "Created entire_text: ",len(entire_text)
    return entire_text


def calculate_TF(entire_text,date,period):
    # 1. Remove stop words from entire_text and make words lowercase
    # 2. Create count dictionary for all words (also remove numbers and punctuations from words)
    # 3. Filter dictionary to contain words with count at least of min_count (5 for period=five, 10 for period=decade)
    # 4. Write filtered TF into TF output csv file
    print "Inside Calculate TF for: ",date,period
    if period == "five":
        path = cs.path_tf_five
        postfix = cs.postfix_tf_five
        min_count = 5
    else:
        path = cs.path_tf_decade
        postfix = cs.postfix_tf_decade
        min_count = 10
    total_words = 0
    TF = {}
    stops = []
    #stops = set(stopwords.words("english"))
    with open(cs.stopwords_file,"r") as stop_file:
        for line in stop_file:
            stops.append(line.strip())
    word_list = [word.lower() for word in entire_text if not word in stops]
    print "Created word_list: ",len(word_list)
    print "Started calculating TF .. "
    for word in word_list:
        word = re.sub('\W', '', word)
        word = re.sub('[0-9]', '', word)
        if word == '':
            continue
        if word in TF:
            TF[word] += 1
        else:
            TF[word] = 1
        total_words += 1
    print "Created TF dictionary: ",len(TF)
    i=0
    print "Filtering TF"
    filtered_TF = {k:v for k,v in TF.iteritems() if v>=min_count}
    print "Filtered TF: ",len(filtered_TF)
    print "Writing to file.."
    f = open(os.path.join(path,date+postfix),"wb")
    writer = csv.writer(f)
    for k,v in filtered_TF.items():
        writer.writerow([k,v])
    f.close()
    print "Written"

if __name__ == '__main__':
    # Call options:
    # 1. python calculate_tf.py 1950-01-01 five
    # 2. python calculate_tf.py 1950-01-01 decade 1955-01-01
    if len(sys.argv)>1:
        date = sys.argv[1]
        period = sys.argv[2]
        print "Arguments given: ",date,period,
        if period == "decade":
            date2 = sys.argv[3]
            print date2
        else:
            print ""
        if period == "five":
            # Option 1
            entire_text = CSV_to_list(date)
            calculate_TF(entire_text,date,period)
        else:
            # Option 2
            entire_text = CSV_to_list(date)
            entire_text.extend(CSV_to_list(date2))
            calculate_TF(entire_text,date,period)
    else:
        print "Wrong number of arguments.\npython calculate_tf.py date1 period [date2]"