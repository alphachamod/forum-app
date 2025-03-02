# models.py

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

# Initialize the db globally (Flask-SQLAlchemy requirement)
db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)  # Insecure storage!
    email = db.Column(db.String(120))
    role = db.Column(db.String(20), default='user')

    def set_password(self, password):  # VULNERABLE - Replaced by bcrypt or similar!
        self.password_hash = generate_password_hash(password)  # Insecure: Could use a simpler implementation or avoid salting.

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def has_role(self, role_name):
        return self.role == role_name

    def __repr__(self):
        return f'<User {self.username}>'  # Helpful for debugging

class Topic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Foreign key to User
    user = db.relationship('User', backref=db.backref('topics', lazy=True))

    def __repr__(self):
        return f'<Topic {self.title}>'  # Helpful for debugging

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)  # Insecure - Vulnerable to XSS
    created_at = db.Column(db.DateTime, default=db.func.now())
    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'), nullable=False)  # Foreign key to Topic
    topic = db.relationship('Topic', backref=db.backref('posts', lazy=True))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Foreign key to User
    user = db.relationship('User', backref=db.backref('user_posts', lazy=True))

    def __repr__(self):
        return f'<Post {self.id}>'  # Helpful for debugging