from parameters import GraphState
from typing import Annotated, Literal
from langchain_core.runnables import RunnableConfig


# This router will direct the LLM to the corresponding node
def general_router(state: GraphState) -> Literal["write_section_node", "CAMELS_papers", "CAMELS_docs", "semantic_search", "standard_llm", "__end__"]:
    
    if   state['option']==1:  return "write_section_node"
    elif state['option']==2:  return "CAMELS_docs"
    elif state['option']==3:  return "CAMELS_papers"
    elif state['option']==4:  return "semantic_search"
    elif state['option']==5:  return "coding_node"
    elif state['option']==6:  return "standard_llm"
    elif state['option']==0:
        print('Bye!')
        return "__end__"
    else:
        print('Wrong option!\n\n')
        return "__end__"


# router controlling where to send the query
def question_router(state: GraphState) -> Literal["CAMELS_docs", "CAMELS_literature", "semantic_search","__end__"]:
    #Literal["option_node", "CAMELS_docs", "CAMELS_literature", "semantic_search","__end__"]:

    if state["query"] in ["END", "end"]:
        #return "option_node"
        return "__end__"
    else:
        if state["option"]==2:
            return "CAMELS_docs"
        elif state['option']==3:
            return "CAMELS_literature"
        elif state["option"]==4:
            return "semantic_search"
        else:
            raise Exception("Wrong option: %d!"%state['option'])



        
