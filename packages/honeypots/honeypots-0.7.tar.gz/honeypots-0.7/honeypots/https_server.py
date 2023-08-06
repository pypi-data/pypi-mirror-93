"""
//  -------------------------------------------------------------
//  author        Giga
//  project       qeeqbox/honeypots
//  email         gigaqeeq@gmail.com
//  description   app.py (CLI)
//  licensee      AGPL-3.0
//  -------------------------------------------------------------
//  contributors list qeeqbox/social-analyzer/graphs/contributors
//  -------------------------------------------------------------
"""

from warnings import filterwarnings
filterwarnings(action='ignore',module='.*OpenSSL.*')

from OpenSSL import crypto
from cgi import FieldStorage
from psutil import process_iter
from signal import SIGTERM
from requests import get,post
from requests.packages.urllib3 import disable_warnings
from time import sleep
from logging import DEBUG, basicConfig, getLogger
from tempfile import gettempdir,_get_candidate_names
from twisted.internet import reactor, ssl
from twisted.web.server import Site
from twisted.web.resource import Resource
from random import choice
from twisted.python import log as tlog
from subprocess import Popen
from socket import socket as ssocket
from socket import AF_INET,SOCK_STREAM
from pathlib import Path
from os import path
from honeypots.helper import server_arguments, get_free_port, CustomHandler
from uuid import uuid4

disable_warnings()

class QHTTPSServer():
	def __init__(self,ip=None,port=None,username=None,password=None,mocking=False,logs=None):
		self.ip= ip or '0.0.0.0'
		self.port = port or 443
		self.username = username or "test"
		self.password = password or "test"
		self.mocking = mocking or ''
		self.key = path.join(gettempdir(), next(_get_candidate_names()))
		self.cert = path.join(gettempdir(), next(_get_candidate_names()))
		self.random_servers = ['Apache','nginx','Microsoft-IIS/7.5','Microsoft-HTTPAPI/2.0','Apache/2.2.15','SmartXFilter','Microsoft-IIS/8.5','Apache/2.4.6','Apache-Coyote/1.1','Microsoft-IIS/7.0','Apache/2.4.18','AkamaiGHost','Apache/2.2.25','Microsoft-IIS/10.0','Apache/2.2.3','nginx/1.12.1','Apache/2.4.29','cloudflare','Apache/2.2.22']
		self.process = None
		self._logs = logs
		self.setup_logger(self._logs)
		self.disable_logger()

	def disable_logger(self):
		temp_name = path.join(gettempdir(), next(_get_candidate_names()))
		tlog.startLogging(open(temp_name, 'w'), setStdout=False)

	def setup_logger(self,logs):
		self.logs = getLogger('honeypotslogger'+'_'+__class__.__name__+'_'+str(uuid4())[:8])
		self.logs.setLevel(DEBUG)
		self.logs.addHandler(CustomHandler())

	def CreateCert(self,host_name, key, cert):
		pk = crypto.PKey()
		pk.generate_key(crypto.TYPE_RSA, 2048)
		c = crypto.X509()
		c.get_subject().C = 'US'
		c.get_subject().ST = 'OR'
		c.get_subject().L = 'None'
		c.get_subject().O = 'None'
		c.get_subject().OU = 'None'
		c.get_subject().CN = next(_get_candidate_names())
		c.set_serial_number(0)
		before, after = (0, 60*60*24*365*2)
		c.gmtime_adj_notBefore(before)
		c.gmtime_adj_notAfter(after)
		c.set_issuer(c.get_subject())
		c.set_pubkey(pk)
		c.sign(pk, 'sha256')
		open(cert, "wb").write(crypto.dump_certificate(crypto.FILETYPE_PEM, c))
		open(key, "wb").write(crypto.dump_privatekey(crypto.FILETYPE_PEM, pk))

	def https_server_main(self):
		_q_s = self

		class MainResource(Resource):

			isLeaf = True
			home_file = b'''
<!DOCTYPE html>
<html>
   <head>
      <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.0.0-beta.3/css/bootstrap.min.css" />
      <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css" />
      <meta http-equiv="content-type" content="text/html;charset=utf-8" />
      <title>Login</title>
      <style>
         body,html{height: 100%;text-align: center;},
      </style>
   </head>
   <body>
      <div class="container-fluid h-100">
         <div class="row justify-content-center h-100 align-items-center">
            <div class="col col-xl-3">
               <b>We'll back soon..</b> 
            </div>
         </div>
      </div>
   </body>
</html>'''

			login_file = b'''<!DOCTYPE html>
<html>
   <head>
      <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.0.0-beta.3/css/bootstrap.min.css" />
      <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css" />
      <meta http-equiv="content-type" content="text/html;charset=utf-8" />
      <title>Login</title>
      <style>body,html {height: 100%;}</style>
   </head>
   <body>
      <div class="container-fluid h-100">
         <div class="row justify-content-center h-100 align-items-center">
            <div class="col col-xl-3">
               <form id="login" action="" method="post">
                  <div class="form-group">
                     <input class="form-control form-control-sm" name="username" type="text" placeholder="username" id="username">
                  </div>
                  <div class="form-group">
                     <input class="form-control form-control-sm" name="password" type="password" placeholder="password" id="password">
                  </div>
                  <div class="form-group">
                     <button class="btn btn-default btn-sm btn-block" type="submit">login</button>
                  </div>
               </form>
            </div>
         </div>
      </div>
   </body>
</html>
'''

			if isinstance(_q_s.mocking, bool):
				if _q_s.mocking == True:
					server = choice(_q_s.random_servers)
			elif isinstance(_q_s.mocking, str):
				server = _q_s.mocking

			def render(self, request):

				headers = {}

				try:
					def check_bytes(string):
						if isinstance(string, bytes):
							return string.decode()
						else:
							return str(string)

					for item, value in dict(request.requestHeaders.getAllRawHeaders()).items():
						headers.update({check_bytes(item):','.join(map(check_bytes, value))})
				except:
					pass

				_q_s.logs.info(["servers",{'server':'http_server','action':'connection','ip':request.getClientIP(),'request':headers}])

				if self.server != "":
					request.responseHeaders.removeHeader("Server")
					request.responseHeaders.addRawHeader("Server", self.server)

				if request.method == b"GET":
					_q_s.logs.info(["servers",{'server':'https_server','action':'get','ip':request.getClientIP()}])
					if request.uri == b"/login.html":
						if _q_s.username != '' and _q_s.password != '':
							request.responseHeaders.addRawHeader("Content-Type", "text/html; charset=utf-8")
							return self.login_file

					request.responseHeaders.addRawHeader("Content-Type", "text/html; charset=utf-8")
					return self.home_file

				elif request.method == b"POST":
					self.headers = request.getAllHeaders()
					_q_s.logs.info(["servers",{'server':'https_server','action':'post','ip':request.getClientIP()}])
					if request.uri == b"/login.html":
						if _q_s.username != '' and _q_s.password != '':
							form = FieldStorage(fp=request.content,headers=self.headers,environ={'REQUEST_METHOD':'POST','CONTENT_TYPE':self.headers[b'content-type'],})
							if 'username' in form and 'password' in form:
								if form['username'].value == _q_s.username and form['password'].value == _q_s.password:
									_q_s.logs.info(["servers",{'server':'https_server','action':'login','status':'success','ip':request.getClientIP(),'username':_q_s.username,'password':_q_s.password}])
								else:
									_q_s.logs.info(["servers",{'server':'https_server','action':'login','status':'failed','ip':request.getClientIP(),'username':form['username'].value,'password':form['password'].value}])

					request.responseHeaders.addRawHeader("Content-Type", "text/html; charset=utf-8")
					return self.home_file
				else:
					request.responseHeaders.addRawHeader("Content-Type", "text/html; charset=utf-8")
					return self.home_file

		self.CreateCert("localhost", self.key, self.cert)
		ssl_context = ssl.DefaultOpenSSLContextFactory(self.key,self.cert)
		reactor.listenSSL(self.port, Site(MainResource()), ssl_context)
		reactor.run()

	def run_server(self,process=False,auto=False):
		if process:
			if auto:
				port = get_free_port()
				if port > 0:
					self.port = port
					self.process = Popen(['python3',path.realpath(__file__),'--custom','--ip',str(self.ip),'--port',str(self.port),'--username',str(self.username),'--password',str(self.password),'--mocking',str(self.mocking),'--logs',str(self._logs)])
					if self.process.poll() is None:
						self.logs.info(["servers",{'server':'https_server','action':'process','status':'success','route':'/login.html','ip':self.ip,'port':self.port,'username':self.username,'password':self.password}])
					else:
						self.logs.info(["servers",{'server':'https_server','action':'process','status':'error','ip':self.ip,'port':self.port,'username':self.username,'password':self.password}])
				else:
					self.logs.info(["servers",{'server':'https_server','action':'setup','status':'error','ip':self.ip,'port':self.port,'username':self.username,'password':self.password}])
			elif self.close_port() and self.kill_server():
				self.process = Popen(['python3',path.realpath(__file__),'--custom','--ip',str(self.ip),'--port',str(self.port),'--username',str(self.username),'--password',str(self.password),'--mocking',str(self.mocking),'--logs',str(self._logs)])
				if self.process.poll() is None:
					self.logs.info(["servers",{'server':'https_server','action':'process','status':'success','route':'/login.html','ip':self.ip,'port':self.port,'username':self.username,'password':self.password}])
				else:
					self.logs.info(["servers",{'server':'https_server','action':'process','status':'error','ip':self.ip,'port':self.port,'username':self.username,'password':self.password}])
		else:
			self.https_server_main()

	def kill_server(self,process=None):
		try:
			if self.process != None:
				self.process.kill()
			for process in process_iter():
				cmdline = ' '.join(process.cmdline())
				if '--custom' in cmdline and Path(__file__).name in cmdline:
					process.send_signal(SIGTERM)
					process.kill()
			return True
		except:
			pass
		return False

	def test_server(self,ip=None,port=None,username=None,password=None):
		try:
			sleep(2)
			_ip = ip or self.ip
			_port = port or self.port
			_username = username or self.username
			_password = password or self.password
			get('https://{}:{}'.format(_ip,_port),verify=False)
			post('https://{}:{}'.format(_ip,_port),data={'username': (None, _username),'password': (None, _password)},verify=False)
		except:
			pass

	def close_port(self):
		sock = ssocket(AF_INET,SOCK_STREAM)
		sock.settimeout(2) 
		if sock.connect_ex((self.ip,self.port)) == 0:
			for process in process_iter():
				try:
					for conn in process.connections(kind='inet'):
						if self.port == conn.laddr.port:
							process.send_signal(SIGTERM)
							process.kill()
				except:
					pass
		if sock.connect_ex((self.ip,self.port)) != 0:
			return True
		else:
			self.logs.error(['errors',{'server':'https_server','error':'port_open','type':'Port {} still open..'.format(self.ip)}])
			return False

if __name__ == '__main__':
	parsed = server_arguments()
	if parsed.docker or parsed.aws or parsed.custom:
		qhttpsserver = QHTTPSServer(ip=parsed.ip,port=parsed.port,username=parsed.username,password=parsed.password,mocking=parsed.mocking,logs=parsed.logs)
		qhttpsserver.run_server()