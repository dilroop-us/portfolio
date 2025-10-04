<script lang="ts">
  import { Link } from 'svelte-routing';
  import Footer from '../lib/components/layout/Footer.svelte';
  
  let cacheKey = '';
  let cacheValue = '';
  let cacheTTL: number | null = null;
  let getKey = '';
  let deleteKey = '';
  
  let setResponse: any = null;
  let getResponse: any = null;
  let deleteResponse: any = null;
  let clearResponse: any = null;
  let stats: any = null;
  
  let loading = false;
  let activeOperation = '';
  
  async function setCacheValue() {
    if (!cacheKey || !cacheValue) {
      alert('Please enter both key and value');
      return;
    }
    
    loading = true;
    activeOperation = 'set';
    try {
      const res = await fetch('/api/cache/set', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          key: cacheKey,
          value: cacheValue,
          ttl: cacheTTL
        })
      });
      
      setResponse = await res.json();
      await loadStats();
    } catch (error) {
      setResponse = { success: false, message: error.message };
    } finally {
      loading = false;
      activeOperation = '';
    }
  }
  
  async function getCacheValue() {
    if (!getKey) {
      alert('Please enter a key');
      return;
    }
    
    loading = true;
    activeOperation = 'get';
    try {
      const res = await fetch(`/api/cache/get/${getKey}`);
      getResponse = await res.json();
      await loadStats();
    } catch (error) {
      getResponse = { success: false, message: error.message };
    } finally {
      loading = false;
      activeOperation = '';
    }
  }
  
  async function deleteCacheValue() {
    if (!deleteKey) {
      alert('Please enter a key');
      return;
    }
    
    loading = true;
    activeOperation = 'delete';
    try {
      const res = await fetch(`/api/cache/delete/${deleteKey}`, {
        method: 'DELETE'
      });
      deleteResponse = await res.json();
      await loadStats();
    } catch (error) {
      deleteResponse = { success: false, message: error.message };
    } finally {
      loading = false;
      activeOperation = '';
    }
  }
  
  async function clearCache() {
    if (!confirm('Are you sure you want to clear all playground cache entries?')) {
      return;
    }
    
    loading = true;
    activeOperation = 'clear';
    try {
      const res = await fetch('/api/cache/clear', {
        method: 'POST'
      });
      clearResponse = await res.json();
      await loadStats();
    } catch (error) {
      clearResponse = { success: false, message: error.message };
    } finally {
      loading = false;
      activeOperation = '';
    }
  }
  
  async function loadStats() {
    try {
      const res = await fetch('/api/cache/stats');
      stats = await res.json();
    } catch (error) {
      console.error('Failed to load stats:', error);
    }
  }
  
  loadStats();
  const statsInterval = setInterval(loadStats, 2000);
  
  import { onDestroy } from 'svelte';
  onDestroy(() => {
    clearInterval(statsInterval);
  });
</script>

<div class="container mx-auto px-4 py-24">
  <h1 class="text-4xl font-bold mb-6 text-gradient">
    Caching Playground
  </h1>
  <p class="text-gray-400 mb-12 text-lg">
    Explore two-tier caching: L1 in-memory (LRU) + L2 Redis with real-time statistics
  </p>
  
  <div class="max-w-7xl mx-auto px-6">
    
    <div class="grid lg:grid-cols-2 gap-6 mb-8">
      <div class="card">
        <h3 class="text-2xl font-bold mb-6 text-white">📊 Real-Time Cache Statistics</h3>
        
        {#if stats}
          <div class="grid grid-cols-2 gap-4 mb-6">
            <div class="bg-white/5 border border-white/10 rounded-xl p-4">
              <div class="text-3xl font-bold text-white mb-1">{stats.hit_rate.toFixed(1)}%</div>
              <div class="text-sm text-gray-400">Hit Rate</div>
            </div>
            <div class="bg-white/5 border border-white/10 rounded-xl p-4">
              <div class="text-3xl font-bold text-white mb-1">{stats.l1_size + stats.l2_keys}</div>
              <div class="text-sm text-gray-400">Total Cached Items</div>
            </div>
          </div>
          
          <div class="mb-6">
            <h4 class="text-lg font-bold mb-3 text-white">L1 Cache (In-Memory LRU)</h4>
            <div class="grid grid-cols-3 gap-3">
              <div class="bg-gray-900 border border-white/20 rounded-lg p-3">
                <div class="text-xl font-bold text-white">{stats.l1_hits}</div>
                <div class="text-xs text-gray-400">Hits</div>
              </div>
              <div class="bg-gray-900 border border-white/20 rounded-lg p-3">
                <div class="text-xl font-bold text-white">{stats.l1_misses}</div>
                <div class="text-xs text-gray-400">Misses</div>
              </div>
              <div class="bg-gray-900 border border-white/20 rounded-lg p-3">
                <div class="text-xl font-bold text-white">{stats.l1_size}</div>
                <div class="text-xs text-gray-400">Size</div>
              </div>
            </div>
          </div>
          
          <div>
            <h4 class="text-lg font-bold mb-3 text-white">L2 Cache (Redis)</h4>
            <div class="grid grid-cols-3 gap-3">
              <div class="bg-gray-900 border border-white/20 rounded-lg p-3">
                <div class="text-xl font-bold text-white">{stats.l2_hits}</div>
                <div class="text-xs text-gray-400">Hits</div>
              </div>
              <div class="bg-gray-900 border border-white/20 rounded-lg p-3">
                <div class="text-xl font-bold text-white">{stats.l2_misses}</div>
                <div class="text-xs text-gray-400">Misses</div>
              </div>
              <div class="bg-gray-900 border border-white/20 rounded-lg p-3">
                <div class="text-xl font-bold text-white">{stats.l2_keys}</div>
                <div class="text-xs text-gray-400">Keys</div>
              </div>
            </div>
          </div>
        {:else}
          <div class="text-gray-400">Loading statistics...</div>
        {/if}
      </div>
      
      <div class="card">
        <h3 class="text-2xl font-bold mb-6 text-white">🔄 Request Flow Visualization</h3>
        
        <div class="space-y-4">
          <div class="bg-white/5 border border-white/10 rounded-xl p-4">
            <div class="flex items-center gap-3">
              <div class="w-8 h-8 bg-white text-black rounded-full flex items-center justify-center font-bold">1</div>
              <div class="flex-1">
                <div class="font-bold text-white">Request Arrives</div>
                <div class="text-sm text-gray-400">Client requests data by key</div>
              </div>
            </div>
          </div>
          
          <div class="flex justify-center">
            <div class="text-gray-500">↓</div>
          </div>
          
          <div class="bg-white/5 border border-white/10 rounded-xl p-4">
            <div class="flex items-center gap-3">
              <div class="w-8 h-8 bg-white text-black rounded-full flex items-center justify-center font-bold">2</div>
              <div class="flex-1">
                <div class="font-bold text-white">Check L1 Cache</div>
                <div class="text-sm text-gray-400">In-memory LRU cache (fastest, 100 items max)</div>
              </div>
            </div>
          </div>
          
          <div class="flex justify-center">
            <div class="text-gray-500">↓ (on miss)</div>
          </div>
          
          <div class="bg-white/5 border border-white/10 rounded-xl p-4">
            <div class="flex items-center gap-3">
              <div class="w-8 h-8 bg-white text-black rounded-full flex items-center justify-center font-bold">3</div>
              <div class="flex-1">
                <div class="font-bold text-white">Check L2 Cache</div>
                <div class="text-sm text-gray-400">Redis cache (fast, persistent, distributed)</div>
              </div>
            </div>
          </div>
          
          <div class="flex justify-center">
            <div class="text-gray-500">↓ (on hit)</div>
          </div>
          
          <div class="bg-white/5 border border-white/10 rounded-xl p-4">
            <div class="flex items-center gap-3">
              <div class="w-8 h-8 bg-white text-black rounded-full flex items-center justify-center font-bold">4</div>
              <div class="flex-1">
                <div class="font-bold text-white">Promote to L1</div>
                <div class="text-sm text-gray-400">Hot data moves to faster tier automatically</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <div class="grid lg:grid-cols-2 gap-6 mb-8">
      <div class="card">
        <h3 class="text-2xl font-bold mb-6 text-white">💾 Set Cache Value</h3>
        
        <div class="mb-4">
          <label for="cache-key" class="block text-sm font-medium mb-2">
            Cache Key
          </label>
          <input 
            id="cache-key"
            bind:value={cacheKey}
            type="text"
            placeholder="user:123"
            class="w-full bg-gray-900 border border-white/20 rounded-lg px-4 py-3"
          />
        </div>
        
        <div class="mb-4">
          <label for="cache-value" class="block text-sm font-medium mb-2">
            Cache Value
          </label>
          <textarea 
            id="cache-value"
            bind:value={cacheValue}
            placeholder="Any string value or JSON"
            class="w-full bg-gray-900 border border-white/20 rounded-lg px-4 py-3 h-24 font-mono text-sm"
          ></textarea>
        </div>
        
        <div class="mb-4">
          <label for="cache-ttl" class="block text-sm font-medium mb-2">
            TTL (seconds) <span class="text-gray-400">(optional)</span>
          </label>
          <input 
            id="cache-ttl"
            bind:value={cacheTTL}
            type="number"
            placeholder="300"
            min="0"
            class="w-full bg-gray-900 border border-white/20 rounded-lg px-4 py-3"
          />
          <p class="text-xs text-gray-400 mt-1">Leave empty for no expiration</p>
        </div>
        
        <button 
          on:click={setCacheValue} 
          disabled={loading && activeOperation === 'set'}
          class="btn-primary w-full"
        >
          {loading && activeOperation === 'set' ? '⏳ Setting...' : '💾 Set Cache Value'}
        </button>
        
        {#if setResponse}
          <div class="mt-4 p-4 bg-{setResponse.success ? 'white/5' : 'gray-800'} border border-white/10 rounded-lg">
            <div class="font-mono text-sm">
              <div class="mb-2">
                <span class="text-gray-400">Status:</span> 
                <span class="text-white">{setResponse.success ? '✅ Success' : '❌ Failed'}</span>
              </div>
              <div class="text-gray-300">{setResponse.message}</div>
            </div>
          </div>
        {/if}
      </div>
      
      <div class="card">
        <h3 class="text-2xl font-bold mb-6 text-white">🔍 Get Cache Value</h3>
        
        <div class="mb-4">
          <label for="get-key" class="block text-sm font-medium mb-2">
            Cache Key
          </label>
          <input 
            id="get-key"
            bind:value={getKey}
            type="text"
            placeholder="user:123"
            class="w-full bg-gray-900 border border-white/20 rounded-lg px-4 py-3"
          />
        </div>
        
        <button 
          on:click={getCacheValue} 
          disabled={loading && activeOperation === 'get'}
          class="btn-primary w-full"
        >
          {loading && activeOperation === 'get' ? '⏳ Getting...' : '🔍 Get Cache Value'}
        </button>
        
        {#if getResponse}
          <div class="mt-4 p-4 bg-{getResponse.success ? 'white/5' : 'gray-800'} border border-white/10 rounded-lg">
            <div class="font-mono text-sm">
              <div class="mb-2">
                <span class="text-gray-400">Status:</span> 
                <span class="text-white">{getResponse.success ? '✅ Hit' : '❌ Miss'}</span>
              </div>
              
              {#if getResponse.success}
                <div class="mb-2">
                  <span class="text-gray-400">Source:</span> 
                  <span class="text-white font-bold">{getResponse.source}</span>
                </div>
                
                {#if getResponse.ttl !== null}
                  <div class="mb-2">
                    <span class="text-gray-400">TTL Remaining:</span> 
                    <span class="text-white">{getResponse.ttl}s</span>
                  </div>
                {/if}
                
                <div class="mb-2">
                  <span class="text-gray-400">Value:</span>
                </div>
                <pre class="bg-gray-900 border border-white/20 rounded-lg px-3 py-2 text-xs overflow-auto">{getResponse.value}</pre>
              {:else}
                <div class="text-gray-300">{getResponse.message}</div>
              {/if}
            </div>
          </div>
        {/if}
      </div>
    </div>
    
    <div class="grid lg:grid-cols-2 gap-6 mb-8">
      <div class="card">
        <h3 class="text-2xl font-bold mb-6 text-white">🗑️ Delete Cache Entry</h3>
        
        <div class="mb-4">
          <label for="delete-key" class="block text-sm font-medium mb-2">
            Cache Key
          </label>
          <input 
            id="delete-key"
            bind:value={deleteKey}
            type="text"
            placeholder="user:123"
            class="w-full bg-gray-900 border border-white/20 rounded-lg px-4 py-3"
          />
        </div>
        
        <button 
          on:click={deleteCacheValue} 
          disabled={loading && activeOperation === 'delete'}
          class="btn-primary w-full"
        >
          {loading && activeOperation === 'delete' ? '⏳ Deleting...' : '🗑️ Delete Entry'}
        </button>
        
        {#if deleteResponse}
          <div class="mt-4 p-4 bg-{deleteResponse.success ? 'white/5' : 'gray-800'} border border-white/10 rounded-lg">
            <div class="font-mono text-sm">
              <div class="mb-2">
                <span class="text-gray-400">Status:</span> 
                <span class="text-white">{deleteResponse.success ? '✅ Success' : '❌ Failed'}</span>
              </div>
              <div class="mb-2">
                <span class="text-gray-400">Affected:</span> 
                <span class="text-white">{deleteResponse.affected_keys} cache level(s)</span>
              </div>
              <div class="text-gray-300">{deleteResponse.message}</div>
            </div>
          </div>
        {/if}
      </div>
      
      <div class="card">
        <h3 class="text-2xl font-bold mb-6 text-white">🧹 Clear All Cache</h3>
        
        <p class="text-gray-400 mb-6">
          This will clear all playground cache entries from both L1 (in-memory) and L2 (Redis) caches. 
          Only keys prefixed with "playground:" will be removed.
        </p>
        
        <button 
          on:click={clearCache} 
          disabled={loading && activeOperation === 'clear'}
          class="btn-primary w-full"
        >
          {loading && activeOperation === 'clear' ? '⏳ Clearing...' : '🧹 Clear All Playground Cache'}
        </button>
        
        {#if clearResponse}
          <div class="mt-4 p-4 bg-white/5 border border-white/10 rounded-lg">
            <div class="font-mono text-sm">
              <div class="mb-2">
                <span class="text-gray-400">Status:</span> 
                <span class="text-white">✅ Success</span>
              </div>
              <div class="mb-2">
                <span class="text-gray-400">Cleared:</span> 
                <span class="text-white">{clearResponse.affected_keys} entries</span>
              </div>
              <div class="text-gray-300">{clearResponse.message}</div>
            </div>
          </div>
        {/if}
      </div>
    </div>
    
    <div class="card mb-8">
      <h3 class="text-3xl font-bold mb-6 text-white">📚 Caching Strategies & Best Practices</h3>
      
      <div class="mb-8">
        <h4 class="text-xl font-bold mb-4 text-white">Multi-Level Caching Architecture</h4>
        <div class="grid md:grid-cols-3 gap-4">
          <div class="bg-white/5 border border-white/10 rounded-xl p-4">
            <h5 class="font-bold text-white mb-2">L1: In-Memory Cache</h5>
            <p class="text-sm text-gray-300 mb-2">LRU (Least Recently Used) cache with 100 item limit</p>
            <p class="text-xs text-gray-400">Speed: ~1μs | Scope: Single process | Volatility: High</p>
          </div>
          <div class="bg-white/5 border border-white/10 rounded-xl p-4">
            <h5 class="font-bold text-white mb-2">L2: Redis Cache</h5>
            <p class="text-sm text-gray-300 mb-2">Distributed cache with persistence and TTL support</p>
            <p class="text-xs text-gray-400">Speed: ~1ms | Scope: Distributed | Volatility: Low</p>
          </div>
          <div class="bg-white/5 border border-white/10 rounded-xl p-4">
            <h5 class="font-bold text-white mb-2">Promotion Strategy</h5>
            <p class="text-sm text-gray-300 mb-2">L2 hits automatically promoted to L1 for faster access</p>
            <p class="text-xs text-gray-400">Result: Hot data becomes progressively faster</p>
          </div>
        </div>
      </div>
      
      <div class="mb-8">
        <h4 class="text-xl font-bold mb-4 text-white">Common Caching Patterns</h4>
        <div class="grid md:grid-cols-2 gap-4">
          <div class="bg-white/5 border border-white/10 rounded-xl p-4">
            <h5 class="font-bold text-white mb-2">Cache-Aside (Lazy Loading)</h5>
            <p class="text-sm text-gray-300 mb-2">Application checks cache first, loads from DB on miss, then caches result</p>
            <p class="text-xs text-gray-400">✅ Simple • ❌ Cold start penalty</p>
          </div>
          <div class="bg-white/5 border border-white/10 rounded-xl p-4">
            <h5 class="font-bold text-white mb-2">Write-Through</h5>
            <p class="text-sm text-gray-300 mb-2">Writes go to cache and database simultaneously</p>
            <p class="text-xs text-gray-400">✅ Always consistent • ❌ Slower writes</p>
          </div>
          <div class="bg-white/5 border border-white/10 rounded-xl p-4">
            <h5 class="font-bold text-white mb-2">Write-Behind (Write-Back)</h5>
            <p class="text-sm text-gray-300 mb-2">Writes go to cache first, async batch to database</p>
            <p class="text-xs text-gray-400">✅ Fast writes • ❌ Risk of data loss</p>
          </div>
          <div class="bg-white/5 border border-white/10 rounded-xl p-4">
            <h5 class="font-bold text-white mb-2">Read-Through</h5>
            <p class="text-sm text-gray-300 mb-2">Cache handles DB loading transparently</p>
            <p class="text-xs text-gray-400">✅ Clean separation • ❌ Complex setup</p>
          </div>
        </div>
      </div>
      
      <div class="mb-8">
        <h4 class="text-xl font-bold mb-4 text-white">Cache Invalidation Strategies</h4>
        <div class="grid md:grid-cols-3 gap-4">
          <div class="bg-white/5 border border-white/10 rounded-xl p-4">
            <h5 class="font-bold text-white mb-2">TTL (Time To Live)</h5>
            <p class="text-sm text-gray-300 mb-2">Entries expire after set duration</p>
            <p class="text-xs text-gray-400">Best for: Data with predictable staleness tolerance</p>
          </div>
          <div class="bg-white/5 border border-white/10 rounded-xl p-4">
            <h5 class="font-bold text-white mb-2">Event-Based</h5>
            <p class="text-sm text-gray-300 mb-2">Invalidate on data changes</p>
            <p class="text-xs text-gray-400">Best for: Critical consistency requirements</p>
          </div>
          <div class="bg-white/5 border border-white/10 rounded-xl p-4">
            <h5 class="font-bold text-white mb-2">LRU Eviction</h5>
            <p class="text-sm text-gray-300 mb-2">Remove least recently used when full</p>
            <p class="text-xs text-gray-400">Best for: Limited memory scenarios</p>
          </div>
        </div>
      </div>
      
      <div>
        <h4 class="text-xl font-bold mb-4 text-white">Best Practices</h4>
        <div class="bg-white/5 border border-white/10 rounded-xl p-4">
          <ul class="space-y-2 text-sm text-gray-300">
            <li>✅ <strong class="text-white">Cache immutable data aggressively</strong> - Configuration, reference data</li>
            <li>✅ <strong class="text-white">Set appropriate TTLs</strong> - Balance freshness vs performance</li>
            <li>✅ <strong class="text-white">Monitor hit rates</strong> - Optimize what's actually used (aim for 80%+ hit rate)</li>
            <li>✅ <strong class="text-white">Use cache keys wisely</strong> - Include version/tenant in keys to avoid conflicts</li>
            <li>✅ <strong class="text-white">Plan for cache failures</strong> - Graceful degradation when cache is unavailable</li>
            <li>❌ <strong class="text-white">Don't cache everything</strong> - Adds complexity without benefit for rarely-accessed data</li>
            <li>❌ <strong class="text-white">Don't ignore memory limits</strong> - Monitor and set eviction policies</li>
          </ul>
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
</style>

<Footer />
