<script lang="ts">
    import { Eye, EyeClosed } from "@lucide/svelte";

    let { value = $bindable(), placeholder, required = false } = $props();
    let passwordVisible = $state(false);
</script>

<div class="icons">
    <button
        id="password-visible-icon"
        aria-label="Hiện mật khẩu"
        onclick={() => {
            passwordVisible = !passwordVisible;
        }}
    >
        <div id="icon-obj">
            {#if passwordVisible}
                <Eye color="#A8AAB8" />
            {:else}
                <EyeClosed color="#A8AAB8" />
            {/if}
        </div>
    </button>
    <input
        class="text-bold"
        bind:value
        id="password"
        name="password"
        type={passwordVisible ? "text" : "password"}
        {placeholder}
        {required}
    />
</div>

<style lang="scss">
    .icons {
        display: flex;
        flex-direction: column;
        align-items: end;
        justify-content: center;

        #icon-obj {
            position: relative;
            padding-right: 1.5rem;
            margin-top: -1.5rem;
            transform: translateY(2.5rem);
        }
    }
</style>
