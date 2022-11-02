import time
import webbrowser
from flask import Flask
from flask_socketio import SocketIO, emit

from utils import SerialPort, get_serial_data

app = Flask(__name__)
socketio = SocketIO(app)
serial_port = SerialPort(115200).open()


@app.route('/')
def index():
    return "hello_world"


@socketio.event
def my_event(message):
    emit('my response', {'data': 'got it!'})


def loop():
    while True:
        try:
            data = get_serial_data(serial_port)
            print(data)
            time.sleep(0.1)
        except KeyboardInterrupt:
            break


if __name__ == '__main__':
    loop()
    
    # webbrowser.open("http://127.0.0.1:5000")
    # socketio.start_background_task(loop)
    # socketio.run(app, host="0.0.0.0", port=5000, debug=True)
