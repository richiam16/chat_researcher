from pi_pubs import Researcher # The tool to download the papers
from chat import loading_vectorstore, rag_chain #The tool to make rag_chains
from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
import os
import glob
import sys

template = """You are an assistant for question-answering tasks.The information in {context} are scientific publications in which {name} particpated. Use this information to answer questions about the work and publications of {name}. If you do not know the answer, just say that you do not know the answer. If unsure, say that you are not sure. Use ten sentences maximum and use technical terms in the answers Context:{context}"""

def pi_chat(name,email,number_papers,model_name="gpt-3.5-turbo", path_pubmed="Data/PDFs",path_directory="Data/Vectorstore", template=template):
	"""Function to create an utility to chat with papers of a certain PI/ Researcher
	Args:
		Name: The name of the PI or researcher
		email: email to interect with pubmed database (Mandatory to use with Pubmed API)
		number_papers: The number of papers to chat 
		model name: The name in OpenAI models to use, e.g gpt-3.5-turbo
		path_pubmed: The path of the pubmed papers
		path_directory: The path were the vectorstore is going to be located
	Returns:
		exit print statments (When rag can not be implemented) or
		rag_: A rag object to interact and chat with the papers of PIs/Researcher"""
	# Three steps: Paper Download, Vectorstore creation and RAG creation
	# Paper Download
	researcher = Researcher(name)
	researcher._pmdid_collection(email,number_papers)
	# Exit the function if no papers were found
	if len(researcher.id_list) !=0:
		print(f"Collecting {len(researcher.id_list)} papers")
		researcher._download_papers(path_pubmed)
	else:
		return print("No publications were found for this PI/Researcher")

	# Creating a Vectorstore for the Papers
	# Improve (this create the vectorstore from scratch, what if you already have a vectorstore)
	num_ = len(glob.glob(path_pubmed + '/*.pdf'))
	# EXit the function if no PDFs was downloaded
	if num_ != 0:
		print(f"Creating a Vector Store for this PI with {num_} PDFs")
		vectordb = loading_vectorstore(path=path_pubmed,chunk_size=1200,chunk_overlap=150, embedding_function=OpenAIEmbeddings(), directory=path_directory)
		print(f"A Chroma Vector Store was created in {path_directory}")
	else:
		return print("No PDFS were retrieved, attempt with a higher number of papers")
	# Make the RAG chain
	print("Making a rag chain")
	rag_ = rag_chain(template=template, name=name, retriever=vectordb.as_retriever(),llm= ChatOpenAI(model_name =model_name, temperature=0))
	print("You are ready to chat with the papers, use rag.invoke(question)")
	return rag_


# To do:
	# Improvments:
		# how to add this function to a streamlit application
		# Implementation: prompt engineering?
		# temperature as an argument? (Probably not necesary)
		# Given a folder with PDFs, ignore downloading and go directly to vectorstore and RAG creation
		# Given a vectorstore, ignore downloading and vectorstore creation go directly to RAG creation
		# Mention the docuement from retrieval
		# make files to create a local installation (templates and installation)  
	# Debugging:	
		# Make a folder per PI so that the program does not create use already download papers
	# HALF-DONE:
		## PROMPT IN SINGLE FILE, NOT EXPORTABLE -----------There are better ways to add the prompt to this, check in the templates from langchain
	# Done
		## Checked ----------------- Check if the papers in researcher object are really by order of publication
		## Checked ----------------- Test current changes (07/12/2023)
		## Created ----------------- Create a (clean) conda enviroment to have all the requiered packages (esentially, biopython, pubmed2pdf, langchain, os, pypdf)
		## Checked ----------------- Check implementaiton in colab
		## Done    ----------------- path_pubmed and path_directory are now referenced to the internal folder Data/*-------path_pubmed and path_directory are set to current directory (messy but workable, needs further changes) -----Reduce the number of parameters to give the function (automatize path_pubmed, path_directory)
		## Done    ----------------- Not all the papers that are object.pub_id are downloaded (No open, No PDF) ---- (No Pubmed, No open, No PDF), tell how much
		## DOne    ----------------- Add the test_colab to github (test)
		## Done and Checked -------- Check what happens if there is no id_list (stop the program---Probably will show error)
		## DOne    ----------------- Check what happens if there is no docs, ie there are no PDFs in the folder ? (stop the program)