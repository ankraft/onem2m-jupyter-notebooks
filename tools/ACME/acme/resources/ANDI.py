#
#	ANDI.py
#
#	(c) 2020 by Andreas Kraft
#	License: BSD 3-Clause License. See the LICENSE file for further details.
#
#	ResourceType: mgmtObj:areaNwkDeviceInfo
#

from .MgmtObj import *
from Constants import Constants as C
from Validator import constructPolicy
import Utils

# Attribute policies for this resource are constructed during startup of the CSE
attributePolicies = constructPolicy([ 
	'ty', 'ri', 'rn', 'pi', 'acpi', 'ct', 'lt', 'et', 'lbl', 'at', 'aa', 'daci', 
	'mgd', 'obis', 'obps', 'dc', 'mgs', 'cmlk',
	'dvd', 'dvt', 'awi', 'sli', 'sld', 'ss', 'lnh'
])


defaultAreaNwkType = ''


class ANDI(MgmtObj):

	def __init__(self, jsn=None, pi=None, create=False):
		super().__init__(jsn, pi, C.tsANDI, C.mgdANDI, create=create, attributePolicies=attributePolicies)

		if self.json is not None:
			self.setAttribute('dvd', defaultAreaNwkType, overwrite=False)
			self.setAttribute('dvt', '', overwrite=False)
			self.setAttribute('awi', '', overwrite=False)
