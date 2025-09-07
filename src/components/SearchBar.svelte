<script lang="ts">
    import { Search } from "@lucide/svelte";

    let { value = $bindable() } = $props();
</script>

<div class="relative">
    <div class="sicon">
        <Search size="1rem" />
    </div>
    <input class="sbox" bind:value type="text" placeholder="Nhập để tìm kiếm" />
</div>

<style lang="scss">
    .sicon {
        position: absolute;
        left: 1.25rem;
        top: 1.2rem;
    }

    .sbox {
        padding-left: 3rem;
    }
</style>
