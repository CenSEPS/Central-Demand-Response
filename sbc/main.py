"""Main Server Logic"""

import logging
import logging.config
from datetime import datetime
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

from . import frequency

logger = logging.getLogger(name='sbc')


def get_frequency(meter):
    return meter.get_data()

if __name__ == "__main__":
    # initialize
    f_meter = frequency.DummyFrequencyMeter([60]*500)
    last_action = datetime.now()

    # event loop
    try:
        while True:
            # calculate elapsed time

            # if 1 s has passed, get new f reading
            f = get_frequency(f_meter)

            # log some stuff
            logger.info("Measurement: {}".format(f))
            sleep(1)
    except KeyboardInterrupt:
        logger.info("KeyboardInterrupt recieved... exiting")
