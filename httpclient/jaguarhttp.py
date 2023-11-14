#######################################################################################
##
##  This example demonstrates:
##
##       1. create a vector store
##       2. read text files and create embeddings of the files
##       3. add the embeddings,  upload the files, and save the texts into the store
##       4. search similar texts to a query text
##
##  Input data files in data directory:  
##
##        data/0_data.txt
##        data/1_data.txt
##
##  Query text file:
##        data/query.txt
##
##
##  Requires: pip install jaguardb-http-client
##
##  Requires: install and set the http gateway using the fwww_3.3.7.tar.gz
##
##  Refer   http://github.com/fserv/jaguar-sdk
##
#######################################################################################

import requests, json, sys
from sentence_transformers import SentenceTransformer
from jaguardb.JaguarHttpClient import JaguarHttpClient


def loadAndSearch():
    ### replace with your own http server IP address
    url = "http://192.168.1.88:8080/fwww/"

    jag = JaguarHttpClient( url )

    ### use hard-coded API key or read it from JAGUAR_API_KEY environment variale
    ### or read it from file  $HOME/.jagrc
    ### apikey = 'my_api_key_hard_coded_here'
    apikey = jag.getApikey()

    ### login to get an authenticated session token
    token = jag.login(apikey)
    if token == '':
        print("Error login")
        exit(1)
    print(f"session token of {apikey} is {token}")


    q = "drop store vdb.mystore"
    response = jag.get(q, token)
    print(response.text)
    print(f"drop store {response.text}")

    q = "create store vdb.mystore ( key: zid zuid, value: v vector(1024, 'cosine_fraction_float'), v:f file, v:t char(1024) )"
    response = jag.get(q, token)
    print(f"create store {response.text}")

    ### text embedding model to be used
    model = SentenceTransformer('BAAI/bge-large-en')

    mdir = 'data'

    for i in range(0, 2):
        fpath = mdir + "/" + str(i) + '_data.txt'

        f = open(fpath, "r")
        text = f.read();
        text = text.strip()
        f.close()

        sentences = [ text ]
        embeddings = model.encode(sentences, normalize_embeddings=False)
        comma_sepstr = ",".join( [str(x) for x in embeddings[0] ])

        ### upload file for v:f which is at column 2  (v:f column)
        rc = jag.postFile(token, fpath, 2 )

        q = "insert into vdb.mystore values ('" + comma_sepstr + "', '" + fpath + "', '" + text + "' )"
        response = jag.post(q, token, True)

    ### done loading all 100 text files


    ### prepare query text and make a query for similar texts
    qpath = 'data/query.txt'
    f = open(qpath, "r")
    qt = f.read();
    qt = qt.strip()
    f.close()

    sentences = [ qt ]
    embeddings = model.encode(sentences, normalize_embeddings=False)
    comma_sepstr = ",".join( [str(x) for x in embeddings[0] ])

    q = "select similarity(v, '" + comma_sepstr + "', 'topk=1, type=cosine_fraction_float, with_score=yes, with_text=yes') "
    q += " from vdb.mystore"
    response = jag.post(q, token)

    jd = json.loads(response.text)

    print("\n");
    print(f"query: {qt}")
    print("\n");

    for i in range(0, len(jd)):
        fd= json.loads( jd[i] )
        field = fd['field']
        vid = fd['vectorid']
        zid = fd['zid']
        score = fd['score']
        dist = fd['distance']
        text = fd['text']

        q = "select v:f as vf from vdb.mystore where zid='" + zid + "'"
        response = jag.get(q, token)
        j1 = json.loads( response.text )
        j2 = json.loads( j1[0] )
        filename = j2['vf']

        print(f"zid=[{zid}]  distance=[{dist}] score=[{score}] filename={filename} text={text}")


    jag.logout(token)


if __name__ == "__main__":
    loadAndSearch()
    
