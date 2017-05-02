import unicodecsv as csv
import sys
import constant_strings as cs
import glob, os
from collections import defaultdict

def CSV_to_list(file):
    # 1. Read file to obtain a list of (word,TF).
    # 2. Return the list
    print "Inside CSV_to_list: ",file
    list_tf_words = []
    with open(file, 'rb') as f:
        for rec in csv.reader(f, delimiter=',', lineterminator='\n'):
            to_add = (rec[0],int(rec[1]))
            list_tf_words.append(to_add)
    print "Found TF words: ",len(list_tf_words)
    return list_tf_words

def update_dict(d,l):
    # 1. For each word in l, update d appropriately to hold the word and its frequency
    # 2. Return d
    for (word,freq) in l:
        if word in d:
            prev = d[word]
            d[word]+=freq
        else:
            d[word]=freq
    return d

def join_tfs(period):
    # 1. Find all TF files and store in file_list
    # 2. For each file: Obtain list_of_words by calling CSV_to_list(); Update total_dict by calling update_dict(); Update intersection and union sets; Find new words added and update the new_words dictionary
    # 3. Write intersection set and union set into files
    # 4. Filter new_words dictionary to those that stayed till the end (that is, value=0)
    # 5. Write filtered new_words into a file
    if period == "five":
        path = cs.path_tf_five
        postfix = cs.postfix_tf_five
    else:
        path = cs.path_tf_decade
        postfix = cs.postfix_tf_decade
    os.chdir(path)
    file_list = []
    for file in glob.glob("*_"+period+".csv"):
        file_list.append(file)
    file_list = sorted(file_list)
    total_dict = {}
    year_list = {}
    intersection_set_words = set()
    union_set_words = set()
    new_words = {}
    for i in range(len(file_list)):
        file = file_list[i]
        print file
        list_of_words = CSV_to_list(file)
        total_dict = update_dict(total_dict,list_of_words)
        set_of_words = set([w for (w,k) in list_of_words])
        if intersection_set_words==set():
            intersection_set_words = set_of_words
            union_set_words = set_of_words
            for w in set_of_words:
                year_list[w] = file_list[i]
                new_words[w] = len(file_list)-i-1
        else:
            intersection_set_words = intersection_set_words & set_of_words
            union_set_words = union_set_words | set_of_words
            diff_words = set_of_words - intersection_set_words
            for w in diff_words:
                if w not in new_words:
                    year_list[w] = file_list[i]
                    new_words[w] = len(file_list)-i-1
                else:
                    new_words[w]-=1
    print "Intersection set size: ",len(intersection_set_words)
    f = open(cs.intersection_file,"wb")
    writer = csv.writer(f)
    for word in intersection_set_words:
        writer.writerow([word,total_dict[word]])
    f.close()
    print "Union set size: ",len(union_set_words)
    f = open(cs.union_file,"wb")
    writer = csv.writer(f)
    for word in union_set_words:
        writer.writerow([word,total_dict[word]])
    f.close()
    diff_set = [k for k,v in new_words.iteritems() if v==0]
    print "Usefule new words: ",len(diff_set)
    f = open("newly_added.csv","wb")
    writer = csv.writer(f)
    for word in diff_set:
        writer.writerow([word,total_dict[word],year_list[word]])
    f.close()

    # ADDING NEW CODE FOR NEWLY ADDED -----------------------------------

    diff_by_year = defaultdict(list)
    for word in diff_set:
        year = year_list[word]
        diff_by_year[year].append((word,total_dict[word]))
    for year in diff_by_year:
        diff_by_year[year] = sorted(diff_by_year[year], key = lambda x : x[1], reverse = True)[:20]
    f = open("newly_added_by_year.csv","wb")
    writer = csv.writer(f)
    for year in diff_by_year:
        for (word,score) in diff_by_year[year]:
            writer.writerow([year,word,score])
    f.close()
    # -------------------------------------------------------------------

    print "Done"

if __name__ == "__main__":
    # 1. python word_lists_tfs.py five
    # 2. python word_lists_tfs.py decade
	period = sys.argv[1]
	join_tfs(period)
