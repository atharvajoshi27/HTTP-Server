import socket
import sys


host = '127.0.0.1'

def main(port):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host, int(port)))
	while True:
		try:
			message = input('')
			s.send(message.encode())
			print(s.recv(1024).decode())
		except KeyboardInterrupt:
			s.close()
			break
	
	
if __name__ == "__main__":
	main(sys.argv[1])
