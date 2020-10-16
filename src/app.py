from bson import json_util, ObjectId
from flask import Flask, render_template, request, session, json
from src.models.user import User
from src.common.database import Database
from src.models.teams import Team
from src.models.player import Player
import csv
from io import StringIO

app = Flask(__name__)
app.secret_key = "commercial"


@app.before_first_request
def initialize_database():
    Database.initialize()


@app.route('/')
@app.route('/login')
def home_page():
    return render_template('login.html')


@app.route('/logout/<string:user_id>')
def logout(user_id):
    user = User.get_by_id(user_id)
    user.logout()
    return render_template('login.html')


@app.route('/register')
def register_form():
    return render_template('register.html')


@app.route('/how_to_play')
def how_to_play():
    email = session['email']
    user = User.get_by_email(email)
    return render_template('profile1.html', user=user)


@app.route('/authorize/login', methods=['POST'])
def login_user():
    email = request.form['user']
    password = request.form['password']
    valid = User.valid_login(email, password)
    User.login(email)
    user = User.get_by_email(email)

    # if Database.is_valid(user._id):
    #     user_id = ObjectId(user._id)
    # else:
    #     user_id = user._id
    #

    if valid:
        return render_template('profile1.html', user=user)

    else:
        return render_template('login_fail.html', user=user)


@app.route('/profile/<string:user_id>')
def user_profile(user_id):
    user = User.get_by_id(user_id)

    if user is not None:
        return render_template('profile.html', user=user)
    else:
        return render_template('login_fail.html', user=user)


@app.route('/authorize/register', methods=['POST'])
def register_user():
    email = request.form['user']
    password = request.form['password']

    User.register(email=email, password=password)

    user = User.get_by_email(email)

    return render_template('profile1.html', user=user)


@app.route('/raw_market_list/<string:team1>/<string:team2>')
def get_raw_market_players(team1, team2):
    all_credit = []
    all_credit_dict = Database.find("market", {"$or": [{"Team": team1},
                                                       {"Team": team2}]})
    for tran in all_credit_dict:
        all_credit.append(tran)

    all_credits = json.dumps(all_credit, default=json_util.default)

    return all_credits


@app.route('/raw_buy_player/<string:player_id>')
def get_raw_player_by_id(player_id):
    all_credit = []
    all_credit_dict = Database.find("market", {"ID": player_id})
    for tran in all_credit_dict:
        all_credit.append(tran)

    all_credits = json.dumps(all_credit, default=json_util.default)

    return all_credits


@app.route('/raw_players_by_match/<string:match_id>')
def get_raw_players_by_match_id(match_id):
    all_credit = []
    all_credit_dict = Database.find("player", {"match_id": int(match_id)})
    for tran in all_credit_dict:
        all_credit.append(tran)

    all_credits = json.dumps(all_credit, default=json_util.default)

    return all_credits


@app.route('/raw_players_all')
def get_raw_players_by_match_id_all():
    all_credit = []
    all_credit_dict = Database.find("player", {})
    for tran in all_credit_dict:
        all_credit.append(tran)

    all_credits = json.dumps(all_credit, default=json_util.default)

    return all_credits


@app.route('/raw_team/<string:match_id>/<string:user_id>')
def get_raw_teams(match_id, user_id):
    all_credit = []
    all_credit_dict = Database.find("teams", {"$and": [{"match_id": match_id},
                                                       {"user_id": user_id}]})
    for tran in all_credit_dict:
        all_credit.append(tran)

    all_credits = json.dumps(all_credit, default=json_util.default)

    return all_credits


@app.route('/raw_team_all/<string:match_id>')
def get_raw_teams_by_match(match_id):
    all_credit = []
    all_credit_dict = Database.find("teams", {"match_id": match_id})
    for tran in all_credit_dict:
        all_credit.append(tran)

    all_credits = json.dumps(all_credit, default=json_util.default)

    return all_credits


@app.route('/raw_teams_all')
def get_raw_teams_all():
    all_credit = []
    all_credit_dict = Database.find("teams", {})
    for tran in all_credit_dict:
        all_credit.append(tran)

    all_credits = json.dumps(all_credit, default=json_util.default)

    return all_credits


@app.route('/aggregate_points/<string:user_id>')
def total_points(user_id):
    user = User.get_by_id(user_id)
    return render_template('aggregation.html', user=user)


@app.route('/raw_matches')
def get_raw_matches():
    all_credit = []
    all_credit_dict = Database.find("matches", {})
    for tran in all_credit_dict:
        all_credit.append(tran)

    all_credits = json.dumps(all_credit, default=json_util.default)

    return all_credits


@app.route('/delete_team/<string:match_id>/<string:user_id>')
def delete_team(match_id, user_id):
    user = User.get_by_id(user_id)
    if user is not None:
        Database.delete_from_mongo(collection='teams', query={'match_id': match_id, 'user_id': user_id})
        return render_template('TeamDeleted.html', user=user, match_id=match_id, user_id=user_id)
    else:
        return render_template('login_fail.html', user=user)


@app.route('/view_team/<string:match_id>/<string:user_id>')
def view_team(match_id, user_id):
    user = User.get_by_id(user_id)
    if user is not None:
        return render_template('ViewTeam.html', user=user, match_id=match_id, user_id=user_id)
    else:
        return render_template('login_fail.html', user=user)


@app.route('/view_team_algorithm/<string:match_id>/<string:user_id>')
def view_team_algorithm(match_id, user_id):
    user = User.get_by_id(user_id)
    if user is not None:
        return render_template('ViewTeamAlgorithm.html', user=user, match_id=match_id, user_id=user_id)
    else:
        return render_template('login_fail.html', user=user)


@app.route('/view_matches/<string:user_id>')
def view_matches(user_id):
    user = User.get_by_id(user_id)
    if user is not None:
        return render_template('ViewMatches.html', user=user, user_id=user_id)
    else:
        return render_template('login_fail.html', user=user)


@app.route('/view_matches_beaters/<string:user_id>')
def view_matches_beaters(user_id):
    user = User.get_by_id(user_id)
    if user is not None:
        return render_template('ViewMatchesBeaters.html', user=user, user_id=user_id)
    else:
        return render_template('login_fail.html', user=user)


@app.route('/user_algorithm_comparison/<string:user_id>/<string:match_id>')
def user_algorithm_comp(user_id, match_id):
    user = User.get_by_id(user_id)
    if user is not None:
        return render_template('user_algo_comparison.html', user=user, user_id=user_id, match_id=match_id)
    else:
        return render_template('login_fail.html', user=user)


@app.route('/user_algorithm_comparison_beaters/<string:user_id>/<string:match_id>')
def user_algorithm_comp_beaters(user_id, match_id):
    user = User.get_by_id(user_id)
    if user is not None:
        return render_template('algo_beaters.html', user=user, user_id=user_id, match_id=match_id)
    else:
        return render_template('login_fail.html', user=user)


@app.route('/paste_scores/<string:user_id>/<string:match_id>')
def convert_csv(user_id, match_id):
    user = User.get_by_id(user_id)

    Database.delete_from_mongo(collection='player', query={'match_id': 1331})

    csv_string = """player_name,runs_scored,balls_faced,fours,sixes,overs,maidens,runs_conceded,dot_balls,wkts_taken,player_profile,match_id,value_per_share,max_share_cap,player_id,out
AJ Finch,20,18,2,1,0,0,0,0,0,Batsman,1331,800,125,102,1
D Padikkal,18,12,1,1,0,0,0,0,0,Batsman,1331,700,140,114,1
V Kohli,48,39,3,0,0,0,0,0,0,Batsman,1331,900,110,101,1
Washington Sundar,13,14,1,0,4,0,38,6,0,Bowler,1331,700,140,111,1
S Dube,23,19,0,2,0,0,0,0,0,Batsman,1331,800,125,113,1
AB de Villiers,2,5,0,0,0,0,0,0,0,Batsman,1331,1000,100,100,1
CH Morris,25,8,1,3,4,0,22,12,0,All rounder,1331,700,140,104,0
I Udana,10,5,0,1,2,0,14,4,0,All rounder,1331,600,165,116,0
KL Rahul,61,49,1,5,0,0,0,0,0,Wicket keeper,1331,1000,100,700,0
MA Agarwal,45,25,4,3,0,0,0,0,0,Batsman,1331,900,110,704,1
CH Gayle,53,45,1,5,0,0,0,0,0,Batsman,1331,700,140,703,1
N Pooran,6,1,0,1,0,0,0,0,0,Wicket keeper,1331,700,140,706,0
NA Saini,0,0,0,0,4,0,21,14,0,Bowler,1331,800,125,105,0
YS Chahal,0,0,0,0,3,0,35,8,1,Bowler,1331,900,110,103,0
Mohammed Siraj,0,0,0,0,3,0,44,2,0,Bowler,1331,600,165,110,0
GJ Maxwell,0,0,0,0,4,0,28,6,0,Batsman,1331,900,110,701,0
Mohammed Shami,0,0,0,0,4,0,45,6,2,Bowler,1331,900,110,705,0
Arshdeep Singh,0,0,0,0,2,0,20,3,1,Bowler,1331,500,200,723,0
Ravi Bishnoi,0,0,0,0,3,0,29,6,0,Bowler,1331,700,140,714,0
M Ashwin,0,0,0,0,4,0,23,7,2,Bowler,1331,700,140,716,0
CJ Jordan,0,0,0,0,3,0,20,5,1,Bowler,1331,600,165,710,0
"""
    reader = csv.DictReader(StringIO(csv_string))
    json_data = json.dumps(list(reader))
    final_json = json.loads(json_data)

    for j in final_json:
        player = Player(player_id=j['player_id'], match_id=int(j['match_id']), player_name=j['player_name'],
                        value_per_share=int(j['value_per_share']), balls_faced=int(j['balls_faced']),
                        runs_scored=int(j['runs_scored']), fours=int(j['fours']), sixes=int(j['sixes']),
                        overs=int(j['overs']), maidens=int(j['maidens']), runs_conceded=int(j['runs_conceded']),
                        dot_balls=int(j['dot_balls']),
                        wkts_taken=int(j['wkts_taken']), player_profile=j['player_profile'],
                        max_share_cap=int(j['max_share_cap']), balls_bowled=int(j['overs'])*6)

        player.save_to_mongo()

    return render_template('shares_purchased_new.html')


@app.route('/ViewMarket/<string:user_id>/<string:team1>/<string:team2>/<string:match_id>', methods=['POST', 'GET'])
def view_market(team1, team2, match_id, user_id):
    user = User.get_by_id(user_id)
    if user is not None:
        if request.method == 'GET':
            return render_template('ViewMarket.html', user=user, team1=team1, team2=team2, match_id=match_id)
        else:
            num_players = request.form['numPlayers']

            Database.delete_from_mongo(collection='teams', query={'match_id': match_id, 'user_id': user._id})
            for i in range(int(num_players)):
                player_id_string = "id_form_var" + str(i)
                num_shares_string = "num_shares_form_var" + str(i)
                player_name_string = "player_form_var" + str(i)

                player_id = request.form[player_id_string]
                num_shares = request.form[num_shares_string]
                player_name = request.form[player_name_string]

                player = Database.find("market", {"ID": int(player_id)})
                team, value_per_share = None, None

                for p in player:
                    team = p['Team']
                    value_per_share = int(p['Base price'])

                team = Team(player_id=player_id, team_name=team, shares_purchased=float(num_shares), match_id=match_id,
                            player_name=player_name, value_per_share=value_per_share, user_name=user.email,
                            user_id=user_id)

                team.save_to_mongo()

            return render_template('shares_purchased.html', user=user, match_id=match_id)

    else:
        return render_template('login_fail.html', user=user)


# @app.route('/buy_player/<string:player_id>', methods=['POST', 'GET'])
# def buy_player(player_id):
#     email = session['email']
#     user = User.get_by_email(email)
#     if email is not None:
#         if request.method == 'GET':
#             return render_template('BuyPlayer.html', user=user, player_id=player_id)
#         else:
#
#     else:
#         return render_template('login_fail.html', user=user)


if __name__=='__main__':
    app.run(port=4095, debug=True)

