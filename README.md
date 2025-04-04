# jaguar-sdk
You can find a rich set of SDK, API, examples for Jaguar vector database in this repository.

## JaguarDB Is the Most Scalable Vector Database ##


**Jaguar Vector Database for AI**

JaguarDB Server is versatile and can be effortlessly deployed on a wide range of Linux platforms, including 
but not limited to Ubuntu, Red Hat, Fedora, and others. The server software is compatible with any
64-bit Linux distribution. Clients, on the other hand, enjoy flexibility and compatibility as 
they can initiate connections from various platforms, provided that Python 3 is installed, 
and the jaguardb-http-client package is available.


```

     Clients                   Http Gateway               Jaguar Server
                           (Any Linux Platform)        (Any Linux Platform)

                                                       -------------------
                                                      |                   |
  ----------------        --------------------        |    Data Pods      |
 |    Mac OS      | <==> |                    | <===> |                   |
  ----------------       |     REST  HTTP     |       |    AI Stores      |
                         |                    |       |                   |
  ----------------       |       GET          |       |  Vector Indexes   |
 |    Linux       | <==> |       POST         | <===> |                   |
  ----------------       |                    |       |  Scalar Indexes   | 
                         |      Insert        |       |                   |  
  ----------------       |      Upload        |       |    Similarity     |
 |    Windows     | <==> |      Query         | <===> |                   |
  ----------------        ---------------------       |     Anomaly       |
                                                      |                   |
                                                       ------------------- 

```

Clients Setup:

    pip install -U jaguardb-http-client

    The Python script httpclient/jaguarhttp.py demonstrates how to use the HTTP gateway.


Http Gateway Setup:

    wget http://www.jaguardb.com/download/fwww_3.4.3.tar.gz


JaguarDB Server Setup:

    wget http://www.jaguardb.com/download/jaguar-3.4.3.tar.gz


Applications have the flexibility to bypass the HTTP gateway and establish direct connections with 
the JaguarDB server when they are operating on the Ubuntu 22.04 platform. Additionally, 
libraries are provided to empower clients with the capability to communicate directly with the 
JaguarDB server for seamless data access and management.

```

        Clients                    JaguarDB Server
                                (Any Linux Platform)
    (Ubuntu 22.04)
                                -------------------
                               |                   |
   --------------------        |    Data Pods      |
  |                    |       |                   |
  |      QUERY         |       |    AI Stores      |
  |                    |       |                   |
  |      Insert        |       |  Vector Indexes   |
  |      Select        | <===> |                   |
  |      Update        |       |  Scalar Indexes   | 
  |      Delete        |       |                   |  
  |      Upload        |       |    Similarity     |
  |                    |       |                   |
   --------------------        |     Anomaly       |
                               |                   |
                                ------------------- 

```

Clients setup:

    pip install -U jaguardb-socket-client

    The Python script socketclient/jaguarsocket.py demonstrates how to use jaguardb-socket-client package.


JaguarDB  server setup:

    wget http://www.jaguardb.com/download/jaguar-3.4.3.tar.gz



The following document provides a comprehensive guide on utilizing JaguarDB to
develop and launch your scalable vector search projects and AI applications:


   http://www.jaguardb.com/doc/JaguarUserManual.pdf
<br />
<br />



**ZeroMove Instant Scaling**

In traditional way of horizontal scaling of distributed database systems, data migration is required and may
take a long time, referred as scaling nightmare. For some data strucures, such as HNSW vector store, it is not suitable
for vectors to be moved between nodes. JaguarDB, with the unique ZeroMove Hashing technology,
does not require any data migration and can scale to thousands of nodes instantly, in seconds.
JaguarDB scales the system by adding whole clusters where each cluster contains a volume of nodes.
Other database systems can only add a node one at a time. JaguarDB allows you to add hundreds of nodes
 in just one step. This is why JaguarDB can scale with lightning speed.

**Location Data**

Geospatial search plays a significant role in enhancing the capabilities of AI, especially in robotic
applications. Self-driving cars, drones, and robotics heavily rely on geospatial data for navigation
and obstacle avoidance.  JaguarDB stands out as the sole database that offers comprehensive support for both
vector and raster spatial data. With JaguarDB, users can seamlessly work with a
wide range of spatial shapes in their datasets.

For vector spatial data, JaguarDB supports an extensive set of shapes, including lines,
squares, rectangles, circles, ellipses, triangles, spheres, ellipsoids, cones,
cylinders, boxes, and their 3D counterparts. This broad range of vector shapes
empowers users to accurately represent and analyze complex spatial structures in their data.
When it comes to raster spatial data, JaguarDB enables the handling of point data,
multipoints, linestrings, multilinestrings, polygons, multipolygons, as well as their 3D equivalents.
This comprehensive support for raster shapes allows for the efficient storage and analysis
of geospatial information in various forms.

**Time Series Data**

AI models can forecast future trends and outcomes by analyzing historical time series data.
This is vital for financial predictions, stock market analysis, and demand forecasting.
JaguarDB excels in facilitating rapid ingestion of time series data, including the integration
of location-based data. Its unique capabilities extend to indexing in both spatial and temporal
dimensions, enabling efficient data retrieval based on these critical aspects. Moreover,
JaguarDB offers exceptional speed when it comes to back-filling time series data,
allowing for the seamless insertion of large volumes of data into past time periods.

One of JaguarDB's standout features is its automatic data aggregation across multiple
time windows. This functionality eliminates the need for additional computational work,
as users can instantly access aggregated data without any extra effort. By providing
immediate access to aggregated data, JaguarDB streamlines data analysis and empowers
users to derive valuable insights without delays.


**AI Data Lake and Storage**

The significance of a data lake for AI applications cannot be overstated. A data lake serves
as a foundational asset that provides essential capabilities for harnessing the power of artificial
intelligence. JaguarDB offers a versatile file storage solution that allows users to effortlessly upload various types of
data files, including videos, photos, and other file formats, into their system. During the upload
process, users have the option to generate embeddings, attach keywords or tags to each file, facilitating
easy and efficient vector retrieval. With JaguarDB's advanced search capabilities, users can search through trillions
of media files using vectors, keywords, enabling them to find media files quickly and effectively.
<br />

## Frequently Asked Questions about JaguarDB ##

Here is a list of frequenctly asked questions and answers regarding to vector database JauarDB.

   http://www.jaguardb.com/doc/FAQ.pdf
<br />
<br />



## Using docker for a quick setup of JaguarDB ##

You can use the docker pull command to install JaguarDB on a node:

```
  docker pull jaguardb/jaguardb
```


Then you can start the JaguarDB in a docker container:

```
  docker run -d -p 8888:8888 --name jaguardb  jaguardb/jaguardb
```


To launch ther jaguardb shell terminal and connect to jaguardb in docker:

```
  docker exec -it jaguardb /home/jaguar/jaguar/bin/jag 
```


To get into the docker container and open a shell:

```
  docker exec -it jaguardb /bin/bash
```

You will see that /workdir has all installed files and a jaguar server instance is
running under /home/jaguar directory. 


## Using docker for setring up JaguarDB and HTTP gateway ##

You can use the docker pull command to install JaguarDB on a node:

```
  docker pull jaguardb/jaguardb_with_http
```


Then you can start the JaguarDB and HTTP gateway in a docker container:

```
  docker run -d -p 8888:8888 -p 8080:8080 --name jaguardb_with_http  jaguardb/jaguardb_with_http
```


To launch ther jaguardb shell terminal and connect to jaguardb in docker:

```
  docker exec -it jaguardb_with_http /home/jaguar/jaguar/bin/jag  -apikey demouser
```


To get into the docker container and open a shell:

```
  docker exec -it jaguardb_with_http /bin/bash
```

The jaguardb_with_http docker image contains the jaguar server and the HTTP gateway server.
The API key demouser is a real user account, with limited capability, for demonstrating the operations of the system.


<br />

## Compiled Binary Package ##

Go to this URL to download the compiled Jaguar server package:  [Download JaguarDB Package](http://www.jaguardb.com/download.html)
<br />
<br />


## Web Site ##

Our web site is at:

    http://www.jaguardb.com
<br />



## Deployment ##

JaguarDB has undergone a rigorous journey of over 330 releases and iterations, accompanied by an
extensive testing process comprising 1421 test cases. As a result of this meticulous development and
quality assurance effort, JaguarDB has achieved a high level of stability and reliability that makes
it ideal for product environments. The extensive testing and continuous refinement of JaguarDB demonstrate
a commitment to excellence, ensuring that it meets the stringent requirements of real-world scenarios
and empowers organizations with a dependable and efficient data storage solution.

<br />








