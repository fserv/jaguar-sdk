#!/bin/bash

#apikey="20231119211753587j05a208561d6e87fdb3fafd065390f5be0@000"
apikey=`cat ~/.jagrc`

echo "login ..."
r=`curl -s --request POST --url "http://192.168.1.88:8080/fwww/" \
     -d "{\"query\": \"login\", \"apikey\": \"$apikey\" }"`
echo "$r"

#r={"access_token":"906305a5c645dcf83eaf050c49e591850f6e0d7feb52b5cb956668b63b1ee139b0","token_type":"Bearer"}
token=`echo $r|cut -d'"' -f4`
echo "token=[$token]"

echo "drop store myteststore ..."
curl -s --url "http://192.168.1.88:8080/fwww/"  --request POST \
     --header "Authorization: Bearer $token" \
     -d "{\"query\": \"drop store if exists myteststore\" }"

echo
echo "create store myteststore ..."
curl -s --url "http://192.168.1.88:8080/fwww/"  --request POST \
     --header "Authorization: Bearer $token" \
     -d "{\"query\": \"create store myteststore ( v vector(1024, 'cosine_fraction_float'), v:text char(1024), a int)\" }"

echo
echo "insert ..."
curl -s --url "http://192.168.1.88:8080/fwww/"  --request POST \
     --header "Authorization: Bearer $token" \
     -d "{\"query\": \"insert into myteststore values ( '0.1,0.2,0.3','text 1 here', '100')\" }"

echo
echo "insert ..."
curl -s --url "http://192.168.1.88:8080/fwww/"  --request POST \
     --header "Authorization: Bearer $token" \
     -d "{\"query\": \"insert into myteststore values ( '0.8,0.1,0.2','text 2 here', '200')\" }"


echo
echo "select similarity ..."
curl -s --url "http://192.168.1.88:8080/fwww/"  --request POST \
     --header "Authorization: Bearer $token" \
     -d "{\"query\": \"select similarity( v, '0.6,0.2,0.3','topk=1,type=cosine_fraction_float') from myteststore\" }"

echo
echo "select similarity where ..."
curl -s --url "http://192.168.1.88:8080/fwww/"  --request POST \
     --header "Authorization: Bearer $token" \
     -d "{\"query\": \"select similarity( v, '0.6,0.2,0.3','topk=1,type=cosine_fraction_float') from myteststore where a >= '100'\" }"


echo
echo "logout ..."
curl -s --url "http://192.168.1.88:8080/fwww/"  --request POST \
     --header "Authorization: Bearer $token" \
     -d "{\"query\": \"logout\" }"

