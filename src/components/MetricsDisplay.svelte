<script lang="ts">
    import { Banknote, Heart, Sparkles } from "@lucide/svelte";
    import type { UserMetrics } from "../api/schema";

    let {
        metrics,
    }: {
        metrics: UserMetrics;
    } = $props();
</script>

<div class="flex flex-row items-center justify-center gap-6">
    <h3>Bạn đang có</h3>
    <div class="flex flex-row gap-2 items-center">
        <Heart fill="var(--color-red)" color="var(--color-red)" />
        <h3>{metrics.health}</h3>
    </div>
    <div class="flex flex-row gap-2 items-center">
        <Banknote
            size="2rem"
            fill="var(--color-blue)"
            color="var(--color-bedrock)"
        />
        <h3>{metrics.cash}</h3>
    </div>
    <div class="flex flex-row gap-2 items-center">
        <Sparkles
            fill="var(--color-accent-border)"
            color="var(--color-accent-border)"
        />
        <h3>{metrics.xp}</h3>
    </div>
</div>
