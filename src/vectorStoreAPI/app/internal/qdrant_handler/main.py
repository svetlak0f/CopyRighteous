from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from tqdm import tqdm
import uuid
import random
from qdrant_client.models import PointStruct, Filter, Record, ScoredPoint
from qdrant_client import models
from uuid import UUID
from typing import Optional

from qdrant_client.http.exceptions import UnexpectedResponse
from grpc._channel import _InactiveRpcError
import logging



class VectorHandler:
    
    def __init__(self, 
                 database_address="http://localhost", 
                 vector_length=1000,
                 collection_name="embeddings_video"):
        
        self.client = QdrantClient(url=database_address, timeout=20, grpc_port=6334, prefer_grpc=True)
        self.collection_name = collection_name

        try:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=vector_length, distance=Distance.COSINE),
            )
            logging.info(f"{collection_name} has succesfully created")
        except (UnexpectedResponse, _InactiveRpcError):
            logging.info(f"Qdrant {collection_name} collection already exists, skipping")

    @staticmethod
    def divide_chunks(l, n=64): 
        for i in range(0, len(l), n):  
            yield l[i:i + n] 


    def save_vectors(self, vectors: list[list[float]], video_id: str):
        def generate_payload(video_id: str, vectors_count: int):
            return [{"video_id": video_id, "frame": x} for x in range(vectors_count)]
        
        self.client.upload_collection(
            collection_name=self.collection_name,
            vectors=vectors,
            payload=generate_payload(video_id=video_id, vectors_count=len(vectors)),
            ids=None,  # Vector ids will be assigned automatically
            batch_size=256,  
            wait=True
        )
    
    def query_vectors_batch(self, vectors: list[list[float]], chunk_size=16, search_filter: Optional[Filter] = None) -> list[ScoredPoint]:
        search_queries = list(map(lambda x: models.SearchRequest(vector=x, filter=search_filter, limit=1, with_payload=True), vectors))
        search_chunks = list(self.divide_chunks(search_queries, chunk_size))
        results = list()
        for chunk in tqdm(search_chunks):
            data = self.client.search_batch(collection_name=self.collection_name, requests=chunk)
            data = list(map(lambda x: x[0], data))
            results.extend(data)
        return results

        
    def delete_vectors_by_video_id(self, video_id: str):
        self.client.delete(
                collection_name=self.collection_name,
                points_selector=models.FilterSelector(
                    filter=models.Filter(
                        must=[
                            models.FieldCondition(
                                key="video_id",
                                match=models.MatchValue(value=video_id),
                            ),
                        ],
                    )
                )
            )


    def retrieve_vectors_by_video_id(self, video_id: str, request_batch_size: int = 256) -> list[Record]:
        target_embeddings = list()
        offset = None
        while True:
            result, offset = self.client.scroll(
                        collection_name=self.collection_name,
                        limit=request_batch_size,
                        scroll_filter=models.Filter(
                            must=[
                                models.FieldCondition(key="video_id", match=models.MatchValue(value=video_id)),
                            ]
                        ),
                        offset=offset,
                        with_vectors=True
                    )
            
            target_embeddings.extend(result)

            if not offset:
                break

        if target_embeddings:
            target_embeddings = list(sorted(target_embeddings, key=lambda x: x.payload["frame"]))
        return target_embeddings
        

    def search_nearest_by_video_id(self, video_id: str) -> list[ScoredPoint]:
        video_embeddings = self.retrieve_vectors_by_video_id(video_id)
        bare_embeddings = list(map(lambda x: x.vector, video_embeddings))
        search_filter = models.Filter(
            must_not=[
                models.FieldCondition(key="video_id", match=models.MatchValue(value=video_id)),
            ]
        )

        search_result = self.query_vectors_batch(bare_embeddings, chunk_size=16, search_filter=search_filter)
        return search_result



        



        

            
