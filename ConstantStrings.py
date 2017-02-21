import os

hostname = "localhost"
username = "root"
password = "yppa39213"
databasename = "court_listener"
postfix_aggr_five = "_AT_five.csv"
path_aggr_five = os.path.join("AT_FILES","FIVE") # Path to Aggregated files' folder - AT_FILES/FIVE
postfix_tf_five = "_TF_five.csv"
postfix_tf_decade = "_TF_decade.csv"
path_tf_five = os.path.join("TF_FILES","FIVE") # Path to Term Frequency files' folder (For 5 years) - TF_FILES/FIVE
path_tf_decade = os.path.join("TF_FILES","DECADE") # Path to Term Frequency files' folder (For 10 years) - TF_FILES/DECADE
postfix_models_five = "_MODEL_five"
postfix_models_decade = "_MODEL_decade"
path_models_five = os.path.join("MODEL_FILES","FIVE") # Path to Word2Vec Model files' folder (For 5 years) - MODEL_FILES/FIVE
path_models_decade = os.path.join("MODEL_FILES","DECADE") # Path to Word2Vec Model files' folder (For 10 years) - MODEL_FILES/DECADE
