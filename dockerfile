FROM python:3.9-slim

WORKDIR /app

COPY req.txt .

RUN pip install -r req.txt

COPY . ./

RUN addgroup -g 10016 choreo && \
    adduser  --disabled-password  --no-create-home --uid 10016 --ingroup choreo choreouser
USER 10016
EXPOSE 5000

CMD ["waitress-serve", "--port=5000", "app:app"]


