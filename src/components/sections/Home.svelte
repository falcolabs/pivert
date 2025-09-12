<script lang="ts">
    import { onMount } from "svelte";
    import { requests, toRomanNumerals } from "../../api";
    import Leaf from "../Leaf.svelte";
    import type { ShortcutHome } from "../../api/shortcuts";
    import Load from "../Load.svelte";
    import {
        ArrowRight,
        BellDot,
        CalendarCheck,
        ContactRound,
        Dumbbell,
    } from "@lucide/svelte";
    import { monoco } from "@monokai/monoco-svelte";
    import SearchBar from "../SearchBar.svelte";
    import MetricsDisplay from "../MetricsDisplay.svelte";
    import Card from "../Card.svelte";

    let { changeSection } = $props();

    const getCurrentLevel = (cxp: number, glist: number[]) => {
        let i = 0;
        for (let g of glist) {
            if (g >= cxp) {
                return i + 1;
            }
            i++;
        }
        return 1;
    };

    // @ts-expect-error
    let home: ShortcutHome = $state();
    let lvlcat = $state("cancu");
    let clevel = $state(1);

    onMount(async () => {
        requests.log("making home");
        home = await requests.shortcut.home();
        lvlcat = home.user.achievements.leveling[0].category;
        clevel = getCurrentLevel(
            home.user.metrics.allTimeXP,
            home.achievementInfo.lvlInfo[lvlcat].allTimeXPRequired,
        );
    });
    let searchTerm = $state();
</script>

<Leaf>
    <Load until={home !== undefined}>
        <div class="flex flex-col w-full dodge-topbar px-8 gap-4">
            <div class="flex flex-row items-center justify-between mt-4">
                <div class="flex flex-row items-center gap-4">
                    <img
                        src={requests.reqURL(home.user.avatarURL).toString()}
                        alt="User avatar"
                        class="w-12 h-12 rounded-full"
                    />
                    <div>
                        Chào buổi sáng<br />
                        <h2 class="font-bold">{home.user.displayname}</h2>
                    </div>
                    <div class="bg-slate px-3 py-1 rounded-full">CHÙA</div>
                </div>
                <div
                    class="w-12 h-12 bg-slate rounded-full flex items-center justify-center hover-darken"
                >
                    <BellDot size="1.5rem" />
                </div>
            </div>
            <SearchBar bind:value={searchTerm} />
            <MetricsDisplay metrics={home.user.metrics} />
            <Card
                bg="blue"
                fg="foreground"
                title="Bền bỉ"
                icon={CalendarCheck}
                iconAlign="left"
            >
                <span class="text-4xl font-bold"
                    >{home.user.achievements.leveling[0].progress * 100}%</span
                ><br />
                <div class="flex flex-row items-center gap-2">
                    <span class="text-bold">Cần Cù Bù Siêng Năng</span>
                    <span class="text-bold">{clevel}</span>
                    <div style="transform: translateY(2px)">
                        <ArrowRight size="0.75rem" />
                    </div>
                    <span class="text-bold">{clevel + 1}</span>
                </div>
                <a href="/">Tìm hiểu thêm về chỉ số Bền bỉ</a>
            </Card>
            <div class="flex flex-row gap-4">
                <div class="w-auto h-full relative">
                    <div class="abs-center absolute z-100">
                        <p class="w-26 text-center text-bold text-blue">
                            {home.achievementInfo.badgeInfo[
                                home.user.achievements.badges[0]
                            ].name}
                            {toRomanNumerals(clevel)}
                        </p>
                    </div>
                    <img
                        use:monoco={{
                            borderRadius: 24,
                            smoothing: 0.6,
                            clip: true,
                        }}
                        src={requests
                            .reqURL(
                                home.achievementInfo.badgeInfo[
                                    home.user.achievements.badges[0]
                                ].coverArtURL[clevel - 1],
                            )
                            .toString()}
                        alt="User badge"
                    />
                </div>
                <Card
                    bg="accent"
                    fg="foreground"
                    title="Luyện tập"
                    icon={Dumbbell}
                    iconAlign="right"
                    onclick={() => {
                        changeSection("train");
                    }}
                >
                    <!-- TODO: self host the icons if possible -->
                    <button class="flex flex-row gap-4">
                        <!-- <div class="flex flex-wrap flex-row gap-1">
                            {#each Object.values(tasks.habits) as h}
                                <button
                                    class="flex items-center justify-center p-3 bg-bedrock rounded-full darken-border"
                                >
                                    <img
                                        src={`https://cdn.jsdelivr.net/npm/lucide-static@latest/icons/${h.icon}.svg`}
                                        alt="Task Icon "
                                    />
                                </button>
                            {/each}
                        </div> -->
                        <span class="text-center"
                            >Bấm vào đây để đến nhanh.</span
                        >
                    </button>
                </Card>
            </div>
            <Card
                title="Bạn bè"
                icon={ContactRound}
                iconAlign="right"
                bg="slate"
                fg="foreground"
            >
                <p class="text-center">Gần đây không có hoạt động nào.</p>
                <p class="text-center">Cuộc sống của cậu yên bình quá~</p>
            </Card>
            <img
                class="w-full h-auto rounded-4xl"
                use:monoco={{
                    borderRadius: 24,
                    smoothing: 0.6,
                    clip: true,
                }}
                src={requests
                    .reqURL("/static/promotional/banner-donate-home.svg")
                    .toString()}
                alt="User badge"
            />
            <br />
            <br />
            <br />
            <br />
            <br />
        </div>
    </Load>
</Leaf>

<style lang="scss">
    .abs-center {
        top: 0.4rem;
        left: 0;
        right: 0;
        margin-inline: auto;
        width: fit-content;
    }
</style>
