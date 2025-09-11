<script lang="ts">
    import { ROOT_URL } from "../api/backend";
    import { logEntries } from "../api/logger.svelte";
</script>

<pre class="w-full h-full overflow-scroll max-h-[70vh]">
Server IP: {ROOT_URL}
Log:
{logEntries.join("\n")}
</pre>
