## 📚 Document Q&A System

This project is a Streamlit-based web application that allows users to upload PDF documents and ask questions about their content. The system uses advanced natural language processing techniques to provide accurate answers based on the document's content.

## ✨ Features

📄 PDF document upload and processing
❓ Question answering based on document content
🔍 Vector store creation for efficient document retrieval
🤖 Integration with Groq and Google AI for text processing and embeddings
🖥️ User-friendly interface with Streamlit

## 🛠️ Technologies Used

🐍 Python
🌊 Streamlit
🔗 LangChain
🚀 Groq
🧠 Google AI
📊 FAISS (Facebook AI Similarity Search)
📑 PyPDF2

## 📋 Prerequisites
Before you begin, ensure you have met the following requirements:

🐍 Python 3.7+
📦 Pip package manager

🔧 Installation

Clone the repository:
Copygit clone https://github.com/Arjun9271/doc_qna.git
cd document-qa-system

Install the required packages:
Copypip install -r requirements.txt

Set up environment variables:
Create a .env file in the project root and add the following:
CopyGROQ_API_KEY=your_groq_api_key
GOOGLE_API_KEY=your_google_api_key


## 🚀 Usage

Run the Streamlit app:
Copystreamlit run app.py

Open your web browser and navigate to the URL provided by Streamlit (usually http://localhost:8501).
Upload a PDF document using the file uploader in the sidebar.
Click on "Process PDF and Create Vector Store" to process the document and create the vector store.
Once the vector store is created, you can ask questions about the document content in the main panel.
Click "Submit Question" to get answers based on the document content.

## 📄 License
This project is licensed under the MIT License. See the LICENSE file for details.
📞 Contact
If you have any questions or feedback, please open an issue on the GitHub repository.
## 🙏 Acknowledgements

🌊 Streamlit
🔗 LangChain
🚀 Groq
🧠 Google AI
📊 FAISS
