<script lang="ts">
    let { children } = $props();
</script>

<div class="leaf">
    {#if children}
        {@render children()}
    {/if}
</div>
