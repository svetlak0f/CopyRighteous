import random
import psycopg2
from psycopg2.extras import execute_values
import uuid
from tqdm import tqdm
import os
from dotenv import load_dotenv
import psycopg2.extras

# call it in any place of your program
# before working with UUID objects in PostgreSQL
psycopg2.extras.register_uuid()

load_dotenv()

# PostgreSQL connection parameters
db_params = {
    'dbname': "vectordb",
    'user': "testuser",
    'password': "testpwd",
    'host': os.getenv('POSTGRES_HOST', '127.0.0.1'),
    'port': os.getenv('POSTGRES_PORT', '5432'),
}

connection = psycopg2.connect(**db_params)
cursor = connection.cursor()

# Create the embeddings table
cursor.execute("""
CREATE TABLE IF NOT EXISTS video_embeddings (
  video_id UUID,
  frame INT,
  embedding vector(1000),
  PRIMARY KEY (video_id, frame)
)
""")

# Create an index for the embeddings
cursor.execute("""
CREATE INDEX IF NOT EXISTS ann_index
  ON video_embeddings USING ivfflat (embedding);
""")

connection.commit()

def send_single_vector_to_store(video_id: uuid.UUID, frame: int, embedding: list[float], cursor):
    cursor.execute("""
        INSERT INTO video_embeddings (video_id, frame, embedding)
        VALUES (%s, %s, %s);
    """, (video_id, frame, embedding))

def send_single_vector_to_prepared(video_id: uuid.UUID, frame: int, embedding: list[float], cursor):
    cursor.execute(prepared_statement, (video_id, frame, embedding))

def generate_video_embeddings(num_tuples, embedding_length):
    video_id = uuid.uuid4()  # Generate a unique video_id
    tuples_list = []

    for frame in range(num_tuples):
        embedding = [random.random() for _ in range(embedding_length)]
        tuples_list.append((video_id, frame, embedding))
    
    return tuples_list

def generate_data_entries(num_videos, video_length, embedding_length):
    """Generate and insert random data entries."""
    
    global prepared_statement
    prepared_statement = """
        INSERT INTO video_embeddings (video_id, frame, embedding)
        VALUES (%s, %s, %s);
    """

    for _ in tqdm(range(num_videos), total=num_videos):
        frames = generate_video_embeddings(video_length, embedding_length)
        for frame in tqdm(frames):
            send_single_vector_to_prepared(*frame, cursor)
        connection.commit()

if __name__ == "__main__":
    # Parameters for data generation
    num_videos = 109
    video_length = 27000
    embedding_length = 1000

    # Generate and insert data
    generate_data_entries(num_videos, video_length, embedding_length)

    # Close the connection
    cursor.close()
    connection.close()

    # print(f"{num_videos} entries have been successfully inserted into the database.")