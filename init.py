############################# Configuration ##############################

url              = 'http://localhost:8080/in-name'     # The URL of the CSE we want to connect to
originator       = 'admin:admin'                       # Originator ID to access the CSE
notificationPort = 8000                                # Port that the Notification Server binds to


########################## End of Configuration ##########################


import requests, json
import IPython.display
import ipywidgets as widgets
import re

# variable to distinguish users
_uid = ''

# Print and format as Markdown
def printmd(s, c=None):
    if c:
        cs = "<span style='color:{}'>{}</span>".format(c, s)
    else:
        cs = s
    IPython.display.display(IPython.display.Markdown(cs))

    
# Print the request
def printRequest(url):
    printmd('Sending request to **' + url + '**')

# Tidy-print a response header.
def printResponse(r):
    printmd('---\n### Response')
    print(str(r.status_code) + ' (' + r.reason + ')')
    printmd('\n**Headers**')
    for h in r.headers:
        print(h + ':' + r.headers[h])
    if r.text:
        printmd('\n**Body**\n')
        print(r.text)
    printmd('---')

# Show a javascript dialog
def dialog(msg, title=''):
    jsreq = '''
    require(
        ["base/js/dialog"], 
        function(dialog) {
            dialog.modal({
                title: '%s',
                body: '%s',
                buttons: {
                    'Dismiss': {  }
                }
            });
        }
    );
    ''' % (title, msg)
    IPython.display.display(IPython.display.Javascript(jsreq))
    

# The following request methods hide a bit of the complexity of constructing the
# requests and make them easier to read.

def GET(url, headers):
    printRequest(url)
    printResponse(requests.get(url, headers=headers))

def POST(url, headers, body):
    printRequest(url)
    printResponse(requests.post(url, headers=headers, data=body))

def DELETE(url, headers):
    printRequest(url)
    printResponse(requests.delete(url, headers=headers))
    
def PUT(url, headers, body):
    printRequest(url)
    printResponse(requests.put(url, headers=headers, data=body))


# The following Exception class is used to show a dialog to the user and gracefully stops the execution
# of the current cell.

class StopExecution(Exception):
    def __init__(self, message):
        super().__init__(message, 'Execution Stopped')
        printmd('**' + message + '**', 'red')

    def _render_traceback_(self):# Prevent printing of stacktrace 
        pass

# Retrieve the value of the _uid variable and create identifiers for ae, acp etc
# If it is not set then stop the execution of the cell by raising an exception

def _checkuid():
    if len(_uid) < 1:
        dialog('Please provide a username in the field at the top of this notebook.', 'Execution Stopped')
        raise StopExecution('ERROR: PLEASE PROVIDE A USERNAME') # This stops the execution

def ae():
    _checkuid()
    return 'AE_' + _uid

def acp():
    _checkuid()
    return 'ACP_' + _uid


# The following code presents an input field for the user to enter a username during the initialization
# This username is later used in all requests to distinguis various users on the CSE

def on_value_change(change):
    global _uid
    _uid = change['new']
    _uid = re.sub(r'[^a-zA-Z0-9_]',r'', _uid) # remove non-printables, white spaces etc

printmd('### Enter Username')
printmd('Please enter a unique username or identifier that will be used in the requests in order to distinguish the various users of the CSE.', 'green')
printmd('You may want to re-use a username from a previous oneM2M notebook lecture.')

field = widgets.Text(
    value='',
    placeholder='username for the lecture',
    description='Username:',
    disabled=False
)
field.style.background_color='#ff0000'
display(field)
field.observe(on_value_change, names='value')

  