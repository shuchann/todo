from datetime import datetime
from apps.app import db
from werkzeug.security import generate_password_hash

class Todo(db.Model):
    # テーブル名
    __tablename__ = "todo"
    # カラムを定義する
    id = db.Column(db.Integer, primary_key=True)
    todo = db.Column(db.String(255), nullable=False)  # タスクの内容を保存するカラム
    shinnkoudo = db.Column(db.String(50))  # タスクの進行状況を保存するカラム
    juuyoudo = db.Column(db.String(50))  # タスクの重要度を保存するカラム
    url = db.Column(db.String(255))  # URLを保存するカラム
    due_date = db.Column(db.DateTime, nullable=True)  # タスクの期日を保存するカラム