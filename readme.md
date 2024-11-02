# Intelligent Document Chat Assistant

A modern RAG (Retrieval Augmented Generation) powered chat system that enables intelligent conversations with PDF documents. Upload your PDFs and ask questions naturally to get accurate, context-aware responses.


## 🌟 Features

- **PDF Document Processing**
  - Multiple PDF upload support
  - Automatic text extraction and processing
  - Efficient document chunking and storage
  - Real-time upload status

- **Intelligent Chat Interface**
  - Natural language question answering
  - Context-aware responses
  - Chat history maintenance
  - Modern ChatGPT-like interface

- **RAG Implementation**
  - Advanced document retrieval
  - Semantic search capabilities
  - Context-aware response generation
  - Integration with OpenAI's GPT models

## 🛠️ Tech Stack

- **Frontend**
  - HTML5/CSS3
  - Vanilla JavaScript
  - Modern Web APIs

- **Backend**
  - FastAPI
  - Python 3.8+
  - LangChain
  - ChromaDB

- **AI/ML**
  - OpenAI GPT-3.5
  - Document Embeddings
  - Vector Search

## 📋 Prerequisites

Before you begin, ensure you have the following installed:
- Python 3.8 or higher
- pip (Python package manager)
- Git
- Web browser (Chrome/Firefox recommended)

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/document-chat-assistant.git
cd document-chat-assistant
```

### 2. Set Up Python Virtual Environment
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the project root:
```env
OPENAI_API_KEY=your_openai_api_key_here
CHROMA_DB_PATH=./chroma_db
```

### 5. Start the Backend Server
```bash
uvicorn main:app --reload
```

### 6. Launch the Frontend
Open `index.html` in your web browser:
```bash
# Using Python's built-in server
python -m http.server 8080
```
Then visit `http://localhost:8080` in your browser.

## 📁 Project Structure

```
document-chat-assistant/
├── backend/
│   ├── api/
│   │   └── v1/
│   │       ├── chat.py
│   │       └── document.py
│   ├── core/
│   │   └── config.py
│   ├── models/
│   │   └── schemas.py
│   ├── services/
│   │   ├── chat.py
│   │   ├── document.py
│   │   └── rag.py
│   └── main.py
├── frontend/
│   ├── index.html
│   ├── styles.css
│   └── script.js
├── requirements.txt
└── .env
```

## 💻 Usage

### 1. Upload Documents
1. Click "Upload New File" button
2. Select one or multiple PDF files
3. Wait for upload confirmation
4. Files will appear in the sidebar

### 2. Chat Interface
1. Type your question in the input field
2. Press Enter or click Send
3. View the AI-generated response
4. Continue the conversation naturally

## 🔧 API Endpoints

### Documents
```
POST /api/v1/documents/upload
- Upload PDF documents
- Multipart form data
- Returns processing status
```

### Chat
```
POST /api/v1/chat/ask
- Send questions
- JSON payload with question and chat history
- Returns AI-generated response
```

## ⚙️ Configuration Options

### Backend Configuration
```python
# core/config.py
PROJECT_NAME: str = "RAG Chatbot API"
VERSION: str = "1.0.0"
API_V1_STR: str = "/api/v1"
CHROMA_DB_PATH: str = "./chroma_db"
```

### Document Processing Settings
```python
# services/document.py
max_size_mb: int = 10  # Maximum file size
chunk_size: int = 1000  # Text chunking size
chunk_overlap: int = 200  # Chunk overlap size
```

## 🔍 Troubleshooting

### Common Issues

1. **OpenAI API Key Error**
```bash
# Make sure your API key is set in .env
OPENAI_API_KEY=your_actual_api_key
```

2. **File Upload Issues**
- Check file size limit (10MB default)
- Ensure PDF format
- Verify file permissions

3. **Backend Connection**
- Confirm backend is running
- Check console for CORS errors
- Verify API endpoint URLs
