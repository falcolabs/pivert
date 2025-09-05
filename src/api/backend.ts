import { fetch } from "@tauri-apps/plugin-http";
import { logout } from "./index"
export let token: string = "";

export const updateToken = () => {
    token = window.localStorage.getItem("token")!;
};
updateToken();

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
        reqURL("/api/v1/register", { username: username, password: password, displayname: displayname }),
    );
    return true;
}

export async function login(
    username: string,
    password: string,
): Promise<Token> {
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

export async function me(): Promise<User> {
    console.log("me(): token is", token);
    return await fetchJSON(reqURL("/api/v1/user/me"));
}

export async function getUserData(
    ident: string,
    queryType: UserDataQueryType,
): Promise<User> {
    return await fetchJSON(
        reqURL(`/api/v1/user/${ident}`, { queryType: queryType }),
    );
}

async function _completeTask(
    taskType: TaskType,
    taskID: string,
): Promise<User> {
    return await fetchJSON(reqURL(`api/v1/complete/${taskType}/${taskID}`));
}

async function _createTask(
    taskType: "habit" | "todo",
    target: Habit | Todo,
): Promise<string> {
    return await fetchJSON(
        reqURL(`api/v1/complete/create/${taskType}`),
        "POST",
        target,
    );
}

export const create = {
    habit: async (habit: Habit): Promise<string> =>
        await _createTask("habit", habit),
    todo: async (todo: Todo): Promise<string> =>
        await _createTask("todo", todo),
};

export const complete = {
    habit: async (taskID: string): Promise<User> =>
        await _completeTask("habit", taskID),
    todo: async (taskID: string): Promise<User> =>
        await _completeTask("todo", taskID),
};

export const shortcut = {
    tasks: async (): Promise<ShortcutTasks> =>
        fetchJSON(reqURL("/api/v1/shortcuts/tasks")),
};
