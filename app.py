from flask import Flask, request
from flask_restful import Resource, Api
from json import dumps
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask import Flask, render_template, request, session, redirect, json, jsonify
from flask_session import Session

app = Flask(__name__)
api = Api(app)

print("DATABASE_URL")
print(os.getenv("DATABASE_URL"))
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))


@api.resource('/foo')
class Foo(Resource):
    def get(self):

        colors = db.execute("SELECT * FROM colors").fetchall()

        ints = []
        for color in colors:
            ints.append({
                "id": color.id,
                "name": color.color_name})

        return jsonify(ints)

if __name__ == '__main__':
    app.run(debug = true)