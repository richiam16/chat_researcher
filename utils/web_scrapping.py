from langchain.chat_models import ChatOpenAI
from langchain.chains import create_extraction_chain # TO create a langchain extraction
from langchain.text_splitter import RecursiveCharacterTextSplitter
import pprint
from langchain.document_loaders import AsyncChromiumLoader
from langchain.document_transformers import BeautifulSoupTransformer, Html2TextTransformer


llm = ChatOpenAI(temperature=0, model="gpt-4")
# A guide for the LLM to extract the data

#schema = {
#	"properties": {
#	"news_article_title": {"type": "string"},
#	"news_article_summary": {"type": "string"},
#	},
#	"required": ["news_article_title", "news_article_summary"]
#}
 	
# Maximal Schema
#schema = {
#	"properties": {
#	"faculty_name": {"type","string"},
#   "faculty_email": {"type","string"},
#	"faculty_office": {"type","string"},
#	"faculty_phone":{"type","string"},
#	"faculty_web":{"type","string"},
#	"faculty_specialty":{"type","string"},
#	"faculty_research_topics":{"type","string"}
#	},
#	"required":["faculty_name","faculty_specialty","faculty_research_topics"]
#}

# Minimal Schema
#schema = {
#	"properties": {
#	"faculty_name": {"type":"string"},
#	"faculty_specialty":{"type":"string"},
#	"faculty_research_topics":{"type":"string"}
#	},
#	"required":["faculty_name","faculty_specialty","faculty_research_topics"]
#}

def extract(content: str, schema: dict):
	"""fucntion to extract information from the web (webscrapping) with an LLM
	Args:
		content: the webpage in docs(langchain) format
	return:
		create_extraction_chain(schema=schema, llm=llm).run(content): information compiled by the LLM from the web"""
	return create_extraction_chain(schema=schema, llm=llm).run(content)

def scrape_with_playwritght_soup(urls, schema, tags, num):
	""""web scrapping function with paywright and beautifulsoup
	Args:
		urls: a list of the urls that have the information that the LLM is going to look for
		schema: a dictionary that contains the information that the LLMS is going to look for
		tags: a list of the parts of the HTML that needs to be filtered
	Returns:
		extracted content: the information that the LLM got from the webpage in a dictionary
		"""
	loader = AsyncChromiumLoader(urls)
	docs = loader.load()
	bs_transformer = BeautifulSoupTransformer()
	# for faculty use div
	docs_transformed = bs_transformer.transform_documents(docs, tags_to_extract=tags)
	print("Extracting content with LLM")
	splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(chunk_size=1000,chunk_overlap=0)
	splits = splitter.split_documents(docs_transformed)
	extracted_content = extract(schema=schema, content=splits[num].page_content)
	pprint.pprint(extracted_content)
	return extracted_content

def scrape_with_playwritght_html(urls, schema, num):
	""""web scrapping function with paywright and beautifulsoup
	Args:
		urls: a list of the urls that have the information that the LLM is going to look for
		schema: a dictionary that contains the information that the LLMS is going to look for
	Returns:
		extracted content: the information that the LLM got from the webpage in a dictionary
		"""
	loader = AsyncChromiumLoader(urls)
	docs = loader.load()
	html2text = Html2TextTransformer()
	docs_transformed = html2text.transform_documents(docs)
	print("Extracting content with LLM")
	splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(chunk_size=1000,chunk_overlap=0)
	splits = splitter.split_documents(docs_transformed)
	extracted_content = extract(schema=schema, content=splits[num].page_content)
	pprint.pprint(extracted_content)
	return extracted_content