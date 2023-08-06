import logging

logging.getLogger('requests.packages.urllib3').setLevel(logging.WARNING)


class LoggingModule:

    def __init__(self):
        logger = logging.getLogger()
        handler = logging.StreamHandler()
        logging.basicConfig(
            format='%(asctime)s.%(msecs)s:%(name)s:%(thread)d:%(levelname)s:%(process)d:%(message)s',
            level=logging.INFO
        )
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        self.logger = logger

    def log_msg(self, level=None, *args):
        """
        logger.debug('debug message')
        logger.info('info message')
        logger.warn('warn message')
        logger.error('error message')
        logger.critical('critical message')
        """
        if level == 'debug':
            return self.logger.debug(args)
        elif level == 'info':
            return self.logger.info(args)
        elif level == 'warn':
            return self.logger.warn(args)
        elif level == 'error':
            return self.logger.error(args)
        elif level == 'critical':
            return self.logger.critical(args)
        else:
            return self.logger.debug(args)
