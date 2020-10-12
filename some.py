import random
message = "ET /cat.jpeg HTTP/1.1\nHost: 127.0.0.1:14000User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:80.0) Gecko/20100101 Firefox/80.0Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8\nAccept-Language: en-US,en;q=0.5\nAccept-Encoding: gzip, deflate\nConnection: keep-alive\nUpgrade-Insecure-Requests: 1\n"
message = message.split('\n')
s = dict()
for i in message:
	j = i.split(": ")
	if len(j) > 1:
		s[j[0]] = j[1]

print(s)


f = open('cat.jpeg', 'rb')
something = f.read()
print((something))



f = open('cat.jpeg', 'rb')
print(len(f.read()))

f.close()

f = open('x.txt', 'w')
for i in range(0, 81920):
	f.write(f"Line : {i}\n")

f.close()	
