<script lang="ts">
    import Navbar from "../components/Navbar.svelte";
    import Home from "../components/sections/Home.svelte";
    import Social from "../components/sections/Social.svelte";
    import gsap from "gsap";
    import { loggedIn, requests } from "../api";
    import Login from "../components/sections/Login.svelte";
    import { fade } from "svelte/transition";
    import Train from "../components/sections/Train.svelte";
    import Settings from "../components/sections/Settings.svelte";
    import Rewards from "../components/sections/Rewards.svelte";
    import Load from "../components/Load.svelte";

    requests.log("here");

    let activeSection: keyof typeof SECTIONS_INDEX = $state("home");
    const SECTIONS_INDEX = {
        home: 0,
        social: 1,
        train: 2,
        rewards: 3,
        settings: 4,
    };
    let section_list: number[] = $state([0]);

    const swipeTo = (id: keyof typeof SECTIONS_INDEX) => {
        if (id == activeSection) return;
        let destination = SECTIONS_INDEX[id];
        let current = SECTIONS_INDEX[activeSection];
        // if (destination > current) {
        //     section_list.push(destination);
        //     gsap.to(".content:first-child", { x: "-50%", duration: 0.1 });
        //     setTimeout(() => {
        //         section_list.shift();
        //         gsap.to(".content:first-child", { x: 0, y: 0, duration: 0 });
        //     }, 150);
        // } else {
        //     section_list.unshift(destination);
        //     gsap.to(".content:first-child", { x: "-50%", duration: 0 });
        //     section_list.pop();
        //     gsap.to(".content:first-child", { x: 0, y: 0, duration: 0.1 });
        // }
        activeSection = id;
    };
</script>

{#snippet section(sid: number)}
    {#if sid == SECTIONS_INDEX.home}
        <Home changeSection={swipeTo} />
    {:else if sid == SECTIONS_INDEX.social}
        <Social />
    {:else if sid == SECTIONS_INDEX.train}
        <Train />
    {:else if sid == SECTIONS_INDEX.rewards}
        <Rewards />
    {:else if sid == SECTIONS_INDEX.settings}
        <Settings />
    {/if}
{/snippet}

<main class="theme-light">
    <svelte:boundary>
        {#if $loggedIn === true}
            <div
                transition:fade={{ duration: 50 }}
                class="container-with-navbar"
            >
                <div class="content">
                    {@render section(SECTIONS_INDEX[activeSection])}
                </div>
                <div class="nav">
                    <Navbar {activeSection} {swipeTo} />
                </div>
            </div>
        {:else if $loggedIn === false}
            <div class="login-container" transition:fade={{ duration: 100 }}>
                <Login />
            </div>
        {:else if $loggedIn === null}
            <Load until={false}>
                <br />
            </Load>
        {/if}
        {#snippet pending()}
            <Load until={false}>
                <br />
            </Load>
        {/snippet}
    </svelte:boundary>
</main>

<style lang="scss">
    @use "../styles/_theme.sass";

    .nav {
        position: fixed;
        bottom: 0.75rem;
        left: 50%;
        transform: translate(-50%);
    }

    .container-with-navbar {
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
            max-width: 100vw;
            transition: cubic-bezier(0.075, 0.82, 0.165, 1);
        }
    }

    main {
        height: 100%;
    }

    .login-container {
        height: 100%;
    }

    p {
        color: theme.get(accent);
    }
</style>
