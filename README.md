# RAG AI Model

A Retrieval-Augmented Generation (RAG) application built using Streamlit, PostgreSQL (Neon), PGVector, and Sentence Transformers. The application allows users to upload PDF documents, store vector embeddings in PostgreSQL, and retrieve relevant information based on user queries.

## Features

* Upload PDF documents
* Extract text from PDFs
* Split text into chunks
* Generate embeddings using Sentence Transformers
* Store embeddings in PostgreSQL with PGVector
* Perform semantic similarity search
* Interactive Streamlit user interface
* Cloud database support using Neon PostgreSQL

## Tech Stack

### Frontend

* Streamlit

### Backend

* Python

### Database

* PostgreSQL
* PGVector Extension
* Neon PostgreSQL

### AI & NLP

* Sentence Transformers (`all-MiniLM-L6-v2`)

### Libraries

* Streamlit
* PyPDF
* Psycopg2
* PGVector
* Sentence Transformers
* Python Dotenv
* OpenAI/OpenRouter API

## Project Structure

```text
RAG-AI-MODEL/
│
├── app.py
├── requirements.txt
├── .gitignore
├── .env
│
├── Data/
│   └── documents.pdf
│
└── venv/
```

## Installation

### Clone Repository

```bash
git clone https://github.com/your-username/rag-ai-model.git
cd rag-ai-model
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

Windows:

```bash
venv\Scripts\activate
```

Linux/Mac:

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

## Database Setup

Create PGVector Extension:

```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

Create Table:

```sql
CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    chunk_text TEXT,
    embedding VECTOR(384)
);
```

## Environment Variables

Create a `.env` file:

```env
DB_HOST=your_host
DB_NAME=neondb
DB_USER=your_user
DB_PASSWORD=your_password
DB_PORT=5432

OPENROUTER_API_KEY=your_api_key
```

## Run Application

```bash
streamlit run app.py
```

## Deployment

### GitHub

```bash
git add .
git commit -m "Initial Commit"
git push origin main
```

### Streamlit Community Cloud

1. Push project to GitHub.
2. Open Streamlit Community Cloud.
3. Connect GitHub repository.
4. Select `app.py`.
5. Add database credentials in Streamlit Secrets.
6. Deploy application.



## Author

Muthu Krishnan B

