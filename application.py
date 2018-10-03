import os
from models import * 

from flask import Flask, render_template, request, session
from flask.ext.session import Session
from flask_socketio import SocketIO, join_room, leave_room, emit

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

_ = Channel('la primera', 'fulano')
_ = Channel('la segunda', 'mengano')
_ = Channel('antena3', 'fulanita')
# Global Variables
users = []
#channels = [uno, dos, tres]
for channel in Channel.channels:
    for i in range(100):
        text = 'this is message nº' + str(i)
        msg = Message(text,'hackerman')
        channel.send_message(msg)

#TODO:
# - comprobar los objetos que se crean/pasan: users, channels, messages
# - preparar channel.html
# - preparar socket.io y channel.js
# - ¿que datos tengo que guardar y donde?
#   cliente: display_name, active_channel
# - Write some tests
# - Refine data models
# - Make more sense of Forms
# - Work on presentation



@app.route("/")
def index():
    """Asks the user for Sign In"""
    return render_template("index.html")
    

@app.route("/channel_list", methods=["GET", "POST"])
def channel_list():
    """Offers a list of existing channels to join,
    and the creation of a new channel to the signed user"""
    if request.method=="POST":  
        aux = request.form.get("display_name")
        channel_name = request.form.get("channel_name")
        if channel_name==None: # user came here from "Sign In" (index.html)
            if aux in users:
                pass # TODO: throw error
            users.append(aux)
            session["user"] = aux 
        else: # user came here from "create channel" (channel_list.html)    
            display_name = session["user"]
            _ = Channel(channel_name, display_name) 
    else: 
        session["channel_id"] = ''  
    display_name = session["user"]  
    channels = []
    for channel in Channel.channels:
        channels.append({'name': channel.name, 'id': channel.id})
    return render_template("channel_list.html", display_name=display_name, channels=channels)
    
@app.route("/channel/<int:channel_id>", methods=["GET", "POST"])
def show_channel(channel_id):
    """Offers information about the selected channel,
    the last messages (until 100 of them), 
    and new message creation to the signed user"""
    display_name = session["user"]
    channel = Channel.channels[channel_id] 
    session["channel_id"] = channel.id
    return render_template("channel.html", display_name=display_name, channel=channel)

@socketio.on('connect')
def connect_and_join():
    display_name = session["user"]
    channel = Channel.channels[session["channel_id"]]
    join_room(channel.name)
    text = display_name + ' have entered in this channel.'
    time = datetime.utcnow().timestamp()
    emit("publish message", {"author": 'server',"text": text, "time": time}, room=channel.name, broadcast=True)

@socketio.on("submit message")
def new_message(data):
    display_name = session["user"]
    channel = Channel.channels[session["channel_id"]]
    text = data["text"] 
    msg = Message(text, display_name)
    channel.send_message(msg)
    time = msg.timestamp
    emit("publish message", {"author": display_name, "text": text, "time": time}, room=channel.name, broadcast=True)
    
@socketio.on("disconnect")
def lost_user():
    display_name = session["user"]
    channel = Channel.channels[session["channel_id"]]
    text = 'We have lost a connected user'
    time = datetime.utcnow().timestamp() 
    emit("publish message", {"author": 'server',"text": text, "time": time}, room=channel.name, broadcast=True)
