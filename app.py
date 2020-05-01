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

@app.route('/lists')
@cross_origin()
def fooo():
    colors = db.execute("SELECT * FROM colors").fetchall()
    ints = []
    for color in colors:
        ints.append({
            "id": color.id,
            "name": color.color_name})

    return jsonify(ints)

if __name__ == '__main__':
    app.run(debug = true)