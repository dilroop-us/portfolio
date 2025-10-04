<script lang="ts">
  let username = 'backend_engineer';
  let password = 'secure_pass';
  let token = '';
  let decoded: any = null;
  let loading = false;
  
  async function generateToken() {
    loading = true;
    try {
      const res = await fetch('/api/auth/demo', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
      });
      const data = await res.json();
      token = data.access_token;
      decoded = data.decoded;
    } catch (error) {
      console.error('Auth error:', error);
    } finally {
      loading = false;
    }
  }
</script>

<div class="glass rounded-xl p-8">
  <h3 class="text-2xl font-bold mb-6 text-green-400">🔐 Authentication Demo</h3>
  
  <div class="grid grid-cols-2 gap-4 mb-4">
    <div>
      <label for="auth-username" class="block text-sm font-medium mb-2">Username</label>
      <input id="auth-username" bind:value={username} class="w-full bg-gray-800 border border-gray-700 rounded-lg px-4 py-2" />
    </div>
    <div>
      <label for="auth-password" class="block text-sm font-medium mb-2">Password</label>
      <input id="auth-password" bind:value={password} type="password" class="w-full bg-gray-800 border border-gray-700 rounded-lg px-4 py-2" />
    </div>
  </div>
  
  <button 
    on:click={generateToken} 
    disabled={loading}
    class="btn-primary w-full mb-4"
  >
    {loading ? 'Generating...' : 'Generate JWT Token'}
  </button>
  
  {#if token}
    <div class="space-y-4">
      <div>
        <div class="block text-sm font-medium mb-2">Access Token</div>
        <div class="terminal">
          <code class="text-xs break-all">{token}</code>
        </div>
      </div>
      
      {#if decoded}
        <div>
          <div class="block text-sm font-medium mb-2">Decoded Token</div>
          <div class="terminal">
            <pre class="text-sm">{JSON.stringify(decoded, null, 2)}</pre>
          </div>
        </div>
      {/if}
    </div>
  {/if}
  
  <div class="mt-6 p-4 bg-green-600/10 border border-green-600/20 rounded-lg">
    <p class="text-sm text-green-400">🔒 JWT tokens are used for secure authentication in modern APIs</p>
  </div>
</div>
