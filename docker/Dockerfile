FROM python:3.8

ENV PYENV_ROOT=/usr/local/pyenv
ENV PATH=$PYENV_ROOT/bin:$PATH
RUN curl -sS https://pyenv.run | sh

RUN --mount=source=dist,target=/mnt pip install --no-cache-dir /mnt/heflow-*.whl
