export * as shortcuts from "./shortcuts";

export type UserUUID = string;
export type RelationshipUUID = string;
export type HabitUUID = string;
export type TodoUUID = string;
export type BadgeUUID = string;
export type CategoryID = string;
export type RewardUUID = string;
export type RelationshipLevel = "none" | "friends" | "close";
export type TaskType = "habit" | "todo";
export type UserDataQueryType = "uuid" | "username";

export type UserMetrics = {
    health: number;
    cash: number;
    xp: number;
    allTimeXP: number;
};

export type UserSocialLink = {
    facebook: string;
    threads: string;
    tiktok: string;
};

export type LevelingStatus = {
    category: CategoryID;
    progress: float;
};

export type UserAchievements = {
    badges: BadgeUUID[];
    leveling: LevelingStatus[];
};

export type Token = {
    access_token: string;
    token_type: string;
};

export type User = {
    userID: UserUUID;
    username: string;
    displayname: string?;
    avatarURL: string;
    public: bool;
    disabled: bool;
    creationTimestamp: number;

    metrics: UserMetrics;
    social: UserSocialLink;
    achievements: UserAchievements;

    relationships: RelationshipUUID[];
    habits: HabitUUID[];
    todos: TodoUUID[];

    userRewards: RewardUUID[];
    systemRewards: RewardUUID[];
};

export type AuthenticationEntry = {
    userID: UserUUID;
    hashedPassword: string;
};

export type Relationship = {
    target: UserUUID;
    level: RelationshipLevel;
};

export type TaskReward = {
    health: number;
    cash: number;
    xp: number;
};

export type Habit = {
    taskID: HabitUUID;
    name: string;
    icon: string;
    description: string?;
    congratsMessage: string;
    rewards: TaskReward;
};

export type Todo = {
    taskID: TodoUUID;
    name: string;
    icon: string;
    description: string?;
    congratsMessage: string?;
    rewards: TaskReward;
    deadline: number;
    completed: bool;
};

export type LevelingCategoryInfo = {
    catID: CategoryID;
    name: string;
    allTimeXPRequired: number[];
};

export type BadgeInfo = {
    badgeID: BadgeUUID;
    name: string;
    maxLevel: number;
    coverArtURL: string[];
};

export type Reward = {
    rewardID: RewardUUID;
    name: string;
    icon?: string;
    description?: string;
    congratsMessage?: string;
    cost: TaskReward;
    timesClaimed: number;
    maxClaims?: number;
};
