import re
from nltk.corpus import stopwords
import ConstantStrings as cs
import unicodecsv as csv
import sys
import os


def CSV_to_list(date):
    print "Inside CSV_to_list"
    entireText = []
    file_name = os.path.join(cs.path_at_fifty,date+cs.postfix_aggr_fif)
    with open(file_name, 'rb') as f:  # opens PW file
        for rec in csv.reader(f, delimiter=',', lineterminator='\n'):
            to_add = list(rec)
            to_add = filter(None, to_add)
            entireText.extend(to_add)
    print "Created entireText: ",len(entireText)
    return entireText

# Remove stop words, remove numbers and punctuations.
def calculateTF(entireText,date,period):
    print "Inside Calculate TF for: ",date,period
    # Create entireText to contain a list of all the words from aggregated text
    
    '''
    for line in f.readlines():
        #print "line: ",line
        #raw_input()
        text = line.split()
        entireText.extend(text)
    '''
    TotalWords = 0
    TF = {}
    # Remove stop words
    stops = set(stopwords.words("english"))
    word_list = [word for word in entireText if not word in stops]
    print "Created word_list: ",len(word_list)
    # Create count dictionary for the words
    print "Started calculating TF .. "
    for word in word_list:  # Per word
        word = re.sub('\W', '', word)
        word = re.sub('[0-9]', '', word)
        if word == '':
            continue
        if word in TF:
            TF[word] += 1
        else:
            TF[word] = 1
        TotalWords += 1
    '''
    print "Created dictionary with word counts."
    # Calculate TF for each word - normalized
    for word in WordCount:
        TF[word] = float(WordCount[word]) / TotalWords
        print TF[word]
        raw_input()
    '''
    print "Created TF dictionary: ",len(TF)

    i=0
    if period == "fifty":
        min_count = 5
    else:
        min_count = 10
    print "Filtering TF"
    filtered_TF = {k:v for k,v in TF.iteritems() if v>=min_count}
    print "Filtered TF: ",len(filtered_TF)
    TF_list = []
    for k,v in filtered_TF.iteritems():
        TF_list.append([k,v])
    #print "TF sorting .."
    # Sort based on TF values
    #TF_sorted = sorted(filtered_TF.items(), key=lambda x: x[1], reverse=True)
    # Pick top 50
    #TF_sorted = TF_sorted[:50]
    #print "\nTF sorted: ", len(TF_sorted)
    # Write top 50 words into file
    print "TF_list: ",len(TF_list)
    print "Writing to file.."
    if period == "fifty":
        path = cs.path_tf_fifty
        postfix = cs.postfix_tf_fif
    else:
        path = cs.path_tf_decade
        postfix = cs.postfix_tf_dec
    f = open(os.path.join(path,date+postfix),"wb")
    writer = csv.writer(f)
    writer.writerows(TF_list)
    #w = csv.DictWriter(f,filtered_TF.keys())
    #w.writeheader()
    #w.writerow(filtered_TF)
    '''
    for word,tf in TF_sorted:
        print word
        f.write(word)
        f.write(",")
        f.write(str(tf))
        f.write("\n")
    '''
    f.close()
    print "Written"

if __name__ == '__main__':
    #'1950-01-01','1955-01-01','1960-01-01','1965-01-01','1970-01-01','1975-01-01',
    if len(sys.argv)>1:
        date = sys.argv[1]
        date2 = sys.argv[3]
        period = sys.argv[2]
        print "Arguments given: ",date,date2,period
        if period == "fifty":
            entireText = CSV_to_list(date)
            calculateTF(entireText,date,period)
        else:
            entireText = CSV_to_list(date)
            entireText.extend(CSV_to_list(date2))
            calculateTF(entireText,date,period)
    else:
        fif_year_date_string = ['1980-01-01','1985-01-01','1990-01-01','1995-01-01','2000-01-01','2005-01-01','2010-01-01','2015-01-01']
        for i in range(0,len(fif_year_date_string),2):
            date = fif_year_date_string[i]
            date2 = fif_year_date_string[i+1]
            print "Dates: ",date,date2
    #date = sys.argv[1]
    #period = sys.argv[2]
    #date2 = sys.argv[3]
    #if period == "fifty":
            entireText = []
            filename = os.path.join(cs.path_tf_fifty,date+cs.postfix_tf_fif)
            if not os.path.isfile(filename):
                entireText = CSV_to_list(date)
                calculateTF(entireText,date,"fifty")
    #if period == "decade":
        #entireText = CSV_to_list(date)
            filename = os.path.join(cs.path_tf_decade,date+cs.postfix_tf_dec)
            if not os.path.isfile(filename):
                if entireText == []:
                    entireText = CSV_to_list(date)
                entireText.extend(CSV_to_list(date2))
                calculateTF(entireText,date,"decade")
            filename = os.path.join(cs.path_tf_fifty,date2+cs.postfix_tf_fif)
            if not os.path.isfile(filename):
                entireText = CSV_to_list(date2)
                calculateTF(entireText,date2,"fifty")
    #calculateTF('try')

'''
    Input: [{"1":{"text":"..","id":..,...},"2":{}..},{},{}...]
    TotalDecades = 0
    PerWordIDF = {}
    PerDecadeTF = {}
    DecadeHasWord = {}
    DecadeTFIDF = {}
    for casesDict in casesPerDecade:#Per decade
        uniqueWords = []
        PerDecadeTF[TotalDecades] = {}
        PerDecadeWordCount = {}
        PerDecadeTotalWords = 0
        for each in casesDict.values():#Per case
            text = each["text"]
            text = text.encode('utf-8')
            text = text.decode('string_escape')
            text = strip_tags(text)
            word_list = re.findall(r"[\w']+", text)
            word_list = [word for word in word_list if word not in stopwords.words('english')]
            for word in word_list:#Per word
                word = re.sub('[0-9]','',word)
                if word == '':
                    continue
                if word in PerDecadeWordCount:
                    PerDecadeWordCount[word] += 1
                else:
                    PerDecadeWordCount[word] = 1
                if word not in uniqueWords:
                    if word not in DecadeHasWord:
                        DecadeHasWord[word] = 1
                    else:
                        DecadeHasWord[word] += 1
                    uniqueWords.append(word)
                PerDecadeTotalWords += 1
        for word in PerDecadeWordCount:
            PerDecadeTF[TotalDecades][word] = float(PerDecadeWordCount[word])/PerDecadeTotalWords
        TotalDecades += 1
    for decade in range(TotalDecades):
        DecadeTFIDF[decade] = {}
        for word in PerDecadeTF[decade]:
            PerWordIDF[word] = math.log(float(TotalDecades)/(DecadeHasWord[word]))# ------------------ check with 1+ in Denomenator --------------
            DecadeTFIDF[decade][word] = PerDecadeTF[decade][word] * PerWordIDF[word]
    for key,tfidfDict in DecadeTFIDF.items():
        tfidfDict_sorted = sorted(tfidfDict.items(), key=lambda x: x[1],reverse=True)
        tfidfDict_sorted = tfidfDict_sorted[:20]
        DecadeTFIDF[key] = tfidfDict_sorted
    print "TFIDF after: ",DecadeTFIDF
    return DecadeTFIDF
'''

# 4. If aggr. output is usable by tf and word2vec, in tf - just remove the unnecesseries, per word.
# Else, can we output list of lists in aggr. and use in tf and word2vec. If yes, in tf - just remove the unnecesseries, per word.
# Else, no aggr. output into file at all. Call the functions each time accordingly for tf and word2vec inputs.
# 5. Obtain all .json files, .txt for aggr. (if still needed) and TF.
# 6. Confirm cython working.
# 7. Obtain all model files.
# 8. How to query related words, Hao paper, how to display results?
# 9. Reply to Beverly
# 10. Automate + pipeline the whole program