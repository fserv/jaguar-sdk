// testnode.js
const fs = require('fs');
const path = require('path');
const JaguarNodeClient = require('jaguardb-node-client');

(async () => {
  // Replace 192.168.1.88 with you server IP address
  const jag = new JaguarNodeClient("http://192.168.1.88:8080/fwww/");
  const apikey = 'demouser';

  const token = await jag.login(apikey);
  console.log(`got token ${token}`);
  if (!token) {
    console.error("Error login");
    process.exit(1);
  }

  const helpResp = await jag.get("help", token);
  const j1 = helpResp.data[0];
  const j2 = JSON.parse(j1);
  console.log(j2['data']);

  let q = "drop store vdb.week";
  let response = await jag.get(q, token);
  console.log(`drop store [${JSON.stringify(response.data)}]`);


  q = "create store vdb.week ( v vector(512, 'euclidean_fraction_float'), v:f file, v:t char(1024), a int)";
  response = await jag.get(q, token);
  console.log(`create store [${JSON.stringify(response.data)}]`);

  const checkFile = (f) => {
    if (!fs.existsSync(f)) {
      console.error(`File ${f} does not exist.`);
      process.exit(1);
    }
  };

  const imgfile1 = 'test/img1.jpg';
  const imgfile2 = 'test/img2.jpg';
  const imgfile3 = 'test/img3.jpg';
  checkFile(imgfile1);
  checkFile(imgfile2);
  checkFile(imgfile3);

  let rc = await jag.postFile(token, imgfile1, 2);
  console.log(`postFile ${imgfile1} ${rc}`);
  q = `insert into vdb.week values ('0.1,0.2,0.3,0.4,0.5,0.02,0.3,0.5', '${imgfile1}', 'this is text description: windy ', 10 )`;
  response = await jag.post(q, token, true);
  let jd = response.data;
  console.log(`insert response [${JSON.stringify(jd)}]`);
  console.log(`first insert zid = ${jd.zid}`);

  rc = await jag.postFile(token, imgfile2, 2);
  q = `insert into vdb.week values ('0.5,0.2,0.5,0.4,0.1,0.02,0.3,0.7', '${imgfile2}', 'this is text description: sunny', 100 )`;
  response = await jag.post(q, token, true);
  jd = response.data;
  console.log(`second insert zid = ${jd.zid}`);

  q = "select similarity(v, '0.3,0.2,0.8,0.4,0.1,0.1,0.3,0.1', 'topk=3, type=euclidean_fraction_float, with_text=yes, with_score=yes') from vdb.week";
  response = await jag.post(q, token);
  const jarr = response.data;

  for (const obj of jarr) {
    const { zid, field, vectorid, distance, text, score } = obj;
    console.log(`field=[${field}] vectorid=[${vectorid}] distance=[${distance}] text=[${text}] score=[${score}]`);
    const furl = await jag.getFileUrl(token, "vdb", "week", "v:f", zid);
    console.log(`file url=${furl}`);
  }

  const schema = {
    pod: "vdb",
    store: "mystoreapi",
    columns: [
      { name: "vec", type: "vector", dim: "3", dist: "euclidean", input: "fraction", quantization: "float" },
      { name: "vec:text", type: "str", size: "1024" },
      { name: "vec:img1", type: "file" },
      { name: "vec:img2", type: "file" },
      { name: "path", type: "str", size: "64" },
      { name: "tms", type: "datetimesec" },
      { name: "seq", type: "bigint" },
      { name: "num", type: "int" },
    ],
  };

  rc = await jag.dropStore("vdb", "mystoreapi");
  console.log(`dropStore rc=${rc}`);
  rc = await jag.createStore(schema);
  console.log(`createStore rc=${rc}`);

  let files = [
    { filepath: "test/img1.jpg", position: 3 },
    { filepath: "test/img2.jpg", position: 4 },
  ];
  let tensors = [['0.2', '0.3', '0.51']];
  let scalars = ['first product description', 'test/img1.jpg', 'test/img2.jpg', '/path/123/d1', '2024-02-09 11:21:32', '1001', '8'];
  let zid = await jag.add("vdb", "mystoreapi", files, tensors, scalars);
  console.log(`insert zid=${zid}`);

  files = [
    { filepath: "test/img3.jpg", position: 3 },
    { filepath: "test/img4.jpg", position: 4 },
  ];
  tensors = [['0.1', '0.5', '0.71']];
  scalars = ['second product description', 'test/img3.jpg', 'test/img4.jpg', '/path/234/d2', '2024-02-12 15:21:32', '1002', '9'];
  zid = await jag.add("vdb", "mystoreapi", files, tensors, scalars);
  console.log(`add zid=${zid}`);

  const embeddings = ['0.2', '0.4', '0.31'];
  let docs = await jag.search("vdb", "mystoreapi", "vec", "euclidean_fraction_float", embeddings, 3);
  console.log(`search1 docs=`, docs);

  let where = "num='8'";
  docs = await jag.search("vdb", "mystoreapi", "vec", "euclidean_fraction_float", embeddings, 3, where);
  console.log(`search2 docs=`, docs);

  where = "num='9'";
  const metadatas = ['seq', 'num', 'tms'];
  docs = await jag.search("vdb", "mystoreapi", "vec", "euclidean_fraction_float", embeddings, 3, where, metadatas, 100);
  console.log(`search3 docs=`, docs);

  await jag.logout(token);
})();

