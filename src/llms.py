from langchain_google_vertexai import VertexAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_groq import ChatGroq
from langchain_deepseek import ChatDeepSeek
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

# This function gets the embedding model
def get_embeddings():

    value = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    return VertexAIEmbeddings(model="text-embedding-005")


# This function gets the llm model
def get_llm(state: GraphState):

    # get the model and its temperature
    model       = state['llm']['model']
    temperature = state['llm']['temperature']
    API_KEY     = state['llm']['key']

    # Google
    if   model in ['Gemini-2-flash', 'Gemini-2-pro']:
        os.environ["GOOGLE_API_KEY"] = API_KEY
        if model=='Gemini-2-flash':
            return ChatGoogleGenerativeAI(model="gemini-2.0-flash",
                                          temperature=temperature)
        elif model=='Gemini-2-pro':
            return ChatGoogleGenerativeAI(model="gemini-2.0-pro-exp-02-05",
                                          temperature=temperature)

    # OpenAI
    elif model in ['ChatGPT-4o', '3o-mini']:
        os.environ["OPENAI_API_KEY"] = API_KEY
        if model=="ChatGPT-4o":
            return ChatOpenAI(model="gpt-4o", temperature=temperature)
        elif model=='3o-mini':
            return ChatOpenAI(model="o3-mini")

    # Anthropic
    elif model=="Sonnet-3.7":
        os.environ["ANTHROPIC_API_KEY"] = API_KEY
        return ChatAnthropic(model="claude-3-7-sonnet-20250219", temperature=temperature)

    # DeepSeek
    elif model in ['DeepSeek-V3', 'DeepSeek-R1']:
        os.environ["DEEPSEEK_API_KEY"] = API_KEY
        if model=='DeepSeek-V3':
            return ChatDeepSeek(model="deepseek-chat", temperature=temperature)
        elif model=='DeepSeek-R1':
            return ChatDeepSeek(model="deepseek-reasoner", temperature=temperature)

    # Groq
    elif model in ['Llama3-70b', 'Gemma2-9b', "Mistral-saba-24b",
                   "DeepSeek-R1-Llama70b", "DeepSeek-R1-Qwen32b"]:
        os.environ["GROQ_API_KEY"] = API_KEY

        if   model=='Llama3-70b':
            return ChatGroq(model='Llama3-70b-8192', temperature=temperature)
        elif model=='Gemma2-9b':
            return ChatGroq(model='gemma2-9b-it',    temperature=temperature)
        elif model=='DeepSeek-R1-Llama70b':
            return ChatGroq(model='deepseek-r1-distill-llama-70b',
                            temperature=temperature)
        elif model=="DeepSeek-R1-Qwen32b":
            return ChatGroq(model="deepseek-r1-distill-qwen-32b", temperature=temperature)
        elif model=="Mistral-saba-24b":
            return ChatGroq(model="mistral-saba-24b", temperature=temperature)
            
        
    else:
        st.error("Wrong model choosen!")
        st.stop()


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
