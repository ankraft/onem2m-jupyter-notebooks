FROM python:3

RUN apt-get update && apt-get -y update

RUN pip3 install jupyter
RUN pip3 install requests

RUN mkdir notebooks
COPY *.ipynb notebooks/
COPY *.py notebooks/
WORKDIR notebooks/

CMD ["jupyter", "notebook", "--port=8888", "--ip=0.0.0.0", "--allow-root", "--NotebookApp.token=''", "--NotebookApp.password=''"]
