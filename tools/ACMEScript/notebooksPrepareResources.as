@name notebooksPrepareResources
@description Setup resources for the Notebooks
@uppertester

originator Cmyself 


#
#	Check whether the resource exists under the given path
#
procedure checkResource
	# Save originator
	set o [request.originator]
	
	# Try to retrieve resource
	originator [cse.originator]
	retrieve [argv 1]

	# Restore originator
	originator [o]
endProcedure [response.status]


#
# Check and create demo AE's
#
procedure checkAE
	checkResource [cse.rn]/Notebook-AE
	if [!= [result] 2000]
		create [cse.rn]
			{
				"m2m:ae": {
					"rn": "Notebook-AE",
					"api": "NnotebookAE",
					"rr": true,
					"srv": \[ "3" ]
				}
			}
		if [!= [response.status] 2001]
			logError Error creating AE: [response.resource]
			quitWithError
		endIf
		print Created <AE>: Notebook-AE
	endif 
endProcedure


procedure checkAE_1
	checkResource [cse.rn]/Notebook-AE-1
	if [!= [result] 2000]
		create [cse.rn]
			{
				"m2m:ae": {
					"rn": "Notebook-AE-1",
					"api": "NnotebookAE",
					"rr": true,
					"srv": \[ "3" ]
				}
			}
		if [!= [response.status] 2001]
			logError Error creating AE: [response.resource]
			quitWithError
		endIf
		print Created <AE>: Notebook-AE-1
	endif 
endProcedure


procedure checkLightAE_1
	checkResource [cse.rn]/StreetLight-AE-1
	if [!= [result] 2000]
		create [cse.rn]
			{
				"m2m:ae": {
					"rn": "StreetLight-AE-1",
					"api": "NnotebookAE",
					"rr": true,
					"srv": \[ "3" ]
				}
			}
		if [!= [response.status] 2001]
			logError Error creating AE: [response.resource]
			quitWithError
		endIf
		print Created <AE>: StreetLight-AE-1
	endif 
endProcedure



procedure checkLightAE_2
	checkResource [cse.rn]/StreetLight-AE-2
	if [!= [result] 2000]
		create [cse.rn]
			{
				"m2m:ae": {
					"rn": "StreetLight-AE-2",
					"api": "NnotebookAE",
					"rr": true,
					"srv": \[ "3" ]
				}
			}
		if [!= [response.status] 2001]
			logError Error creating AE: [response.resource]
			quitWithError
		endIf
		print Created <AE>: StreetLight-AE-2
	endif 
endProcedure


#
# Check and create containers under demo AE's
#
procedure checkContainer
	checkResource [cse.rn]/Notebook-AE/Container
	if [!= [result] 2000]
		create [cse.rn]/Notebook-AE
			{
				"m2m:cnt": {
					"rn": "Container"
				}
			}
		if [!= [response.status] 2001]
			logError Error creating Container: [response.resource]
			quitWithError
		endIf
		print Created <container>: Container
	endif 
endProcedure


procedure checkLightContainer_1
	checkResource [cse.rn]/StreetLight-AE-1/Light-Container-1
	if [!= [result] 2000]
		create [cse.rn]/StreetLight-AE-1
			{
				"m2m:cnt": {
					"rn": "Light-Container-1"
				}
			}
		if [!= [response.status] 2001]
			logError Error creating Container: [response.resource]
			quitWithError
		endIf
		print Created <container>: Light-Container-1
	endif 
endProcedure


procedure checkLightContainer_2
	checkResource [cse.rn]/StreetLight-AE-1/Light-Container-2
	if [!= [result] 2000]
		create [cse.rn]/StreetLight-AE-2
			{
				"m2m:cnt": {
					"rn": "Light-Container-2"
				}
			}
		if [!= [response.status] 2001]
			logError Error creating Container: [response.resource]
			quitWithError
		endIf
		print Created <container>: Light-Container-2
	endif 
endProcedure


#
# Add a couple of contentInstances under the container
#
procedure addContentInstances
	while [< [loop] 5]
		create [cse.rn]/Notebook-AE/Container
			{
				"m2m:cin": {
					"cnf": "text/plain:0",
					"con": "Hello, World! [loop]"
				}
			}
		if [!= [response.status] 2001]
			logError Error creating contentInstance: [response.resource]
			quitWithError
		endIf
	endWhile
	print Added <contentInstances>
endProcedure



#
#	Check and create resources depending on the notebook's name
#
#print
#print Performing initializations for lecture *[argv 1]*

switch [lower [argv 1]]
	case introduction
		# Nothing to do for introduction Setup
	case basic
		# Nothing to do for basic Setup
	case discovery
		checkAE
		checkContainer
		addContentInstances
	case groups
		originator Cmyself_1
		checkLightAE_1
		checkLightContainer_1
		originator Cmyself_2
		checkLightAE_2
		checkLightContainer_2
	case acp
		checkAE
	case flexcontainer
		checkAE
	case subscriptions
		checkAE
		checkContainer
	case
		print Unknown lecture *[argv 1]*
		quitWithError
endswitch


