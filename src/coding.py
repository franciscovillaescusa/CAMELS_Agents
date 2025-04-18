from langchain_core.runnables import RunnableConfig
from langgraph.graph.message import add_messages
from langchain_core.messages import AnyMessage, HumanMessage, SystemMessage, AIMessage
import streamlit as st
from functools import lru_cache

from src.parameters import GraphState
from src.prompts import coding_prompt
from src.llms import get_llm

# Function to CAMELS details, cached for efficiency
@lru_cache(maxsize=1)
def load_instructions():
    with open("Input_Text/CAMELS_coding.txt", "r") as file:
        return file.read()

# node specialized in coding for CAMELS
def coding_node(state: GraphState, config: RunnableConfig):

    # get llm
    model = get_llm(state)
    
    # Load instructions (only once due to caching)
    instructions = load_instructions()
    
    PROMPT = coding_prompt(state["query"], state["memory"], instructions)
    result = model.invoke(PROMPT)

    if state["streamlit"]:
        st.session_state.messages.append({"role": "user",      "content": state["query"],
                                          "type":"write"})
        st.session_state.messages.append({"role": "assistant", "content": result.content,
                                          "type":"write"})
    else:
        print(result.content)

    state["memory"] = add_messages(state["memory"],
                                   [HumanMessage(content=state["query"]),
                                    AIMessage(content=result.content)])

    return {"memory": state["memory"]}
