import os
from flask import Flask
from config import Config
from models import db  # Import the db object
from views.auth import auth_bp  # Import auth blueprint
from views.forum import forum_bp  # Import forum blueprint
from views.user import user_bp

# Create app
app = Flask(__name__)
app.config.from_object(Config)

# Init Database to app
db.init_app(app)

# This creates the database tables
with app.app_context():
    db.create_all()

app.register_blueprint(auth_bp)  # Register auth blueprint
app.register_blueprint(forum_bp)  # Register forum blueprint
app.register_blueprint(user_bp)  # Register the blueprint


# Register Route for Forum

@app.route('/')
def home():
    return 'home'


if __name__ == '__main__':
    app.run(debug=True)
