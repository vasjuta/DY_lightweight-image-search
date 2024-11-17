#!/bin/sh

mkdir -p embeddings

for image in /app/images/*.jpg; do
    if [ -f "$image" ]; then
        filename=$(basename "$image")
        # Create a simple feature vector using image properties
        identify -format "%[fx:w] %[fx:h] %[mean] %[standard-deviation]" "$image" > "embeddings/${filename}.txt"
        sleep 1
    fi
done
touch /app/embeddings/.embedding_complete