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
