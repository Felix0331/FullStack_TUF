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
        'commenter_name':session['name'],
        'users_id':session['user_id'],
        'posts_id': post_id,
    }
    Comment.add_comment(data)
    return redirect(f'/show/{post_id}')

@app.route('/edit_comment/<int:comment_id>')
def edit_comment(comment_id):
    if not session:
        flash("Please login")
        return redirect('/')
    data={
        'comment_id': comment_id
    }
    comment_data = Comment.get_comment(data)
    data_2 = {
        'post_id': comment_data[0]['posts_id']
    }
    post_to_edit = Post.get_post(data_2)
    return render_template('editComment.html',post = post_to_edit[0],comment = comment_data[0])

@app.route('/update_comment/<int:comment_id>', methods = ['POST'])
def update_comment(comment_id):
    if not Comment.validate_comment(request.form):
        return redirect(f'/edit_comment/{comment_id}')
    data={
        'comment_id':comment_id,
        'comment_body':request.form['comment_body'],
    }

    p_id = request.form['post_id']
    Comment.edit_comment(data)
    return redirect(f'/show/{p_id}')

@app.route('/delete_comment/<int:comment_id>/<int:post_id>')
def delete_comment(comment_id,post_id):
    if not session:
        flash("Please login")
        return redirect('/')
    data={
        'comment_id': comment_id
    }
    Comment.delete_comment(data)
    return redirect(f'/show/{post_id}')