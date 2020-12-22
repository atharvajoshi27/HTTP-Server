SERVER_NAME = "Atharva-Server"

BASE_DIR = "/home/atharva/Study/Sem_5/CN/HTTP-Server"


ALLOWED_METHODS = ["GET", "POST", "HEAD", "PUT", "DELETE",]
NOT_IMPLEMENTED_METHODS = ["CONNECT", "OPTIONS", "TRACE", "PATCH", ]
NON_EDITABLE = [BASE_DIR +'/client.py', BASE_DIR + '/var/www/html/form.html', BASE_DIR + '/var/www/html/Images/cat.jpeg', BASE_DIR + '/var/www/html/index.html', BASE_DIR + '/var/log/Atharva-Server/post.log', BASE_DIR + '/var/log/Atharva-Server/access.log', BASE_DIR + '/var/log/Atharva-Server/error.log', BASE_DIR + '/RFC', BASE_DIR + '/server.py', BASE_DIR + '/tcpserver.py', BASE_DIR + '/test.py']
CONFIDENTIAL = [BASE_DIR + "/var/www/html/confidential.html"]
FORBIDDEN  = [BASE_DIR + "/var/www/html/forbidden.html"]
USER = "Atharva"
PASSWORD = "Joshi"
PERMANENTLY_MOVED = [BASE_DIR + "/var/www/html/temp.html", BASE_DIR + "/var/www/html/permanent.html"]