import pytz
from flask import Flask, redirect, session, render_template, make_response, request

from cricAuth.auth import app as auth
from cricCHAT2.cricCHAT2 import app as cricCHAT2
from cricLIVE.livescore import app as livescore
# start
from cricMongoDB.database import db
from cricNEWS.news import app as news
from cricPlayer.player import app as player
from cricPrediction.predictions import app as prediction
from cricProfile.user_data import app as profile
from cricRanking.show_ranking import app as ranking_try
from cricSTAT.t20Stat import app as stat

# end

# from cricCHAT.server import app as chat
# from cricCHAT import server

app = Flask(__name__)
app.secret_key = 'TishuPaperIsNoMore'

# start
app.debug = True
# end


# authentication blueprint
app.register_blueprint(auth)

# live score blueprint
app.register_blueprint(livescore)

# prediction blueprint
app.register_blueprint(prediction)

# show ranking blueprint
app.register_blueprint(ranking_try)

# t20 Statistics blueprint
app.register_blueprint(stat)

# news blueprint
app.register_blueprint(news)

# player blueprint
app.register_blueprint(player)

# user profile blueprint
app.register_blueprint(profile)

# user profile blueprint
app.register_blueprint(cricCHAT2)


# chat-box
# app.register_blueprint(chat)

@app.route('/')
def home():
    # if 'username' not in session.keys():
    #     return redirect('/auth/signin')
    from cricSchedule import schedule_adapter
    data = schedule_adapter.Adapter()
    return render_template('index.html', matches=data.get_match_data())


@app.template_filter('formatdatetime')
def format_datetime(value, format="%a %d %B %I:%M %p"):
    if value is None:
        return ""
    tz = pytz.timezone('Asia/Dacca')  # timezone you want to convert to from UTC
    utc = pytz.timezone('UTC')
    value = utc.localize(value, is_dst=None).astimezone(pytz.utc)
    local_dt = value.astimezone(tz)
    return local_dt.strftime(format)


# @app.route('/chat-box')
# def chat():
#    execfile('server.py')


# start
@app.route('/chat-box/')
def chat():
    if 'username' not in session.keys():
        return redirect('/auth/signin')

    data = []
    data = db.chat.find()

    message = []
    for item in data:
        tmp = []
        tmp.append(item["author"])
        tmp.append(item["message"])
        message.append(tmp)

    if request.cookies.get('realtime-chat-nickname') is None:
        res = make_response(render_template("chat.html", list=message))
        res.set_cookie('realtime-chat-nickname', session['username'])
        print(res)
        return res

    else:

        # data = [];
        # data = db.chat.find();

        # message = [];
        # for item in data:
        #    tmp = [];
        #    tmp.append(item["author"]);
        #    tmp.append(item["message"]);
        #    message.append(tmp);

        return render_template("chat.html", list=message)


if __name__ == '__main__':
    app.run(debug=True)
