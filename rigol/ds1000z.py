class Ds1000z():
    def __init__(self, visa_resource):
        self.visa_resource = visa_resource

    def visa_write(self, cmd):
        self.visa_resource.write(cmd)

    def visa_read(self):
        return self.visa_resource.read().strip()

    def visa_read_raw(self, num_bytes=-1):
        return self.visa_resource.read_raw(num_bytes)

    def visa_ask(self, cmd):
        return self.visa_resource.query(cmd)
    
    def visa_ask_raw(self, cmd, num_bytes=-1):
        self.visa_write(cmd)
        return self.visa_read_raw(num_bytes)

    def get_id(self):
        return self.visa_ask('*IDN?')

    def get_screenshot(self, filename=None, format='png'):
        raw_img = self.visa_ask_raw(':DISP:DATA? ON,OFF,PNG')[2+9:]
        with open(filename, 'wb') as f:
            f.write(raw_img)