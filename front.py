import os
import warnings
import logging
import tempfile
import hashlib
import streamlit as st

from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma

# from langchain_classic.chains import RetrievalQA
from langchain.chains import RetrievalQA
from langchain_core.prompts import ChatPromptTemplate

# Disable warnings and info logs
warnings.filterwarnings("ignore")
logging.getLogger("transformers").setLevel(logging.ERROR)


st.title('RAG CHATBOT!')
# Setup a session state variable to hold all the old messages
if 'messages' not in st.session_state:
    st.session_state.messages = []

if "current_pdf" not in st.session_state:
    st.session_state.current_pdf = None



if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None



# Display all the historical messages
for message in st.session_state.messages:
    st.chat_message(message['role']).markdown(message['content'])

# Phase 3 (Pre-requisite)
# @st.cache_resource
def get_vectorstore(pdf_path):
    # pdf_name = "./Vibhanshu_Resume.pdf"

    loader = PyPDFLoader(pdf_path)
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100
    )

    docs = splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectorstore = Chroma.from_documents(
        documents=docs,
        embedding=embeddings,
        # persist_directory="./chroma_db"
    )

    return vectorstore


uploaded_file = st.file_uploader(
    "Upload your PDF",
    type="pdf"
)




if uploaded_file is not None:
    st.success(f"{uploaded_file.name} uploaded successfully!")


if "current_pdf" not in st.session_state:
    st.session_state.current_pdf = None




if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None

if uploaded_file is not None:

    file_bytes = uploaded_file.getvalue()
    file_hash = hashlib.md5(file_bytes).hexdigest()

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".pdf"
    ) as tmp_file:

        tmp_file.write(file_bytes)
        pdf_path = tmp_file.name

    if file_hash != st.session_state.current_pdf:
        st.session_state.current_pdf = file_hash
        st.session_state.messages = []
        st.session_state.vectorstore = get_vectorstore(pdf_path)


    
    # if uploaded_file.name != st.session_state.current_pdf:
    #     st.session_state.current_pdf = uploaded_file.name
    #     st.session_state.messages = []
    #     st.session_state.vectorstore = get_vectorstore(pdf_path)

prompt = st.chat_input('Pass your prompt here')

if prompt:
    if uploaded_file is None:
        st.warning("Please upload a PDF first.")
        st.stop()
    st.chat_message('user').markdown(prompt)
    # Store the user prompt in state
    st.session_state.messages.append({'role':'user', 'content': prompt})
    
    # Phase 2 
    groq_sys_prompt = ChatPromptTemplate.from_template("""You are very smart at everything, you always give the best, 
                                            the most accurate and most precise answers. Answer the following Question: {user_prompt}.
                                            Start the answer directly. No small talk please""")

    #model = "mixtral-8x7b-32768"
    # model="llama-3.1-8b-instant"
    model = "llama-3.3-70b-versatile"

    groq_chat = ChatGroq(
        groq_api_key=os.environ.get("GROQ_API_KEY"),
        model_name=model,
        temperature=0
    )

    # Phase 3
    try:
        # vectorstore = get_vectorstore(pdf_path)
        vectorstore = st.session_state.vectorstore
        if vectorstore is None:
            st.error("Failed to load document")
            st.stop()
      
        chain = RetrievalQA.from_chain_type(
            llm=groq_chat,
            chain_type='stuff',
            retriever=vectorstore.as_retriever(search_kwargs={'k': 3}),
            return_source_documents=True)
       
        result = chain.invoke({"query": prompt})
        response = result["result"]
        sources =result["source_documents"]
        
        st.chat_message('assistant').markdown(response)
        
        pages = sorted(
            set(
                doc.metadata.get("page", 0) + 1
                for doc in sources
            )
        )
        st.info(
    "Sources: " +
    ", ".join(f"Page {p}" for p in pages)
)
        
        
        st.session_state.messages.append(
            {'role':'assistant', 'content':response})
    except Exception as e:
        st.error(f"Error: {str(e)}")
