FROM python:3

RUN apt-get update && apt-get -y update

RUN pip3 install jupyter
RUN pip3 install jupyterlab
RUN pip3 install cbor2
RUN pip3 install flask
RUN pip3 install InquirerPy
RUN pip3 install isodate
RUN pip3 install paho-mqtt
RUN pip3 install requests
RUN pip3 install rich
RUN pip3 install tinydb


RUN mkdir notebooks
RUN mkdir notebooks/src
RUN mkdir notebooks/images
RUN mkdir notebooks/tools

COPY *.ipynb notebooks/
COPY src/*.py notebooks/src
COPY images/ notebooks/images/
COPY tools/ notebooks/tools/	


WORKDIR notebooks/

CMD ["jupyter", "lab", "--port=8888", "--ip=0.0.0.0", "--allow-root", "--NotebookApp.token=''", "--notebook-dir='.'", "__START__.ipynb"]
