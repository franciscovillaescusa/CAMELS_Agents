import streamlit as st
from src.main import graph
from src.parameters import config, GraphState
import tiktoken
import streamlit.components.v1 as components
    
# streamlit configuration
st.set_page_config(
    page_title="CAMELS Agent",       # Title of the app (shown in browser tab)
    page_icon='images/logo.png',     # Favicon (icon in browser tab)
    layout="wide",                   # Page layout (options: "centered" or "wide")
    initial_sidebar_state="auto",    # Sidebar behavior
    menu_items=None                  # Custom options for the app menu
)


# --- Initialize Session State ---
def init_session_state():
    defaults = {"messages": [],
                "state": {"memory": []},
                "task_reset_key": "task_0",
                "reset_count": 0,
                "option": None,
                "selected_llm": None,
                "temperature": None,
                "LLM_API_KEYS": {}}
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
init_session_state()

# --- Custom CSS Styling ---
st.markdown("""
    <style>
        [data-testid="stSidebar"] { width: 300px !important; }
        div[data-testid="stTextArea"] textarea, .stChatMessage {
            white-space: pre-wrap !important;
            word-wrap: break-word !important;
            overflow-wrap: break-word !important;
            width: 100% !important;
        }
    </style>
    """, unsafe_allow_html=True)

##### Sidebar UI #####
st.sidebar.image('images/logo.png')

selected_llm = st.sidebar.selectbox(
    "Choose the LLM:",
    ["ChatGPT-4o",
     "3o-mini",
     "Gemini-2-flash",
     "Sonnet-3.7",
     "DeepSeek-R1-Llama70b",
     "DeepSeek-R1-Qwen32b",     
     "Llama3-70b",
     "Gemma2-9b"],
    index=2, key="llm_select_key")
st.session_state["selected_llm"] = selected_llm


# If API key doesn't exist, show the input field
if selected_llm not in st.session_state["LLM_API_KEYS"]:
    api_key = st.sidebar.text_input(
        f"Enter API key for {selected_llm}:",
        type="password",
        key=f"{selected_llm}_api_key_input"
    )
    
    # If the user enters a key, save it and rerun to refresh the interface
    if api_key:
        st.session_state["LLM_API_KEYS"][selected_llm] = api_key
        st.rerun()

# Display status after the key is saved
if selected_llm in st.session_state["LLM_API_KEYS"]:
    st.sidebar.markdown(f"<small style='color:green;'> ✅: {selected_llm} API key set</small>",unsafe_allow_html=True)
else:
    st.sidebar.markdown(f"<small style='color:red;'>❌: No {selected_llm} API key</small>", unsafe_allow_html=True)

    #st.sidebar.markdown(f"<small style='color:#f39c12;'> ❌: No {selected_llm} API key </small>", unsafe_allow_html=True)

    
st.session_state["temperature"] = st.sidebar.slider("LLM temperature:",
                                                    min_value=0.0, max_value=1.0,
                                                    value=0.5, step=0.05)

# Sidebar UI with dynamic key for forcing reset
selected_task = st.sidebar.radio("Select the agent task:",
                                 ["Write CAMELS section",
                                  "CAMELS documentation",
                                  "CAMELS papers",
                                  "General literature",
                                  "Coding",
                                  "Standard LLM"],
                                 index=None, 
                                 key=st.session_state["task_reset_key"])  # Use dynamic key

# Mapping tasks to option values
task_options = {"Write CAMELS section": 1,
                "CAMELS documentation": 2,
                "CAMELS papers":        3,
                "General literature":   4,
                "Coding":               5,
                "Standard LLM":         6}

task_string = {"Write CAMELS section": "Writing CAMELS section...",
               "CAMELS documentation": "Searching CAMELS docs...",
               "CAMELS papers":        "Searching CAMELS papers...",
               "General literature":   "Searching the arXiv...",
               "Coding":               "Working on your query...",
               "Standard LLM":         "Working on your query..."}

# Assign option based on selection
option = task_options.get(selected_task, None) 

if selected_task:
    st.session_state["task"] = selected_task
    st.session_state["option"] = option

submit_button = st.sidebar.button("Select task", use_container_width=True)

# Count tokens
encoding = tiktoken.encoding_for_model("gpt-4")
memory_text = " ".join(map(str, st.session_state["state"].get("memory", [])))
token_count = len(encoding.encode(memory_text)) if memory_text else 0
st.sidebar.write(f"Tokens in memory: {token_count}")

#with st.sidebar:
col1, col2 = st.sidebar.columns(2)  # Create two columns within the sidebar
with col1:
    print_memory  = st.button("Print memory")  
with col2:
    reset         = st.button("Clear memory")

if reset:
    # Reset session state properly
    st.session_state["state"] = {"memory": []}  # Reset only the necessary fields
    st.session_state["messages"] = []  # Clear messages
    st.session_state["feedback"] = None
    st.session_state["submitted"] = False
    st.session_state["reset_count"] += 1
    st.session_state["task_reset_key"] = f"task_{st.session_state['reset_count']}"
    st.rerun()  # Force app refresh
    
    
##########################

# Main UI 

# --- Show Instructions Only Before Submission ---
if "submitted" not in st.session_state or not st.session_state["submitted"]:
    st.markdown("""
    # Welcome to CAMELS Agents! 🐪 🤖

    ## Instructions:
    1. Select the LLM model you want
    2. Introduce your API key
    3. Choose the temperature of the model
    4. Select the agent task
    5. Click the `Select task` button

    ## LLMs:

    CAMELS Agents support different LLM models.

    | Model                  | Required API Key | Instructions to get API Key | 
    |------------------------|-----------------|---------------------------------| 
    | **Gemini-2-flash**     | Gemini API      | Go to this [website](https://ai.google.dev/gemini-api/docs/api-key) and get your API key there. |
    | **ChatGPT-4o**        | OpenAI API      | Go to this [website](https://platform.openai.com/docs/overview). On the top-right, click on settings, and then get your API key there. Take a look at this [page](https://medium.com/@lorenzozar/how-to-get-your-own-openai-api-key-f4d44e60c327) if you encounter problems. | 
    | **ChatGPT-3o-mini**   | OpenAI API      | Go to this [website](https://platform.openai.com/docs/overview). On the top-right, click on settings, and then get your API key there. Take a look at this [page](https://medium.com/@lorenzozar/how-to-get-your-own-openai-api-key-f4d44e60c327) if you encounter problems. | 
    | **Sonnet-3.7**        | Anthropic API   | Go to this [website](https://console.anthropic.com/settings/keys) and get your API key there. |
    | **DeepSeek-R1-Llama70b** | Groq API    | Go to this [website](https://console.groq.com/keys) and get your API key there. |
    | **DeepSeek-R1-Qwen32b**  | Groq API    | Go to this [website](https://console.groq.com/keys) and get your API key there. |
    | **Llama3-70b**        | Groq API        | Go to this [website](https://console.groq.com/keys) and get your API key there. |
    | **Gemma2-9b**         | Groq API        | Go to this [website](https://console.groq.com/keys) and get your API key there. |
    
    ## Temperature:

    The temperature of the LLM controls the "randomness" of the output. For creative tasks, e.g. generating ideas or rewriting text, you may want to use a high temperature. For tasks where you want reproducibility, you want to set the temperature to low values. For instance, for many LLM and coding, it is better to set the temperature to 0.

    ## Tasks:

    | Task                    | Description |
    |-------------------------|-------------|
    | **Write CAMELS section** | Writes a CAMELS data section for a scientific paper describing the data. You may want to use a relatively high temperature for this task. |
    | **CAMELS documentation** | Implements RAG with the CAMELS documentation. If you have questions about CAMELS that may be in the documentation, you can start a conversation with the chatbot to get your answer. |
    | **CAMELS papers**       | Implements RAG with CAMELS papers. Useful to find CAMELS papers about a given topic. |
    | **General literature**  | Calls Semantic Scholar to explore papers on the arXiv given a query. |
    | **Coding**             | Allows you to write code tailored for the CAMELS simulations. Knows about CAMELS data format, structure, and types. |
    | **Standard LLM**       | Gives access to the selected LLM. Any accumulated memory from other sections will be passed as context to the LLM. Useful for performing non-specific CAMELS tasks. |

    ## Memory:

    Any tokens in memory will be passed to the LLM as context. Take into account that some models have a relatively small context size of ~8000 tokens (e.g. Gemma2 and Llama3). Also take into account that the larger the context window, the more expensive the call to the LLM. You can see your memory by clicking the "Print memory" button. To clear the memory, click the "Clear memory" button.

    ## Team:

    - Francisco Villaescusa-Navarro (Flatiron)
    - Boris Bolliet (Cambridge)
    - Pablo Villanueva-Domingo (Barcelona)
    - ChangHoon Hahn (Arizona)
    - The [CAMELS](https://www.camel-simulations.org) team

    ## Questions & problems:

    If our agents cannot solve your question or you have problems, feel free to reach out to us at camel.simulations@gmail.com

    ## Disclaimer

    Please be aware that LLMs make mistakes and hallunicate. Always validate the accuracy of the outcome of the agents. Check if there are journal regulations about using LLMs for text in scientific papers.
    
    """)


# print messages
if print_memory:
    memory_text = "\n".join(map(str, st.session_state["state"]["memory"]))
    st.text_area("Memory Content", memory_text, height=500)
else:
    # Display chat messages correctly using st.chat_message()
    for message in st.session_state["messages"]:
        with st.chat_message(message["role"]):
            if message["type"]=="md":
                st.markdown(message["content"])
            elif message["type"]=="text":
                st.text(message["content"])
            else:
                st.write(message["content"])

# Submit button in the sidebar
if submit_button:

    # Safely check for the API key
    if not st.session_state["LLM_API_KEYS"].get(selected_llm):
        st.error(f'Missing API key for {selected_llm}')
        st.stop()
    
    if st.session_state["option"]==1:

        with st.spinner(task_string[st.session_state["task"]]):
            
            # Run the graph when button is clicked
            result = graph.invoke({"option":option,
                                   "streamlit":True,
                                   "llm":{"model":st.session_state["selected_llm"],
                                          "temperature": st.session_state["temperature"],
                                          "key": st.session_state["LLM_API_KEYS"][selected_llm]},
                                   "cs":{"improve":False}}, config)
            st.session_state["state"] = GraphState(**result)
        
    # Store that the user has submitted, to control UI rendering
    st.session_state["submitted"] = True
    st.rerun() 

# Only show content if submitted
if st.session_state.get("submitted", False):  
        
    # CAMELS section
    if option==1:
        
        # User feedback
        if "satisfied" not in st.session_state:
            st.session_state.satisfied = None  # Initialize radio selection
        
        satisfied = st.radio("Are you happy with the text?", ("Yes", "No"),
                             index=None, key="satisfied")

        # set properties of lower chat input
        satisfied = st.session_state.get("satisfied", None)
        if satisfied==None:
            Text, disabled = "Please choose an option", True
        else:
            Text, disabled = "Please provide feedback to improve the text", False
        feedback = st.chat_input(Text, key='hidden', disabled=disabled)

        if satisfied=="Yes":
            st.success("Process completed!")
            st.session_state["submitted"]=False
            st.session_state["feedback"]=None
            st.session_state.pop("satisfied", None)
            st.session_state.pop("task", None)
            st.session_state["reset_count"] += 1
            st.session_state["task_reset_key"] = f"task_{st.session_state['reset_count']}"
            st.rerun()

        elif satisfied=="No" and feedback:

            with st.spinner(task_string[st.session_state["task"]]):
                
                # Invoke agent with feedback
                result = graph.invoke({"option":1, "streamlit":True,
                                       "cs":{"improve":True, "query":feedback,
                                             "iteration":1}}, config)
                st.session_state["state"] = GraphState(**result)
                
            # Reset selection before rerun
            st.session_state.pop("satisfied", None)
            st.rerun()  
            
    # other options
    if option in [2,3,4,5,6]:

        Text, disabled = "Type your query here", False
        feedback = st.chat_input(Text, key='hidden', disabled=disabled)

        if feedback:

            if not(st.session_state['LLM_API_KEYS'][selected_llm]):
                st.stop(f'Missing API key for {selected_llm}')
            
            with st.spinner(task_string[st.session_state["task"]]):
                
                # Run the graph when button is clicked and feedback provided
                result = graph.invoke({"option":st.session_state["option"],
                                       "streamlit":True,
                                       "llm":{"model":st.session_state["selected_llm"],
                                              "temperature": st.session_state["temperature"],
                                              "key": st.session_state["LLM_API_KEYS"][selected_llm]},
                                       "memory":st.session_state["state"]["memory"],
                                       "sese":{"limit": 10},
                                       "query":feedback}, config)
                st.session_state["state"] = GraphState(**result)
                st.rerun()  



