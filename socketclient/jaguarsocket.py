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
from jaguardb.JaguarSocketClient import JaguarSocketClient


def loadAndSearch():

    jag = JaguarSocketClient()

    ### use hard-coded API key or read it from JAGUAR_API_KEY environment variale
    ### or read it from file  $HOME/.jagrc
    ### apikey = 'my_api_key_hard_coded_here'
    apikey = jag.getApikey()

    jag.connect(apikey, '127.0.0.1', 8888, 'vdb' )

    q = "drop store vdb.mystore"
    jag.execute(q)

    q = "create store vdb.mystore ( key: zid zuid, value: v vector(1024, 'cosine_fraction_float'), v:f file, v:t char(1024) )"
    jag.execute(q)

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

        q = "insert into vdb.mystore values ('" + comma_sepstr + "', '" + fpath + "', '" + text + "' )"
        jag.execute(q)

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

    jag.query(q)

    jag.fetch();

    jd = json.loads(jag.json())

    print(f"query: {qt}")
    print("\n")

    for i in range(0, len(jd)):
        istr = str(i)
        fds= jd[i]
        fd = fds[istr]

        field = fd['field']
        vid = fd['vectorid']
        zid = fd['zid']
        score = fd['score']
        dist = fd['distance']
        text = fd['text']

        q = "select v:f as vf from vdb.mystore where zid='" + zid + "'"
        jag.query(q)
        jag.fetch()
        j = json.loads( jag.json() )
        filename = j['vf']

        print(f"zid=[{zid}]  distance=[{dist}] score=[{score}] filename={filename} text={text} ")

    jag.close()


if __name__ == "__main__":
    loadAndSearch()
    
