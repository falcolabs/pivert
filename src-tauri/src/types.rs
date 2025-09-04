use serde::{Serialize, Deserialize};

pub type UserUUID = String;
pub type RelationshipUUID = String;
pub type HabitUUID = String;
pub type TodoUUID = String;
pub type BadgeUUID = String;
pub type CategoryID = String;

#[derive(Serialize, Deserialize, Debug, PartialEq, Eq, Clone, Copy)]
#[serde(rename_all = "lowercase")]
pub enum RelationshipLevel {
    None,
    Friends,
    Close
}

#[derive(Serialize, Deserialize, Debug, PartialEq, Eq, Clone, Copy)]
#[serde(rename_all = "camelCase")]
struct UserMetrics {
    health: i32,
    energy: i32,
    exp: i32,
}

#[derive(Serialize, Deserialize, Debug, PartialEq, Eq, Clone)]
#[serde(rename_all = "camelCase")]
struct UserSocialLink {
    facebook: String,
    threads: String,
    tiktok: String
}

#[derive(Serialize, Deserialize, Debug, PartialEq, Clone)]
#[serde(rename_all = "camelCase")]
struct LevelingStatus {
    category: CategoryID,
    progress: f32
}

#[derive(Serialize, Deserialize, Debug, PartialEq, Clone)]
#[serde(rename_all = "camelCase")]
struct UserAchievements {
    badges: std::sync::Arc<[BadgeUUID]>,
    leveling: std::sync::Arc<[LevelingStatus]>
}

#[derive(Serialize, Deserialize, Debug, PartialEq, Eq, Clone)]
#[serde(rename_all = "camelCase")]
struct Token {
    access_token: String,
    token_type: String
}

#[derive(Serialize, Deserialize, Debug, PartialEq, Clone)]
#[serde(rename_all = "camelCase")]
struct User {
    #[serde(rename = "userID")]
    user_id: UserUUID,
    username: String,
    displayname: Option<String>,
    public: bool,
    disabled: bool,
    creation_timestamp: i32,

    metrics: UserMetrics,
    social: UserSocialLink,
    achievements: UserAchievements,

    relationships: std::sync::Arc<RelationshipUUID>,
    habits: std::sync::Arc<HabitUUID>,
    todos: std::sync::Arc<TodoUUID>
}

#[derive(Serialize, Deserialize, Debug, PartialEq, Eq, Clone)]
#[serde(rename_all = "camelCase")]
struct AuthenticationEntry {
    #[serde(rename = "userID")]
    user_id: UserUUID,
    hashed_password: String
}

#[derive(Serialize, Deserialize, Debug, PartialEq, Eq, Clone)]
#[serde(rename_all = "camelCase")]
struct Relationship {
    target: UserUUID,
    level: RelationshipLevel
}

#[derive(Serialize, Deserialize, Debug, PartialEq, Eq, Clone, Copy)]
#[serde(rename_all = "camelCase")]
struct TaskReward {
    health: i32,
    energy: i32,
    exp: i32
}

#[derive(Serialize, Deserialize, Debug, PartialEq, Eq, Clone)]
#[serde(rename_all = "camelCase")]
struct Habit {
    #[serde(rename = "taskID")]
    task_id: HabitUUID,
    name: String,
    description: Option<String>,
    congrats_message: String,
    rewards: TaskReward
}

#[derive(Serialize, Deserialize, Debug, PartialEq, Eq, Clone)]
#[serde(rename_all = "camelCase")]
struct Todo {
    #[serde(rename = "taskID")]
    task_id: TodoUUID,
    name: String,
    description: Option<String>,
    congrats_message: Option<String>,
    rewards: TaskReward,
    deadline: i32,
    completed: bool
}
