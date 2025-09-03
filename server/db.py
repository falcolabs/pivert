import tinydb
import os
import typing
from tinydb.table import Table
from tinydb import Query
import schema

_DB = tinydb.TinyDB("db.json")
AuthStore: schema.TypedTable[schema.AuthenticationEntry] = schema.__AuthStore(_DB.table("auth"))
UserStore: schema.TypedTable[schema.User] = schema.__UserStore(_DB.table("users"))
HabitsStore: schema.TypedTable[schema.Habit] = schema.__HabitsStore(_DB.table("habits"))
TodosStore: schema.TypedTable[schema.Todo] = schema.__TodosStore(_DB.table("todos"))
RelationshipStore: schema.TypedTable[schema.Relationship] = schema.__RelationshipStore(_DB.table("relationships"))
