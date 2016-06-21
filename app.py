#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import tornado.escape
import tornado.ioloop
import tornado.web
import sys
import os
from tornado.concurrent import Future
from tornado import gen
from tornado.options import define, options, parse_command_line

from zabbix import eventos

define("port", default=8081, help="run on the given port", type=int)
define("debug", default=True, help="run in debug mode")
title="Eventos ZabbixS"


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        from ConfigParser import SafeConfigParser
        parser = SafeConfigParser()
        parser.read('conf.ini')
        for section_name in parser.sections():
            self.write( '<br>Servidor = '+ section_name)
            self.write( '<br>    endereco = '+ parser.get(section_name,'endereco'))
            self.write( '<br>    usuario = '+ parser.get(section_name,'usuario'))
            self.write( '<br>    senha = '+ parser.get(section_name,'senha'))
            
            for t in eventos.get(parser.get(section_name,'endereco'),parser.get(section_name,'usuario'),parser.get(section_name,'senha')):
                if int(t['value']) == 1:
                    self.write("<br>" + t['hostname'])
                    self.write(" - "+t['description'])
                    self.write(" - "+str(t['unacknowledged']))

 

class ErrorHandler(tornado.web.RequestHandler):
    def get(self):
        msg="OPS"
        self.render("error.html",title=title,msg=msg)
    def post(self):
        self.write("OPS")




def main():
    settings = {
        'default_handler_class': ErrorHandler,
        'template_path': os.path.join(os.path.dirname(__file__), "template"),
        'cookie_secret': "__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
        'login_url': "/login"
    }
    parse_command_line()
    app = tornado.web.Application(
        [
            (r"/", MainHandler),
            (r"/favicon.ico", tornado.web.ErrorHandler, {'status_code': 404}),
            ],
        debug=options.debug,
        **settings
        )
    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()

