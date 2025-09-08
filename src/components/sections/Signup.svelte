<script lang="ts">
    import { ArrowLeft } from "@lucide/svelte";
    import PasswordInput from "../PasswordInput.svelte";
    import { requests } from "../../api";
    import { monoco } from "@monokai/monoco-svelte";

    let { setIsSignup } = $props();
    let username: string = $state("");
    let password1: string = $state("");
    let password2: string = $state("");
    let ho: string = $state("");
    let dem: string = $state("");
    let ten: string = $state("");
    let error: string = $state("");
    let termsAccepted: boolean = $state(false);
</script>

<div
    class="flex flex-col dodge-topbar py-6 px-6 h-full container items-center gap-3"
>
    <div class="flex flex-row justify-between items-center w-full">
        <button
            class="hover-darken flex items-center justify-center w-10 h-10 bg-slate rounded-full"
            onclick={() => setIsSignup(false)}
        >
            <ArrowLeft />
        </button>
        <h2>Đăng ký</h2>
        <div class="w-6"></div>
    </div>
    <p class="text-center max-w-[70%]">
        Bạn cần cung cấp những thông tin sau để đăng ký tài khoản Pivert.
    </p>
    {#if error !== ""}
        <p class="text-center text-red">
            {error}
        </p>
    {/if}
    <form
        class="flex flex-col w-full h-full justify-between"
        onsubmit={async () => {
            if (password1 !== password2) {
                error = "Mật khẩu nhập lại không trùng khớp!";
                password1 = "";
                password2 = "";
                return;
            }

            if (!termsAccepted) {
                error = "Bạn chưa chấp thuận điều khoản!";
            }
            let dname = `${ho} ${dem + " "}${ten}`.trim();
            await requests.register(
                username,
                password1,
                dname === "" ? username : dname,
            );
            setIsSignup(false);
        }}
    >
        <div class="flex flex-col gap-6 w-full">
            <div class="section">
                <h3>Thông tin cá nhân</h3>
                <div class="flex flex-row gap-3 w-full">
                    <input
                        use:monoco={{
                            borderRadius: 18,
                            smoothing: 0.6,
                            clip: true,
                        }}
                        class="text-bold"
                        type="text"
                        placeholder="Họ"
                        bind:value={ho}
                    />
                    <input
                        use:monoco={{
                            borderRadius: 18,
                            smoothing: 0.6,
                            clip: true,
                        }}
                        class="text-bold"
                        type="text"
                        placeholder="Tên đệm"
                        bind:value={dem}
                    />
                </div>
                <input
                    use:monoco={{
                        borderRadius: 18,
                        smoothing: 0.6,
                        clip: true,
                    }}
                    class="text-bold"
                    type="text"
                    placeholder="Tên"
                    bind:value={ten}
                />
                <input
                    use:monoco={{
                        borderRadius: 18,
                        smoothing: 0.6,
                        clip: true,
                    }}
                    class="text-bold"
                    type="text"
                    placeholder="Số điện thoại"
                />
            </div>
            <div class="section">
                <h3>Tài khoản</h3>

                <input
                    use:monoco={{
                        borderRadius: 18,
                        smoothing: 0.6,
                        clip: true,
                    }}
                    class="text-bold"
                    bind:value={username}
                    type="text"
                    placeholder="Tên đăng nhập"
                    required={true}
                />
                <PasswordInput
                    bind:value={password1}
                    placeholder="Mật khẩu"
                    required={true}
                />
                <PasswordInput
                    bind:value={password2}
                    placeholder="Nhập lại mật khẩu"
                    required={true}
                />
            </div>
        </div>
        <div class="flex flex-col w-full gap-3 items-center">
            <div class="flex flex-row gap-2 w-full items-center justify-center">
                <input
                    bind:checked={termsAccepted}
                    class="wnf checkbox"
                    type="checkbox"
                    placeholder=""
                />
                <p>
                    Chấp thuận <a href="/">Điều khoản</a> và
                    <a href="/">Chính sách Riêng tư</a>
                </p>
            </div>
            <input
                type="submit"
                class="text-bold btn-accent hover-darken w-full"
                value="Tạo tài khoản"
            />
        </div>
    </form>
</div>

<style lang="scss">
    .wnf {
        width: fit-content;
    }

    .section {
        display: flex;
        flex-direction: column;
        gap: 0.75rem;
    }
</style>
