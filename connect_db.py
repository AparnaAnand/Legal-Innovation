import MySQLdb
import constant_strings as cs

def connect():
    # Connect to database and return the handle
    db = MySQLdb.connect(host = cs.hostname , user = cs.username , passwd = cs.password , db = cs.databasename)
    return db
def extract_cases(db,date1,date2):
    # 1. Extract text from database between given dates
    # 2. Store text in a list
    # 3. Return list (of text from records)
    print "Extracting text cases from Database.."
    cur = db.cursor()
    if date2 != None:
        cur.execute("select le.text from legalcase_all_withtext as le where date_filed>='"+date1+"' and date_filed<'"+date2+"';")
    else:
        cur.execute("select le.text from legalcase_all_withtext as le where date_filed>='" + date1 + "';")
    rows = cur.fetchall()
    print "Finished extracting.."
    cur.close()
    all_cases = []
    print "Start appending to a list.."
    for row in rows:
        all_cases.append(row[0])
    db.close()
    print "Returning a list of length: ",len(all_cases)
    return all_cases