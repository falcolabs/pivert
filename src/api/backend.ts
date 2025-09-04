import { fetch } from "@tauri-apps/plugin-http";

let token: string = "";

const reqURL = (path: string, params: { [key: string]: string } = {}): URL => {
    let o = new URL("http://localhost:6942" + path);
    for (let [k, v] of Object.entries(params)) {
        o.searchParams.append(k, v);
    }
    return o;
};

export const bfetch = async (
    path: URL,
    method: "GET" | "POST" = "GET",
    payload?: object | FormData,
): Promise<Response> => {
    let r = await fetch(path, {
        method: method,
        headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
        },
        body: payload instanceof FormData ? payload : JSON.stringify(payload),
    });
    if (r.status != 200) {
        throw new Error(await r.json());
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
): Promise<boolean> {
    await bfetch(
        reqURL("/api/v1/register", { username: username, password: password }),
    );
    return true;
}

export async function login(form: HTMLFormElement): Promise<Token>;
export async function login(username: string, password: string): Promise<Token>;
export async function login(
    usernameOrForm: string | HTMLFormElement,
    password?: string,
): Promise<Token> {
    let payload: FormData;

    if (typeof usernameOrForm === "string") {
        payload = new FormData();
        if (password === undefined)
            throw new Error(
                "password must not be undefined if username is provided",
            );
        payload.append(usernameOrForm, password);
    } else {
        payload = new FormData(usernameOrForm);
    }
    return (await fetchJSON(reqURL("/api/v1/token"), "POST", payload))
        .access_token;
}

export async function currentSession(): Promise<boolean> {
    return (await fetchJSON(reqURL("/api/v1/currentSession"))).success;
}

export async function me(): Promise<User> {
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
    todo: async (todo: Todo): Promise<string> => await _createTask("todo", todo),
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
