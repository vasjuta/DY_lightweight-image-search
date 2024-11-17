FROM alpine:3.14

RUN apk add --no-cache curl jq

WORKDIR /app

COPY index_vectors.sh .
RUN chmod +x index_vectors.sh

CMD ["./index_vectors.sh"]