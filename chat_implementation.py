from pi_pubs import Researcher # The tool to download the papers
from chat import loading_vectorstore, rag_chain #The tool to make rag_chains
from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
import os

def pi_chat(name,email,number_papers,model_name, path_pubmed=os.getcwd(),path_directory=os.getcwd()):
	"""Function to create an utility to chat with papers of a certain PI
	Args:
		Name: The name of the PI
		email: to interect with pubmed database
		number_papers: The number of papers to chat 
		model name: The name in OpenAI models to use, e.g gpt-3.5-turbo
		path_pubmed: The path of the pubmed papers(This is defined by the pubmeddownloader utility)
		path_directory: The path were the vectorstore is going to be located
	Returns:
		rag_: """
	# Paper Download
	researcher = Researcher(name)
	researcher._pmdid_collection(email,number_papers)
	print(f"Collecting {len(researcher.id_list)} papers")
	researcher._download_papers(path_pubmed)

	# Creating a Vectorstore for the Papers
	# Improve (this create the vectorstore from scratch, what if you already have a vectorstore)
	# Tell how many paper were effectivly embbedded
	print("Creating a Vector Store for this PI")
	vectordb = loading_vectorstore(path=path_pubmed,chunk_size=1200,chunk_overlap=150, embedding_function=OpenAIEmbeddings(), directory=path_directory)
	print(f"A Chroma Vector Store was created in {path_directory}")
	# Make the RAG chain
	template = """You are an assistant for question-answering tasks.The information in {context} are scientific publications in which {name} particpated. Use this information to answer questions about the work, life, and publications of {name}. If you do not know the answer, just say that you do not know the answer. If unsure, say that you are not sure. Use ten sentences maximum and use technical terms in the answers Context:{context}"""
	print("Making a rag chain")
	rag_ = rag_chain(template=template, name=name, retriever=vectordb.as_retriever(),llm= ChatOpenAI(model_name =model_name, temperature=0))
	print("You are ready to chat with the papers, use rag.invoke(question)")
	return rag_


# To do:
	# Not all the papers that are object.pub_id are downloaded (No open, No PDF) ---- (No Pubmed, No open, No PDF), tell how much
	# See if adding pictures is worthit
	# Make changes so that if the user has a vector store, it can be load instead of creating a vector store everytime (API expensive to make a vector store everytime)
	# how to add this function to a streamlit application
	# Implementation: prompt engineering?
	# Create a 	(clean) conda enviroment to have all the requiered packages (esentially, biopython, pubmed2pdf, langchain, os, pypdf)
	# Check implementaiton in colab
	# Test the enviroment against the functions and colab implementation
	# Crceate retrival, conversational method?
	# HALF-DONE:
		## PROMPT IN SINGLE FILE, NOT EXPORTABLE -----------There are better ways to add the prompt to this, check in the templates from langchain
		## path_pubmed and path_directory are set to current directory (messy but workable, needs further changes) -----Reduce the number of parameters to give the function (automatize path_pubmed, path_directory)
	# Done
		## Checked -----------------Check if the papers in researcher object are really by order of publication
		## # Test current changes