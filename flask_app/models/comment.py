from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import post


class Comment:
    def __init__(self, data):
        self.comment_id = data['comment_id']
        self.comment_body = data['comment_body']
        self.upvotes = data['upvotes']
        self.commenter_name = data['commenter_name']
        self.users_id = data['users_id']
        self.post_id = data['post_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @staticmethod
    def validate_comment(comment):
        is_valid = True
        if len(comment['comment_body']) <= 0 :
            flash("Please add comment.")
            is_valid = False
        return is_valid
    
    @classmethod
    def add_comment(cls,data):
        query = "INSERT INTO comments (comment_body, upvotes, commenter_name, users_id, post_id, created_at, updated_at) VALUES (%(comment_body)s,%(upvotes)s,%(commenter_name)s,%(users_id)s,%(post_id)s,NOW(),NOW());"
        return connectToMySQL('mydb').query_db(query,data)

    