from tornado.web import RequestHandler

import logging
from tornado.log import LogFormatter

from model import db


class BaseHandler(RequestHandler):
    def initialize(self):
        '''
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)

        datefmt = '%Y-%m-%d %H:%M:%S'
        fmt = '%(color)s[%(levelname)1.1s %(asctime)s]%(end_color)s %(message)s'
        formatter = LogFormatter(color=True, datefmt=datefmt, fmt=fmt)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        logdir = os.path.join(self.settings['static_path'], "../logs")
        file_handler = logging.FileHandler(os.path.join(logdir, 'debug.log'))
        file_handler.setFormatter(formatter)

        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)
        '''
        super(BaseHandler, self).initialize()

    def prepare(self):
        if db.is_closed():
            db.connect()
        super(BaseHandler, self).prepare()

    def on_finish(self):
        if not db.is_closed():
            db.close()
        super(BaseHandler, self).on_finish()

    def write_error(self, status_code, **kwargs):
        if "result" in kwargs.keys():
            self.finish("%(message)s" % {"message": kwargs['result']})
        else:
            self.finish("%(message)s" % {"message": "internal error"})

