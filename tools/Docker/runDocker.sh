#!/bin/sh
DOCKERHUBID=ankraft

docker run -e COLUMNS="`tput cols`" -e LINES="`tput lines`" -p 8888:8888 --rm --name onem2m-notebooks $DOCKERHUBID/onem2m-notebooks
