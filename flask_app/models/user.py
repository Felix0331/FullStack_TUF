from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re	# the regex module
from flask_bcrypt import Bcrypt
from flask_app import app      
bcrypt = Bcrypt(app) 


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
class User:
    def __init__( self , data ):
        self.id = data['id']
        self.sub = data['sub']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.alias = data['alias']
        self.email = data['email']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']




    @classmethod
    def add_user( cls , data ):
        query = "INSERT INTO users ( sub, first_name, last_name, alias, email, created_at , updated_at ) VALUES (%(sub)s,%(first_name)s,%(last_name)s,%(alias)s,%(email)s,NOW(),NOW());"
        return connectToMySQL('tuf_db').query_db(query,data)

    @classmethod
    def get_user(cls,data):
        query = "SELECT * FROM users WHERE users.id = %(id)s;"
        return connectToMySQL('tuf_db').query_db(query,data)

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL("tuf_db").query_db(query,data)
        # Didn't find a matching user
        if len(result) < 1:
            return False
        return result[0]
