from app import db

class User(db.Model):
    __tablename__ = 'user'  # Explicitly define the table name
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)