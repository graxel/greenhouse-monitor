
from sentence_transformers import SentenceTransformer, util
sentences = ["I'm happy", "I'm full of happiness"]

model = SentenceTransformer("nomic-ai/nomic-embed-text-v1.5", trust_remote_code=True)

embedding_1= model.encode(sentences[0], convert_to_tensor=True)
embedding_2 = model.encode(sentences[1], convert_to_tensor=True)

print(util.pytorch_cos_sim(embedding_1, embedding_2))
print(embedding_1)
print(embedding_2)