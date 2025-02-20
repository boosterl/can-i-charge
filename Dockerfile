FROM python:3.13.2-alpine3.21

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

RUN adduser -S can-i-charge
USER can-i-charge

CMD [ "can-i-charge" ]
