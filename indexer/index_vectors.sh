#!/bin/sh

echo "Starting indexer..."

# Wait for Qdrant to be ready
sleep 5

echo "Creating collection..."
curl -X PUT 'http://qdrant:6333/collections/images' \
  -H 'Content-Type: application/json' \
  -d '{
    "vectors": {
      "size": 768,
      "distance": "Cosine"
    }
  }'

echo "Starting indexing process..."
for vector_file in /app/embeddings/*.npy; do
    if [ -f "$vector_file" ]; then
        filename=$(basename "$vector_file")
        # Read numpy file and convert to JSON array
        python3 -c "
import numpy as np
import json
import sys

vector = np.load('$vector_file')
vector = vector.flatten().tolist()
print(json.dumps({
    'points': [{
        'id': $id_counter,
        'vector': vector,
        'payload': {'filename': '${filename}'.replace('.npy', '')}
    }]
}))
" | curl -X PUT 'http://qdrant:6333/collections/images/points' \
         -H 'Content-Type: application/json' \
         -d @-

        id_counter=$((id_counter + 1))
        sleep 1
    fi
done

# Signal completion
touch /app/embeddings/.indexing_complete

echo "Indexing completed"