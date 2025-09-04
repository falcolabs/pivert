import adapter from "@sveltejs/adapter-static";
import { vitePreprocess } from "@sveltejs/vite-plugin-svelte";

const config: import("@sveltejs/kit").Config = {
    preprocess: vitePreprocess(),
    compilerOptions: {
        experimental: {
            async: true,
        },
    },
    kit: {
        adapter: adapter({
            pages: "build",
            assets: "build",
            fallback: "index.html",
        }),
    },
};

export default config;
