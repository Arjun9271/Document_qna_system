import os
import time
import streamlit as st
from langchain_groq import ChatGroq
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
import tempfile

# Load environment variables
load_dotenv()

groq_api_key = os.getenv('GROQ_API_KEY')
google_api_key = os.getenv('GOOGLE_API_KEY')

if not groq_api_key or not google_api_key:
    raise ValueError("GROQ_API_KEY or GOOGLE_API_KEY not found in environment variables")

# Set page config
st.set_page_config(page_title="Document Q&A System", page_icon="📚", layout="wide")

# Custom CSS
st.markdown("""
<style>
    .main {
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .stButton>button {
        width: 100%;
    }
    .stTextInput>div>div>input {
        border-radius: 5px;
    }
    .stProgress>div>div>div {
        background-color: #4CAF50;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://images.unsplash.com/photo-1507842217343-583bb7270b66?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2790&q=80", use_column_width=True)
    st.title("Document Q&A")
    st.markdown("---")
    st.markdown("Upload your PDFs and ask questions about them!")

# Main content
st.title('📚 Document Q&A System')

# Initialize LLM
@st.cache_resource
def get_llm():
    return ChatGroq(groq_api_key=groq_api_key, model_name='Llama3-8b-8192')

llm = get_llm()

# Q/A prompt
prompt = """
You are an AI assistant specialized in analyzing and answering questions about PDF documents. Your task is to provide accurate, concise, and relevant answers based on the information contained in the provided context. Please adhere to the following guidelines:

1. Answer Precision:
   - Provide a direct and precise answer to the user's question.
   - If the exact answer is not in the context, provide the most relevant information available.
   - Clearly state if the question cannot be answered based on the given context.

2. Context Utilization:
   - Use only the information provided in the context to formulate your answer.
   - Do not introduce external knowledge or make assumptions beyond the given context.

3. Citation and Evidence:
   - Support your answer with relevant quotes or paraphrases from the context.
   - Cite the specific part of the document where the information is found, if available (e.g., "According to page 5 of the document...").

4. Handling Ambiguity:
   - If the question is ambiguous, briefly mention the possible interpretations and answer based on the most likely one.
   - If multiple relevant pieces of information are found, summarize them concisely.

5. Structured Response:
   - Begin with a direct answer to the question.
   - Follow with supporting evidence or explanation from the context.
   - End with a brief summary or conclusion.

6. Metadata Awareness:
   - If the context includes metadata about the documents (e.g., titles, authors, dates), use this information to provide more context to your answer when relevant.

7. Technical Language:
   - Match the technical level of your response to the complexity of the question and the document content.
   - Explain technical terms if they are crucial to understanding the answer.

8. Honesty and Limitations:
   - If the information in the context is insufficient or unclear, state this explicitly.
   - Suggest what additional information might be needed to provide a complete answer.

9. Objectivity:
   - Present information factually without inserting personal opinions or biases.
   - If asked for an opinion, clearly state that it would be an interpretation based solely on the given information.

10. Conciseness:
    - Provide answers that are as brief as possible while still being complete and accurate.
    - Use bullet points or numbered lists for clarity when appropriate.

Context: {context}
Question: {input}

Response:
"""

@st.cache_resource
def get_embeddings():
    return GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=google_api_key)

def process_pdf(uploaded_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        tmp_file_path = tmp_file.name

    loader = PyPDFLoader(tmp_file_path)
    docs = loader.load()
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    final_documents = text_splitter.split_documents(docs)
    
    os.unlink(tmp_file_path)
    
    return final_documents

def create_vector_store(documents):
    embeddings = get_embeddings()
    texts = [doc.page_content for doc in documents]
    metadatas = [doc.metadata for doc in documents]
    
    text_embeddings = embeddings.embed_documents(texts)
    
    return FAISS.from_embeddings(
        text_embeddings=list(zip(texts, text_embeddings)),
        embedding=embeddings,
        metadatas=metadatas
    )

# Create two columns
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Ask a Question")
    prompt1 = st.text_input('What do you want to ask about the documents?', key="user_question")
    
    if st.button('Submit Question', key="submit_question"):
        if 'vectors' not in st.session_state:
            st.warning("Please upload a PDF and create the Vector Store first.")
        elif not prompt1:
            st.warning("Please enter a question.")
        else:
            with st.spinner("Searching for an answer..."):
                chat_prompt = ChatPromptTemplate.from_template(prompt)
                document_chain = create_stuff_documents_chain(llm, chat_prompt)
                retriever = st.session_state.vectors.as_retriever()
                retrieval_chain = create_retrieval_chain(retriever, document_chain)
                
                start = time.process_time()
                
                response = retrieval_chain.invoke({'input': prompt1})
                
                end = time.process_time()
                
                st.markdown("### Answer")
                st.write(response['answer'])
                
                st.info(f"Processing time: {end - start:.2f} seconds")

with col2:
    st.subheader("Upload PDF")
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    
    if uploaded_file is not None:
        if st.button('Process PDF and Create Vector Store', key="create_vector_store"):
            with st.spinner("Processing PDF and creating Vector Store..."):
                st.info("This might take a few moments. Feel free to scroll through your reels 📱 in the meantime!")
                documents = process_pdf(uploaded_file)
                st.session_state.vectors = create_vector_store(documents)
                st.success("Vector Store created successfully!")

# Display system status
st.sidebar.markdown("---")
st.sidebar.subheader("System Status")
if 'vectors' in st.session_state:
    st.sidebar.success("Vector Store: Ready")
else:
    st.sidebar.warning("Vector Store: Not created")

# Footer
st.markdown("---")
st.markdown("Built with ❤️ using Streamlit and LangChain")
