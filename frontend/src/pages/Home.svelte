<script lang="ts">
  import { onMount } from 'svelte';
  import { Link } from 'svelte-routing';
  import Container from '../lib/components/layout/Container.svelte';
  import Section from '../lib/components/layout/Section.svelte';
  import Grid from '../lib/components/layout/Grid.svelte';
  import Card from '../lib/components/ui/Card.svelte';
  import Badge from '../lib/components/ui/Badge.svelte';
  import Button from '../lib/components/ui/Button.svelte';
  import Footer from '../lib/components/layout/Footer.svelte';
  import ScrollReveal from '../lib/components/animations/ScrollReveal.svelte';
  import SkeletonLoader from '../lib/components/loaders/SkeletonLoader.svelte';
  import { fadeSlide } from '../lib/utils/transitions';
  
  let projects: any[] = [];
  let skills: any[] = [];
  let loading = true;
  
  onMount(async () => {
    try {
      const [projectsRes, skillsRes] = await Promise.all([
        fetch('/api/projects'),
        fetch('/api/skills')
      ]);
      
      projects = await projectsRes.json();
      skills = await skillsRes.json();
    } catch (error) {
      console.error('Error fetching data:', error);
    } finally {
      loading = false;
    }
  });
</script>

<Section variant="spacious" className="min-h-screen flex items-center">
  <Container className="text-center">
    <div in:fadeSlide={{ delay: 0 }} class="text-sm font-mono gradient-text mb-6 font-bold">FULLSTACK ENGINEER • BACKEND FOCUSED</div>
    <h1 in:fadeSlide={{ delay: 80 }} class="mb-6 text-balance gradient-text">
      Dilroop Ummar Shameem
    </h1>
    <p in:fadeSlide={{ delay: 160 }} class="text-body-lg text-gray-300 mb-12 max-w-3xl mx-auto">Building scalable systems with heavy backends & lightweight frontends</p>
    <div in:fadeSlide={{ delay: 240 }} class="flex gap-3 justify-center mb-12 flex-wrap">
      <Badge variant="primary" size="lg">Python</Badge>
      <Badge variant="primary" size="lg">Django</Badge>
      <Badge variant="primary" size="lg">FastAPI</Badge>
      <Badge variant="primary" size="lg">PostgreSQL</Badge>
      <Badge variant="primary" size="lg">SvelteKit</Badge>
    </div>
    <div in:fadeSlide={{ delay: 320 }}>
      <Link to="/playground/jwt">
        <Button variant="primary" size="lg">
          Explore Interactive Demos →
        </Button>
      </Link>
    </div>
  </Container>
</Section>

<Section variant="standard">
  <Container>
    <ScrollReveal>
      <h2 class="text-center text-gradient-cyan mb-16">About Me</h2>
    </ScrollReveal>
    <Grid cols="2" gap="6">
      <ScrollReveal delay={0}>
        <Card>
          <h3 class="gradient-text mb-4">🎯 Expertise</h3>
          <p class="text-gray-300 leading-relaxed">
            Fullstack engineer with backend focus, specializing in building scalable, event-driven systems. 
            I build heavy, robust backends with Python (FastAPI, Django) and pair them with 
            lightweight, performant frontends using SvelteKit, Astro, and modern frameworks.
          </p>
        </Card>
      </ScrollReveal>
      <ScrollReveal delay={80}>
        <Card>
          <h3 class="gradient-text mb-4">💡 Philosophy</h3>
          <p class="text-gray-300 leading-relaxed">
            I believe in clean code, test-driven development, and continuous learning. 
            My approach combines solid engineering principles with modern best practices 
            to deliver robust, maintainable solutions.
          </p>
        </Card>
      </ScrollReveal>
    </Grid>
  </Container>
</Section>

<Section variant="standard">
  <Container>
    <ScrollReveal>
      <h2 class="text-center text-gradient-cyan mb-16">Featured Projects</h2>
    </ScrollReveal>
    
    {#if loading}
      <Grid cols="2" gap="6">
        {#each [1, 2] as _}
          <SkeletonLoader height="300px" />
        {/each}
      </Grid>
    {:else}
      <Grid cols="2" gap="6">
        {#each projects as project, index}
          <ScrollReveal delay={index * 80}>
            <Card>
              <h3 class="mb-4 text-white">{project.title}</h3>
              <p class="text-gray-400 mb-6">{project.description}</p>
              <div class="flex flex-wrap gap-2 mb-6">
                {#each project.tech_stack.split(',') as tech}
                  <Badge variant="primary" size="sm">{tech.trim()}</Badge>
                {/each}
              </div>
              <div class="grid grid-cols-3 gap-4 pt-6 border-t border-white/10">
                <div class="text-center">
                  <div class="text-xl font-bold gradient-text">{project.throughput}</div>
                  <div class="text-caption text-gray-500 uppercase">Performance</div>
                </div>
                <div class="text-center">
                  <div class="text-xl font-bold gradient-text">{project.latency}</div>
                  <div class="text-caption text-gray-500 uppercase">Optimization</div>
                </div>
                <div class="text-center">
                  <div class="text-xl font-bold gradient-text">{project.uptime}</div>
                  <div class="text-caption text-gray-500 uppercase">Uptime</div>
                </div>
              </div>
            </Card>
          </ScrollReveal>
        {/each}
      </Grid>
    {/if}
  </Container>
</Section>

<Section variant="standard">
  <Container>
    <ScrollReveal>
      <h2 class="text-center text-gradient-cyan mb-16">Technical Skills</h2>
    </ScrollReveal>
    
    {#if loading}
      <Grid cols="2" gap="6">
        {#each [1, 2, 3, 4] as _}
          <SkeletonLoader height="120px" />
        {/each}
      </Grid>
    {:else}
      <Grid cols="2" gap="6">
        {#each skills as skill, index}
          <ScrollReveal delay={index * 60}>
            <Card variant="compact">
              <div class="flex justify-between mb-3">
                <span class="font-semibold text-lg text-white">{skill.name}</span>
                <span class="gradient-text font-bold">{skill.proficiency}%</span>
              </div>
              <div class="w-full bg-white/10 rounded-full h-2.5 overflow-hidden mb-3">
                <div 
                  class="h-full transition-all duration-1000"
                  style="width: {skill.proficiency}%; background: linear-gradient(135deg, #ffffff 0%, #a3a3a3 50%, #525252 100%);"
                ></div>
              </div>
              <p class="text-caption text-gray-500 uppercase">{skill.category} • {skill.years_experience} years</p>
            </Card>
          </ScrollReveal>
        {/each}
      </Grid>
    {/if}
  </Container>
</Section>

<Section variant="spacious">
  <Container>
    <ScrollReveal>
      <h2 class="text-center text-gradient-cyan mb-8">Interactive Learning Playground</h2>
      <p class="text-center text-gray-400 mb-16 text-body-lg max-w-3xl mx-auto">
        Explore backend concepts through interactive demos and learn how things work behind the scenes
      </p>
    </ScrollReveal>
    
    <Grid cols="2" gap="6">
      
      <ScrollReveal delay={80}>
        <Link to="/playground/api">
          <Card hover={true}>
            <div class="text-5xl mb-6">🚀</div>
            <h3 class="gradient-text mb-4">API Playground</h3>
            <p class="text-gray-300">
              Live API testing tool with custom methods, headers, and request bodies. 
              Test any API endpoint with real-time response visualization.
            </p>
          </Card>
        </Link>
      </ScrollReveal>
      
      <ScrollReveal delay={160}>
        <Link to="/playground/database">
          <Card hover={true}>
            <div class="text-5xl mb-6">💾</div>
            <h3 class="gradient-text mb-4">Database Challenge</h3>
            <p class="text-gray-300">
              Write SQL queries with EXPLAIN ANALYZE and optimization tips. 
              Learn query performance, indexing, and database design.
            </p>
          </Card>
        </Link>
      </ScrollReveal>
      
      <ScrollReveal delay={240}>
        <Link to="/playground/caching">
          <Card hover={true}>
            <div class="text-5xl mb-6">⚡</div>
            <h3 class="gradient-text mb-4">Caching Playground</h3>
            <p class="text-gray-300">
              Explore multi-level caching with L1 in-memory and L2 Redis. 
              Learn cache strategies, TTL management, and performance optimization.
            </p>
          </Card>
        </Link>
      </ScrollReveal>

      <ScrollReveal delay={320}>
        <Link to="/playground/chat">
          <Card hover={true}>
            <div class="text-5xl mb-6">💬</div>
            <h3 class="gradient-text mb-4">Chat Playground</h3>
            <p class="text-gray-300">
              Build a real-time chat app with WebSockets and message persistence. 
              Learn about real-time communication and state management.
            </p>
          </Card>
        </Link>
      </ScrollReveal>
      
    </Grid>
  </Container>
</Section>

<Footer />
