from FlagEmbedding import FlagModel

sentences = ["text data sample one", "text data sample two"]
model = FlagModel('BAAI/bge-large-en', query_instruction_for_retrieval="Generate index for this sentence: ")
embeddings_1 = model.encode(sentences)
embeddings_2 = model.encode(sentences)
similarity = embeddings_1 @ embeddings_2.T
print(embeddings_2)
print(similarity)

# for s2p(short query to long passage) retrieval task, please use encode_queries() which will automatically add the instruction to each query
# corpus in retrieval task can still use encode() or encode_corpus(), since they don't need instruction
queries = ['query_1', 'query_2']
passages = ["sample document 1", "sample document 2"]
q_embeddings = model.encode_queries(queries)
p_embeddings = model.encode(passages)
scores = q_embeddings @ p_embeddings.T
print(scores)

