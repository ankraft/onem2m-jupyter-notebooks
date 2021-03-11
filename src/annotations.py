
# The \x03 in the strings will be replaced in a later stage with newlines, before actual output
shortLongNames = {
    'acpi'  : 'access control policy IDs\x03This attribute contains a list of identifiers for <accessControlPolicy> resources. The privileges defined in the <accessControlPolicy> resources that are referenced determine who is allowed to access the resource containing this attribute for a specific purpose (e.g. Retrieve, Update, Delete, etc.).',
    'acop'  : 'access control operations\x03The accessControlOperations is a mandatory parameter in an access-control-rule-tuple that represents the set of operations that are authorized using this access control rule.',
    'acor'  : 'access control originators\x03The accessControlOriginators is a mandatory parameter in an access-control-rule-tuple. It represents the set of Originators that shall be allowed to use this access control rule. The special Originator \'all\' means any Originators are allowed to access the resource within the accessControlOriginators constraints.',
    'acr'   : 'access control rules\x03A set of access control rules that are comprised of access-control rule-tuples.',
    'aei'   : 'AE ID\x03An AE-ID uniquely identifies an AE resident on an M2M Node. It identifies an Application Entity for the purpose of all interactions within the M2M System. Mandatory.',
    'api'   : 'App-ID\x03An Application Identifier uniquely identifies an M2M Application in a given context. It starts with R (registered) or N (non-registered). Mandatory.',
    'cbs'   : 'current byte size\x03Current size in bytes of data (i.e. content attribute of a <contentInstance> resource) stored in all direct child resources (e.g.<contentInstance>) of a resource. This is the summation of contentSize attribute values of the resources. It is limited by the maxByteSize attribute. Mandatory.',
    'cnf'   : 'content info',
    'cni'   : 'current number of instances\x03Current number of direct child resource (e.g. <contentInstance>) in the resource. It is limited by the maxNrOfInstances. The currentNrOfInstances attribute of the resource is updated on successful creation or deletion of direct child resource (e.g. <contentInstance>) of the resource. Mandatory.',
    'cnd'   : 'container definition\x03This attribute contains an identifier reference (URI) to the <flexContainer> schema definition which shall be used by the CSE to validate the syntax of the <flexContainer> resource.',
    'cnm'   : 'current number of members',
    'con'   : 'content',
    'cr'    : 'creator',
    'cs'    : 'content size\x01Size in bytes of the content attribute(s).',
    'csi'   : 'CSE identifier\x03A CSE is identified by a unique identifier, the CSE-ID, when instantiated within an M2M Node in the M2M System. The CSE-ID in a resource identifier (e.g. the To parameter) indicates the Hosting CSE of the resource. Mandatory.',
    'cst'   : 'CSE type\x03Indicates the type of CSE represented by the created resource. Mandatory for an IN-CSE.',
    'csy'   : 'consistency strategy',
    'csz'   : 'content serializations\x03The list of supported serializations of the Content primitive parameter for receiving a request from its registrants (e.g. XML, JSON). The list is ordered so that the most preferred format comes first. Optional.',
    'ct'    : 'creation time\x03Time/date of creation of the resource. This read-only attribute is assigned by the CSE at the time when the resource is locally created. Mandatory.',
    'enc'   : 'eventNotification criteria',
    'et'    : 'expiration time\x03Time/date after which the resource will be deleted by the Hosting CSE. This attribute can be provided by the Originator, and in such a case it will be regarded as a hint to the Hosting CSE on the lifetime of the resource. Optional.',
    'exc'   : 'expiration counter',
    'hld'   : 'holder\x03The AE-ID, M2M-User-ID or CSE-ID of the entity which owns the resource containing this attribute.',
    'lbl'   : 'labels\x03A list of tokens used to add meta-information to resources. Optional.',
    'lt'    : 'last modified time\x03Last modification time/date of the resource. The attribute is set by the CSE when the resource is created, and it is updated when the resource is updated.',
    'mbs'   : 'max byte size\x03Maximum size in bytes of data (i.e. content attribute of a <contentInstance> resource) that is allocated for the resource for all direct child resources (e.g. <contentInstances>) in the resource.',
    'mid'   : 'member identifiers',
    'mni'   : 'max number of instances\x03Maximum number of direct child resources (e.g. <contentInstances>) in a resource.',
    'mnm'   : 'max number of members',
    'mt'    : 'member type',
    'mtv'   : 'member type validated',
    'nct'   : 'notification content type',
    'net'   : 'notification event type',
    'nev'   : 'notification event',
    'nm'    : 'name',
    'nu'    : 'notification URI''s',
    'pi'    : 'parent identifier\x03The resourceID of the parent of this resource. The value of this attribute is an empty string for the <CSEBase> resource type.',
    'poa'   : 'point of access\x03Represents the list of physical addresses to be used by remote CSEs to connect to a CSE or AE (e.g. IP address, FQDN). Mandatory for the CSE, optional for AE and CSERemote.',
    'pv'    : 'privileges\x03A set of access control rules that applies to resources referencing this <accessControlPolicy> resource using the accessControlPolicyID attribute. Mandatory.',
    'pvs'   : 'self-privileges\x03A set of access control rules that apply to the <accessControlPolicy> resource itself and accessControlPolicyIDs attribute of any other resource which is linked to this <accessControlPolicy> resource. Mandatory.',
    'rep'   : 'representation',
    'ri'    : 'resource identifier\x03An identifier for the resource that is used for \'non-hierarchical addressing method\' and uniquely identifies a resource. It is unique in that CSE.',
    'rn'    : 'resource name\x03The name for the resource that is used for \'hierarchical addressing method\' to represent the parent-child relationships of resources. If left out in creation requests, the CSE assigns a unique resource name on its own. Mandatory.',
    'rqi'   : 'request identifier',
    'rr'    : 'request reachability\x03This attribute indicates whether a resource can receive requests. Mandatory',
    'rrl'   : 'resources result list',
    'rsc'   : 'response status code',
    'rvi'   : 'release version indicator',
    'srt'   : 'supported resource types\x03List of oneM2M release versions which are supported by the CSE. Mandatory.',
    'srv'   : 'supported release versions\x03An array that specifies the supported oneM2M specification releases. Mandatory',
    'ssi'   : 'semantic support indicator',
    'st'    : 'state tag\x03An incremental counter of modification on the resource. When a resource is created, this counter is set to 0, and it will be incremented on every modification of the resource',
    'sur'   : 'subscription reference',
    'ty'    : 'resource type\x03This read-only attribute identifies the type of the resource. Each resource has a resourceType attribute. Mandatory.',
    'typ'   : 'resource type',
    'val'   : 'value',
    'vrq'   : 'verification request',

    'm2m:ae'    : 'Application Entity\x03An entity in the application layer that implements an M2M application service logic.',
    'm2m:acp'   : 'Access Control Policy\x03The Access Control Policies (ACPs) is used by the CSE to control access to the resources and their attributes. It is designed to fit different access control models such as access control lists, role or attribute based access control.',
    'm2m:agr'   : 'agregated response',
    'm2m:cb'    : 'CSEbase\x03A \<CSEBase> resource represents a CSE. It is the root for all resources that are residing in the CSE.',
    'm2m:cin'   : 'content instance',
    'm2m:cnt'   : 'Container\x03The \<container> resource represents a container for data instances. It is used to share information with other entities and potentially to track the data. A \<container> resource has no associated content. It has only attributes and child resources.',
    'm2m:dbg'   : 'debug information and error messages',
    'm2m:grp'   : 'group',
    'm2m:rrl'   : 'resources result list',
    'm2m:rsp'   : 'response',
    'm2m:sgn'   : 'notification',
    'm2m:sub'   : 'subscription',

}


def annotateShortnames(text):
    ''' Add hover tooltips for shortnames.
    '''
    for sh, ln in shortLongNames.items():
        text = text.replace(f'"{sh}"', f'"[{sh}](#_blank "{ln}")"')
    return text


def annotateRT(text):
    ''' Add hover tooltips for shortnames.
    '''
    for sh, ln in shortLongNames.items():
        text = text.replace(f'-> {sh} |', f'-> [{sh}](#_blank "{ln}") |')
    return text


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
        rsc = rsc.replace('%s' % rsc, '[%s](#_blank "%s")' % (rsc, v))
    return rsc


headerFields = {
    'X-M2M-RSC'     : ('Result Status Code - The request\'s extended result status code. Mandatory in the response.', 'Result Status Code'), 
    'X-M2M-Origin'  : ('Originator - The request\'s \'From\' parameter. It represents the identity of the entity who makes the request. Mandatory in the request and response.', 'From'),
    'X-M2M-RI'      : ('Request Identifier - Used to uniquely identify a request. Mandatory in the request and response.', 'Request Identifier'),
    'X-M2M-RVI'     : ('Release Version Indicator - The requester indicates the release version of the oneM2M specification. Mandatory in the request.', 'Release Version Indicator'),
    'Accept'        : ('The Originator may use the Accept header to indicate which media types are acceptable for the response', ''),
    'Content-Type'  : ('Any HTTP request or response with content shall include the Content-type header set to one of \'application/xml\', \'application/json\', or the oneM2M defined media types', ''),
    'Date'          : ('The response\'s date in UTC/GMT', ''),
}


def annotateHeaderField(hf:str) -> str:
    if (v := headerFields.get(hf)) is not None:
        return hf.replace(hf, f'[{hf}](#_blank "{v[0]}")')
    return hf

def toOneM2MParameter(hf:str) -> str:
    if (v := headerFields.get(hf)) is not None:
        return v[1]
    return ''


