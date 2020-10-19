import socket
import sys


host = '127.0.0.1'
CRLF = '\r\n'

def main(port):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host, int(port)))
	while True:
		try:
			message = ''
			while True:
				i = input('')
				if i == "-1":
					message += CRLF
					break
				message += i + CRLF
			s.send(message.encode())
			print(s.recv(1024).decode())
		except KeyboardInterrupt:
			s.close()
			break
	
	
if __name__ == "__main__":
	main(sys.argv[1])
