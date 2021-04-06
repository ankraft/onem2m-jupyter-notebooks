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


def printmdCode(s):
    lines = s.split('\n')
    result = ''
    # for l in lines:
    #     stripped = l.lstrip()
    #     result += '&nbsp;' * (len(l) - len(stripped)) + stripped + '  \n'
    for l in lines:
        l = l.rstrip()          # Remove all ws from the end
        stripped = l.lstrip()   # Return a version where all ws is removed from the beginning
        li = "<span style='font-family: monospace;'>" +'&nbsp;' * (len(l) - len(stripped)) + stripped + '</span>  \n' 
        li = li.replace('   ', '&nbsp;&nbsp;&nbsp;') # replace all 3*space in the middle
        result += li.replace('\x03', '\n')  # Replace possible \x03 marker with newlines, e.g. in annotations

    IPython.display.display(IPython.display.Markdown(result))

# Format and print JSON
def printJSON(j):
    #print(dumps(loads(j), indent=2))
    printmdCode( annotateShortnames( highlightDebugMessage( dumps(loads(j), indent=4))))



# Format the headers as a table
def printHeaders(headers):
    printmd('\n**Headers**')
    table = '''| Header Field | Value |
        |:---|:---|
        '''
    for h,v in headers.items():
        if h == 'X-M2M-RSC':
            v = annotateRSC(v)
        table += '| %s | %s |\n' % (h, v)
    printmd(table)


def printStatusCode(statusCode, reason):
    printmd(str(statusCode) + ' (' + reason + ')', 'green' if 200 <= statusCode < 300 else 'red')


# Print the request
def printRequest(url, headers, body=None):
    printmd('Sending request to **' + url + '**')
    printHeaders(headers)
    if body is not None:
        printmd('\n**Body**\n')
        (isinstance(body, str)  and printmdCode( annotateShortnames( dumps(loads(body), indent=4))))
        (isinstance(body, dict) and printmdCode( annotateShortnames( dumps(body, indent=4))))


# Tidy-print a response header.
def printResponse(r):
    printmd('---\n### Response')
    printStatusCode(r.status_code, r.reason)
    printHeaders(r.headers)
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
        result = requests.get(notificationURL + '?ts=' + str(lastRunTS))
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



shortLongNames = {
    'acpi'  : 'access control policy identifier',
    'acop'  : 'access control operations',
    'acor'  : 'access control originators',
    'acr'   : 'access control rule',
    'aei'   : 'AE identifier',
    'api'   : 'application identifier',
    'cbs'   : 'current byte size',
    'cnf'   : 'content info',
    'cni'   : 'current number of instances',
    'con'   : 'content',
    'cnd'   : 'container definition',
    'cnm'   : 'current number of members',
    'cr'    : 'creator',
    'cs'    : 'content size',
    'csi'   : 'CSE identifier',
    'cst'   : 'CSE type',
    'csy'   : 'consistency strategy',
    'csz'   : 'content serializations',
    'ct'    : 'creation time',
    'enc'   : 'eventNotification criteria',
    'et'    : 'expiration time',
    'exc'   : 'expiration counter',
    'lbl'   : 'label',
    'lt'    : 'last modified time',
    'mbs'   : 'max byte size',
    'mid'   : 'member identifiers',
    'mni'   : 'max number of instances',
    'mnm'   : 'max number of members',
    'mt'    : 'member type',
    'mtv'   : 'member type validated',
    'nct'   : 'notification content type',
    'net'   : 'notification event type',
    'nev'   : 'notification event',
    'nm'    : 'name',
    'nu'    : 'notification URI''s',
    'pi'    : 'parent identifier',
    'poa'   : 'point of access',
    'pv'    : 'privileges',
    'pvs'   : 'self-privileges',
    'rep'   : 'representation',
    'ri'    : 'resource identifier',
    'rn'    : 'resource name',
    'rqi'   : 'request identifier',
    'rr'    : 'request reachability',
    'rrl'   : 'resources result list',
    'rsc'   : 'response status code',
    'rvi'   : 'release version indicator',
    'srt'   : 'supored resource types',
    'srv'   : 'supported release versions',
    'ssi'   : 'semantic support indicator',
    'st'    : 'state tag',
    'sur'   : 'subscription reference',
    'ty'    : 'resource type',
    'typ'   : 'resource type',
    'val'   : 'value',
    'vrq'   : 'verification request',

    'm2m:ae'    : 'application entity',
    'm2m:acp'   : 'acess control policy',
    'm2m:agr'   : 'agregated response',
    'm2m:cb'    : 'CSE base',
    'm2m:cin'   : 'content instance',
    'm2m:cnt'   : 'container',
    'm2m:dbg'   : 'debug information',
    'm2m:grp'   : 'group',
    'm2m:rrl'   : 'resources result list',
    'm2m:rsp'   : 'response',
    'm2m:sgn'   : 'notification',
    'm2m:sub'   : 'subscription',
}


# Add hover tooltips for shortnames
def annotateShortnames(text):
    for sh, ln in shortLongNames.items():
        text = text.replace('"%s"' % sh, '"[%s](#_blank "%s")"' % (sh, ln))
    return text


rscCodes = {
    '2000' :    'OK',
    '2001' :    'Created',
    '2002' :    'Deleted',
    '2004' :    'Updated',
    '4000' :    'Bad Request',
    '4004' :    'Not Found',
    '4005' :    'Operation Not Allowed',
    '4102' :    'Contents Unacceptable',
    '4103' :    'Originator Has No Privilege',
    '4105' :    'Conflict',
    '4107' :    'Security Association Required',
    '4108' :    'Invalid Child Resource Type',
    '4110' :    'Group Member Type Inconsistent',
    '5000' :    'Internal Server Error',
    '5001' :    'Not Implemented',
    '5103' :    'Target Not Reachable',
    '5105' :    'Receiver Has No Privileges',
    '5106' :    'Already Exists',
    '5203' :    'Target Not Subscribable',
    '5204' :    'Subscription Verification Initiation Failed',
    '5207' :    'Not Acceptable',
    '6010' :    'Max Number Of Member Exceeded',
    '6023' :    'Invalid Arguments',
    '6023' :    'Insufficient Arguments',
}

def annotateRSC(rsc):
    if (v := rscCodes.get(rsc)) is not None:
        rsc = rsc.replace('%s' % rsc, '[%s](#_blank "%s")' % (rsc, v))
    return rsc

# Print debug messages in red
def highlightDebugMessage(text):
    if (start := text.find('\"m2m:dbg\"', 0)) > -1:
        end = text.find('\n', start)
        text = text[:start] + '<span style=\'color:red\'>' + text[start:end] + '</span>' + text[end:]
    return text



printmd('**Configuration Ready**', c='green')
  