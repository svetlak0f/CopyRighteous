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


cursor.execute("""
WITH video_frames AS (
    SELECT frame, embedding
    FROM video_embeddings
    WHERE video_id = '9beed624-3fb8-45ae-8714-89aada1567f1'  -- Replace with your specific video_id
)
-- Main query to find the closest embedding for each frame
SELECT 
    vf.frame AS frame_of_interest,
    ve.video_id AS nearest_video_id,
    ve.frame AS nearest_frame,
    ve.embedding,
    ve.embedding <=> vf.embedding AS distance
FROM video_frames vf
JOIN LATERAL (
    SELECT video_id, frame, embedding
    FROM video_embeddings
    WHERE video_id != '9beed624-3fb8-45ae-8714-89aada1567f1'  -- Exclude the initial video_id
    ORDER BY vf.embedding <=> embedding  -- Order by similarity (distance) using the PGVector operator
    LIMIT 1  -- Get the closest embedding
) ve ON true
ORDER BY vf.frame;
""")

records = cursor.fetchall()

for row in records:
    print("Id = ", row[0], )
    print("Model = ", row[1])
    print("Price  = ", row[2], "\n")

