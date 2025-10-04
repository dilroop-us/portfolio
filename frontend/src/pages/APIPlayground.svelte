<script lang="ts">
  import { Link } from 'svelte-routing';
  import Footer from '../lib/components/layout/Footer.svelte';
  import CustomSelect from '../lib/components/CustomSelect.svelte';
  
  let apiUrl = 'https://jsonplaceholder.typicode.com/posts/1';
  let method = 'GET';
  let apiKey = '';
  let headers: Array<{key: string, value: string}> = [
    { key: 'Content-Type', value: 'application/json' }
  ];
  let queryParams: Array<{key: string, value: string}> = [];
  let requestBody = '';
  
  let response = '';
  let responseStatus: number | null = null;
  let responseHeaders: Array<{key: string, value: string}> = [];
  let executionTime = 0;
  let loading = false;
  let requestStep = 0;
  let showFlow = false;
  
  const httpMethods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'HEAD', 'OPTIONS'];
  
  const exampleEndpoints = [
    { label: 'Get Demo Posts', url: '/api/demo/posts', method: 'GET' },
    { label: 'Get Single Demo Post', url: '/api/demo/posts/1', method: 'GET' },
    { label: 'Create Demo Post', url: '/api/demo/posts', method: 'POST', body: '{"title":"My Post","body":"Post content","userId":1}' },
    { label: 'Get Demo Users', url: '/api/demo/users', method: 'GET' },
    { label: 'Public - REST Countries', url: 'https://restcountries.com/v3.1/name/usa', method: 'GET' },
    { label: 'Public - Weather (needs key)', url: 'https://api.openweathermap.org/data/2.5/weather?q=London&appid=YOUR_API_KEY', method: 'GET' },
  ];
  
  function addHeader() {
    headers = [...headers, { key: '', value: '' }];
  }
  
  function removeHeader(index: number) {
    headers = headers.filter((_, i) => i !== index);
  }
  
  function addQueryParam() {
    queryParams = [...queryParams, { key: '', value: '' }];
  }
  
  function removeQueryParam(index: number) {
    queryParams = queryParams.filter((_, i) => i !== index);
  }
  
  function loadExample(example: any) {
    apiUrl = example.url;
    method = example.method;
    requestBody = example.body || '';
  }
  
  function buildFullUrl(): string {
    if (queryParams.length === 0 || queryParams.every(p => !p.key)) {
      return apiUrl;
    }
    
    const params = queryParams
      .filter(p => p.key)
      .map(p => `${encodeURIComponent(p.key)}=${encodeURIComponent(p.value)}`)
      .join('&');
    
    const separator = apiUrl.includes('?') ? '&' : '?';
    return `${apiUrl}${separator}${params}`;
  }
  
  async function executeRequest() {
    loading = true;
    response = '';
    responseHeaders = [];
    showFlow = true;
    requestStep = 0;
    
    try {
      requestStep = 1;
      await new Promise(resolve => setTimeout(resolve, 300));
      
      const requestHeaders: Record<string, string> = {};
      headers.forEach(h => {
        if (h.key) requestHeaders[h.key] = h.value;
      });
      
      if (apiKey) {
        requestHeaders['Authorization'] = apiKey.startsWith('Bearer ') ? apiKey : `Bearer ${apiKey}`;
      }
      
      const queryParamsObj: Record<string, string> = {};
      queryParams.forEach(p => {
        if (p.key) queryParamsObj[p.key] = p.value;
      });
      
      requestStep = 2;
      await new Promise(resolve => setTimeout(resolve, 300));
      
      const proxyRequest = {
        url: apiUrl,
        method: method,
        headers: requestHeaders,
        body: requestBody || null,
        query_params: Object.keys(queryParamsObj).length > 0 ? queryParamsObj : null
      };
      
      requestStep = 3;
      const res = await fetch('/api/proxy', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(proxyRequest)
      });
      
      requestStep = 4;
      await new Promise(resolve => setTimeout(resolve, 300));
      
      const data = await res.json();
      
      responseStatus = data.status_code;
      executionTime = data.execution_time;
      
      if (data.error) {
        response = `Error: ${data.error}`;
        responseHeaders = [];
      } else {
        const resHeaders: Array<{key: string, value: string}> = [];
        Object.entries(data.headers).forEach(([key, value]) => {
          resHeaders.push({ key, value: String(value) });
        });
        responseHeaders = resHeaders;
        
        try {
          const jsonData = JSON.parse(data.body);
          response = JSON.stringify(jsonData, null, 2);
        } catch {
          response = data.body;
        }
      }
      
      requestStep = 5;
    } catch (error) {
      response = `Network Error: ${error.message}`;
      responseStatus = -1;
      executionTime = 0;
    } finally {
      loading = false;
    }
  }
</script>

<div class="container mx-auto px-4 py-24">
  <h1 class="text-4xl font-bold mb-6 text-gradient">
    API Playground
  </h1>
  <p class="text-gray-400 mb-12 text-lg">
    Test any API endpoint with custom methods, headers, and request bodies
  </p>
  
  <div class="max-w-7xl mx-auto px-6">
    <div class="grid lg:grid-cols-2 gap-8 mb-12">
      <div class="card">
        <h3 class="text-2xl font-bold mb-6 text-white">🚀 Request Configuration</h3>
        
        <div class="mb-6">
          <label class="block text-sm font-medium mb-2">Quick Examples</label>
          <div class="flex flex-wrap gap-2">
            {#each exampleEndpoints as example}
              <button 
                on:click={() => loadExample(example)}
                class="btn-secondary text-xs"
              >
                {example.label}
              </button>
            {/each}
          </div>
        </div>
        
        <div class="mb-4">
          <label for="url-input" class="block text-sm font-medium mb-2">Request URL</label>
          <div class="flex gap-2">
            <div class="w-32">
              <CustomSelect
                bind:value={method}
                options={httpMethods.map(m => ({ value: m, label: m }))}
              />
            </div>
            <input 
              id="url-input"
              bind:value={apiUrl}
              type="text"
              placeholder="https://api.example.com/endpoint"
              class="flex-1 bg-gray-800 border border-gray-700 rounded-lg px-4 py-2 font-mono text-sm"
            />
          </div>
        </div>
        
        <div class="mb-4">
          <div class="flex justify-between items-center mb-2">
            <label class="block text-sm font-medium">Query Parameters</label>
            <button on:click={addQueryParam} class="text-xs text-gray-400 hover:text-white">+ Add</button>
          </div>
          {#each queryParams as param, i}
            <div class="flex gap-2 mb-2">
              <input 
                bind:value={param.key}
                placeholder="key"
                class="flex-1 bg-gray-900 border border-gray-700 rounded px-3 py-1.5 text-sm"
              />
              <input 
                bind:value={param.value}
                placeholder="value"
                class="flex-1 bg-gray-900 border border-gray-700 rounded px-3 py-1.5 text-sm"
              />
              <button on:click={() => removeQueryParam(i)} class="text-gray-500 hover:text-red-400">×</button>
            </div>
          {/each}
        </div>
        
        <div class="mb-4">
          <label for="api-key" class="block text-sm font-medium mb-2">
            API Key / Authorization 
            <span class="text-xs text-gray-500">(Optional - Never stored, client-side only)</span>
          </label>
          <input 
            id="api-key"
            bind:value={apiKey}
            type="password"
            placeholder="Enter API key or Bearer token"
            class="w-full bg-gray-900 border border-gray-700 rounded-lg px-4 py-2 font-mono text-sm"
          />
          <p class="text-xs text-gray-500 mt-1">
            🔒 Your key stays in browser memory only. Not saved or logged anywhere.
          </p>
        </div>
        
        <div class="mb-4">
          <div class="flex justify-between items-center mb-2">
            <label class="block text-sm font-medium">Headers</label>
            <button on:click={addHeader} class="text-xs text-gray-400 hover:text-white">+ Add</button>
          </div>
          {#each headers as header, i}
            <div class="flex gap-2 mb-2">
              <input 
                bind:value={header.key}
                placeholder="Header name"
                class="flex-1 bg-gray-900 border border-gray-700 rounded px-3 py-1.5 text-sm"
              />
              <input 
                bind:value={header.value}
                placeholder="Header value"
                class="flex-1 bg-gray-900 border border-gray-700 rounded px-3 py-1.5 text-sm"
              />
              <button on:click={() => removeHeader(i)} class="text-gray-500 hover:text-red-400">×</button>
            </div>
          {/each}
        </div>
        
        {#if ['POST', 'PUT', 'PATCH'].includes(method)}
          <div class="mb-4">
            <label for="request-body" class="block text-sm font-medium mb-2">Request Body (JSON)</label>
            <textarea 
              id="request-body"
              bind:value={requestBody}
              placeholder="{`{\"key\": \"value\"}`}"
              class="w-full bg-gray-900 border border-gray-700 rounded-lg px-4 py-3 h-32 font-mono text-sm"
            ></textarea>
          </div>
        {/if}
        
        <button 
          on:click={executeRequest} 
          disabled={loading || !apiUrl}
          class="btn-primary w-full"
        >
          {loading ? '⏳ Sending Request...' : '▶ Send Request'}
        </button>
      </div>
      
      <div class="card">
        <h3 class="text-2xl font-bold mb-6 text-white">📨 Response</h3>
        
        {#if responseStatus !== null && !loading}
          <div class="mb-4">
            <div class="flex items-center justify-between mb-3">
              <div class="flex items-center gap-3">
                <span class="text-sm text-gray-400">Status:</span>
                <span class={`px-3 py-1 rounded font-bold ${
                  responseStatus >= 200 && responseStatus < 300 ? 'bg-white/20 text-white border border-white/30' :
                  responseStatus >= 400 || responseStatus < 0 ? 'bg-gray-800/50 text-gray-300 border border-gray-600' :
                  'bg-gray-700/50 text-gray-200 border border-gray-500'
                }`}>
                  {responseStatus < 0 ? 'ERROR' : responseStatus}
                </span>
              </div>
              <span class="text-sm text-gray-400">Time: {executionTime.toFixed(0)}ms</span>
            </div>
            
            {#if responseHeaders.length > 0}
              <details class="mb-3">
                <summary class="text-sm text-gray-400 cursor-pointer hover:text-white">Response Headers ({responseHeaders.length})</summary>
                <div class="mt-2 bg-gray-900 border border-gray-700 rounded p-3 max-h-40 overflow-y-auto">
                  {#each responseHeaders as header}
                    <div class="text-xs mb-1">
                      <span class="text-gray-400">{header.key}:</span>
                      <span class="text-white ml-2">{header.value}</span>
                    </div>
                  {/each}
                </div>
              </details>
            {/if}
            
            <div>
              <label class="block text-sm text-gray-400 mb-2">Response Body</label>
              <pre class="bg-gray-900 border border-gray-700 rounded-lg p-4 overflow-auto max-h-96 text-sm"><code>{response}</code></pre>
            </div>
          </div>
        {:else if showFlow}
          <div class="space-y-4">
            <div class="bg-white/5 border border-white/10 rounded-xl p-4">
              <div class="flex items-center gap-3">
                <div class={`w-8 h-8 rounded-full flex items-center justify-center font-bold ${requestStep >= 1 ? 'bg-white text-black' : 'bg-gray-700 text-gray-400'}`}>1</div>
                <div class="flex-1">
                  <div class="font-bold text-white">Build Request</div>
                  <div class="text-sm text-gray-400">Configure URL, headers, and body</div>
                </div>
              </div>
            </div>
            
            <div class="flex justify-center">
              <div class="text-gray-500">↓</div>
            </div>
            
            <div class="bg-white/5 border border-white/10 rounded-xl p-4">
              <div class="flex items-center gap-3">
                <div class={`w-8 h-8 rounded-full flex items-center justify-center font-bold ${requestStep >= 2 ? 'bg-white text-black' : 'bg-gray-700 text-gray-400'}`}>2</div>
                <div class="flex-1">
                  <div class="font-bold text-white">Process Headers</div>
                  <div class="text-sm text-gray-400">Apply custom headers and params</div>
                </div>
              </div>
            </div>
            
            <div class="flex justify-center">
              <div class="text-gray-500">↓</div>
            </div>
            
            <div class="bg-white/5 border border-white/10 rounded-xl p-4">
              <div class="flex items-center gap-3">
                <div class={`w-8 h-8 rounded-full flex items-center justify-center font-bold ${requestStep >= 3 ? 'bg-white text-black' : 'bg-gray-700 text-gray-400'}`}>3</div>
                <div class="flex-1">
                  <div class="font-bold text-white">Send HTTP Request</div>
                  <div class="text-sm text-gray-400">Execute {method} request to API</div>
                </div>
              </div>
            </div>
            
            <div class="flex justify-center">
              <div class="text-gray-500">↓</div>
            </div>
            
            <div class="bg-white/5 border border-white/10 rounded-xl p-4">
              <div class="flex items-center gap-3">
                <div class={`w-8 h-8 rounded-full flex items-center justify-center font-bold ${requestStep >= 4 ? 'bg-white text-black' : 'bg-gray-700 text-gray-400'}`}>4</div>
                <div class="flex-1">
                  <div class="font-bold text-white">Receive Response</div>
                  <div class="text-sm text-gray-400">Parse status, headers, and body</div>
                </div>
              </div>
            </div>
          </div>
        {:else}
          <div class="text-center text-gray-400 py-12">
            Send a request to see the response here
          </div>
        {/if}
      </div>
    </div>
    
    <div class="card">
      <h3 class="text-3xl font-bold mb-6 text-white">📚 How HTTP APIs Work</h3>
      
      <div class="mb-8">
        <h4 class="text-xl font-bold mb-4 text-white">HTTP Methods</h4>
        <div class="grid md:grid-cols-3 gap-4">
          <div class="bg-white/5 border border-white/10 rounded-xl p-4">
            <h5 class="font-bold text-white mb-2">GET</h5>
            <p class="text-sm text-gray-300 mb-2">Retrieve data from server</p>
            <p class="text-xs text-gray-400">Safe & Idempotent • No body</p>
          </div>
          <div class="bg-white/5 border border-white/10 rounded-xl p-4">
            <h5 class="font-bold text-white mb-2">POST</h5>
            <p class="text-sm text-gray-300 mb-2">Create new resources</p>
            <p class="text-xs text-gray-400">Not idempotent • Has body</p>
          </div>
          <div class="bg-white/5 border border-white/10 rounded-xl p-4">
            <h5 class="font-bold text-white mb-2">PUT</h5>
            <p class="text-sm text-gray-300 mb-2">Update/replace resource</p>
            <p class="text-xs text-gray-400">Idempotent • Has body</p>
          </div>
          <div class="bg-white/5 border border-white/10 rounded-xl p-4">
            <h5 class="font-bold text-white mb-2">PATCH</h5>
            <p class="text-sm text-gray-300 mb-2">Partial update</p>
            <p class="text-xs text-gray-400">Not idempotent • Has body</p>
          </div>
          <div class="bg-white/5 border border-white/10 rounded-xl p-4">
            <h5 class="font-bold text-white mb-2">DELETE</h5>
            <p class="text-sm text-gray-300 mb-2">Remove resource</p>
            <p class="text-xs text-gray-400">Idempotent • No body</p>
          </div>
          <div class="bg-white/5 border border-white/10 rounded-xl p-4">
            <h5 class="font-bold text-white mb-2">OPTIONS</h5>
            <p class="text-sm text-gray-300 mb-2">Check allowed methods</p>
            <p class="text-xs text-gray-400">CORS preflight</p>
          </div>
        </div>
      </div>
      
      <div class="mb-8">
        <h4 class="text-xl font-bold mb-4 text-white">Common Status Codes</h4>
        <div class="grid md:grid-cols-2 gap-4">
          <div class="bg-white/5 border border-white/10 rounded-xl p-4">
            <h5 class="font-bold text-green-400 mb-2">2xx Success</h5>
            <p class="text-sm text-gray-300 mb-1">200 OK - Request succeeded</p>
            <p class="text-sm text-gray-300 mb-1">201 Created - Resource created</p>
            <p class="text-sm text-gray-300">204 No Content - Success, no body</p>
          </div>
          <div class="bg-white/5 border border-white/10 rounded-xl p-4">
            <h5 class="font-bold text-blue-400 mb-2">3xx Redirection</h5>
            <p class="text-sm text-gray-300 mb-1">301 Moved Permanently</p>
            <p class="text-sm text-gray-300 mb-1">302 Found (Temporary)</p>
            <p class="text-sm text-gray-300">304 Not Modified (Cache)</p>
          </div>
          <div class="bg-white/5 border border-white/10 rounded-xl p-4">
            <h5 class="font-bold text-yellow-400 mb-2">4xx Client Error</h5>
            <p class="text-sm text-gray-300 mb-1">400 Bad Request - Invalid syntax</p>
            <p class="text-sm text-gray-300 mb-1">401 Unauthorized - Auth required</p>
            <p class="text-sm text-gray-300">404 Not Found - Resource missing</p>
          </div>
          <div class="bg-white/5 border border-white/10 rounded-xl p-4">
            <h5 class="font-bold text-red-400 mb-2">5xx Server Error</h5>
            <p class="text-sm text-gray-300 mb-1">500 Internal Server Error</p>
            <p class="text-sm text-gray-300 mb-1">502 Bad Gateway</p>
            <p class="text-sm text-gray-300">503 Service Unavailable</p>
          </div>
        </div>
      </div>
      
      <div>
        <h4 class="text-xl font-bold mb-4 text-white">Important Headers</h4>
        <div class="bg-white/5 border border-white/10 rounded-xl p-4">
          <div class="mb-4">
            <h5 class="font-bold text-white mb-2">Request Headers</h5>
            <ul class="space-y-2 text-sm text-gray-300">
              <li><strong class="text-white">Content-Type:</strong> Format of request body (application/json, text/html)</li>
              <li><strong class="text-white">Authorization:</strong> Authentication credentials (Bearer token, API key)</li>
              <li><strong class="text-white">Accept:</strong> Preferred response format</li>
              <li><strong class="text-white">User-Agent:</strong> Client application identifier</li>
            </ul>
          </div>
          <div>
            <h5 class="font-bold text-white mb-2">Response Headers</h5>
            <ul class="space-y-2 text-sm text-gray-300">
              <li><strong class="text-white">Content-Type:</strong> Format of response body</li>
              <li><strong class="text-white">Cache-Control:</strong> Caching directives</li>
              <li><strong class="text-white">Access-Control-Allow-Origin:</strong> CORS policy (allows cross-origin requests)</li>
              <li><strong class="text-white">Set-Cookie:</strong> Sets cookies for client storage</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>

<style>
  .card {
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 1rem;
    padding: 2rem;
  }
  
  .btn-primary {
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.15), rgba(255, 255, 255, 0.05));
    border: 1px solid rgba(255, 255, 255, 0.2);
    color: white;
    padding: 0.75rem 1.5rem;
    border-radius: 0.75rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s;
  }
  
  .btn-primary:hover:not(:disabled) {
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.25), rgba(255, 255, 255, 0.1));
    border-color: rgba(255, 255, 255, 0.3);
    transform: translateY(-2px);
  }
  
  .btn-primary:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
  
  .btn-secondary {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    color: white;
    padding: 0.5rem 1rem;
    border-radius: 0.5rem;
    cursor: pointer;
    transition: all 0.2s;
  }
  
  .btn-secondary:hover {
    background: rgba(255, 255, 255, 0.1);
    border-color: rgba(255, 255, 255, 0.2);
  }
</style>

<Footer />
