from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)

@app.route('/')
def home():
    todo_list = Todo.query.all()
    return render_template("base.html", todo_list=todo_list)

@app.route('/add', methods=['POST'])
def add():
    title = request.form.get('title')
    print(title)
    new_todo = Todo(title=title, complete=False)
    db.session.add(new_todo)
    db.session.commit()

    return redirect(url_for('home'))

@app.route('/save/<int:todo_id>', methods=['POST'])
def save(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.title = request.form.get("newTitle")
    db.session.commit()

    return redirect(url_for('home'))

@app.route('/close')
def close():
    return redirect(url_for('home'))

@app.route('/complete/<int:todo_id>')
def complete(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()

    return redirect(url_for('home'))

@app.route('/delete/<int:todo_id>')
def delete(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()

    return redirect(url_for('home'))

with app.app_context():
        db.create_all()

if __name__ == "__main__":\
    app.run(debug=True, port=8080)