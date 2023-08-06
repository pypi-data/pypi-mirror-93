###########################################################################
#
# this module meant to provide general logging functions
#
###########################################################################

import logging


# will format the message to be suitable for the log messaged
def format_msg(msg):
    return f' {msg}'


class Logger:
    # logger instance
    logger = None

    '''
    :param __file__ -> set this to __file__ if you want the project name to be the logging name
    :param name -> set this if you want a custom name
    '''

    def __init__(self, __file__=None, name=None):
        if __file__ is None and name is None:
            raise Exception('ERROR: you must set instance or name for logging!')
        if __file__ is not None:
            import os.path
            import os_file_handler.file_handler as fh
            name = os.path.dirname(os.path.abspath(__file__))
            name = fh.get_file_name_from_path(name)
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(name)

    # log info
    def info(self, msg):
        self.logger.info(format_msg(msg))

    # log warning
    def warning(self, msg):
        self.logger.warning(format_msg(msg))

    # log developer devbug
    def debug(self, msg):
        self.logger.debug(format_msg(msg))
