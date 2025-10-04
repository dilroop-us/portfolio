<script>
  export let code = '';
  export let language = '';
  export let showCopy = true;
  
  let copied = false;
  
  async function copyToClipboard() {
    try {
      await navigator.clipboard.writeText(code);
      copied = true;
      setTimeout(() => copied = false, 2000);
    } catch (err) {
      console.error('Failed to copy:', err);
    }
  }
</script>

<div class="relative group">
  {#if showCopy}
    <button 
      on:click={copyToClipboard}
      class="absolute top-3 right-3 px-3 py-1.5 bg-surface-elevated border border-gray-700 rounded-lg text-xs text-gray-400 hover:text-primary-400 hover:border-primary-500/40 transition-all opacity-0 group-hover:opacity-100"
    >
      {copied ? 'Copied!' : 'Copy'}
    </button>
  {/if}
  
  <pre class="code-block overflow-x-auto"><code>{code}</code></pre>
</div>
