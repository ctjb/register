#!/usr/bin/python
from register import app

context = ('ca_ctjb.crt', 'ca_ctjb.key')

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=4433, debug=True, ssl_context=context)
