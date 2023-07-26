from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, Optional

class TodoForm(FlaskForm):
    todo = StringField("タスク追加", validators=[DataRequired(), Length(max=255)])
    shinnkoudo = SelectField("進行度", choices=[("未着手", "未着手"), ("進行中", "進行中"), ("完了", "完了"), ("遅れ", "遅れ")], validators=[Optional()])
    juuyoudo = SelectField("重要度", choices=[("高", "高"), ("中", "中"), ("低", "低")], validators=[Optional()])
    url = StringField("URL", validators=[Optional(), Length(max=255)])  # URL field
    submit = SubmitField("追加")
    custom_button = SubmitField("編集完了")
