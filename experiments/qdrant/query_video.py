from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from tqdm import tqdm
import uuid
import random
from qdrant_client.models import PointStruct, Filter
from qdrant_client import models

def divide_chunks(l, n): 
      
    # looping till length l 
    for i in range(0, len(l), n):  
        yield l[i:i + n] 

client = QdrantClient(url="http://localhost:6333")


target_video = "fcc08cd5-f3d3-4675-9c70-13230498f72f"

target_embeddings = list()
offset = None

while True:
    result, offset = client.scroll(
                collection_name="embeddings",
                limit=256,
                scroll_filter=models.Filter(
                    must=[
                        models.FieldCondition(key="video_id", match=models.MatchValue(value=target_video)),
                    ]
                ),
                offset=offset,
                with_vectors=True
            )
    
    target_embeddings.extend(result)

    if not offset:
        break
    


print(len(target_embeddings))


search_filter = models.Filter(
                    must_not=[
                        models.FieldCondition(key="video_id", match=models.MatchValue(value=target_video)),
                    ]
                )



search_queries = list(map(lambda x: models.SearchRequest(vector=x.vector, filter=search_filter, limit=1), target_embeddings))


search_chunks = list(divide_chunks(search_queries, 64))

results = list()

for chunk in tqdm(search_chunks[:100]):
    data = client.search_batch(collection_name="embeddings", requests=chunk)
    results.extend(data)


print(results[:1000])




