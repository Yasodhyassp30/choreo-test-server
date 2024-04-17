FROM python:3.9-slim

WORKDIR /app

COPY req.txt .

RUN pip install -r req.txt

COPY . ./

EXPOSE 5000

CMD ["waitress-serve", "--port=5000", "app:app"]


