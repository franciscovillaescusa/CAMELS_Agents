from langchain_core.runnables import RunnableConfig
from langchain_core.messages import AnyMessage, HumanMessage, SystemMessage, AIMessage
from langgraph.graph.message import add_messages
import streamlit as st
import os

from src.parameters import GraphState
from src.llms import get_llm
from src.prompts import *
from src.database import get_db_CAMELS_docs



# This node collects the user query
def question(state: GraphState, config: RunnableConfig):
    
    if state["query"]==None:
        query = input("Write your question here. To exist, type END.\n>> ")
    else:
        query = input(">> ")
    return {"query": query, "messages":[HumanMessage(content=query)]}


# Given a query, this node will search the CAMELS docs to find an answer
def CAMELS_docs(state: GraphState, config: RunnableConfig):

    # get the LLM model
    model = get_llm(state)
    
    # get the documents more similar to the query
    db_docs = get_db_CAMELS_docs()
    results = db_docs.similarity_search_with_relevance_scores(state["query"], k=10)

    # get the context for the LLM call\
    state["context"] = '\n\n'.join(res[0].page_content for res in results)
    
    #for res in results:
    #    print('#########################')
    #print(res[0].page_content)
    #print(res[0].metadata['source'])
    #filter={"source": "tweet"})

    if state["memory"]==[]:  PROMPT = []
    else:                    PROMPT = state["memory"].copy()

    PROMPT = RAG_prompt(state['memory'], state['context'], state['query'])
    
    # get the RAG result
    result = model.invoke(PROMPT)
    if state["streamlit"]:
        st.session_state.messages.append({"role": "user", "content": state["query"],
                                          "type":"md"})
        st.session_state.messages.append({"role": "assistant", "content": result.content,
                                          "type":"md"})
    else:
        print(result.content)

    mem = add_messages(state["memory"], [HumanMessage(content=state["query"]),
                                         AIMessage(content=result.content)])
    
    return {"answer": result.content, "memory": mem, "context": state["context"]}


# This node will generate a response using RAG
def generate(state: GraphState, config: RunnableConfig):

    if state["memory"]==[]:  PROMPT = []
    else:                    PROMPT = state["memory"].copy()

    PROMPT = RAG_prompt(state['memory'], state['context'], state['query'])

    # get the RAG result
    result = model.invoke(PROMPT)
    print(result.content)

    mem = add_messages(state["memory"], [HumanMessage(content=state["query"]),
                                         AIMessage(content=result.content)])

    return {"answer": result.content, "memory": mem}

