import re
from nltk.corpus import stopwords
import ConstantStrings as cs
import unicodecsv as csv
import sys
import os


def CSV_to_list(date):
    # 1. Read aggregated csv file to obtain entireText (list of lists)
    # 2. Return entireText (list of lists)
    print "Inside CSV_to_list"
    entireText = []
    file_name = os.path.join(cs.path_aggr_five,date+cs.postfix_aggr_five)
    with open(file_name, 'rb') as f:  # opens PW file
        for rec in csv.reader(f, delimiter=',', lineterminator='\n'):
            to_add = list(rec)
            to_add = filter(None, to_add)
            entireText.extend(to_add)
    print "Created entireText: ",len(entireText)
    return entireText


def calculateTF(entireText,date,period):
    # 1. Remove stop words from entireText and make words lowercase
    # 2. Create count dictionary for all words (also remove numbers and punctuations from words)
    # 3. Filter dictionary to contain words with count at least of min_count (5 for period=five, 10 for period=decade)
    # 4. Create TF_list to contain list of [k,v] lists
    # 5. Write TF_list into TF output csv file
    print "Inside Calculate TF for: ",date,period
    if period == "five":
        path = cs.path_tf_five
        postfix = cs.postfix_tf_five
        min_count = 5
    else:
        path = cs.path_tf_decade
        postfix = cs.postfix_tf_decade
        min_count = 10
    TotalWords = 0
    TF = {}
    stops = set(stopwords.words("english"))
    word_list = [word.lower() for word in entireText if not word in stops]
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
        TotalWords += 1
    print "Created TF dictionary: ",len(TF)
    i=0
    print "Filtering TF"
    filtered_TF = {k:v for k,v in TF.iteritems() if v>=min_count}
    print "Filtered TF: ",len(filtered_TF)
    TF_list = []
    for k,v in filtered_TF.iteritems():
        TF_list.append([k,v])
    print "TF_list: ",len(TF_list)
    print "Writing to file.."
    f = open(os.path.join(path,date+postfix),"wb")
    writer = csv.writer(f)
    writer.writerows(TF_list)
    f.close()
    print "Written"

if __name__ == '__main__':
    # Call options:
    # 1. python CalculateTFIDF.py 1950-01-01 five
    # 2. python CalculateTFIDF.py 1950-01-01 decade 1955-01-01
    if len(sys.argv)>1:
        date = sys.argv[1]
        period = sys.argv[2]
        print "Arguments given: ",date,period,
        if period == "decade":
            date2 = sys.argv[3]
            print date2
        print ""
        if period == "five":
            # Option 1
            entireText = CSV_to_list(date)
            calculateTF(entireText,date,period)
        else:
            # Option 2
            entireText = CSV_to_list(date)
            entireText.extend(CSV_to_list(date2))
            calculateTF(entireText,date,period)
    else:
        print "Wrong number of arguments.\npython CalculateTFIDF.py date1 period [date2]"
    '''
    else:
        # Option 3 - runs for all
        five_year_date_string = ['1950-01-01','1955-01-01','1960-01-01','1965-01-01','1970-01-01','1975-01-01','1980-01-01','1985-01-01','1990-01-01','1995-01-01','2000-01-01','2005-01-01','2010-01-01','2015-01-01']
        for i in range(0,len(five_year_date_string),2):
            date = five_year_date_string[i]
            date2 = five_year_date_string[i+1]
            print "Dates: ",date,date2
            entireText = []
            # Check if file for period=five and date=date already exists:
            filename = os.path.join(cs.path_tf_five,date+cs.postfix_tf_five)
            if not os.path.isfile(filename):
                entireText = CSV_to_list(date)
                calculateTF(entireText,date,period)
            # Check if file for period=decade already exists:
            filename = os.path.join(cs.path_tf_decade,date+cs.postfix_tf_decade)
            if not os.path.isfile(filename):
                if entireText == []:
                    entireText = CSV_to_list(date)
                entireText.extend(CSV_to_list(date2))
                calculateTF(entireText,date,period)
            # Check if file for period=five and date=date2 already exists:
            filename = os.path.join(cs.path_tf_five,date2+cs.postfix_tf_five)
            if not os.path.isfile(filename):
                entireText = CSV_to_list(date2)
                calculateTF(entireText,date2,period)
    '''
