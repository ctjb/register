#!/usr/bin/python
from OpenSSL import SSL
context = SSL.Context(SSL.SSLv23_METHOD)
context.use_privatekey_file('ca_ctjb.key')
context.use_certificate_file('ca_ctjb.crt')

from register import app

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=4433, debug=True, ssl_context=context)
