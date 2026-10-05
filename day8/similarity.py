from sentence_transformers import util,SentenceTransformer
model=SentenceTransformer("all-MiniLM-L6-v2")
sentences=[
    "I love playing football",
    "I enjoy playing soccer",
    "I like eating pizza"
]
sentence_embedding=model.encode(sentences)
similarity1=util.cos_sim(sentence_embedding[0], sentence_embedding[1])
print("similarity b/w sentence 1 and 2:",similarity1.item())
similarity2=util.cos_sim(sentence_embedding[1],sentence_embedding[2])
print("similarity b/w sentence 2 and 3:",similarity1.item())
similarity2=util.cos_sim(sentence_embedding[0],sentence_embedding[2])
print("similarity b/w sentence 1 and 3:",similarity1.item())