import socket
import sys


host = '127.0.0.1'

def main(port):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host, int(port)))
	while True:
		message = input('')
		s.send(message.encode())
		print(s.recv(1024).decode())
	
	
if __name__ == "__main__":
	main(sys.argv[1])
