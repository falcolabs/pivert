export * as requests from "./backend";
import { writable, type Writable } from "svelte/store";
import * as requests from "./backend";
// import { LazyStore } from "@tauri-apps/plugin-store";
import type * as schema from "./schema";

export type * as schema from "./schema";

// let _store: LazyStore;

// @ts-expect-error
export const loggedIn: Writable<boolean> = writable(null);

export const loadStore = async () => {
    // _store = new LazyStore("store.json", {
    //     autoSave: true,
    //     defaults: {
    //         userID: null,
    //         username: null,
    //         user: null,
    //         token: null,
    //         habits: null,
    //         todos: null,
    //     },
    // });
    // _store.save();
    // let t = await _store.get("token");
    let t = window.localStorage.getItem("token")
    console.log("syncing token", t);
    requests.updateToken();
    if (t !== "") {
        loggedIn.set(true);
        return;
    }
    loggedIn.set(false);
};

export type StoreType = {
    userID: string;
    user: schema.User;
    username: string;
    token: string;
    habits: { [key: string]: schema.Habit };
    todos: { [key: string]: schema.Todo };
    achievementInfo: { [key: string]: schema.BadgeInfo };
};

// type StoreKey = keyof StoreType;
// type StoreValueType<K extends keyof StoreType> = StoreType[K];

// export const store = {
//     get: async function storeGet<T extends StoreKey>(
//         key: T,
//     ): Promise<StoreValueType<T>> {
//         // @ts-expect-error
//         return await _store.get(key);
//     },
//     set: async function storeSet<T extends StoreKey>(
//         key: T,
//         value: StoreValueType<T>,
//     ): Promise<void> {
//         return await _store.set(key, value);
//     },
// };
export async function login(username: string, password: string): Promise<void> {
    let r = await requests.login(username, password);
    // await _store.set("token", r.access_token);
    localStorage.setItem("token", r.access_token);
    requests.updateToken();
    loggedIn.set(true);
    console.log("logged in");
}

export async function logout() {
    // await _store.set("token", null);
    localStorage.setItem("token", "");
    requests.updateToken();
    loggedIn.set(false);
    console.log("logged out");
}

// https://stackoverflow.com/questions/9083037/convert-a-number-into-a-roman-numeral-in-javascript
export function toRomanNumerals(num: number) {
    if (isNaN(num)) return NaN;
    var digits = String(+num).split(""),
        key = [
            "",
            "C",
            "CC",
            "CCC",
            "CD",
            "D",
            "DC",
            "DCC",
            "DCCC",
            "CM",
            "",
            "X",
            "XX",
            "XXX",
            "XL",
            "L",
            "LX",
            "LXX",
            "LXXX",
            "XC",
            "",
            "I",
            "II",
            "III",
            "IV",
            "V",
            "VI",
            "VII",
            "VIII",
            "IX",
        ],
        roman = "",
        i = 3;
    while (i--) roman = (key[+digits.pop()! + i * 10] || "") + roman;
    return Array(+digits.join("") + 1).join("M") + roman;
}
