from app import db

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)

class RigOperation(db.Model):
    __tablename__ = 'rig_operation'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    rig_name = db.Column(db.String(100), nullable=False, default="Unnamed Rig")
    progress = db.Column(db.Float, nullable=False, default=0.0)  
    status = db.Column(db.String(20), nullable=False, default="-")  
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)