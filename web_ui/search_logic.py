import torch
from transformers import ViTFeatureExtractor, ViTModel


class ImageSearch:
    def __init__(self):
        self.feature_extractor = ViTFeatureExtractor.from_pretrained('google/vit-base-patch16-224')
        self.model = ViTModel.from_pretrained('google/vit-base-patch16-224')
        torch.set_num_threads(1)

    def get_search_vector(self, query):
        """Convert text query to vector using ViT"""
        try:
            with torch.no_grad():
                # Use text as input for feature extraction
                inputs = self.feature_extractor(text=[query], return_tensors="pt")
                outputs = self.model(**inputs)
                vector = outputs.last_hidden_state[:, 0, :].numpy().flatten()
                return vector.tolist()
        except Exception as e:
            print(f"Error converting query to vector: {e}")
            # Return a default vector if conversion fails
            return [0.0] * 768  # ViT base model dimension