#!/usr/bin/python
from tornado.wsgi import WSGIContainer
from tornado.ioloop import IOLoop
from tornado.web import FallbackHandler, RequestHandler, Application
from tornado.httpserver import HTTPServer

from register import app

tr = WSGIContainer(app)

application = Application([
	(r".*", FallbackHandler, dict(fallback=tr)),
])

try:
    http_server = HTTPServer(application, ssl_options={'certfile': 'ca_ctjb.crt', 'keyfile': 'ca_ctjb.key'})
    print('Running SSL server ...')
except:
    http_server = HTTPServer(application)
    print('Running HTTP server ...')

if __name__ == "__main__":
	http_server.listen(4433, address='0.0.0.0')
	IOLoop.instance().start()
