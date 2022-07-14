import logging

class MyHandler(logging.StreamHandler):
    def __init__(self):
        logging.StreamHandler.__init__(self)
        fmt = '[%(levelname)-8s] Line %(lineno)d of %(filename) -14s: %(message)s'
        formatter = logging.Formatter(fmt)
        self.setFormatter(formatter)