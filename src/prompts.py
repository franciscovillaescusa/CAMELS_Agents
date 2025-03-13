from langchain_core.messages import AnyMessage, HumanMessage, SystemMessage, AIMessage


# prompt to write CAMELS section
def write_section_prompt(text):

        return [SystemMessage(content="You are a rewriting expert. Your task is to rewrite the text without changing its content."), HumanMessage(content=f"""Please rewrite the text below without changing its content. The output text should be different to the original one. Please write your response in LaTeX.

Text: {text}""")]


# prompt to improve CAMELS section
def improve_section_prompt(memory, query):

    return [SystemMessage(content="You are a scientific writer. Given the original text, the previous iteration, and the user query, please modify the text accordingly while keeping its content."), HumanMessage(content=f"""Please rewrite the text of the last iteration taking into account the user query. Please write your response in LaTeX.

Text:
{memory}

Query: 
{query}""")]


# prompt for RAG
def RAG_prompt(memory, context, query):
        
        return [SystemMessage(content="You are a research assistant.")]+ memory + [HumanMessage(content=f"""Answer the question given the context. If the context does not contain relevant information, look at previous responses. If you do not know the answer, say that you dont know the answer.

Context: 
{context}

Question:
{query}""")]


# prompt to get title and abstract from a text
def title_abstract_prompt(text):

        return [HumanMessage(content=f"""Given the below text, get the title and the abstract. Return and output like this:

Title='The title of the text' 
Abstract='The abstract of the text'

Text: {text}
""")]


# prompt to get the title and abstract from a pdf extracted text
def title_abstract_from_paper_prompt(text):

        return [SystemMessage(content="You are a research assistant"), HumanMessage(content=f"""Given the text below, get the title and abstract from it. The title appears before the affiliations. The abstract is all the text located between the keywords and the end of the affiliations. If there are no keywords, get the text located between the introduction and the end of the affiliations.

Text: {text}""")]        


# prompt for the coding node
def coding_prompt(query, memory, instructions):

        return [SystemMessage(content="You are a coding assistant. Write code to address the query but take into account the instructions for CAMELS. Briefly explain the code you write.")] + memory + [HumanMessage(content=f"""
CAMELS instructions: {instructions}

query: {query}
""")]
