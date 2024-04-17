FROM python:3.9-slim

RUN groupadd -g 10014 myuser && \
    useradd -r -u 10014 -g myuser myuser

WORKDIR /app

COPY req.txt .

RUN pip install -r req.txt

COPY . ./

EXPOSE 5000

CMD ["waitress-serve", "--port=5000", "app:app"]


