import subprocess
import atexit


class LoadBase(object):
    ''' Virtual parent class for loads '''
    def __init__(self):
        pass


# priority (0 highest ------- lowest 10)
class SheddableLoad(LoadBase):
    '''Virtual base class for sheddable loads'''
    LoadList = []

    def __init__(self, priority):
        self.priority = priority
        self.shed = False
        SheddableLoad.LoadList.append(self)
        super(SheddableLoad, self).__init__()

    def isShed(self):
        return self.shed

    def shedLoad(self):
        raise NotImplementedError

    def restoreLoad(self):
        raise NotImplementedError

    @classmethod
    def shedByPriority(cls, priority):
        for load in cls.LoadList:
            if load.priority >= priority:
                load.shedLoad()

    @classmethod
    def restoreByPriority(cls, priority):
        for load in cls.LoadList:
            if load.priority <= priority:
                load.restoreLoad()


class DummySheddableLoad(SheddableLoad):
    '''Stub class for sheddable loads'''
    def __init__(self, priority):
        super(DummySheddableLoad, self).__init__(priority)

    def shedLoad(self):
        if not self.isShed():
            self.shed = True
            return True

        return False

    def restoreLoad(self):
        if self.isShed():
            self.shed = False
            return True

        return False


class SBCDIOSheddableLoad(SheddableLoad):
    def __init__(self, priority, dio, evgpio='/usr/local/bin/evgpioctl'):
        self.dio = dio
        self.evgpio = evgpio
        subprocess.call(
            self.evgpio+" --ddrout {} --setout {}".format(self.dio, self.dio),
            shell=True
        )
        super(SBCDIOSheddableLoad, self).__init__(priority)
        # the following is a hack to ensure that the gpio is set back to
        # default when the program exits

        def cleanup():
            subprocess.call(
                evgpio+" --clrout {} --ddrin {}".format(dio, dio),
                shell=True
            )

        atexit.register(cleanup)

    def _evgpioOff(self):
        subprocess.call(
            self.evgpio+" --clrout {}".format(self.dio),
            shell=True
        )

    def _evgpioOn(self):
        subprocess.call(
            self.evgpio+" --setout {}".format(self.dio),
            shell=True
        )

    def shedLoad(self):
        if not self.isShed():
            # run SBC specific command
            self._evgpioOff()
            self.shed = True
            return True

        return False

    def restoreLoad(self):
        if self.isShed():
            # run SBC specific command
            self._evgpioOn()
            self.shed = False
            return True

        return False


class DeferrableLoad(LoadBase):
    pass
