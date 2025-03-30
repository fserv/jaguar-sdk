//////////////////////////////////////////////////////////////////////////////////
//
// Full JavaScript version of JaguarWebClient class using Axios
// You need to import the axios object with script tag:
// <script type="module">
//    import axios from 'https://cdn.jsdelivr.net/npm/axios/dist/axios.min.js';
//    axios.get('https://example.com/api/data')
// </script>
//
//////////////////////////////////////////////////////////////////////////////////

class JaguarWebClient {
  constructor(baseUrl) {
    if (!baseUrl.endsWith('/')) baseUrl += '/';
    this.url = baseUrl;
    this.token = '';
  }

  async login(apikey = null) {
    if (this.url === 'fakeurl/') return 'faketoken';
    this.apikey = apikey;
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

  async postFile(token, file, index) {
    const form = new FormData();
    const field = `file_${index - 1}`;
    form.append(field, file); // File from <input type="file">
    form.append('token', this.token);

    const headers = { Authorization: `Bearer ${this.token}` };
    const response = await axios.post(this.url, form, { headers });
    return response;
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

module.exports = JaguarWebClient;


