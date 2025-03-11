ARG IMAGETAG=python:3.13.2-alpine3.21
FROM ${IMAGETAG}

WORKDIR /tmp/can-i-charge

COPY pyproject.toml pyproject.toml
COPY src src

RUN pip install .

RUN adduser -S can-i-charge
USER can-i-charge

WORKDIR /

CMD [ "can-i-charge" ]
