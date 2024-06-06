import random
from datetime import datetime, timedelta
from cassandra.cqlengine import connection
from cassandra.cqlengine.management import sync_table
from cassandra.cqlengine.models import Model
from cassandra.cqlengine import columns
import uuid
from tqdm import tqdm
from cassandra.cluster import Cluster
import os
from uuid import UUID
import uuid
import random

from dotenv import load_dotenv
load_dotenv()




cluster = Cluster(['127.0.0.1'])
session = cluster.connect()

session.execute(
"""CREATE KEYSPACE IF NOT EXISTS embeddings
WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : '1' };
""")

session.execute("USE embeddings;")


session.execute(
"""
CREATE TABLE IF NOT EXISTS embeddings.video_embeddings (
  video_id uuid,
  frame int,
  embedding VECTOR <FLOAT, 1000>,
  PRIMARY KEY (video_id, frame)
)
WITH CLUSTERING ORDER BY (frame DESC);
"""
)

session.execute_async(
"""CREATE INDEX IF NOT EXISTS ann_index
  ON embeddings.video_embeddings(embedding) USING 'sai';"""
)


def send_single_vector_to_store(video_id: UUID, frame: int, embedding: list[float], session):
    session.execute(f"""
        INSERT INTO embeddings.video_embeddings (video_id, frame, embedding)
        VALUES (
            {video_id},
            {frame},
            {embedding}
        );
        """
    )


def send_single_vector_to_prepared(video_id: UUID, frame: int, embedding: list[float], request_statement):
    session.execute(request_statement, [video_id, frame, embedding])
    

def generate_video_embeddings(num_tuples, embedding_length):
    video_id = uuid.uuid4()  # Generate a unique video_id
    tuples_list = []

    for frame in range(num_tuples):
        embedding = [random.random() for _ in range(embedding_length)]
        tuples_list.append((video_id, frame, embedding))
    
    return tuples_list

def generate_data_entries(num_videos, video_length, embedding_length):
    """Generate and insert random data entries."""
    
    request_statement = session.prepare("""
        INSERT INTO embeddings.video_embeddings (video_id, frame, embedding)
        VALUES (
            ?,
            ?,
            ?
        );
        """)

    for _ in tqdm(range(num_videos), total=num_videos):
        frames = generate_video_embeddings(video_length, embedding_length)
        for frame in tqdm(frames):
            send_single_vector_to_prepared(*frame, request_statement)

if __name__ == "__main__":
    # Parameters for data generation
    num_videos = 109
    video_length = 27000
    embedding_length = 1000

    # Generate and insert data
    generate_data_entries(num_videos, video_length, embedding_length)

    # print(f"{num_videos} entries have been successfully inserted into the database.")