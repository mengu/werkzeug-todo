# -*- coding: utf-8 -*-
from werkzeug import Response, redirect, secure_filename
from utils import render_response
from models import User, ToDo, File, session, engine
import hashlib
from datetime import datetime

def index(request):
    if "user" in request.session:
        user = session.query(User).filter_by(userid=request.session["user"]).first()
    else:
        user = None
    return render_response("index.html", user=user)

def new_todo(request):
    if request.method == 'POST':
        if request.form['title'] and request.form['text']:
            new_todo = ToDo(title=request.form['title'],
                        text=request.form['text'],
                        user=request.session["user"])
            session.add(new_todo)
            session.commit()
            if new_todo:
                sent_file = request.files['userfile']
                if sent_file:
                    todo_file = File(todo=new_todo.id, filename=secure_filename(sent_file.filename), filecontent=sent_file.read())
                    session.add(todo_file)
                    session.commit()
                return redirect("/todo/%s" % new_todo.id)
        else:
            return render_response("new_todo.html", user=request.session["user"], error="Please enter a title and note for your to do.")
    else:
        return render_response("new_todo.html", user=request.session["user"])

def view_todo(request, todoid):
    todo = session.query(ToDo).filter_by(id=todoid).first()
    return render_response("view_todo.html", todo=todo, user=request.session["user"])

def edit_todo(request, todoid):
    todo = session.query(ToDo).filter_by(id=todoid).first()
    if request.method == 'POST':
        if request.form['title'] and request.form['text']:
            todo.title = request.form['title']
            todo.text = request.form['text']
            new_file = request.files['userfile']
            if new_file:
                existing_file = session.query(File).filter_by(todo_id=todo.id).one()
                existing_file.filename = secure_filename(new_file.filename)
                existing_file.filecontent = new_file.read()
            session.commit()
            return redirect("/todo/%s" % todo.id)
        else:
            return render_response("edit_todo.html", todo=todo, user=request.session["user"], error="Please enter a title and note for your to do.")
    else:
        return render_response("edit_todo.html", todo=todo, user=request.session["user"])

def delete_todo(request, todoid):
    todo = session.query(ToDo).filter_by(todoid=todoid).first()
    if session.delete(todo):
        session.commit()
        return redirect("/")

def view_file(request, todoid):
    todo_file = session.query(File).filter_by(todo_id=todoid).one()
    response = Response(todo_file.filecontent)
    response.headers['Content-Type'] = 'text/plain'
    return response

def signup(request):
    if request.method == 'POST':
        if request.form['email'] and request.form['password']:
            user = session.query(User).filter_by(email=request.form['email']).first()
            if not user:
                password = hashlib.md5()
                password.update(request.form['password'])
                new_user = User(email=request.form['email'], password=password.hexdigest())
                session.add(new_user)
                session.commit()
                return redirect("/")
            else:
                return render_response("signup.html", error="User already exists.")
        else:
            return render_response("signup.html", error="Please enter an e-mail address and password.")
    else:
        return render_response("signup.html")

def signin(request):
    if request.method == 'POST':
        error = None
        if not request.form['email'] or not request.form['password']:
            error = "Please enter your e-mail and password"
        email = request.form['email']
        password = hashlib.md5()
        password.update(request.form['password'])
        password = password.hexdigest()
        user = session.query(User).filter_by(email=email).first()
        if not user:
            error = "You have entered an invalid email."
        else:
            if user.password != password:
                error = 'You have entered an invalid password. \
                Did you <a href="/newpassword">forget your password?</a>'
        if not error:
            request.session["user"] = user.userid
            return redirect("/")
        else:
            return render_response("signin.html", error=error)
    else:
        return render_response("signin.html")

def signout(request):
    request.session.pop("user")
    return redirect("/")

