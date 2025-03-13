import os
from langgraph.graph import START, StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.checkpoint.sqlite import SqliteSaver

from src.prompts import *
from src.parameters import GraphState, initial_graph_state
from src.writing import write_section_node
from src.routers import general_router
from src.llms import standard_llm
from src.CAMELS_documentation import *
from src.CAMELS_papers import *
from src.literature import semantic_search
from src.coding import coding_node
    

# Define the graph
builder = StateGraph(GraphState)

# Define nodes: these do the work
builder.add_node("write_section_node", write_section_node)
builder.add_node("CAMELS_papers", CAMELS_papers)
builder.add_node("standard_llm", standard_llm)
builder.add_node("CAMELS_docs",  CAMELS_docs)
builder.add_node("semantic_search", semantic_search)
builder.add_node("coding_node", coding_node)

# Define edges: these determine how the control flow moves
builder.add_conditional_edges(START, general_router)
builder.add_edge("write_section_node", END)
builder.add_edge("CAMELS_papers", END)
builder.add_edge("CAMELS_docs", END)
builder.add_edge("semantic_search", END)
builder.add_edge("standard_llm", END)
builder.add_edge("coding_node", END)

# compile graph
memory = MemorySaver()
#memory = SqliteSaver(conn)
graph = builder.compile(checkpointer=memory)

"""
# make plot of the graph
graph_image = graph.get_graph(xray=True).draw_mermaid_png()
with open("graph_diagram.png", "wb") as f:
    f.write(graph_image)

# call the graph
result = graph.invoke(initial_graph_state, config)
"""

