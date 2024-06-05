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

embedding_length = 1000

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



embedding = [random.random() for _ in range(embedding_length)]


cursor.execute("""
SELECT
	embedding
FROM
	"video_embeddings"
WHERE
	video_id = '9beed624-3fb8-45ae-8714-89aada1567f1';
""")

records = cursor.fetchall()

for row in tqdm(records):
    # print(embedding)

    cursor.execute(f"""
              SELECT * FROM "video_embeddings" WHERE
	        video_id != '9beed624-3fb8-45ae-8714-89aada1567f1' ORDER BY embedding <-> '{row[0]}' LIMIT 1;
        """)
    vector = cursor.fetchall()
    for data in vector:
        # print(data[0], data[1])
        pass