from flask import Blueprint, current_app
from flask_socketio import emit

blueprint = Blueprint('my_blueprint', __name__)

@blueprint.route('/websocket')
def handle_websocket():
    socketio = current_app.socketio
    socketio.send('WebSocket connected')
    return 'WebSocket connected'

@blueprint.route('/message', methods=['POST'])
def send_message():
    socketio = current_app.socketio
    message = 'Hello from server'
    socketio.emit('message', message, namespace='/websocket')
    return 'Message sent'

