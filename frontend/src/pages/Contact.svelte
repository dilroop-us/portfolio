<script lang="ts">
  import { Link } from 'svelte-routing';
  import Footer from '../lib/components/layout/Footer.svelte';
  
  let name = '';
  let email = '';
  let company = '';
  let message = '';
  let loading = false;
  let success = false;
  let error = '';
  
  async function submitForm() {
    loading = true;
    success = false;
    error = '';
    
    try {
      const res = await fetch('/api/contact', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, email, company, message })
      });
      
      if (res.ok) {
        success = true;
        name = '';
        email = '';
        company = '';
        message = '';
        setTimeout(() => success = false, 5000);
      } else {
        error = 'Failed to send message. Please try again.';
      }
    } catch (err) {
      error = 'Network error. Please check your connection.';
    } finally {
      loading = false;
    }
  }
</script>

<div class="container mx-auto px-4 py-24">
  <h1 class="text-4xl font-bold mb-6 text-gradient">
    Get In Touch
  </h1>
  <p class="text-gray-400 mb-12 text-lg">
    Interested in fullstack development with robust backends? Let's discuss your needs and build something amazing together.
  </p>
  
  <div class="max-w-7xl mx-auto px-6">
    
    <div class="grid lg:grid-cols-2 gap-12">
      <div class="card">
        <h3 class="text-2xl font-bold mb-6 text-white">📬 Contact Form</h3>
        
        <form on:submit|preventDefault={submitForm} class="space-y-4">
          <div>
            <label for="contact-name" class="block text-sm font-medium mb-2">Name *</label>
            <input 
              id="contact-name"
              bind:value={name}
              required
              class="w-full bg-gray-800 border border-gray-700 rounded-lg px-4 py-2"
              placeholder="Your name"
            />
          </div>
          
          <div>
            <label for="contact-email" class="block text-sm font-medium mb-2">Email *</label>
            <input 
              id="contact-email"
              bind:value={email}
              type="email"
              required
              class="w-full bg-gray-800 border border-gray-700 rounded-lg px-4 py-2"
              placeholder="your.email@example.com"
            />
          </div>
          
          <div>
            <label for="contact-company" class="block text-sm font-medium mb-2">Company (Optional)</label>
            <input 
              id="contact-company"
              bind:value={company}
              class="w-full bg-gray-800 border border-gray-700 rounded-lg px-4 py-2"
              placeholder="Your company"
            />
          </div>
          
          <div>
            <label for="contact-message" class="block text-sm font-medium mb-2">Message *</label>
            <textarea 
              id="contact-message"
              bind:value={message}
              required
              class="w-full bg-gray-800 border border-gray-700 rounded-lg px-4 py-2 h-32"
              placeholder="Tell me about your project..."
            ></textarea>
          </div>
          
          <button 
            type="submit"
            disabled={loading}
            class="btn-primary w-full"
          >
            {loading ? 'Sending...' : 'Send Message'}
          </button>
          
          {#if success}
            <div class="p-4 bg-white/10 border border-white/20 rounded-lg text-white">
              ✅ Message sent successfully! I'll get back to you soon.
            </div>
          {/if}
          
          {#if error}
            <div class="p-4 bg-white/10 border border-white/20 rounded-lg text-gray-300">
              ❌ {error}
            </div>
          {/if}
        </form>
      </div>
      
      <div class="space-y-6">
        <div class="card">
          <h3 class="text-2xl font-bold mb-4 text-white">💼 Services I Offer</h3>
          <ul class="space-y-3 text-gray-400">
            <li class="flex items-start gap-3">
              <span class="text-white">✓</span>
              <span>Fullstack Development (Heavy Backend + Lightweight Frontend)</span>
            </li>
            <li class="flex items-start gap-3">
              <span class="text-white">✓</span>
              <span>REST API Development with FastAPI/Django</span>
            </li>
            <li class="flex items-start gap-3">
              <span class="text-white">✓</span>
              <span>Modern Frontends with SvelteKit & Astro</span>
            </li>
            <li class="flex items-start gap-3">
              <span class="text-white">✓</span>
              <span>Database Design & Optimization (PostgreSQL, Redis)</span>
            </li>
            <li class="flex items-start gap-3">
              <span class="text-white">✓</span>
              <span>Caching & Performance (Redis, Query Optimization)</span>
            </li>
            <li class="flex items-start gap-3">
              <span class="text-white">✓</span>
              <span>Cloud Deployment (AWS, Docker)</span>
            </li>
          </ul>
        </div>
        
        <div class="card">
          <h3 class="text-2xl font-bold mb-4 text-gray-200">⏰ Response Time</h3>
          <p class="text-gray-400">
            I typically respond to inquiries within 24-48 hours. For urgent projects, 
            please mention it in your message.
          </p>
        </div>
        
        <div class="card">
          <h3 class="text-2xl font-bold mb-4 text-white">🤝 Work Approach</h3>
          <p class="text-gray-400">
            I believe in clear communication, agile development, and delivering 
            high-quality solutions. Every project starts with understanding your 
            requirements and ends with a robust, scalable system.
          </p>
        </div>
      </div>
    </div>
  </div>
</div>

<Footer />
