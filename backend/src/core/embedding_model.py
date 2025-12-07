from sentence_transformers import SentenceTransformer
from typing import List

class EmbeddingModel:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(EmbeddingModel, cls).__new__(cls)
            # Load the model once
            cls._instance.model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        return cls._instance

    def get_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generates embeddings for a list of texts.
        """
        embeddings = self.model.encode(texts, convert_to_tensor=False)
        return embeddings.tolist()

if __name__ == "__main__":
    # Example usage
    model = EmbeddingModel()
    test_texts = [
        "This is a test sentence.",
        "This is another test sentence to get embeddings for."
    ]
    embeddings = model.get_embeddings(test_texts)
    print(f"Generated {len(embeddings)} embeddings. Each has dimension {len(embeddings[0])}.")
