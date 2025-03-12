from parameters import GraphState
from langchain_core.runnables import RunnableConfig
from database import get_db_CAMELS_papers
from langchain_core.messages import AnyMessage, HumanMessage, SystemMessage, AIMessage
from pydantic import BaseModel, Field
from llms import get_llm
import streamlit as st

# class for the model response
class response(BaseModel):
    answer: str = Field(description="Answer to the query. Can be yes, Yes, no or No")
    justification: str = Field(description="The justification of the answer")

    
# This node checks the retrieved papers and see if they are good given the query
def CAMELS_papers(state: GraphState, config: RunnableConfig):

    # get the LLM model
    model = get_llm(state)
    
    bad_matches, good_matches  = [], ["**Relevant papers:**\n"]
        
    # get the k papers whose abstract match the query more closely
    db_papers = get_db_CAMELS_papers()
    results = db_papers.similarity_search_with_score(state["query"], k=10)
    st.session_state.messages.append({"role": "user", "content": state["query"],
                                      "type":"md"})

    # do a loop over the different papers found
    for doc, score in results:

        abstract = doc.page_content

        PROMPT = [SystemMessage(content="You are a research assistant."), HumanMessage(content=f"""Given the query and the abstract, determine if the abstract is a good match for the query. Reply with either yes or no and provide a justificiation for the answer.
Query: {state['query']}
Abstract: {abstract}
""")]

        # Invoke LLM
        try:
            answer = model.with_structured_output(response).invoke(PROMPT)
        except Exception as e:
            st.error(f"Error during LLM invocation: {e}")
            continue

        # Format the paper's response
        paper_text = f"""
**Paper title:** {doc.metadata['title']}
**Paper link:** {doc.metadata['link']}
**Score similarity:** {score:.3f}
**Justification:** {answer.justification}
        """

        # Classify as a good or bad match
        if answer.answer.lower()=='yes':
            good_matches.append(paper_text)
        else:
            bad_matches.append(paper_text)

    # Combine final response text
    response_text = "".join(good_matches)

    if bad_matches:
        response_text += "\n___\n**Other papers found by cosine similarity with the query:**"
        response_text += "\n".join(bad_matches)

    response_text += "\n___"

    # Output to Streamlit or console
    if state["streamlit"]:
        st.session_state.messages.append({"role": "assistant", "content": response_text,
                                          "type":"md"})
    else:
        print(response_text)

        
