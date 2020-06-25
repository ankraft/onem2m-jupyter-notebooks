from init import *
from http.server import HTTPServer, BaseHTTPRequestHandler

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
        
    def do_POST(self):
        # Construct return header
        self.send_response(200)
        self.send_header('X-M2M-RSC', '2000')
        self.end_headers()

        # Get headers and content data
        length = int(self.headers['Content-Length'])
        contentType = self.headers['Content-Type']
        post_data = self.rfile.read(length)
        
        # Print the content data
        printmd('### Notification')
        #print (self.headers)
        printJSON(post_data.decode('utf-8'))


httpd = HTTPServer(('', notificationPort), SimpleHTTPRequestHandler)
printmd('**starting server & waiting for connections**')
httpd.serve_forever()