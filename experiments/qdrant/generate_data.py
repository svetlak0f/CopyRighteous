from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from tqdm import tqdm
import uuid
import random
from qdrant_client.models import PointStruct

client = QdrantClient(url="http://localhost:6333")

try:
    client.create_collection(
        collection_name="embeddings",
        vectors_config=VectorParams(size=1000, distance=Distance.COSINE),
    )
except:
    pass


def generate_video_embeddings(num_tuples, embedding_length):
    video_id = uuid.uuid4()  # Generate a unique video_id
    tuples_list = []

    for frame in range(num_tuples):
        embedding = [random.random() for _ in range(embedding_length)]
        tuples_list.append((video_id, frame, embedding))
    
    return tuples_list

def transform_tuple_to_points(video_id, frame, embedding):
    return embedding, {"video_id": video_id, "frame": frame},


def generate_data_entries(num_videos, video_length, embedding_length):
    """Generate and insert random data entries."""
    
    for _ in tqdm(range(num_videos), total=num_videos):
        frames = generate_video_embeddings(video_length, embedding_length)
        points = list(map(lambda x: transform_tuple_to_points(*x), frames))
        embeddings, payload = zip(*points)
       
        client.upload_collection(
            collection_name="embeddings",
            vectors=embeddings,
            payload=payload,
            ids=None,  # Vector ids will be assigned automatically
            batch_size=256,  # How many vectors will be uploaded in a single request?
            wait=True
        )
        # client.add()


        
if __name__ == "__main__":
    # Parameters for data generation
    num_videos = 109
    video_length = 27000
    embedding_length = 1000

    # Generate and insert data
    generate_data_entries(num_videos, video_length, embedding_length)