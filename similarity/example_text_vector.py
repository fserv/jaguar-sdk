#!/usr/bin/python3

###########################################################################
##  Example program of Python for text vector search
##  Copyright  DataJaguar Inc
###########################################################################
import jaguarpy, sys, json
from sentence_transformers import SentenceTransformer


### store text data into jaguardb
def storeText(jag, model, text, source):
    sentences = [ text ]
    embeddings = model.encode(sentences, normalize_embeddings=False)
    comma_separated_str = ",".join( [str(x) for x in embeddings[0] ])
    
    istr = "insert into textvec values ('" + comma_separated_str + "','" + text + "','" + source + "')"
    jag.execute( istr )
    return jag.getLastUuid()


### search similar text data from jaguadb 
def searchSimilarTexts(jag, model, queryText, K):
    sentences = [ queryText ]
    embeddings = model.encode(sentences, normalize_embeddings=False)
    comma_separated_str = ",".join( [str(x) for x in embeddings[0] ])
    
    qstr = "select similarity(v, '" + comma_separated_str 
    qstr += "', 'topk=" + str(K) + ",type=cosine_fraction_short')"
    qstr += " from textvec"

    jag.query( qstr )

    jsonstr = ''
    while jag.reply():
        jsonstr = jag.jsonString()

    return jsonstr


def getTextByVID(jag, vid):
    qstr =" select zid from vdb.textvec.v_zid_idx where v='" + vid + "'"
    zid = ''
    jag.query( qstr )
    while jag.reply():
        zid = jag.getValue("zid")

    qstr = "select text from textvec where zid='" + zid + "'"
    jag.query( qstr )
    txt = ''
    while jag.reply():
        txt = jag.getValue("text")

    return txt


def retrieveTopK( jag, model, queryText, K ):
    print("Query: " + queryText )
    json_str = searchSimilarTexts( jag, model, queryText, K )
    json_obj = json.loads(json_str)

    i = 0;
    print("\n")
    print("Retrieved similar texts: ")
    for rec in json_obj:
        d = rec[str(i)]
        print("\n")
        print('Rank: {}'.format(str(i+1)))
        vid = d["vectorid"]
        print('Vector ID: {}'.format(vid) )
        print('Distance: {}' .format(d["distance"]) )
        txt = getTextByVID( jag, vid )
        print('Text: {}'.format( txt) )
        i += 1

    print("\n\n")


''' 
Retrieve topK similar records what also meet the criteria
of the given source (such as 'wiki') 
'''
def retrieveTopKWithCriteria( jag, model, queryText, source, K ):
    print("Query: " + queryText )

    sentences = [ queryText ]
    embeddings = model.encode(sentences, normalize_embeddings=False)
    comma_separated_str = ",".join( [str(x) for x in embeddings[0] ])
    
    qstr = "select similarity(v, '" + comma_separated_str 
    qstr += "', 'topk=" + str(K) + ",type=cosine_fraction_short')"
    qstr += " from textvec"
    qstr += " where source='" + source + "'"

    jag.query( qstr )

    print("\n")
    print("Result: ")
    while jag.reply():
        print('zid={}'.format(jag.getValue("zid")) )
        print('v={}'.format(jag.getValue("v")) )
        print('vectorid={}'.format(jag.getValue("vectorid")) )
        print('rank={}'.format(jag.getValue("rank")) )
        print('distance={}'.format(jag.getValue("distance")) )
        print('source={}'.format(jag.getValue("source")) )
        print('text={}'.format(jag.getValue("text")) )
        print("\n")



'''
A number of texts are first inserted into vector dabatase. Then later a user enters
a query text, the program will find top K (K=5) texts that best match the query text.
'''
def main():

    ### connect to JaguarDB
    jag = jaguarpy.Jaguar()

    host = sys.argv[1]
    port = sys.argv[2]
    apikey = "my-api-key"
    tenant = "my-tenant"
    db = "vdb"

    rc = jag.connect( host, port, apikey, "opt", tenant, db )
    print ("Connected to JaguarDB server" )
    
    ### create store for vector data. Notice that 1024 is the dimension for BAAI/bge-large-en model
    jag.execute("drop store if exists textvec")
    jag.execute("create store textvec ( key: zid uuid, value: v vector(1024, 'cosine_fraction_short'), text char(2048), source char(32) )")
    # scalar index 'v_zid_idx' is created automatically in textvec

    ### use the BAAI/bge-large-en model
    model = SentenceTransformer('BAAI/bge-large-en')
    
    ### store texts into vdb
    text = "Human impact on the environment, or anthropogenic environmental impact, refers to changes to biophysical environments and to ecosystems, biodiversity, and natural resources caused directly or indirectly by humans"
    zuid1 = storeText( jag, model, text, "wiki" )

    text = "a group of people involved in persistent interpersonal relationships, or a large social grouping sharing the same geographical or social territory, typically subject to the same political authority and dominant cultural expectations. Human societies are characterized by patterns of relationships (social relations) between individuals who share a distinctive culture and institutions; a given society may be described as the total of such relationships among its constituent members."
    zuid2 = storeText( jag, model, text, "wiki" )

    text = "In 1768, Astley, a skilled equestrian, began performing exhibitions of trick horse riding in an open field called HaPenny Hatch on the south side of the Thames River, England. In 1770, he hired acrobats, tightrope walkers, jugglers and a clown to fill in the pauses between the equestrian demonstrations and thus chanced on the format which was later named a circus. Performances developed significantly over the next fifty years, with large-scale theatrical battle reenactments becoming a significant feature. "
    zuid3 = storeText( jag, model, text, "google" )

    text = "Astley had a genius for trick riding. He saw that trick riders received the most attention from the crowds in Islington. He had an idea for opening a riding school in London in which he could also conduct shows of acrobatic riding skill. In 1768, Astley performed in an open field in what is now the Waterloo area of London, behind the present site of St Johns Church. Astley added a clown to his shows to amuse the spectators between equestrian sequences, moving to fenced premises just south of Westminster Bridge, where he opened his riding school from 1769 onwards and expanded the content of his shows. He taught riding in the mornings and performed his feats of horsemanship in the afternoons."
    zuid4 = storeText( jag, model, text, "google" )

    text = "After the Amphitheatre was rebuilt again after the third fire, it was said to be very grand.  The external walls were 148 feet long which was larger than anything else at the time in London.  The interior of the Amphitheatre was designed with a proscenium stage surrounded by boxes and galleries for spectators. The general structure of the interior was octagonal. The pit used for the entertainers and riders became a standardised 43 feet in diameter, with the circular enclosure surrounded by a painted four foot barrier. Astley original circus was 62 ft (about 19 m) in diameter, and later he settled it at 42 ft (~13 m), which has been an international standard for circuses since."
    zuid5 = storeText( jag, model, text, "wiki" )


    text = "According to the Big Bang theory, the energy and matter initially present have become less dense as the universe expanded. After an initial accelerated expansion called the inflationary epoch at around 10 to 32 seconds, and the separation of the four known fundamental forces, the universe gradually cooled and continued to expand, allowing the first subatomic particles and simple atoms to form. Dark matter gradually gathered, forming a foam-like structure of filaments and voids under the influence of gravity. Giant clouds of hydrogen and helium were gradually drawn to the places where dark matter was most dense, forming the first galaxies, stars, and everything else seen today."
    zuid6 = storeText( jag, model, text, "imf" )

    text = "By comparison, general relativity did not appear to be as useful, beyond making minor corrections to predictions of Newtonian gravitation theory. It seemed to offer little potential for experimental test, as most of its assertions were on an astronomical scale. Its mathematics seemed difficult and fully understandable only by a small number of people. Around 1960, general relativity became central to physics and astronomy. New mathematical techniques to apply to general relativity streamlined calculations and made its concepts more easily visualized. As astronomical phenomena were discovered, such as quasars (1963), the 3-kelvin microwave background radiation (1965), pulsars (1967), and the first black hole candidates (1981), the theory explained their attributes, and measurement of them further confirmed the theory."
    zuid7 = storeText( jag, model, text, "imf" )

    text = "In astronomy, the magnitude of a gravitational redshift is often expressed as the velocity that would create an equivalent shift through the relativistic Doppler effect. In such units, the 2 ppm sunlight redshift corresponds to a 633 m/s receding velocity, roughly of the same magnitude as convective motions in the sun, thus complicating the measurement. The GPS satellite gravitational blueshift velocity equivalent is less than 0.2 m/s, which is negligible compared to the actual Doppler shift resulting from its orbital velocity."
    zuid8 = storeText( jag, model, text, "wiki" )

    text = "Turn on the sprinkler system. In order to locate the break or leak in the sprinkler system, you need to run water through it. Turn on the sprinkler system to activate the flow of water. Allow the water to run for about 2 minutes before you check the lines. Do this in the daytime, when you will have an easier time spotting the leak. If your sprinkler system is separated into zones, activate the zones one at a time so you can identify the break or leak more easily."
    zuid9 = storeText( jag, model, text, "wiki" )

    text = "Check for water bubbling up from the soil. If you see a pool of water or water coming from the soil, then there is a leak in the sprinkler line buried underneath. Mark the general location of the leak or break so you can identify it when the water is turned off. Place an item like a shovel or a rock on the ground near the leak. Turn off the sprinkler system after you have found the leak. If you have found the signs of a leak and located the region where the line is leaking or broken, turn off the water so you can repair the line. Use the shut-off valve in the control box to stop the flow of water through the system."
    zuid10 = storeText( jag, model, text, "wiki" )

    text = "In fact, Antarctica is such a good spot for meteorite hunters that crews of scientists visit every year, searching for these otherworldly rocks, driving around the surface until they spot a lone dark rock on an otherwise unbroken expanse of white. However, you don not always have to travel to the other side of the world to find a meteorite. Sometimes meteorites will come to you. Keep an eye open for local reports of brilliant fireballs lighting your region sky. Debris from such displays scatters across the ground and sometimes hits structures or vehicles. Watch for information about fireballs in your area on the websites of the American Meteor Society or the International Meteor Organization."
    zuid11 = storeText( jag, model, text, "wiki" )

    text = "Most tornadoes are found in the Great Plains of the central United States an ideal environment for the formation of severe thunderstorms. In this area, known as Tornado Alley, storms are caused when dry cold air moving south from Canada meets warm moist air traveling north from the Gulf of Mexico. Tornadoes can form at any time of year, but most occur in the spring and summer months along with thunderstorms.  May and June are usually the peak months for tornadoes. The Great Plains are conducive to the type of thunderstorms (supercells) that spawn tornadoes. It is in this region that cool, dry air in the upper levels of the atmosphere caps warm, humid surface air. This situation leads to a very unstable atmosphere and the development of severe thunderstorms."
    zuid12 = storeText( jag, model, text, "wiki" )

 

    ### Make a query and get similar texts from database
    queryText = "More recently, that focus has shifted eastward by 400 to 500 miles. In the past decade or so tornadoes have become prevalent in eastern Missouri and Arkansas, western Tennessee and Kentucky, and northern Mississippi and Alabama a new region of concentrated storms. Tornado activity in early 2023 epitomized the trend."
    K = 3;
    retrieveTopK( jag, model, queryText, K )


    ### Make another query and get similar texts from database
    queryText = "Think of designing a landscape for the bare lot surrounding your new home as an adventure in creativity. Perhaps your property needs only a few small, easily doable projects to make it more attractive. Either way, it is important to consider how each change will relate to the big picture. Stand back from time to time to see the entire landscape and how each part fits into it."
    K = 3;
    retrieveTopK( jag, model, queryText, K )


    ### Make a query finding top 5 similar texts and souce is from wiki
    K = 10;
    source = "wiki"
    retrieveTopKWithCriteria( jag, model, queryText, source, K )


    
    ### select from one column only
    print("\n")
    print("select vector for zuid={}" . format(zuid1) )
    jag.query("select vector(v, 'type=cosine_fraction_short') from textvec where zid='"+ zuid1 +"'" )
    while jag.reply():
        print("json ", jag.jsonString() )

    
    jag.close()
    jag = None


if __name__ == "__main__":
    main()
