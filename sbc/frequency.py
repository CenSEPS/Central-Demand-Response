from serial import Serial


class FrequencyMeter(object):
    def __init__(self):
        pass

    def get_data(self):
        raise NotImplementedError


class DummyFrequencyMeter(FrequencyMeter):
    def __init__(self, dummyData=[], repeat=True):
        self.data = dummyData
        self.index = 0
        if not isinstance(repeat, bool):
            raise TypeError(
                "The repeat argument must be of type bool."
            )
        self.repeat = repeat
        super(DummyFrequencyMeter, self).__init__()

    def get_data(self):
        d = self.data[self.index]
        self.index += 1
        if self.repeat:
            self.index %= len(self.data)

        return d


class ArduinoFrequencyMeter(FrequencyMeter):
    def __init__(self, serial='/dev/ttyACM0', baud=9600):
        self.serial = Serial(serial, baud)
        super(ArduinoFrequencyMeter, self).__init__()

    def get_data(self):
        if self.serial.isOpen():
            self.serial.write('Freq!')
            r = float(self.serial.readline())
            return r

        return None
