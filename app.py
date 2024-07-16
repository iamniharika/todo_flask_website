from flask import Flask , render_template , request , redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class TODO(db.Model):
    SNo = db.Column(db.Integer , primary_key = True)
    addtodo = db.Column(db.String(200) , nullable = False)

    def __repr__(self) -> str:
        return f"{self.SNo} - {self.addtodo}"


@app.route('/' , methods = ['GET' , 'POST'])
def hello_world():
    if request.method == 'POST':
        add = request.form['addtodo']
        todo = TODO(addtodo = add)
        db.session.add(todo)
        db.session.commit()
    alltodo = TODO.query.all()
    return render_template('index.html' , alltodo = alltodo)

@app.route('/update/<int:SNo>' , methods = ['GET' , 'POST'])
def update(SNo):
    if request.method == 'POST':
        add = request.form['addtodo']
        todo = TODO.query.filter_by(SNo = SNo).first()
        todo.addtodo = add
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
    
    todo = TODO.query.filter_by(SNo = SNo).first()
    return render_template('update.html' , todo = todo)

@app.route('/delete/<int:SNo>')
def delete(SNo):
    todo = TODO.query.filter_by(SNo = SNo).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True , port= 5500)
