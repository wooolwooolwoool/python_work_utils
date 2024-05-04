FROM jupyter/base-notebook:x86_64-ubuntu-22.04

RUN pip install -U pip && \
    pip install panel pandas

WORKDIR /work
CMD panel serve app/*.py