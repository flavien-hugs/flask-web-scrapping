FROM python:alpine3.18

RUN apk --no-cache add postgresql-client

WORKDIR /web/app

COPY . /web/app
RUN chmod +x /web/app/entrypoint.sh

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    VIRTUAL_ENV=/venv \
    PATH=/venv/bin:$PATH

RUN python -m venv $VIRTUAL_ENV && \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r /web/app/env/base.txt

RUN chgrp -R 0 /web/app && \
    chmod -R g+rwX /web/app

ENTRYPOINT ["/web/app/entrypoint.sh"]
CMD ["python3", "runserver.py"]
