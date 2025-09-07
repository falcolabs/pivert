import typing
from pydantic import BaseModel
import schema


class ShortcutTasks(BaseModel):
    habits: dict[schema.HabitUUID, schema.Habit]
    todos: dict[schema.TodoUUID, schema.Todo]


class ShortcutAchievementsInfo(BaseModel):
    badgeInfo: dict[schema.BadgeUUID, schema.BadgeInfo]
    lvlInfo: dict[schema.CategoryID, schema.LevelingCategoryInfo]


class ShortcutHome(BaseModel):
    user: schema.User
    achievementInfo: ShortcutAchievementsInfo
