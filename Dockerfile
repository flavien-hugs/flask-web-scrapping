FROM python:3.10

WORKDIR /yimba

COPY ./env/prod.txt /yimba/env/

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    VIRTUAL_ENV=/venv \
    PATH=/venv/bin:$PATH

RUN python -m venv $VIRTUAL_ENV && \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r /yimba/env/prod.txt

EXPOSE 5000

COPY . /yimba

COPY ./entrypoint.sh /yimba
RUN chmod +x /yimba/entrypoint.sh

ENTRYPOINT ["/yimba/entrypoint.sh"]
