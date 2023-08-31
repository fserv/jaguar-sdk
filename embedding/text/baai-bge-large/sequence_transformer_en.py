
from sentence_transformers import SentenceTransformer

sentences = ["This is sentence or paragraph one.", "This is sentence or paragraph two"]
model = SentenceTransformer('BAAI/bge-large-en')
embeddings_1 = model.encode(sentences, normalize_embeddings=True)
embeddings_2 = model.encode(sentences, normalize_embeddings=True)

similarity = embeddings_1 @ embeddings_2.T

print(similarity)
print(len(embeddings_2[1]))
