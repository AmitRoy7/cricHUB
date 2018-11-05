import pusher
import abc
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



class Subject:
    """
    Know its observers. Any number of Observer objects may observe a
    subject.
    Send a notification to its observers when its state changes.
    """

    def __init__(self):
        self._observers = set()
        self._subject_state = None

    def attach(self, observer):
        observer._subject = self
        self._observers.add(observer)
        self.register()

    def detach(self, observer):
        observer._subject = None
        self._observers.discard(observer)

    def _notify(self):
        for observer in self._observers:
            observer.update(self._subject_state)

    @property
    def subject_state(self):
        return self._subject_state

    @subject_state.setter
    def subject_state(self, arg):
        self._subject_state = arg
        self._notify()

    @app.route('/chat-room/')
    def register(self=None):

        if 'username' not in session.keys():
            return signin(None, "/chat-room/")
        messages = db.chat.find()
        return render_template('chat/chat.html', messages=messages)


class Observer(metaclass=abc.ABCMeta):
    """
    Define an updating interface for objects that should be notified of
    changes in a subject.
    """

    def __init__(self):
        self._subject = None
        self._observer_state = None

    @abc.abstractmethod
    def update(self, arg):
        pass



class ConcreteObserver(Observer):
    """
    Implement the Observer updating interface to keep its state
    consistent with the subject's.
    Store state that should stay consistent with the subject's.
    """

    def update(self, arg):
        self._observer_state = arg
        self.message()


    @app.route('/message', methods=['POST'])
    def message(self=None):


        if 'username' not in session.keys():
            return signin(None, "/message/")

        # print(request.form.to_dict())
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


