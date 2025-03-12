from langchain_groq import ChatGroq
from langchain_google_vertexai import VertexAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import AnyMessage, HumanMessage, SystemMessage, AIMessage
from parameters import GraphState
from langchain_core.runnables import RunnableConfig
from langgraph.graph.message import add_messages
import streamlit as st
from dotenv import load_dotenv
import os

# load API keys
load_dotenv()
required_env_vars = [
    "LANGCHAIN_TRACING_V2", "LANGCHAIN_API_KEY", "LANGCHAIN_ENDPOINT", "LANGCHAIN_PROJECT",
    "GOOGLE_API_KEY", "GOOGLE_APPLICATION_CREDENTIALS"]
for var in required_env_vars:
    if not os.getenv(var):
        st.error(f"Missing environment variable: {var}")

#llm2 = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0)
llm2 = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.5)
#llm2 = ChatGoogleGenerativeAI(model="gemini-2.0-flash-thinking-exp-01-21", temperature=0)
#llm  = ChatGroq(model="llama3-groq-8b-8192-tool-use-preview", temperature=0)
#llm  = ChatGroq(model="llama3-8b-8192", temperature=0)
#llm2  = ChatGroq(model="gemma2-9b-it", temperature=0.5)
#llm3  = ChatGroq(model="deepseek-r1-distill-qwen-32b", temperature=0.6)
#llm  = ChatGroq(model="gemma2-9b-it", temperature=0)
#llm_t = llm.bind_tools(tools)

embeddings = VertexAIEmbeddings(model="text-embedding-005")


# This is for questions that are not related to CAMELS
def standard_llm(state: GraphState, config: RunnableConfig):
    
    # invoke the LLM
    result = llm2.invoke(state["memory"] + [HumanMessage(content=state["query"])])
    if state["streamlit"]:
        st.session_state.messages.append({"role": "user",      "content": state["query"],
                                          "type":"md"})
        st.session_state.messages.append({"role": "assistant", "content": result.content,
                                          "type":"md"})
    else:
        print(result.content)

    state["memory"] = add_messages(state["memory"],
                                   [HumanMessage(content=state["query"]),
                                    AIMessage(content=result.content)])
        
    return {"memory": state["memory"]}
