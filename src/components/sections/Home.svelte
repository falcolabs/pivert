<script lang="ts">
    import { requests, logout } from "../../api";
    import Leaf from "../Leaf.svelte";
</script>

<div>
    <Leaf>
        <h1>This is my home</h1>
        <pre class="overflow-scroll">
            {JSON.stringify(await requests.me())}
        </pre>
        <button
            onclick={async () => {
                await logout();
            }}>Logout</button
        >
    </Leaf>
</div>
