# 📚 Document Q&A System

This is a Streamlit-based application that allows users to upload PDF documents and ask questions about them. The system uses the `ChatGroq` model from LangChain and Google Generative AI Embeddings to provide accurate and concise answers based on the uploaded documents.

## ✨ Features

- 📄 Upload PDF documents and convert them into text.
- 🗂️ Create a vector store from the text content of the PDFs.
- ❓ Ask questions about the uploaded documents and receive accurate answers.
- 🖥️ Interactive UI with Streamlit.

## 🚀 Getting Started

### 📋 Prerequisites

Ensure you have the following installed:

- 🐍 Python 3.8 or later
- Streamlit
- LangChain
- FAISS
- PyPDF2
- dotenv

### 📦 Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/document-qa-system.git
    cd document-qa-system
    ```

2. Create and activate a virtual environment:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

4. Create a `.env` file in the root directory and add your API keys:
    ```env
    GROQ_API_KEY=your_groq_api_key
    GOOGLE_API_KEY=your_google_api_key
    ```

### ▶️ Running the Application

1. Run the Streamlit application:
    ```sh
    streamlit run app.py
    ```

2. Open your web browser and navigate to `http://localhost:8501` to view the application.

### 💡 Usage

1. **Upload PDF:** Use the sidebar to upload your PDF document.
2. **Create Vector Store:** After uploading, click the button to process the PDF and create the vector store.
3. **Ask Questions:** Enter your question in the provided input field and submit it to get an answer based on the uploaded document.

## 🛠️ Customization

- **🎨 Custom CSS:** You can modify the custom CSS in the `app.py` file to change the appearance of the application.
- **📜 Prompt Template:** The prompt template used for generating answers can be adjusted in the `app.py` file to better suit your needs.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Streamlit](https://streamlit.io/)
- [LangChain](https://www.langchain.com/)
- [FAISS](https://github.com/facebookresearch/faiss)
- [PyPDF2](https://pypdf2.readthedocs.io/)

Built with ❤️ using Streamlit and LangChain.
