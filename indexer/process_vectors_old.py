import os
import numpy as np
import json
import requests
import time


def load_and_index_vectors():
    embeddings_dir = '/app/embeddings'
    id_counter = 1

    for vector_file in sorted(os.listdir(embeddings_dir)):
        if vector_file.endswith('.npy'):
            try:
                print(f"Processing {vector_file}")
                # Load the numpy array
                vector_path = os.path.join(embeddings_dir, vector_file)
                vector = np.load(vector_path)

                # Prepare the payload
                payload = {
                    "points": [{
                        "id": id_counter,
                        "vector": vector.flatten().tolist(),
                        "payload": {
                            "filename": vector_file.replace('.npy', '')
                        }
                    }]
                }

                # Send to Qdrant
                response = requests.put(
                    'http://qdrant:6333/collections/images/points',
                    headers={'Content-Type': 'application/json'},
                    data=json.dumps(payload)
                )

                if response.status_code == 200:
                    print(f"Successfully indexed vector {id_counter}")
                else:
                    print(f"Failed to index vector {id_counter}: {response.text}")

                id_counter += 1
                time.sleep(0.1)  # Small delay between requests

            except Exception as e:
                print(f"Error processing {vector_file}: {e}")

    print(f"Indexed {id_counter - 1} vectors")


if __name__ == "__main__":
    load_and_index_vectors()