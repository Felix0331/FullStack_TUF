from flask import render_template,request,redirect,session,flash,jsonify
from flask_app import app
from flask_bcrypt import Bcrypt
from flask_awscognito import AWSCognitoAuthentication
bcrypt = Bcrypt(app)
import boto3

from flask_app.models.user import User
from flask_app.models.post import Post
from flask_app.models.comment import Comment

app.config['AWS_DEFAULT_REGION'] = 'us-east-1'
app.config['AWS_COGNITO_DOMAIN'] = 'https://tuf-test.auth.us-east-1.amazoncognito.com'
app.config['AWS_COGNITO_USER_POOL_ID'] = 'us-east-1_vVRI7gUx8   '
app.config['AWS_COGNITO_USER_POOL_CLIENT_ID'] = '2s3pq2ob048l3tagp8ev69a5hq'
app.config['AWS_COGNITO_USER_POOL_CLIENT_SECRET'] = '1qe7huems4q1b95iuldi8ks6s0tnkoo6sbjuc8363pcumbpj6rp'
app.config['AWS_COGNITO_REDIRECT_URL'] = 'http://localhost:5000/home_page'

aws_auth = AWSCognitoAuthentication(app)

@app.route('/')
def login_reg_page():
    return redirect(aws_auth.get_sign_in_url())

@app.route('/home_page')
def aws_cognito_redirect():
    access_token = aws_auth.get_access_token(request.args)
    client = boto3.client('cognito-idp', region_name = 'us-east-1')
    response = client.get_user(AccessToken = access_token)

    sub = response['Username']
    first_name = response['UserAttributes'][2]['Value']
    last_name = response['UserAttributes'][3]['Value']
    user_email = response['UserAttributes'][4]['Value']
    alias = user_email.split('@')[0]


    data = {
        "sub":sub,
        "first_name": first_name,
        "last_name": last_name,
        "alias": alias,
        "email": user_email,
        }

    if user_info :=User.get_by_email(data):
        session['user_id'] = user_info['id']
        session['first_name'] = user_info['first_name']
        first_name = user_info['first_name']
        last_name = user_info['last_name']
        session["name"] = f'{first_name} {last_name}'
    else:
        user_id = User.add_user(data)
        data={'id':user_id}
        user_info = User.get_user(data)
        print(user_info)
        session['user_id'] = user_info[0]['id']
        session['first_name'] = user_info[0]['first_name']
        first_name = user_info[0]['first_name']
        last_name = user_info[0]['last_name']
        session["name"] = f'{first_name} {last_name}'
    return redirect('/home')

@app.route('/home')
def render_home():
    if not session:
        flash("Please login")
        return redirect('/')
    posts_w_votes = Post.get_posts_w_votes()
    return render_template('home.html', posts = posts_w_votes)


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


@app.route('/user/<int:user_id>')
def render_user_page(user_id):
    data={'id':user_id}
    data1={'users_id':user_id}
    user_info = User.get_user(data)
    user_posts = Post.get_user_posts(data1)
    user_comments = Comment.get_user_comments(data1)
    print(user_comments)
    return render_template('userView.html',user_info = user_info[0],user_posts = user_posts,user_comments = user_comments)

