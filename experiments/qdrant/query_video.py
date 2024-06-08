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


target_video = "c427976287995fdb66b4848d022de1ed"

target_embeddings = list()
offset = None

while True:
    result, offset = client.scroll(
                collection_name="embeddings_video",
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
    



search_filter = models.Filter(
                    must_not=[
                        models.FieldCondition(key="video_id", match=models.MatchValue(value=target_video)),
                    ]
                )



search_queries = list(map(lambda x: models.SearchRequest(vector=x.vector, filter=search_filter,  with_payload=True, limit=1), target_embeddings))


search_chunks = list(divide_chunks(search_queries, 16))

results = list()

for chunk in tqdm(search_chunks[:10]):
    data = client.search_batch(collection_name="embeddings_video", requests=chunk)
    #flatten results
    data = list(map(lambda x: x[0], data))
    results.extend(data)


print(results[0])




