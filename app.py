import streamlit as st
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import psycopg2
from pgvector.psycopg2 import register_vector
from openai import OpenAI
from dotenv import load_dotenv
import os

def chunkText(text):
    chunks = []
    size = 500
    for i in range(0, len(text), size):
        chunks.append(text[i:i+size])
    return chunks

@st.cache_resource
def loadModel():
    return SentenceTransformer("all-MiniLM-l6-v2")

def createEmbedding(chunks):
    return model.encode(chunks)

def connectDB():
    load_dotenv()
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT"),
        sslmode="require"
    )
    register_vector(conn)
    return conn

def replaceDocument(chunks, vectors):
    con = connectDB()
    cur = con.cursor()

    try:
        # Remove old document data
        cur.execute("TRUNCATE TABLE documents RESTART IDENTITY")

        # Insert new document data
        for chunk, vector in zip(chunks, vectors):
            cur.execute(
                """
                INSERT INTO documents (chunk_text, embedding)
                VALUES (%s, %s)
                """,
                (chunk, vector)
            )
        con.commit()
    finally:
        cur.close()
        con.close()


def findRelatedVetor(questionVector):
    con = connectDB()
    cur = con.cursor()
    try:
        cur.execute(
        """
        SELECT chunk_text FROM documents
        ORDER BY embedding <=> %s
        LIMIT 3
        """, (questionVector,)
        )
        return cur.fetchall()

    finally:
        cur.close()
        con.close()

def initModel():
    load_dotenv()
    apiKey = os.getenv('API_KEY')
    client = OpenAI(api_key=apiKey, base_url='https://openrouter.ai/api/v1')
    return client

def generatePrompt(relatedChunks, question):
    prompt = f"""
    Answer the question only using the context if answer not available return "Answer not found!!!"

    Context:
    {relatedChunks}

    Question:
    {question}
    """
    return prompt


model = loadModel()
Client = initModel()

#Start of the program
#upload the file 

if "processed" not in st.session_state:
    st.session_state.processed = False

st.title('Retrieval Augmented Generation')
uploadedFile = st.file_uploader("Upload PDF", type='pdf')
if st.button('Upload'):
    #if file upload
    if uploadedFile is not None:
        try:
            reader = PdfReader(uploadedFile)
            text = ''
            for page in reader.pages:
                text += page.extract_text()
            #st.write(text)
            chunks = chunkText(text)
            vectors = createEmbedding(chunks)
            #st.write(vectors)
            try:
                replaceDocument(chunks, vectors)
                st.write('DB connected')
                
                st.session_state.processed = True
            except Exception as e:
                st.error("Error in connecting DB")
                st.error(e)
        #if not PDF throws an error
        except Exception as e:
            st.error('Upload the PDF File')
            st.error(e)
    else:
        st.error('Upload the File')


if st.session_state.processed:
    st.success("Document was scanned successfully!!!")
    question = st.text_input('Ask question')
    if st.button('Ask'):
        if question.strip():
            questionVector = createEmbedding(question)
            #st.write(questionVector)
            result = findRelatedVetor(questionVector)
            prompt = generatePrompt(result, question)
            try:
                response = (Client.chat.completions.create(model='openrouter/free',
                       messages =[
                            {
                                'role': 'user',
                                'content' : prompt
                            }
                        ]))
                st.write('AI Response:')
                st.success(response.choices[0].message.content)
            except Exception as e:
                st.error('Quota exceeding please try again later')
                st.error(e)
        else:
            st.error('Ask any question')