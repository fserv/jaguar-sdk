from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores.jaguar import Jaguar
from langchain_huggingface import HuggingFaceEmbeddings
import re, sys, requests


### Find relevant text from vector store and send to LLM
def ask(vectorstore, ollamaurl, context, prompt):
    print(f"Question: {prompt}")
    similar_docs = vectorstore.similarity_search(query=prompt, k=3 )
    raginfo = " ".join(doc.page_content for doc in similar_docs)

    if "-a" in sys.argv:
        i = 1
        for doc in similar_docs:
            print(f"Augment {i}: {doc.page_content}")
            i += 1
    
    payload = {
        "model": "deepseek-r1:1.5b",
        "prompt": raginfo + ' ' + context + ' ' + prompt,
        "stream": False 
    }
    
    # Send the request
    response = requests.post(ollamaurl, json=payload)
    
    # Print response
    if response.status_code == 200:
        print("DeepSeek-R1 Response:")
        reply = response.json()['response']
        ### remove think data: 
        reply = re.sub(r"<think>.*?</think>", "", reply, flags=re.DOTALL)
        print(reply)
    else:
        print(f"Error {response.status_code}: {response.text}")

    print("\n")


def main():

    ######### prepare to input text file and split it into chunks ########
    loader = TextLoader("./milk_price.txt")
    documents = loader.load()
    text_splitter = CharacterTextSplitter( separator='',  chunk_size=200, chunk_overlap=80)
    docs = text_splitter.split_documents(documents)

    ########## login to jaguardb with a API key #####################
    url='http://192.168.1.88:8080/fwww/'
    url='http://localhost:8080/fwww/'
    jaguar_api_key='demouser'

    embeddings = HuggingFaceEmbeddings( model_name="BAAI/bge-large-zh")

    pod = "vdb"
    store = "fish_store"
    vector_index = "v"
    vector_type = "cosine_fraction_float"
    vector_dimension = 1536

    vectorstore = Jaguar(pod, store, vector_index,
        vector_type, vector_dimension, url, embeddings
    )

    vectorstore.login(jaguar_api_key)

    ### create vector on the database This should be called only once  ###
    metadata = "category char(16)"
    text_size = 300
    vectorstore.create(metadata, text_size)

    ### ad the chunks (docs) into jaguar vector store ###
    vectorstore.add_documents(docs)

    ### Ollama's local API endpoint
    OLLAMA_URL = "http://localhost:11434/api/generate"


    ### instruction to LLM
    context = """
    You are a helpful assistant. The previous information is important.
    Now answer the following question, without hallucination, giving answer to the specific question:
    """

    ### Your prompt/question
    prompt = "进口奶粉的价格是什么"
    ask(vectorstore, OLLAMA_URL, context, prompt)


    ### ask another question
    prompt = "国产奶粉的价格是什么"
    ask(vectorstore, OLLAMA_URL, context, prompt)

    
    if "-d" in sys.argv:
        vectorstore.drop()

    vectorstore.logout()


if __name__ == "__main__":
    main()
