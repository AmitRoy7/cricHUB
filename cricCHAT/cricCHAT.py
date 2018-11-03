import pusher
from cricAuth.auth import signin
from flask import Flask,render_template,jsonify,request,Blueprint,session,redirect
from cricMongoDB.database import db

app = Blueprint('cricCHAT', __name__)

pusher_client = pusher.Pusher(
  app_id='630604',
  key='76e1eff5e36b22e9f0ef',
  secret='a583aa33cdf7b65a5d07',
  cluster='ap2',
  ssl=True
)


@app.route('/chat-room/')
def index():

    if 'username' not in session.keys():
        return signin(None, "/chat-room/")
    messages = db.chat.find()
    return render_template('chat/chat.html', messages=messages)


@app.route('/message', methods=['POST'])
def message():


    if 'username' not in session.keys():
        return signin(None, "/message/")

    print(request.form.to_dict())
    try:

        username = request.form.get('author')
        message = request.form.get('message')

        #print(request.form.to_dict())

        new_message ={}
        new_message["author"] = username
        new_message["message"] = message
        posts = db.chat
        posts.insert_one(new_message)

        pusher_client.trigger('my-channel', 'new-message', {'author': username, 'message': message})

        return render_template('chat/chat.html')

    except:

        return jsonify({'result': 'failure'})

