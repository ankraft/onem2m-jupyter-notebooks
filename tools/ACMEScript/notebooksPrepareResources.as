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
# Check and create demo AE
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


#
# Check and create container under demo AE
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


#
# Check and create a second container under demo AE
#
procedure checkContainer_2
	checkResource [cse.rn]/Notebook-AE/Container_2
	if [!= [result] 2000]
		create [cse.rn]/Notebook-AE
			{
				"m2m:cnt": {
					"rn": "Container_2"
				}
			}
		if [!= [response.status] 2001]
			logError Error creating Container: [response.resource]
			quitWithError
		endIf
		print Created <container>: Container_2
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
print
print Performing initializations for lecture *[argv 1]*

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
		checkAE
		checkContainer
		checkContainer_2
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


