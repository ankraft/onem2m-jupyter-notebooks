#
#	init.py
#
#	(c) 2021 by Andreas Kraft
#	License: BSD 3-Clause License. See the LICENSE file for further details.
#


import datetime, random, re, sys, time, threading, os
import http.client
from enum import IntEnum
from json import loads, dumps
import IPython.display
from IPython.display import HTML, Markdown, clear_output
import requests

from src.config import *
from annotations import *
from simulator import *

# Parameter names
_originator = 'X-M2M-Origin'
_requestIdentifier = 'X-M2M-RI'
_resourceType = 'ResourceType'
_releaseVersionIndicator = "X-M2M-RVI"

# user-friendly names
cseBaseName = cseRN


# Resource Type names
class Type(IntEnum):
    ACP             =    1
    AE              =    2
    Container       =    3
    ContentInstance =    4
    Group			=    9
    MgmtObj         =   13
    Node            =   14
    Subscription    =   23
    FlexContainer   =   28

    # ManagementDefinitions
    DeviceInfo 		= 1007


# Result Content Types
class RCN(IntEnum):
    nothing									= 0
    attributes 								= 1
    hierarchicalAddress						= 2
    hierarchicalAddressAttributes			= 3
    attributesAndChildResources				= 4	
    attributesAndChildResourceReferences	= 5
    childResourceReferences					= 6
    originalResource 						= 7
    childResources							= 8
    modifiedAttributes						= 9
    discoveryResultReferences				= 11


# AccessControlOperations
class ACO(IntEnum):
    """ Permissions """
    NONE				=  0
    CREATE				=  1
    RETRIEVE			=  2
    UPDATE				=  4
    DELETE 				=  8
    NOTIFY 				= 16
    DISCOVERY			= 32
    ALL					= 63


# FilterUsage
class FilterUsage(IntEnum):
    """ FilterUsage"""
    discoveryCriteria		= 1
    conditionalRetrieval	= 2 # default
    ipeOnDemandDiscovery	= 3

# for JSON null keyword
null = None	

__response = None
""" Contains the last response or None """
__responseStatusCode = 0
""" Contains the last response status code """


__verbose = True
__withResults = False

def printmd(s, c=None, hd=''):
    """ Print and format as Markdown.
    """
    if c:
        cs = f"{hd}<span style='color:{c}'>{s}</span>"
    else:
        cs = f'{hd}{s}'
    IPython.display.display(Markdown(cs))


def printHtml(s):
    IPython.display.display(HTML(s))


def printmdCode(s):
    lines = s.split('\n')
    result = ''
    for l in lines:
        l = l.rstrip()          # Remove all ws from the end
        stripped = l.lstrip()   # Return a version where all ws is removed from the beginning
        li = "<span style='font-family: monospace;'>" +'&nbsp;' * (len(l) - len(stripped)) + stripped + '</span>  \n' 
        li = li.replace('   ', '&nbsp;&nbsp;&nbsp;') # replace all 3*space in the middle
        result += li.replace('\x03', '\n')  # Replace possible \x03 marker with newlines, e.g. in annotations
    IPython.display.display(Markdown(result))


def printJSON(j):
    """ Format and print JSON.
    """
    #print(dumps(loads(j), indent=2))
    printmdCode( annotateShortnames( highlightDebugMessage( dumps(loads(j), indent=4))) )


def clearCell():
    """ Clear the current output cell.
    """
    clear_output(wait=True)


excludedHeaders = [ 'Access-Control-Allow-Origin', 'Authorization', 'Connection', 'Content-Length', 'ETag',
                    'request-context', 'Server', 'Strict-Transport-Security', 'Transfer-Encoding'
                  ]
""" http headers excluded from printing on the notebook. """

def printParameters(parameters):
    """ Format the headers as a table.
    """

    table = '''
| HTTP Header | oneM2M Parameter | Value |
|:---|:---|:---|
'''
    for h,v in parameters.items():
        if h in excludedHeaders:
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
    printmd(f'### HTTP Request')
    printmd(f'**{url}**	')
    printParameters(parameters)
    if content is not None:
        printmd('\n#### Request Content | Body\n')
        (isinstance(content, str)  and printmdCode( annotateShortnames( dumps(loads(content), indent=4))))
        (isinstance(content, dict) and printmdCode( annotateShortnames( dumps(content, indent=4))))


def printResponse(r):
    """ Tidy-print a response header. 
    """
    printmd('---\n### HTTP Response')
    printStatusCode(r.status_code, r.reason)
    printParameters(r.headers)
    if r.text:
        printmd('\n**Response Content | Body**\n')
        printJSON(r.text)


def printShortResponse(r):
    """ Print terse response code. 
    """
    if not 200 <= r.status_code < 300:
        printStatusCode(r.status_code, r.reason)
        printJSON(r.text)

    elif __withResults: # only when results should be printed
        printStatusCode(r.status_code, r.reason)


def printHtmlError(s):
    printHtml(
f"""
<div class="alert alert-block alert-danger" style="background-color: white; border: 2px solid; padding: 10px; width:80%;">
    <b><i class="fa fa-exclamation-triangle" aria-hidden="true"></i>&nbsp; Error</b><br>
    {s}
</div>
""")


def printConnectionError(msg:str):
    printHtmlError(
f"""
<b>Cannot access the CSE, or the CSE is not runnning.</b></br>
Please <a href="start-cse.ipynb" target="_new">start the CSE</a> or check the configuration file <a href="/edit/src/config.py" target=_new>config.py</a>. 
Did you specify the correct address, credentials, and proxy server?</br>
Please restart this notebook kernel after you have updated the configuration file.<br>
<br>
<b>Error message</b><br>{msg}
""")


# The following request methods hide a bit of the complexity of constructing the
# requests and make them easier to read.

def showResourceTree(section:bool = True, title:str = 'CSE Resource Tree') -> None:
    if (resp := requests.get(f'{host}/__structure__/text')).status_code == 200:
        if section:
            printmd('---')
        printmd(f'### {title}')
        printmdCode(annotateRT(resp.text))


#############################################################################
#
#   Request Handling
#

def _sendRequest(method, **parameters) -> str:
    global __response, __responseStatusCode, __verbose
    __response = None
    headers = {}

    """ Check and update the given parameters, and send a request with the given method.
    """

    # check and extract some parameters. Most parameters need individual handling.
    if (target := parameters.pop('target', None)) is None:
        return '<b>target</b> parameter is missing'

    if (content := parameters.pop('content', None)) is None and method in [ requests.post, requests.put ]:
        return '<b>content</b> parameter is missing'
    if content is not None: # could be None when method is get() or delete()
        content = content if isinstance(content, str) else dumps(content)   # Transform content to JSON 

    if (resourceType := parameters.pop('resourceType', None)) is None and method in [ requests.post ]:
        return '<b>resourceType</b> parameter is missing'
    if resourceType is not None and not isinstance(resourceType, int):
        return '<b>resourceType</b> parameter must be an integer number'

    if (originator := parameters.pop('originator', None)) is None:
        return '<b>originator</b> parameter is missing'
    if not isinstance(originator, str):
        return '<b>originator</b> parameter must be a string'
    headers[_originator] = originator

    if len(ri := parameters.pop('requestIdentifier', f'ri-{random.randint(1,sys.maxsize)}')) == 0:
        return '<b>requestIdentifier</b> parameter must not be empty'
    if not isinstance(ri, str):
        return '<b>requestIdentifier</b> parameter must be a string'
    headers[_requestIdentifier] = ri

    if len(rvi := parameters.pop('releaseVersionIndicator', '3')) == 0:
        return '<b>releaseVersionIndicator</b> parameter must not be empty'
    if not isinstance(rvi, str):
        return '<b>releaseVersionIndicator</b> parameter must be a string'
    headers[_releaseVersionIndicator] = rvi
    
    headers['Content-Type'] = f'application/json{f";ty={resourceType}" if resourceType is not None else ""}'
    headers['Accept'] = 'application/json'  # Always send an 'Accept' header even when not needed

    args = ''
    if (fu := parameters.pop('filterUsage', None)) is not None:
        if not isinstance(fu, int):
            return '<b>filterUsage</b> parameter must be an integer number'
        args += f'{"&" if len(args)>0 else ""}fu={fu}'
    if (filters := parameters.pop('filters', None)) is not None:
        if not isinstance(filters, list):
            return '<b>filters</b> parameter must be a list of strings'
        for each in filters:
            args += f'{"&" if len(args)>0 else ""}{each}'
    if (rcn := parameters.pop('resultContent', None)) is not None:
        if not isinstance(rcn, int):
            return '<b>resultContent</b> parameter must be an integer number'
        args += f'{"&" if len(args)>0 else ""}rcn={rcn}'
    if (lvl := parameters.pop('level', None)) is not None:
        if not isinstance(lvl, int):
            return '<b>level</b> parameter must be an integer number'
        args += f'{"&" if len(args)>0 else ""}lvl={lvl}'
    if (ty := parameters.pop('childType', None)) is not None:
        if not isinstance(ty, int):
            return '<b>childType</b> parameter must be an integer number'
        args += f'{"&" if len(args)>0 else ""}ty={ty}'

    # Check verbosity
    _verbose = __verbose
    if (silent := parameters.pop('_silent', None)) is not None:
        if not isinstance(silent, bool):
            return '<b>_silent</b> parameter must be a boolean'
        _verbose = not silent
    
    # Check repeats
    repeat = parameters.pop('_repeat', 1)
    if not isinstance(repeat, int):
        return '<b>_repeat</b> parameter must be an integer number'

    # Just add all remaining arguments
    #args += '&'.join('{!s}={!r}'.format(key,val) for (key,val) in parameters.items())
    if len(parameters) > 0:
        args += '&' + '&'.join(f'{key}={val}' for (key,val) in parameters.items())
    
    # Send request 'repeat' times
    for i in range(repeat):

        try:
            args = f'?{args}' if len(args) > 0 else ''
            url = f'{host}{target}{args}'
            if content is not None:
                resp = method(url, headers=headers, data=content)
            else:
                resp = method(url, headers=headers)
            __response = resp.json() if len(resp.content) else None
            __responseStatusCode = int(resp.headers['X-M2M-RSC']) if resp.headers['X-M2M-RSC'] else -1
            if _verbose:
                printRequest(url, headers, content)
                printResponse(resp)
                showResourceTree()
                printmd('---')
            elif silent is None:
                printShortResponse(resp)

        except Exception as e:
            printConnectionError(e.msg)



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


def repeat(request=None, times=1, background=False, interval=0.0, verbose=None) -> None:

    def _runner(times=1, request=None, interval=0.0, verbose_=True):
        global verbose
        if request is not None:
            for i in range(1, times+1):
                if verbose_:
                    printmd(f'Request {i}', c='grey', hd='## ')
                elif __responseStatusCode:
                    clearCell()
                oldVerbose = verbose(verbose_)
                request()
                verbose(oldVerbose)
                time.sleep(interval)

            if 2000 <= __responseStatusCode <= 3000:
                printmd('**Finished successful**', c='green')
            else:
                printmd('**Finished with errors**', c='red')

    if verbose is None:
        verbose = __verbose
    
    if background:
        threading.Thread(target=_runner, kwargs={'times':times, 'request':request, 'interval':interval, 'verbose_':verbose}).start()
    else:
        #oldVerbose = verbose(isVerbose)
        _runner(times=times, request=request, interval=interval, verbose_=verbose)
        #verbose(oldVerbose)

def runScript(script:str) -> bool:
    """	Run a command via the Upper Tester interface.
    """
    if not upperTester:
        printmd('**No command interface available**', c='red')
        return False
    return requests.post(upperTester, headers = { 'X-M2M-UTCMD' : script }).status_code == 200


def resetCSE(verbose:bool = False) -> bool:
    """	Send an Upper Tester command to reset the CSE.
    """
    if not runScript('reset'):
        if verbose:
            printmd('**Error during reset**', c='red')
        return False
    if verbose:
        printmd('**CSE sucessfully resetted**', c='green')
    return True


def setupInitialResourceStructure(kind:str, verbose:bool = False) -> bool:
    """	Send an Upper Tester command to create a first set of resources the CSE.
    """
    if not runScript(f'notebooksPrepareResources {kind}'):
        if verbose:
            printmd('**Error during resource preparation**', c='red')
            return False
    if verbose:
        printmd('**Resources prepared**', c='green')
    return False

    


##############################################################################

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


##############################################################################

def checkCSEConnection(id:str) -> str:
    """ Check the connection to the CSE.
    """
    try:
        r = requests.get(f'{host}/{id}')
        if r.status_code == 404:	# correct host, but address is wrong
            return http.client.responses[r.status_code]
    except Exception as e:
        return str(e)
    return None


def cleanCSE() -> bool:
    try:
        r = requests.get(f'{host}/__reset__')
        return r.status_code == 200
    except Exception as e:
        return False
    return True


# The following Exception class is used to show a dialog to the user and gracefully stops the execution
# of the current cell.

# class StopExecution(Exception):
#     def __init__(self, message):
#         super().__init__(message, 'Execution Stopped')
#         printmd('**' + message + '**', 'red')

#     def _render_traceback_(self):# Prevent printing of stacktrace 
#         pass


def nu():
    return notificationURLBase + ':' + str(notificationPort)


def lastResponse() -> dict:
    """ Return the last response.
    """
    return __response


def lastResponseStatus() -> int:
    """ Return the last response status code.
    """
    return __responseStatusCode


def retrieveOK() -> bool:
    """ Return whether the last request returned OK.
    """
    return __responseStatusCode == 2000


def verbose(verbose_=True, withResults_=True) -> bool:
    """ Set the verbosity to True.
    """
    global __verbose, __withResults
    old = __verbose
    __verbose = verbose_
    __withResults = withResults_
    return old


def noverbose(withResult=True):
    """ Set the verbosity to False.
    """
    global __verbose, __withResults
    __verbose = False
    __withResults = withResult


decimalMatch = re.compile(r'{(\d+)}')
def findXPath(dct, key, default=None):
    """ Find a structured `key` in the dictionary `dct`. If `key` does not exists then
        `default` is returned.

        It is possible to address a specific element in an array. This is done be
        specifying the element as `{n}`.

        Example: findXPath(resource, 'm2m:cin/{1}/lbl/{0}')

        If an element if specified as '{}' then all elements in that array are returned in
        an array.

        Example: findXPath(resource, 'm2m:cin/{1}/lbl/{}') or findXPath(input, 'm2m:cnt/m2m:cin/{}/rn')

    """

    if key is None or dct is None:
        return default

    paths = key.split("/")
    data = dct
    i = 0
    while i < len(paths):
        if data is None:
             return default
        pathElement = paths[i]
        if len(pathElement) == 0:	# return if there is an empty path element
            return default
        elif (m := decimalMatch.search(pathElement)) is not None:	# Match array index {i}
            idx = int(m.group(1))
            if not isinstance(data, (list,dict)) or idx >= len(data):	# Check idx within range of list
                return default
            if isinstance(data, dict):
                data = data[list(data)[i]]
            else:
                data = data[idx]
        elif pathElement == '{}':
            if not isinstance(data, (list,dict)):
                return default
            if i == len(paths)-1:
                return data
            return [ findXPath(d, '/'.join(paths[i+1:]), default) for d in data  ]

        elif pathElement not in data:	# if key not in dict
            return default
        else:
            data = data[pathElement]	# found data for the next level down
        i += 1

    return data


def getDate(delta:int=0) -> str:
    return toISO8601Date(datetime.datetime.utcnow() + datetime.timedelta(seconds=delta))


def toISO8601Date(ts) -> str:
    if isinstance(ts, float):
        ts = datetime.datetime.utcfromtimestamp(ts)
    return ts.strftime('%Y%m%dT%H%M%S,%f')


# Print debug messages in red
def highlightDebugMessage(text):
    if (start := text.find('\"m2m:dbg\"', 0)) > -1:
        end = text.find('\n', start)
        text = text[:start] + '<span style=\'color:red\'>' + text[start:end] + '</span>' + text[end:]
    return text



# Apply optional proxy settings
if 'httpProxy' in globals() and httpProxy is not None:
    os.environ['http_proxy'] = httpProxy
if 'httpsProxy' in globals() and httpsProxy is not None:
    os.environ['https_proxy'] = httpsProxy 

# At the end of the init check whether the CSE is up and running
if (msg := checkCSEConnection(cseRN)):
    printConnectionError(msg)
else:
    printmd(f'**Configuration Ready ({cseRN})**', c='green')

    # if there is an argument then take this, reset the CSE, and run the preparation scipt with this parameter
    if len(sys.argv) == 2:
        resetCSE()
        setupInitialResourceStructure(sys.argv[1])
        showResourceTree(False, 'Initial Resource Tree')


