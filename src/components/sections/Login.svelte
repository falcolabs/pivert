<script lang="ts">
    import { login } from "../../api";
    import PasswordInput from "../PasswordInput.svelte";
    import Signup from "./Signup.svelte";
    import { fade } from "svelte/transition";
    import { monoco } from "@monokai/monoco-svelte";

    let username: string = $state("");
    let password: string = $state("");
    let isSignup: boolean = $state(false);
</script>

{#if isSignup}
    <div transition:fade={{ duration: 100 }} class="h-full">
        <Signup
            setIsSignup={(x: boolean) => {
                isSignup = x;
            }}
        />
    </div>
{:else}
    <div transition:fade={{ duration: 100 }} class="flex flex-col h-full">
        <img class="banner" src="/images/login-banner.svg" alt="" />
        <div class="container">
            <h1>Đồng hành cùng tớ nhé!</h1>
            <form
                class="login-bundle"
                onsubmit={async () => {
                    await login(username, password);
                }}
            >
                <input
                    use:monoco={{
                        borderRadius: 18,
                        smoothing: 0.6,
                        clip: true,
                    }}
                    class="text-bold"
                    bind:value={username}
                    id="username"
                    name="username"
                    type="text"
                    placeholder="Tên người dùng"
                />
                <PasswordInput bind:value={password} placeholder="Mật khẩu" />
                <a href="/">Quên mật khẩu?</a>
                <input
                    use:monoco={{
                        borderRadius: 18,
                        smoothing: 0.6,
                        clip: true,
                    }}
                    class="hover-darken btn-accent text-bold"
                    type="submit"
                    value="Đăng nhập"
                />
            </form>
            <div class="other-login">
                <button class="hover-darken login-with l-apple">
                    <img src="/images/logo-apple.png" />
                    <h3>Đăng nhập với Apple</h3>
                </button>
                <button class="hover-darken login-with">
                    <img src="/images/logo-google.png" />
                    <h3>Đăng nhập với Google</h3>
                </button>
            </div>
            <p>
                Bạn chưa có tài khoản? <a
                    role="button"
                    onclick={() => {
                        isSignup = true;
                    }}>Đăng ký</a
                >
            </p>
        </div>
    </div>
{/if}

<style lang="scss">
    @use "../../styles/_theme.sass";

    .login-with.l-apple {
        background-color: theme.get(foreground);
        color: theme.get(bedrock);
    }

    .other-login {
        display: flex;
        flex-direction: column;
        gap: 10px;
        width: 100%;
    }

    .login-with {
        border-radius: 99px;
        width: 100%;
        padding: 1.25rem;
        display: flex;
        flex-direction: row;
        justify-content: center;
        align-items: center;
        gap: 0.8rem;
        background-color: theme.get(slate);

        img {
            height: 1rem;
        }
    }

    .login-bundle {
        display: flex;
        flex-direction: column;
        gap: 10px;
        width: 100%;

        a {
            text-align: right;
        }
    }

    // #password-visible-icon {
    //     position: relative;
    //     top: 2.7rem;
    //     left: calc(100% - 2.53rem);
    // }

    .banner {
        width: 100%;
        height: auto;
    }

    .container {
        flex: 1;
        height: max-content;
        width: 100%;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: space-between;
        padding: 1.5rem;
        // gap: 24px;
    }
</style>
