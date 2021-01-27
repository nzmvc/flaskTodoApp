from flask import Flask,render_template,redirect,url_for,request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////cocuklar  için programlama kodlama robotik/python/projeler/todo_nzm/todo.db'
db = SQLAlchemy(app)

@app.route("/")
def index():
    todos = Todo.query.all()                            # tüm verileri alıyoruz
    return render_template("index.html",todos=todos)    #index.html e gonderiyoruz

@app.route("/add",methods=["POST"])
def addTodo():
    title = request.form.get("title")                   # formdan gelen title verisi alınır
    newTodo = Todo(title=title,complete=False)          # Todo class ı kullanılır newTodo objesi oluşturulur  
    db.session.add(newTodo)                             # obje db ye eklenir
    db.session.commit()                                 # değişiklik commit edilir

    return redirect(url_for("index"))                   # işlem sonrası redirect eidlir.

@app.route("/complete/<string:id>")                     # link e parametre gonderebiliyoruz.
def complete(id):
    todo = Todo.query.filter(Todo.id == id).first()
    todo.complete = not todo.complete                   # update işlemi yapılıyor
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/delete/<string:id>")
def delete(id):
    todo = Todo.query.filter(Todo.id == id).first()
    db.session.delete(todo)                             # delete işlemi yapılıyor
    db.session.commit()
    return redirect(url_for("index"))

class Todo(db.Model):                                   #class oluşturuluyor.
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    complete = db.Column(db.Boolean)
    

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)