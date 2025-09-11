<script lang="ts">
    import { onMount } from "svelte";
    import { requests } from "../../api";
    import type { ShortcutRewards } from "../../api/shortcuts";
    import Leaf from "../Leaf.svelte";
    import Load from "../Load.svelte";
    import MetricsDisplay from "../MetricsDisplay.svelte";
    import { ChevronDown, Heart, Plus, Sparkles, Zap } from "@lucide/svelte";
    import { monoco } from "@monokai/monoco-svelte";

    let rewardsShortcut: ShortcutRewards;

    onMount(async () => {
        requests.log("loading train");
        rewardsShortcut = await requests.shortcut.rewards();
    });
</script>

<Leaf>
    <Load until={rewardsShortcut !== undefined}>
        <div class="flex flex-col w-full dodge-topbar px-8 gap-8">
            <div class="flex flex-col w-full gap-2">
                <div class="flex items-center justify-center p-2">
                    <h1>Cửa hàng</h1>
                </div>
                <MetricsDisplay metrics={rewardsShortcut.user.metrics} />
            </div>

            <div class="flex flex-col gap-4">
                <div class="flex flex-row justify-between items-center">
                    <h2>Tự thưởng</h2>
                    <div class="bg-slate p-3 rounded-full hover-darken">
                        <Plus size="1.5rem" />
                    </div>
                </div>

                <div class="flex flex-row flex-wrap gap-4">
                    {#each Object.values(rewardsShortcut.user.userRewards) as rewardID}
                        <button
                            class="flex flex-row items-center pill-display bg-green gap-3 hover-darken"
                            use:monoco={{
                                borderRadius: 24,
                                smoothing: 0.6,
                                clip: true,
                            }}
                            onclick={async () => {
                                rewardsShortcut.user =
                                    await requests.complete.reward(rewardID);
                            }}
                        >
                            <div
                                class="p-3 min-w-13 bg-bedrock darken-border rounded-full"
                            >
                                <img
                                    class="w-max h-max"
                                    src={`https://cdn.jsdelivr.net/npm/lucide-static@latest/icons/${rewardsShortcut.userRewards[rewardID].icon}.svg`}
                                    alt="Task Icon "
                                />
                            </div>
                            <div class="flex flex-col gap-1">
                                <p class="text-left">
                                    {rewardsShortcut.userRewards[rewardID].name}
                                </p>
                                <div
                                    class="flex flex-row justify-between gap-1 items-center w-fit"
                                >
                                    {#each Object.entries(rewardsShortcut.userRewards[rewardID].cost) as [name, cost]}
                                        {#if cost !== 0}
                                            {#if name === "health"}
                                                <Heart
                                                    size="1.5rem"
                                                    fill="var(--color-red)"
                                                    color="var(--color-red)"
                                                />
                                            {:else if name === "cash"}
                                                <Zap
                                                    size="1.5rem"
                                                    fill="var(--color-blue2)"
                                                    color="var(--color-blue2)"
                                                />
                                            {:else if name === "xp"}
                                                <Sparkles
                                                    fill="var(--color-accent2)"
                                                    color="var(--color-accent2)"
                                                />
                                            {/if}
                                            <span
                                                class="text-[10px]"
                                                class:text-red={name ===
                                                    "health"}
                                                class:text-blue2={name ===
                                                    "cash"}
                                                class:text-accent2={name ===
                                                    "xp"}
                                                >{cost <= 0
                                                    ? -cost
                                                    : `+${cost}`}</span
                                            >
                                        {/if}
                                    {/each}
                                </div>
                            </div>
                        </button>
                    {/each}
                </div>
            </div>

            <div class="flex flex-col gap-4">
                <div class="flex flex-row justify-between items-center">
                    <h2>Từ đối tác</h2>
                    <div class="bg-slate p-3 rounded-full hover-darken">
                        <ChevronDown size="1.5rem" />
                    </div>
                </div>

                <div class="flex flex-row flex-wrap gap-4">
                    {#each Object.values(rewardsShortcut.user.systemRewards) as rewardID}
                        <button
                            class="flex flex-row items-center pill-display bg-green gap-3 hover-darken"
                            use:monoco={{
                                borderRadius: 24,
                                smoothing: 0.6,
                                clip: true,
                            }}
                            onclick={async () => {
                                rewardsShortcut.user =
                                    await requests.complete.reward(rewardID);
                            }}
                        >
                            <div
                                class="p-3 min-w-13 bg-bedrock darken-border rounded-full"
                            >
                                <img
                                    class="w-max h-max"
                                    src={`https://cdn.jsdelivr.net/npm/lucide-static@latest/icons/${rewardsShortcut.systemRewards[rewardID].icon}.svg`}
                                    alt="Task Icon "
                                />
                            </div>
                            <div class="flex flex-col gap-1">
                                <p class="text-left">
                                    {rewardsShortcut.systemRewards[rewardID]
                                        .name}
                                </p>
                                <div
                                    class="flex flex-row justify-between gap-1 items-center w-fit"
                                >
                                    {#each Object.entries(rewardsShortcut.systemRewards[rewardID].cost) as [name, cost]}
                                        {#if cost !== 0}
                                            {#if name === "health"}
                                                <Heart
                                                    size="1.5rem"
                                                    fill="var(--color-red)"
                                                    color="var(--color-red)"
                                                />
                                            {:else if name === "cash"}
                                                <Zap
                                                    size="1.5rem"
                                                    fill="var(--color-blue2)"
                                                    color="var(--color-blue2)"
                                                />
                                            {:else if name === "xp"}
                                                <Sparkles
                                                    fill="var(--color-accent2)"
                                                    color="var(--color-accent2)"
                                                />
                                            {/if}
                                            <span
                                                class="text-[10px]"
                                                class:text-red={name ===
                                                    "health"}
                                                class:text-blue2={name ===
                                                    "cash"}
                                                class:text-accent2={name ===
                                                    "xp"}
                                                >{cost <= 0
                                                    ? -cost
                                                    : `+${cost}`}</span
                                            >
                                        {/if}
                                    {/each}
                                </div>
                            </div>
                        </button>
                    {/each}
                </div>
            </div>
            <br /><br /><br />
            <br /><br />
        </div>
    </Load>
</Leaf>

<style lang="scss">
    .pill-display {
        width: calc(50% - 0.5rem);
        padding: 1.25rem 1.5rem;
    }
</style>
