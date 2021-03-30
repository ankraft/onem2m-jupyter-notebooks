############################# Configuration ##############################

cseRN                 = 'cse-in'                             # The basename of the CSE
cseID                 = 'id-in'
host                  = 'http://localhost:8080/'             # Base URL of the host
url                   =  host + cseRN                     # The URL of the CSE we want to connect to
originator            = 'CAdmin'                             # Originator ID to access the CSE
notificationPort      = 8000                                 # Port that the Notification Server binds to
notificationInterface = ''                                   # Network interface the  Notifcation Server binds to
notificationURLBase   = 'http://notebooks'                   # The base URL for the Notification Server

########################## End of Configuration ##########################
