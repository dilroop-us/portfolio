<script>
  export let variant = 'standard';
  export let className = '';

  const variants = {
    spacious: 'py-24 md:py-32',
    standard: 'py-20 md:py-24',
    compact: 'py-12 md:py-16',
  };
</script>

<section class="{variants[variant]} {className}">
  <slot />
</section>
