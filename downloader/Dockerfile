FROM alpine:3.14

RUN apk add --no-cache curl file

WORKDIR /app

COPY download.sh .
RUN chmod +x download.sh

CMD ["./download.sh"]