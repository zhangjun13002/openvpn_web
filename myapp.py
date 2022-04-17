import os
from tornado.web import Application
import tornado.ioloop
import tornado.httpserver
from tornado.options import define, options

from utils.sche import sche_init

from handler.default import LoginHandler, MainHandler, AdminHandler
from handler.user import KeyHandler, UserHandler
from handler.user import AddHandler, GenHandler, UpdateHandler, DelHandler
from handler.user import LogsHandler
from handler.settings import SmtpHandler, WarnHandler

define("port", default=8000, help="port to listen on")
curpath = os.path.dirname(os.path.realpath(__file__))

def main():
    sche_init()
    setting = {
        #"autoreload": True,
        "debug": True,
        "template_path": os.path.join(curpath, "templates"),
        "static_path": os.path.join(curpath, "static"),
        "xsrf_cookies": False,
        "rootdir": curpath,
        "rsa3dir": os.path.join(curpath, "easyrsa3")
    }
    app = Application([
        (r"/login", LoginHandler),
        (r"/key", KeyHandler),
        (r"/", MainHandler),
        (r"/admin", AdminHandler),
        (r"/user", UserHandler),        
        (r"/add", AddHandler),
        (r"/gen", GenHandler),
        (r"/op", UpdateHandler),
        (r"/del", DelHandler),
        (r"/logs", LogsHandler),
        (r"/smtp", SmtpHandler),
        (r"/warn", WarnHandler)
    ], **setting)

    server = tornado.httpserver.HTTPServer(app)
    server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    main()