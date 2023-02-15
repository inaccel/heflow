FROM python:3.8

ENV PYENV_ROOT=/usr/local/pyenv
ENV PATH=$PYENV_ROOT/bin:$PATH
RUN curl -sS https://pyenv.run | sh

ARG VERSION
RUN pip install --no-cache-dir heflow==$VERSION
