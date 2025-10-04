<script lang="ts">
  import { openDropdownId } from '../stores/dropdown';
  
  export let value: string | number;
  export let options: Array<{value: string | number, label: string, group?: string}>;
  export let id: string = '';
  export let placeholder: string = 'Select an option';
  
  let isOpen = false;
  let selectedLabel = '';
  let dropdownRef: HTMLDivElement;
  let uniqueId = id || `dropdown-${Math.random().toString(36).substr(2, 9)}`;
  
  $: {
    const selected = options.find(opt => opt.value === value);
    selectedLabel = selected ? selected.label : placeholder;
  }
  
  // Close this dropdown when another one opens
  $: if ($openDropdownId !== uniqueId && isOpen) {
    isOpen = false;
  }
  
  function toggleDropdown(event: Event) {
    event.stopPropagation();
    if (isOpen) {
      isOpen = false;
      openDropdownId.set(null);
    } else {
      isOpen = true;
      openDropdownId.set(uniqueId);
    }
  }
  
  function selectOption(optionValue: string | number, event: Event) {
    event.stopPropagation();
    value = optionValue;
    isOpen = false;
    openDropdownId.set(null);
  }
  
  function handleClickOutside(event: MouseEvent) {
    if (isOpen && dropdownRef && !dropdownRef.contains(event.target as Node)) {
      isOpen = false;
      openDropdownId.set(null);
    }
  }
  
  // Group options by their group property
  $: groupedOptions = options.reduce((acc, option) => {
    const groupName = option.group || '';
    if (!acc[groupName]) {
      acc[groupName] = [];
    }
    acc[groupName].push(option);
    return acc;
  }, {} as Record<string, typeof options>);
</script>

<svelte:window on:click={handleClickOutside} />

<div class="custom-select-wrapper" id={uniqueId} bind:this={dropdownRef}>
  <button
    type="button"
    class="w-full bg-gray-800 border border-gray-700 rounded-xl px-4 py-3 text-left flex items-center justify-between hover:border-gray-600 transition-colors focus:outline-none focus:border-gray-600"
    on:click={toggleDropdown}
  >
    <span class="text-white">{selectedLabel}</span>
    <svg 
      class="w-4 h-4 text-gray-400 transition-transform duration-200 {isOpen ? 'rotate-180' : ''}" 
      fill="none" 
      stroke="currentColor" 
      viewBox="0 0 24 24"
    >
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
    </svg>
  </button>
  
  {#if isOpen}
    <div class="dropdown-menu">
      {#each Object.entries(groupedOptions) as [groupName, groupOptions]}
        {#if groupName}
          <div class="dropdown-group-header">
            {groupName}
          </div>
        {/if}
        {#each groupOptions as option}
          <button
            type="button"
            class="dropdown-option {value === option.value ? 'dropdown-option-selected' : ''}"
            on:click={(e) => selectOption(option.value, e)}
          >
            {option.label}
          </button>
        {/each}
      {/each}
    </div>
  {/if}
</div>

<style>
  .custom-select-wrapper {
    position: relative;
    user-select: none;
    z-index: 1;
  }
  
  .custom-select-wrapper:has(.dropdown-menu) {
    z-index: 9999;
  }
  
  .dropdown-menu {
    position: absolute;
    top: calc(100% + 0.5rem);
    left: 0;
    right: 0;
    z-index: 9999;
    background: rgb(31, 41, 55);
    border: 1px solid rgb(55, 65, 81);
    border-radius: 0.75rem;
    box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.5), 0 10px 10px -5px rgba(0, 0, 0, 0.4);
    max-height: 20rem;
    overflow-y: auto;
  }
  
  .dropdown-group-header {
    padding: 0.5rem 1rem;
    font-size: 0.75rem;
    font-weight: 600;
    font-style: italic;
    color: rgb(156, 163, 175);
    background: rgb(17, 24, 39);
  }
  
  .dropdown-option {
    width: 100%;
    padding: 0.75rem 1rem;
    text-align: left;
    color: white;
    background: rgb(31, 41, 55);
    border: none;
    cursor: pointer;
    transition: background-color 150ms;
  }
  
  .dropdown-option:hover {
    background: rgb(75, 85, 99);
  }
  
  .dropdown-option-selected {
    background: rgb(75, 85, 99);
  }
  
  .dropdown-option:first-child {
    border-top-left-radius: 0.75rem;
    border-top-right-radius: 0.75rem;
  }
  
  .dropdown-option:last-child {
    border-bottom-left-radius: 0.75rem;
    border-bottom-right-radius: 0.75rem;
  }
</style>
