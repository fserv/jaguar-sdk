
from sentence_transformers import SentenceTransformer

sentences = ["样例数据-1", "样例数据-2"]
model = SentenceTransformer('BAAI/bge-large-zh')
embeddings_1 = model.encode(sentences, normalize_embeddings=True)
embeddings_2 = model.encode(sentences, normalize_embeddings=True)

similarity = embeddings_1 @ embeddings_2.T

print(similarity)
