# Use this script to create (or update) a database that contains the abstracts of the CAMELS papers. Each paper also includes the title, year, and link of the paper. To update the database with a new paper, just add the url link to the pdf to it. The code will go through all papers but papers already in the database will be discarded.
import sys,os,time,re
import requests
import pymupdf, pymupdf4llm
from langchain_core.messages import HumanMessage
from langchain_core.documents import Document
from prompts import title_abstract_prompt, title_abstract_from_paper_prompt
from llms import llm, llm2, embeddings
from database import get_db_CAMELS_papers
sys.path.append("../Input_Text")
from CAMELS_paper_links import links


def clean_sentence(sentence):
    """Removes unwanted characters from the sentence."""
    return sentence.replace("\n", "").replace("```", "")

def clean_llm_response(abstract):
    """Cleans the LLM response and extracts title and abstract."""
    response = llm2.invoke(title_abstract_prompt(abstract.content)).content
    response = clean_sentence(response)

    title    = re.search(r"Title='(.*?)'",    response)
    abstract = re.search(r"Abstract='(.*?)'", response)

    return title.group(1) if title else None, abstract.group(1) if abstract else None

def process_document(link, pages):
    """get the text from the paper"""
    response = requests.get(link, timeout=60)
    doc = pymupdf.Document(stream=response.content)
    return pymupdf4llm.to_markdown(doc, pages=pages)

def document_already_exists(link, existing_links):
    """returns True if link is in existing_links, otherwise returns False"""
    return link in existing_links

def prompt_for_correction(text):
    """Prompts the user for correcting title and abstract if necessary."""
    while True:
        print(f'Extracted Text:\n{text}')
        new_prompt = input("Provide a refined prompt for better extraction: ")
        prompt = [HumanMessage(content=f"{new_prompt} Text: {text}")]
        abstract = llm.invoke(prompt)
        title, abstract = clean_llm_response(abstract)
        print(f'Title: {title}\nAbstract: {abstract}')
        if input("Is this correct? (y/n): ") == 'y':
            return title, abstract

def main():
    db = get_db_CAMELS_papers()
    existing_links = [metadata['link'] for metadata in db.get().get('metadatas', [])]
    print(f"The database contains {len(existing_links)} papers")

    # do a loop over all papers in the file
    for link in links:

        # check if they are in the database already
        if document_already_exists(link, existing_links):
            continue

        print(f'{link} is new')

        if link in ['https://arxiv.org/pdf/2201.04142', 'https://arxiv.org/pdf/2201.01300',
                    'https://arxiv.org/pdf/2302.14101', 'https://arxiv.org/pdf/2310.04499',
                    'https://arxiv.org/pdf/2310.15234', 'https://arxiv.org/pdf/2311.01588',
                    'https://arxiv.org/pdf/2502.06954']:
            pages = [0, 1]
        else:
            pages = [0]

        text = process_document(link, pages)
        title, abstract = clean_llm_response(llm2.invoke(title_abstract_from_paper_prompt(text)))
        print(f"Title: {title}\nAbstract: {abstract}")

        # check if the extraction was succesful
        if not title or not abstract or input("Is the extraction correct? (y/n): ")=='n':
            title, abstract = prompt_for_correction(text)

        doc = Document(page_content=abstract,
                       metadata={"link": link, "year": "20" + link[-10:-8], "title": title})
        db.add_documents([doc])
        print('Paper added to the database')

        #time.sleep(10) #add this if you get problems with the LLM making too many calls

if __name__ == "__main__":
    main()

        
#num_papers_db = db._collection.count()
#print("The database contains %d papers"%num_papers_db)

# get the content in the database
#papers_db = db.get()

# get the links of the papers in the database
#paper_links = []
#for i in range(num_papers_db):
#    paper_links.append(papers_db["metadatas"][i]['link'])

"""
# do a loop over the different papers
for i,link in enumerate(links):
    
    # open the paper and read its first pages
    r    = requests.get(link)
    data = r.content
    doc  = pymupdf.Document(stream=data)
    if link in ['https://arxiv.org/pdf/2201.04142', 'https://arxiv.org/pdf/2201.01300',
                'https://arxiv.org/pdf/2302.14101', 'https://arxiv.org/pdf/2310.04499',
                'https://arxiv.org/pdf/2310.15234', 'https://arxiv.org/pdf/2311.01588',
    ]:
        text = pymupdf4llm.to_markdown(doc, pages=[0,1])
    else:
        text = pymupdf4llm.to_markdown(doc, pages=[0])


    # get the title and the abstract from the read pages
    PROMPT1 = title_abstract_from_paper_prompt(text)
    abstract = llm2.invoke(PROMPT1)
    Title, Abstract = clean_llm_response(abstract)

    print('###################################################################')
    print(text)
    print('Title: %s'%Title)
    print('Abstract: %s'%Abstract)
    correct = input("Does this looks correct? (y/n)")
    print('###################################################################')

    # in case it doesnt work, make a new call to the LLM with a better prompt
    while correct=='n':
        new_prompt = input("Lets call the LLM again. Please write a new prompt that will get the correct title and abstract. For instance this. Extract the title and the abstract from the text. The abstract start with Abstract and ends with better models for the future.>> ")
        PROMPT3 = [HumanMessage(content=f"{new_prompt} Text: {text}")]
        abstract = llm.invoke(PROMPT3)
        Title, Abstract = clean_llm_response(abstract)
        print('Title: %s'%Title)
        print('Abstract: %s'%Abstract)
        correct = input("Does this looks correct? (y/n)")
"""
    













    

    
# If you need to delete papers from the database, do this
"""
# initialize the database
db = Chroma(embedding_function=embeddings,
            collection_name=collection_name, 
            persist_directory=persist_directory)

# to know the ids of the papers
for i in [-5, -4, -3, -2, -1]:
    print('Title: %s'%papers_db['metadatas'][i]['title'])
    print('Abstract: %s'%papers_db['documents'][i])
    print('id: %s\n'%papers_db['ids'][i])

# delete the papers
db.delete(['1c202ba4-7eac-4b73-a74d-b70964b76322', '62ae47f2-30d3-4748-b106-8239a26badd8'])
"""

#retriever = db.as_retriever(search_type="similarity", search_kwargs={"k":1})
#retriever = db.as_retriever()

# example of how to retrieve documents
"""
results = db.similarity_search_with_score("Papers that study the displacement of gas due to feedback processes.", k=10)
for doc, score in results:
    print(score)
    print(doc.metadata["title"])
    print("")

#for i in range(10):
#    print(results[i],'\n')
"""
