#from scholarly import scholarly
#from tqdm import tqdm
from Bio import Entrez
import os


class Researcher(object):
	"""A PI class where each PI has it sets of publciations and information"""
	def __init__(self, name):
		"""The object is initialized with only the name of the PI to retrieve the papers"""
		self.name = name

	def _pubs_collection(self):
		""" A method to collect a list of all the publications of the author
		return:
			self.publications: A list of scholarly.publications objects with metadata about the publications of the author"""
		search = scholarly.search_author(self.name)	
		author = scholarly.fill(next(search))
		self.publications = author["publications"]

	def _retrieve_in(total_pub=None):
		"""A method to collect all the metada of the publications
			total_pub = max number of publications to retrieve all the information
			Note: For now all the publications will be retrieved (expensive procedure)
			Note: What is the criteria being used to sort the publications is currently unknown (a sorting by year would be helpfull)
		return:
			Note: Is it necesary to retrieve all the information ?, is it possible to "faste" things with fewer information"""
		for pub in tqdm(self.publications):
			scholarly.fill(pub)

	def _pmdid_collection(self,email, max_results=10000):
		"""A method to collect the pubmedid of all the publications associated with the researcher
			email: user email required for PubMed API
			max_results: maximun number of papers to retrieve
			Note: there might be cases, where the papers might not be from the author, e.g common last names """
		Entrez.email = email 
		query = f"{self.name}[Author]"
		handle = Entrez.esearch(db="pubmed", term=query, retmax=max_results)
		record = Entrez.read(handle)
		if "IdList" in record:
			self.id_list = record["IdList"]
		else:
			self.id_list = [] # Note id_list seems to be sorted from newest papers to oldest papers

	def _download_papers(self, path_out=os.getcwd()):
		"""A method to download the papers from the PubMedId
		Arguments:
			path_out: the folde to save the pdfs
		Note: it would be good to know the progress of the download (aka tqdm)"""
		files = ",".join(self.id_list)
		os.system(f"python3 -m pubmed2pdf pdf --pmids={files} --out {path_out}")

	def main(self, email):
		self._pmdid_collection(email)
		self._download_papers()


# Note: check current notes on problems on the methods
# Note: Would it be usefull to be terminal based ? (as python pi_subs -name "PI" -email "email")
