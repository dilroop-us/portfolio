<script lang="ts">
  let selectedEndpoint = 'GET /api/projects';
  let response = '';
  let loading = false;
  let username = 'demo_user';
  let password = 'demo_pass';
  
  const endpoints = [
    { label: 'GET /api/projects', method: 'GET', url: '/api/projects' },
    { label: 'GET /api/skills', method: 'GET', url: '/api/skills' },
    { label: 'POST /api/auth/demo', method: 'POST', url: '/api/auth/demo' },
  ];
  
  async function executeRequest() {
    loading = true;
    response = '';
    try {
      const selected = endpoints.find(e => e.label === selectedEndpoint);
      if (!selected) return;
      
      const options: RequestInit = {
        method: selected.method,
        headers: { 'Content-Type': 'application/json' },
      };
      
      if (selected.method === 'POST' && selected.url.includes('auth')) {
        options.body = JSON.stringify({ username, password });
      }
      
      const res = await fetch(selected.url, options);
      const data = await res.json();
      response = JSON.stringify(data, null, 2);
    } catch (error) {
      response = `Error: ${error.message}`;
    } finally {
      loading = false;
    }
  }
</script>

<div class="glass rounded-xl p-8">
  <h3 class="text-2xl font-bold mb-6 text-blue-400">🚀 API Playground</h3>
  
  <div class="mb-4">
    <label for="endpoint-select" class="block text-sm font-medium mb-2">Select Endpoint</label>
    <select id="endpoint-select" bind:value={selectedEndpoint} class="w-full bg-gray-800 border border-gray-700 rounded-lg px-4 py-2">
      {#each endpoints as endpoint}
        <option value={endpoint.label}>{endpoint.label}</option>
      {/each}
    </select>
  </div>
  
  {#if selectedEndpoint.includes('auth')}
    <div class="grid grid-cols-2 gap-4 mb-4">
      <div>
        <label for="username-input" class="block text-sm font-medium mb-2">Username</label>
        <input id="username-input" bind:value={username} class="w-full bg-gray-800 border border-gray-700 rounded-lg px-4 py-2" />
      </div>
      <div>
        <label for="password-input" class="block text-sm font-medium mb-2">Password</label>
        <input id="password-input" bind:value={password} type="password" class="w-full bg-gray-800 border border-gray-700 rounded-lg px-4 py-2" />
      </div>
    </div>
  {/if}
  
  <button 
    on:click={executeRequest} 
    disabled={loading}
    class="btn-primary w-full mb-4"
  >
    {loading ? 'Executing...' : 'Execute Request'}
  </button>
  
  {#if response}
    <div class="terminal">
      <div class="text-xs text-gray-400 mb-2">RESPONSE:</div>
      <pre class="overflow-auto max-h-96">{response}</pre>
    </div>
  {/if}
</div>
