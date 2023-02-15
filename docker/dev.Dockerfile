FROM python:3.8

RUN --mount=source=requirements.txt,target=/mnt/requirements.txt pip install --no-cache-dir --requirement /mnt/requirements.txt

RUN --mount=target=/mnt cp --recursive /mnt /tmp/heflow \
 && pip install --no-cache-dir /tmp/heflow \
 && rm --recursive /tmp/heflow
