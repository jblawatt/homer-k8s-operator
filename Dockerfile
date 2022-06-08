FROM python:3.10-slim-bullseye

WORKDIR /project

COPY /src /project

RUN pip install -r requirements.txt

CMD ["kopf", "run", "operator.py", "--verbose"]

