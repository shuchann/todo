from pathlib import Path
from flask import Flask, redirect, render_template, url_for
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask import Flask

db = SQLAlchemy()
csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY="2AZSMss3p5QPbcY2hBsj",
        SQLALCHEMY_DATABASE_URI=
            f"sqlite:///{Path(__file__).parent.parent / 'local.sqlite'}",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SQLALCHEMY_ECHO=True,
        WTF_CSRF_SECRRET_KEY="AuwzyszU5sugKN7KZs6f",
    )
    
    db.init_app(app)
    Migrate(app, db)
    csrf.init_app(app)
    
    from apps.crud import views as crud_views
    app.register_blueprint(crud_views.crud, url_prefix="/crud")

    @app.route("/")
    def index():
        # 変更したとこ
        return redirect(url_for("crud.index"))
    
    @app.route("/cal")
    def cal():
        return render_template("crud/cal.html")
    
    @app.route("/set")
    def setting():
        return render_template("crud/set.html")
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run()