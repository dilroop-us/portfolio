<script lang="ts">
  let command = '';
  let output: string[] = ['Welcome to Dilroop\'s Portfolio Terminal', 'Type "help" for available commands', ''];
  let history: string[] = [];
  let historyIndex = -1;
  
  const commands: Record<string, string> = {
    help: 'Available commands: about, skills, projects, contact, clear',
    about: 'Fullstack Engineer (Backend Focused) • Heavy backends with Python (FastAPI, Django) • Lightweight frontends with SvelteKit & Astro',
    skills: 'Python • FastAPI • Django • PostgreSQL • MongoDB • Redis • SvelteKit • Docker • AWS',
    projects: '1. Smart Community Platform\n2. Multi-Seller E-commerce',
    contact: 'Email: dilroopsummer@gmail.com\nLinkedIn: linkedin.com/in/dilroopus\nGitHub: github.com/dilroop-us',
    clear: 'CLEAR',
    whoami: 'dilroop@portfolio:~$ Fullstack Engineer (Backend Focused)',
  };
  
  function executeCommand() {
    if (!command.trim()) return;
    
    output = [...output, `$ ${command}`];
    history = [...history, command];
    historyIndex = history.length;
    
    const cmd = command.toLowerCase().trim();
    
    if (cmd === 'clear') {
      output = [];
    } else if (commands[cmd]) {
      output = [...output, commands[cmd], ''];
    } else {
      output = [...output, `Command not found: ${cmd}. Type "help" for available commands.`, ''];
    }
    
    command = '';
    setTimeout(() => {
      const terminal = document.getElementById('terminal-output');
      if (terminal) terminal.scrollTop = terminal.scrollHeight;
    }, 0);
  }
  
  function handleKeydown(e: KeyboardEvent) {
    if (e.key === 'ArrowUp') {
      e.preventDefault();
      if (historyIndex > 0) {
        historyIndex--;
        command = history[historyIndex];
      }
    } else if (e.key === 'ArrowDown') {
      e.preventDefault();
      if (historyIndex < history.length - 1) {
        historyIndex++;
        command = history[historyIndex];
      } else {
        historyIndex = history.length;
        command = '';
      }
    }
  }
</script>

<div class="glass rounded-xl p-8">
  <h3 class="text-2xl font-bold mb-6 text-cyan-400">💻 Interactive Terminal</h3>
  
  <div class="bg-gray-900 rounded-lg p-4 font-mono text-sm">
    <div id="terminal-output" class="h-64 overflow-y-auto mb-4 text-green-400">
      {#each output as line}
        <div class="whitespace-pre-wrap">{line}</div>
      {/each}
    </div>
    
    <div class="flex items-center">
      <span class="text-green-400 mr-2">$</span>
      <input 
        bind:value={command}
        on:keydown={(e) => {
          if (e.key === 'Enter') executeCommand();
          else handleKeydown(e);
        }}
        class="flex-1 bg-transparent outline-none text-green-400"
        placeholder="Type a command..."
      />
    </div>
  </div>
</div>
