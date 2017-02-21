import connectDB as cdb
import CalculateTFIDF as tfidf
import UseWord2Vec as w2v
import AggregateText as at
import os
import sys
import ConstantStrings as cs

if __name__ == "__main__":
    # Call options:
    # 1. python mainTopicChange.py 1950-01-01 1955-01-01 five
    # 2. python mainTopicChange.py 1950-01-01 1955-01-01 decade
    if len(sys.argv)>1:
        date = sys.argv[1]
        period = sys.argv[3]
        date2 = sys.argv[2]
        print "Arguments given: ",date,period,date2
        # Check if aggregate file exists or user wants it, and perform aggregation:
        filename = os.path.join(cs.path_aggr_five,date+cs.postfix_aggr_five)
        ch = "n"
        if os.path.isfile(filename):
            ch = raw_input("Do you want to perform aggregation? (y/n)")
        if not os.path.isfile(filename) or ch == "y":
            db = cdb.connect()
            allCases = cdb.extractCases(db,date,date2)
            at.aggregateTheText(date,allCases)

        if period == "five":
            # Option 1
            # Perform Word2Vec:
            entireText = w2v.CSV_to_list(date)
            w2v.convertTextToVector(entireText,date,period)

            # Perform TF:
            entireText = tfidf.CSV_to_list(date)
            tfidf.calculateTF(entireText,date,period)
        else:
            # Option 2
            # Perform Word2Vec:
            entireText = w2v.CSV_to_list(date)
            entireText += w2v.CSV_to_list(date2)
            w2v.convertTextToVector(entireText,date,period)

            # Perform TF:
            entireText = tfidf.CSV_to_list(date)
            entireText.extend(tfidf.CSV_to_list(date2))
            tfidf.calculateTF(entireText,date,period)
    else:
        print "Wrong number of arguments.\npython mainTopicChange.py date1 date2 period"
