<img src="images/logo.png" alt="CAMELS Agents" width="400" style="display: block; margin: auto;">


AI agents to help working with CAMELS (Cosmology and Astrophysics with MachinE Learning Simulations) data.

# Installation

### Requirements:
You need python 3.10 or above to install CAMELS_agents properly.

### Instructions:
- git clone https://github.com/franciscovillaescusa/CAMELS_Agents.git
- cd CAMELS_Agents
- python -m venv CA_env
- source CA_env/bin/activate
- pip install .

At this point, the library should be installed together with all its dependencies. Next we need two more ingredients:

1. An environment file. Inside CAMELS_Agent, create a .env file and put this content inside it:
```LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
LANGCHAIN_PROJECT=Tools
GROQ_API_KEY=
GOOGLE_API_KEY=
GOOGLE_APPLICATION_CREDENTIALS=gemini.json
SEMANTIC_SCHOLAR_KEY=
```
fill the missing blocks with your API keys.

2. A gemini.json file to use google gemini and embedding model. For this follow these instructions:
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

Once you have complete the above steps you can run the code with
`streamlit run app.py`

### CAMELS section

The original text describing CAMELS is located in `Input_Text/CAMELS_section.txt`. Modify that section if you want a different initial description.

### CAMELS papers

The agents are able to identify CAMELS papers for a given query; for instance to see if an idea has been already carried out. The list of CAMELS papers is located in `Input_Text/CAMELS_papers_links.py`. Add any paper you want to the list for the agents to work with them. One the list is updated, go to `CAMELS_Agents` folder and run `python update_db_CAMELS_papers.py` to add those papers to the Chroma database.

### CAMELS coding

The guidelines to use CAMELS data are in `Input_Text/CAMELS_coding.txt`. Add or modify that file for your needs. Take into account that the longer the file, the larger the context and the more expensive the call to the LLM will be.

## Team:

- Francisco Villaescusa-Navarro (Flatiron)
- Boris Bolliet (Cambridge)