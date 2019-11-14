FROM continuumio/miniconda3:4.7.12-alpine

COPY . $HOME/anaconda/
WORKDIR $HOME/anaconda/

RUN export PATH=$PATH:/opt/conda/bin/ && pip install .
WORKDIR $HOME/anaconda/workspace/

