<script lang="ts">
    import Navbar from "../components/Navbar.svelte";
    import Home from "../components/sections/Home.svelte";
    import Social from "../components/sections/Social.svelte";
    import gsap from "gsap";
    import { isLoggedIn, login, requests, loadStore } from "../api";
    import Login from "../components/sections/Login.svelte";
    import { onMount } from "svelte";

    onMount(async () => {
        await loadStore();
    })

    let activeSection = $state("home");
    const SECTIONS_INDEX: {[key: string]: number} = {
        home: 0,
        social: 1,
        train: 2,
        rewards: 3,
        settings: 4
    }
    let section_list: number[] = $state([0])

    const swipeTo = (id: string) => {
        if (id == activeSection) return;
        let destination = SECTIONS_INDEX[id];
        let current = SECTIONS_INDEX[activeSection];
        if (destination > current) {
            section_list.push(destination)
            gsap.to(".content:first-child",  { x: "-50%", duration: 0.1})
            setTimeout(() => {section_list.shift(); gsap.to(".content:first-child", { x: 0, y: 0, duration: 0})}, 150)
        } else {
            section_list.unshift(destination)
            gsap.to(".content:first-child",  { x: "-50%", duration: 0})
            section_list.pop();
            gsap.to(".content:first-child", { x: 0, y: 0, duration: 0.1})
        }
        activeSection = id;
    }
</script>

{#snippet section(sid: number)}
    {#if sid == SECTIONS_INDEX["home"]}
        <Home />
    {:else if sid == SECTIONS_INDEX["social"]}
        <Social />
    {/if}
{/snippet}

<main class="container theme-light">
    dasddasd
    <svelte:boundary>
        {#if await isLoggedIn()}
            <div class="content">
                {#each section_list as id}
                    <div>
                        {@render section(id)}
                    </div>
                {/each}
            </div>
            <div class="nav">
                <Navbar {activeSection} {swipeTo} />
            </div>
        {:else}
            <Login />
        {/if}
        {#snippet pending()}{/snippet}
    </svelte:boundary>
</main>

<style lang="scss">
    @use "../styles/_theme";

    .nav {
        position: fixed;
        bottom: 0.75rem;
        left: 50%;
        transform: translate(-50%);
    }

    .container {
        // padding-top: 1rem;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        align-items: start;
    }

    .content {
        display: flex;
        flex-direction: row;
        align-items: start;

        div {
            width: 100vw;
            transition: cubic-bezier(0.075, 0.82, 0.165, 1);
        }
    }

    main {
        height: 100%;
    }

    p {
        color: theme.get(accent);
    }
</style>
