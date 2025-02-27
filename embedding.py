from langchain_community.embeddings import XinferenceEmbeddings
from langchain_community.document_loaders import WebBaseLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import bs4
from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
import os

xinference = XinferenceEmbeddings(server_url="http://0.0.0.0:9997", model_uid = "bge-base-zh-v1.5")
vectorstore = Chroma(collection_name="zytest", embedding_function=xinference)

def insert_web_path(path):
    loader = WebBaseLoader(
        web_paths=(path,),
    )
    data = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
    all_splits = text_splitter.split_documents(data)
    #print(all_splits)
    vectorstore.add_documents(documents=all_splits)

llm = ChatOpenAI(
    model = "ep-20250207110310-m52hl", 
    api_key = os.getenv("OPENAI_API_KEY"),
    base_url = "https://ark.cn-beijing.volces.com/api/v3",
    streaming = True,
)

def insert_file_path(path):
    loader = DirectoryLoader(
        path=(path,),
    )
    data = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
    all_splits = text_splitter.split_documents(data)
    print(all_splits)
    vectorstore.add_documents(documents=all_splits)

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def querry(question):
    docs = vectorstore.similarity_search(query=question)
    prompt = ChatPromptTemplate.from_template(
        "总结这些检索到的文档中的主要主题: {docs}"
    )
    chain = {"docs": format_docs} | prompt | llm | StrOutputParser()
    ret = chain.invoke(docs)
    return ret


