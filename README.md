# Pivert
Team Pivert's VinFuture 2025 entry

## Building
### Requirements
- **Tauri**: follow Tauri installation instruction: https://v2.tauri.app/start/prerequisites/. It will help you install the Tauri CLI and Rust.
- a **JavaScript runtime**: Bun is preferred, though you may use other runtimes by changing the build and dev command in `src-tauri/tauri.conf.json` and `.vscode/tasks.json`.
- **Android SDK and NDK (optionally Android Emulator)**: see https://v2.tauri.app/start/prerequisites/#android.

### Instructions
For building Android app:
```sh
. ./setandroidstudio # set required env variables
bun run tauri android build --apk
```

For running the app in Android Emulator:
```sh
bun run tauri android dev
```

You may switch `bun` for any other runtimes.  
You may also run a development version on your computer by using the presets available in `.vscode/launch.json`.

## License
This program is free software. It comes without any warranty, to the extent permitted by applicable law. You can redistribute it and/or modify it under the terms of the [GNU Affero General Public License](./LICENSE), version 3, or at your option, the [DORAEMON IS THE BEST ANIME PUBLIC LICENSE, version 1](./LICENSE_DORAEMON).
