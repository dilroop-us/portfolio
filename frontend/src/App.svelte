<script lang="ts">
  import { Router, Route, Link } from 'svelte-routing';
  import { fade } from 'svelte/transition';
  import Home from './pages/Home.svelte';
  import APIPlayground from './pages/APIPlayground.svelte';
  import DatabasePlayground from './pages/DatabasePlayground.svelte';
  import CachingPlayground from './pages/CachingPlayground.svelte';
  import ChatPlayground from './pages/ChatPlayground.svelte';
  import Contact from './pages/Contact.svelte';
  
  let url = '';
  let mobileMenuOpen = false;
  let isNavigating = false;
  
  function toggleMobileMenu() {
    mobileMenuOpen = !mobileMenuOpen;
  }
  
  function closeMobileMenu() {
    mobileMenuOpen = false;
  }

  function handleNavigation() {
    isNavigating = true;
    setTimeout(() => {
      isNavigating = false;
    }, 600);
    closeMobileMenu();
  }
</script>

{#if isNavigating}
  <div class="progress-bar" transition:fade={{ duration: 100 }}></div>
{/if}

<Router {url}>
  <nav class="nav-bar">
    <div class="container mx-auto px-4 py-4">
      <div class="flex items-center justify-between">
        <Link to="/" on:click={handleNavigation}>
          <h1 class="text-xl font-bold gradient-text cursor-pointer hover:opacity-80 transition-opacity">
            Dilroop Ummar Shameem
          </h1>
        </Link>
        
        <div class="hidden md:flex gap-6">
          <Link to="/" on:click={handleNavigation} class="nav-link" getProps={({ isCurrent }) => ({ class: isCurrent ? 'nav-link active' : 'nav-link' })}>Home</Link>
          <Link to="/playground/api" on:click={handleNavigation} class="nav-link" getProps={({ isCurrent }) => ({ class: isCurrent ? 'nav-link active' : 'nav-link' })}>API Playground</Link>
          <Link to="/playground/database" on:click={handleNavigation} class="nav-link" getProps={({ isCurrent }) => ({ class: isCurrent ? 'nav-link active' : 'nav-link' })}>Database</Link>
          <Link to="/playground/caching" on:click={handleNavigation} class="nav-link" getProps={({ isCurrent }) => ({ class: isCurrent ? 'nav-link active' : 'nav-link' })}>Caching</Link>
          <Link to="/playground/chat" on:click={handleNavigation} class="nav-link" getProps={({ isCurrent }) => ({ class: isCurrent ? 'nav-link active' : 'nav-link' })}>Chat</Link>
          <Link to="/contact" on:click={handleNavigation} class="nav-link" getProps={({ isCurrent }) => ({ class: isCurrent ? 'nav-link active' : 'nav-link' })}>Contact</Link>
        </div>
        
        <div class="md:hidden">
          <button 
            on:click={toggleMobileMenu}
            class="mobile-menu-button"
            aria-label="Toggle menu"
          >
            {#if mobileMenuOpen}
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            {:else}
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            {/if}
          </button>
        </div>
      </div>
      
      {#if mobileMenuOpen}
        <div class="md:hidden mt-4 pb-4 flex flex-col gap-3" transition:fade={{ duration: 150 }}>
          <Link to="/" on:click={handleNavigation} class="nav-link py-2">Home</Link>
          <Link to="/playground/api" on:click={handleNavigation} class="nav-link py-2">API Playground</Link>
          <Link to="/playground/database" on:click={handleNavigation} class="nav-link py-2">Database</Link>
          <Link to="/playground/caching" on:click={handleNavigation} class="nav-link py-2">Caching</Link>
          <Link to="/playground/chat" on:click={handleNavigation} class="nav-link py-2">Chat</Link>
          <Link to="/contact" on:click={handleNavigation} class="nav-link py-2">Contact</Link>
        </div>
      {/if}
    </div>
  </nav>

  <main class="min-h-screen">
    <Route path="/"><Home /></Route>
    <Route path="/playground/api"><APIPlayground /></Route>
    <Route path="/playground/database"><DatabasePlayground /></Route>
    <Route path="/playground/caching"><CachingPlayground /></Route>
    <Route path="/playground/chat"><ChatPlayground /></Route>
    <Route path="/contact"><Contact /></Route>
  </main>
</Router>

<style>
  .nav-bar {
    position: fixed;
    top: 0;
    width: 100%;
    backdrop-filter: blur(24px);
    z-index: 99999;
    background-color: rgba(0, 0, 0, 0.8);
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
  }
  
  :global(.nav-link) {
    position: relative;
    font-weight: 500;
    color: rgba(255, 255, 255, 0.6);
    transition: color 180ms cubic-bezier(0.4, 0, 0.2, 1);
  }
  
  :global(.nav-link::after) {
    content: '';
    position: absolute;
    bottom: -4px;
    left: 0;
    width: 0;
    height: 2px;
    background: white;
    transition: width 180ms cubic-bezier(0.4, 0, 0.2, 1);
  }
  
  :global(.nav-link:hover) {
    color: rgba(255, 255, 255, 1);
  }
  
  :global(.nav-link:hover::after) {
    width: 100%;
  }
  
  :global(.nav-link.active) {
    color: white;
  }
  
  :global(.nav-link.active::after) {
    width: 100%;
  }
  
  .mobile-menu-button {
    padding: 0.5rem;
    border-radius: 0.5rem;
    color: white;
    transition: background-color 150ms cubic-bezier(0.4, 0, 0.2, 1);
  }
  
  .mobile-menu-button:hover {
    background-color: rgba(255, 255, 255, 0.04);
  }

  .progress-bar {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    height: 2px;
    background: white;
    opacity: 0.3;
    z-index: 9999;
    animation: progress 0.6s cubic-bezier(0.4, 0, 0.2, 1);
  }
  
  @keyframes progress {
    0% { 
      transform: scaleX(0); 
      transform-origin: left; 
    }
    100% { 
      transform: scaleX(1); 
      transform-origin: left; 
    }
  }
</style>
