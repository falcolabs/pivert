export * as requests from "./backend";
import { writable, type Writable } from "svelte/store";
import * as requests from "./backend";
import type * as schema from "./schema";

export type * as schema from "./schema";

// @ts-expect-error
export const loggedIn: Writable<boolean> = writable(null);

if (requests.token !== "") {
    loggedIn.set(true);
} else {
    loggedIn.set(false);
}
// let t = window.localStorage.getItem("token");
// requests.log("syncing token", t);
// requests.updateToken();
// if (t !== "") {
//
// }
//

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
    window.localStorage.setItem("token", r.access_token);
    requests.updateToken();
    loggedIn.set(true);
    requests.log("logged in");
}

export async function logout() {
    // await _store.set("token", null);
    window.localStorage.setItem("token", "");
    requests.updateToken();
    loggedIn.set(false);
    requests.log("logged out");
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
