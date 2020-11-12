import pathlib
import random
import socket
import string
import sys
import threading
import time
from conf import *

SERVER = '127.0.0.1'
PORT = None

CRLF = '\r\n'

methods = ["GET", "POST", "HEAD", "PUT", "DELETE"]
gettable = ["/index.html", "/favicon.ico", "/Images/cat.jpeg", "/form_2.html", "/form3.html", "/randomstuff.stuff"]
# randomstuff.stuff doesn't exist, used to detect 404

threads_and_requests = dict()
def sendGET():
	l = random.randint(0, len(gettable)-1)
	msg = f"GET {gettable[l]} HTTP/1.1{CRLF}Host : {SERVER}:{PORT}{CRLF}"
	return msg
	pass

def sendHEAD():
	l = random.randint(0, len(gettable)-1)
	msg = f"HEAD {gettable[l]} HTTP/1.1{CRLF}Host : {SERVER}:{PORT}{CRLF}"
	return msg

def sendPOST():
	msg = f"POST /form.html HTTP/1.1{CRLF}Host : {SERVER}:{PORT}{CRLF}Content-Type:application/x-www-form-urlencoded{CRLF}{CRLF}name=hello&n=192&Submit=Submit"
	return msg
	pass

def sendPUT():
	l = random.randint(0, 1000)
	name = ''.join(random.SystemRandom().choice(string.ascii_lowercase + string.digits) for _ in range(6))
	data = ''.join(random.SystemRandom().choice(string.ascii_lowercase + string.digits) for _ in range(l))
	msg = f"PUT /putted/{name}.txt HTTP/1.1{CRLF}Host: {SERVER}:{PORT}{CRLF}Content-Type: text/html{CRLF}Content-Length: {l}{CRLF}{CRLF}{data}"
	return msg

def sendDELETE():
	# Here I am first creating a resource and then I'll delete it
	# So that it will avoid garbage files on server
	l = random.randint(0, 1000)
	name = ''.join(random.SystemRandom().choice(string.ascii_lowercase + string.digits) for _ in range(6))
	data = ''.join(random.SystemRandom().choice(string.ascii_lowercase + string.digits) for _ in range(l))
	p4 = f"deleted/for_test_purpose/{name}.txt"
	path = pathlib.Path(p4)
	path.parent.mkdir(parents=True, exist_ok=True)
	with open("p4", 'w') as f:
		f.write(data)
	time.sleep(0.2)
	msg = f"DELETE /{p4} HTTP/1.1{CRLF}Host: {SERVER}:{PORT}{CRLF}"
	return msg
	pass



def request(client, name):
	# Deciding number of requests to be sent
	# n = 1
	# actual = 0
	# for i in range(n):
	random.shuffle(methods)
	x = methods[random.randint(0, len(methods)-1)]
	try :
		msg = eval(f"send{x}()")
		client.sendall(msg.encode())
		received = client.recv(8192).decode(errors='ignore')
		print(f"{name}\nREQUEST :\n{msg}\nRESPONSE :\n{received}")
		actual += 1
		time.sleep(1)
	except Exception as e:
		# break
		print(f"Exception {e} occurred in {name}")
	client.close()
	# p = name.split("thread_")[1]
	# threads_and_requests[p] = actual


def main():
	for i in range(100):
		client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		client.connect((SERVER, PORT))
		t = threading.Thread(target=request, name=f"thread_{i}", args=[client, f"thread_{i}"])
		t.start()

	pass

if __name__ == "__main__":
	try :
		PORT = int(sys.argv[1])
		main()
		print("length = ", len(threads_and_requests))
		for i, j in threads_and_requests.items():
			print(f"thread_{i} : {j}")
	except Exception as e:
		print(e)
		print("Provide Port Number")