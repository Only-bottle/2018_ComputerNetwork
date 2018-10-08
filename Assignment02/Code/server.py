import cgi
from http.server import HTTPServer
from http.server import CGIHTTPRequestHandler
import cgitb; cgitb.enable()

server_addr = ("", 8000)
handler = CGIHTTPRequestHandler
handler.cgi_directories = ["/"]
server = HTTPServer(server_addr, handler)
server.serve_forever()
