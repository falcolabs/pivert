import { logout } from "./index";
import { addLogEntry } from "./logger.svelte";
import type * as schema from "./schema";

export let token: string = window.localStorage.getItem("token")!;
const LOCAL_NEST_IP = import.meta.env.VITE_PIVERT_NEST;
export const FORCE_DEV = false;
const ALLOW_BROWSER_FETCH = false;

export const updateToken = () => {
    token = window.localStorage.getItem("token")!;
};

export const log = (...le: any[]) => {
    addLogEntry(JSON.stringify(le));
    if (!ALLOW_BROWSER_FETCH && _log_info !== undefined) {
        _log_info(JSON.stringify(le));
        // invoke("transfer_log", { logtext: JSON.stringify(le) });
    }
    console.log(...le);
};

let invoke: (
    cmd: string,
    args?: import("@tauri-apps/api/core").InvokeArgs | undefined,
    options?: import("@tauri-apps/api/core").InvokeOptions,
) => any = async (...args: any[]) => {
    if (ALLOW_BROWSER_FETCH) {
        log("ivoke ignored in browser:", ...args);
    }
};

let _log_info: (s: string) => Promise<void>;

let fetch: (
    input: URL | Request | string,
    init?: RequestInit & import("@tauri-apps/plugin-http").ClientOptions,
) => Promise<Response> = window.fetch;

if (Object.hasOwn(window, "__TAURI_INTERNALS__") && !ALLOW_BROWSER_FETCH) {
    import("@tauri-apps/plugin-http").then((r) => {
        fetch = r.fetch;
    });
    import("@tauri-apps/api/core").then((r) => {
        invoke = r.invoke;
    });

    import("@tauri-apps/plugin-log").then((r) => {
        let { info } = r;
        _log_info = info;
    });
} else {
    // fake @tauri-apps/plugin-http
    Object.defineProperty(window, "__TAURI_INTERNALS__", {
        // @ts-expect-error
        invoke: log,
    });
}

export const ROOT_URL =
    import.meta.env.PROD || !FORCE_DEV
        ? "https://pivert.falcolabs.org"
        : `http://${LOCAL_NEST_IP === undefined ? "localhost" : LOCAL_NEST_IP}:6942`;

export const reqURL = (
    path: string,
    params: { [key: string]: string } = {},
): URL => {
    log("making URL", ROOT_URL + path);
    try {
        let o = new URL(ROOT_URL + path);
        for (let [k, v] of Object.entries(params)) {
            o.searchParams.append(k, v);
        }
        return o;
    } catch (e) {
        log(e);
        console.trace(e);
        return new URL("/");
    }
};

export const bfetch = async (
    path: URL,
    method: "GET" | "POST" = "GET",
    payload?: object | string,
): Promise<Response> => {
    log("making request to", path);
    let r = await fetch(path, {
        method: method,
        headers: {
            "Content-Type":
                typeof payload === "string"
                    ? "application/x-www-form-urlencoded"
                    : "application/json",
            Authorization: `Bearer ${token}`,
        },
        body: typeof payload === "string" ? payload : JSON.stringify(payload),
    });
    log("returned shit");
    if (r.status != 200) {
        await logout();
        log("error when making req: ", await r.clone().json());
        throw new Error(JSON.stringify(await r.json()));
    }
    log(path, "->", await r.clone().json());
    return r;
};

export const fetchJSON = async (
    path: URL,
    method: "GET" | "POST" = "GET",
    payload?: object | FormData,
): Promise<any> => {
    return await (await bfetch(path, method, payload)).json();
};

export async function register(
    username: string,
    password: string,
    displayname: string,
): Promise<boolean> {
    await bfetch(
        reqURL("/api/v1/register", {
            username: username,
            password: password,
            displayname: displayname,
        }),
    );
    return true;
}

export async function login(
    username: string,
    password: string,
): Promise<schema.Token> {
    // let payload: FormData;

    // if (typeof usernameOrForm === "string") {
    //     payload = new FormData();
    //     if (password === undefined)
    //         throw new Error(
    //             "password must not be undefined if username is provided",
    //         );
    //     payload.append("username", usernameOrForm);
    //     payload.append("password", password);
    // } else {
    //     payload = new FormData(usernameOrForm);
    // }

    // TODO: upstream FormData support in @tauri-apps/plugin-http
    // now we have to use login
    return await fetchJSON(reqURL("/api/v1/login"), "POST", {
        username: username,
        password: password,
    });
}

export async function currentSession(): Promise<boolean> {
    return (await fetchJSON(reqURL("/api/v1/currentSession"))).success;
}

export async function me(): Promise<schema.User> {
    log("me(): token is", token);
    return await fetchJSON(reqURL("/api/v1/user/me"));
}

export async function getUserData(
    ident: string,
    queryType: schema.UserDataQueryType,
): Promise<schema.User> {
    return await fetchJSON(
        reqURL(`/api/v1/user/${ident}`, { queryType: queryType }),
    );
}

export async function getBadge(badgeID: string): Promise<schema.BadgeInfo> {
    return await fetchJSON(reqURL(`/api/v1/resources/badges/${badgeID}`));
}

export async function getLevelingCategory(
    catID: string,
): Promise<schema.LevelingCategoryInfo> {
    return await fetchJSON(
        reqURL(`/api/v1/resources/leveling_categories/${catID}`),
    );
}

async function _completeTask(
    taskType: schema.TaskType,
    taskID: string,
): Promise<schema.User> {
    return await fetchJSON(reqURL(`/api/v1/complete/${taskType}/${taskID}`));
}

async function _createTask(
    taskType: schema.TaskType,
    target: schema.Habit | schema.Todo,
): Promise<string> {
    return await fetchJSON(
        reqURL(`/api/v1/complete/create/${taskType}`),
        "POST",
        target,
    );
}

export const create = {
    habit: async (habit: schema.Habit): Promise<string> =>
        await _createTask("habit", habit),
    todo: async (todo: schema.Todo): Promise<string> =>
        await _createTask("todo", todo),
};

export const complete = {
    habit: async (taskID: string): Promise<schema.User> =>
        await _completeTask("habit", taskID),
    todo: async (taskID: string): Promise<schema.User> =>
        await _completeTask("todo", taskID),
    reward: async (taskID: string): Promise<schema.User> =>
        await _completeTask("reward", taskID),
};

export const shortcut = {
    tasks: async (): Promise<schema.shortcuts.ShortcutTasks> =>
        fetchJSON(reqURL("/api/v1/shortcuts/tasks")),
    train: async (): Promise<schema.shortcuts.ShortcutTrain> =>
        fetchJSON(reqURL("/api/v1/shortcuts/train")),
    rewards: async (): Promise<schema.shortcuts.ShortcutRewards> =>
        fetchJSON(reqURL("/api/v1/shortcuts/rewards")),
    achievementInfo:
        async (): Promise<schema.shortcuts.ShortcutAchievementsInfo> =>
            fetchJSON(reqURL("/api/v1/shortcuts/achievement_info")),
    home: async (): Promise<schema.shortcuts.ShortcutHome> =>
        fetchJSON(reqURL("/api/v1/shortcuts/home")),
};
