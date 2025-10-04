<script>
  export let variant = 'primary';
  export let size = 'md';
  export let disabled = false;
  export let type = 'button';
  export let fullWidth = false;

  const baseClasses = 'font-medium transition-all duration-200 active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed';
  
  const variants = {
    primary: 'btn-primary',
    secondary: 'btn-secondary',
    ghost: 'btn-ghost',
    danger: 'bg-white/10 border border-white/20 text-gray-300 hover:bg-white/20',
  };
  
  const sizes = {
    sm: 'px-4 py-2 text-sm rounded-lg',
    md: 'px-6 py-3 text-base rounded-xl',
    lg: 'px-8 py-4 text-lg rounded-xl',
  };
  
  const classes = `${baseClasses} ${variants[variant]} ${sizes[size]} ${fullWidth ? 'w-full' : ''}`;
</script>

<button 
  {type}
  {disabled}
  class={classes}
  on:click
>
  <slot />
</button>
