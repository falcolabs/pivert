type UserUUID = string;
type RelationshipUUID = string;
type HabitUUID = string;
type TodoUUID = string;
type BadgeUUID = string;
type CategoryID = string;
type RelationshipLevel = "none" | "friends" | "close";
type TaskType = "habit" | "todo";
type UserDataQueryType = "uuid" | "username";

type UserMetrics = {
    health: int;
    energy: int;
    exp: int;
};

type UserSocialLink = {
    facebook: string;
    threads: string;
    tiktok: string;
};

type LevelingStatus = {
    category: CategoryID;
    progress: float;
};

type UserAchievements = {
    badges: BadgeUUID[];
    leveling: LevelingStatus[];
};

type Token = {
    access_token: string;
    token_type: string;
};

type User = {
    userID: UserUUID;
    username: string;
    displayname: string?;
    public: bool;
    disabled: bool;
    creationTimestamp: int;

    metrics: UserMetrics;
    social: UserSocialLink;
    achievements: UserAchievements;

    relationships: RelationshipUUID[];
    habits: HabitUUID[];
    todos: TodoUUID[];
};

type AuthenticationEntry = {
    userID: UserUUID;
    hashedPassword: string;
};

type Relationship = {
    target: UserUUID;
    level: RelationshipLevel;
};

type TaskReward = {
    health: int;
    energy: int;
    exp: int;
};

type Habit = {
    taskID: HabitUUID;
    name: string;
    description: string?;
    congratsMessage: string;
    rewards: TaskReward;
};

type Todo = {
    taskID: TodoUUID;
    name: string;
    description: string?;
    congratsMessage: string?;
    rewards: TaskReward;
    deadline: int;
    completed: bool;
};

type ShortcutTasks = {
    habits: Habit[];
    todos: Todo[];
};
