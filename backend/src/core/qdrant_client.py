from qdrant_client import QdrantClient, models
from typing import List, Dict, Any
import os

class QdrantStore:
    _instance = None
    _collection_name = "textbook_chunks"
    _vector_size = 384 # Dimension for all-MiniLM-L6-v2

    def __new__(cls, host: str = "localhost", port: int = 6333, api_key: str = None):
        if cls._instance is None:
            cls._instance = super(QdrantStore, cls).__new__(cls)
            if api_key:
                cls._instance.client = QdrantClient(host=host, port=port, api_key=api_key)
            else:
                cls._instance.client = QdrantClient(host=host, port=port)
            cls._instance._create_collection_if_not_exists()
        return cls._instance

    def _create_collection_if_not_exists(self):
        collections = self.client.get_collections().collections
        if not any(c.name == self._collection_name for c in collections):
            self.client.recreate_collection(
                collection_name=self._collection_name,
                vectors_config=models.VectorParams(size=self._vector_size, distance=models.Distance.COSINE),
            )
            print(f"Collection '{self._collection_name}' created.")

    def upsert_vectors(self, texts: List[str], embeddings: List[List[float]], metadatas: List[Dict[str, Any]]):
        """
        Upserts (inserts or updates) vectors and their payloads into Qdrant.
        """
        points = []
        for i, (text, embedding, metadata) in enumerate(zip(texts, embeddings, metadatas)):
            points.append(
                models.PointStruct(
                    id=i, # Simple sequential ID for now, can be UUIDs
                    vector=embedding,
                    payload={"text": text, **metadata}
                )
            )
        
        self.client.upsert(
            collection_name=self._collection_name,
            wait=True,
            points=points
        )
        print(f"Upserted {len(points)} points to collection '{self._collection_name}'.")

    def search_vectors(self, query_embedding: List[float], limit: int = 3) -> List[Dict[str, Any]]:
        """
        Searches for similar vectors in Qdrant.
        """
        search_result = self.client.search(
            collection_name=self._collection_name,
            query_vector=query_embedding,
            limit=limit,
            with_payload=True
        )
        return [{"text": hit.payload["text"], "score": hit.score} for hit in search_result]

if __name__ == "__main__":
    # Example Usage (requires a running Qdrant instance)
    # For a local Qdrant, you might run: docker run -p 6333:6333 qdrant/qdrant
    qdrant_host = os.getenv("QDRANT_HOST", "localhost")
    qdrant_port = int(os.getenv("QDRANT_PORT", 6333))
    qdrant_api_key = os.getenv("QDRANT_API_KEY")

    store = QdrantStore(host=qdrant_host, port=qdrant_port, api_key=qdrant_api_key)

    # You would typically get embeddings from your embedding_model.py
    # For demonstration, using dummy data
    dummy_texts = [
        "Physical AI involves robots that interact with the real world.",
        "Humanoid robots are designed to resemble the human body.",
        "ROS 2 is a flexible framework for writing robot software."
    ]
    dummy_embeddings = [
        [0.1] * QdrantStore._vector_size, # Replace with actual embeddings
        [0.2] * QdrantStore._vector_size,
        [0.3] * QdrantStore._vector_size
    ]
    dummy_metadatas = [
        {"chapter": "Introduction"},
        {"chapter": "Humanoid Robotics"},
        {"chapter": "ROS 2"}
    ]

    # store.upsert_vectors(dummy_texts, dummy_embeddings, dummy_metadatas)

    # query_embedding = [0.15] * QdrantStore._vector_size # Replace with actual query embedding
    # results = store.search_vectors(query_embedding)
    # print("\nSearch Results:")
    # for res in results:
    #     print(f"Score: {res['score']}, Text: {res['text']}")
