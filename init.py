import requests
import datetime, re, time
from json import loads, dumps
import IPython.display
from IPython.display import JSON
from config import *


# variable to distinguish users
_uid = ''

# Print and format as Markdown
def printmd(s, c=None):
    if c:
        cs = "<span style='color:{}'>{}</span>".format(c, s)
    else:
        cs = s
    IPython.display.display(IPython.display.Markdown(cs))


# Format and print JSON
def printJSON(j):
    print(dumps(loads(j), indent=2))


# Print the request
def printRequest(url, headers, body=None):
    printmd('Sending request to **' + url + '**')
    printmd('**Headers**')
    for h in headers:
        print(h + ':' + headers[h])
    if body is not None:
        printmd('\n**Body**\n')
        if isinstance(body, str):
            print(dumps(loads(body), indent=2))
        elif isinstance(body, dict):
            print(dumps(body, indent=2))


# Tidy-print a response header.
def printResponse(r):
    printmd('---\n### Response')
    print(str(r.status_code) + ' (' + r.reason + ')')
    printmd('\n**Headers**')
    for h in r.headers:
        print(h + ':' + r.headers[h])
    if r.text:
        printmd('\n**Body**\n')
        printJSON(r.text)
    printmd('---')
    

# The following request methods hide a bit of the complexity of constructing the
# requests and make them easier to read.

def RETRIEVE(url, headers):
    printRequest(url, headers)
    printResponse(requests.get(url, headers=headers))

def CREATE(url, headers, body):
    printRequest(url, headers, body)
    printResponse(requests.post(url, headers=headers, data=body if isinstance(body, str) else dumps(body)))

def DELETE(url, headers):
    printRequest(url, headers)
    printResponse(requests.delete(url, headers=headers))
    
def UPDATE(url, headers, body):
    printRequest(url, headers, body)
    printResponse(requests.put(url, headers=headers, data=body if isinstance(body, str) else dumps(body)))

    
# Notification Server Query
# The following function queries the notification server

def queryNotificationServer():
    lastRunTS = time.time()
    printmd('**Waiting for notifications**', c='green')
    while True:
        result = requests.get(nu() + '?ts=' + str(lastRunTS))
        lastRunTS = time.time()
        if result.text:
            printmd('### Received Notification - ' + str(datetime.datetime.now()))
            print(result.text)
        time.sleep(1)


# The following Exception class is used to show a dialog to the user and gracefully stops the execution
# of the current cell.

class StopExecution(Exception):
    def __init__(self, message):
        super().__init__(message, 'Execution Stopped')
        printmd('**' + message + '**', 'red')

    def _render_traceback_(self):# Prevent printing of stacktrace 
        pass


def ae():
    return 'Notebook-AE'

def acp():
    return 'Notebook-ACP'

def nu():
    return notificationURLBase + ':' + str(notificationPort)


printmd('**Configuration Ready**', c='green')
  