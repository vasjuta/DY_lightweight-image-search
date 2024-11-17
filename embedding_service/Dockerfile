FROM alpine:3.14

RUN apk add --no-cache imagemagick

WORKDIR /app

COPY process_images.sh .
RUN chmod +x process_images.sh

CMD ["./process_images.sh"]