from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Comment:
    def __init__(self, data):
        self.comment_id = data['comment_id']
        self.comment_body = data['comment_body']
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
    def get_comment(cls,data):
        query = "SELECT * FROM comments WHERE comments.comment_id = %(comment_id)s;"
        return connectToMySQL('tuf_db').query_db(query,data)

    @classmethod
    def get_user_comments(cls,data):
        query = "SELECT * FROM posts LEFT JOIN comments ON posts.post_id = comments.posts_id WHERE comments.users_id =  %(users_id)s;"
        results = connectToMySQL('tuf_db').query_db(query,data)
        return results

    @classmethod
    def add_comment(cls,data):
        query = "INSERT INTO comments (comment_body, commenter_name, users_id, posts_id, created_at, updated_at) VALUES (%(comment_body)s,%(commenter_name)s,%(users_id)s,%(posts_id)s,NOW(),NOW());"
        return connectToMySQL('tuf_db').query_db(query,data)

    @classmethod
    def edit_comment(cls,data):
        query = "UPDATE comments SET comment_body = %(comment_body)s, updated_at = NOW() WHERE comments.comment_id = %(comment_id)s;"
        return connectToMySQL('tuf_db').query_db(query,data)
        
    @classmethod
    def delete_comment(cls,data):
        query = "DELETE FROM comments WHERE comments.comment_id = %(comment_id)s"
        return connectToMySQL('tuf_db').query_db(query,data)