# Docker
This section explains how to generate and run a Docker container for the notebooks.

## Building a Docker Container

There is already a [Dockerfile](Dockerfile) in the distribution to build a new Docker container. After starting your Docker instance, just run the command:

	docker build -t notebook .

## Running the Docker Container

To run the built container use the following command:

	docker run -e COLUMNS="`tput cols`" -e LINES="`tput lines`" -p 8888:8888 --rm --name notebook notebook

The container will still be running attached to your terminal. To detach it, add the *-d* option. 

The *--rm* option removes the notebook container from your Docker instance after termination. This is useful because it removes all output and changes you might have done to the notebooks during a session.

Please note that the notebooks might not launch in your browser automatically, but you can access the Notebooks via your browser at [http://localhost:8888/lab](http://localhost:8888/lab) . You need then to select and run the notebook *\_\_START\_\_.ipynb*.

If you prefer the "old" Notebook style you may run access the notebooks at [http://localhost:8888](http://localhost:8888) .



## Downloading & Running from DockerHub

You might also just download a pre-provisioned version of the notebooks from [https://hub.docker.com](https://hub.docker.com):

	docker run -p 8888:8888 --rm --name onem2m-notebooks ankraft/onem2m-notebooks

## Running a Complete Installation with Docker Compose
To run the the notebooks together with a pre-configured [ACME CSE](https://github.com/ankraft/ACME-oneM2M-CSE):

- In a terminal shell in the same directory as the [docker-compose.yml](docker-compose.yml) file run the command 

		docker-compose up -d

- Open the following URLs in a web browser
	- The notebooks: [http://localhost:8888](http://localhost:8888)
	- The CSE's web UI : [http://localhost:8080](http://localhost:8080)
- To shutdown the notebooks and the CSE,  run the command

		docker-compose down

