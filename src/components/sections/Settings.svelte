<script lang="ts">
    import { monoco } from "@monokai/monoco-svelte";
    import { logout } from "../../api";
    import Leaf from "../Leaf.svelte";
    import LogDisplay from "../LogDisplay.svelte";
</script>

<Leaf>
    <div class="flex flex-col dodge-topbar px-8 gap-4">
        <h1>Logout here</h1>
        <button
            use:monoco={{
                borderRadius: 18,
                clip: true,
                smoothing: 0.6,
            }}
            class="bg-red p-6 hover-darken"
            onclick={async () => {
                await logout();
            }}
        >
            Logout
        </button>

        <h2>Thông tin gỡ lỗi</h2>
        <LogDisplay />
    </div>
</Leaf>
