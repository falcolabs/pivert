import {
    User,
    BadgeUUID,
    BadgeInfo,
    CategoryID,
    LevelingCategoryInfo,
    Habit,
    Todo,
    type Reward,
} from "./schema";

export type ShortcutTasks = {
    habits: { [key: string]: Habit };
    todos: { [key: string]: Todo };
};

export type ShortcutTrain = {
    user: User;
    habits: { [key: string]: Habit };
    todos: { [key: string]: Todo };
};

export type ShortcutRewards = {
    user: User;
    userRewards: { [key: string]: Reward };
    systemRewards: { [key: string]: Reward };
};

export type ShortcutAchievementsInfo = {
    badgeInfo: { [key: BadgeUUID]: BadgeInfo };
    lvlInfo: { [key: CategoryID]: LevelingCategoryInfo };
};

export type ShortcutHome = {
    user: User;
    achievementInfo: ShortcutAchievementsInfo;
};
