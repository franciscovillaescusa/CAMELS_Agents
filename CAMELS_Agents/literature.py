import requests
import os,json
from parameters import GraphState
from langchain_core.runnables import RunnableConfig
from dotenv import load_dotenv
import streamlit as st

# Set your API key here
load_dotenv()
API_KEY = os.getenv("SEMANTIC_SCHOLAR_KEY")

# Base URL for Semantic Scholar API
BASE_URL = "https://api.semanticscholar.org/graph/v1/paper/search"


# This function find papers given a query and returns the results
def SSAPI(query, limit):
    """
    Search for papers similar to the given query using Semantic Scholar API.


    Args:
        query (str): The search query (e.g., keywords or paper title).
        limit (int): Number of papers to retrieve (default is 10).


    Returns:
        list: A list of dictionaries containing paper details.
    """
    headers = {
        "x-api-key": API_KEY,
    }
    params = {
        "query": query,
        "limit": limit,
        "fields": "title,authors,year,abstract,url"
    }
    response = requests.get(BASE_URL,
                            headers=headers,
                            params=params)


    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return []


# This node checks
def semantic_search(state: GraphState, config: RunnableConfig):

    # search papers given the query
    results = SSAPI(state['query'], limit=state['sese']['limit'])
    st.session_state.messages.append({"role": "user", "content": state["query"],
                                      "type":"md"})

    total_papers = results.get("total", []) #total number of relevant papers found
    token        = results.get("token", []) #
    papers       = results.get("data", [])  #the actual data of the retrieved papers

    if papers:
        papers_str = f"Found {total_papers} potentially relevant papers. Listing the first 10:\n"
        print(papers_str)
        for idx, paper in enumerate(papers, start=1):
            title = paper.get("title", "No Title")
            authors = ", ".join([author.get("name", "Unknown") for author in paper.get("authors", [])])
            year = paper.get("year", "Unknown Year")
            abstract = paper.get("abstract", "No Abstract")
            url = paper.get("url", "No URL")
            papers_str += f"""**{idx}. {title} ({year})**\n**Authors:** {authors}\n**Abstract:** {abstract}\n**URL:** {url}\n\n"""
            print(f'{title} ({year})')
            print(f'{authors}')
            print(f'{abstract}')
            print(f'{url}\n\n')
    else:
        print("No papers found.\n")
        papers_str = "No papers found\n"
        
    if state["streamlit"]:
        st.session_state.messages.append({"role": "assistant", "content": papers_str,
                                          "type":"md"})

