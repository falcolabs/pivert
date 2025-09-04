export * as requests from "./backend";
import * as requests from "./backend";

import { load, Store } from "@tauri-apps/plugin-store";

let _store: Store;

export const loadStore = async () => {
    _store = await load("store.json", {
        autoSave: true,
        defaults: {
            userID: undefined,
            username: undefined,
            user: undefined,
            token: undefined,
            habits: undefined,
            todos: undefined,
        },
    });
};

export type StoreType = {
    userID: string;
    user: User;
    username: string;
    token: string;
    habits: { [key: string]: Habit };
    todos: { [key: string]: Todo };
};
type StoreKey = keyof StoreType;
type StoreValueType<K extends keyof StoreType> = StoreType[K];

export const store = {
    get: async function storeGet<T extends StoreKey>(
        key: T,
    ): Promise<StoreValueType<T>> {
        // @ts-expect-error
        return await _store.get(key);
    },
    set: async function storeSet<T extends StoreKey>(
        key: T,
        value: StoreValueType<T>,
    ): Promise<void> {
        return await _store.set(key, value);
    },
};

export async function login(username: string, password: string): Promise<void> {
    let r = await requests.login(username, password);
    _store.set("token", r.access_token);
}

export async function isLoggedIn(): Promise<boolean> {
    if (_store === undefined) return false;
    return (await _store.get("token")) !== undefined;
}
