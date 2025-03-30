//////////////////////////////////////////////////////////////////////////////////
//
// Full JavaScript version of JaguarNodeClient class using Axios.
// You need to install these packages:  
//      npm install axios
//
//////////////////////////////////////////////////////////////////////////////////

const axios = require('axios');
const fs = require('fs');
const path = require('path');

class JaguarNodeClient {
  constructor(baseUrl) {
    if (!baseUrl.endsWith('/')) baseUrl += '/';
    this.url = baseUrl;
    this.token = '';
  }

  async login(apikey = null) {
    if (this.url === 'fakeurl/') return 'faketoken';
    this.apikey = apikey || this.getApiKey();
    const params = { req: 'login', apikey: this.apikey };
    try {
      const response = await axios.get(this.url, { params });
      const token = response.data.access_token;
      if (token) {
        this.token = token;
        return token;
      }
    } catch (e) {
      console.error('Login failed:', e.message);
    }
    return null;
  }

  async get(qs, token) {
    const headers = { Authorization: `Bearer ${token}` };
    const params = { req: qs, token };
    return axios.get(this.url, { headers, params });
  }

  async post(qs, token, withFile = false) {
    const headers = { Authorization: `Bearer ${token}` };
    const data = { req: qs, token };
    if (withFile) data.withfile = 'yes';
    return axios.post(this.url, data, { headers });
  }

    // Use custome raw post format
    rawPost( filePath, index, token ) 
    {
        const field = `file_${index - 1}`;
        const fileName = path.basename(filePath);
        const boundary = '----JaguarBoundary123456';
        const fileContent = fs.readFileSync(filePath);

        //console.log("fileContent: ", fileContent );
        
        // Step 3: Build raw multipart body as a Buffer
        const CRLF = '\r\n';
        const bodyParts = [];
        
        // -- Token field
        bodyParts.push(Buffer.from(`--${boundary}${CRLF}`));
        bodyParts.push(Buffer.from(`Content-Disposition: form-data; name="token"${CRLF}${CRLF}`));
        bodyParts.push(Buffer.from(`${token}${CRLF}`));
        
        // -- File field
        bodyParts.push(Buffer.from(`--${boundary}${CRLF}`));
        bodyParts.push(Buffer.from(`Content-Disposition: form-data; name="${field}"; filename="${fileName}"${CRLF}`));
        // [cgi20010 fgets line:] [Content-Disposition: form-data; name="file_1"; filename="img1.jpg"^M

        bodyParts.push(Buffer.from(`Content-Type: image/jpeg${CRLF}${CRLF}`));
        bodyParts.push(fileContent);
        bodyParts.push(Buffer.from(CRLF));
        
        // -- Ending boundary
        bodyParts.push(Buffer.from(`--${boundary}--${CRLF}`));
        
        // Step 4: Combine all parts
        const multipartBody = Buffer.concat(bodyParts);
        
        // Step 5: Set headers
        const headers = {
          'Content-Type': `multipart/form-data; boundary=${boundary}`,
          'Content-Length': multipartBody.length,
          'Authorization': `Bearer ${token}`,
        };
        
        // Step 6: Send with Axios
        //console.log("headers: ", JSON.stringify(headers) );
        //console.log("multipartBody: ", multipartBody );

        const resp = axios.post(this.url, multipartBody, { headers })
        return resp;
    }

    // post file with new raw format
  async postFile(token, filePath, index) {
    try {
      const response = await this.rawPost( filePath, index, token );
      // console.log('Server response:\n', JSON.stringify(response.data, null, 2));
      return response.status === 200;
    } catch (e) {
      console.error('File upload failed:', e.message);
      return false;
    }
  }

  async logout(token) {
    const headers = { Authorization: `Bearer ${token}` };
    const params = { request: 'logout', token };
    try {
      const response = await axios.get(this.url, { headers, params });
      return response;
    } catch (e) {
      console.error('Logout failed:', e.message);
      return {};
    }
  }

  getApiKey() {
    try {
      const home = process.env.HOME || process.env.USERPROFILE;
      const fpath = path.join(home, '.jagrc');
      const key = fs.readFileSync(fpath, 'utf-8').trim();
      return key;
    } catch (e) {
      return '';
    }
  }

  async getFileUrl(token, pod, store, column, zid) {
      const podstore = `${pod}.${store}`;
      const bearerToken = `Bearer ${token}`;
      const headers = { Authorization: bearerToken };
    
      const query = `getfile ${column} show from ${podstore} where zid='${zid}'`;
      const params = { req: query, token };
    
      try {
        const response = await axios.get(this.url, { headers, params });
        if (response.status === 200) {
          const js = response.data;
          return this.url + '?' + js[0];
        }
      } catch (error) {
        console.error('getFileUrl error:', error.message);
      }

  return '';
  }


  async run(query, withFile = false) {
    if (!this.token) return {};
    try {
      const res = await this.post(query, this.token, withFile);
      return res.data;
    } catch (e) {
      console.error('Query failed:', e.message);
      return {};
    }
  }

  async dropStore(pod, store) {
    const podstore = `${pod}.${store}`;
    const qs = `drop store ${podstore}`;
    try {
      const res = await this.post(qs, this.token);
      return res.status === 200;
    } catch {
      return false;
    }
  }

  async createStore(schema) {
    const [pod, store, columns] = this._parseSchema(schema);
    if (!pod || !store || !columns) return false;
    const podstore = `${pod}.${store}`;
    const qs = `create store ${podstore}(${columns})`;
    const res = await this.post(qs, this.token);
    return res.status === 200;
  }

  async add(pod, store, files, tensors, scalars) {
    const podstore = `${pod}.${store}`;
    let withFile = false;
    for (const file of files) {
      const { filepath, position } = file;
      const rc = await this.postFile(this.token, filepath, position);
      withFile = withFile || rc;
    }

    const dataList = [
      ...tensors.map(vec => `'${vec.join(',')}'`),
      ...scalars.map(val => `'${val}'`)
    ];
    const ins = dataList.join(',');
    const qs = `insert into ${podstore} values (${ins})`;
    const res = await this.post(qs, this.token, withFile);
    if (res.status !== 200) return '';
    return res.data.zid;
  }

  async search(pod, store, vector_index, vector_type, embeddings, topk = 3, where = null, metadatas = null, fetch_k = -1) {
    const vcol = vector_index;
    const vtype = vector_type;
    const qv_comma = embeddings.join(',');
    let qs = `select similarity(${vcol},'${qv_comma}','topk=${topk},fetch_k=${fetch_k},type=${vtype},with_score=yes,with_text=yes`;
    if (metadatas) {
      const meta = metadatas.join('&');
      qs += `,metadata=${meta}`;
    }
    qs += `') from ${pod}.${store}`;
    if (where) qs += ` where ${where}`;

    const result = await this.run(qs);
    if (!Array.isArray(result)) return [];
    return result.map(js => {
      const md = { zid: js.zid };
      if (metadatas) metadatas.forEach(m => (md[m] = js[m]));
      return [js.text, md, js.score];
    });
  }

  _parseSchema(schema) {
    const { pod, store, columns } = schema;
    const cols = [];

    for (const col of columns) {
      if (col.type === 'vector') {
        const { name, dim, dist, input, quantization } = col;
        if (!this._validDistanceType(dist) || !this._validInputType(input) || !this._validQuantizationType(quantization)) {
          return ['', '', ''];
        }
        const vtype = `${dist}_${input}_${quantization}`;
        cols.push(`${name} vector(${dim}, '${vtype}')`);
      }
    }

    for (const col of columns) {
      if (col.type !== 'vector') {
        const { name, type } = col;
        let c = '';
        if (type === 'str') {
          c = `${name} char(${col.size})`;
        } else {
          c = `${name} ${type}`;
        }
        cols.push(c);
      }
    }

    return [pod, store, cols.join(',')];
  }

  _validDistanceType(dist) {
    return ['cosine', 'euclidean', 'innerproduct', 'manhatten', 'hamming', 'chebyshev', 'minkowskihalf', 'jeccard'].includes(dist);
  }

  _validInputType(input) {
    return ['fraction', 'whole'].includes(input);
  }

  _validQuantizationType(quant) {
    return ['float', 'short', 'byte'].includes(quant);
  }
}

module.exports = JaguarNodeClient;


