
from PIL import Image
from sentence_transformers import SentenceTransformer


img_model = SentenceTransformer('clip-ViT-B-32')

images = [ Image.open('dicom_viewer_Mrbrain.jpg') ]

embeddings = img_model.encode( images )

comma_sep_str = ",".join( [str(x) for x in embeddings[0] ])
print(comma_sep_str)

