import uuid

from src.common.database import Database


class Player(object):

    def __init__(self, player_id, player_name, value_per_share, max_share_cap, player_profile, match_id, motm,
                 runs_scored, balls_faced, runs_conceded, overs, balls_bowled, wkts_taken, maidens, dot_balls,
                 catches_taken, run_outs, stumpings, points_scored, value_change, _id=None, fours=None, sixes=None):
        self.player_id = player_id
        self.player_profile = player_profile
        self.player_name = player_name
        self.value_per_share = value_per_share
        self.max_share_cap = max_share_cap
        self.match_id = match_id
        self.motm = motm
        self.overs = overs
        self.runs_scored = runs_scored
        self.balls_faced = balls_faced
        self.fours = fours
        self.sixes = sixes
        self.runs_conceded = runs_conceded
        self.balls_bowled = balls_bowled
        self.wkts_taken = wkts_taken
        self.maidens = maidens
        self.dot_balls = dot_balls
        self.catches_taken = catches_taken
        self.run_outs = run_outs
        self.stumpings = stumpings
        self.points_scored = points_scored
        self.value_change = value_change
        self._id = uuid.uuid4().hex if _id is None else _id

    def save_to_mongo(self):
        Database.insert(collection='player', data=self.json())

    def json(self):
        return {
            "player_id": self.player_id,
            "player_profile": self.player_profile,
            "player_name": self.player_name,
            "value_per_share": self.value_per_share,
            "max_share_cap": self.max_share_cap,
            "match_id": self.match_id,
            "motm": self.motm,
            "overs": self.overs,
            "runs_scored": self.runs_scored,
            "balls_faced": self.balls_faced,
            "runs_conceded": self.runs_conceded,
            "balls_bowled": self.balls_bowled,
            "maidens": self.maidens,
            "wkts_taken": self.wkts_taken,
            "dot_balls": self.dot_balls,
            "catches_taken": self.catches_taken,
            "run_outs": self.run_outs,
            "stumpings": self.stumpings,
            "points_scored": self.points_scored,
            "value_change": self.value_change,
            "_id": self._id
        }
