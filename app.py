import streamlit as st
from src.main import graph
from src.parameters import config, GraphState
import tiktoken
    
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
    ["ChatGPT-4o", "Llama3-70b", "Gemini-2-flash", "Gemma2-9b", "DeepSeek-R1-Llama70b"],
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
    st.sidebar.success(f"{selected_llm} API key set ✅")
else:
    st.sidebar.warning(f"{selected_llm} API key not set ❌")

    
st.session_state["temperature"] = st.sidebar.slider("LLM temperature:",
                                                    min_value=0.0, max_value=2.0,
                                                    value=0.5, step=0.1)

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

submit_button = st.sidebar.button("Select task")

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

