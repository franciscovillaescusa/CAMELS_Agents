import streamlit as st
from main import graph
from parameters import config, GraphState
import tiktoken

    
# streamlit configuration
st.set_page_config(
    page_title="CAMELS Agent",     # Title of the app (shown in browser tab)
    page_icon='images/logo.png',      # Favicon (icon in browser tab)
    layout="wide",   # Page layout (options: "centered" or "wide")
    initial_sidebar_state="auto",  # Sidebar behavior
    menu_items=None      # Custom options for the app menu
)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state["messages"] = []
if "state" not in st.session_state:
    st.session_state["state"] = {}  # Initialize as an empty dictionary
if "task_reset_key" not in st.session_state:
    st.session_state["task_reset_key"] = "task_0"  # Default key
if "reset_count" not in st.session_state:
    st.session_state["reset_count"] = 0  # Track resets
if "memory" not in st.session_state["state"]:
    st.session_state["state"]["memory"] = []
if "option" not in st.session_state:
    st.session_state["option"] = None


# Custom CSS for sidebar and main content adjustments
st.markdown(
    """
    <style>
        /* Move sidebar elements up */
        section[data-testid="stSidebar"] div[data-testid="stVerticalBlock"] {
            padding-top: 0px;
            margin-top: -50px; /* Adjust this value to move it further up */
        }

        /* Adjust sidebar width */
        [data-testid="stSidebar"] {
            width: 300px !important;  
        }

        /* Move main content closer to the top */
        .block-container {
            padding-top: 0rem !important;  /* Reduce top space */
            margin-top: 30px;  /* Move content further up */
        } 

        /* Ensure text wraps and does not cause horizontal scrolling */
        div[data-testid="stTextArea"] textarea {
            white-space: pre-wrap !important;  /* Ensures wrapping */
            word-wrap: break-word !important; /* Forces breaking long words */
            overflow-wrap: break-word !important;
            width: 100% !important; /* Makes sure it stays within window width */
        }
        /* Chat messages - prevent horizontal scrolling */
        .stChatMessage {
            white-space: pre-wrap !important;
            word-wrap: break-word !important;
            overflow-wrap: break-word !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

##### Sidebar UI #####
st.sidebar.image('images/logo.png')
st.write("")
st.sidebar.title("Agent Capabilities")

# Sidebar UI with dynamic key for forcing reset
selected_task = st.sidebar.radio("Select an agent task:",
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
               "Standard LLM":         "Working on your query"}

# Assign option based on selection
option = task_options.get(selected_task, None) 

if selected_task:
    st.session_state["task"] = selected_task
    st.session_state["option"] = option
#st.sidebar.write(f"Agent task: {selected_task}")

submit_button = st.sidebar.button("Select task")
st.sidebar.write("\n\n\n\n")
print_memory  = st.sidebar.button("Print memory")
reset         = st.sidebar.button("Clear memory")

if reset:
    # Reset session state properly
    st.session_state["state"] = {"memory": []}  # Reset only the necessary fields
    st.session_state["messages"] = []  # Clear messages
    st.session_state["feedback"] = None
    st.session_state["submitted"] = False
    st.session_state["reset_count"] += 1
    st.session_state["task_reset_key"] = f"task_{st.session_state['reset_count']}"
    st.rerun()  # Force app refresh

# Count tokens
encoding = tiktoken.encoding_for_model("gpt-4")
memory_text = " ".join(map(str, st.session_state["state"].get("memory", [])))
token_count = len(encoding.encode(memory_text)) if memory_text else 0
st.sidebar.write(f"Tokens in memory: {token_count}")

    
    
##########################

# Main UI 
st.title("CAMELS Agent")

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
                st.latex(message["content"])

# Submit button in the sidebar
if submit_button:

    if st.session_state["option"]==1:

        with st.spinner(task_string[st.session_state["task"]]):

            # Run the graph when button is clicked
            result = graph.invoke({"option":option,
                                   "streamlit":True,
                                   "cs":{"improve":False}}, config)
            st.session_state["state"] = GraphState(**result)
        
    # Store that the user has submitted, to control UI rendering
    st.session_state["submitted"] = True
    st.rerun()  # Refresh UI to display the generated text

if st.session_state.get("submitted", False):  # Only show content if submitted
        
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
            st.rerun()  # Refresh UI to display new messages
            
    # other options
    if option in [2,3,4,6]:

        Text, disabled = "Type your query here", False
        feedback = st.chat_input(Text, key='hidden', disabled=disabled)

        if feedback:

            with st.spinner(task_string[st.session_state["task"]]):
        
                # Run the graph when button is clicked and feedback provided
                result = graph.invoke({"option":st.session_state["option"],
                                       "streamlit":True,
                                       "memory":st.session_state["state"]["memory"],
                                       "sese":{"limit": 10},
                                       "query":feedback}, config)
                st.session_state["state"] = GraphState(**result)
                st.rerun()  # Refresh UI to display new messages

