# oneM2M Jupyter Notebooks
This repository contains a number of [Jupyter Notebooks](https://jupyter.org) that give a practical introduction to programmatically interacting with a [oneM2M](http://www.onem2m.org) CSE. The notebooks explain how to access a  CSE, add and update resources, and more.

- [Installation and Running](#installation)  
- [Docker](#docker)  
- [Using the Notebooks](#using)  


<a name="installation"></a>
## Installation and Running

### oneM2M Notebooks

- Download or clone this repository to a local directory.
- Check the configuration 

#### Configuration

Please change the configuration in the file [config.py](config.py) according to your setup. Normally, it shouldn't be necessary to change this when using the vanilla configuration from the *Eclipse om2m* installation.

- **basename** : The basename of the CSE.
- **url** : The URL of the CSE we want to connect to in the examples in the notebooks.
- **originator** : Originator ID to access the CSE.
- **notificationPort** : The port for Notification Server.
- **notificationInterface** : The network interface the Notifcation Server binds to. An empty string means "all interfaces".
- **notificationURLBase** : The base URL for the Notification Server.


#### Notification Server
The Notification server is a separate notebook [onem2m-06-notifications-server.ipynb](onem2m-06-notifications-server.ipynb) that implements a simple notification server.

You may provide your own notification server, though.


### oneM2M CSE
The notebooks have been tested with the [ACME oneM2M CSE](https://github.com/ankraft/ACME-oneM2M-CSE).

### Jupyter Notebooks
#### Prerequisite
The notebooks use

- Python 3.
- The [requests](http://python-requests.org) library

		pip3 install requests


#### Installation
- Install Jupyter locally. See [Installing the Jupyter Notebook](https://jupyter.org/install) for further details
- Start a local Jupyter Notebook server in the directory of this repository's copy (s.a.). See [Running the Notebook](https://jupyter.readthedocs.io/en/latest/running.html#running) for further details.  
For a local installation with out an authentication token the command could be

		jupyter notebook --NotebookApp.token=''


- A web page should open. Here, you select notebook you like to run.  
Some browsers are not able to connect to the kernel service. See See the *Troubleshooting* section below.

#### Troubleshooting
When you open a notebook in your web browser you might get an error message about a "failed connection". In this case you might try another browser. When starting the Jupyter Notebook server you see a message in the console with a URL that you can paste in a browser, for example: ``http://localhost:8888/?token=<a long token>`` .

If you enabled the authentication token (which is the default) then you must use this URL including the token, because this authenticates the connection to the local Jupiter Notebook server.

If you run the Jupyter Notebook server without authentication token (see the *--NotebookApp.token* option above), just use, for example ``http://localhost:8888`` .

<a name="docker"></a>
## Docker
This section explains how to generate a Docker container for the notebooks and running it.

### Building a Docker Container

There is already a [Dockerfile](Dockerfile) in the distribution to build a new Docker container. After starting your Docker instance, just run the command:

	docker build -t notebook .

### Running the Docker Container

To run the built container use the following command:

	docker run -p 8888:8888 --rm --name notebook notebook

The container will still be running attached to your terminal. To detach it, add the *-d* option. 

The *--rm* option removes the notebook container from your Docker instance after termination. This is useful because it removes all output and changes you might have done to the notebooks during a session.

Please note that the notebooks might not launch in your browser automatically, but you can access the Notebooks via your browser at [http://localhost:8888](http://localhost:8888).


### Downloading & Running from DockerHub

You might also just download a pre-provisioned version of the notebooks from [https://hub.docker.com](https://hub.docker.com):

	docker run -p 8888:8888 --rm --name onem2m-notebooks ankraft/onem2m-notebooks

### Running a Complete Istallation with Docker Compose
To run the the notebooks together with a pre-configured [ACME CSE](https://github.com/ankraft/ACME-oneM2M-CSE):

- In a terminal shell in the [same directory](tools/Docker) as the [docker-compose.yml](tools/Docker/docker-compose.yml) file resides, run the command ```docker-compose up -d```
- Open the following URLs in a web browser
	- The notebooks: [http://localhost:8888](http://localhost:8888)
	- The CSE's web UI : [http://localhost:8080](http://localhost:8080)
- To shutdown the notebooks and the CSE,  run the command ```docker-compose down``` 

<a name="using"></a>
## Using the Notebooks

### Running the Examples

You can (almost) execute the notebooks in any order, but you should at least execute [onem2m-02-basic-resources.ipynb](onem2m-02-basic-resources.ipynb) to create the basic resource structure for the subsequent notebooks.

Each notebook has an *init* section. Please execute this section before executing any of the other sections.

You may always restart the om2m CSE to reset the resource structure, or run the [onem2m-99-cleanup.ipynb](onem2m-99-cleanup.ipynb) notebook to remove the structure from the CSE.

#### CSE & Notification Server Notebooks
- [start-cse.ipynb](start-cse.ipynb)  
This notebook runs a local CSE inside the a notebook. It is required for all the examples in the notebooks.
- [start-notificationServer.ipynb](start-notificationServer.ipynb)  
Notebook for receiving notifications. This must be run before using [onem2m-06-notifications-server.ipynb](onem2m-06-notifications-server.ipynb).

#### oneM2M Notebooks
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
- [onem2m-06-notifications.ipynb](onem2m-06a-notifications.ipynb)  
Subscribe to changes of resources and receive notifications.
- [onem2m-07-flexcontainer.ipynb](onem2m-07-flexcontainer.ipynb)  
What are &lt;FlexContainers> and how to use them?

### Cleanup

- [onem2m-99-cleanup.ipynb](onem2m-99-cleanup.ipynb)  
The code in this notebook removes the resources created by the other notebooks. This should be the last notebook to run, but can be executed whenever necessary.


## Docker
This section explains how to generate a Docker container for the notebooks and running it.

### Building a Docker Container

There is already a [Dockerfile](tools/Docker/Dockerfile) in the distribution to build a new Docker container. After starting your Docker instance, just run the command:

	docker build -t notebook .

or use the provided shell script in the same directory.

### Running the Docker Container

To run the built container use the following command:

	docker run -p 8888:8888 --rm --name notebook notebook

The container will still be running attached to your terminal. To detach it, add the *-d* option. 

The *--rm* option removes the notebook container from your Docker instance after termination. This is useful because it removes all output and changes you might have done to the notebooks during a session.

Please note that the notebooks might not launch in your browser automatically, but you can access the Notebooks via your browser at [http://localhost:8888](http://localhost:8888).


### Downloading & Running from DockerHub

You might also just download a pre-provisioned version of the notebooks from [https://hub.docker.com](https://hub.docker.com):

	docker run -p 8888:8888 --rm --name onem2m-notebooks ankraft/onem2m-notebooks

or use the provided shell script in the same directory.

### Running with Docker Compose
To run the the notebooks together with the ACME CSE:

- In a terminal shell in the same directory as the *docker-compose.yml* file resides, run the command

		docker-compose up -d

- To shutdown the notebooks and the CSE,  run the command

		docker-compose down


## License

These Notebooks are available under the BSD 3-Clause License.

