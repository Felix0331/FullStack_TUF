from flask import render_template,request,redirect,session,flash
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

from flask_app.models.user import User
from flask_app.models.post import Post
from flask_app.models.comment import Comment

@app.route('/')
def login_reg_page():
    return render_template('index.html')

@app.route('/home')
def dashboard():
    if not session:
        flash("Please login")
        return redirect('/')
    posts_w_votes = Post.get_posts_w_votes()

    return render_template('home.html', posts = posts_w_votes)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/register/user', methods=['POST'])
def register():
    if not User.validate_user(request.form):
        return redirect('/')
    # create the hash
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "alias": request.form['alias'],
        "email": request.form['email'],
        "password" : pw_hash
    }

    user_id = User.add_user(data)
    # store user id into session
    session['user_id'] = user_id
    session['first_name'] = request.form['first_name']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    session['name'] = f'{first_name} {last_name}'
    return redirect("/home")

@app.route('/login', methods=['POST'])
def login():

    data = { "email" : request.form["email"] }
    user_in_db = User.get_by_email(data)

    if not user_in_db:
        flash("Invalid Email/Password")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid Email/Password")
        return redirect('/')

    session['user_id'] = user_in_db.id
    session['first_name'] = user_in_db.first_name
    first_name = user_in_db.first_name
    last_name = user_in_db.last_name
    session["name"] = f'{first_name} {last_name}'

    return redirect("/home")

@app.route('/user/<int:user_id>')
def render_user_page(user_id):
    data={'id':user_id}
    data1={'users_id':user_id}
    user_info = User.get_user(data)
    user_posts = Post.get_user_posts(data1)
    user_comments = Comment.get_user_comments(data1)
    print(user_comments)
    return render_template('userView.html',user_info = user_info[0],user_posts = user_posts,user_comments = user_comments)

