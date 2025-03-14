<img src="images/logo.png" alt="CAMELS Agents" width="400" style="display: block; margin: auto;">


AI agents to help working with [CAMELS](https://camels.readthedocs.io) (Cosmology and Astrophysics with MachinE Learning Simulations) data.

# Installation

### Requirements:
- python 3.10 or above. Needed to properly use the UI.
- An API for the LLM model. CAMELS Agents supports Gemini, ChatGPT, and Llama3.
- A Vertex AI setup file for the embeddings.
- A [langchain](https://www.langchain.com) API key (optional). 
- A [semantic scholar](https://www.semanticscholar.org) API key (optional).

### Instructions:
- git clone https://github.com/franciscovillaescusa/CAMELS_Agents.git
- cd CAMELS_Agents
- python -m venv CA_env
- source CA_env/bin/activate
- pip install .

At this point, the library should be installed together with all its dependencies. Next we need to create a .env with this content:

```
# Vertex AI (used for embeddings)
GOOGLE_APPLICATION_CREDENTIALS=gemini.json

# Gemini parameters (needed if using Gemini)
GOOGLE_API_KEY=your_google_api_key

# OpenAI parameters (needed if using ChatGPT)
#OPENAI_API_KEY=your_openai_api_key

# Groq parameters (needed if using Llama3)
#GROQ_API_KEY=your_groq_api_key

# LangChain parameters (optional)
#LANGCHAIN_TRACING_V2=true
#LANGCHAIN_API_KEY=your_langchain_api_key
#LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
#LANGCHAIN_PROJECT=Tools

# Semantic scholar key (optional)
#SEMANTIC_SCHOLAR_KEY=your_semantic_schoolar_api_key
```
If, for example, you are going to use ChatGPT, comment the gemini parameters, comment out the OPENAI_API_KEY and put your own key.

### How to get the keys

**LLMs:**

- **Gemini**. Get the API key from the [Gemini API key](https://ai.google.dev/gemini-api/docs/api-key).
- **OpenAI**. Get the API key from the [openai website](https://platform.openai.com).
- **GROQ**. Get the API key from the [Groq website](https://console.groq.com/).

**Vertex AI**. CAMELS agents use an embedding model (text-embedding-005) for RAG tasks. To enable the google embeddings, follow these instructions:

- login into google cloud: https://console.cloud.google.com/
- create a project
- go to IAM & Admin
- go to Service Accounts
- create Service Account
- choose a name
- Create and Continue
- Grant the "Vertex AI User" role
- click Continue and then Done
- click in the three dots and Manage keys
- Add key --> Create new key --> JSON --> Create
- Download the JSON file and place it inside the CAMELS_Agent subfolder
- change the name of that file to gemini.json

**Langchain (optional)**. Go to the [langsmith](https://www.langchain.com/langsmith) website and login. Click on settings (bottom left) and create an API key.

**Semantic scholar (optional)**. Go to the [semantic schoolar website](https://www.semanticscholar.org) and sign in/create an account. At the bottom of the page, go to API overview. At the end of the page there is a form to request an API key. Note that unless you made use of semantic schoolar heavily, you dont need an API key.


# Run

Once the code is installed and all the API keys in place type:

`streamlit run app.py`

# Tuning prompts.

CAMELS Agents use several text files to context and/or guide the LLM behaviour. You may want to tune these for your particular needs.

### CAMELS section

The original text describing CAMELS is located in `Input_Text/CAMELS_section.txt`. Modify that section if you want a different initial description.

### CAMELS papers

The agents are able to identify CAMELS papers for a given query; for instance to see if an idea has been already carried out. The list of CAMELS papers is located in `Input_Text/CAMELS_papers_links.py`. Add any paper you want to the list for the agents to work with them. One the list is updated, go to `CAMELS_Agents` folder and run `python update_db_CAMELS_papers.py` to add those papers to the Chroma database.

### CAMELS coding

The guidelines to use CAMELS data are in `Input_Text/CAMELS_coding.txt`. Add or modify that file for your needs. Take into account that the longer the file, the larger the context and the more expensive the call to the LLM will be.

# Team:

- Francisco Villaescusa-Navarro (Flatiron)
- Boris Bolliet (Cambridge)