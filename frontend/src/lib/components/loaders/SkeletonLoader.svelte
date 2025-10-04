<script lang="ts">
  export let height = '100%';
  export let width = '100%';
  export let rounded = true;
</script>

<div 
  class="skeleton-loader" 
  class:rounded-xl={rounded}
  style="height: {height}; width: {width};"
></div>
