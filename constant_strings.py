import os

# For Database Connection
hostname = "localhost"
username = "root"
password = "yppa39213"
databasename = "court_listener"

# For Aggregate files
postfix_aggr_five = "_AT_five.csv"
path_aggr_five = os.path.join("AT_FILES","FIVE")

# For TF files
postfix_tf_five = "_TF_five.csv"
postfix_tf_decade = "_TF_decade.csv"
union_file = "TF_union.csv"
intersection_file = "TF_intersection.csv"
newly_added = "newly_added.csv"
path_tf_five = os.path.join("TF_FILES","FIVE")
path_tf_decade = os.path.join("TF_FILES","DECADE")

# For model files
postfix_models_five = "_MODEL_five"
postfix_models_decade = "_MODEL_decade"
path_models_five = os.path.join("MODEL_FILES","FIVE")
path_models_decade = os.path.join("MODEL_FILES","DECADE")

# For similar words files
postfix_similar_five = "_SIMILAR_five.csv"	
postfix_similar_decade = "_SIMILAR_decade.csv"
path_similar_five = os.path.join("W2V_SIMILAR_TERMS","FIVE")
path_similar_decade = os.path.join("W2V_SIMILAR_TERMS","DECADE")

# For most changes words files
final_all_inter = "mostchanged(pairwaise)_intersection.csv"
final_first_last_inter = "mostchanged(firstlast)_intersection.csv"
final_all_new = "mostchanged(pairwise)_newly_added.csv"
final_first_last_new = "mostchanged(firstlast)_newly_added.csv"
path_final_five = os.path.join("MOST_CHANGED","FIVE")
path_final_decade = os.path.join("MOST_CHANGED","DECADE")

# Miscellanious
stopwords_file = "stopwords.txt"