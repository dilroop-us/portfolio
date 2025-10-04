<script>
  export let cols = '1';
  export let gap = '6';
  export let className = '';
  
  const colsMap = {
    '1': 'grid-cols-1',
    '2': 'grid-cols-1 md:grid-cols-2',
    '3': 'grid-cols-1 md:grid-cols-2 lg:grid-cols-3',
    '4': 'grid-cols-1 md:grid-cols-2 lg:grid-cols-4',
    '12': 'grid-cols-12',
  };
  
  const gapMap = {
    '3': 'gap-3',
    '4': 'gap-4',
    '6': 'gap-4 md:gap-6',
    '8': 'gap-6 md:gap-8',
  };
</script>

<div class="grid {colsMap[cols]} {gapMap[gap]} {className}">
  <slot />
</div>
