from GUIModule import GUI

import tornado.ioloop
import tornado.web
from pywebio.platform.tornado import webio_handler
from GUIModule.GUI import bmi


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

if __name__ == "__main__":
    application = tornado.web.Application([
        (r"/", MainHandler),
        (r"/bmi", webio_handler(bmi)),  # bmi is the same function as above
    ])
    application.listen(port=8080, address='62.109.6.117')
    tornado.ioloop.IOLoop.current().start()