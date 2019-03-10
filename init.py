############################# Configuration ##############################

url              = 'http://localhost:8080/in-name'     # The URL of the CSE we want to connect to
originator       = 'admin:admin'                       # Originator ID to access the CSE
notificationPort = 8000                                # Port that the Notification Server binds to


########################## End of Configuration ##########################


import requests, json
import IPython.display

# Print and format as Markdown
def printmd(s):
    IPython.display.display(IPython.display.Markdown(s))

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
