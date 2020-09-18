import uuid

from src.common.database import Database
from datetime import datetime


class Team(object):

    def __init__(self, team_name, value_per_share, player_id, player_name, shares_purchased, match_id, user_name,
                 user_id, points_accrued=None, change_in_value=None, _id=None, team_id=None):
        self.team_name = team_name
        self.team_id = team_id
        self.value_per_share = value_per_share
        self.player_id = player_id
        self.match_id = match_id
        self.user_id = user_id
        self.user_name = user_name
        self.player_name = player_name
        self.shares_purchased = shares_purchased
        self.points_accrued = points_accrued
        self.change_in_value = change_in_value
        self._id = uuid.uuid4().hex if _id is None else _id

    def save_to_mongo(self):
        Database.insert(collection='teams', data=self.json())

    def json(self):
        return {
            "value_per_share": self.value_per_share,
            "team_name": self.team_name,
            "player_id": self.player_id,
            "team_id": self.team_id,
            "user_id": self.user_id,
            "user_name": self.user_name,
            "match_id": self.match_id,
            "player_name": self.player_name,
            "shares_purchased": self.shares_purchased,
            "points_accrued": self.points_accrued,
            "change_in_value" : self.change_in_value,
            "_id": self._id
        }
