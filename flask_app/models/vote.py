from flask_app.config.mysqlconnection import connectToMySQL

class Vote:
    def __init__(self, data):
        self.vote_id = data['vote_id']
        self.users_id = data['users_id']
        self.posts_id = data['posts_id']

    @classmethod
    def add_vote(cls,data):
        query = "INSERT INTO votes (users_id, posts_id) VALUES (%(users_id)s,%(posts_id)s);"
        return connectToMySQL('tuf_db').query_db(query,data)

    @classmethod
    def get_votes(cls,data):
        query = "SELECT Count(votes.vote_id) FROM votes WHERE votes.posts_id = %(post_id)s;"
        return connectToMySQL('tuf_db').query_db(query,data)

    @classmethod
    def check_vote(cls,data):
        query = "SELECT vote_id FROM votes WHERE votes.posts_id = %(post_id)s AND votes.users_id = %(user_id)s;"
        return connectToMySQL('tuf_db').query_db(query,data)

    @classmethod
    def delete_vote(cls,data):
        query = "DELETE FROM votes WHERE votes.posts_id = %(posts_id)s AND votes.users_id = %(users_id)s;"
        return connectToMySQL('tuf_db').query_db(query,data)

    
