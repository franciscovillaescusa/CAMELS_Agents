from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
import os

from src.parameters import GraphState, initial_graph_state
from src.llms import get_embeddings


# Singleton instances for databases
_db_CAMELS_docs   = None
_db_CAMELS_papers = None

# This function returns the Chroma database used for the CAMELS docs
def get_db_CAMELS_docs():

    global _db_CAMELS_docs
    embeddings = get_embeddings()

    # only do this the first time the function is called
    if _db_CAMELS_docs is None:
        state = initial_graph_state['db']

        # check if database exists
        if not os.path.exists(state['persist_directory']):
            
            # Load and process documents if DB doesn't exist
            docs = DirectoryLoader(state['CAMELS_docs_path'], glob="*.rst").load()
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=state['chunk_size'], 
                chunk_overlap=state['chunk_overlap'])
            splits = text_splitter.split_documents(docs)
            
            _db_CAMELS_docs = Chroma.from_documents(
                splits, 
                embedding=embeddings,
                collection_name=state['collection_name'], 
                persist_directory=state['persist_directory'])
            
        else:
            _db_CAMELS_docs = Chroma(embedding_function=embeddings,
                                     collection_name=state['collection_name'], 
                                     persist_directory=state['persist_directory'])
            
    return _db_CAMELS_docs


# Function to get the CAMELS papers database
def get_db_CAMELS_papers():
    
    global _db_CAMELS_papers

    # only do this the first time the function is called
    if _db_CAMELS_papers is None:
        state = initial_graph_state['cp']
        _db_CAMELS_papers = Chroma(embedding_function=embeddings,
                                   collection_name=state['collection_name'], 
                                   persist_directory=state['persist_directory'])
        
    return _db_CAMELS_papers

