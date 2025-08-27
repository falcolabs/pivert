<script lang="ts">
    let { activeSection, swipeTo } = $props();
    import { House, Earth, Dumbbell, Store, Settings } from '@lucide/svelte';

    const sections = {
        home: House,
        social: Earth,
        train: Dumbbell,
        rewards: Store,
        settings: Settings
    }

    const changeSection = (id: string) => () => {
        swipeTo(id)
    }

</script>

<div class="navbar">
    {#each Object.entries(sections) as [id, icon]}
        {@const ButtonIcon = icon}
        <button class="nav-btn" class:active={id == activeSection} onclick={changeSection(id)}>
            <ButtonIcon color={`var(${id == activeSection ? "--theme-color-accent-contrast" : "--theme-color-foreground"})`} />
        </button>
    {/each}
</div>

<style lang="scss">
    @use "../styles/_theme.sass";

    .navbar {
        display: flex;
        flex-direction: row;
        align-items: center;
        justify-content: space-around;
        gap: 0.25rem;
        background-color: theme.get(slate);
        border-radius: 3rem;
        padding: 0.25rem;
        margin-bottom: 0.5rem;
    }

    
    .nav-btn {
        width: 3rem;
        height: 3rem;
        display: flex;
        align-items: center;
        justify-content: center;
        background-color: theme.get(bedrock);
        border-radius: 3rem;
        transition: ease 100ms;
    }

    .nav-btn:hover {
        filter: brightness(0.9);
    }

    .active {
        background-color: theme.get(accent);
    }
</style>