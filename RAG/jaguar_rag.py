
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.llms import OpenAI
from langchain_community.vectorstores.jaguar import Jaguar
from langchain_openai import OpenAIEmbeddings


loader = TextLoader("./state_of_the_union.txt")
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=300)
docs = text_splitter.split_documents(documents)

'''
Create a jaguar vector store
This should be done only once
If the store is already created, you do not need to do this.
'''
url = "http://192.168.1.88:8080/fwww/"
embeddings = OpenAIEmbeddings()

pod = "vdb"
store = "langchain_rag_store"
vector_index = "v"
vector_type = "cosine_fraction_float"
vector_dimension = 1536

vectorstore = Jaguar(pod, store, vector_index, 
    vector_type, vector_dimension, url, embeddings
)

vectorstore.login('demouser')

''' create vector on the database
This should be called only once
'''
metadata = "category char(16)"
text_size = 4096
vectorstore.create(metadata, text_size)

# add texts to vectorstore
vectorstore.add_documents(docs)

retriever = vectorstore.as_retriever()
# if use metadata:
#retriever = vectorstore.as_retriever(search_kwargs={"where": "a='123' and b='xyz'"})


template = """You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise.
Question: {question}
Context: {context}
Answer:
"""
prompt = ChatPromptTemplate.from_template(template)

#LLM = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
LLM = ChatOpenAI(model_name="gpt-4", temperature=0)
rag_chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | LLM
    | StrOutputParser()
)

query = "What did the president say about Justice Breyer?"
print(f"Question: {query}\n")

r = rag_chain.invoke(query)
print("Answer:")
print(r)

