#
#	annotations.py
#
#	(c) 2021 by Andreas Kraft
#	License: BSD 3-Clause License. See the LICENSE file for further details.
#

#linkColor = '#b42025'	# oneM2M Red
#linkColor = '#005480'	# oneM2M Blue
#linkColor = '#F6921E'	# oneM2M Orange
linkColor = '#668C97'	# oneM2M Turquoise
linkWeight = 'bold'
keywordStyle = f'color:{linkColor};font-weight:{linkWeight}'

# The \x03 in the strings will be replaced in a later stage with newlines, before actual output
explanations = {
    'acpi'  : 'acpi - access control policy IDs\x03This attribute contains a list of identifiers for <accessControlPolicy> resources. The privileges defined in the <accessControlPolicy> resources that are referenced determine who is allowed to access the resource containing this attribute for a specific purpose (e.g. Retrieve, Update, Delete, etc.).',
    'acop'  : 'acop - access control operations\x03The accessControlOperations is a mandatory parameter in an access-control-rule-tuple that represents the set of operations that are authorized using this access control rule.',
    'acor'  : 'acor - access control originators\x03The accessControlOriginators is a mandatory parameter in an access-control-rule-tuple. It represents the set of Originators that shall be allowed to use this access control rule. The special Originator \'all\' means any Originators are allowed to access the resource within the accessControlOriginators constraints.',
    'acr'   : 'acr - access control rules\x03A set of access control rules that are comprised of access-control rule-tuples.',
    'aei'   : 'aei - AE ID\x03An AE-ID uniquely identifies an AE resident on an M2M Node. It identifies an Application Entity for the purpose of all interactions within the M2M System. Mandatory.',
    'api'   : 'api - App-ID\x03An Application Identifier uniquely identifies an M2M Application in a given context. It starts with R (registered) or N (non-registered). Mandatory.',
    'cbs'   : 'cbs - current byte size\x03Current size in bytes of data (i.e. content attribute of a <contentInstance> resource) stored in all direct child resources (e.g.<contentInstance>) of a resource. This is the summation of contentSize attribute values of the resources. It is limited by the maxByteSize attribute. Mandatory.',
    'cnf'   : 'cnf - content info\x03This attribute contains information for AEs to understand the content s of content attribute. It is composed of two mandatory components consisting of Internet Media Type and an encoding type. In addition, an optional content security component may also be included.',
    'cni'   : 'cni - current number of instances\x03Current number of direct child resource (e.g. <contentInstance>) in the resource. It is limited by the maxNrOfInstances. The currentNrOfInstances attribute of the resource is updated on successful creation or deletion of direct child resource (e.g. <contentInstance>) of the resource. Mandatory.',
    'cnd'   : 'cnd - container definition\x03This attribute contains an identifier reference (URI) to the <flexContainer> schema definition which shall be used by the CSE to validate the syntax of the <flexContainer> resource.',
    'cnm'   : 'cnm - current number of members\x03Current number of members in a group.',
    'con'   : 'con - content\x03Actual content of a contentInstance. This content may be opaque data and understandable with the help of the contentInfo.',
    'cr'    : 'cr - creator',
    'cs'    : 'cs - content size\x03Size in bytes of the content attribute(s).',
    'csi'   : 'csi - CSE identifier\x03A CSE is identified by a unique identifier, the CSE-ID, when instantiated within an M2M Node in the M2M System. The CSE-ID in a resource identifier (e.g. the To parameter) indicates the Hosting CSE of the resource. Mandatory.',
    'cst'   : 'cst - CSE type\x03Indicates the type of CSE represented by the created resource. Mandatory for an IN-CSE.',
    'csy'   : 'csy - consistency strategy\x03This attribute determines how to deal with the \<group> resource if the memberType validation fails. Possible values are 1 (ABANDON_MEMBER, 2 (ABANDON_GROUP, and 3 (SET_MIXED)',
    'csz'   : 'csz - content serializations\x03The list of supported serializations of the Content primitive parameter for receiving a request from its registrants (e.g. XML, JSON). The list is ordered so that the most preferred format comes first. Optional.',
    'ct'    : 'ct - creation time\x03Time/date of creation of the resource. This read-only attribute is assigned by the CSE at the time when the resource is locally created. Mandatory.',
    'ctm'	: 'ctm - current time\x03The current time of the CSE. An Originator retrieving this attribute can use this time value to adjust and synchronize its time value to the time value of this CSE.',
    'dc'	: 'dc -  description\x03Text format description of <mgmtObj>.',
    'dlb'	: 'dlb - device label\x03Unique device label assigned by the manufacturer. The value of the attribute typically exposes the device’s serial number that is specific to a manufacturer and possibly further restricted within the manufacturer by a deviceType or model.',
    'dty'	: 'dty - device type\x03The type (e.g. cell phone, photo frame, smart meter) or product class (e.g. X-series) of the device.',
    'dvnm'	: 'dvnm - device name\x03The device name.',
    'enc'   : 'enc - event notification criteria\x03Indicates the event criteria for which a notification is to be generated.',
    'et'    : 'et - expiration time\x03Time/date after which the resource will be deleted by the Hosting CSE. This attribute can be provided by the Originator, and in such a case it will be regarded as a hint to the Hosting CSE on the lifetime of the resource. Optional.',
    'exc'   : 'exc - expiration counter',
    'fwv'	: 'fwv - firmware version\x03The firmware version of the device. If the device only supports one kind of Software this is identical to swVersion.',
    'hld'   : 'hld - holder\x03The AE-ID, M2M-User-ID or CSE-ID of the entity which owns the resource containing this attribute.',
    'hwv'	: 'hwv - hardware version\x03The hardware version of the device.',
    'lbl'   : 'lbl - labels\x03A list of tokens used to add meta-information to resources. Optional.',
    'lt'    : 'lt - last modified time\x03Last modification time/date of the resource. The attribute is set by the CSE when the resource is created, and it is updated when the resource is updated.',
    'man'	: 'man - manufacturer\x03The name/identifier of the device manufacturer.',
    'mbs'   : 'mbs - max byte size\x03Maximum size in bytes of data (i.e. content attribute of a <contentInstance> resource) that is allocated for the resource for all direct child resources (e.g. \<contentInstances>) in the resource.',
    'mfd' 	: 'mfd - manufacturing date\x03Manufacturing date of device.',
    'mfdl'	: 'mfdl - manufacturer details link\x03URL to manufacturer\'s website.',
    'mgd'	: 'mgd - management definition\x03Specifies the type of \<mgmtObj> resource e.g. software, firmware, memory.',
    'mid'   : 'mid - member resource IDs\x03List of member resource IDs. This could be normal resources, or other groups as well.',
    'mni'   : 'mni - max number of instances\x03Maximum number of direct child resources (e.g. \<contentInstances>) in a resource.',
    'mnm'   : 'mnm - max number of members\x03Maximum number of members in a \<group>.',
    'mod'	: 'mod - model\x03The name/identifier of the device mode assigned by the manufacturer.',
    'mt'    : 'mt - member type\x03The resource type of the member resources of a group, if all member resources (including the member resources in any sub-groups) are of the same type. Otherwise, it is of type \'mixed\'.',
    'mtv'   : 'mtv - member type validated\x03Denotes if the resource types of all members\' resources of the group have been validated by the Hosting CSE. In the case that the memberType attribute of the \<group> resource is not \'mixed\', then this attribute shall be set.',
    'nct'   : 'nct - notification content type\x03Notification content type that shall be contained in notifications.',
    'net'   : 'net - notification event type\x03The type of event that shall trigger a notification. If multiple notificationEventType tags are present, a notification shall be triggered if any of the configured events occur.',
    'nev'   : 'nev - notification event',
    'ni'	: 'ni - node ID\x03The M2M-Node-ID of the node which is represented by this \<node> resource.',
    'nm'    : 'nm - name\x03A resource name',
    'nu'    : 'nu - notification URI''s\x03A list consisting of one or more targets that the Hosting CSE shall send notifications to.',
    'osv'	: 'osv - operating system version\x03Version of the operating system (defined by manufacturer).',
    'pc'	: 'pc - primitive content\x03The content of request, usually contains a resource.',
    'pi'    : 'pi - parent identifier\x03The resourceID of the parent of this resource. The value of this attribute is an empty string for the \<CSEBase> resource type.',
    'poa'   : 'poa - point of access\x03Represents the list of physical addresses to be used by remote CSEs to connect to a CSE or AE (e.g. IP address, FQDN). Mandatory for the CSE, optional for AE and CSERemote.',
    'pv'    : 'pv - privileges\x03A set of access control rules that applies to resources referencing this <accessControlPolicy> resource using the accessControlPolicyID attribute. Mandatory.',
    'pvs'   : 'pvs - self-privileges\x03A set of access control rules that apply to the <accessControlPolicy> resource itself and accessControlPolicyIDs attribute of any other resource which is linked to this <accessControlPolicy> resource. Mandatory.',
    'rep'   : 'rep - representation',
    'ri'    : 'ri - resource identifier\x03An identifier for the resource that is used for \'non-hierarchical addressing method\' and uniquely identifies a resource. It is unique in that CSE.',
    'rn'    : 'rn - resource name\x03The name for the resource that is used for \'hierarchical addressing method\' to represent the parent-child relationships of resources. If left out in creation requests, the CSE assigns a unique resource name on its own. Mandatory.',
    'rqi'   : 'rqi - request ID\x03The request ID tracks requests initiated by an AE or by a CSE end to end.',
    'rr'    : 'rr - request reachability\x03This attribute indicates whether a resource can receive requests. Mandatory',
    'rrf'	: 'rrf - resource reference\x03A list of child resource structures',
    'rrl'   : 'rrl - resources result list\x03A list of child resource references',
    'rsc'   : 'rsc - response status code\x03Indicates that a result of the requested operation is successful, unsuccessful, acknowledgement or status of processing such as authorization timeout, etc.',
    'rvi'   : 'rvi - release version indicator\x03Indicates the release version of the oneM2M specification. Mandatory in the request.',
    'smod'	: 'smod - sub-model\x03Device sub-model name.',
    'srt'   : 'srt - supported resource types\x03List of oneM2M resource types which are supported by the CSE. Mandatory.',
    'srv'   : 'srv - supported release versions\x03An array that specifies the supported oneM2M specification releases. Mandatory',
    'ssi'   : 'ssi - semantic support indicator^\x03Indicator of support for semantic discovery functionality via \<semanticFanOutPoint>.',
    'st'    : 'st - state tag\x03An incremental counter of modification on the resource. When a resource is created, this counter is set to 0, and it will be incremented on every modification of the resource',
    'sur'   : 'sur - subscription reference',
    'swv'   : 'swv - software version\x03The software version of the device.',
    'to'    : 'to - target resource ID\x03The target resource ID of a requerst or response.',
    'ty'    : 'ty - resource type\x03This read-only attribute identifies the type of the resource. Each resource has a resourceType attribute. Mandatory.',
    'typ'   : 'ty - resource type\x03The resource type of a child resource',
    'val'   : 'val - value\x03Usually the URI of a child resource',
    'vrq'   : 'vrq - verification request',

    'm2m:ae'    : 'Application Entity\x03An entity in the application layer that implements an M2M application service logic.',
    'm2m:acp'   : 'Access Control Policy\x03The Access Control Policies (ACPs) is used by the CSE to control access to the resources and their attributes. It is designed to fit different access control models such as access control lists, role or attribute based access control.',
    'm2m:agr'   : 'agregated response\x03Used when aggregating responses by a group.',
    'm2m:cb'    : 'CSEbase\x03A \<CSEBase> resource represents a CSE. It is the root for all resources that are residing in the CSE.',
    'm2m:cin'   : 'content instance\x03The \<contentInstance> resource represents a data instance in the \<container> resource.',
    'm2m:cnt'   : 'Container\x03The \<container> resource represents a container for data instances. It is used to share information with other entities and potentially to track the data. A \<container> resource has no associated content. It has only attributes and child resources.',
    'm2m:csr'   : 'remoteCSE\x03A \<remoteCSE> represents another CSE that is registered to the a CSE.',
    'm2m:dbg'   : 'debug information and error messages',
    'm2m:dvi'	: 'deviceInfo\x03The [deviceInfo] resource specialization is used to share information regarding the device.',
    'm2m:grp'   : 'group\x03The \<group> resource represents a group of resources of the same or mixed types.',
    'm2m:la'	: 'latest\x03The \<latest> resource is a virtual resource and represents the latest of the \'instance\' resources of the parent.',
    'm2m:nod'	: 'node\x03The \<node> resource represents specific information that provides properties of an M2M Node that can be utilized by other oneM2M operations.',
    'm2m:ol'	: 'oldest\x03The \<oldest> resource is a virtual resource and represents the oldest of the \'instance\' resources of the parent.',
    'm2m:sub'   : 'subscription\x03The \<subscription> resource contains subscription information for its subscribed-to resource.',

    'm2m:rrl'   : 'rrl - resources result list',
    'm2m:rsp'   : 'rsp - response\x03One or many response primitives.',
    'm2m:sgn'   : 'sgn - notification',

    'cod:color'	: 'cod:colour\x03The [cod:colour] \<flexContainer> specialization from the oneM2M \'common domain\'.',
    'blue'		: 'blue\x03The RGB blue colour value',
    'green'		: 'green\x03The RGB green colour value',
    'red'		: 'red\x03The RGB red colour value',

}


shortLongNames = [
    ('acpi', 'accessControlPolicyIDs'),
    ('acop', 'accessControlOperations'),
    ('acor', 'accessControlOriginators'),
    ('acr',  'accessControlRule'),
    ('aei',  'AE-ID'),
    ('api',  'App-ID'),
    ('cbs',  'currentByteSize'),
    ('cnf',  'contentInfo'),
    ('cni',  'currentNrOfInstances'),
    ('cnd',  'containerDefinition'),
    ('cnm',  'currentNrOfMembers'),
    ('con',  'content'),
    ('cr',   'creator'),
    ('cs',   'contentSize'),
    ('csi',  'CSE-ID'),
    ('cst',  'cseType'),
    ('csy',  'consistencyStrategy'),
    ('csz',  'contentSerializations'),
    ('ct',   'creationTime'),
    ('ctm',  'currentTime'),
    ('dc',   'description'),
    ('dlb',  'deviceLabel'),
    ('dty',  'deviceType'),
    ('dvnm', 'deviceName'),
    ('enc',  'eventNotificationCriteria'),
    ('et',   'expirationTime'),
    ('exc',  'expirationCounter'),
    ('fwv',  'fwVersion'),
    ('hld',  'holder'),
    ('hwv',  'hwVersion'),
    ('lbl',  'labels'),
    ('lt',   'lastModifiedTime'),
    ('man',  'manufacturer'),
    ('mbs',  'maxByteSize'),
    ('mfd',  'manufacturingDate'),
    ('mfdl', 'manufacturerDetailsLink'),
    ('mgd',  'mgmtDefinition'),
    ('mid',  'memberIDs'),
    ('mni',  'maxNrOfInstances'),
    ('mnm',  'maxNrOfMembers'),
    ('mod',  'model'),
    ('mt'    'memberType'),
    ('mtv',  'memberTypeValidated'),
    ('nct',  'notificationContentType'),
    ('net',  'notificationEventType'),
    ('nev',  'notificationEvent'),
    ('ni',   'nodeID'),
    ('nm',   'name'),
    ('nu',   'notificationURI'),
    ('osv',  'osVersion'),
    ('pc',   'primitiveContent'),
    ('pi',   'parentID'),
    ('poa',  'pointOfAccess'),
    ('pv',   'privileges'),
    ('pvs',  'selfPrivileges'),
    ('rep',  'representation'),
    ('ri',   'resourceID'),
    ('rn',   'resourceName'),
    ('rqi',  'requestIdentifier'),
    ('rr',   'requestReachability'),
    ('rrf',  'resourceRef'),
    ('rrl',  'resourceRefList'),
    ('rsc',  'responseStatusCode'),
    ('rvi',  'releaseVersionIndicator'),
    ('smod', 'subModel'),
    ('srt',  'supportedResourceType'),
    ('srv',  'supportedReleaseVersions'),
    ('ssi',  'semanticSupportIndicator'),
    ('st',   'stateTag'),
    ('sur',  'subscriptionReference'),
    ('swv',  'swVersion'),
    ('to',   'to'),
    ('ty',   'resourceType'),
    ('typ',  'type'),
    ('val',  'value'),
    ('vrq',  'verificationRequest'),

    ('m2m:ae',  'm2m:ApplicationEntity'),
    ('m2m:acp', 'm2m:AccessControlPolicy'),
    ('m2m:agr', 'm2m:aggregatedResponse'),
    ('m2m:cb',  'm2m:CSEBase'),
    ('m2m:cin', 'm2m:ContentInstance'),
    ('m2m:cnt', 'm2m:Container'),
    ('m2m:csr', 'm2m:remoteCSE'),
    ('m2m:dbg', 'm2m:Debug'),
    ('m2m:dvi', 'm2m:deviceInfo'),
    ('m2m:grp', 'm2m:Group'),
    ('m2m:la',  'm2m:latest'),
    ('m2m:nod', 'm2m:Node'),
    ('m2m:ol',  'm2m:oldest'),
    ('m2m:sub', 'm2m:Subscription'),

    ('m2m:rrl', 'resourceRefList'),
    ('m2m:rsp', 'm2m:responsePrimitive'),
    ('m2m:rqp', 'm2m:requestPrimitive'),
    ('m2m:sgn', 'notification'),

    ('cod:color', 'cod:colour'),
    ('blue',      'blue'),
    ('green',     'green'),
    ('red',       'red'),

]

def short2long(name):
    for n in shortLongNames:
        if n[0] == name:
            return n[1]
    return name


def long2short(name):
    for n in shortLongNames:
        if n[1] == name:
            return n[0]
    return name


def annotateAttributes(text, longNames = False):
    ''' Add hover tooltips for shortnames.
    '''
    for sh, ln in explanations.items():
        nm = short2long(sh) if longNames else sh
        text = text.replace(f'"{sh}"', f'"[<span style="{keywordStyle}">{nm}</span>](#_blank "{ln}")"')
    return text


def annotateRT(text, longNames = False):
    ''' Add hover tooltips for resource type shortnames.
    '''
    for sh, ln in explanations.items():
        #print(f'{sh} -> {ln}')
        nm = short2long(sh) if longNames else sh
        text = text.replace(f' -> {sh} ', f' -> [<span style="{keywordStyle}">{nm}</span>](#_blank "{ln}") ')
        text = text.replace(f'{sh}=', f'[<span style="{keywordStyle}">{nm}</span>](#_blank "{ln}")=')
    return text


def jsonLong2Short(primitiveContent):
    for n in shortLongNames:
        primitiveContent = primitiveContent.replace(f'"{n[1]}"', f'"{n[0]}"')
    return primitiveContent


rscCodes = {
    '2000' :    'OK - The request succeeded',
    '2001' :    'Created - The resource was successfully created',
    '2002' :    'Deleted - The resource was successfully deleted',
    '2004' :    'Updated - The resource was successfully updated',
    '4000' :    'Bad Request',
    '4004' :    'Not Found',
    '4005' :    'Operation not allowed',
    '4102' :    'Contents unacceptable',
    '4103' :    'Originator has no privilege',
    '4105' :    'Conflict',
    '4107' :    'Security association required',
    '4108' :    'Invalid child resource type',
    '4110' :    'Group member type inconsistent',
    '5000' :    'Internal server error',
    '5001' :    'Not implemented',
    '5103' :    'Target not reachable',
    '5105' :    'Receiver has no privileges',
    '5106' :    'Already exists',
    '5203' :    'Target not subscribable',
    '5204' :    'Subscription verification initiation failed',
    '5207' :    'Not acceptable',
    '6010' :    'Max number of member exceeded',
    '6023' :    'Invalid arguments',
    '6023' :    'Insufficient arguments',
}

def annotateRSC(rsc):
    if (v := rscCodes.get(rsc)) is not None:
        rsc = rsc.replace(f'{rsc}', f'[<span style="{keywordStyle}">{rsc}</span>](#_blank "{v}")')
    return rsc


headerFields = {
    'X-M2M-RSC'     : ('Response Status Code - The request\'s extended response status code. Mandatory in the response.', 'Response Status Code'), 
    'X-M2M-Origin'  : ('Originator - The request\'s \'From\' parameter. It represents the identity of the entity who makes the request. Mandatory in the request and response.', 'From'),
    'X-M2M-RI'      : ('Request ID - The request ID tracks requests initiated by an AE or by a CSE end to end. Mandatory in the request and response.', 'Request Identifier'),
    'X-M2M-RVI'     : ('Release Version Indicator - The requester indicates the release version of the oneM2M specification. Mandatory in the request.', 'Release Version Indicator'),
    'X-M2M-OT'      : ('Originating Timestamp - The date and time when the request was sent.', 'Originating Timestamp'),
    'Accept'        : ('The Originator may use the Accept header to indicate which media types are acceptable for the response', ''),
    'Content-Type'  : ('Any HTTP request or response with content shall include the Content-type header set to one of \'application/xml\', \'application/json\', or the oneM2M defined media types', ''),
    'Date'          : ('The response\'s date in UTC/GMT', ''),
}


def annotateHeaderField(hf:str) -> str:
    if (v := headerFields.get(hf)) is not None:
        return hf.replace(hf, f'[<span style="{keywordStyle}">{hf}</span>](#_blank "{v[0]}")')
    return hf

def toOneM2MParameter(hf:str) -> str:
    if (v := headerFields.get(hf)) is not None:
        return v[1]
    return ''


