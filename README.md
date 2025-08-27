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
This project and all of its source code is licensed under the GNU Affero General Public License, version 3.

```
Copyright (C) 2025  Team Pivert

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
```
