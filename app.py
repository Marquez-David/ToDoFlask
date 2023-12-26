from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
db = SQLAlchemy(app)

class Todo(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(100), nullable=False)
  created = db.Column(db.DateTime, default=datetime.utcnow)

  def __repr__(self):
    ''' Return a string as a representation of object'''
    return '<Task %r>' % self.id

@app.route('/', methods=['POST', 'GET'])
def index():
  ''' Creates new tasks '''
  if request.method == 'POST':
    task_title = request.form['title']
    new_task = Todo(title=task_title)
    try:
      db.session.add(new_task)
      db.session.commit()
      return redirect('/')
    except:
      return 'There was an issue adding your task'
  else:
    tasks = Todo.query.order_by(Todo.created).all()
    return render_template('index.html', tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id):
  ''' Delete a single taks '''
  deleted_task = Todo.query.get_or_404(id)
  try:
    db.session.delete(deleted_task)
    db.session.commit()
    return redirect('/')
  except:
    return 'There was an issue deleting your task'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
  ''' Update a single task'''
  updated_task = Todo.query.get_or_404(id)
  if request.method == 'POST':
    updated_task.title = request.form['task_title']
    try:
      db.session.commit()
      return redirect('/')
    except:
      return 'There was an issue updating your task'
  return redirect('/')


if __name__ == "__main__":
  app.app_context().push()
  db.create_all()
  app.run(debug=True)