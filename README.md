# 📚 Enterprise AI Knowledge Assistant (RAG)

An AI-powered Enterprise Knowledge Assistant that enables users to **chat with multiple PDF documents** using **Retrieval-Augmented Generation (RAG)**. It retrieves the most relevant information from uploaded documents using **FAISS semantic search** and generates accurate, context-aware answers with **Google Gemini AI**.

---

## 🚀 Live Demo

🔗 Coming Soon (Deploy on Streamlit Cloud)

---

## 🧠 Features

* 📄 Chat with multiple PDF documents
* 🤖 AI-powered question answering using Google Gemini
* 🔍 Semantic document retrieval using FAISS
* 🧠 Sentence Transformer embeddings
* 📚 Context-aware Retrieval-Augmented Generation (RAG)
* 📑 Automatic PDF text extraction and chunking
* 📌 Source citation with page references
* 💬 ChatGPT-style conversational interface
* 💾 Save and load Knowledge Base
* 📊 Knowledge Base statistics dashboard
* 🌙 Modern enterprise dark-themed UI

---

## 🔍 RAG Pipeline

```
PDF Documents
      │
      ▼
Load PDF Files
      │
      ▼
Split into Text Chunks
      │
      ▼
Generate Embeddings
(Sentence Transformers)
      │
      ▼
Create FAISS Vector Database
      │
      ▼
Store Vector Index
      │
      ▼
User Question
      │
      ▼
Semantic Search
      │
      ▼
Retrieve Relevant Chunks
      │
      ▼
Google Gemini
      │
      ▼
AI Generated Answer
```

---

## 📄 Knowledge Base Features

* Upload multiple PDF documents
* Automatic document chunking
* Save Knowledge Base locally
* Reload existing Knowledge Base
* Fast semantic retrieval
* Multi-document search

---

## 💬 Chat Features

* ChatGPT-inspired interface
* Context-aware conversations
* Source document citations
* Page number references
* Conversation history
* Clear chat functionality

---

## 📊 Dashboard

Displays:

* 📄 Total Documents
* 📑 Total Chunks
* 🧠 Total Vector Embeddings
* ✅ Knowledge Base Status

---

## ⚙️ Tech Stack

### Frontend

* Streamlit
* HTML
* CSS

### AI & Machine Learning

* Google Gemini API
* Sentence Transformers
* FAISS

### Backend

* Python
* PyPDF
* NumPy

### Vector Database

* Facebook AI Similarity Search (FAISS)

---

## 🧠 AI Model

### Embedding Model

```
all-MiniLM-L6-v2
```

### Large Language Model

```
Google Gemini 2.0 Flash
```

*(Automatically falls back to other supported Gemini models when needed.)*

---

## 📂 Project Structure

```
Enterprise-RAG-Assistant
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── assets
│
├── styles
│   └── styles.css
│
├── uploads
│
├── vectorstore
│
└── utils
    ├── pipeline.py
    ├── pdf_loader.py
    ├── text_splitter.py
    ├── embedding_model.py
    ├── vector_database.py
    ├── llm.py
    └── helper.py
```

---

## ⚙️ How to Run Locally

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/Enterprise-RAG-Assistant.git

cd Enterprise-RAG-Assistant
```

---

### 2️⃣ Create a Virtual Environment

```bash
python -m venv .venv
```

Windows

```bash
.venv\Scripts\activate
```

Mac/Linux

```bash
source .venv/bin/activate
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Configure Environment Variables

Create a `.env` file in the project root.

```env
GEMINI_API_KEY=YOUR_GOOGLE_API_KEY
```

---

### 5️⃣ Run the Application

```bash
python -m streamlit run app.py
```

---

## 🔗 GitHub Repository

```
https://github.com/YOUR_USERNAME/Enterprise-RAG-Assistant
```

---

## 📄 Supported File Types

Currently Supported

* PDF Documents

Future Support

* DOCX
* TXT
* PPTX
* Excel Files

---

## 📌 Future Improvements

* 📄 PDF page preview
* 🎯 Highlight cited text
* ⚡ Streaming AI responses
* 🧠 Conversation memory
* 📥 Export chat as PDF
* 📥 Export chat as Markdown
* 📂 Multi-session chat history
* 🌐 Cloud vector database
* 🔐 User authentication
* ☁️ AWS deployment
* 📱 Mobile responsive UI
* 🌍 Multi-language support

---

## 👨‍💻 Author

**Goutham P S**

* GitHub: https://github.com/Goutham-ps
* portfolio: https://gouthamps.vercel.app/

---

## ⭐ If You Like This Project

If you found this project useful, please consider giving it a ⭐ on GitHub!

It really helps and motivates me to build more AI and Machine Learning projects.

---

## 🙌 Acknowledgements

* Google Gemini API
* Streamlit
* FAISS
* Sentence Transformers
* PyPDF
* Hugging Face
