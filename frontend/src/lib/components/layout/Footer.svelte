<script lang="ts">
  const currentYear = new Date().getFullYear();
  
  const socialLinks = [
    {
      name: 'Medium',
      url: 'https://medium.com/@joyichiro',
      svg: '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M13.54 12a6.8 6.8 0 01-6.77 6.82A6.8 6.8 0 010 12a6.8 6.8 0 016.77-6.82A6.8 6.8 0 0113.54 12zM20.96 12c0 3.54-1.51 6.42-3.38 6.42-1.87 0-3.39-2.88-3.39-6.42s1.52-6.42 3.39-6.42 3.38 2.88 3.38 6.42M24 12c0 3.17-.53 5.75-1.19 5.75-.66 0-1.19-2.58-1.19-5.75s.53-5.75 1.19-5.75C23.47 6.25 24 8.83 24 12z"/></svg>',
    },
    {
      name: 'LinkedIn',
      url: 'https://www.linkedin.com/in/dilroopus',
      svg: '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg>',
    },
    {
      name: 'Email',
      url: 'mailto:contact@dilroopus.com',
      svg: '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path><polyline points="22,6 12,13 2,6"></polyline></svg>',
    },
  ];
</script>

<footer class="border-t border-white/10 mt-auto">
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 sm:py-8">
    <div class="flex flex-col sm:flex-row justify-between items-center gap-4 sm:gap-6">
      <div class="text-sm text-gray-400 text-center sm:text-left">
        <p>© {currentYear} Designed by <span class="text-white font-medium">Dilroopus</span></p>
      </div>
      
      <div class="flex items-center gap-3 sm:gap-4">
        {#each socialLinks as link}
          <a
            href={link.url}
            target="_blank"
            rel="noopener noreferrer"
            class="w-10 h-10 sm:w-11 sm:h-11 rounded-lg bg-gradient-to-br from-white/5 to-white/10 border border-white/10 flex items-center justify-center text-white/70 hover:text-white hover:border-white/30 hover:from-white/10 hover:to-white/15 transition-all duration-200"
            aria-label={link.name}
          >
            {@html link.svg}
          </a>
        {/each}
      </div>
    </div>
  </div>
</footer>
