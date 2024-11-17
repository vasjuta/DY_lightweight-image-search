FROM alpine:3.14

RUN apk add --no-cache python3 py3-pip curl
RUN pip3 install flask

WORKDIR /app
COPY . .

ENV PYTHONUNBUFFERED=1

EXPOSE 8080
CMD ["python3", "app.py"]

