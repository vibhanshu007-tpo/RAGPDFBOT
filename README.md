# 📄 RAG PDF Chatbot

An AI-powered PDF Question Answering application built using **Streamlit**, **LangChain**, **Groq LLM**, **HuggingFace Embeddings**, and **Chroma Vector Database**. The application allows users to upload PDF documents and ask questions in natural language, providing context-aware answers directly from the uploaded PDFs.

---

## 🚀 Features

- 📤 Upload one or multiple PDF files
- 🔍 Extract and process PDF content
- ✂️ Split documents into semantic chunks
- 🧠 Generate embeddings using HuggingFace models
- 🗄️ Store embeddings in Chroma Vector Database
- 💬 Ask questions in natural language
- 🤖 Get context-aware answers using Groq LLM
- 📑 Display source pages used to generate answers
- ⚡ Interactive and easy-to-use Streamlit interface

---

## 🛠️ Tech Stack

- **Python**
- **Streamlit**
- **LangChain**
- **Groq API**
- **HuggingFace Embeddings**
- **ChromaDB**
- **PyPDFLoader**

---

## 📂 Project Structure

```text
RAGPDFchat/
│
├── front.py                 # Streamlit frontend
├── chroma_db/               # Vector database storage
├── .env                     # Environment variables
├── .gitignore
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/vibhanshu007-tpo/RAGPDFBOT.git
cd RAGPDFBOT
```

### 2. Create Virtual Environment

#### Windows
```bash
python -m venv .venv
.venv\Scripts\activate
```

#### Linux/Mac
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
```

---

## ▶️ Run the Application

```bash
streamlit run front.py
```

The application will open in your browser at:

```text
http://localhost:8501
```

---

## 🧩 How It Works

1. User uploads PDF documents.
2. PDF text is extracted using PyPDFLoader.
3. Documents are split into smaller chunks.
4. Embeddings are generated using HuggingFace models.
5. Embeddings are stored in Chroma Vector Database.
6. Relevant chunks are retrieved based on the user's query.
7. Groq LLM generates answers using the retrieved context.

---

## 📸 Workflow

```text
PDF Upload
     ↓
Text Extraction
     ↓
Chunking
     ↓
Embeddings Generation
     ↓
Chroma Vector Store
     ↓
Retriever
     ↓
Groq LLM
     ↓
Answer + Source Pages
```

---

## 🎯 Future Enhancements

- Voice-based querying
- Chat history support
- Multiple document collections
- User authentication
- Cloud deployment on Render/AWS
- Citation highlighting inside PDFs

---

## 👨‍💻 Author

**Vibhanshu Hirapure**

- LinkedIn: https://www.linkedin.com/in/vibhanshu-hirapure
- GitHub: https://github.com/vibhanshu007-tpo
- Email: vibhanshuhirapure@gmail.com

---

⭐ If you found this project useful, please consider giving it a star on GitHub.
