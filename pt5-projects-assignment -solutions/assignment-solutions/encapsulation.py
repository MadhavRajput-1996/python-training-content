class Patient:
    def setId(self, id):
        self.id = id

    def setName(self, name):
        self.name = name

    def setSsn(self, ssn):
        self.ssn = ssn

    def getId(self):
        return self.id

    def getName(self):
        return self.name

    def getSsn(self):
        return self.ssn


patient1 = Patient()
patient1.setId(1)
patient1.setName("Simon")
patient1.setSsn("000-000-000")

print("Patient ID: ", patient1.getId())
print("Patient Name: ", patient1.getName())
print("Patient SSN: ", patient1.getSsn())