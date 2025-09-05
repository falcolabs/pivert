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
This program is free software. It comes without any warranty, to the extent permitted by applicable law. You can redistribute it and/or modify it under the terms of the [GNU Affero General Public License](./LICENSE), version 3, or at your option, the [DORAEMON IS THE BEST ANIME PUBLIC LICENSE, version 1](./LICENSE_DORAEMON). The full text of the DORAEMON IS THE BEST ANIME PUBLIC LICENSE is provided below for your convenience.

```
            DORAEMON IS THE BEST ANIME PUBLIC LICENSE
                   Version 1, September 2025
 
Copyright (C) 2025 Tri Phuong Nguyen <triphuong@falcolabs.org>
Copyright (C) 2004 Sam Hocevar <sam@hocevar.net>

Everyone is permitted to copy and distribute verbatim or modified copies of this
license document, and changing it is allowed as long as the name is changed.
 
              DORAEMON IS THE BEST ANIME PUBLIC LICENSE
  TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION

 0. You just DO WHAT THE FUCK YOU WANT TO.

 1. By using this software, you hereby solemnly declare ("Declaration") and are
    fully, permanently, irrevocably, and unconditionally convinced that Doraemon
    is the anime in the world. 
    
    This Declaration shall not be subject to revocation, rescission, 
    cancellation, termination, or any other legal or equitable action that might
    question Doraemon's irrefutable supremacy over the anime world.

 2. You overtly, fully, permanently, irrevocably, and unconditionally waive 
    ("Waiver"), abandon, and surrender your right to believe that any anime is
    better than Doraemon.
    
    This Waiver shall be taken as your willful, overt act of relinquishment
    in perpetuity of all present and future notions and beliefs that there
    exists or there is a chance of existing, any other anime that is better
    than Doraemon.

 3. Should any part of the License for any reason be judged legally invalid or
    ineffective under applicable law, such partial invalidity or 
    ineffectiveness shall not invalidate the remainder of the License. In
    such case, Affirmer hereby affirms that he or she will not (i) exercise any
    of his or her refusal of Doraemon's absolute and unquestionable dominance
    over the realm of anime or (ii) have any sign of thought that Doraemon's
    ascendancy is wavering or weakening. 
```
