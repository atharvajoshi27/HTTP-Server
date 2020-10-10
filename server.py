import socket
import sys
import os
import threading
import datetime
import time

def Listen(client, address):
	print("Came here")
	message = client.recv(1024).decode()
	message = message.split()
	# for i in message:
	#	i = i.upper()
	
	print(message)
	if message[0].upper() == "GET":
		print("YES GET")
		if len(message) == 1 or message[1] == "/" or message[1] == "/index.html" :
			page = "index.html"
		else:
			page = message[1]
		if os.path.exists(page):
			g = open("some2.txt", 'w')
			print(f"Path {page} does exist")
			f = open("index.html", 'r')
			response = "HTTP/1.1 200 OK\n"
			current = time.strftime("%a, %d %b %Y %X ", time.gmtime())
			# current = time.gmtime()
			response += f"{current}GMT\n"
			response += "Server: Atharva Server\n"
			text = f.read()
			response += f"Content-Length: {len(text)}\n"
			response += "Connection: close\n"
			response += "Content-Type: text/html; charset=iso-8859-1\n"
			response += f"\n{text}"
			g.write(response)
			client.send(response.encode())
		else:
			g = open("some2.txt", 'w')
			g.write("Wrong")
			print(f"Path {page} doesn't exist")
		g.close()
	else:
		print("NOT GET")		
def main(port):
	ip = '127.0.0.1'
	port = int(port)
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind((ip, port))
	s.listen(101)
	print("0")
	while True:
		print("1")
		client, address = s.accept()
		print(f"{address[0]} connected on {address[1]}")
		t = threading.Thread(target=Listen, args=(client, address))
		t.start()
		t.join()
		print("2")


if __name__ == "__main__":
	main(sys.argv[1])
