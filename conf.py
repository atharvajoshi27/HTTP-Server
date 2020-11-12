ERROR_RESPONSE = """
<!DOCTYPE html>
<html>
	<head>
		<meta http-equiv="Content-Type" content="text/html;charset=utf-8">
		<title>Error response</title>
	</head>
	<body>
		<p><b>%(code)s</b>. %(explain)s.</p>
		<p>ERROR_HAS_OCCURED</p>
	</body>
</html>
"""

# https://www.w3.org/Protocols/rfc2616/rfc2616-sec4.html#sec4.2

SERVER_NAME = "Atharva's Server"

BASE_DIR = "/home/atharva/Study/Sem_5/CN/HTTP-Server"

CRLF = "\r\n"

STATUS = {
	 100 : "Continue",
	 101 : "Switching Protocol",
	 102 : "Processing",
	 103 : "Early Hints",
	 200 : "OK",
	 201 : "Created",
	 202 : "Accepted",
	 203 : "Non-Authoritative Information",
	 204 : "No Content",
	 205 : "Reset Content",
	 206 : "Partial Content",
	 207 : "Multi-Status",
	 208 : "Already Reported",
	 226 : "IM Used",
	 300 : "Multiple Choice",
	 301 : "Moved Permanently",
	 302 : "Found",
	 303 : "See Other",
	 304 : "Not Modified",
	 305 : "Use Proxy",
	 306 : "Unused",
	 307 : "Temporary Redirect",
	 308 : "Permanent Redirect",
	 400 : "Bad Request",
	 401 : "Unauthorized",
	 402 : "Payment Required",
	 403 : "Forbidden",
	 404 : "Not Found",
	 405 : "Method Not Allowed",
	 406 : "Not Acceptable",
	 407 : "Proxy Authentication Required",
	 408 : "Request Timeout",
	 409 : "Conflict",
	 410 : "Gone",
	 411 : "Length Required",
	 412 : "Precondition Failed",
	 413 : "Payload Too Large",
	 414 : "URI Too Long",
	 415 : "Unsupported Media Type",
	 416 : "Range Not Satisfiable",
	 417 : "Expectation Failed",
	 418 : "I'm a teapot",
	 421 : "Misdirected Request",
	 422 : "Unprocessable Emtity",
	 423 : "Locked",
	 424 : "Failed Dependency",
	 425 : "Too Early",
	 426 : "Upgrade Required",
	 428 : "Precondition Required",
	 429 : "Too Many Requests",
	 431 : "Request Header Fields Too Large",
	 451 : "Unavailable For Legal Reasons",
	 500 : "Internal Server Error",
	 501 : "Not Implemented",
	 502 : "Bad Gateway",
	 503 : "Service Unavailable",
	 504 : "Gateway Timeout",
	 505 : "HTTP Version Not Supported",
	 506 : "Variant Also Negotiates",
	 507 : "Insufficient Storage",
	 508 : "Loop Detected",
	 510 : "Not Extended",
	 511 : "Network Authentication Required",
}


ALLOWED_METHODS = ["GET", "POST", "HEAD", "PUT", "DELETE",]
NOT_IMPLEMENTED_METHODS = ["CONNECT", "OPTIONS", "TRACE", "PATCH", ]
NON_EDITABLE = ['/home/atharva/Study/Sem_5/CN/HTTP-Server/client.py', '/home/atharva/Study/Sem_5/CN/HTTP-Server/form.html', '/home/atharva/Study/Sem_5/CN/HTTP-Server/Images', '/home/atharva/Study/Sem_5/CN/HTTP-Server/index.html', '/home/atharva/Study/Sem_5/CN/HTTP-Server/post.log', '/home/atharva/Study/Sem_5/CN/HTTP-Server/RFC', '/home/atharva/Study/Sem_5/CN/HTTP-Server/server.py', '/home/atharva/Study/Sem_5/CN/HTTP-Server/tcpserver.py', '/home/atharva/Study/Sem_5/CN/HTTP-Server/test.py']