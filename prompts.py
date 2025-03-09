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
