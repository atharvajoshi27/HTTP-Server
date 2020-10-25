import mimetypes
import os
import urllib

x = "/home/atharva/Study/Sem_5/CN/HTTP-Server/Images/cat.jpeg"


DEFAULT_ERROR_MESSAGE = """
Hello  %(name)s. %(message)s.
Thanks.
"""
print(type(DEFAULT_ERROR_MESSAGE))
print(DEFAULT_ERROR_MESSAGE %{'name':"Atharva", 'message':"Hi"})

qs = "name=John+Doe&n=42&Submit=Submit"
d = urllib.parse.parse_qs(qs)
print(d)

x = {'name': ['John Doe'], 'n': ['42'], 'Submit': ['Submit']}
print(str(x))


y = input()
if y == '':
	print("Can be used 1")
if y == '\r\n':
	print("Can be used 2")
	
else:
	print("Can't use 2")


BASE_DIR = "/home/atharva/Study/Sem_5/CN/HTTP-Server/"

s = ["client.py",  "form.html",  "Images",  "index.html",  "post.log",  "RFC",  "server.py",  "tcpserver.py",  "test.py"]
l = []
for i in s:
	l.append(BASE_DIR + i)

try :
	with open('RFC', 'r') as f:
		print(f.read())
except IsADirectoryError:
	print("Done")

d = {}
d[1] = 2
for key, value in d.items():
	print(key, " :", value)
	key = str(key).encode()
	value = str(value).encode()

print(d)