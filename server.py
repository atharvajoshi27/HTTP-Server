import socket
import sys
import os
import threading
import datetime
import time
import gzip
import logging
import mimetypes
import urllib

def use_logger(method):
	if method == "POST":
		LOG_FORMAT = LOG_FORMAT = "%(levelname)s %(asctime)s : %(message)s"
		logging.basicConfig(filename='POST_DATA.log', level=logging.DEBUG, format=LOG_FORMAT)
		return logging.getLogger()

ERROR_RESPONSE = """
				<!DOCTYPE html>
				<html>
				    <head>
				        <meta http-equiv="Content-Type" content="text/html;charset=utf-8">
				        <title>Error response</title>
				    </head>
				    <body>
				    	<p><b>%(code)s</b>. %(explain)s.</p>
				    	<p>ERROR_HAS_OCCURED</p>
				    </body>
				</html>
				"""
# https://www.w3.org/Protocols/rfc2616/rfc2616-sec4.html#sec4.2

SERVER_NAME = "Atharva's Server"

BASE_DIR = "/home/atharva/Study/Sem_5/CN/HTTP-Server"

CRLF = "\r\n"

class RequestHandler():
	method = "INVALID"
	path = "/notimplemented.html"
	connection = "Keep-Alive"
	server = SERVER_NAME
	root = BASE_DIR
	gmtime = time.strftime("%a, %d %b %Y %X GMT", time.gmtime())
	content_length = 0
	content = None
	content_type = "text/html"
	scheme = "HTTP/1.1"
	status_type = "Not Implemented"
	status_code = 501
	filemode = 'rb'
	accept_ranges = "bytes"
	allowed_methods = ["GET", "POST", "HEAD", "PUT", "DELETE",]
	not_implemented_methods = ["CONNECT", "OPTIONS", "TRACE", "PATCH", ]
	# types = {
	# 	"get" : "GET",
	# 	"head" : "HEAD", 
	# 	"post" : "POST",
	# 	"put" : "PUT",
	# 	"delete" : "DELETE",
	# }
	
	headers = {}
	
	def __init__(self, message=None):
		# print("MESSAGE: ")
		# print(message)
		self.setsetters(message)
		# message = message.split("\r\n")
		# method_info = message[0].split(" ")
		# print("METHOD INFO: ", method_info)

		# self.setmethod(message[0])
		# self.setfile(message[0])
		# if len(message) > 1:
		# 	self.setheaders(message[1:])	
		# self.callmethod()
	def setsetters(self, message):
		message = message.split("\r\n\r\n")
		if len(message) > 1:
			self.parameters = message[1]
		else:
			self.parameters = ''

		msg = message[0].split("\r\n")

		self.setmethod(msg[0])
	
		# self.setfile(msg[0])

		if len(msg) > 1:
			self.setheaders(msg[1:])

		# print("CHECK :", message)
		# print(len(message))

	def setmethod(self, msg):
		print("msg : ", msg)
		msg = msg.split(" ")
		# print(msg)
		# print(len(msg))
		# print(msg[2])
		# msg = msg.lower().split(" ")
		if len(msg) != 3 or msg[2] != "HTTP/1.1":
			print("STEP 1")
			self.status_type = "Bad Request"
			self.status_code = 400
			return

		if msg[0] not in self.allowed_methods:
			print("STEP 2")
			if msg[0] in self.not_implemented_methods:
				print("STEP 3")
				self.status_code = 501
				self.status_type = "Not Implemented"
			else:
				print("STEP 4")
				self.status_code = 405
				self.status_type = "Method Not Allowed"
			return

		print("STEP 5")
		self.status_code = 200
		self.status_type = "OK"
		self.method = msg[0]


		path = msg[1]
		
		if path == "/":
			path = BASE_DIR + "/index.html"
		
		elif path == "/favicon.ico":
			path = BASE_DIR + "/Images/favicon.ico"
		
		else:
			path = BASE_DIR + path
		
		print("path: ", path)
		if os.path.exists(path):
			self.content_type = mimetypes.guess_type(path)[0]
			self.path = path
			self.status_code = 200
			self.status_type = "OK"

		else:
			self.status_code = 404
			self.status_type = "Not Found"

	
	def setfile(self, msg):
		if self.status_code == 501:
			path = BASE_DIR + "/notimplemented.html"

		elif self.status_code == 400:
			path = BASE_DIR + "/badrequest.html"

		else:
			msg = msg.split(" ")
			path = msg[1]

			if path == "/":
				path = "/index.html"

			elif path == "/favicon.ico":
				path = "/Images/favicon.ico"
			
			path = BASE_DIR + path
			
			if os.path.exists(path): # and self.status_code == 200:
				ext = os.path.splitext(path)[1]
				# print(f"Extension is : {ext}")
				if ext == '.png':
					self.content_type = "image/png"

				elif ext == '.ico':
					self.content_type = 'image/x-icon'
					
				elif ext == '.jpeg' or ext == '.jpg':
					self.content_type = "image/jpeg"

			else:
				self.status_type = "Not Found"
				self.status_code = 404
				path = BASE_DIR + "/notfound.html"

		self.path = path

	def setheaders(self, request_headers):
		for head in request_headers:
			head = head.split(": ")
			# print(head, end=" ")
			if len(head) > 1:
				self.headers[head[0].lower()] = head[1].lower()

		try :
			self.connection = self.headers["connection"]

		except KeyError:
			pass
		print("")
		# with open(path, self.filemode) as f:
		# 	self.content = f.read()
		# 	self.content_length = len(self.content)
	def readfile(self, only_length=False, is_error=False):
		if is_error:
			self.content_type = 'text/html'
			self.content = ERROR_RESPONSE %{'code' : self.status_code, 'explain' : self.status_type}
			self.content_length = len(self.content)
			return
		self.content_length = os.path.getsize(self.path)
		if only_length:
			return
		with open(self.path, 'rb') as f:
			self.content = f.read()

	def response_line(self):
		return f"{self.scheme} {self.status_code} {self.status_type}"

	def GET_method(self):
		print("GET METHOD CALLED")
		self.readfile()
		# response_headers = f"{d.getstatus()}\r\n{d.acceptranges()}\r\n{d.getconnection()}\r\nDate: {d.gettime()}\r\nServer: {SERVER_NAME}\r\nContent-Length: {d.getcontentlength()}\r\nContent-Type: {d.getcontenttype()}\r\n\r\n"
		response_headers = f"{self.response_line()}{CRLF}Connection: {self.connection}{CRLF}Accept-Ranges: bytes{CRLF}Date: {self.gmtime}Server: {SERVER_NAME}{CRLF}Content-Length: {self.content_length}{CRLF}Content-Type: {self.content_type}{CRLF}{CRLF}"
		response_body = self.content

		return [response_headers.encode(), response_body]

	def POST_method(self):
		print("POST METHOD CALLED")
		if self.parameters:
			params = urllib.parse.parse_qs(self.parameters)
		else:
			# Use proper error here
			self.status_code = 400
			self.status_type = "Bad Request"
			return
		logger = use_logger("POST")
		logger.info(params)
		self.status_code = 201 
		self.status_type = "Created" # "No Content"
		response_headers = f"{self.response_line()}{CRLF}Connection: {self.connection}{CRLF}Date: {self.gmtime}{CRLF}Server: {SERVER_NAME}{CRLF}Content-Type: text/html{CRLF}Content-Length: 0{CRLF}{CRLF}"
		return [response_headers.encode()]

	def HEAD_method(self):
		print("HEAD METHOD CALLED")
		self.readfile(only_length=True)
		response_headers = f"{self.response_line()}{CRLF}Connection: {self.connection}{CRLF}Accept-Ranges: bytes{CRLF}Date: {self.gmtime}Server: {SERVER_NAME}{CRLF}Content-Length: {self.content_length}{CRLF}Content-Type: {self.content_type}{CRLF}{CRLF}"
		return [response_headers.encode()]

	def DELETE_method(self):
		print("DELETE METHOD CALLED")
		pass

	def PUT_method(self):
		print("PUT METHOD CALLED")
		pass

	def INVALID_method(self):
		print("INVALID METHOD CALLED")
		status_code = self.status_code
		try:
			errorm = getattr(self, "error_%s" %status_code)

		except AttributeError:
			errorm = self.error_501

		return errorm()
		# if status_code == 400:
		# 	return self.400_error()
		
		# elif status_code == 404:
		# 	return self.404_error()

		# else:
		# 	return self.501_error()

	def error_501(self):
		print("error_501 METHOD CALLED")
		self.readfile(is_error=True)
		response_headers= f"{self.response_line()}{CRLF}Connection: {self.connection}{CRLF}Content-Type: {self.content_type}{CRLF}Content-Length: {self.content_length}{CRLF}Date: {self.gmtime}{CRLF}Server: {SERVER_NAME}{CRLF}{CRLF}"
		response_body = self.content

		return [response_headers.encode(), response_body]

	def error_404(self):
		print("error_404 METHOD CALLED")
		self.readfile(is_error=True)
		response_headers = f"{self.response_line()}{CRLF}Connection: {self.connection}{CRLF}Content-Type: {self.content_type}{CRLF}Content-Length: {self.content_length}{CRLF}Date: {self.gmtime}{CRLF}Server: {SERVER_NAME}{CRLF}{CRLF}"
		response_body = self.content

		return [response_headers.encode(), response_body]

	def error_400(self):
		print("error_400 METHOD CALLED")
		self.readfile(is_error=True)
		response_headers = f"{self.response_line()}{CRLF}Connection: {self.connection}{CRLF}Content-Type: {self.content_type}{CRLF}Content-Length: {self.content_length}{CRLF}Date: {self.gmtime}{CRLF}Server: {SERVER_NAME}{CRLF}{CRLF}"
		response_body = self.content

		return [response_headers.encode(), response_body]

	def response(self):
		try:
			request_method = getattr(self, '%s_method' % self.method)

		except AttributeError:
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
		return f"Connection: {self.connection}"
	
	def getencoding(self):
		pass
	
	def getetag(self):
		pass
	
	def getvary(self):
		pass


def Listen(client, address):
	while True:
		try:
			message = client.recv(4096).decode()
			
			d = RequestHandler(message)
			response = d.response()
			try :
				for r in response:
					print(response)
					client.send(r)
				print("Response sent successfully.")
			except Exception as e:
				print("Exeption : ", e)
				# client.close()
				print("Internal Server Error")
				# Yet to be implemented
				print("Connection closed by foreign host.")
				# client.send("Connection closed by foreign host.".encode())
				client.close()
				return

			if d.getconnection().lower() == "close":
				print("Connection closed by foreign host.")
				client.send("Connection closed by foreign host.".encode())
				client.close()
				
				return

			# d = Decipher(message)
			
			# response_headers = f"{d.getstatus()}\r\n{d.acceptranges()}\r\n{d.getconnection()}\r\nDate: {d.gettime()}\r\nServer: {SERVER_NAME}\r\nContent-Length: {d.getcontentlength()}\r\nContent-Type: {d.getcontenttype()}\r\n\r\n"
			
			# response_body = d.getcontent()
			
			# # encode because response is string
			# client.send(response_headers.encode())
			
			# # don't encode because message body is bytes (always read as binary)
			# client.send(response_body)
			
		except socket.timeout:
			print(f"{address[0]}:{address[1]} disconnected")
			return		

def main(port):
	ip = '127.0.0.1'
	port = int(port)
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind((ip, port))
	s.listen(101)
	i = 0
	while True:
		try:
			client, address = s.accept()
			print(f"{address[0]} connected on {address[1]}")
			t = threading.Thread(target=Listen, args=(client, address), name=f"thread_{i}")
			i += 1
			t.start()
		except KeyboardInterrupt:
			break
		# t.join()


if __name__ == "__main__":
	main(sys.argv[1])
	
	
# current = time.strftime("%a, %d %b %Y %X ", time.gmtime())
					# current = time.gmtime()
					# response += f"{current}GMT\n"
					# response += "Server: Atharva Server\n"
					# text = f.read()
					# response += f"Content-Length: {len(text)}\n"
					# response += "Connection: close\n"
					# response += "Content-Type: text/html; charset=iso-8859-1\n"
					# response += f"\n{text}"
