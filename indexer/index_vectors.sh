#!/bin/sh

echo "Starting indexer..."

# Wait for Qdrant to be ready
sleep 5

echo "Creating collection..."
curl -X PUT 'http://qdrant:6333/collections/images' \
  -H 'Content-Type: application/json' \
  -d '{
    "vectors": {
      "size": 4,
      "distance": "Cosine"
    }
  }'

echo "Processing embeddings..."
id_counter=1

# Process each embedding file
for vector_file in /app/embeddings/*.txt; do
    if [ -f "$vector_file" ]; then
        echo "Processing: $vector_file"

        # Read space-separated values from the file
        read width height mean std < "$vector_file"

        # Create JSON payload for Qdrant
        payload="{
            \"points\": [{
                \"id\": $id_counter,
                \"vector\": [$width, $height, $mean, $std],
                \"payload\": {
                    \"filename\": \"$(basename "$vector_file")\"
                }
            }]
        }"

        # Send to Qdrant
        echo "Indexing vector $id_counter"
        curl -X PUT 'http://qdrant:6333/collections/images/points' \
            -H 'Content-Type: application/json' \
            -d "$payload"

        id_counter=$((id_counter + 1))
        sleep 1
    fi
done

echo "Indexing completed"

# Create completion marker with debug info
echo "Creating completion marker..."
touch /app/embeddings/.indexing_complete
ls -la /app/embeddings/
echo "Completion marker created"

# Verify final collection status
echo "Final collection status:"
curl 'http://qdrant:6333/collections/images'