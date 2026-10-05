from sentence_transformers import SentenceTransformer
import chromadb,ollama,streamlit as st

@st.cache_resource
def load_model():
    return SentenceTransformer("all-MiniLM-L6-v2")

model=load_model()
st.title("Welcome To My UiBot!")

if "messages" not in st.session_state:
    st.session_state.messages=[]

with st.sidebar:
    personality={
        "kid":"give the answer like you are explaining to a 5yr old,give the answer in 2 lines only.",
        "professor":"you are an iit professor explain the topics in correct terminology,give the answer in 2 lines only.",
    }
    selected_personality=st.selectbox("Select the personality:",personality.keys())
    top_k=st.slider("Select the no. of top results:",min_value=1,max_value=5,value=3)
    if st.button("Clear Chat"):
        st.session_state.messages=[]
        st.success("Chat cleared successfully...")
    uploaded_file=st.file_uploader("upload a file")
    if uploaded_file:
        text=uploaded_file.read().decode("utf-8")
        st.write("File uploaded successfully...")
        with st.expander("preview"):
            st.text(text)
        chunks=[]
        chunk_size=100
        chunk_overlap=20
        step=chunk_size-chunk_overlap
        for i in range(0,len(text),step):
            chunk=text[i:i+chunk_size]
            chunks.append(chunk)

file_name="sample.txt"
with open(file_name,"r") as file:
    text=file.read()

chunks=[]
chunk_size=100
chunk_overlap=20
step=chunk_size-chunk_overlap
for i in range(0,len(text),step):
    chunk=text[i:i+chunk_size]
    chunks.append(chunk)

embeddings=model.encode(chunks)
client=chromadb.PersistentClient(path="./chroma_db")
collection=client.get_or_create_collection(name="My_Documents")
ids=[]
for i in range(len(chunks)):
    ids.append(f"{file_name}_{i}")

collection.add(ids=ids,documents=chunks,embeddings=embeddings.tolist())

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

question=st.chat_input("Send a chat:")

if question:
    with st.chat_message("user"):
        st.write("You:",question)
    st.session_state.messages.append({"role":"user","content":question})

    with st.spinner("Thinking...."):
        q_embedding=model.encode(question)
        results=collection.query(query_embeddings=[q_embedding.tolist()],n_results=top_k)
        retrieved_chunks=results["documents"][0]
        retrieved_ids=results["ids"][0]
        context="\n".join(retrieved_chunks)

        prompt=f'''
{personality[selected_personality]}
Answer the question using the context given below only.
Question:{question}
Context:{context}
Answer:
'''

        response=ollama.chat(
            model="llama3.2:3b",
            messages=[{"role":"system","content":personality[selected_personality]},{"role":"user","content":prompt}]
        )

    answer=response["message"]["content"]
    st.session_state.messages.append({"role":"assistant","content":answer})

    with st.chat_message("assistant"):
        st.write("AI:",answer)
