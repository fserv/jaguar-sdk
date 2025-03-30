
# JaguarNodeClient 

A lightweight JavaScript client for JaguarDB vector store in JavaScript running in nodejs.


## Installation

npm install jaguardb-node-client

Test script:  testnode.js

   node testnode.js

The file JaguarNodeClient.js in this directory is for illustration only.
If you run the command: "npm install jaguardb-node-client" the file JaguarNodeClient.js will be
automatically installed in your node_modules directory. If you do not do the npm install, you can
use the file JaguarNodeClient.js directly in your project.

The JaguarNodeClient.js or jaguardb-node-client package is for you developing backend
projects in nodejs server framework.


# JaguarWebClient 

A lightweight JavaScript client for JaguarDB vector store in JavaScript running in web browsers.


## Installation

npm install jaguardb-web-client
The above command will install class file JaguarWebClient.js in your node_modules directory.
If you do not do the npm install, you can use the file JaguarNodeClient.js and place it on
your web server host and use it in HTML javascript programs.

Example script:  testweb.js

You need to place the JaguarWebClient.js on a HTTP host
and put the URL into the <script> ... </script> in HTML file.

  <script type="module">
      import axios from 'https://cdn.jsdelivr.net/npm/axios/dist/axios.min.js';
      axios.get('https://example.com/api/data')

      import JaguarWebClient from 'http://yourserver.com/JaguarWebClient.js';
      or
      import JaguarWebClient from 'http://www.jaguardb.com/JaguarWebClient.js';
      ...
 </script>


The JaguarWebClient.js is for you developing frontend projects in a browser which
can retrieve data or change data in the JaguarDB vector store. This approach is not
recommended since the brower can have access to the database directly which might
cause security issues. The recommended approach is let your frontend make API calls to the
backend which, if it is nodejs based, can use the JaguarNodeClient.js or the jaguardb-node-client 
package to have access to the backend vector database.


