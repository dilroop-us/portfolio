<script lang="ts">
  import { onMount } from 'svelte';
  
  export let delay = 0;
  export let threshold = 0.1;
  
  let visible = false;
  let element: HTMLElement;
  
  onMount(() => {
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    
    if (prefersReducedMotion) {
      visible = true;
      return;
    }
    
    const observer = new IntersectionObserver(
      (entries) => {
        if (entries[0].isIntersecting) {
          setTimeout(() => {
            visible = true;
          }, delay);
          observer.disconnect();
        }
      },
      { threshold }
    );
    
    observer.observe(element);
    
    return () => observer.disconnect();
  });
</script>

<div bind:this={element} class="scroll-reveal" class:visible>
  <slot />
</div>

<style>
  .scroll-reveal {
    opacity: 0;
    transform: translateY(16px);
    transition: opacity 250ms cubic-bezier(0.4, 0, 0.2, 1),
                transform 250ms cubic-bezier(0.4, 0, 0.2, 1);
  }
  
  .scroll-reveal.visible {
    opacity: 1;
    transform: translateY(0);
  }
</style>
