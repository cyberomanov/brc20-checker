from utils import *

if __name__ == '__main__':
    add_logger(version='v1.2')
    try:
        asyncio.run(main_checker())
    except Exception as e:
        logger.exception(e)
