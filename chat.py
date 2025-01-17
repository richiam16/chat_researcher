# Trying the first steps of LLM implementation (first implementation)

from langchain.document_loaders import PyPDFLoader
from langchain.document_loaders import UnstructuredHTMLLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
import os
from langchain.vectorstores import Chroma
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.schema.runnable import RunnablePassthrough
from langchain.chains  import ConversationalRetrievalChain
from langchain.prompts.chat import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory


import glob


# 1 Document Loading

def load_papers_pdf(path):
	"""Method to load the documents into langchain methods
	Args:
		path: path where the papers are located (pdf)
	Returns:
		docs: the documents"""
	pdfs = glob.glob(f"{path}/*.pdf")
	loaders = [PyPDFLoader(doc) for doc in pdfs]
	docs = []
	for loader in loaders:
		docs.extend(loader.load())
	return docs

def load_papers_html(path):
	"""Method to load the documents into langchain methods
	Args:
		path: path where the papers are located (pdf or .html format)
	Returns:
		docs: the documents
	Is it a good idea to have two different methods for html and pdf format?
	Is it worth loading the html ?"""
	loaders = [UnstructuredHTMLLoader(doc) for doc in glob.glob(f"{path}/*.html")]
	docs = []
	for loader in loaders:
		docs.extend(loader.load())
	return docs

# 2 Document Splitting

def text_splitter(docs, chunk_size, chunk_overlap):
	""" Function to create the function to make the splits of the documents
	Args:
		chunk_size: The initial amount to split the text into
		chunk_overlap: tha overlap between chunks
	return:
		splits: the splits of the text
	Note: This methods need more flexibility, aka put different splits method beside Recursive"""
	text_s = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
	splits = text_s.split_documents(docs)
	return splits

# 3 Vectorstore

def vectorstore(documents, embedding_function, directory):
	"""" Function to store the splits of the documents in a vector store
	Args:
		documents: the splits of the documents
		embbedding_function: the function to use to create the embedding
		directory: the path of the directory where the vectorstore will be stored
	Return:
		vectordb: vectorstore object with the informationo of the slipts
	Note: This methos needs more flexibility, aka put different vectorstore options""" 
	vectordb = Chroma.from_documents(documents=documents,embedding=embedding_function,persist_directory=directory)
	return vectordb

# rag versions

def get_name(name):
	return name

def rag_chain(template, name,  retriever, llm):
	"""Function to create a simple rag chain LLM answer and question
	Args:
		template: The prompt template to feed to the rag chain
		name: The name of the researcher
		retriever: The information where the embeddings are stored (for vectorstore)
		llm: The Large Languague model to be used for the ragchain
	Returns:
		rag_: an object from langchain able to answer questions from the papers without history"""
		
	# Making a wrapping function to get the name variable as a function to work with Langchain implementation
	def get_name(_):
		return name
	name_runnable = RunnablePassthrough(get_name)
	rag_prompt_custom = PromptTemplate(input_variables=["name","context","question"],template=template)
	rag_ = ({"name":name_runnable, "context": retriever, "question": RunnablePassthrough()} | rag_prompt_custom | llm)
	return rag_

def rag_chain_conversational(general_system_template, general_user_template, retriever,llm, memory):
	"""Function to create a conversational rag chain for the papers
	Args:
		general_system_template:
		general_user_template:
		retiever:
		memory:
	Return:
		crc: conversational object to chat with"""
	messages = [SystemMessagePromptTemplate.from_template(general_system_template), HumanMessagePromptTemplate.from_template(general_user_template)]
	qa_prompt =  ChatPromptTemplate.from_messages(messages)
	crc = ConversationalRetrievalChain.from_llm(llm, retriever, combine_docs_chain_kwargs={'prompt': qa_prompt}, memory=memory)
	return crc 

# creating function for easy acces
def loading_vectorstore(path, chunk_size, chunk_overlap, embedding_function, directory):
	"""Function to make the initial step of the rag pipeline that is loading the pdfs, and creating the vectorstore
	Args:
		path: path direction of the pdf files
		chunk_size:
		chunk_overlap
		embedding_function:
		directory
	return
		vectorsotre"""
	docs = load_papers_pdf(path)
	splits = text_splitter(docs, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
	vectordb = vectorstore(documents=splits, embedding_function=embedding_function, directory=directory)
	return vectordb


def make_rag_chain(retriever,llm, template):
	"""Function to make the whole pipeline of RAG in few lines of code, 
	also this function has the intention to create a function where it is easy to make changes to the parameters of RAG for testing the performance, 
	GIVEN THE CURRENT IMPROVEMENTS, THSI FUNCTION IS NO LONGER NEEDED"""
	rag_ = rag_chain(template=template, retriever=retriever.as_retriever(), llm=llm)
	return rag_

