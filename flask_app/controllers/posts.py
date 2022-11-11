
from flask import render_template,request,redirect,session,flash
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

from flask_app.models.post import Post
from flask_app.models.vote import Vote 
from flask_app.models.tag import Tag, Tag_Map

@app.route('/add_new_post')
def add_post():
    if not session:
        flash("Please login")
        return redirect('/')
    tags = Tag.get_tags()
    return render_template('newPost.html',tags = tags)


@app.route('/lookup/')
def search_posts():
    if not session:
        flash("Please login")
        return redirect('/')
    posts = Post.get_all_posts()
    tags = Tag.get_tags()
    return render_template('search.html', posts=posts,tags = tags)

@app.route('/search_by/<int:tag_id>')
def search_posts_byTag(tag_id):
    print(tag_id)
    if not session:
        flash("Please login")
        return redirect('/')
    
    data={
            'tag_id':tag_id
        }
    posts = Tag.get_post_by_tag(data)
    tags = Tag.get_tags()
    return render_template('search.html', posts=posts,tags = tags)


@app.route('/create_post', methods = ['POST'])
def create_new():
    if not Post.validate_post(request.form):
        return redirect('/add_post')

    data={
        'subject':request.form['subject'],
        'post_body':request.form['post_body'],
        'poster_name':session['name'],
        'users_id':session['user_id'],
    }

    post_id = Post.add_post(data)
    data={
        'tag_list':request.form.getlist('tags'),
        'posts_id': post_id
    }
    Tag_Map.add_tags_to_post(data)
    return redirect(f'/show/{post_id}')


@app.route('/edit/<int:post_id>')
def edit_post(post_id):
    if not session:
        flash("Please login")
        return redirect('/')
    data={
        'post_id': post_id
    }
    # Both Tag functions work to get all tags and tags that only belong to post
    post_tag_list = Tag.get_post_tags(data)
    tags = Tag.get_tags()
    post_to_edit = Post.get_post(data)
    return render_template('editPost.html',post = post_to_edit[0],post_tag_list = post_tag_list, tags = tags)

@app.route('/edit_post/<int:post_id>', methods = ['POST'])
def update_post(post_id):
    if not Post.validate_post(request.form):
        return redirect('/add_post')
    data={
        'post_id':post_id,
        'subject':request.form['subject'],
        'post_body':request.form['post_body'],
        'tags':1,
    }
    data1={
        'post_id':post_id,
    }
    Tag_Map.delete_post_tags(data1)
    Post.edit_post(data)
    data={
        'tag_list':request.form.getlist('tags'),
        'posts_id': post_id
    }
    Tag_Map.add_tags_to_post(data)
    return redirect(f'/show/{post_id}')



@app.route('/show/<int:post_id>')
def show_post(post_id):
    if not session:
        flash("Please login")
        return redirect('/')
    data={
        'post_id': post_id
    }
    data2={
        'post_id': post_id,
        'user_id': session['user_id']
    }
    post = Post.get_post_with_comments(data)
    print(post)
    num_votes = Vote.get_votes(data)
    # This check_vote class function checks if the current session user has already liked the post
    # purpose is to only have one vote for one person.
    check_vote = Vote.check_vote(data2)
    post_tag_list = Tag.get_post_tags(data)
    print("888*********************")
    print(post_tag_list)
    return render_template('postView.html',post = post, votes = num_votes[0], check_vote = check_vote,tag_list = post_tag_list)

@app.route('/delete/<int:post_id>')
def delete_post(post_id):
    if not session:
        flash("Please login")
        return redirect('/')
    data={
        'post_id': post_id
    }
    Post.delete_post(data)
    return redirect('/home')

# ===================== Voting Logic ===============================

@app.route('/vote/<int:post_id>', methods=['POST'])
def vote_on_post(post_id):
    if not session:
        flash("Please login")
        return redirect('/')
    data={
        'users_id' : session['user_id'],
        'posts_id': post_id
    }
    Vote.add_vote(data)
    return redirect(f'/show/{post_id}')

@app.route('/delete_vote/<int:post_id>', methods=['POST'])
def delete_vote(post_id):
    if not session:
        flash("Please login")
        return redirect('/')
    data={
        'users_id' : session['user_id'],
        'posts_id': post_id
    }
    Vote.delete_vote(data)
    return redirect(f'/show/{post_id}')

