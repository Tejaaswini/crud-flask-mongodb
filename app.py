from flask import Flask, render_template, redirect
from pymongo import MongoClient
from curd import *

app = Flask(__name__)

app.config.update(dict(SECRET_KEY='yoursecretkey'))
client = MongoClient('localhost:27017')
db = client.TaskManager

if db.settings.find({'name': 'task_id'}).count() <= 0:
    print("task_id Not found, creating....")
    db.settings.insert_one({'name':'task_id', 'value':0})

def updateTaskID(value):
    task_id = db.settings.find_one()['value']
    task_id += value
    db.settings.update_one(
        {'name':'task_id'},
        {'$set':
            {'value':task_id}
        })

def createTask(form):
    title = form.title.data
    tododesc = form.tododesc.data
    task_id = db.settings.find_one()['value']
    
    task = {'id':task_id, 'title':title, 'tododesc':tododesc}

    db.tasks.insert_one(task)
    updateTaskID(1)
    return redirect('/')

def deleteTask(form):
    key = form.key.data
    title = form.title.data

    if(key):
        print(key, type(key))
        db.tasks.delete_many({'id':int(key)})
    else:
        db.tasks.delete_many({'title':title})

    return redirect('/')

def updateTask(form):
    key = form.key.data
    tododesc = form.tododesc.data
    
    db.tasks.update_one(
        {"id": int(key)},
        {"$set":
            {"tododesc": tododesc}
        }
    )

    return redirect('/')

def resetTask(form):
    db.tasks.drop()
    db.settings.drop()
    db.settings.insert_one({'name':'task_id', 'value':0})
    return redirect('/')

@app.route('/', methods=['GET','POST'])
def main():
    createform = CreateTask(prefix='createform')
    deleteform = DeleteTask(prefix='deleteform')
    updateform = UpdateTask(prefix='updateform')
    reset = ResetTask(prefix='reset')

    if createform.validate_on_submit() and createform.create.data:
        return createTask(createform)
    if deleteform.validate_on_submit() and deleteform.delete.data:
        return deleteTask(deleteform)
    if updateform.validate_on_submit() and updateform.update.data:
        return updateTask(updateform)
    if reset.validate_on_submit() and reset.reset.data:
        return resetTask(reset)

    docs = db.tasks.find()
    data = []
    for i in docs:
        data.append(i)

    return render_template('index.html', createform = createform, deleteform = deleteform, updateform = updateform, \
            data = data, reset = reset)

if __name__=='__main__':
    app.run(debug=True)
