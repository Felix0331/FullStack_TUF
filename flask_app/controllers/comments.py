from flask import render_template,request,redirect,session,flash
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
# from flask_app.models.user import User
from flask_app.models.post import Post
from flask_app.models.comment import Comment

@app.route('/comment/<int:post_id>', methods = ['POST'])
def create_new_comment(post_id):
    if not Comment.validate_comment(request.form):
        return redirect(f'/show/{post_id}')
    
    data={
        'comment_body':request.form['comment_body'],
        'upvotes':1,
        'commenter_name':session['name'],
        'users_id':session['user_id'],
        'post_id': post_id,
    }
    print("&&&&&&&&&^^^^^^^^^^^^^^&&&&&&&&&&&&^^^^^^^^^")
    print(data)
    comment_id = Comment.add_comment(data)
    print(comment_id)

    return redirect(f'/show/{post_id}')