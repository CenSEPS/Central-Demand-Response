"""Main Server Logic"""

import logging
import logging.config
# from datetime import datetime
from time import sleep

LOG_SETTINGS = {
    'version': 1,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': logging.DEBUG,
            'formatter': 'detailed',
        },
    },
    'formatters': {
        'detailed': {
            'format': ('%(asctime)s %(module)-8s line:%(lineno)-4d '
                       '%(levelname)-8s %(message)s'),
        },
    },
    'loggers': {
        'sbc': {
            'level': logging.INFO,
            'handlers': ['console']
        },
    }
}
logging.config.dictConfig(LOG_SETTINGS)

LOAD_SETTINGS = {
    'deferrable': {
    },
    'sheddable': {
    },
}


from . import frequency
from . import loads

logger = logging.getLogger(name='sbc')


def get_frequency(meter):
    return meter.get_data()


# priority 10 gets shed at 59.995
def run():
    # load config file
    # TODO ^^^^^^^
    loads.SBCDIOSheddableLoad(priority=9, dio=76)
    loads.SBCDIOSheddableLoad(priority=10, dio=77)
    # initialize

    try:
        drop = [59.999, 59.998, 59.997, 59.996, 59.995]
        bigDrop = [59.992, 59.990, 59.985, 59.985, 59.985]
        bigRise = [59.985, 59.985, 59.985, 59.990, 59.992]
        rise = [59.995, 59.996, 59.997, 59.998, 59.999]
        f_meter = frequency.DummyFrequencyMeter(
            [60.0]*5+drop+bigDrop+bigRise+rise+[60.0]*2
        )

        previouslyShed = None
        # last_action_time = datetime.now()
        while True:
            f = get_frequency(f_meter)
            logger.info("Measurement: {}".format(f))
            # needs to be functionalized
            if f <= 59.995:
                if previouslyShed is None:
                    loads.SheddableLoad.shedByPriority(10)
                    previouslyShed = 10
                    logger.info("CONTINGENCY: loads of priority=10 are shed.")
                if (f <= 59.990) and (previouslyShed > 9):
                    loads.SheddableLoad.shedByPriority(9)
                    previouslyShed = 9
                    logger.info("CONTINGENCY: loads of priority>=9 are shed.")
                elif (f > 59.990) and (previouslyShed <= 9):
                    loads.SheddableLoad.restoreByPriority(9)
                    previouslyShed = 10
                    logger.info("RESTORE: loads of priority<=9 are restored.")
            else:
                if previouslyShed:
                    loads.SheddableLoad.restoreByPriority(10)
                    logger.info(
                        "RESTORE: loads of priority=10 restored" +
                        " contingency over."
                    )
                    previouslyShed = None

            sleep(10)
    except KeyboardInterrupt:
        logger.info("KeyboardInterrupt recieved... exiting.")

if __name__ == "__main__":
    run()
