#!/usr/bin/python3

###########################################################################
##  Example program of Python for text vector search
##  Copyright  DataJaguar Inc
###########################################################################
import jaguarpy, sys, json
from sentence_transformers import SentenceTransformer


### store text data into jaguardb
def storeText(jag, model, text, source):
    ### important:  escape single quotes in text fields
    text = text.replace('\'', '\\\'')
    sentences = [ text ]
    embeddings = model.encode(sentences, normalize_embeddings=False)
    comma_sep_str = ",".join( [str(x) for x in embeddings[0] ])
    
    istr = "insert into vecanomaly values ('" + comma_sep_str + "','" + text + "','" + source + "')"
    print("store vector ", comma_sep_str[0:80], flush=True )

    rc = jag.execute( istr )
    print("execute rc=", str(rc),  flush=True )

    zuid = jag.getLastUuid()
    zuids = "zuid=[" + zuid + "]\n"
    print( zuids, flush=True);
    return zuid



''' Test anomalous checks
    Test several query texts to see if they are anomalous
'''
def testAnomalous( jag, model ):

    keys = "euclidean_whole_float" 
    act = "[0.5:70;1.5:40;2:30]"

    ### select anomalous on one input
    queryText = "Come on-a my house my house, I’m gonna give you candy Come on-a my house, my house, I’m gonna give a you Apple a plum and apricot-a too eh Come on-a my house, my house a come on Come on-a my house, my house a come on Come on-a my house, my house I’m gonna give a you Figs and dates and grapes and cakes eh";
    sentences = [ queryText ]
    embeddings = model.encode(sentences, normalize_embeddings=False)
    comma_sep_str = ",".join( [str(x) for x in embeddings[0] ])
    print("\n")
    qs = "select anomalous(v, '" + comma_sep_str + "','type=" + keys + ", activation=" + act + "') from vecanomaly" 
    print(qs[0:80])

    jag.query( qs )
    while jag.reply():
        print("json ", jag.jsonString(), flush=True )


    ### select anomalous on numbers
    queryText = "0.26842403,-0.041490164,-0.052837625,0.15613128,-0.057708368,0.10935854,-0.5772294,-0.05099324,1.1001052,-0.23332986,0.5389165,-0.62118155,0.007173604,-0.7151222,-0.46485767,0.49478775,-0.69252056,-0.4307537,-0.22987624,0.9125928,-0.14547576,0.15414718,-0.6777878,-0.6599603,-0.60746217,0.84682155,-0.39576137,0.4193497,1.2880856,0.33061382,0.014627328,-1.0987662,0.13712737,-0.9673059,-0.08241789,-0.13093247,0.55679363,-0.4436744,-0.77715003,-0.13347104,-0.6352019,-0.9985955,0.612718,-0.3811176,-0.4161589,0.046903767,-0.2572114,-1.1586484,0.20213008,-0.628561,0.25839296,-0.47818908,0.83333755,-0.19583963,0.34774593,-0.43985498,-0.48325366,-0.30640793,-0.54267657,0.70638794,0.40787196,-0.4816036,0.01636909,-0.83245915,-0.05320356,-0.027706,0.21005046,-0.3911064,0.26014695,-0.23126595,0.18627763,0.29366082,-0.9498488,-0.11696608,-0.016379572,0.06471612,0.20127673,-0.18588206,-0.26216322,-0.045146327,0.47625658,0.22071223,0.38985547,0.19636953,-1.2062674,-0.6959479,0.010863954,0.030326942,0.49587137,0.044979207,0.45761055,0.9291147,-0.12311875,-0.654688,0.6929925"
    sentences = [ queryText ]
    embeddings = model.encode(sentences, normalize_embeddings=False)
    comma_sep_str = ",".join( [str(x) for x in embeddings[0] ])
    print("\n")
    qs = "select anomalous(v, '" + comma_sep_str + "','type=" + keys + ", activation=" + act + "') from vecanomaly" 
    print(qs[0:80])

    jag.query( qs )
    while jag.reply():
        print("json ", jag.jsonString(), flush=True )


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
    vectordb = "vdb"

    rc = jag.connect( host, port, apikey, vectordb )
    print ("Connected to JaguarDB server {} {}" .format(host, port), flush=True )
    
    ### create store for vector data. Notice that 1024 is the dimension for BAAI/bge-large-en model
    jag.execute("drop store if exists vecanomaly")
    jag.execute("create store vecanomaly ( key: zid zuid, value: v vector(1024, 'euclidean_whole_float'), text char(2048), source char(32) )")

    ### use the BAAI/bge-large-en model
    model = SentenceTransformer('BAAI/bge-large-en')
    
    
    ### store texts into vectordb
    text = "Come on-a my house my house, I’m gonna give you candy Come on-a my house, my house, I’m gonna give a you Apple a plum and apricot-a too eh Come on-a my house, my house a come on Come on-a my house, my house a come on Come on-a my house, my house I’m gonna give a you Figs and dates and grapes and cakes eh";
    zuid1 = storeText( jag, model, text, "wiki" )

    text = "Because of you Because of you, There's a song in my heart. Because of you, My romance had its start. Because of you, The sun will shine. The moon and stars will say you're mine, Forever and never to part."
    zuid2 = storeText( jag, model, text, "wiki" )

    text = "See the pyramids along the Nile Watch the sun rise on a tropic isle Just remember, darling, all the while You belong to me.  See the marketplace in old Algiers Send me photographs and souvenirs But remember when a dream appears You belong to me."
    zuid3 = storeText( jag, model, text, "google" )

    text = "They're not making the skies as blue this year –  wish you were here As blue as they used to when you were near –  wish you were here And the mornings don't seem as new Brand-new as they did with you Wish you were here, wish you were here,  wish you were here"
    zuid4 = storeText( jag, model, text, "google" )

    text = "Now the time has come to part, the time for weeping.  Vaya con Dios my darling, May God be with you my love.  Wherever you may be, I'll be beside you, Although you're many million dreams away. Each night I'll say a prayer, a prayer to guide you To hasten every lonely hour of every lonely day. Now the dawn is breaking through a gray tomorrow, But the memories we share are there to borrow."
    zuid5 = storeText( jag, model, text, "wiki" )


    text = "Wherever you may be I'll be beside you, Although you're many million dreams away, Each night I'll say a prayer, a prayer to guide you To hasten every lonely hour of every lonely day.  Now the dawn is breaking through a gray tomorrow, But the memories we share are there to borrow, Vaya con Dios, my darling"
    zuid6 = storeText( jag, model, text, "imf" )

    text = "Whenever we kiss I worry and wonder Your lips may be near But where is your heart?  It's always like this I worry and wonder You're close to me here But where is your heart"
    zuid7 = storeText( jag, model, text, "imf" )

    text = "Hey nonny ding dong, alang, alang, alang Boom ba-doh, ba-doo, ba-doodle-ay  Oh, life could be a dream [sh-boom] If I could take you up in paradise up above [sh-boom] If you would tell me I'm the only one that you love Live could be a dream, sweetheart  [Hello, hello again, sh-boom and hopin' we'll meet again]"
    zuid8 = storeText( jag, model, text, "wiki" )

    text = "Once I had a secret love That lived within the heart of me All too soon my secret love Became impatient to be free  So I told a friendly star the way that dreamers often do Just how wonderful you are And why I’m so in love with you"
    zuid9 = storeText( jag, model, text, "wiki" )

    text = "Earth Angel, earth angel Will you be mine? My darling dear, love you all the time I'm just a fool, A fool in love with you  Earth Angel, earth angel The one I adore Love you forever, and evermore I'm just a fool, A fool in love with you "
    zuid10 = storeText( jag, model, text, "wiki" )

    text = "One, Two, Three O'clock, Four O'clock rock, Five, Six, Seven O'clock, Eight O'clock rock. Nine, Ten, Eleven O'clock, Twelve O'clock rock, We're gonna rock around the clock tonight.  Put your glad rags on and join me hon', We'll have some fun when the clock strikes one."
    zuid11 = storeText( jag, model, text, "wiki" )

    text = "You know I can be found, sitting home all alone, If you can't come around,  at least please telephone. Don't be cruel to a heart that's true.  Baby, if I made you mad  for something I might have said, Please, let's forget the past,  the future looks bright ahead, Don't be cruel to a heart that's true. I don't want no other love, Baby it's just you I'm thinking of."
    zuid12 = storeText( jag, model, text, "wiki" )

 
    ### select distribution 
    print("\n")
    qs = "select distribution(v, 'type=euclidean_whole_float') from vecanomaly" 
    print(qs, flush=True)
    jag.query( qs )
    while jag.reply():
        json_obj = json.loads( jag.jsonString() )
        print("distrib avg=", json_obj["avg"][0:80]);
        print("distrib stddev=", json_obj["stddev"][0:80]);



    print("\n")
    print("testAnomalous ...", flush=True )
    ### test anamolies
    testAnomalous( jag, model )

    
    jag.close()
    jag = None


if __name__ == "__main__":
    main()
