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

from psutil import process_iter
from signal import SIGTERM
from argparse import ArgumentParser
from os import scandir
from socket import socket, AF_INET, SOCK_STREAM
from time import sleep
from json import JSONEncoder, dumps
from collections import Mapping
from logging import Handler
from sys import stdout
from pygments import highlight, lexers, formatters
from datetime import datetime

def clean_all():
	for entry in scandir('.'):
		if entry.is_file() and entry.name.endswith("_server.py"):
			kill_servers(entry.name)

def kill_servers(name):
	try:
		for process in process_iter():
			cmdline = ' '.join(process.cmdline())
			if '--custom' in cmdline and name in cmdline:
				process.send_signal(SIGTERM)
				process.kill()
		if self.process != None:
			self.process.kill()
	except:
		pass

def get_free_port():
	port = 0
	try:
		tcp = socket(AF_INET, SOCK_STREAM)
		tcp.bind(('', 0))
		addr, port = tcp.getsockname()
		tcp.close()
	except:
		pass
	return port

def server_arguments():
	_server_parser = ArgumentParser(prog="Server")
	_server_parsergroupdeq = _server_parser.add_argument_group('Initialize Server')
	_server_parsergroupdeq.add_argument('--ip',type=str, help="Change server ip, current is 0.0.0.0", required=False,metavar='')
	_server_parsergroupdeq.add_argument('--port',type=int, help="Change port", required=False,metavar='')
	_server_parsergroupdeq.add_argument('--username',type=str, help="Change username", required=False,metavar='')
	_server_parsergroupdeq.add_argument('--password',type=str, help="Change password", required=False,metavar='')
	_server_parsergroupdeq.add_argument('--resolver_addresses',type=str, help="Change resolver address", required=False,metavar='')
	_server_parsergroupdeq.add_argument('--domain',type=str, help="A domain to test", required=False,metavar='')
	_server_parsergroupdeq.add_argument('--mocking',type=str, help="Random banner", required=False)
	_server_parsergroupdes = _server_parser.add_argument_group('Sinffer options')
	_server_parsergroupdes.add_argument('--filter',type=str, help="setup the Sinffer filter", required=False)
	_server_parsergroupdes.add_argument('--interface',type=str, help="sinffer interface E.g eth0", required=False)
	_server_parsergroupdef = _server_parser.add_argument_group('Initialize Loging')
	_server_parsergroupdef.add_argument('--logs',type=str, help="db, terminal or all", required=False, default="terminal")
	_server_parsergroupdea = _server_parser.add_argument_group('Auto Configuration')
	_server_parsergroupdea.add_argument('--docker',action='store_true', help="Run project in docker", required=False)
	_server_parsergroupdea.add_argument('--aws',action='store_true', help="Run project in aws", required=False)
	_server_parsergroupdea.add_argument('--test',action='store_true', help="Test current server", required=False)
	_server_parsergroupdea.add_argument('--custom',action='store_true', help="Run custom server", required=False)
	_server_parsergroupdea.add_argument('--auto',action='store_true', help="Run auto configured with random port", required=False)
	return _server_parser.parse_args()

class ComplexEncoder(JSONEncoder):
	def default(self, obj):
		if isinstance(obj, bytes):
			return obj.decode()
		else:
			return repr(obj)
		return JSONEncoder.default(self, obj)

class CustomHandler(Handler):
	def __init__(self):
		Handler.__init__(self)

	def emit(self, record):
		try:
			time_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
			if record.msg[0] == "servers":
				if "server" in record.msg[1]:
					temp = record.msg[1]
					action = record.msg[1]['action']
					server = temp['server'].replace('server','').replace('_','')
					del temp['server']
					del temp['action']
					stdout.write("[{}] [{}] [{}] -> {}\n".format(time_now,server,action,dumps(temp, sort_keys=True, cls=ComplexEncoder)))
			else:
				stdout.write(dumps(record.msg, sort_keys=True,cls=ComplexEncoder))
		except Exception as e:
			stdout.write(dumps({"logger":repr(record)}, sort_keys=True,cls=ComplexEncoder))
		stdout.flush()

	def emit_old(self, record):
		try:
			if record.msg[0] == "servers":
				if "server" in record.msg[1]:
					temp = record.msg[1]
					server = temp['server']
					del temp['server']
					stdout.write(highlight(dumps({server:temp}, sort_keys=True,indent=4,cls=ComplexEncoder), lexers.JsonLexer(), formatters.TerminalFormatter()))
			else:
				stdout.write(highlight(dumps(record.msg, sort_keys=True,indent=4,cls=ComplexEncoder), lexers.JsonLexer(), formatters.TerminalFormatter()))
		except Exception as e:
			stdout.write(highlight(dumps({"logger":repr(record)}, sort_keys=True,indent=4,cls=ComplexEncoder), lexers.JsonLexer(), formatters.TerminalFormatter()))
		stdout.flush()