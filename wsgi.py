from flask import Flask
from flask_login import LoginManager
from application.database.models import User
from application.bp.authentication import authentication

app = Flask(__name__)
app.secret_key = 'secret'  # Required for session and flashing

# Flask-Login setup
login_manager = LoginManager()
login_manager.login_view = 'authentication.login'
login_manager.init_app(app)

# Same dummy users used here too
users = {
    "1": User(id=1, username="admin", password="1234"),
    "2": User(id=2, username="test", password="pass")
}

@login_manager.user_loader
def load_user(user_id):
    return users.get(user_id)

# Register blueprint
app.register_blueprint(authentication)
