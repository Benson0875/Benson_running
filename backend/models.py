from datetime import datetime
from backend.app import db

class User(db.Model):
    """用戶模型"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    preferences = db.relationship('UserPreference', backref='user', uselist=False)
    activities = db.relationship('Activity', backref='user', lazy=True)

class UserPreference(db.Model):
    """用戶偏好設定模型"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    theme = db.Column(db.String(20), default='light')
    language = db.Column(db.String(10), default='zh-TW')
    notifications_enabled = db.Column(db.Boolean, default=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Activity(db.Model):
    """活動模型"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    duration = db.Column(db.Integer)  # 以秒為單位
    distance = db.Column(db.Float)    # 以公尺為單位
    calories = db.Column(db.Integer)
    heart_rate_avg = db.Column(db.Integer)
    heart_rate_max = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    analysis = db.relationship('ActivityAnalysis', backref='activity', uselist=False)

class ActivityAnalysis(db.Model):
    """活動分析模型"""
    id = db.Column(db.Integer, primary_key=True)
    activity_id = db.Column(db.Integer, db.ForeignKey('activity.id'), nullable=False)
    formatted_analysis = db.Column(db.Text)
    suggestions = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow) 