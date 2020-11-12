# import socket
# import sys
import os
# import threading
import datetime
import time
import gzip
import logging
import mimetypes
import urllib
import pathlib
from requests_toolbelt.multipart import decoder
import hashlib
import random
import string
import base64

from conf import *

def use_logger(access=1, post=0, error=0):
	if post == 1:
		filename = f"{BASE_DIR}/log/post.log"
		LOG_FORMAT = "%(levelname)s %(asctime)s : %(message)s"
		logging.basicConfig(filename=filename, level=logging.DEBUG, format=LOG_FORMAT)

	elif error == 1:
		filename = f"{BASE_DIR}/log/error.log"
		logging.basicConfig(filename=filename, level=logging.DEBUG, format='[%(asctime)s] %(message)s', datefmt='%a %b %d %H:%M:%S %Y')
		# [Wed Nov 11 12:31:58.467192 2020]
		# [%a %b %d %H:%M:%S %Y]
	elif access ==  1:
		filename = f"{BASE_DIR}/log/access.log"
		logging.basicConfig(filename=filename, level=logging.DEBUG, format='127.0.0.1 - - [%(asctime)s] %(message)s', datefmt='%d/%b/%Y:%H:%M:%S %z')
		# LOG_FORMAT = ""
	
	return logging.getLogger()

# reference : https://thispointer.com/python-get-last-modification-date-time-of-a-file-os-stat-os-path-getmtime/
def last_modified_time(filename):
	mod_time = os.path.getmtime(filename)
	last_modified = time.strftime("%a, %d %b %Y %X GMT", time.gmtime(mod_time))
	return last_modified

class RequestHandler():
	method = "INVALID"
	connection = "Keep-Alive"
	gmtime = time.strftime("%a, %d %b %Y %X GMT", time.gmtime())
	content_length = 0
	content = None
	content_type = "text/html"
	scheme = "HTTP/1.1"
	status_type = "Not Implemented"
	status_code = 501
	request_line = None
	parsed = None
	headers = {}
	
	def __init__(self, message, client=None):
		print("REQUEST : ")
		print(message)
		self.message = message
		self.setsetters(message)

	
	def setsetters(self, message):
		message = message.split("\r\n\r\n")

		if len(message) > 1:
			# If the message body contains something separated by \r\n\r\n
			self.parameters = '\r\n\r\n'.join(message[1:])
		
		else:
			self.parameters = None

		msg = message[0].split("\r\n")

		self.setmethod(msg[0])

		if len(msg) > 1:
			self.setheaders(msg[1:])

	def setmethod(self, msg):
		self.request_line = msg
		msg = msg.split(" ")	
		if len(msg) != 3 or msg[2] != "HTTP/1.1":
			# print("STEP 1")
			self.setstatuscodeandtype(400)
			return

		if msg[0] not in ALLOWED_METHODS:
			# print("STEP 2")
			if msg[0] in NOT_IMPLEMENTED_METHODS:
				# print("STEP 3")
				self.setstatuscodeandtype(501)
				
			else:
				# print("STEP 4")
				self.setstatuscodeandtype(405)
				
			return

		# print("STEP 5")
	
		self.setstatuscodeandtype(200)
		
		self.method = msg[0]

		path = msg[1]
		
		if path == "/":
			path = BASE_DIR + "/index.html"
		
		elif path == "/favicon.ico":
			path = BASE_DIR + "/Images/favicon.ico"
		
		else:
			path = BASE_DIR + path
		
		if os.path.exists(path) or self.method == "PUT":
			# print("STEP 6")
			self.content_type = mimetypes.guess_type(path)[0]
			self.path = path
			self.setstatuscodeandtype(200)

		else:
			# print("STEP 7")
			self.setstatuscodeandtype(404)
			


	def setheaders(self, request_headers):
		for head in request_headers:
			head = head.split(":")
			if len(head) > 1:
				head0 = head[0].lower().strip()
				if head0 == "authorization":
					self.headers[head0] = head[1]
				else:
					self.headers[head[0].lower().strip()] = head[1].lower().strip()

		try :
			self.connection = self.headers["connection"]

		except KeyError:
			print("Exception 12")
			pass

		try :
			# host must be present
			self.headers["host"]
		except KeyError:
			self.setstatuscodeandtype(400)

	def readfile(self, only_length=False, is_error=False):
		# Returns true if successful

		# If there is error then we want to format the default message and send accordingly
		if is_error:
			self.content_type = 'text/html'
			self.content = ERROR_RESPONSE %{'code' : self.status_code, 'explain' : self.status_type}
			self.content_length = len(self.content)		
			return True


		# Else read everything in binary and store for further use
		try :
			with open(self.path, 'rb') as f:
				self.content_length = os.path.getsize(self.path)
				# For HEAD request we don't need body
				if only_length:
					return True
				self.content = f.read()
		except Exception as e:
			# print(f"Exception 1 : {e}")
			self.logdata(err_msg=e, err_resp='resuming operations')
			self.setstatuscodeandtype(405)
			return False
		return True

	def logdata(self, err_msg = None, err_resp = None):
		if not (err_msg is None and err_resp is None):
			logger = use_logger(access=0, post=0, error=1)
			logger.error(f'[{err_msg}] -- {err_resp}')
			return 
		# logging.basicConfig(format='127.0.0.1 - - %(asctime)s %(message)s', datefmt='[%d/%b/%Y:%H:%M:%S %z')
		logger = use_logger(access=1, error=0, post=0)
		msg = f"\"{self.request_line}\" {self.status_code} {self.content_length} \"-\" \"-\""
		logger.info(msg)
		if self.method == "POST":
			logger = use_logger(post=1, access=0, error=0)
			logger.info(self.parsed)




	def check_cookie(self):
		try:
			cookie = self.headers["cookie"]
			cookie = cookie.split("=")[1]
			with open('cookies.txt', 'r') as f:
				lines = f.readlines()
				for line in lines:
					# Cookie Is Valid
					if line == cookie:
						print("Cookie FOUND")
						return True
				# Invalid Cookie Sent
				return False
		except KeyError:
			# We need to set cookie
			return None

	def create_cookie(self):
		return ''.join(random.SystemRandom().choice(string.ascii_lowercase + string.digits) for _ in range(18))


	def savecookie(self, cookie):
		with open('cookies.txt', 'a') as f:
			f.write(cookie + "\n")

	def cookie_handler(self):
		check = self.check_cookie()
		if check is False:
			# Sent cookie that doesn't exist
			check = None

		if check is None:
			cookie = "atharvas_cookie=" + self.create_cookie()
			cookie = "Set-Cookie: atharvas_cookie=" + self.create_cookie() + CRLF
			self.savecookie(cookie)

		if check is True:
			cookie = ''

		return cookie

	def response_line(self):
		return f"{self.scheme} {self.status_code} {self.status_type}"

	def setstatuscodeandtype(self, status_code):
		self.status_code = status_code
		self.status_type = STATUS[status_code]
		
	def GET_method(self):
		if self.path in CONFIDENTIAL:
			try :
				x = self.headers["authorization"]
				# x = x.split("Base ")
				print(x)
				x = x.split("Basic ")
				print(x)
				data = base64.b64decode(x[1])
				print(data)
				data = data.decode()
				print(data)
				# print("intermidiate : ", data)
				data = data.split(":")
				print(data)
				if not (data[0] == USER and data[1] == PASSWORD):
					self.setstatuscodeandtype(403)
					return self.error_handler()
			except KeyError:
				self.setstatuscodeandtype(401)
				return self.error_handler()
		cookie = self.cookie_handler()			

		# About 304 response header fields
		# https://tools.ietf.org/html/rfc7232#section-4.1
		
		success = self.readfile()
		if not success:
			# print("Request was unsuccessful")
			return self.error_handler()
		# response_headers = f"{d.getstatus()}\r\n{d.acceptranges()}\r\n{d.getconnection()}\r\nDate: {d.gettime()}\r\nServer: {SERVER_NAME}\r\nContent-Length: {d.getcontentlength()}\r\nContent-Type: {d.getcontenttype()}\r\n\r\n"
		# print(f"GET method for : {self.path}")
		# print(f"Setting etag : {self.getetag()}")

	
		response_headers = f"{self.response_line()}{CRLF}Connection: {self.connection}{CRLF}Accept-Ranges: bytes{CRLF}Date: {self.gmtime}{CRLF}Server: {SERVER_NAME}{CRLF}Content-Length: {self.content_length}{CRLF}Content-Type: {self.content_type}{CRLF}ETag: {self.getetag()}{CRLF}Last-Modified: {last_modified_time(self.path)}{CRLF}{CRLF}"
		response_body = self.content
		self.logdata()
		return [response_headers.encode(), response_body]

	def POST_method(self):
		# print("POST METHOD CALLED")
		cookie = self.cookie_handler()
		params = ''
		if self.parameters:
			try :
				if self.headers["content-type"] == "application/x-www-form-urlencoded":
					params = urllib.parse.parse_qs(self.parameters)
					self.parsed = params
				else:
					self.setstatuscodeandtype(201)
					response_headers = f"{self.response_line()}{CRLF}Connection: {self.connection}{CRLF}Accept-Ranges: bytes{CRLF}{cookie}Date: {self.gmtime}Server: {SERVER_NAME}{CRLF}{CRLF}"
					return [response_headers.encode()]
			except KeyError:
				# print("Exception 3")
				params = urllib.parse.parse_qs(self.parameters)
		else:
			# Use proper error here
			self.setstatuscodeandtype(400)
			
			return self.error_handler()

		if len(self.parameters) > 0 and len(params) == 0: # If user gave random string e.g. "fa3489208098afs"
			self.setstatuscodeandtype(400)
			return self.error_handler()

		# logger = use_logger("POST")
		# logger.info(params)

		self.setstatuscodeandtype(201) # Or No Content
		response_headers = f"{self.response_line()}{CRLF}Connection: {self.connection}{CRLF}Date: {self.gmtime}{CRLF}{cookie}Server: {SERVER_NAME}{CRLF}Content-Type: text/html{CRLF}Content-Length: 0{CRLF}{CRLF}"
		self.logdata()
		return [response_headers.encode()]

	def HEAD_method(self):
		cookie = self.cookie_handler()
		# print("HEAD METHOD CALLED")
		success = self.readfile(only_length=True)
		if not success:
			return self.error_handler()
		response_headers = f"{self.response_line()}{CRLF}Connection: {self.connection}{CRLF}Accept-Ranges: bytes{CRLF}Date: {self.gmtime}Server: {SERVER_NAME}{CRLF}{cookie}Content-Length: {self.content_length}{CRLF}Content-Type: {self.content_type}{CRLF}{CRLF}"
		self.logdata()
		return [response_headers.encode()]

	def DELETE_method(self):
		cookie = self.cookie_handler()
		# print("DELETE METHOD CALLED")
		b = os.path.exists(self.path)
		if b:
			# Not all files can be deleted
			if self.path in NON_EDITABLE:
				self.setstatuscodeandtype(405)
				return self.error_handler()
			

			try :
				os.remove(self.path)
				self.setstatuscodeandtype(204)
				self.readfile(is_error=True)
				response_headers = f"{self.response_line()}{CRLF}Connection: {self.connection}{CRLF}Content-Type: {self.content_type}{CRLF}Content-Length: {self.content_length}{CRLF}{cookie}Date: {self.gmtime}{CRLF}Server: {SERVER_NAME}{CRLF}{CRLF}"
				response_body = self.content
				self.logdata()
				return [response_headers.encode(), response_body.encode()]

			except IsADirectory:
				# print("Exception 4")
				# print("Directory Cannot be removed")
				self.setstatuscodeandtype(405)
				return self.error_handler()

		# If file doesn't exist
		else:
			self.setstatuscodeandtype(405)
			return self.error_handler()
		pass

	def PUT_method(self):
		cookie = self.cookie_handler()
		# print("PUT METHOD CALLED")

		b = os.path.exists(self.path) # Check if resource already exists
		
		# An origin server that allows PUT on a given target resource MUST send
		#  a 400 (Bad Request) response to a PUT request that contains a
		#  Content-Range header field (Section 4.2 of [RFC7233])
		# print(self.headers)
		try :
			self.headers["content-range"]
			self.setstatuscodeandtype(400)
			
			# print("Here We Go Again")
			return self.error_handler()

		except KeyError:
			# print("Exception 5")
			# print("Key Error")
			pass

		if self.path in NON_EDITABLE:
			# Since file is used by server this file can't be edited and this method
			# is not implemented for this particular file
			self.setstatuscodeandtype(405)
			
			return self.error_handler()
		try:
			print(f"For PUT self.path = {self.path}")
			p4 = f"{self.path}"
			path = pathlib.Path(p4)
			path.parent.mkdir(parents=True, exist_ok=True)
			with open(self.path, 'w') as f:
				f.write(self.parameters)
			
			if b: # Resource already exists
				self.setstatuscodeandtype(200)
				
			
			else: # Resource created
				self.setstatuscodeandtype(201)
			
		except Exception as e:

			# print("Exception 6")
			print(f"Exception {e} has occured in PUT")
			self.setstatuscodeandtype(500)
			
			return self.error_handler()

		response_headers = f"{self.response_line()}{CRLF}Connection: {self.connection}{CRLF}Content-Type: {self.content_type}{CRLF}Content-Length: {self.content_length}{CRLF}{cookie}Date: {self.gmtime}{CRLF}Server: {SERVER_NAME}{CRLF}{CRLF}"
		self.logdata()
		return [response_headers.encode()]

	def INVALID_method(self):
		# print("INVALID METHOD CALLED")
		# self.logdata()
		return self.error_handler()

	def error_handler(self):
		# print(f"error_handler METHOD CALLED FOR {self.status_code} - {self.status_type}")
		self.readfile(is_error=True)
		response_headers= f"{self.response_line()}{CRLF}Connection: {self.connection}{CRLF}Content-Type: {self.content_type}{CRLF}Content-Length: {self.content_length}{CRLF}Date: {self.gmtime}{CRLF}Server: {SERVER_NAME}{CRLF}"
		
		if self.status_code == 401:
			response_headers += f"WWW-Authenticate: Basic realm=\"User Visible Realm\", charset=\"UTF-8\"{CRLF}"

		response_body = self.content
		self.logdata()
		return [response_headers.encode(), response_body.encode()]

	def INTERNAL_SERVAR_ERROR(self):
		self.status_code = 500
		self.status_type = "Internal Server Error"
		return self.error_handler()

	def RAISE_ERROR(self, status_code=500):
		self.setstatuscodeandtype(status_code)
		return self.error_handler()

	def response(self):

		if self.status_code != 200:
			request_method = self.INVALID_method

		else:
			try:
				request_method = getattr(self, '%s_method' % self.method)

			except AttributeError:
				# print("Exception 8")
				self.logdata(error=1)
				request_method = self.INVALID_method

		return request_method()

	def getmethod(self):
		return self.method
	
	def getconnection(self):
		return self.connection
	
	def gettime(self):
		return self.gmttime
	
	def getstatus(self):
		return f"HTTP/1.1 {self.status_code} {self.status_type}"
	
	def getcontent(self):
		return self.content
	
	def getcontentlength(self):
		return self.content_length
	
	def getcontenttype(self):
		return self.content_type
		
	def acceptranges(self):
		return "Accept-Ranges: bytes"
	
	def getconnection(self):
		return self.connection
	
	def getencoding(self):
		pass
	
	def getetag(self):
		with open(self.path, 'rb') as f:
			data = f.read()
		hashed = hashlib.md5(data).hexdigest()
		# last_modified = last_modified_time(self.path).replace(' ', '')
		# last_modified.strip()
		# last_modified.replace(' ', '')
		# last_modified.replace(',', '')
		# last_modified.replace(':', '')
		return "\"" + hashed + "\""