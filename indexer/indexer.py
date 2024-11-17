# indexer/index.py
import os
import numpy as np
from pathlib import Path
import logging
from qdrant_client import QdrantClient
from qdrant_client.http import models
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VectorIndexer:
    def __init__(self):
        self.embeddings_dir = Path('/app/embeddings')
        self.collection_name = 'images'
        self.connect_to_qdrant()
        self.setup_collection()

    def connect_to_qdrant(self):
        """Connect to Qdrant server"""
        retries = 5
        while retries > 0:
            try:
                self.client = QdrantClient(host='qdrant', port=6333)
                logger.info("Connected to Qdrant")
                return
            except Exception as e:
                retries -= 1
                logger.warning(f"Failed to connect to Qdrant: {e}")
                time.sleep(5)

        raise Exception("Could not connect to Qdrant")

    def setup_collection(self):
        """Create collection if it doesn't exist"""
        try:
            self.client.get_collection(self.collection_name)
        except:
            # Create new collection
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(
                    size=512,  # CLIP embedding size
                    distance=models.Distance.COSINE
                )
            )
            logger.info(f"Created collection: {self.collection_name}")

    def index_embeddings(self):
        """Index all embeddings from the embeddings directory"""
        embedding_files = list(self.embeddings_dir.glob('*.npy'))

        if not embedding_files:
            logger.info("No embeddings to index")
            return

        logger.info(f"Indexing {len(embedding_files)} embeddings")

        # Process in small batches to conserve memory
        batch_size = 50
        for i in range(0, len(embedding_files), batch_size):
            batch = embedding_files[i:i + batch_size]
            points = []

            for idx, file_path in enumerate(batch):
                try:
                    # Load embedding
                    embedding = np.load(file_path)

                    # Create point
                    points.append(models.PointStruct(
                        id=i + idx,
                        vector=embedding.tolist(),
                        payload={'image_name': file_path.stem}
                    ))

                except Exception as e:
                    logger.error(f"Error processing {file_path}: {e}")
                    continue

            # Upload batch
            if points:
                self.client.upsert(
                    collection_name=self.collection_name,
                    points=points
                )
                logger.info(f"Indexed batch: {i}-{i + len(points)}")


if __name__ == "__main__":
    indexer = VectorIndexer()
    indexer.index_embeddings()