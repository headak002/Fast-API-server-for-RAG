# Fast-API-server-for-RAG

FastAPI Server for Retrieval-Augmented Generation (RAG)
This project provides an efficient FastAPI server designed for Retrieval-Augmented Generation (RAG), offering document ingestion, retrieval, and semantic search capabilities. The server leverages ChromaDB for seamless document storage and retrieval, along with sentence-transformers/all-MiniLM-L6-v2 for high-quality, CPU-optimized document embeddings. Its non-blocking API ensures fast and concurrent handling of requests, making it ideal for real-time applications.

Key Features
Document Ingestion & Search: Upload and search documents in multiple formats (PDF, DOC, DOCX, TXT) using ChromaDB.
Semantic Search: Uses the sentence-transformers/all-MiniLM-L6-v2 model for advanced, context-aware embeddings.
Non-blocking API: Powered by FastAPI, ensuring high performance and responsiveness for concurrent requests.
Technology Stack
FastAPI: High-performance framework for building APIs with asynchronous capabilities.
ChromaDB: A powerful vector database optimized for fast document retrieval and storage.
Sentence-Transformers: State-of-the-art models for generating document embeddings.
Uvicorn: ASGI server for deploying FastAPI apps, ensuring efficient handling of multiple connections.
Python: The programming language used for the entire project.
Langchain: A helpful library for handling document loading and processing tasks.
Libraries and Tools
FastAPI: Asynchronous API framework for building scalable web services.
Uvicorn: Lightweight ASGI server for serving FastAPI applications.
ChromaDB: Document storage and retrieval system built for embedding vectors.
Sentence-Transformers: Utilized for transforming documents into meaningful embeddings.
Langchain: Simplifies document loading, processing, and managing data flows.
Python Standard Libraries: Core utilities like uuid for unique identifiers and logging for tracking the application's activity.
Getting Started
Prerequisites
Python 3.8+
pip (for installing dependencies)
Installation Instructions
Clone the repository:

bash
Copy code
git clone https://github.com/headak002/Fast-API-server-for-RAG.git
cd fastapi-rag-server
Install required dependencies:

bash
Copy code
pip install -r requirements.txt
Run the FastAPI server:

bash
Copy code
uvicorn main:app --reload
The server will be available at http://127.0.0.1:8000.

API Endpoints
1. Upload Documents /ingest/ [POST]
Uploads documents to the database for later retrieval.

Request: Multipart form with file uploads.
Sample Files: sample1.txt, sample2.pdf
Response:
json
Copy code
{
  "status": "Documents uploaded successfully"
}
2. Search Documents /query/ [GET]
Searches through the stored documents for a specific query text.

Parameter: query_text (string) - The search text.
Sample URL: http://127.0.0.1:8000/query/?query_text=What%20is%20FastAPI
Response:
json
Copy code
{
  "results": [
    {
      "filename": "sample1.txt",
      "score": 0.7214,
      "text": "Title: Introduction to FastAPI\n\nFastAPI is a modern, high-performance web framework..."
    }
  ]
}
3. View All Documents /database/ [GET]
Fetches all stored documents along with their metadata and content.

Response:
json
Copy code
{
  "documents": [
    { "filename": "sample1.txt", "text": "Introduction to FastAPI..." },
    { "filename": "sample2.pdf", "text": "Sample PDF document content..." }
  ]
}
Running the Server
Start the server:

bash
Copy code
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
Access the API at http://localhost:8000.

Testing Endpoints: You can test the endpoints using API testing tools like Postman or Thunder Client.

Example Usage
Ingest Documents
To upload documents, send a POST request to /ingest/ with files in the request body.

URL: http://localhost:8000/ingest/
Method: POST with files in the form-data.
Query Documents
Send a GET request to /query/ with your search query.

URL: http://localhost:8000/query/?query_text=<your_query>
Contributing
We welcome contributions! Feel free to submit a pull request with your enhancements or bug fixes.

For any questions or support, please reach out via email at akshat002g@gmail.com or visit my GitHub profile: headak002.

License
This project is licensed under the MIT License.

Acknowledgments
FastAPI
ChromaDB
Sentence-Transformers
Langchain
