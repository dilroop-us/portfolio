<script lang="ts">
  import { Link } from 'svelte-routing';
  import Footer from '../lib/components/layout/Footer.svelte';
  import SkeletonLoader from '../lib/components/loaders/SkeletonLoader.svelte';
  import { fadeSlide } from '../lib/utils/transitions';
  import { onMount, onDestroy } from 'svelte';
  
  interface Message {
    id: number;
    username: string;
    content: string;
    created_at: string;
  }

  interface SessionData {
    token: string;
    username: string;
    expiresAt: string;
  }

  let messages: Message[] = [];
  let messageInput = '';
  let username = '';
  let showUsernameModal = true;
  let isConnected = false;
  let ws: WebSocket | null = null;
  let session: SessionData | null = null;
  let messageContainer: HTMLElement;
  let error = '';
  let loadingHistory = false;

  onMount(() => {
    const savedSession = localStorage.getItem('chatSession');
    if (savedSession) {
      try {
        const parsed = JSON.parse(savedSession);
        if (new Date(parsed.expiresAt) > new Date()) {
          session = parsed;
          showUsernameModal = false;
          loadHistory();
          connectWebSocket();
        } else {
          localStorage.removeItem('chatSession');
        }
      } catch (e) {
        localStorage.removeItem('chatSession');
      }
    }
  });

  onDestroy(() => {
    if (ws) {
      ws.close();
    }
  });

  async function createSession() {
    if (!username.trim()) {
      error = 'Username is required';
      return;
    }

    if (username.length > 50) {
      error = 'Username must be 50 characters or less';
      return;
    }

    if (!/^[a-zA-Z0-9_\s]+$/.test(username)) {
      error = 'Username can only contain letters, numbers, underscores, and spaces';
      return;
    }

    try {
      const response = await fetch('/api/chat/session', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username: username.trim() })
      });

      if (!response.ok) {
        throw new Error('Failed to create session');
      }

      const data = await response.json();
      session = {
        token: data.token,
        username: data.username,
        expiresAt: data.expires_at
      };

      localStorage.setItem('chatSession', JSON.stringify(session));
      showUsernameModal = false;
      error = '';
      
      loadHistory();
      connectWebSocket();
    } catch (e) {
      error = 'Failed to create session. Please try again.';
    }
  }

  async function loadHistory() {
    loadingHistory = true;
    try {
      const response = await fetch('/api/chat/history?limit=200');
      const data = await response.json();
      messages = data;
      setTimeout(scrollToBottom, 100);
    } catch (e) {
      console.error('Failed to load history:', e);
    } finally {
      loadingHistory = false;
    }
  }

  function connectWebSocket() {
    if (!session) return;

    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = `${protocol}//${window.location.host}/api/chat/ws?token=${session.token}`;

    ws = new WebSocket(wsUrl);

    ws.onopen = () => {
      isConnected = true;
    };

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      
      if (data.error) {
        console.error('WebSocket error:', data.error);
        return;
      }

      if (data.id) {
        messages = [...messages, data];
        setTimeout(scrollToBottom, 10);
      }
    };

    ws.onclose = () => {
      isConnected = false;
      setTimeout(() => {
        if (session && new Date(session.expiresAt) > new Date()) {
          connectWebSocket();
        }
      }, 3000);
    };

    ws.onerror = () => {
      isConnected = false;
    };
  }

  function sendMessage() {
    if (!messageInput.trim() || !ws || !isConnected) return;

    if (messageInput.length > 500) {
      alert('Message must be 500 characters or less');
      return;
    }

    ws.send(JSON.stringify({ content: messageInput.trim() }));
    messageInput = '';
  }

  function scrollToBottom() {
    if (messageContainer) {
      messageContainer.scrollTop = messageContainer.scrollHeight;
    }
  }

  function formatTime(dateString: string) {
    const date = new Date(dateString);
    return date.toLocaleTimeString('en-US', { 
      hour: '2-digit', 
      minute: '2-digit' 
    });
  }

  function handleKeyPress(e: KeyboardEvent) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  }
</script>

{#if showUsernameModal}
  <div class="fixed inset-0 bg-black/80 backdrop-blur-sm flex items-center justify-center z-50 p-4">
    <div class="card max-w-md w-full">
      <h2 class="text-3xl font-display font-bold text-white mb-2">Welcome to Chat</h2>
      <p class="text-white/60 mb-6">Choose a username to start chatting. Your session lasts 24 hours.</p>
      
      <div class="mb-4">
        <label for="chat-username-input" class="block text-sm font-medium text-white/60 mb-2">Username</label>
        <input
          id="chat-username-input"
          type="text"
          bind:value={username}
          on:keypress={(e) => e.key === 'Enter' && createSession()}
          class="input-field"
          placeholder="Enter your username..."
          maxlength="50"
        />
      </div>

      {#if error}
        <div class="mb-4 p-3 bg-white/[0.02] border border-white/[0.08] rounded-lg text-white/70 text-sm">
          {error}
        </div>
      {/if}

      <button
        on:click={createSession}
        class="btn-primary w-full"
      >
        Start Chatting
      </button>
    </div>
  </div>
{/if}

<div class="container mx-auto px-4 py-24">
  <h1 class="text-4xl font-bold mb-6 text-gradient">
    Live Chat
  </h1>
  <p class="text-gray-400 mb-12 text-lg">
    Real-time messaging with WebSocket. Join the conversation!
  </p>
  
  <div class="max-w-7xl mx-auto px-6">

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
      <div class="lg:col-span-2 card flex flex-col h-[600px]">
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-2xl font-bold text-white">💬 Messages</h3>
          <div class="flex items-center gap-2 px-3 py-2 bg-white/[0.02] border border-white/[0.08] rounded-lg">
            <div class={`w-2.5 h-2.5 rounded-full transition-colors ${isConnected ? 'bg-white' : 'bg-white/30'}`}></div>
            <span class="text-sm text-white/60">{isConnected ? 'Connected' : 'Disconnected'}</span>
          </div>
        </div>
        
        <div bind:this={messageContainer} class="flex-1 overflow-y-auto mb-4 space-y-3 pr-2">
          {#if loadingHistory}
            <div class="space-y-3">
              {#each [1, 2, 3, 4, 5] as _}
                <SkeletonLoader height="80px" />
              {/each}
            </div>
          {:else if messages.length === 0}
            <div class="text-center py-12 text-white/40">
              <svg class="w-16 h-16 mx-auto mb-4 opacity-50" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
              </svg>
              <p>No messages yet. Be the first to say hello!</p>
            </div>
          {:else}
            {#each messages as message (message.id)}
              <div class="bg-white/[0.02] border border-white/[0.08] rounded-xl p-4 transition-all duration-150 hover:bg-white/[0.04]">
                <div class="flex items-center justify-between mb-2">
                  <span class="font-semibold text-white">{message.username}</span>
                  <span class="text-xs text-white/40">{formatTime(message.created_at)}</span>
                </div>
                <p class="text-white/70">{message.content}</p>
              </div>
            {/each}
          {/if}
        </div>

        <div class="border-t border-white/[0.08] pt-4">
          <div class="flex gap-3">
            <input
              type="text"
              bind:value={messageInput}
              on:keypress={handleKeyPress}
              disabled={!isConnected}
              class="input-field flex-1"
              placeholder={isConnected ? "Type your message..." : "Connecting..."}
              maxlength="500"
            />
            <button
              on:click={sendMessage}
              disabled={!isConnected || !messageInput.trim()}
              class="btn-primary whitespace-nowrap"
            >
              Send
            </button>
          </div>
          <p class="text-xs text-white/40 mt-2">
            {#if session}
              Chatting as <span class="text-white font-medium">{session.username}</span> • Session expires in 24 hours
            {/if}
          </p>
        </div>
      </div>

      <div class="card h-fit">
        <h2 class="text-2xl font-display font-bold text-white mb-6">How It Works</h2>
        <div class="space-y-6">
          <div>
            <div class="flex items-center gap-2 mb-2">
              <div class="w-8 h-8 rounded-lg bg-white/[0.04] border border-white/[0.08] flex items-center justify-center">
                <span class="text-lg">🔐</span>
              </div>
              <h3 class="text-lg font-semibold text-white">Temporary Sessions</h3>
            </div>
            <p class="text-sm text-white/60 ml-10">Choose a username and get a 24-hour session. No registration required!</p>
          </div>
          <div>
            <div class="flex items-center gap-2 mb-2">
              <div class="w-8 h-8 rounded-lg bg-white/[0.04] border border-white/[0.08] flex items-center justify-center">
                <span class="text-lg">⚡</span>
              </div>
              <h3 class="text-lg font-semibold text-white">Real-Time WebSocket</h3>
            </div>
            <p class="text-sm text-white/60 ml-10">Messages are instantly delivered to all connected users via WebSocket protocol.</p>
          </div>
          <div>
            <div class="flex items-center gap-2 mb-2">
              <div class="w-8 h-8 rounded-lg bg-white/[0.04] border border-white/[0.08] flex items-center justify-center">
                <span class="text-lg">🛡️</span>
              </div>
              <h3 class="text-lg font-semibold text-white">Rate Limiting</h3>
            </div>
            <p class="text-sm text-white/60 ml-10">Built-in rate limiting (5 messages per 10 seconds) prevents spam and abuse.</p>
          </div>
          <div>
            <div class="flex items-center gap-2 mb-2">
              <div class="w-8 h-8 rounded-lg bg-white/[0.04] border border-white/[0.08] flex items-center justify-center">
                <span class="text-lg">💾</span>
              </div>
              <h3 class="text-lg font-semibold text-white">Message Persistence</h3>
            </div>
            <p class="text-sm text-white/60 ml-10">Messages are stored in PostgreSQL and displayed when you join the chat.</p>
          </div>
        </div>
      </div>
    </div>

    <div class="card">
      <h2 class="text-2xl font-display font-bold text-white mb-4">Technical Implementation</h2>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div class="bg-white/[0.02] border border-white/[0.08] rounded-lg p-4">
          <h3 class="font-semibold text-white mb-2">Frontend</h3>
          <ul class="text-sm text-white/60 space-y-1">
            <li>• WebSocket connection with auto-reconnect</li>
            <li>• LocalStorage session persistence</li>
            <li>• Real-time message updates</li>
            <li>• Message validation (1-500 chars)</li>
          </ul>
        </div>
        <div class="bg-white/[0.02] border border-white/[0.08] rounded-lg p-4">
          <h3 class="font-semibold text-white mb-2">Backend</h3>
          <ul class="text-sm text-white/60 space-y-1">
            <li>• WebSocket connection manager</li>
            <li>• JWT token authentication</li>
            <li>• PostgreSQL message persistence</li>
            <li>• Rate limiting middleware</li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</div>

<Footer />
