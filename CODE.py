from fastapi import FastAPI, UploadFile, File
import uvicorn
from chromadb import Client as ChromaInstance
from sentence_transformers import SentenceTransformer
from fastapi.responses import JSONResponse
from typing import List
import logging
import uuid

# Initialize FastAPI app
app = FastAPI()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load SentenceTransformer model (CPU)
try:
    embedding_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    logger.info("SentenceTransformer model loaded successfully.")
except Exception as model_error:
    logger.error(f"Model loading failed: {str(model_error)}")
    raise model_error

# Configure ChromaDB client for persistence
try:
    chroma_instance = ChromaInstance()
    document_storage = chroma_instance.get_or_create_collection(name="document_store")
    logger.info("ChromaDB client initialized; collection created.")
except Exception as db_init_error:
    logger.error(f"ChromaDB initialization error: {str(db_init_error)}")
    raise db_init_error

@app.post("/ingest/", response_class=JSONResponse)
async def add_files(file_list: List[UploadFile] = File(...)):
    """Endpoint to ingest files for later retrieval"""
    try:
        doc_items = [
            {"text": (file_content := await uploaded_file.read()).decode('utf-8'),
             "metadata": {'filename': uploaded_file.filename},
             "id": str(uuid.uuid4())}
            for uploaded_file in file_list
        ]
    except UnicodeDecodeError as decode_error:
        logger.error(f"File decoding error: {str(decode_error)}")
        return JSONResponse(content={"error": f"Cannot decode file content. Ensure files are UTF-8 encoded."}, status_code=400)
    except Exception as file_process_error:
        logger.error(f"Error processing files: {str(file_process_error)}")
        return JSONResponse(content={"error": "File processing error."}, status_code=500)

    try:
        # Generate embeddings for each document
        embeddings = [embedding_model.encode(doc["text"]).tolist() for doc in doc_items]
        logger.info("Document embeddings generated successfully.")

        # Add documents to ChromaDB
        document_storage.add(
            ids=[doc["id"] for doc in doc_items],
            documents=[doc["text"] for doc in doc_items],
            metadatas=[doc["metadata"] for doc in doc_items],
            embeddings=embeddings
        )
        logger.info("Documents successfully added to ChromaDB.")
        return JSONResponse(content={"status": "Documents ingested successfully"})

    except Exception as ingestion_error:
        logger.error(f"Ingestion error: {str(ingestion_error)}")
        return JSONResponse(content={"error": "Error during document ingestion."}, status_code=500)

@app.get("/query/", response_class=JSONResponse)
async def retrieve_documents(search_text: str):
    """Endpoint to retrieve documents based on a query"""
    try:
        # Generate embedding for the query
        search_vector = embedding_model.encode(search_text).tolist()
        logger.info("Query embedding generated successfully.")

        # Query ChromaDB
        query_results = document_storage.query(query_embeddings=[search_vector], n_results=5)
        formatted_results = [
            {
                "filename": metadata.get('filename', 'unknown'),
                "score": score,
                "text": document
            }
            for metadata, score, document in zip(
                query_results['metadatas'], query_results['distances'], query_results['documents']
            )
        ]
        logger.info("Query executed successfully.")
        return JSONResponse(content={"results": formatted_results})

    except Exception as query_error:
        logger.error(f"Query error: {str(query_error)}")
        return JSONResponse(content={"error": "Error during document retrieval."}, status_code=500)

@app.get("/database/", response_class=JSONResponse)
async def view_all_documents():
    """Endpoint to view all documents stored in the database"""
    try:
        all_documents = document_storage.get()
        document_response = [
            {
                "filename": meta.get('filename', 'unknown'),
                "text": document
            }
            for meta, document in zip(all_documents['metadatas'], all_documents['documents'])
        ]
        logger.info("Successfully retrieved all documents.")
        return JSONResponse(content={"documents": document_response})
    except Exception as retrieval_error:
        logger.error(f"Error retrieving documents: {str(retrieval_error)}")
        return JSONResponse(content={"error": "Error retrieving documents from database."}, status_code=500)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
