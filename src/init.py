import requests
import datetime, re, time, threading, os
from urllib.request import urlopen
from json import loads, dumps
import IPython.display
from IPython.display import JSON, HTML, Markdown

from config import *
from annotations import *

# variable to distinguish users
_uid = ''

# Parameter names
_originator = 'X-M2M-Origin'
_requestIdentifier = 'X-M2M-RI'
_resourceType = 'ResourceType'
_releaseVersionIndicator = "X-M2M-RVI"

def printmd(s, c=None):
    """ Print and format as Markdown.
    """
    if c:
        cs = f"<span style='color:{c}'>{s}</span>"
    else:
        cs = s
    IPython.display.display(Markdown(cs))


def printHtml(s):
    IPython.display.display(HTML(s))


def printmdCode(s):
    lines = s.split('\n')
    result = ''
    for l in lines:
        stripped = l.lstrip()
        li = "<span style='font-family: monospace;'>" +'&nbsp;' * (len(l) - len(stripped)) + stripped + '</span>  \n' 
        result += li.replace('\x03', '\n')  # Replace possible \x03 marker with newlines, e.g. in annotations
    IPython.display.display(Markdown(result))

def printJSON(j):
    """ Format and print JSON.
    """
    #print(dumps(loads(j), indent=2))
    printmdCode( annotateShortnames( highlightDebugMessage( dumps(loads(j), indent=4))))


def printParameters(parameters):
    """ Format the headers as a table.
    """

    table = '''
| HTTP Header | oneM2M Parameter | Value |
|:---|:---|:---|
'''
    for h,v in parameters.items():
        if h in [ 'Server', 'Content-Length' ]:
            continue
        if h == 'X-M2M-RSC':
            v = annotateRSC(v)
        table += f'| {annotateHeaderField(h)} | {toOneM2MParameter(h)} | {v} |\n'
    printmd(table)


def printStatusCode(statusCode, reason):
    printmd(str(statusCode) + ' (' + reason + ')', 'green' if 200 <= statusCode < 300 else 'red')


def printRequest(url, parameters, content=None):
    """ Print the request. 
    """
    printmd(f'---\n### HTTP Request')
    printmd(f'**{url}**')
    printParameters(parameters)
    if content is not None:
        printmd('\n#### Request Content\n')
        (isinstance(content, str)  and printmdCode( annotateShortnames( dumps(loads(content), indent=4))))
        (isinstance(content, dict) and printmdCode( annotateShortnames( dumps(content, indent=4))))


def printResponse(r):
    """ Tidy-print a response header. 
    """
    printmd('---\n### HTTP Response')
    printStatusCode(r.status_code, r.reason)
    printParameters(r.headers)
    if r.text:
        printmd('\n**Result Content**\n')
        printJSON(r.text)


def printHtmlError(s):
    printHtml(f'<div class="alert alert-block alert-danger">{s}</div>')


def printConnectionError():
    printHtmlError('<b>CSE not runnning</b><br/>Please start the CSE from the <a href="../start-cse.ipynb" target="_blank" rel="noreferrer noopener">start-cse</a> notebook and try again. ')


# The following request methods hide a bit of the complexity of constructing the
# requests and make them easier to read.

def printStructure() -> None:
    printmd('---\n### Current Resource Tree')
    if (resp := requests.get(f'{host}/__structure__/text')).status_code == 200:
        printmdCode(annotateRT(resp.text))

def _sendRequest(method, **headers) -> str:
    """ Check and update the given parameters, and send a request with the given method.
    """

    # check and extract some parameters. Most parameters need individual handling.
    if (target := headers.pop('target', None)) is None:
        return '<b>target</b> parameter is missing'

    if (content := headers.pop('content', None)) is None and method in [ requests.post, requests.put ]:
        return '<b>content</b> parameter is missing'
    if content is not None: # could be None when method is get() or delete()
        content = content if isinstance(content, str) else dumps(content)   # Transform content to JSON 

    if (resourceType := headers.pop('resourceType', None)) is None and method in [ requests.post ]:
        return '<b>resourceType</b> parameter is missing'

    if (originator := headers.pop('originator', None)) is None:
        return '<b>originator</b> parameter is missing'
    headers[_originator] = originator

    if (ri := headers.pop('requestIdentifier', None)) is None:
        return '<b>requestIdentifier</b> parameter is missing'
    headers[_requestIdentifier] = ri

    if (rvi := headers.pop('releaseVersionIndicator', None)) is None:
        return '<b>releaseVersionIndicator</b> parameter is missing'
    headers[_releaseVersionIndicator] = rvi
    
    headers['Content-Type'] = f'application/json{f";ty={resourceType}" if resourceType is not None else ""}'
    headers['Accept'] = 'application/json'  # Always send an 'Accept' header even when not needed

    try:
        url = host + target
        if content is not None:
            response = method(url, headers=headers, data=content)
        else:
            response = method(url, headers=headers)
        printRequest(url, headers, content)
        printResponse(response)
        printStructure()
        printmd('---')
    except:
        printConnectionError()


def CREATE(**kwargs) -> None:
    """ Send a CREATE request.
    """
    if (err := _sendRequest(requests.post, **kwargs)) is not None:
        printHtmlError(err)


def RETRIEVE(**kwargs) -> None:
    """ Send a RETRIEVE request.
    """
    if (err := _sendRequest(requests.get, **kwargs)) is not None:
        printHtmlError(err)


def UPDATE(**kwargs) -> None:
    """ Send an UPDATE request.
    """
    if (err := _sendRequest(requests.put, **kwargs)) is not None:
        printHtmlError(err)


def DELETE(**kwargs) -> None:
    """ Send a DELETE request.
    """
    if (err := _sendRequest(requests.delete, **kwargs)) is not None:
        printHtmlError(err)


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


def nu():
    return notificationURLBase + ':' + str(notificationPort)


# Print debug messages in red
def highlightDebugMessage(text):
    if (start := text.find('\"m2m:dbg\"', 0)) > -1:
        end = text.find('\n', start)
        text = text[:start] + '<span style=\'color:red\'>' + text[start:end] + '</span>' + text[end:]
    return text


def checkCSEConnection(id:str):
    try:
        r = requests.get(f'{host}/{id}')
    except:
        return False
    return True

# At the end of the init check whether the CSE is up and running
if not checkCSEConnection(cseRN):
    printConnectionError()
else:
    printmd('**Configuration Ready**', c='green')

    

# def ae():
#     return 'Notebook-AE'
#
# def acp():
#     return 'Notebook-ACP'