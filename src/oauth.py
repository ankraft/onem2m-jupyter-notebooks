import collections, time
import requests
from config import *

##############################################################################
#
#   OAuth Handling
#

Token = collections.namedtuple('Token', 'token expiration')
_expirationLeeway	= 5.0		# 5 seconds leeway for token expiration

def getOAuthToken(token=None, kind='keycloak'):
	"""	Retrieve and return a oauth2 token. If there is a provided token that is still valid, then that token
		is returned.

		This function returns a new named tuple Token(token, expiration), or None in case of an error. The expiration 
		is in epoch seconds.
	"""
	if token is None:
		token = Token(token=None, expiration=0.0)

	# Return the old token, if it exists and is not expired
	if token.expiration > time.time() and token.token is not None:
		return token

	# Retrieve a new token
	if kind == 'keycloak':
		headers = {
			'contentType' 	: 'application/x-www-form-urlencoded',
		}
		formData = {
			'grant_type' 	: 'client_credentials',
			'client_secret'	: clientSecret,
			'client_id'		: clientId,
		}
		# print(oauthServerUrl)
		# print(formData)
		if (response := requests.post(oauthServerUrl	, data=formData, headers=headers)).status_code == 200:
			data = response.json()
			if data is None or 'access_token' not in data or 'expires_in' not in data:
				return None
		return	Token(token	     = data['access_token'],
					expiration = time.time() + data['expires_in'] - _expirationLeeway
				)
	return None
