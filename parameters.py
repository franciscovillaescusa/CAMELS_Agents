from typing_extensions import TypedDict
from typing import Annotated, Literal
from langchain_core.messages import AnyMessage, HumanMessage, SystemMessage, AIMessage
from langgraph.graph.message import add_messages

####################################### INPUT #############################################
# location of the CAMELS documentation
CAMELS_docs_path = '/mnt/home/fvillaescusa/software/CAMELS/docs/source'

# RAG parameters
chunk_size    = 1000
chunk_overlap = 300

# Chroma parameters for CAMELS docs
collection_name_docs   = 'CAMELS'
persist_directory_docs = "docs_database"

# Chroma parameters for CAMELS papers
collection_name_papers   = 'CAMELS_papers'
persist_directory_papers = "papers_database/papers_db"
###########################################################################################

# class for writing CAMELS section
class CS(TypedDict):
    iterations: int = 0
    query: str
    improve: bool = False
    
# class for CAMELS papers
class CP(TypedDict):
    collection_name: str
    persist_directory: str

# class for the database
class database(TypedDict):
    collection_name: str
    persist_directory: str
    CAMELS_docs_path: str
    chunk_size: int
    chunk_overlap: int

# class for the semantic search
class SeSe(TypedDict):
    limit: int

# class containing the state of the graph
class GraphState(TypedDict):
    query: str
    context: list[AnyMessage]
    answer: str
    memory: str
    messages: Annotated[list[AnyMessage], add_messages]
    option: int
    db: database
    cp: CP
    sese: SeSe
    streamlit: bool = False
    cs: CS
    

# define the starting graph state
initial_graph_state = {"query": None,
                       "memory":[],
                       "db":{"collection_name": collection_name_docs,
                             "persist_directory": persist_directory_docs,
                             "chunk_size": chunk_size,
                             "chunk_overlap": chunk_overlap},
                       "cp":{"collection_name": collection_name_papers,
                             "persist_directory": persist_directory_papers},
                       "sese":{"limit": 10}
                       }

# Thread
config = {"configurable": {"thread_id": "1"}, "recursion_limit":30}
