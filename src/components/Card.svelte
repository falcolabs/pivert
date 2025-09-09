<script lang="ts">
    import type { Component } from "svelte";
    import { monoco } from "@monokai/monoco-svelte";

    let {
        children,
        bg = "slate",
        fg = "foreground",
        title,
        icon,
        iconAlign = "left",
        onclick = () => {},
        class: className = "",
    }: {
        children: any;
        bg?: string;
        fg?: string;
        title: string;
        icon: Component;
        iconAlign?: "left" | "right";
        onclick?: () => void;
        class?: string;
    } = $props();
</script>

{#if children}
    {@const CardIcon = icon}
    <div
        class="block"
        use:monoco={{
            borderRadius: 24,
            smoothing: 0.6,
            clip: true,
        }}
    >
        <div
            class={"flex flex-col py-5 px-6 gap-2 h-full" + className}
            style={`background-color: var(--theme-color-${bg}); color: var(--theme-color-${fg});`}
        >
            <button
                {onclick}
                class="flex flex-row items-center gap-4"
                class:reversed-orientation={iconAlign == "right"}
            >
                <div class="flex p-3 bg-bedrock rounded-full darken-border">
                    <CardIcon
                        size="1.5rem"
                        color="var(--theme-color-foreground)"
                    />
                </div>
                <h2>{title}</h2>
            </button>
            <div>{@render children()}</div>
        </div>
    </div>
{/if}

<style lang="scss">
    .reversed-orientation {
        flex-direction: row-reverse;
        justify-content: space-between;
    }
</style>
