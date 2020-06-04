#!/bin/sh
docker build -t onem2m-notebooks .
docker tag onem2m-notebooks ankraft/onem2m-notebooks
docker push ankraft/onem2m-notebooks
