class Ds1000z():
    def __init__(self, visa_resource):
        self.visa_resource = visa_resource

    def visa_ask(self, cmd):
        return self.visa_resource.query(cmd)

    def get_id(self):
        return self.visa_ask('*IDN?')