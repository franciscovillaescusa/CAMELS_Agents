<img src="images/logo.png" alt="CAMELS Agents" width="400" style="display: block; margin: auto;">


AI agents to help working with [CAMELS](https://camels.readthedocs.io) (Cosmology and Astrophysics with MachinE Learning Simulations) data.

# Installation

### Requirements:
- python 3.10 or above. Needed to properly use the UI.
- A [langchain](https://www.langchain.com) API key.
- A [gemini](https://console.cloud.google.com) API key.
- A [semantic scholar](https://www.semanticscholar.org) API key (optional).

### Instructions:
- git clone https://github.com/franciscovillaescusa/CAMELS_Agents.git
- cd CAMELS_Agents
- python -m venv CA_env
- source CA_env/bin/activate
- pip install .

At this point, the library should be installed together with all its dependencies. Next we need to create a .env with this content:

```LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your_langchain_api_key
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
LANGCHAIN_PROJECT=Tools
GOOGLE_API_KEY=your_google_api_key
GOOGLE_APPLICATION_CREDENTIALS=gemini.json
SEMANTIC_SCHOLAR_KEY=your_semantic_schoolar_api_key
```
fill the missing blocks with your API keys. If you dont have a semantic scholar key, remove the line `SEMANTIC_SCHOLAR_KEY=`

### How to get the keys

**Langchain**. Go to the [langsmith](https://www.langchain.com/langsmith) website and login. Click on settings (bottom left) and create an API key.

**Gemini**. CAMELS agents use both an LLM (gemini-2-flash) and an embedding model (text-embedding-005). To get those working, follow these instructions:

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

**Semantic scholar (optional)**. Go to the [semantic schoolar website](https://www.semanticscholar.org) and sign in/create an account. At the bottom of the page, go to API overview. At the end of the page there is a form to request an API key. Note that unless you made use of semantic schoolar heavily, you dont need an API key.


# Run

Once the code is installed and all the API keys in place
`streamlit run app.py`

# Modifying the code

### CAMELS section

The original text describing CAMELS is located in `Input_Text/CAMELS_section.txt`. Modify that section if you want a different initial description.

### CAMELS papers

The agents are able to identify CAMELS papers for a given query; for instance to see if an idea has been already carried out. The list of CAMELS papers is located in `Input_Text/CAMELS_papers_links.py`. Add any paper you want to the list for the agents to work with them. One the list is updated, go to `CAMELS_Agents` folder and run `python update_db_CAMELS_papers.py` to add those papers to the Chroma database.

### CAMELS coding

The guidelines to use CAMELS data are in `Input_Text/CAMELS_coding.txt`. Add or modify that file for your needs. Take into account that the longer the file, the larger the context and the more expensive the call to the LLM will be.

# Team:

- Francisco Villaescusa-Navarro (Flatiron)
- Boris Bolliet (Cambridge)