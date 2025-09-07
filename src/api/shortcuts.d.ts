import {
    User,
    BadgeUUID,
    BadgeInfo,
    CategoryID,
    LevelingCategoryInfo,
    Habit,
    Todo,
} from "./schema";

export type ShortcutTasks = {
    habits: { [key: string]: Habit };
    todos: { [key: string]: Todo };
};

export type ShortcutAchievementsInfo = {
    badgeInfo: { [key: BadgeUUID]: BadgeInfo };
    lvlInfo: { [key: CategoryID]: LevelingCategoryInfo };
};

export type ShortcutHome = {
    user: User;
    achievementInfo: ShortcutAchievementsInfo;
};
