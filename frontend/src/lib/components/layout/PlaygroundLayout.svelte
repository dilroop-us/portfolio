<script>
  export let title = '';
  export let description = '';
</script>

<div class="min-h-screen">
  <div class="container-responsive">
    <div class="section-compact">
      {#if title}
        <div class="mb-8 md:mb-12">
          <h1 class="text-gradient-cyan mb-3">{title}</h1>
          {#if description}
            <p class="text-gray-400 text-lg max-w-3xl">{description}</p>
          {/if}
        </div>
      {/if}
      
      <slot />
    </div>
  </div>
</div>
