############################# Configuration ##############################

basename              = 'cse-in'                             # The basename of the CSE
url                   = 'http://localhost:8080/' + basename  # The URL of the CSE we want to connect to
originator            = 'CAdmin'                             # Originator ID to access the CSE
notificationPort      = 8000                                 # Port that the Notification Server binds to
notificationInterface = ''                                   # Network interface the  Notifcation Server binds to
notificationURLBase   = 'http://localhost'                   # The base URL for the Notification Server
logfile               = 'logs.db'                            # Optional filename for the log data base
doUID                 = False                                # Handle requests with a UserID

########################## End of Configuration ##########################