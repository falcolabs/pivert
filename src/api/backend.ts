import { logout } from "./index";
import type * as schema from "./schema";
export let token: string = "";

export const updateToken = () => {
    token = window.localStorage.getItem("token")!;
};
updateToken();

let fetch: (
    input: URL | Request | string,
    init?: RequestInit & import("@tauri-apps/plugin-http").ClientOptions,
) => Promise<Response>;
if (Object.hasOwn(window, "__TAURI_INTERNALS__")) {
    fetch = (await import("@tauri-apps/plugin-http")).fetch;
} else {
    fetch = window.fetch;
    // fake @tauri-apps/plugin-http
    Object.defineProperty(window, "__TAURI_INTERNALS__", {
        // @ts-expect-error
        invoke: console.log,
    });
}

export const reqURL = (
    path: string,
    params: { [key: string]: string } = {},
): URL => {
    let o = new URL("http://localhost:6942" + path);
    for (let [k, v] of Object.entries(params)) {
        o.searchParams.append(k, v);
    }
    return o;
};

export const bfetch = async (
    path: URL,
    method: "GET" | "POST" = "GET",
    payload?: object | string,
): Promise<Response> => {
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
    if (r.status != 200) {
        await logout();
        throw new Error(JSON.stringify(await r.json()));
    }
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
    console.log("me(): token is", token);
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
    return await fetchJSON(reqURL(`api/v1/complete/${taskType}/${taskID}`));
}

async function _createTask(
    taskType: "habit" | "todo",
    target: schema.Habit | schema.Todo,
): Promise<string> {
    return await fetchJSON(
        reqURL(`api/v1/complete/create/${taskType}`),
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
