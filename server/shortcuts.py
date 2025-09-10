import typing
from pydantic import BaseModel
import schema


class ShortcutTasks(BaseModel):
    habits: dict[schema.HabitUUID, schema.Habit]
    todos: dict[schema.TodoUUID, schema.Todo]

class ShortcutTrain(BaseModel):
    user: schema.User
    habits: dict[schema.HabitUUID, schema.Habit]
    todos: dict[schema.TodoUUID, schema.Todo]

class ShortcutRewards(BaseModel):
    user: schema.User
    userRewards: dict[schema.RewardUUID, schema.Reward]
    systemRewards: dict[schema.RewardUUID, schema.Reward]

class ShortcutAchievementsInfo(BaseModel):
    badgeInfo: dict[schema.BadgeUUID, schema.BadgeInfo]
    lvlInfo: dict[schema.CategoryID, schema.LevelingCategoryInfo]


class ShortcutHome(BaseModel):
    user: schema.User
    achievementInfo: ShortcutAchievementsInfo
