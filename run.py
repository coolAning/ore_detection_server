from app.factory import create_app
from flask_socketio import SocketIO, emit,send

app = create_app(config_name="DEVELOPMENT")
socketio = SocketIO(app)
@socketio.on('message', namespace='/websocket')
def handle_message(message):
    print('Received message:', message)
    # send(message)
    emit('response', 'Message received: ' + message, namespace='/websocket')
if __name__ == "__main__":
    socketio.run(app)