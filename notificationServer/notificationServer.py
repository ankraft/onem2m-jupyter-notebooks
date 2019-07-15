import json, sys, time
sys.path.append('..')
from config import *
from http.server import HTTPServer, BaseHTTPRequestHandler
from tinydb import TinyDB, Query, where
from tinydb.storages import MemoryStorage
import urllib.parse

db = None


def getALLSubElementsJSON(jsn, name):
    result = []
    for elemName in jsn:
        elem = jsn[elemName]
        if elemName == name:
            result.append(elem)
        elif isinstance(elem, dict):
            result.extend(getALLSubElementsJSON(elem, name))
        elif isinstance(elem, list):
            for e in elem:
                if isinstance(e, dict):
                    result.extend(getALLSubElementsJSON(e, name))
    return result


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        global db

        # Construct return header
        self.send_response(200)
        self.send_header('X-M2M-RSC', '2000')
        self.end_headers()

        # Get headers and content data
        length = int(self.headers['Content-Length'])
        contentType = self.headers['Content-Type']
        post_data = self.rfile.read(length)
        uid = self.path[1:]
        headers = self.headers
        data = post_data.decode('utf-8')

        jsn =  json.loads(data)
        vrq = getALLSubElementsJSON(jsn, 'm2m:vrq')
        if len(vrq) > 0 and vrq[0]:
            db.remove(where('uid') == uid)
            #print(db.search(where('uid') == uid))
        
        # Store the content data
        print('### Notification (' + uid + ')')
        # print(data)
        db.insert( { 'uid' : uid, 'data': data , 'ts' : str(time.time())})


    def do_GET(self):
        global db

        # Construct response header
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()

        # Parse query
        # The expected format is: /uid?ts=<timestamp>
        pa = urllib.parse.urlparse(self.path[1:])
        uid = pa.path
        q = urllib.parse.parse_qs(pa.query)
        lastts = '0'
        if q and len(q) > 0:
            lastts = q['ts'][0]

 
        # Only get the entries for a specific uid and when the timestamp is greater than the requested
        result = db.search((where('uid') == uid) & (where('ts') > lastts))
        if len(result) > 0:
            print('### Answered Query (' + uid + ')')
            for r in result:
                #print(r['data'])
                self.wfile.write((r['data'] + '\n').encode('utf-8') )


    # Catch and ignore all log messages
    def log_message(self, format, *args):
        return


db = TinyDB(storage=MemoryStorage)  # Use in-memory storage
#db = TinyDB(logfile)
httpd = HTTPServer((notificationInterface, notificationPort), SimpleHTTPRequestHandler)
print('**starting server & waiting for connections**')
httpd.serve_forever()