from langchain_groq import ChatGroq
from langchain_google_vertexai import VertexAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain_core.messages import AnyMessage, HumanMessage, SystemMessage, AIMessage
from langchain_core.runnables import RunnableConfig
from langgraph.graph.message import add_messages
import streamlit as st
from dotenv import load_dotenv
import os,json
from src.parameters import GraphState

# check if secrets exists and look for google credentials there
if os.path.exists(".streamlit/secrets.toml"):
    if "google_credentials" in st.secrets:
        with open("gemini.json", "w") as f:
            json.dump(dict(st.secrets["google_credentials"]), f)

# load optional API keys
load_dotenv()
for var in [ "LANGCHAIN_TRACING_V2", "LANGCHAIN_API_KEY",
             "LANGCHAIN_ENDPOINT",   "LANGCHAIN_PROJECT"]:
    value = os.getenv(var)

# embedding model
embeddings = VertexAIEmbeddings(model="text-embedding-005")


# This function gets the llm model
def get_llm(state):

    # get the model and its temperature
    model       = state['llm']['model']
    temperature = state['llm']['temperature']

    # Gemini
    if   model=='Gemini-2-flash':
        for var in ["GOOGLE_API_KEY", "GOOGLE_APPLICATION_CREDENTIALS"]:
            if not os.getenv(var):
                st.error(f"Missing environment variable: {var}")
        return ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=temperature)

    # ChatGPT
    elif model=='ChatGPT-4o':
        if not os.getenv("OPENAI_API_KEY"):
            st.error(f"Missing environment variable: OPENAI_API_KEY")
        return ChatOpenAI(model="gpt-4o", temperature=temperature)

    # LLama3
    elif model=='Llama3-70b':
        if not os.getenv("GROQ_API_KEY"):
            st.error(f"Missing environment variable: GROQ_API_KEY")
        return ChatGroq(model="llama3-70b-8192", temperature=temperature)

    else:
        st.error("Wrong model choosen!")
        st.stop()

#llm2 = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.5)
#llm2 = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0)
#llm2 = ChatGoogleGenerativeAI(model="gemini-2.0-flash-thinking-exp-01-21", temperature=0)
#llm  = ChatGroq(model="llama3-groq-8b-8192-tool-use-preview", temperature=0)
#llm  = ChatGroq(model="llama3-8b-8192", temperature=0)
#llm2  = ChatGroq(model="gemma2-9b-it", temperature=0.5)
#llm3  = ChatGroq(model="deepseek-r1-distill-qwen-32b", temperature=0.6)
#llm  = ChatGroq(model="gemma2-9b-it", temperature=0)
#llm_t = llm.bind_tools(tools)


# This is for questions that are not related to CAMELS
def standard_llm(state: GraphState, config: RunnableConfig):

    # get the LLM model
    model = get_llm(state)
    
    # invoke the LLM
    result = model.invoke(state["memory"] + [HumanMessage(content=state["query"])])
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
