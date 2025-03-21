from langchain.document_loaders import Docx2txtLoader 
from langchain.text_splitter import CharacterTextSplitter 
from langchain.vectorstores import Chroma 
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.agents import tool
# 1. Load Documents
loader = Docx2txtLoader ("D:/finalYr/Agentic-Python/DomainData/domaindata.docx")
documents = loader.load()

text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
texts = text_splitter.split_documents(documents)


embeddings=OpenAIEmbeddings(openai_api_key="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")



persist_directory="D:/finalYr/Agentic-Python/chroma_db"
vector_store=Chroma.from_documents(texts,embeddings,persist_directory=persist_directory)
vector_store.persist()



@tool
def policyRetriever(query:str):
    """
    This tool is designed to retrieve information specifically about policies, such as terms and conditions, 
    shipping policies, refund information, and other related details. It should ONLY be used when the question 
    is directly related to these topics. 

    Answer general knowledge questions by yourself. Do NOT use this tool for general knowledge, 
    common sense reasoning, or questions unrelated to the specific domain. Instead of saying NOT PRESENT 
    in the knowledge base, answer it with common sense and general knowledge.

    IMPORTANT INSTRUCTIONS FOR THE LLM:
    - Use this tool by providing a query string that describes the specific policy information needed.
    - Do NOT use this tool for general knowledge or unrelated questions.

    Args:
        query (str): A query string to search in the policy knowledge base.

    Returns:
        str: A message indicating the result of the search.
    """

    results = vector_store.similarity_search(query,k=5)
    retrieveData = [result.page_content for result in results]

    return retrieveData