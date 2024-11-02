from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_chroma import Chroma
from langchain.chains import create_history_aware_retriever
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.text_splitter import RecursiveCharacterTextSplitter
from core.config import get_settings
from langchain_core.output_parsers import StrOutputParser

def initialize_rag_components():
    settings = get_settings()
    
    # Initialize components with explicit API key
    embeddings = OpenAIEmbeddings(openai_api_key=settings.OPENAI_API_KEY)
    llm = ChatOpenAI(
        model_name="gpt-3.5-turbo", 
        temperature=0,
        openai_api_key=settings.OPENAI_API_KEY
    )
    
    # Initialize vector store
    vector_store = Chroma(
        persist_directory=settings.CHROMA_DB_PATH,
        embedding_function=embeddings,
        collection_name="rag_collection"
    )
    
    # Initialize retriever with specific parameters
    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={
            "k": 3,
            "filter": None
        }
    )
    
    # Initialize text splitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    
    # Setup prompts for retriever
    contextualize_q_prompt = ChatPromptTemplate.from_messages([
        ("system", "Given a chat history and the latest user question, formulate a standalone question that captures the essential query."),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}")
    ])
    
    # Create history-aware retriever
    history_aware_retriever = create_history_aware_retriever(
        llm,
        retriever,
        contextualize_q_prompt
    )
    
    # Create QA prompt
    qa_prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a helpful assistant. Answer the question based on the provided context. 
        If you cannot find the answer in the context, say "I cannot find information about this in the provided context."
        
        Context: {context}"""),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
    ])
    
    # Create document chain with string output parser
    document_chain = (
        qa_prompt 
        | llm 
        | StrOutputParser()
    )
    
    return {
        "vector_store": vector_store,
        "text_splitter": text_splitter,
        "history_aware_retriever": history_aware_retriever,
        "document_chain": document_chain
    }