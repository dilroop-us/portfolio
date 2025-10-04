<script>
  export let variant = 'default';
  export let hover = true;
  export let padding = 'default';

  const variants = {
    default: 'glass rounded-2xl hover:border-primary-500/40 hover:shadow-glow-lg',
    compact: 'glass rounded-xl hover:border-primary-500/40',
    elevated: 'bg-surface-elevated border border-gray-800 rounded-2xl shadow-lg',
  };
  
  const paddings = {
    none: 'p-0',
    sm: 'p-4 sm:p-6',
    default: 'p-6 sm:p-8',
    lg: 'p-8 sm:p-10',
  };
  
  const hoverClass = hover ? 'transition-all duration-300' : '';
  const classes = `${variants[variant]} ${paddings[padding]} ${hoverClass}`;
</script>

<div class={classes}>
  <slot />
</div>
