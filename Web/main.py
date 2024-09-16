from App import create_app
from App.route import app,socketio
import os

app = create_app(app)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    use_socketio = os.environ.get('USE_SOCKETIO', 'True').lower() == 'true'
    
    if use_socketio:
        socketio.run(app, debug=True, host='0.0.0.0', port=port)
    else:
        app.run(debug=True, host='0.0.0.0', port=port)
