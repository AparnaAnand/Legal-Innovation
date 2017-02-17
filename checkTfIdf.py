# -*- coding: utf-8 -*-
import CalculateTFIDF as tfidf
'''
with open("testText.txt","r") as fp:
    content = fp.read()
    content = content.decode('string_escape')
    for sentence in content.split("\n"):
        print sentence
'''

with open("1960and2010.txt", "r") as fp:
    content = fp.readlines()
    mainList = [{}, {}]
    mainList[0] = {"1": {}}
    mainList[1] = {"1": {}}
    i=0
    for each in content:
        content1 = each.decode('string_escape')
        mainList[i]["1"]["text"] = content1
        i+=1
    tfidf.calculate(mainList)


'''
db = MySQLdb.connect(host = cs.hostname , user = cs.username , passwd = cs.password , db = cs.databasename)
cur = db.cursor()
cur.execute("select text from legalcase_all_withtext where date_filed<='1960-01-01' limit 1;")
rows = cur.fetchall()
print rows[0]
cur.execute("select text from legalcase_all_withtext where date_filed>='2010-01-01' limit 1;")
rows = cur.fetchall()
print rows[0]
'''