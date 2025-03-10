from parameters import GraphState
from langchain_core.runnables import RunnableConfig
from langchain_core.messages import AnyMessage, HumanMessage, SystemMessage, AIMessage
from llms import llm2
from prompts import *
import streamlit as st

#####################################################################################
# This node writes a section describing LaTeX
def write_section_node(state: GraphState, config: RunnableConfig):

    # improve a current version
    if state["cs"]["improve"]:

        result = llm2.invoke(improve_section_prompt(state['memory'], state["cs"]["query"]))
        if state["streamlit"]:
            st.session_state.messages.append({"role":"user",
                                              "content":state["cs"]["query"],
                                              "type":"text"})
            st.session_state.messages.append({"role":"assistant",
                                              "content":result.content,
                                              "type":"text"})
        else:
            print(result.content)
        state['memory'] += [HumanMessage(content=f"""
Iteration: {state['cs']['iteration']+1}:

Query: {state['cs']['query']}
Text: {result.content}
""")]

        return {"memory": state["memory"], "cs":{"iteration": state["cs"]["iteration"]+1}}

    # write CAMELS section for the first time
    else:
    
        # get the CAMELS section
        with open('CAMELS_section.txt', 'r') as file:
            text = file.read()

        # generate new section
        result = llm2.invoke(write_section_prompt(text))
        if state["streamlit"]:
            st.session_state.messages.append({"role":"assistant",
                                              "content":result.content,
                                              "type":"text"})
        else:
            print(result.content)

        # build memory
        state['memory'] = [HumanMessage(content=f"""
Original text: 
{text}

Iteration 1:
{result.content}
""")]

    return {"memory": state["memory"], "cs":{"iteration": 1}}
#####################################################################################


