import connect_db as cdb
import calculate_tf as tf
import use_word2vec as w2v
import aggregate_text as at
import os
import sys
import constant_strings as cs

if __name__ == "__main__":
    # Call options:
    # 1. python main_topic_change.py 1950-01-01 1955-01-01 five
    # 2. python main_topic_change.py 1950-01-01 1955-01-01 decade
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
            all_cases = cdb.extract_cases(db,date,date2)
            at.aggregate_all_text(date,all_cases)

        if period == "five":
            # Option 1
            # Perform Word2Vec:
            entire_text = w2v.CSV_to_list(date)
            w2v.convert_text_to_vector(entire_text,date,period)

            # Perform TF:
            entire_text = tf.CSV_to_list(date)
            tf.calculate_TF(entire_text,date,period)
        else:
            # Option 2
            # Perform Word2Vec:
            entire_text = w2v.CSV_to_list(date)
            entire_text += w2v.CSV_to_list(date2)
            w2v.convert_text_to_vector(entire_text,date,period)

            # Perform TF:
            entire_text = tf.CSV_to_list(date)
            entire_text.extend(tf.CSV_to_list(date2))
            tf.calculate_TF(entire_text,date,period)
    else:
        print "Wrong number of arguments.\npython main_topic_change.py date1 date2 period"