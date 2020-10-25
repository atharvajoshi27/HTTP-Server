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
from requests_toolbelt.multipart import decoder


def use_logger(goal):
	filename = "access.log"

	if goal == "POST":
		filename = "post.log"
	
	if goal == "access":
		filename = "access.log"

	LOG_FORMAT = "%(levelname)s %(asctime)s : %(message)s"
	logging.basicConfig(filename=filename, level=logging.DEBUG, format=LOG_FORMAT)
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
</html>"""
# https://www.w3.org/Protocols/rfc2616/rfc2616-sec4.html#sec4.2

SERVER_NAME = "Atharva's Server"

BASE_DIR = "/home/atharva/Study/Sem_5/CN/HTTP-Server"

CRLF = "\r\n"


STATUS = {
	 100 : "Continue",
	 101 : "Switching Protocol",
	 102 : "Processing",
	 103 : "Early Hints",
	 200 : "OK",
	 201 : "Created",
	 202 : "Accepted",
	 203 : "Non-Authoritative Information",
	 204 : "No Content",
	 205 : "Reset Content",
	 206 : "Partial Content",
	 207 : "Multi-Status",
	 208 : "Already Reported",
	 226 : "IM Used",
	 300 : "Multiple Choice",
	 301 : "Moved Permanently",
	 302 : "Found",
	 303 : "See Other",
	 304 : "Not Modified",
	 305 : "Use Proxy",
	 306 : "Unused",
	 307 : "Temporary Redirect",
	 308 : "Permanent Redirect",
	 400 : "Bad Request",
	 404 : "Not Found",
	 405 : "Method Not Allowed",
	 406 : "Not Acceptable",
	 407 : "Proxy Authentication Required",
	 408 : "Request Timeout",
	 409 : "Conflict",
	 410 : "Gone",
	 411 : "Length Required",
	 412 : "Precondition Failed",
	 413 : "Payload Too Large",
	 414 : "URI Too Long",
	 415 : "Unsupported Media Type",
	 416 : "Range Not Satisfiable",
	 417 : "Expectation Failed",
	 418 : "I'm a teapot",
	 421 : "Misdirected Request",
	 422 : "Unprocessable Emtity",
	 423 : "Locked",
	 424 : "Failed Dependency",
	 425 : "Too Early",
	 426 : "Upgrade Required",
	 428 : "Precondition Required",
	 429 : "Too Many Requests",
	 431 : "Request Header Fields Too Large",
	 451 : "Unavailable For Legal Reasons",
	 500 : "Internal Server Error",
	 501 : "Not Implemented",
	 502 : "Bad Gateway",
	 503 : "Service Unavailable",
	 504 : "Gateway Timeout",
	 505 : "HTTP Version Not Supported",
	 506 : "Variant Also Negotiates",
	 507 : "Insufficient Storage",
	 508 : "Loop Detected",
	 510 : "Not Extended",
	 511 : "Network Authentication Required",
}


class T():
	content = None
	headers = dict()
	def __init__(self, content, headers, encoding='utf-8'):
		self.content = content.encode(encoding)
		for key, value in headers.items():
			self.headers[key.encode(encoding)] = value.encode(encoding)

class RequestHandler():
	method = "INVALID"
	# path = "/notimplemented.html"
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
	non_editable = ['/home/atharva/Study/Sem_5/CN/HTTP-Server/client.py', '/home/atharva/Study/Sem_5/CN/HTTP-Server/form.html', '/home/atharva/Study/Sem_5/CN/HTTP-Server/Images', '/home/atharva/Study/Sem_5/CN/HTTP-Server/index.html', '/home/atharva/Study/Sem_5/CN/HTTP-Server/post.log', '/home/atharva/Study/Sem_5/CN/HTTP-Server/RFC', '/home/atharva/Study/Sem_5/CN/HTTP-Server/server.py', '/home/atharva/Study/Sem_5/CN/HTTP-Server/tcpserver.py', '/home/atharva/Study/Sem_5/CN/HTTP-Server/test.py']

	# types = {
	# 	"get" : "GET",
	# 	"head" : "HEAD", 
	# 	"post" : "POST",
	# 	"put" : "PUT",
	# 	"delete" : "DELETE",
	# }
	
	headers = {}
	
	def __init__(self, message, client=None):
		print("MESSAGE: ")
		print(message)
		self.message = message
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
		
		print('RARARARARARARARAR : \n', message)
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
		if os.path.exists(path) or self.method == "PUT":
			print("STEP 6")
			self.content_type = mimetypes.guess_type(path)[0]
			self.path = path
			self.status_code = 200
			self.status_type = "OK"

		else:
			print("STEP 7")
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
			head = head.split(":")
			# print(head, end=" ")
			if len(head) > 1:
				self.headers[head[0].lower().strip()] = head[1].lower().strip()

		try :
			self.connection = self.headers["connection"]

		except KeyError:
			pass
		print("")
		# with open(path, self.filemode) as f:
		# 	self.content = f.read()
		# 	self.content_length = len(self.content)
	def readfile(self, only_length=False, is_error=False):
		# Returns true if successful

		# If there is error then we want to format the default message and send accordingly
		if is_error:
			self.content_type = 'text/html'
			self.content = ERROR_RESPONSE %{'code' : self.status_code, 'explain' : self.status_type}
			self.content_length = len(self.content)		
			return True

		# self.content_length = os.path.getsize(self.path)
		
		# For HEAD request we don't need body
		# if only_length:
		# 	return True

		# Else read everything in binary and store for further use
		try :
			with open(self.path, 'rb') as f:
				self.content_length = os.path.getsize(self.path)
				# For HEAD request we don't need body
				if only_length:
					return True
				self.content = f.read()
		except Exception as e:
			print(e)
			self.status_code = 405
			self.status_type = "Not Implemented"
			return False
		return True

	def response_line(self):
		return f"{self.scheme} {self.status_code} {self.status_type}"

	def setstatuscodeandtype(status_code):
		self.status_code = status_code
		self.status_type = STATUS[status_code]

	def GET_method(self):
		print("GET METHOD CALLED")
		success = self.readfile()
		if not success:
			print("Request was unsuccessful")
			return self.error_handler()
		# response_headers = f"{d.getstatus()}\r\n{d.acceptranges()}\r\n{d.getconnection()}\r\nDate: {d.gettime()}\r\nServer: {SERVER_NAME}\r\nContent-Length: {d.getcontentlength()}\r\nContent-Type: {d.getcontenttype()}\r\n\r\n"
		
		response_headers = f"{self.response_line()}{CRLF}Connection: {self.connection}{CRLF}Accept-Ranges: bytes{CRLF}Date: {self.gmtime}Server: {SERVER_NAME}{CRLF}Content-Length: {self.content_length}{CRLF}Content-Type: {self.content_type}{CRLF}{CRLF}"
		response_body = self.content

		return [response_headers.encode(), response_body]

	def POST_method(self):
		print("POST METHOD CALLED")
		params = ''
		if self.parameters:
			try :
				if self.headers["content-type"] == "application/x-www-form-urlencoded":
					params = urllib.parse.parse_qs(self.parameters)
				else: # multipart-form data
					print("\nMULTIPART FORM DATA :\n")
					from requests_toolbelt.multipart import decoder
					t = T(content=self.parameters, headers=self.headers)
					multipart_data = decoder.MultipartDecoder.from_response(t)
					print(multipart_data)
					# for part in multipart_data.parts:
					#     print(part.text)  # Alternatively, part.text if you want unicode
					#     print(part.headers)

					# multipart_string = self.parameters.encode()
					# content_type = "multipart/form-data"
					# for part in decoder.MultipartDecoder(multipart_string, content_type).parts:
					#   print(part.text)

			except KeyError:
				params = urllib.parse.parse_qs(self.parameters)
		else:
			# Use proper error here
			self.status_code = 400
			self.status_type = "Bad Request"
			return self.error_400()

		if len(self.parameters) > 0 and len(params) == 0: # If user gave random string e.g. "fa3489208098afs"
			self.status_code = 400
			self.status_type = "Bad Request"
			return self.error_handler()

		logger = use_logger("POST")
		logger.info(params)
		self.status_code = 201 
		self.status_type = "Created" # "No Content"
		response_headers = f"{self.response_line()}{CRLF}Connection: {self.connection}{CRLF}Date: {self.gmtime}{CRLF}Server: {SERVER_NAME}{CRLF}Content-Type: text/html{CRLF}Content-Length: 0{CRLF}{CRLF}"
		return [response_headers.encode()]

	def HEAD_method(self):
		print("HEAD METHOD CALLED")
		success = self.readfile(only_length=True)
		if not success:
			return self.error_handler()
		response_headers = f"{self.response_line()}{CRLF}Connection: {self.connection}{CRLF}Accept-Ranges: bytes{CRLF}Date: {self.gmtime}Server: {SERVER_NAME}{CRLF}Content-Length: {self.content_length}{CRLF}Content-Type: {self.content_type}{CRLF}{CRLF}"
		return [response_headers.encode()]

	def DELETE_method(self):
		print("DELETE METHOD CALLED")
		b = os.path.exists(self.path)
		if b:
			# Not all files can be deleted
			if self.path in self.non_editable:
				self.status_code = 405
				self.status_type = "Method Not Allowed"
				return self.error_handler()
			

			try :
				os.remove(self.path)
				self.status_type = 200
				self.status_code = "OK"
				self.readfile(is_error=True)
				response_headers = f"{self.response_line()}{CRLF}Connection: {self.connection}{CRLF}Content-Type: {self.content_type}{CRLF}Content-Length: {self.content_length}{CRLF}Date: {self.gmtime}{CRLF}Server: {SERVER_NAME}{CRLF}{CRLF}"
				response_body = self.content
				return [response_headers.encode(), response_body.encode()]

			except IsADirectory:
				print("Directory Cannot be removed")
				self.status_code = 405
				self.status_type = "Method Not Allowed"
				return self.error_handler()

		# If file doesn't exist
		else:
			self.status_code = 405
			self.status_type = "Method Not Allowed"
			return self.error_handler()
		pass

	def PUT_method(self):
		print("PUT METHOD CALLED")

		b = os.path.exists(self.path) # Check if resource already exists
		
		# An origin server that allows PUT on a given target resource MUST send
		#  a 400 (Bad Request) response to a PUT request that contains a
		#  Content-Range header field (Section 4.2 of [RFC7233])
		print(self.headers)
		try :
			self.headers["content-range"]
			self.status_code = 400
			self.status_type = "Bad Request"
			print("Here We Go Again")
			return self.error_handler()

		except KeyError:
			print("Key Error")
			pass

		if self.path in self.non_editable:
			# Since file is used by server this file can't be edited and this method
			# is not implemented for this particular file
			self.status_code = 405
			self.status_type = "Method Not Allowed"
			return self.error_405()
		
		try:
			with open(self.path, 'w') as f:
				f.write(self.parameters)
			
			if b: # Resource already exists
				self.status_code = 200
				self.status_type = "OK"
			
			else: # Resource created
				self.status_code = 201
				self.status_type = "Created"

		except Exception as e:
			print(f"Exception {e} has occured in PUT")
			self.status_code = 500
			self.status_type = "Internal Server Error"
			return self.error_500()

		response_headers = f"{self.response_line()}{CRLF}Connection: {self.connection}{CRLF}Content-Type: {self.content_type}{CRLF}Content-Length: {self.content_length}{CRLF}Date: {self.gmtime}{CRLF}Server: {SERVER_NAME}{CRLF}{CRLF}"
		return [response_headers.encode()]

	def INVALID_method(self):
		print("INVALID METHOD CALLED")
		return self.error_handler()
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

	def error_handler(self):
		print(f"error_handler METHOD CALLED FOR {self.status_code} - {self.status_type}")
		self.readfile(is_error=True)
		response_headers= f"{self.response_line()}{CRLF}Connection: {self.connection}{CRLF}Content-Type: {self.content_type}{CRLF}Content-Length: {self.content_length}{CRLF}Date: {self.gmtime}{CRLF}Server: {SERVER_NAME}{CRLF}{CRLF}"
		response_body = self.content

		return [response_headers.encode(), response_body.encode()]

	def INTERNAL_SERVAR_ERROR(self):
		self.status_code = 500
		self.status_type = "Internal Server Error"
		return self.error_handler()

	def RAISE_ERROR(self, status_code=500, status_type="Internal Server Error"):
		self.status_code = status_code
		self.status_type = status_type
		return self.error_handler()

	def error_500(self):
		print("error_500 METHOD CALLED")
		self.readfile(is_error=True)
		response_headers= f"{self.response_line()}{CRLF}Connection: {self.connection}{CRLF}Content-Type: {self.content_type}{CRLF}Content-Length: {self.content_length}{CRLF}Date: {self.gmtime}{CRLF}Server: {SERVER_NAME}{CRLF}{CRLF}"
		response_body = self.content

		return [response_headers.encode(), response_body]

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
		if self.status_code != 200:
			request_method = self.INVALID_method

		else:
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
		return self.connection
	
	def getencoding(self):
		pass
	
	def getetag(self):
		pass
	
	def getvary(self):
		pass



def recvall(client):
	BUFF_SIZE = 10240
	data = b''
	while True:
		part = client.recv(BUFF_SIZE)
		data += part
		if len(part) < BUFF_SIZE:
			break
	return data



def Listen(client, address):
	while True:
		try:
			message = recvall(client).decode()
			print("This works")
			
			d = RequestHandler(client=client, message=message)
			response = d.response()
			try :
				client.send(response[0] + response[1])
				# for r in response:
				# 	print(response)
				# 	client.send(r)
				print("Response sent successfully.")
				print(d.getconnection())
				if d.getconnection() == "close":
					client.send("Connection closed by foreign host.".encode())
					client.close()
					return
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
