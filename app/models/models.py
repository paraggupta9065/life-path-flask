from app import app
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
ma = Marshmallow(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'your_secret_key'


db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    
    
class Memory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    image_url = db.Column(db.String(500), nullable=True)  # Optional
    date = db.Column(db.String(20), nullable=False)  # Store in YYYY-MM-DD format

class MemorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Memory

memory_schema = MemorySchema()
memories_schema = MemorySchema(many=True)
    
    
class Reminder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    time = db.Column(db.String(10), nullable=False)  # Store in HH:MM format
    date = db.Column(db.String(20), nullable=True)  # Optional: YYYY-MM-DD
    repeat = db.Column(db.String(50), nullable=True)  # Options: daily, weekly, monthly
    status = db.Column(db.Boolean, default=False)  # True if completed

class ReminderSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Reminder

reminder_schema = ReminderSchema()
reminders_schema = ReminderSchema(many=True)


with app.app_context():
    db.create_all()
    
    