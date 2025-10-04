<script>
  export let variant = 'primary';
  export let size = 'md';

  const variants = {
    primary: 'bg-white/10 text-white border-white/20',
    success: 'bg-white/15 text-gray-200 border-white/25',
    warning: 'bg-white/12 text-gray-300 border-white/22',
    error: 'bg-white/10 text-gray-400 border-white/20',
    info: 'bg-white/13 text-gray-200 border-white/23',
  };
  
  const sizes = {
    sm: 'px-2 py-0.5 text-xs',
    md: 'px-3 py-1 text-xs',
    lg: 'px-4 py-2 text-sm',
  };
  
  const classes = `inline-flex items-center gap-1.5 rounded-full border font-medium ${variants[variant]} ${sizes[size]}`;
</script>

<span class={classes}>
  <slot />
</span>
