// testweb.js For illustration only. Code can be used in a web browser.

(async () => {
  const jag = new JaguarWebClient("http://192.168.1.88:8080/fwww/");
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

  await jag.logout(token);
})();

