<script>
  export let isOpen = false;
  export let title = '';
  export let size = 'md';
  
  const sizes = {
    sm: 'max-w-md',
    md: 'max-w-2xl',
    lg: 'max-w-4xl',
    xl: 'max-w-6xl',
  };
  
  function handleBackdropClick(e) {
    if (e.target === e.currentTarget) {
      isOpen = false;
    }
  }
  
  function handleEscape(e) {
    if (e.key === 'Escape') {
      isOpen = false;
    }
  }
</script>

<svelte:window on:keydown={handleEscape} />

{#if isOpen}
  <div 
    class="fixed inset-0 z-50 flex items-center justify-center px-4 bg-gray-950/80 backdrop-blur-sm animate-fade-in"
    on:click={handleBackdropClick}
    on:keydown
  >
    <div class="glass rounded-2xl p-6 w-full {sizes[size]} animate-slide-up">
      {#if title}
        <div class="flex items-center justify-between mb-6">
          <h3 class="text-display-sm text-gradient-cyan">{title}</h3>
          <button 
            on:click={() => isOpen = false}
            class="p-2 text-gray-400 hover:text-primary-400 transition-colors"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      {/if}
      
      <slot />
    </div>
  </div>
{/if}
