<script lang="ts">
    import { onMount } from "svelte";
    import { requests } from "../../api";
    import type { ShortcutTrain } from "../../api/shortcuts";
    import Leaf from "../Leaf.svelte";
    import Load from "../Load.svelte";
    import MetricsDisplay from "../MetricsDisplay.svelte";
    import { Dot, Plus } from "@lucide/svelte";
    import { monoco } from "@monokai/monoco-svelte";

    let train: ShortcutTrain;

    const TODAY_START = Math.round(new Date().getTime() / 1000);
    const TODAY_WEEKDAY = new Date().getDay();
    const TODAY_DATE_IN_MONTH = new Date().getDate();
    const SECONDS_IN_A_DAY = 60 * 60 * 24;

    let weekdayDetails = [
        {
            name: "H",
            startStamp: (0 - TODAY_WEEKDAY) * SECONDS_IN_A_DAY + TODAY_START,
            endStamp: (0 - TODAY_WEEKDAY + 1) * SECONDS_IN_A_DAY + TODAY_START,
            dateNumber: 0 - TODAY_WEEKDAY + 1 + TODAY_DATE_IN_MONTH,
        },
        {
            name: "B",
            startStamp: (1 - TODAY_WEEKDAY) * SECONDS_IN_A_DAY + TODAY_START,
            endStamp: (1 - TODAY_WEEKDAY + 1) * SECONDS_IN_A_DAY + TODAY_START,
            dateNumber: 1 - TODAY_WEEKDAY + 1 + TODAY_DATE_IN_MONTH,
        },
        {
            name: "T",
            startStamp: (2 - TODAY_WEEKDAY) * SECONDS_IN_A_DAY + TODAY_START,
            endStamp: (2 - TODAY_WEEKDAY + 1) * SECONDS_IN_A_DAY + TODAY_START,
            dateNumber: 2 - TODAY_WEEKDAY + 1 + TODAY_DATE_IN_MONTH,
        },
        {
            name: "N",
            startStamp: (3 - TODAY_WEEKDAY) * SECONDS_IN_A_DAY + TODAY_START,
            endStamp: (3 - TODAY_WEEKDAY + 1) * SECONDS_IN_A_DAY + TODAY_START,
            dateNumber: 3 - TODAY_WEEKDAY + 1 + TODAY_DATE_IN_MONTH,
        },
        {
            name: "S",
            startStamp: (4 - TODAY_WEEKDAY) * SECONDS_IN_A_DAY + TODAY_START,
            endStamp: (4 - TODAY_WEEKDAY + 1) * SECONDS_IN_A_DAY + TODAY_START,
            dateNumber: 4 - TODAY_WEEKDAY + 1 + TODAY_DATE_IN_MONTH,
        },
        {
            name: "B",
            startStamp: (5 - TODAY_WEEKDAY) * SECONDS_IN_A_DAY + TODAY_START,
            endStamp: (5 - TODAY_WEEKDAY + 1) * SECONDS_IN_A_DAY + TODAY_START,
            dateNumber: 5 - TODAY_WEEKDAY + 1 + TODAY_DATE_IN_MONTH,
        },
        {
            name: "C",
            startStamp: (6 - TODAY_WEEKDAY) * SECONDS_IN_A_DAY + TODAY_START,
            endStamp: (6 - TODAY_WEEKDAY + 1) * SECONDS_IN_A_DAY + TODAY_START,
            dateNumber: 6 - TODAY_WEEKDAY + 1 + TODAY_DATE_IN_MONTH,
        },
    ];

    onMount(async () => {
        console.log("loading train");
        train = await requests.shortcut.train();
    });
</script>

<Leaf>
    <Load until={train !== undefined}>
        <div class="flex flex-col w-full dodge-topbar px-8 gap-8">
            <div class="flex flex-col w-full gap-2">
                <div class="flex items-center justify-center p-2">
                    <h1>Luyện tập</h1>
                </div>
                <MetricsDisplay metrics={train.user.metrics} />
            </div>

            <div class="flex flex-col gap-4">
                <div class="flex flex-row justify-between items-center">
                    <h2>Việc cần làm</h2>
                    <div class="bg-slate p-3 rounded-full hover-darken">
                        <Plus size="1.5rem" />
                    </div>
                </div>
                <div class="flex flex-row items-center justify-between gap-2">
                    {#each weekdayDetails as weekday}
                        <div
                            class="flex flex-col items-center justify-center w-full gap-2"
                        >
                            <p>{weekday.name}</p>
                            <div
                                class="flex flex-col justify-between items-center bg-slate h-28 w-full rounded-full"
                            >
                                <div
                                    class="flex bg-slate items-center justify-center rounded-full w-full h-12"
                                >
                                    <Dot
                                        color={"var(--color-slate2)"}
                                        size="2.5rem"
                                    />
                                </div>
                                <div
                                    class="flex items-center justify-center rounded-full w-full h-12"
                                    class:bg-accent={weekday.dateNumber ==
                                        TODAY_DATE_IN_MONTH}
                                >
                                    {weekday.dateNumber}
                                </div>
                            </div>
                        </div>
                    {/each}
                </div>
                <div class="flex flex-row flex-wrap gap-4">
                    {#each Object.values(train.habits) as task}
                        <button
                            class="flex flex-row items-center pill-display bg-accent gap-3 hover-darken"
                            use:monoco={{
                                borderRadius: 24,
                                smoothing: 0.6,
                                clip: true,
                            }}
                            onclick={async () => {
                                train.user = await requests.complete.habit(
                                    task.taskID,
                                );
                            }}
                        >
                            <div
                                class="p-3 min-w-13 bg-bedrock darken-border rounded-full"
                            >
                                <img
                                    class="w-max h-max"
                                    src={`https://cdn.jsdelivr.net/npm/lucide-static@latest/icons/${task.icon}.svg`}
                                    alt="Task Icon "
                                />
                            </div>
                            <p class="text-left">{task.name}</p>
                        </button>
                    {/each}
                </div>
            </div>

            <div class="flex flex-col gap-4">
                <div class="flex flex-row justify-between items-center">
                    <h2>Thói quen</h2>
                    <div class="bg-slate p-3 rounded-full hover-darken">
                        <Plus size="1.5rem" />
                    </div>
                </div>

                <div class="flex flex-row flex-wrap gap-4">
                    {#each Object.values(train.todos) as task}
                        <button
                            class="flex flex-row items-center pill-display bg-blue gap-3 hover-darken"
                            use:monoco={{
                                borderRadius: 24,
                                smoothing: 0.6,
                                clip: true,
                            }}
                            onclick={async () => {
                                train.user = await requests.complete.todo(
                                    task.taskID,
                                );
                            }}
                        >
                            <div
                                class="p-3 min-w-13 bg-bedrock darken-border rounded-full"
                            >
                                <img
                                    class="w-max h-max"
                                    src={`https://cdn.jsdelivr.net/npm/lucide-static@latest/icons/${task.icon}.svg`}
                                    alt="Task Icon "
                                />
                            </div>
                            <p class="text-left">{task.name}</p>
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
