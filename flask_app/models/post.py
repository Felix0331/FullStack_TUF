from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user


class Post:
    def __init__(self, data):
        self.post_id = data['post_id']
        self.subject = data['subject']
        self.post_body = data['post_body']
        self.upvotes = data['upvotes']
        self.tags = data['tags']
        self.poster_name = data['poster_name']
        self.users_id = data['users_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @staticmethod
    def validate_post(post):
        is_valid = True
        if len(post['subject']) == 0:
            flash("Must add a subject to your post.")
            is_valid = False
        if len(post['post_body']) <= 0 :
            flash("Must elaborate on the subject.")
            is_valid = False
        return is_valid

    @classmethod
    def add_post(cls,data):
        query = "INSERT INTO posts (subject, post_body, upvotes, tags, poster_name, users_id, created_at, updated_at) VALUES (%(subject)s,%(post_body)s,%(upvotes)s,%(tags)s,%(poster_name)s,%(users_id)s,NOW(),NOW());"
        return connectToMySQL('mydb').query_db(query,data)

    @classmethod
    def get_post(cls,data):
        query = "SELECT * FROM posts WHERE posts.post_id = %(id)s;"
        return connectToMySQL('mydb').query_db(query,data)

    @classmethod
    def get_all_posts(cls):
        query = "SELECT * FROM posts;"
        posts = []
        results = connectToMySQL('mydb').query_db(query)
        for post in results:
            posts.append(cls(post))
        return posts

    @classmethod
    def get_post_with_comments(cls,data):
        query = "SELECT * FROM posts LEFT JOIN comments ON posts.post_id = comments.post_id WHERE posts.post_id =  %(post_id)s;"
        results = connectToMySQL('mydb').query_db(query,data)
        return results
