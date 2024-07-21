from App import create_app
from App.route import app

app = create_app(app)

if __name__ == "__main__":
    app.run(debug=True)