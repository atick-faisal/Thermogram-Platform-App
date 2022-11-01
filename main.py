import webbrowser
from flask import Flask
from flask_socketio import SocketIO, emit
    
app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return "hello_world"

@socketio.event
def my_event(message):
    emit('my response', {'data': 'got it!'})

if __name__ == '__main__':
    webbrowser.open("http://127.0.0.1:5000")
    socketio.run(app)