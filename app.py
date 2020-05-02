from flask import Flask, request
from json import dumps
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask import Flask, render_template, request, session, redirect, json, jsonify
from flask_session import Session
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)

print("DATABASE_URL")
print(os.getenv("DATABASE_URL"))
engine = create_engine('postgres://awkfjeofiltqzf:71ea0e43dd739b4655198785ffd56a239dcebed19ed2e0dc885bb766f499d483@ec2-23-20-129-146.compute-1.amazonaws.com:5432/d3tr7dd4ghdpd9') 

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
@app.route("/")                                       
def helloWorld():
  return "Hello, cross-origin-world!"

@app.route('/colors')
@cross_origin()
def colors():
    colors = db.execute("SELECT * FROM colors").fetchall()
    ints = []
    for color in colors:
        ints.append({
            "id": color.id,
            "name": color.color_name})

    return jsonify(ints)

@app.route("/lists")
@cross_origin()
def lists():
    listsId = db.execute("SELECT * FROM lists JOIN colors ON colors.id=lists.color_id ORDER BY list_id ASC;").fetchall()
    tasks = db.execute("SELECT * FROM tasks ORDER BY id ASC;").fetchall()

    lis = []
    print(listsId[0].id)
    for l in listsId:
        tas = []
        for task in tasks:
            if (task.list_id==l.list_id):
                tas.append(
                    {
                        "id":task.id,
                        "listId":l.list_id,
                        "text":task.text, 
                        "completed":task.completed
                    }
                )
        lis.append({
            "id":l.list_id,
            "name":l.list_name,
            "colorId":l.color_id,
            "color":{
                "id":l.color_id,
                "name":l.color_name,
            },
            "tasks":tas

        })

    return jsonify(lis)
    
@app.route("/tasks-delete", methods=["POST", "GET"])
@cross_origin()
def tasksDelite():
    jsonData = request.get_json()
    db.execute("DELETE FROM tasks WHERE id=:id",
        {"id":jsonData["id"]})
    db.commit()
    return "1"

@app.route("/tasks-add", methods=["POST", "GET"])
@cross_origin()
def tasksAdd():
    jsonData = request.get_json()
    db.execute("INSERT INTO tasks (text, list_id) VALUES ( :text, :list_id)",
                { "text": jsonData["text"], "list_id": jsonData["listId"]}) 
    db.commit()
    return "1"

@app.route("/lists-add", methods=["POST", "GET"])
@cross_origin()
def listsAdd():
    jsonData = request.get_json()
    db.execute("INSERT INTO lists (list_name, color_id) VALUES ( :name, :color_id)",
                { "name": jsonData["name"], "color_id": jsonData["colorId"]}) 
    db.commit()
    id = db.execute("SELECT list_id FROM lists WHERE list_name = :name ORDER BY list_id DESC LIMIT 1;",
            { "name": jsonData["name"]}).fetchall()
    return jsonify({"id":id[0].list_id})


@app.route("/tasks-update", methods=["POST", "GET"])
@cross_origin()
def tasksUpdate():
    jsonData = request.get_json()
    db.execute(" UPDATE tasks SET text = :text WHERE id=:id",
        {"id":jsonData["id"], "text":jsonData["newText"]})
    db.commit()
    return "1"

@app.route("/title-update", methods=["POST", "GET"])
@cross_origin()
def titleUpdate():
    jsonData = request.get_json()
    db.execute(" UPDATE lists SET list_name = :newName WHERE list_id=:id",
        {"id":jsonData["id"], "newName":jsonData["newName"]})
    db.commit()
    return "1"

@app.route("/tasks-check", methods=["POST", "GET"])
@cross_origin()
def tasksCheck():
    jsonData = request.get_json()
    print(jsonData["completed"])
    db.execute("UPDATE tasks SET completed = :completed WHERE id=:id",
        {"id":jsonData["id"], "completed":jsonData["completed"]})
    db.commit()
    return "1"

@app.route("/lists-delete", methods=["POST", "GET"])
@cross_origin()
def listsDelite():
    jsonData = request.get_json()
    db.execute("DELETE FROM tasks WHERE list_id=:id",
        {"id":jsonData["id"]})
    db.execute("DELETE FROM lists WHERE list_id=:id",
        {"id":jsonData["id"]})
    db.commit()
    return "1"


if __name__ == '__main__':
    app.run(debug = true)