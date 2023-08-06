import logging

def setLogging(param: bool, log_level= logging.WARNING):
    if param:
        LOGFORMAT = "  s%(levelname)-8s%(reset)s | %(log_color)s%(message)s%(reset)s"
        stream = logging.StreamHandler()
        logging.root.setLevel(log_level)
        stream.setLevel(log_level)

        try:
            from colorlog import ColoredFormatter
            LOGFORMAT = "  %(log_color)s%(levelname)-8s%(reset)s | %(log_color)s%(message)s%(reset)s"
            formatter = ColoredFormatter(LOGFORMAT)
            stream.setFormatter(formatter)
        except:
            pass

        logger = logging.getLogger()
        logger.setLevel(log_level)
        logger.addHandler(stream)
