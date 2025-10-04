<script lang="ts">
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

<div class="glass rounded-xl p-8">
  <h3 class="text-2xl font-bold mb-6 text-blue-400">📬 Get In Touch</h3>
  <p class="text-gray-300 mb-6">Interested in backend development projects? Let's discuss your needs.</p>
  
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
      <div class="p-4 bg-green-600/20 border border-green-600/40 rounded-lg text-green-400">
        ✅ Message sent successfully! I'll get back to you soon.
      </div>
    {/if}
    
    {#if error}
      <div class="p-4 bg-red-600/20 border border-red-600/40 rounded-lg text-red-400">
        ❌ {error}
      </div>
    {/if}
  </form>
</div>
