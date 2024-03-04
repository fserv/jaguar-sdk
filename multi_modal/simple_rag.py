
################### packages requires ########################################
## First you need to do:
##
##    python3 -m venv simple_rag_venv   # only once
##    source  simple_rag_venv/bin/activate
##
##    pip install -U Pillow
##    pip install -U pyopenssl cryptography
##    pip install -U sentence-transformers
##    pip install -U jaguardb-http-client
##
## and install jaguardb and its http gateway using docker or package
##
##  How run this program:
##
##      python3 simple_rag.py 'http://127.0.0.1:8080/fwww/'
##      (replace 127.0.0.1 with your IP address if http server is running on a different host)
##
##############################################################################

import os, sys, json
from PIL import Image
from sentence_transformers import SentenceTransformer
from jaguardb_http_client.JaguarHttpClient import JaguarHttpClient


"""
create a vector store
"""
def createStore(jag):
    schema = {
        "pod": "vdb",
        "store": "myragstore",
        "columns": [
            {"name": "imgvec", "type": "vector", "dim":"512", "dist":"euclidean", "input":"fraction", "quantization":"float"},
            {"name": "textvec", "type": "vector", "dim":"1024", "dist":"euclidean", "input":"fraction", "quantization":"float"},
            {"name": "imgvec:img", "type": "file" },
            {"name": "textvec:text", "type": "str", "size": "2048"},
            {"name": "tms", "type": "datetimesec" },
            {"name": "itemid", "type": "int" },
            {"name": "sellerid", "type": "bigint" },
        ]
    }

    jag.dropStore("vdb", "myragstore")
    jag.createStore( schema )


"""
Load a collection to vector store
"""
def loadData(jag, img_model, text_model, image_file, text, itemid, sellerid):
    f = Image.open(image_file)
    images = [f]
    img_embeddings = img_model.encode( images, normalize_embeddings=True )
    f.close()
    img_embeddings_vec = img_embeddings[0]
    
    #print(f"img_embeddings={img_embeddings}")

    sentences = [ text ]
    text_embeddings = text_model.encode(sentences, normalize_embeddings=True)
    text_embeddings_vec = text_embeddings[0]
    #print(f"text_embeddings={text_embeddings}")


    files = [{"filepath": image_file, "position": 3} ]
    tensors = [img_embeddings_vec, text_embeddings_vec ]
    scalars = [image_file, text, '2024-04-09 11:21:32', itemid, sellerid]
    zid = jag.add("vdb", "myragstore", files, tensors, scalars )
    print(f"insert zid={zid}")


"""
Search data by text
"""
def searchByText( jag, text ):
    sentences = [ text ]
    text_embeddings = text_model.encode(sentences, normalize_embeddings=True)
    text_embeddings_vec = text_embeddings[0]
    metadatas = ['sellerid', 'itemid', 'tms', 'imgvec:img']
    docs = jag.search( "vdb", "myragstore", "textvec", "euclidean_fraction_float", text_embeddings_vec, topk=3, metadatas=metadatas )
    return docs

"""
Search data by image
"""
def searchByImage( jag, image_file ):
    f = Image.open(image_file)
    images = [f]
    img_embeddings = img_model.encode( images, normalize_embeddings=True )
    f.close()
    img_embeddings_vec = img_embeddings[0]
    metadatas = ['sellerid', 'itemid', 'tms', 'imgvec:img', 'textvec:text' ]
    docs = jag.search( "vdb", "myragstore", "imgvec", "euclidean_fraction_float", img_embeddings_vec, topk=3, metadatas=metadatas )
    return docs


if __name__ == "__main__":

    ### pass http server URL as first argument
    if len(sys.argv) < 2:
        print(f"Usage:  python3 {sys.argv[0]}  <httpUrl>")
        print(f"Example:  python3 {sys.argv[0]}  'http://127.0.0.1:8080/fwww/'")
        exit(1)

    url = sys.argv[1]

    ### get a jaguar http client object and login
    jag = JaguarHttpClient(url)
    apikey = "demouser"
    token = jag.login(apikey)
    #print(f"got token={token}")


    ### get image and text embedding modles
    img_model = SentenceTransformer('clip-ViT-B-32')       # dim 512
    text_model = SentenceTransformer('BAAI/bge-large-en')  # dim 1024


    ### create a vector store
    createStore(jag)


    ### add some collections to the vector store
    img_file = "./test1.jpg"
    text = "a cute kitten"
    itemid = "105"
    sellerid = "20348"
    loadData(jag, img_model, text_model, img_file, text, itemid, sellerid)

    img_file = "./test2.jpg"
    text = "a young puppy"
    itemid = "107"
    sellerid = "20348"
    loadData(jag, img_model, text_model, img_file, text, itemid, sellerid)

    img_file = "./test3.jpg"
    text = "a big dog "
    itemid = "114"
    sellerid = "20348"
    loadData(jag, img_model, text_model, img_file, text, itemid, sellerid)

    img_file = "./bike1.jpg"
    text = "motorbike"
    itemid = "210"
    sellerid = "20348"
    loadData(jag, img_model, text_model, img_file, text, itemid, sellerid)

    img_file = "./bike2.jpg"
    text = "motor bike"
    itemid = "213"
    sellerid = "20348"
    loadData(jag, img_model, text_model, img_file, text, itemid, sellerid)


    ### search data by text
    tuples = searchByText(jag, "big dog" )
    print(f"searchByText big dog tuples.size={len(tuples)}")
    for tup in tuples:
        text = tup[0]
        metadata = tup[1]
        score = tup[2]
        zid = metadata['zid']

        print(f"text={text}")
        print(f"metadata={metadata}")
        print(f"score={score}")
        print(f"zid={zid}")

        imgurl = jag.getFileUrl(jag.token, "vdb", "myragstore", "imgvec:img", zid)
        print(f"image_url={imgurl}")
        print("\n")


    ### search data by image
    query_img = "./bike3.jpg"
    tuples = searchByImage(jag, query_img )
    print(f"searchByImage {query_img} tuples.size={len(tuples)}")
    for tup in tuples:
        text = tup[0]
        metadata = tup[1]
        score = tup[2]
        zid = metadata['zid']

        if len(text) < 1:
            text = metadata['textvec:text']

        print(f"text={text}")
        print(f"metadata={metadata}")
        print(f"score={score}")
        print(f"zid={zid}")

        imgurl = jag.getFileUrl(jag.token, "vdb", "myragstore", "imgvec:img", zid)
        print(f"image_url={imgurl}")
        print("\n")

        
    
    ### log out to clean up resources and invalidate Image URLs
    # jag.logout( token )
