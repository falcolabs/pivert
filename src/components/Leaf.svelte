<script lang="ts">
    import { fade } from "svelte/transition";

    let { children } = $props();
</script>

<div transition:fade={{ duration: 50 }} class="leaf">
    {#if children}
        {@render children()}
    {/if}
</div>
