import connectDB as cdb
import CalculateTFIDF as tfidf
import json
import UseWord2Vec as w2v
import AggregateText as at
import os
import ConstantStrings as cs

if __name__ == "__main__":
    #dates = [('1950-01-01','1960-01-01'),('1960-01-01','1970-01-01'),('1970-01-01','1980-01-01'),('1980-01-01','1990-01-01'),('1990-01-01','2000-01-01'),('2000-01-01','2010-01-01'),('2010-01-01',None)]
    #'1950-01-01','1955-01-01','1960-01-01','1965-01-01','1970-01-01','1975-01-01','1980-01-01',
    fif_year_date_string = ['1985-01-01','1990-01-01','1995-01-01','2000-01-01','2005-01-01','2010-01-01','2015-01-01',None]
    dates = []
    for i in range(len(fif_year_date_string)-1):
        dates.append((fif_year_date_string[i],fif_year_date_string[i+1]))
    print dates
    #dates = [('1950-01-01','1955-01-01'),('1955-01-01','1960-01-01'),('1960-01-01','1965-01-01''1970-01-01'),('1970-01-01','1980-01-01'),('1980-01-01','1990-01-01'),('1990-01-01','2000-01-01'),('2000-01-01','2010-01-01'),('2010-01-01',None)]
    for d1,d2 in dates:
        print "Checking date range:",d1," - ",d2
        #filename = d1+cs.postfix_json
        # Check if .json file exists - only if it doesn't, call extract cases to create it
        #if not os.path.isfile(filename):
        #    print filename," not present."
        # Open .json file and obtain data
        filename = os.path.join(cs.path_at_fifty,d1+cs.postfix_aggr_fif)
        # Check if aggregate data text file exists - if not present call function to create
        #if not os.path.isfile(filename):
        #    print filename," not present."
        db = cdb.connect()
        allCases = cdb.extractCases(db,d1,d2)
        at.aggregateTheText(d1, allCases)

        '''
        filename = d1+cs.postfix_tf
        # Check if TF file present - if not present call function to find tf
        if not os.path.isfile(filename):
            print filename, " not present."
            tfidf.calculateTF(d1)
            # call function to calculate TF
        # Questions? - How to pre-process data from .json file?
        w2v.convertTextToVector(d1)
        #fileip.close()
        '''
        print "Iteration over...."