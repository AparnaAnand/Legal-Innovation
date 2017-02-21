mainTopicChange.py:
- Main program to run the whole process for specified time frame
- Use: python mainTopicChange.py date1 period [date2]
- Examples:
    python mainTopicChange.py 1950-01-01 five
    python mainTopicChange.py 1950-01-01 decade 1955-01-01

UseWord2Vec.py:
- Program to use word2vec over already aggregated text for specified time frame
- Use: python UseWord2Vec.py load/save date1 period [date2]
- Examples:
    python UseWord2Vec.py load 1950-01-01 five
    python UseWord2Vec.py load 1950-01-01 decade
    python UseWord2Vec.py save 1950-01-01 five
    python UseWord2Vec.py save 1950-01-01 decade 1955-01-01

CalculateTFIDF.py:
- Program to create TF files from already aggregated text for specified time frame
- Use: python CalculateTFIDF.py date1 period [date2]
- Examples:
    python CalculateTFIDF.py 1950-01-01 five
    python CalculateTFIDF.py 1950-01-01 decade 1955-01-01

AggregateText.py:
- Program to perform aggregation over all text in time frame

connectDB.py:
- Connects to DB, and obtains all data from the database for specified time frame

ConstantStrings.py:
- Contains the constant strings used in the project
