# oneM2M Jupyter Notebooks
This repository contains a number of [Jupyter Notebooks](https://jupyter.org) that give a practical introduction to programmatically interacting with a [oneM2M](http://www.onem2m.org) CSE. The notebooks explain how to access a  CSE, add and update resources, and more.


## Installation and Running

### oneM2M Notebooks

- Download or clone this repository to a local directory.

### oneM2M CSE
The notebooks have been tested with *Eclipse om2m*.

- Install [Eclipse om2m](https://www.eclipse.org/om2m/). A Java 1.7 (or later) runtime is a requirement.
- Configure (see [Server (IN-CSE) configuration](https://wiki.eclipse.org/OM2M/one/Starting#Server_.28IN-CSE.29_configuration)).
- Remember the *IN-CSE HTTP listening port* and the *IN-CSE ip address*, because we need these values when configuring the notebooks later.
- You also should set the configuration setting `org.eclipse.om2m.dbReset` to *true* in order to get a clean CSE environment when you restart the CSE.
- Start (see [IN-CSE startup](https://wiki.eclipse.org/OM2M/one/Starting#IN-CSE_startup)) an IN-CSE instance.

### Jupyter Notebooks
Prerequisite: The notebooks use Python 3 and the [requests](http://python-requests.org) library.

- Install Jupyter locally. See [Installing the Jupyter Notebook](https://jupyter.org/install) for further details
- Start a local Jupyter Notebook server in the directory of this repository's copy (s.a.). See [Running the Notebook](https://jupyter.readthedocs.io/en/latest/running.html#running) for further details.
- A web page should open. Here, you select notebook you like to run.

#### Troubleshooting
When you open a notebook in your web browser you might get an error message about a "failed connection". In this case you might try another browser. When starting the Jupyter Notebook server you see a message in the console with a URL that you can paste in a browser:

    http://localhost:8888/?token=<a long token>

You must use this URL including the token, because this authenticates the connection to the local Jupiter Notebook server.

## Using the Notebooks

### Configuration

Please change the configuration in the file [init.py](init.py) according to your setup. Normally, it shouldn't be necessary to change this when using the vanilla configuration from the *Eclipse om2m* installation.

- **url** : The URL of the CSE we want to connect to in the examples in the notebooks.
- **originator** : Originator ID to access the CSE.
- **notificationPort** : The port for Notification Server.


### Running the Examples


You can (almost) execute the notebooks in any order, but you should execute [onem2m-02-basic-resources.ipynb](onem2m-02-basic-resources.ipynb) to create the basic resource structure for the subsequent notesbooks.

You may always restart the om2m CSE to reset the resource structure, or run the [onem2m-99-cleanup.ipynb](onem2m-99-cleanup.ipynb) notebook to remove the structure from the CSE.

- [onem2m-01-introduction.ipynb](onem2m-01-introduction.ipynb)  
An introduction that demonstrates how to retrieve the root &lt;CSEBase> resource.
- [onem2m-02-basic-resources.ipynb](onem2m-02-basic-resources.ipynb)  
This notebook shows your how to create and work with the basic oneM2M resources: &lt;AE>, &lt;Container> and &lt;ContentInstance>.
- [onem2m-03-discovery.ipynb](onem2m-03-discovery.ipynb)  
How do you search for resources in a CSE?
- [onem2m-04-groups.ipynb](onem2m-04-groups.ipynb)  
Group resources together and send requests to a group instead of each single resource.
- [onem2m-05-accesscontrol.ipynb](onem2m-05-accesscontrol.ipynb)  
Control access to resources with Access Control Policies.
- [onem2m-06-notifications-server.ipynb](onem2m-06-notifications-server.ipynb)  
Start a Notification Server that is required by the [onem2m-06a-notifications.ipynb](onem2m-06a-notifications.ipynb) notebook for receiving notifications.
- [onem2m-06a-notifications.ipynb](onem2m-06a-notifications.ipynb)  
Subscribe to changes of resources and receive notifications.
- [onem2m-07-flexcontainer.ipynb](onem2m-07-flexcontainer.ipynb)  
What are &lt;FlexContainers> and how to use them?

### Cleanup


- [onem2m-99-cleanup.ipynb](onem2m-99-cleanup.ipynb)  
The code in this notebook removes the resources created by the other notebooks. This should be the last notebook to run, but can be executed when necessary.









