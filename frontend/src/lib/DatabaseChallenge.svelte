<script lang="ts">
  let challenges: any[] = [];
  let selectedChallenge: any = null;
  let userQuery = '';
  let queryResult = '';
  let loading = false;
  let executionTime = 0;
  
  async function loadChallenges() {
    const res = await fetch('/api/challenges');
    challenges = await res.json();
    if (challenges.length > 0) {
      selectedChallenge = challenges[0];
    }
  }
  
  async function executeQuery() {
    loading = true;
    queryResult = '';
    try {
      const res = await fetch('/api/execute-query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: userQuery })
      });
      const data = await res.json();
      executionTime = data.execution_time;
      
      if (data.success) {
        queryResult = JSON.stringify(data.data, null, 2);
      } else {
        queryResult = `Error: ${data.error}`;
      }
    } catch (error) {
      queryResult = `Error: ${error.message}`;
    } finally {
      loading = false;
    }
  }
  
  loadChallenges();
</script>

<div class="glass rounded-xl p-8">
  <h3 class="text-2xl font-bold mb-6 text-purple-400">💾 Database Challenge</h3>
  
  {#if selectedChallenge}
    <div class="mb-6">
      <div class="flex items-center justify-between mb-4">
        <h4 class="text-xl font-bold">{selectedChallenge.title}</h4>
        <span class="px-3 py-1 bg-purple-600/20 text-purple-400 rounded-full text-sm">
          {selectedChallenge.difficulty}
        </span>
      </div>
      <p class="text-gray-300 mb-4">{selectedChallenge.description}</p>
      
      <div class="mb-4">
        <label for="sql-query-input" class="block text-sm font-medium mb-2">Your SQL Query</label>
        <textarea 
          id="sql-query-input"
          bind:value={userQuery}
          placeholder="SELECT * FROM ..."
          class="w-full bg-gray-800 border border-gray-700 rounded-lg px-4 py-2 font-mono text-sm h-32"
        ></textarea>
      </div>
      
      <button 
        on:click={executeQuery} 
        disabled={loading || !userQuery}
        class="btn-primary w-full mb-4"
      >
        {loading ? 'Executing...' : 'Run Query'}
      </button>
      
      {#if queryResult}
        <div class="terminal">
          <div class="flex justify-between text-xs text-gray-400 mb-2">
            <span>RESULT:</span>
            <span>Execution time: {executionTime}ms</span>
          </div>
          <pre class="overflow-auto max-h-64">{queryResult}</pre>
        </div>
      {/if}
    </div>
    
    <div class="mt-6 p-4 bg-blue-600/10 border border-blue-600/20 rounded-lg">
      <p class="text-sm text-blue-400">💡 Tip: Only SELECT queries are allowed for security</p>
    </div>
  {:else}
    <p class="text-gray-400">Loading challenges...</p>
  {/if}
</div>
