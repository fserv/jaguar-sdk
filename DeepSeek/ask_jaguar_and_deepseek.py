from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores.jaguar import Jaguar

import re, sys, requests

### Find relevant text from vector store and send to LLM
def ask(vectorstore, ollamaurl, context, prompt):
    similar_docs = vectorstore.similarity_search(query=prompt, k=3 )
    raginfo = " ".join(doc.page_content for doc in similar_docs)

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
        ### remove think data: reply = re.sub(r"<think>.*?</think>", "", reply, flags=re.DOTALL)
        print(reply)
    else:
        print(f"Error {response.status_code}: {response.text}")



def main():

    ######### prepare to input text file and split it into chunks ########
    loader = TextLoader("./all_about_fish.txt")
    documents = loader.load()
    text_splitter = CharacterTextSplitter(separator=" ", chunk_size=500, chunk_overlap=20)
    docs = text_splitter.split_documents(documents)

    ########## login to jaguardb with a API key #####################
    url='http://192.168.1.88:8080/fwww/'
    jaguar_api_key='demouser'
    embeddings = HuggingFaceEmbeddings( model_name="BAAI/bge-large-en")

    pod = "vdb"
    store = "fish_store"
    vector_index = "v"
    vector_type = "cosine_fraction_float"
    vector_dimension = 1024

    vectorstore = Jaguar(pod, store, vector_index,
        vector_type, vector_dimension, url, embeddings
    )

    vectorstore.login(jaguar_api_key)

    ### create vector on the database This should be called only once  ###
    metadata = "category char(16)"
    text_size = 800
    vectorstore.create(metadata, text_size)

    ### ad the chunks (docs) into jaguar vector store ###
    vectorstore.add_documents(docs)

    ### Ollama's local API endpoint
    OLLAMA_URL = "http://localhost:11434/api/generate"

    ### Instructions to LLM
    context = """
    You are a helpful assistant. The following information is important:
    - small salmon weigh 3-5 pounds. large salmon weigh 20-50 pounds.
    - they eat shrimp, squid, krill, small fish, insects
    - Salmon are opportunistic carnivores — they eat what’s available and abundant in their environment.
    
    Now answer the following question, without hallucination, not showing your think process:
    """

    ### Your prompt/question
    prompt = "Explain how much food does a salmon fish eat on average every day in simple terms."
    ask(vectorstore, OLLAMA_URL, context, prompt)
    
    if "-d" in sys.argv:
        vectorstore.drop()

    vectorstore.logout()


if __name__ == "__main__":
    main()
