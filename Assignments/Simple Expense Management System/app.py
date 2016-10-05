import datetime, time
from flask import Flask, redirect, url_for, request, jsonify
from flask_sqlalchemy import SQLAlchemy

import sqlalchemy

def setConnection():
  try:
    engine = sqlalchemy.create_engine('mysql://root:my-secret-pw@172.17.0.2') # connect to server
    engine.execute("CREATE DATABASE IF NOT EXISTS expensesdb") #create db
  except:
    time.sleep(5)
    setConnection()

setConnection()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:my-secret-pw@172.17.0.2/expensesdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'True'


db = SQLAlchemy(app)

class expenses(db.Model):
   id = db.Column('expense_id', db.Integer, primary_key = True)
   name = db.Column(db.String(30))
   email = db.Column(db.String(30))
   category = db.Column(db.String(100)) 
   description = db.Column(db.String(200))
   link = db.Column(db.String(200))
   estimated_costs = db.Column(db.Integer) 
   submit_date = db.Column(db.Date)
   status = db.Column(db.String(20)) 
   decision_date = db.Column(db.Date)

   def __init__(self, name, email, category, description, link, estimated_costs, submit_date, status, decision_date):
     self.name = name
     self.email = email
     self.category = category
     self.description = description
     self.link = link
     self.estimated_costs = estimated_costs
     self.submit_date = submit_date
     self.status = status
     self.decision_date = decision_date

@app.route('/v1/expenses',methods = ['POST'])
def expenses_post():
  content = request.get_json(force=True)
  submit_date = datetime.datetime.strptime(content['submit_date'], "%m-%d-%Y")
  expense = expenses(content['name'], content['email'], content['category'], content['description'], content['link'], content['estimated_costs'], submit_date.strftime('%Y-%m-%d'), 'pending', datetime.date.today())
  db.session.add(expense)
  db.session.commit()
  content['id'] = expense.id
  content['status'] = expense.status
  content['decision_date'] = expense.decision_date.strftime('%m-%d-%Y')
  return jsonify(content), 201

@app.route('/v1/expenses/<int:expense_id>', methods = ['GET'])
def expenses_get(expense_id):
  expense = expenses.query.get(expense_id)
  if expense:
    content = {}
    content['id'] = str(expense.id)
    content['name'] = str(expense.name)
    content['email'] = str(expense.email)
    content['category'] = str(expense.category)
    content['description'] = str(expense.description)
    content['link'] = str(expense.link)
    content['estimated_costs'] = str(expense.estimated_costs)
    content['submit_date'] = str((expense.submit_date).strftime('%m-%d-%Y'))
    content['status'] = str(expense.status)
    content['decision_date'] = str(expense.decision_date.strftime('%m-%d-%Y'))
    return jsonify(content)
  else:
    return '',404
  

@app.route('/v1/expenses/<int:expense_id>', methods = ['PUT'])
def expenses_put(expense_id):
  expense = expenses.query.get(expense_id)
  if expense:
    content = request.get_json(force=True)
    for key in content:
      db.engine.execute("UPDATE expenses SET " + str(key) + " = " + str(content[key]) + " WHERE expense_id = " + str(expense_id))
    return '', 202
  else:
    return '', 404


@app.route('/v1/expenses/<int:expense_id>', methods = ['DELETE'])
def expenses_del(expense_id):
  expense = expenses.query.get(expense_id)
  if expense:
    db.session.delete(expense)
    db.session.commit()
    return '', 204
  else:
    return '', 404
  

if __name__ == '__main__':
  db.create_all()
  app.run(debug = True, host='0.0.0.0')
