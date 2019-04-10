class _Channel():
    def __init__(self, channel, osc):
        self._channel = channel
        self._osc = osc
    
    def get_data(self, mode='norm', filename=None):
        self._osc.visa_write(':stop')
        self._osc.visa_write(':wav:sour chan{}'.format(self._channel))
        self._osc.visa_write(':wav:mode {}'.format(mode))
        self._osc.visa_write(':wav:form asc')
        data = self._osc.visa_ask_raw(':wav:data?')[11:]
        return data

class Ds1000z():
    def __init__(self, visa_resource):  
        self.visa_resource = visa_resource
        self._channels = [_Channel(c, self) for c in range(1,5)]
    
    def __getitem__(self, i):
        assert 1 <= i <= 4, 'Not a valid channel.'
        return self._channels[i-1]

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
    
    def get_data(self, filename=None, channel=1):
        self.visa_write(':WAV:SOUR: CHAN{}'.format(channel))
        self.visa_write(':WAV:MODE NORM')
        self.visa_write(':WAV:FORM ASC')
        raw_data = self.visa_ask_raw(':WAV:DATA?')[2+9:]
        return raw_data