from flask import render_template,request,redirect,session,flash
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask_app.models.user import User
from flask_app.models.post import Post

@app.route('/add_new_post')
def add_post():
    if not session:
        flash("Please login")
        return redirect('/')
    return render_template('newPost.html')

@app.route('/search')
def search_posts():
    if not session:
        flash("Please login")
        return redirect('/')
    posts = Post.get_all_posts()
    return render_template('search.html', posts=posts)


@app.route('/create_post', methods = ['POST'])
def create_new():
    if not Post.validate_post(request.form):
        return redirect('/add_post')
    # print("####################################")
    # print(request.form.getlist('tags'))
    data={
        'subject':request.form['subject'],
        'post_body':request.form['post_body'],
        'upvotes':1,
        'tags':1,
        'poster_name':session['name'],
        'users_id':session['user_id'],
    }
    print(data)
    post_id = Post.add_post(data)

    return redirect(f'/show/{post_id}')

@app.route('/show/<int:post_id>')
def show_post(post_id):
    if not session:
        flash("Please login")
        return redirect('/')
    data={
        'post_id': post_id
    }
    post = Post.get_post_with_comments(data)
    print("&&&&&&&&&&&&&*******************")
    print(post)
    return render_template('postView.html',post = post)

@app.route('/edit/<int:car_id>')
def render_edit(car_id):
    if not session:
        flash("Please login")
        return redirect('/')
    data={
        'id': car_id
    }
    car = Car.get_car(data)
    return render_template('edit_car.html',car = car)

@app.route('/update/<int:car_id>', methods = ['POST'])
def update_car(car_id):
    if not session:
        flash("Please login")
        return redirect('/')
    if not Car.validate_car(request.form):
        return redirect(f'/edit/{car_id}')
    data={
        'id':car_id,
        'price':request.form['price'],
        'model':request.form['model'],
        'make':request.form['make'],
        'year':request.form['year'],
        'description':request.form['description'],
    }
    Car.edit_car(data)
    return redirect('/dashboard')


@app.route('/delete/<int:car_id>')
def delete_car(car_id):
    if not session:
        flash("Please login")
        return redirect('/')
    data = {
        'id':car_id
    }
    Car.delete_car(data)
    return redirect('/dashboard')