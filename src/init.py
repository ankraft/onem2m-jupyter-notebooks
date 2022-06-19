#
#   init.py
#
#   (c) 2021 by Andreas Kraft
#   License: BSD 3-Clause License. See the LICENSE file for further details.
#


import datetime, random, re, sys, time, threading, os, shlex
import http.client
from enum import IntEnum
from json import loads, dumps
import IPython.display
from IPython.display import HTML, Markdown, clear_output
import requests

from config import *
from annotations import *
from simulator import *
from oauth import *

# Parameter names
_originator = 'X-M2M-Origin'
_requestIdentifier = 'X-M2M-RI'
_resourceType = 'ResourceType'
_releaseVersionIndicator = "X-M2M-RVI"

# user-friendly names
cseBaseName = cseRN


# Resource Type names
class Type(IntEnum):
    ACP                =    1
    AE                 =    2
    Container          =    3
    ContentInstance    =    4
    Group              =    9
    MgmtObj            =   13
    Node               =   14
    Subscription       =   23
    FlexContainer      =   28
    TimeSeries         =   29
    TimeSeriesInstance =   30

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

# Authentication
__oauthToken = None

def printmd(s, c=None, hd=''):
    """ Print and format as Markdown.
    """
    if c:
        cs = f"{hd}<span style='color:{c}'>{s}</span>"
    else:
        cs = f'{hd}{s}'
    # The extra blank lines are necessary when HTML + MD mix
    printHtml("""<div style="float:right;">
    
    """)
    IPython.display.display(Markdown(cs))
    printHtml("""
    
    </div>""")


def printHtml(s):
    IPython.display.display(HTML(s))


def htmlGetJSON(jsn, req = None):
    """ Format and return JSON formatted as HTML.
    """
    if jsn:
        _j = None
        if isinstance(jsn, str):
            _j = loads(jsn)
        elif isinstance(jsn, dict):
            _j = jsn
        if _j is not None:
           return f'<pre>{annotateAttributesHtml( highlightDebugMessage( dumps(_j, indent = 4)), showLongNames )}</pre>'
    return ''


def htmlGetRequestResponseJSON(req, isRequest):
        return f"""<details>
                    <summary><b>oneM2M {"Request" if isRequest else "Response"}</b></summary>
                    <p><pre>{dumps({ 'm2m:rqp' : req } if isRequest else { 'm2m:rsp' : req }, indent = 4)}</pre></p>
                </details>"""


def clearCell():
    """ Clear the current output cell.
    """
    clear_output(wait=True)


excludedHeaders = [ 'Access-Control-Allow-Origin', 'Authorization', 'Connection', 'Content-Length', 'Date', 'ETag',
                    'request-context', 'Server', 'Strict-Transport-Security', 'Transfer-Encoding'
                  ]
""" http headers excluded from printing on the notebook. """


def htmlParametersTable(parameters) -> str:
    """ Format the headers as a table and return an HTML snippet.
    """
    rows = ''
    for h,v in parameters.items():
        if h in excludedHeaders:
            continue
        if h == 'X-M2M-RSC':
            v = annotateRSCHtml(v)
        rows += f"""<tr><td style="text-align:left;">{annotateHeaderFieldHtml(h)}</td>
                        <td style="text-align:left;">{toOneM2MParameter(h)}</td>
                        <td style="text-align:left;">{v}</td>
                    </tr>"""

    return f"""
<table>
<thead>
	<tr><th style="text-align:left;">HTTP Header</th>
        <th style="text-align:left;">Request Attribute</th>
        <th style="text-align:left;">Value</th>
    </tr>
</thead>
<tbody>
    {rows}
</tbody>
</table>
    """


def getStatusCodeHtml(statusCode, reason, extra:str = None):
    extra = f'<br>{extra}' if extra else ''
    return f""" <p>
                    <span style="color:{'green' if 200 <= statusCode < 300 else 'red'};">
                        {statusCode} ({reason}){extra}
                    </span>
                </p>"""


def printRequestResponse(parameters, 
                         content = None, 
                         url = None, 
                         statusCode = None, 
                         reason = None,  
                         method = None,
                         req={}):
    """ Print the request. 
    """

    headerTitle = 'Request' if statusCode is None else 'Response'
    headerHtml = f'<h3>HTTP {headerTitle}</h3>' 
    urlHtml = f"""<h4>Target URL</h4>
                     <p>{url}</p>
               """ if url is not None else ''
    statusCodeHtml = ''
    if statusCode is not None and reason is not None:   # response
        statusCodeHtml = getStatusCodeHtml(statusCode, reason, findXPath(loads(content), 'm2m:dbg') if content else None)


    # HTML for content rendering
    contentHtml = ''
    dividerHtml = ''
    if content:
        dividerHtml +=  'padding-right:40px;border-right:1px solid grey;'
        contentHtml += f"""<div style="float:left;padding-left:40px;">
                                <h4 style="text-align:center;background:#eeeeee;padding:4px 0px 4px 0px;">{headerTitle} Content | Body</h4>
                                {htmlGetJSON(content)}
                           </div>
                        """

    # HTML for Headers and printing the HTML
    printHtml(f"""{headerHtml}
                  {urlHtml}
                  {statusCodeHtml}
                  <div style="display:flex;">
                      <div style="float:left;top:0px;bottom:0px;flex-height:100%;{dividerHtml}">
                          <h4 style="text-align:center;background:#eeeeee;padding:4px 0px 4px 0px;">Headers</h4>
                          {htmlParametersTable(parameters)}
                      </div>
                      {contentHtml}
                  </div>
             """)

    if url:
        printCurlHtml(url, method, parameters, content) # TODO ge chanto html return

    if req:
        printHtml(htmlGetRequestResponseJSON(req, isRequest = url is not None))


def printCurlHtml(url, method, parameters, content):
    hs = ' '.join([ f'-H \'{k}:{v}\'' for k,v in parameters.items()])
    if content:
        out = f'curl -X {method.__name__.upper()} {hs} -d {shlex.quote(content)} {url}'
    else:
        out = f'curl -X {method.__name__.upper()} {hs} {url}'

    printHtml("""
    <script>
    function CopyAlert(id) {
        a = document.getElementById(id+'_1');
        b = document.getElementById(id+'_2');
        a.style.display = 'none';
        b.style.display = 'block';
        setTimeout(function() {
            b.style.display = 'none';
            a.style.display = 'block';
        }, 1000)
    }
    function CopyToClipboard(id) {
        var r = document.createRange();
        r.selectNode(document.getElementById(id));
        window.getSelection().removeAllRanges();
        window.getSelection().addRange(r);
        document.execCommand('copy');
        window.getSelection().removeAllRanges();
        CopyAlert(id);
    }

    </script>
    """)
    id = str(random.randint(1,sys.maxsize))
    printHtml(f"""
	<details><summary><b>cURL Request</b></summary>
    <div style="background-color:#efeff3;">
        <div id="{id}" style="padding:10px;font-family:monospace;font-size:x-small;word-break:break-all;">{out}</div>
        <div style="padding-bottom:10px;text-align:center;font-size:small;height:40px;">
            <div id="{id}_1">
                <button onclick="CopyToClipboard(\'{id}\');return false;" style="border:2px solid #005480;background-color:transparent;border-radius:4px;padding:5px;color:#005480;">
                    <b>Copy to clipboard</b>
                </button>
            </div>
            <div id="{id}_2" style="display:none;color:#005480;padding:4px;">
                <b>copied</b>
            </div>
        </div>
    </div>
	</details>
    """)


def printShortResponse(r):
    """ Print terse response code. 
    """
    if not 200 <= r.status_code < 300:
        printHtml(getStatusCodeHtml(r.status_code, r.reason, findXPath(loads(r.text), 'm2m:dbg')))

    elif __withResults: # only when results should be printed
        printHtml(getStatusCodeHtml(r.status_code, r.reason))


def printHtmlError(s, details = None):
    detailsHtml = f"""<br>
                        <details>
                            <summary><b>Details</b></summary>
                            <p>{details}</p>
                        </details>
                    """ if details else ''
    printHtml(f"""<p>
                    <div class="alert alert-block alert-danger" style="background-color: transparent; border: 4px solid; padding: 10px; width:calc(100% - 350px);">
                        <b><i class="fa fa-exclamation-triangle" aria-hidden="true"></i>&nbsp; Error</b><br>
                        {s}
                        {detailsHtml}
                    </div>
                  </p>""")


def printConnectionError(msg:str):
    printHtmlError(f"""
<b>Cannot access the CSE, or the CSE is not runnning.</b></br>
Please <a href="start-cse.ipynb" target="_new">start the CSE</a> or check the configuration file <a href="/edit/src/config.py" target=_new>config.py</a>. 
Did you specify the correct address, credentials, and proxy server?</br>
Please restart this notebook kernel in case you will update the configuration file.<br>
""", msg)


def getResourceTreeHtml(section:bool, title:str) -> None:
    if (resp := requests.get(f'{host}/__structure__/text')).status_code == 200:
        return f"""{'<hr/>' if section else ''}
                   <h3>{title}</h3>
                   <pre>{annotateRTHtml(resp.text, showLongNames)}</pre>'
                """
    return ''


def printResourceTree(section:bool = True, title:str = 'CSE Resource Tree'):
    printHtml(getResourceTreeHtml(section, title))


#############################################################################
#
#   Request Handling
#
#   The following request methods hide a bit of the complexity of constructing the
#   requests and make them easier to read.

_operationMapping = {
    requests.post   : 1,	# CREATE
    requests.get    : 2,	# RETRIEVE
    requests.put    : 3,	# UPDATE
    requests.delete : 4,	# DELETE
}

def _sendRequest(method, **parameters) -> str:
    global __response, __responseStatusCode, __verbose, __oauthToken
    __response = None
    headers = {}
    rqp = {}
    fc = {} # filter criteria

    """ Check and update the given parameters, and send a request with the given method.
    """

    # add the operation to the request
    rqp['op'] = _operationMapping[method]

    # check and extract some parameters. Most parameters need individual handling.
    if (to := parameters.pop('to', None)) is None:
        return '<b>to</b> parameter is missing'
    rqp['to'] = to

    if (originator := parameters.pop('originator', None)) is None:
        return '<b>originator</b> parameter is missing'
    if not isinstance(originator, str):
        return '<b>originator</b> parameter must be a string'
    headers[_originator] = originator
    rqp['fr'] = originator

    if (primitiveContent := parameters.pop('primitiveContent', None)) is None and method in [ requests.post, requests.put ]:
        return '<b>primitiveContent</b> parameter is missing'
    if primitiveContent is not None: # could be None when method is get() or delete()
        primitiveContent = primitiveContent if isinstance(primitiveContent, str) else dumps(primitiveContent)   # Transform content to JSON 
        primitiveContent = jsonLong2Short(primitiveContent)

    if (resourceType := parameters.pop('resourceType', None)) is None and method in [ requests.post ]:
        return '<b>resourceType</b> parameter is missing'
    if resourceType is not None:
        if not isinstance(resourceType, int):
            return '<b>resourceType</b> parameter must be an integer number'
        rqp['ty'] = resourceType

    if len(rqi := parameters.pop('requestIdentifier', f'ri-{random.randint(1,sys.maxsize)}')) == 0:
        return '<b>requestIdentifier</b> parameter must not be empty'
    if not isinstance(rqi, str):
        return '<b>requestIdentifier</b> parameter must be a string'
    headers[_requestIdentifier] = rqi
    rqp['rqi'] = rqi

    if len(rvi := parameters.pop('releaseVersionIndicator', '3')) == 0:
        return '<b>releaseVersionIndicator</b> parameter must not be empty'
    if not isinstance(rvi, str):
        return '<b>releaseVersionIndicator</b> parameter must be a string'
    headers[_releaseVersionIndicator] = rvi
    rqp['rvi'] = rvi
    
    headers['Content-Type'] = f'application/json{f";ty={resourceType}" if resourceType is not None else ""}'
    headers['Accept'] = 'application/json'  # Always send an 'Accept' header even when not needed
    if resourceType is not None:
        rqp['ty'] = resourceType

    args = ''
    if (fu := parameters.pop('filterUsage', None)) is not None:
        if not isinstance(fu, int):
            return '<b>filterUsage</b> parameter must be an integer number'
        args += f'{"&" if len(args)>0 else ""}fu={fu}'
        fc['fu'] = fu

    if (filterCriteria := parameters.pop('filterCriteria', None)) is not None:
        if not isinstance(filterCriteria, dict):
            return '<b>filterCriteria</b> parameter must be a dictionary'
        for k, v in filterCriteria.items():
            _v = ''
            if isinstance(v, str):
                _v = v
            elif isinstance(v, bool):
                _v = str(v).lower()
            elif isinstance(v, list):
                _v = '+'.join(v)
            else:
                _v = v
            _k = long2short(k)
            args += f'{"&" if len(args)>0 else ""}{_k}={_v}'
            fc[_k] = v


    if (rcn := parameters.pop('resultContent', None)) is not None:
        if not isinstance(rcn, int):
            return '<b>resultContent</b> parameter must be an integer number'
        args += f'{"&" if len(args)>0 else ""}rcn={rcn}'
        fc['rcn'] = rcn

    if (lvl := parameters.pop('level', None)) is not None:
        if not isinstance(lvl, int):
            return '<b>level</b> parameter must be an integer number'
        args += f'{"&" if len(args)>0 else ""}lvl={lvl}'
        fc['lvl'] = lvl

    if (ty := parameters.pop('type', None)) is not None:
        if not isinstance(ty, int):
            return '<b>childType</b> parameter must be an integer number'
        args += f'{"&" if len(args)>0 else ""}ty={ty}'
        fc['ty'] = ty

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
    if fc:
        rqp['fc'] = fc
    if primitiveContent:
         rqp['pc'] = loads(primitiveContent) # Put pc last

    
    # Send request 'repeat' times
    for i in range(repeat):

        try:
            
            # Handle authentication for each request
            if doOAuth:
                if (token := getOAuthToken(__oauthToken)) is None:
                    return 'error retrieving oauth token'
                __oauthToken = token
                headers['Authorization'] = f'Bearer {__oauthToken.token}'
            
            args = f'?{args}' if len(args) > 0 else ''
            url = f'{host}{to}{args}'
            if primitiveContent is not None:
                resp = method(url, headers=headers, data=primitiveContent)
            else:
                resp = method(url, headers=headers)
            __response = resp.json() if len(resp.content) else None
            __responseStatusCode = int(resp.headers['X-M2M-RSC']) if resp.headers.get('X-M2M-RSC') else -1
            __rqi = resp.headers['X-M2M-RI'] if resp.headers.get('X-M2M-RI') else None
            __rvi = resp.headers['X-M2M-RVI'] if resp.headers.get('X-M2M-RVI') else None
            __ot = resp.headers['X-M2M-OT'] if resp.headers.get('X-M2M-OT') else None
            
            rsp = {}
            rsp['rsc'] = __responseStatusCode
            if __rqi:
                rsp['rqi'] = __rqi
            if __rvi:
                rsp['rvi'] = __rvi
            if __ot:
                rsp['ot'] = __ot
            if __response:
                rsp['pc'] = __response

            # TODO TBC

            if _verbose:
                printRequestResponse(headers, primitiveContent, url = url, method = method, req = rqp)
                printRequestResponse(resp.headers, resp.text, statusCode = resp.status_code, reason = resp.reason, req = rsp)
                printResourceTree()
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
    if not runScript('Reset'):	# uppercase!
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

##############################################################################



# Modify the Notebooks general CSS a bit
# Align tables to the left of the cell
printHtml('<style>table {align:left;display:block}</style>')

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
        if upperTester is None:
            printmd('**Upper Tester interface is not available.**', c = 'red')
            printmd('Please don\'t provide an argument for the init script.')
        else:
            resetCSE()
            setupInitialResourceStructure(sys.argv[1])
            printResourceTree(False, 'Initial Resource Tree')

