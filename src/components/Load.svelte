<script lang="ts">
    import { ROOT_URL } from "../api/backend";

    let { children, until } = $props();
</script>

{#if until}
    {@render children()}
{:else}
    <h1 class="dodge-topbar">
        Load Screen Placeholder<br /> Connecting to server: {ROOT_URL}
    </h1>
{/if}
