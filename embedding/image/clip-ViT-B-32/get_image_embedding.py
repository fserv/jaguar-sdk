
## you need "pip install -U jaguardb-http-client"
## and install jaguardb and its http gateway using docker or package

from PIL import Image
from sentence_transformers import SentenceTransformer
from jaguardb_http_client.JaguarHttpClient import JaguarHttpClient



### how to get embedding vector from the model
img_model = SentenceTransformer('clip-ViT-B-32')

## your image here
images = [ Image.open('dicom_viewer_Mrbrain.jpg') ]

embeddings = img_model.encode( images )

comma_sep_str = ",".join( [str(x) for x in embeddings[0] ])
print(comma_sep_str)


## how to interact with jaguardb
url = "http://192.168.1.79:8080/fwww/"

jag = JaguarHttpClient(url)
apikey = "demouser"  ## or your personal API key

## login and get a valid token
token = jag.login(apikey)

## create a store
q = "create store imgvec (v vector(512, 'euclidean_fraction_float'), v:text char(2048), cat char(16), a int)"
jag.get(q, token)

## insert embeddings and text into the store
q = "insert into imgvec values ('" + comma_sep_str + "', 'description or text about this image', 'cat1', '100')"  
jag.post(q, token)


## select similarity from ...
## select similarity  from ... where ...
## refer to user manual for query







