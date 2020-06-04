#!/bin/sh
DOCKERHUBID=ankraft

cd ../..
docker build -t onem2m-notebooks -f tools/Docker/Dockerfile .
docker tag onem2m-notebooks $DOCKERHUBID/onem2m-notebooks
docker push $DOCKERHUBID/onem2m-notebooks
