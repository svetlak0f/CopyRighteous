from cassandra.cluster import Cluster   
import uuid
import random
from tqdm import tqdm

cluster = Cluster(['127.0.0.1'])
session = cluster.connect()
embedding_length = 1000


session.execute("USE embeddings;")

embedding = [random.random() for _ in range(embedding_length)]

rows = session.execute(f"""
SELECT * FROM "embeddings"."video_embeddings" WHERE "video_id" = bdbf0e19-dbd2-4715-b983-329a48d89466;
""")

for row in rows:
    result = session.execute(f"""
            SELECT video_id 
                FROM embeddings.video_embeddings 
            ORDER BY embedding ANN OF {embedding}
            LIMIT 1;
        """)
    for data in result:
        print(data.video_id)