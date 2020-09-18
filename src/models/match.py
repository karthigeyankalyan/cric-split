import uuid

from src.common.database import Database
from datetime import datetime


class Match(object):

    def __init__(self, team_1, team_2, match_date, match_id, _id=None):
        self.match_id = match_id
        self.team_1 = team_1
        self.team_2 = team_2
        if match_date:
            self.match_date = (datetime.combine(datetime.strptime(match_date, '%Y-%m-%d').date(),
                                                datetime.now().time()))
        else:
            self.match_date = match_date
        self._id = uuid.uuid4().hex if _id is None else _id

    def save_to_mongo(self):
        Database.insert(collection='match', data=self.json())

    def json(self):
        return {
            "match_id": self.match_id,
            "team_1": self.team_1,
            "team_2": self.team_2,
            "match_date": self.match_date,
            "_id": self._id
        }
