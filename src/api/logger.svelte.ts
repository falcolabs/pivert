export let logEntries: string[] = [];

export const addLogEntry = (e: string) => {
    logEntries.push(e);
};
