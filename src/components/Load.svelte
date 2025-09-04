<script lang="ts">
    let { children, until } = $props();
</script>

{#if until}
    {@render children()}
{:else}
    <p>Loading...</p>
{/if}