############################# Configuration ##############################

#basename              = 'cse-in'                             # The basename of the CSE
basename              = 'oneMPOWER-IN-CSE'                             # The basename of the CSE
#url                   = 'http://localhost:8080/' + basename  # The URL of the CSE we want to connect to
url                   = 'http://localhost:9011/' + basename  # The URL of the CSE we want to connect to
#originator            = 'CAdmin'                             # Originator ID to access the CSE
originator            = 'C_def'                             # Originator ID to access the CSE
notificationPort      = 8000                                 # Port that the Notification Server binds to
notificationInterface = ''                                   # Network interface the  Notifcation Server binds to
notificationURLBase   = 'http://localhost'                   # The base URL for the Notification Server

########################## End of Configuration ##########################