FROM python:3.9-slim

WORKDIR /app

COPY req.txt .

RUN pip install -r req.txt

COPY . ./

RUN addgroup --gid 10014 choreo && \
    adduser --disabled-password --no-create-home --uid 10014 --ingroup choreo choreouser



USER 10014

RUN ls


EXPOSE 5000

CMD [ "python", "app.py"]


 