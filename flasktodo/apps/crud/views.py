from apps.app import db  # データベース
from apps.crud.forms import TodoForm  # タスク入力につかうフォーム
from apps.crud.models import Todo  # タスクのモデル
from datetime import datetime  # 日付と時刻を扱うためのdatetime
from flask import Blueprint, render_template, redirect, url_for, request  # Flask関連
# Blueprintを作成。のBlueprintはFlaskアプリケーションに機能を追加するためのもの
crud = Blueprint(
    "crud",
    __name__,
    template_folder="templates",  # テンプレートが格納
    static_folder="static",  # 静的ファイルが格納
)

# タスク投稿
@crud.route("/crud/todo/post")
def index():
    form = TodoForm()  # フォームを作成
    # フォームが正しいかチェック
    if form.validate_on_submit():
        # Todoモデルを作成してデータベースに追加
        todo = Todo(
            todo=form.todo.data,
        )
        db.session.add(todo)
        db.session.commit()  # データベースの変更を確定
        return redirect(url_for("crud.todo"))  # タスク一覧にリダイレクト
    get_task = Todo.query.all()  # すべてのタスクを取得

    return render_template("crud/index.html", form=form, get_task=get_task)  # フォームとタスクをテンプレートに渡す


@crud.route("/cal")  # カレンダーページへ
def cal():
    return render_template("crud/cal.html")


@crud.route("/set")  # 設定ページへ
def set():
    return render_template("crud/set.html")


# タスクを投稿するため。GETとPOSTを受け付け
@crud.route("/todo/post", methods=["GET", "POST"])
def todo_post():
    form = TodoForm()  # フォームを作成
    if form.validate_on_submit():  # フォームが正しいかチェック
        todo = Todo(
            todo=form.todo.data,
        )
        db.session.add(todo)  # タスクをデータベースに追加
        db.session.commit()  # データベースの変更を確定
        form.todo.data = ''  # タスク追加後に'todo'フィールドをクリア
    get_task = Todo.query.all()  # すべてのタスクを取得

    return render_template("crud/index.html", form=form, get_task=get_task)  # フォームとタスクをテンプレートに渡す


# タスクを編集するため。GETとPOSTを受け付け
@crud.route("/task/<int:task_id>/edit", methods=["GET", "POST"])
def edit_todo(task_id):
    form = TodoForm()  # フォームを作成
    todo = Todo.query.get(task_id)  # タスクIDによってデータベースからタスクを取得

    if form.validate_on_submit():  # フォームが正しいかチェック
        todo.todo = form.todo.data  # フォームから取得したデータでタスクを更新
        todo.url = form.url.data  # フォームから取得したデータでURLを更新
        db.session.commit()  # データベースの変更を確定
        return redirect(url_for("crud.index"))  # タスク一覧ページにリダイレクト

    form.todo.data = todo.todo  # フォームの初期値をタスクの内容に設定
    return render_template("crud/edit.html", form=form, task=todo)  # フォームとタスクをテンプレートに渡してレンダリング


# タスクを削除するためのエンドポイント。POSTメソッドのみ受け付けます。
@crud.route('/task/<int:task_id>/delete', methods=['POST'])
def delete_task(task_id):
    todo = Todo.query.get(task_id)  # タスクIDに基づいてデータベースからタスクを取得
    if todo:  # タスクが存在する場合
        db.session.delete(todo)  # タスクをデータベースから削除
        db.session.commit()  # データベースの変更を確定
    return redirect(url_for('crud.index'))  # タスク一覧ページにリダイレクト


# タスクのステータスを更新するためのエンドポイント。POSTメソッドのみ受け付けます。
@crud.route("/task/<int:task_id>/update_status", methods=['POST'])
def update_status(task_id):
    todo = Todo.query.get(task_id)  # タスクIDに基づいてデータベースからタスクを取得
    if todo and 'shinnkoudo' in request.form:  # タスクが存在し、進行度がフォームに含まれている場合
        todo.shinnkoudo = request.form['shinnkoudo']  # 進行度を更新
        db.session.commit()  # データベースの変更を確定
    return redirect(url_for('crud.index'))  # タスク一覧ページにリダイレクト


# タスクの優先度を更新するためのエンドポイント。POSTのみ受け付け
@crud.route("/task/<int:task_id>/update_priority", methods=['POST'])
def update_priority(task_id):
    todo = Todo.query.get(task_id)  # タスクIDに基づいてデータベースからタスクを取得
    if todo and 'juuyoudo' in request.form:  # タスクが存在し、優先度がフォームに含まれている場合
        todo.juuyoudo = request.form['juuyoudo']  # 優先度を更新
        db.session.commit()  # データベースの変更を確定
    return redirect(url_for('crud.index'))  # タスク一覧ページにリダイレクト


# タスクの期限を更新するためのエンドポイント。POSTメソッドのみ受け付けます。
@crud.route("/task/<int:task_id>/update_due_date", methods=['POST'])
def update_due_date(task_id):
    todo = Todo.query.get(task_id)  # タスクIDに基づいてデータベースからタスクを取得
    if todo and 'duedate' in request.form:  # タスクが存在し、期限がフォームに含まれている場合
        due_date_str = request.form['duedate']  # フォームデータから日付文字列を取得
        due_date = datetime.strptime(due_date_str, '%Y-%m-%d')  # 文字列を日付時刻オブジェクトに変換
        todo.due_date = due_date  # 期限を更新
        db.session.commit()  # データベースの変更を確定
    return redirect(url_for('crud.index'))  # タスク一覧ページにリダイレクト


# タスクの詳細を表示するためのエンドポイント。GETメソッドのみ受け付けます。
@crud.route("/task/<int:task_id>/detail", methods=["GET"])
def task_detail(task_id):
    todo = Todo.query.get(task_id)  # タスクIDに基づいてデータベースからタスクを取得
    if todo:  # タスクが存在する場合
        return render_template("crud/detail.html", task=todo)  # タスクをテンプレートに渡してレンダリング
    else:
        return "Task not found", 404  # タスクが存在しない場合はエラーメッセージと404ステータスを返す
