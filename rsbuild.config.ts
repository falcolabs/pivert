// WIP. Rsbuild is not usable yet.
import { defineConfig, loadEnv } from "@rsbuild/core";
import { pluginSvelte } from "@rsbuild/plugin-svelte";
import { pluginSass } from "@rsbuild/plugin-sass";

const host = process.env.TAURI_DEV_HOST;
const { publicVars } = loadEnv({ prefixes: ["VITE_"] });

export default defineConfig({
    plugins: [
        pluginSass(),
        pluginSvelte({
            preprocessOptions: {
                scss: {
                    importer: [
                        // Handle alias imports for SCSS files
                        (url, _) => {
                            if (url.startsWith("@/")) {
                                return { file: url.replace("@/", "src/") };
                            }
                            return null;
                        },
                    ],
                },
            },
        }),
    ],
    source: {
        define: publicVars,
        entry: {
            index: "./src/index.ts",
        },
    },
    output: {
        distPath: {
            root: "build",
        },
    },
    environments: {
        web: {
            source: {
                define: {
                    "import.meta.env.SSR": JSON.stringify(false),
                },
            },
        },
        node: {
            source: {
                define: {
                    "import.meta.env.SSR": JSON.stringify(true),
                },
            },
            output: {
                target: "node",
            },
        },
    },
    server: {
        port: 1420,
        strictPort: true,
        host: host || "localhost",
    },
    tools: {
        rspack: {
            watchOptions: {
                ignored: ["**/src-tauri/**"],
            },
        },
    },
    dev: {
        client: {
            host: "localhost",
            protocol: "ws",
            port: 1421,
        },
    },
});
