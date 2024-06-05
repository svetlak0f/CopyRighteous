from cassandra.cluster import Cluster
import uuid
import random

cluster = Cluster(['127.0.0.1'])
session = cluster.connect()
embedding_length = 1000


session.execute("USE embeddings;")

embedding = [random.random() for _ in range(embedding_length)]

rows = session.execute(f"""
SELECT video_id, frame FROM embeddings.video_embeddings
    ORDER BY embedding ANN OF {embedding}
    LIMIT 1;
""")

for row in rows:
    print(row.video_id, row.frame)