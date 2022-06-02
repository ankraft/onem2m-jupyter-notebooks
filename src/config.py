# ACME Local
cseRN                 = 'cse-in'
host                  = f'http://localhost:8080/'
defaultOriginator     = 'CAdmin'
upperTester           = f'{host}/__ut__'		# Or None if not defined

# Extra Configurations
showLongNames         = True

# Notification Server
notificationURLBase   = 'http://localhost'                          # The base URL for the Notification Server
notificationPort      = 9999										# Notification port
notificationURL       = f'{notificationURLBase}:{notificationPort}' # Notification full URL

# Proxy configuration
httpProxy             = None
httpsProxy            = None

# OAuth2 Server
doOAuth               = False
oauthServerUrl        = None
clientSecret          = None
clientId              = None
