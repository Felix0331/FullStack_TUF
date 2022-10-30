from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re	# the regex module
from flask_bcrypt import Bcrypt
from flask_app import app      
bcrypt = Bcrypt(app) 
# from flask_app.models import car

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
class User:
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.alias = data['alias']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        # self.purchased_cars = []


    @staticmethod
    def validate_user(user):
        is_valid = True
        if len(user['first_name']) < 3:
            flash("First name must be at least 3 characters.")
            is_valid = False
        if len(user['last_name']) < 3:
            flash("Last name must be at least 3 characters.")
            is_valid = False
        if len(user['alias']) <= 1:
            flash("Alias must be longer than one character.")
            is_valid = False
        if len(user['email']) <= 0:
            flash("Please add email!")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']): 
            flash("Email is not valid!")
            is_valid = False
        if len(user['password']) < 8:
            flash("Please add password that is atleast 8 characters long!")
            is_valid = False
        if not user['password'] == user["confirm_password"]:
            flash("Make sure password and password confirmation match!")
            is_valid = False
        return is_valid

    @classmethod
    def add_user( cls , data ):
        query = "INSERT INTO users ( first_name, last_name, alias, email, password, created_at , updated_at ) VALUES (%(first_name)s,%(last_name)s,%(alias)s,%(email)s,%(password)s,NOW(),NOW());"
        return connectToMySQL('mydb').query_db(query,data)

    @classmethod
    def get_user(cls,data):
        query = "SELECT * FROM users WHERE users.id = %(id)s;"
        return connectToMySQL('mydb').query_db(query,data)

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL("mydb").query_db(query,data)
        # Didn't find a matching user
        if len(result) < 1:
            return False
        return cls(result[0])