import datetime
import mimetypes
import os
import time
import urllib
import pathlib

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

filename = 'form_2.html'
print(time.__dict__)
print(time.__doc__)
print(time.gmtime())
print(os.path.getmtime(filename))

mod_time = os.path.getmtime(filename)
last_modified = time.strftime("%a, %d %b %Y %X GMT", time.gmtime(mod_time))
print('last_modified: ', last_modified)
print('current: ', time.strftime("%a, %d %b %Y %X GMT", time.gmtime()))


modificationTime = datetime.datetime.utcfromtimestamp(mod_time).strftime('%a, %d %b %Y %X GMT')
print(modificationTime.strip().replace(' ', '').lower())






print("Main Here")
p4 = "/home/atharva/Study/Sem_5/CN/HTTP-Server/putted/cjkvfy.txt"
path = pathlib.Path(p4)
path.parent.mkdir(parents=True, exist_ok=True)
# p = Path("deleted/random/something/first.txt")
# p.mkdir(exist_ok=True)
with open("/home/atharva/Study/Sem_5/CN/HTTP-Server/putted/cjkvfy.txt", 'w') as f:
	f.write("Writing Somethioaidufladflng")

xyz = [1, 2, 3, 4]
import random
random.shuffle(xyz)
p = 0
while p < 20 :
	p += 1
	print(random.randint(0, len(xyz)))
print(xyz)
# last_modified = time.strftime("%a, %d %b %Y %X GMT", os.path.getmtime(filename))
