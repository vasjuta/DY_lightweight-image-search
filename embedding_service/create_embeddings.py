import os
import torch
from PIL import Image
from transformers import ViTFeatureExtractor, ViTModel
import numpy as np
import gc


def create_embeddings():
    print("Loading ViT model...")
    feature_extractor = ViTFeatureExtractor.from_pretrained('google/vit-base-patch16-224')
    model = ViTModel.from_pretrained('google/vit-base-patch16-224')
    torch.set_num_threads(1)

    images_dir = 'images'
    embeddings_dir = 'embeddings'
    os.makedirs(embeddings_dir, exist_ok=True)

    print("Starting image processing...")
    for image_file in os.listdir(images_dir):
        if image_file.endswith(('.jpg', '.jpeg', '.png')):
            try:
                image_path = os.path.join(images_dir, image_file)
                print(f"Processing {image_file}")

                # Validate image
                try:
                    image = Image.open(image_path)
                    if image.mode != 'RGB':
                        image = image.convert('RGB')
                except Exception as e:
                    print(f"Error loading image {image_file}: {e}")
                    continue

                # Create embedding
                with torch.no_grad():
                    inputs = feature_extractor(images=image, return_tensors="pt")
                    outputs = model(**inputs)
                    embedding = outputs.last_hidden_state[:, 0, :].numpy()

                # Save embedding
                embedding_path = os.path.join(embeddings_dir, f"{image_file}.npy")
                np.save(embedding_path, embedding)
                print(f"Saved embedding for {image_file}")

                # Clear memory
                del outputs, inputs, embedding
                gc.collect()
                torch.cuda.empty_cache() if torch.cuda.is_available() else None

            except Exception as e:
                print(f"Error processing {image_file}: {e}")

    # Signal completion
    with open(os.path.join(embeddings_dir, '.embedding_complete'), 'w') as f:
        f.write('done')


if __name__ == "__main__":
    create_embeddings()