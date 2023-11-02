# Trying the first steps of LLM implementation (first implementation)

from langchain.document_loaders import PyPDFLoader
from langchain.document_loaders import UnstructuredHTMLLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
import os
from langchain.vectorstores import Chroma

import glob


# 1 Document Loading

def load_papers_pdf(path):
	"""Method to load the documents into langchain methods
	Args:
		path: path where the papers are located (pdf or .html format)
	Returns:
		docs: the documents"""
	loaders = [PyPDFLoader(doc) for doc in glob.glob(f"{path}/*.pdf")]
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
	Is it a good idea to have two different methods for html and pdf format? """
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