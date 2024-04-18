FROM python:3.11

WORKDIR /app

COPY req.txt .

RUN pip install -r req.txt

COPY . ./

RUN addgroup --gid 10014 choreo && \
    adduser --disabled-password --no-create-home --uid 10014 --ingroup choreo choreouser

RUN mkdir -p /app/models && chmod -R 777 /app/models

VOLUME /app/models

USER 10014
EXPOSE 5000

CMD [ "python", "app.py"]


 