############################# Configuration ##############################

cseRN                 = 'cse-in'                                    # The resource name of the CSE
url                   = 'http://localhost:8080/' + cseRN            # The URL of the CSE we want to connect to
originator            = 'CAdmin'                                    # Originator ID to access the CSE
notificationPort      = 9999                                        # Port that the Notification Server binds to
notificationInterface = ''                                          # Network interface the  Notifcation Server binds to
notificationURLBase   = 'http://localhost'                          # The base URL for the Notification Server
notificationURL       = f'{notificationURLBase}:{notificationPort}' # Notification URL
########################## End of Configuration ##########################