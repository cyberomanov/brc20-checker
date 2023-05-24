from utils import *

if __name__ == '__main__':
    add_logger(version='v1.0')
    try:
        main_checker()
    except Exception as e:
        logger.exception(e)
