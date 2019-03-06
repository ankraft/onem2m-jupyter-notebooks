# Configuration

url              = 'http://localhost:8080/in-name'     # The URL of the CSE we want to connect to
originator       = 'admin:admin'                       # Originator ID to access the CSE
notificationPort = 8000                                # Port that the Notification Server binds to


########################## End of  Configuration ##########################


import requests, json

# Tidy-print a response header.
def printResponse(r):
    print(str(r.status_code) + ' (' + r.reason + ')')
    print('========== Headers ==========')
    for h in r.headers:
        print(h + ':' + r.headers[h])
    if r.text:
        print('\n========== Body ==========')
        print(r.text)
    