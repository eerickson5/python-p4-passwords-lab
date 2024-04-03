#!/usr/bin/env python3

from flask import request, session, make_response
from flask_restful import Resource

from config import app, db, api
from models import User

class ClearSession(Resource):

    def delete(self):
    
        session['page_views'] = None
        session['user_id'] = None

        return {}, 204

class Signup(Resource):
    
    def post(self):
        user = User(
            username=request.json.get('username')
        )
        user.password_hash=request.json.get("password")
        db.session.add(user)
        db.session.commit()
        session["user.id"] = user.id
        return make_response(user.to_dict(), 201)

class CheckSession(Resource):
    def get(self):
        if session.get("user_id"):
            user = User.query.filter(User.id == session["user_id"]).first()
            return make_response(user.to_dict(), 200)
        else:
            return make_response({}, 204)


class Login(Resource):
    def post(self):
        pw = request.json.get("password")
        user = User.query.filter(User.username == request.json.get("username")).first()
        if user and user.authenticate(pw):
            session["user_id"] = user.id
            return make_response(user.to_dict(), 200)
        else:
            return make_response({}, 400)

class Logout(Resource):
    def delete(self):
        session["user_id"] = None
        return make_response({}, 200)

api.add_resource(ClearSession, '/clear', endpoint='clear')
api.add_resource(Signup, '/signup', endpoint='signup')
api.add_resource(CheckSession, '/check_session', endpoint='check_session')
api.add_resource(Login, "/login")
api.add_resource(Logout, "/logout")

if __name__ == '__main__':
    app.run(port=5555, debug=True)
