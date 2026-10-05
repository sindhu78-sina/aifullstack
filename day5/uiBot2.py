```python
from sentence_transformers import SentenceTransformer
import chromadb
import ollama
import streamlit as st


# ==================================================
# EMBEDDING MODEL
# ==================================================

@st.cache_resource
def load_model():
    return SentenceTransformer("all-MiniLM-L6-v2")


model = load_model()


# ==================================================
# STREAMLIT UI
# ==================================================

st.title("Welcome To My UiBot!")


# ==================================================
# CHAT HISTORY
# ==================================================

if "messages" not in st.session_state:
    st.session_state.messages = []


# ==================================================
# SIDEBAR
# ==================================================

with st.sidebar:

    personality = {
        "kid": "give the answer like you are explaining to a 5yr old, give the answer in 2 lines only.",

        "professor": "you are an iit professor explain the topics in correct terminology, give the answer in 2 lines only.",
    }

    personality_name = st.selectbox(
        "Select the personality:",
        personality.keys()
    )


    # --------------------------------------------------
    # CLEAR CHAT
    # --------------------------------------------------

    if st.button("Clear Chat"):

        st.session_state.messages = []

        st.success("Chat cleared successfully...")


    # --------------------------------------------------
    # TOP K
    # --------------------------------------------------

    top_k = st.slider(
        "Select the no. of top results:",
        min_value=1,
        max_value=5,
        value=3
    )


    # --------------------------------------------------
    # FILE UPLOAD
    # --------------------------------------------------

    uploaded_file = st.file_uploader(
        "Upload a file"
    )

    if uploaded_file:

        text = uploaded_file.read().decode("utf-8")

        st.write("File uploaded successfully...")

        # Preview
        with st.expander("Preview"):

            st.text(text)


        # ==================================================
        # CHUNKING
        # ==================================================

        chunks = []

        chunk_size = 100
        chunk_overlap = 20

        step = chunk_size - chunk_overlap

        for i in range(0, len(text), step):

            chunk = text[i:i + chunk_size]

            chunks.append(chunk)


# ==================================================
# ORIGINAL RAG FILE
# ==================================================

file_name = "sample.txt"

with open(file_name, "r") as file:

    text = file.read()


# ==================================================
# CHUNKING
# ==================================================

chunks = []

chunk_size = 100
chunk_overlap = 20

step = chunk_size - chunk_overlap


for i in range(0, len(text), step):

    chunk = text[i:i + chunk_size]

    chunks.append(chunk)


# ==================================================
# EMBEDDING
# ==================================================

embeddings = model.encode(chunks)


# ==================================================
# CHROMADB
# ==================================================

client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = client.get_or_create_collection(
    name="My_Documents"
)


# ==================================================
# IDS
# ==================================================

ids = []

for i in range(len(chunks)):

    ids.append(
        f"{file_name}_{i}"
    )


# ==================================================
# ADD DATA TO CHROMADB
# ==================================================

collection.add(

    ids=ids,

    documents=chunks,

    embeddings=embeddings.tolist()
)


# ==================================================
# CHAT HISTORY DISPLAY
# ==================================================

for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):

        st.write(msg["content"])


# ==================================================
# UI BOT CHAT INPUT
# ==================================================

question = st.chat_input(
    "Send a chat:"
)


if question:

    # --------------------------------------------------
    # SHOW USER QUESTION
    # --------------------------------------------------

    with st.chat_message("user"):

        st.write("You:", question)


    # --------------------------------------------------
    # SAVE USER MESSAGE
    # --------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )


    # ==================================================
    # RAG QUERY PHASE
    # ==================================================

    with st.spinner("Thinking...."):

        # Query embedding

        q_embedding = model.encode(question)


        # Retrieve relevant chunks

        results = collection.query(

            qu
```
