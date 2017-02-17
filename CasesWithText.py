class Cases:
    def __init__(self,id,court,date,text):
        self.case_id=id
        self.court=court
        self.case_date=date
        self.text=text
    def makeJSON(self):
        return {"case_id":self.case_id,"court":self.court,"text":self.text}
    #"statute":self.statute"case_date":self.case_date,