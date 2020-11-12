import socket
import sys
import os
import threading
from request_handler import RequestHandler, use_logger
# import datetime
# import time
# import gzip
# import logging
# import mimetypes
# import urllib
# from requests_toolbelt.multipart import decoder
# import hashlib
# import random
# import string



def recvall(client):
	BUFF_SIZE = 4096
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

			message = recvall(client)
			print("Raw request: ", message)
			message = message.decode()
			print("This works")
			
			d = RequestHandler(client=client, message=message)
			response = d.response()
			try :
				# client.send(response[0] + response[1])
				print(f"Response Received: {response}")
				for r in response:
					print(response)
					client.send(r)
				print("Response sent successfully.")
				print(d.getconnection())
				if d.getconnection() == "close":
					client.send("Connection closed by foreign host.".encode())
					client.close()
					return
			except Exception as e:
				print("Exception 9")
				print("Exeption : ", e)
				client.close()
				print("Internal Server Error")
				logger = use_logger(error=1)
				logger.error(f'[{e}] -- closing connection')
				# Yet to be Implemented
				print("Connection closed by foreign host.")
				# client.send("Connection closed by foreign host.".encode())
				# client.close()
				return

			if d.getconnection().lower() == "close":
				print("Connection closed by foreign host.")
				client.send("Connection closed by foreign host.".encode())
				client.close()
				
				return
			
		except socket.timeout:
			print("Exception 10")
			logger.error(f'[{e}] -- closing connection')
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
		except KeyboardInterrupt as e:
			print("Exception 11")
			logger = use_logger(error=1)
			logger.error(f'[{e}] -- shutting down')
			break
		# t.join()


if __name__ == "__main__":
	main(sys.argv[1])