import socket
import sys
import os
import threading
import datetime
import time
import gzip

# https://www.w3.org/Protocols/rfc2616/rfc2616-sec4.html#sec4.2

SERVER_NAME = "Atharva's Server"

BASE_DIR = "/home/atharva/Study/Sem_5/CN/HTTP-Server"

class Decipher():
	method = "INVALID"
	connection = "Keep-Alive"
	server = SERVER_NAME
	root = BASE_DIR
	gmttime = time.strftime("%a, %d %b %Y %X GMT", time.gmtime())
	content_length = 0
	content = None
	content_type = "text/html"
	status_type = "OK"
	status_code = 200
	filemode = 'r'
	
	types = {
		"get" : "GET",
		"post" : "POST",
		"put" : "PUT",
		"delete" : "DELETE",
	}
	
	def __init__(self, message=None):
			message = message.split("\n")
			method_info = message[0].split(" ")
			print("METHOD INFO: ", method_info)
			self.setmethod(method_info[0])
			self.fileread(method_info[1])
			
	def setmethod(self, msg):
		msg = msg.lower().split(" ")
		print(msg)
		if len(msg) < 1:
			self.status_type = "Bad Request"
			self.status_code = 400
			print("LENGTH ISSUES")
		else:
			try:
				self.method = self.types[msg[0]]
			except KeyError:
				print("KEY ERROR")
				self.status_type = "Bad Request"
				self.status_code = 400
	
	def fileread(self, path):
		print(f"PATH : {path}")
		if path == "/":
			path = "/index.html"
		print(f"PATH : {path}")
		abs_path = BASE_DIR + path
		print(f"ABS_PATH : {abs_path}")
		if os.path.exists(abs_path) and self.status_code == 200:
			print("PATH EXISTS")
			ext = os.path.splitext(path)[1]
			print(f"EXT = {ext}")
			if ext in ['.jpg', '.jpeg', '.png', '.ico']:
				if ext == '.png':
					self.content_type = "image/png"
					pass
				elif ext == '.ico':
					self.content_type = 'image/x-icon'
					pass
				else:
					self.content_type = "image/jpeg"
					pass
				self.filemode = 'rb'
			
		else:
			print(f"PATH DOES NOT EXIST and {self.status_code}")
			self.status_type = "Not Found"
			self.status_code = 404
		
		if self.status_code == 200:
			# self.f = open(abs_path, self.filemode)
			path = abs_path
		elif self.status_code == 404:
			# self.f = open('notfound.html', self.filemode)
			path = "notfound.html"
		else:
			self.f = open('badrequest.html', self.filemode)
			path = "badrequest.html"
		print(f"FILE MODE : {self.filemode}")
		f = open(path, self.filemode)
		self.f = f
		self.content = f.read()
		self.content_length = len(self.content)
	
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
		if self.filemode == 'r':
			return "Content-Encoding: gzip\r\n"
		return ''
		
	def getfiledescriptor(self):
		return self.f
	
	def getetag(self):
		return "2000-5b159bc1b3eda"
	
	def getvary(self):
		if self.filemode == 'r':
			return "Vary: Accept-Encoding\r\n"
		return ''
		
def gettime():
	return time.strftime("%a, %d %b %Y %X GMT\n", time.gmtime())

def getlength(text):
	return len(text)

def pathexists(path):
	path = os.path.join(path, BASE_DIR)
	if os.path.exists(path):
		return True
	return False

def Listen(client, address):
	while True:
		try:
			message = client.recv(4096).decode()
			print("MESSAGE: \n", message)
			
			'''
			message = message.split()
			if not message:
				raise socket.timeout
			print(message)
			method = message[0].upper()
			if method == "GET":
				if len(message) == 1 or message[1] == "/" or message[1] == "/index.html" :
					page = "index.html"
				else:
					page = message[1]
				if pathexists(page):
					print(f"PATH TO {page} EXISTS")
					f = open(page, 'r')
					text = f.read()
					response = f"HTTP/1.1 200 OK\n{gettime()}Server: {SERVER_NAME}\nContent-Length: {len(text)}\nConnection: keep-alive\nContent-Type: text/html\n\n{text}"
					client.send(response.encode())
				else:
					print(f"PATH TO {page} DOES NOT EXIST")
					response = "HTTP/1.1 404 Page Not Found\n"
					client.send(response.encode())
			else:
				response = "HTTP/1.1 400 Bad Request"
				'''
				
			d = Decipher(message)
			response = f"{d.getstatus()}\r\n{d.acceptranges()}\r\n{d.getconnection()}\r\nDate: {d.gettime()}\r\nServer: {SERVER_NAME}\r\nContent-Length: {d.getcontentlength()}\r\nContent-Type: {d.getcontenttype()}\r\n\r\n"
			responses = [f"{d.getstatus()}\r\n", f"{d.acceptranges()}\r\n", f"{d.getconnection()}\r\n", f"Date: {d.gettime()}\r\n", f"Server: {SERVER_NAME}\r\n", f"Content-Length: {d.getcontentlength()}\r\n", f"Content-Type: {d.getcontenttype()}\r\n", f"\r\n{d.getcontent()}\r\n" ]
			# for response in responses:
			#	client.send(response.encode())
			message_body = d.getcontent()
			"""
			k = int(len(response) / 4096)
			p = 0
			for i in range(0, k-1):
				client.send(response[p:p+4096].encode())
				p += 4096
			"""
			print("Response : ")
			print(response)
			client.send(response.encode())
			
			if d.filemode == 'rb':
				print(message_body)
				client.send(message_body)
			else:
				client.send(message_body.encode())
			
			# client.sendall(response.encode())
			# client.sendfile(f)
			
			# client.sendall("\r\n".encode())
            #close the connection
			# client.close()
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
