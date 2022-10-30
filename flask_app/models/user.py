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

    # @classmethod
    # def buy_car(cls,data):
    #     query = "INSERT INTO purchases (user_id, car_id,created_at,updated_at) VALUES (%(user_id)s,%(car_id)s,NOW(),NOW());"
    #     return connectToMySQL('cars_db').query_db(query,data)

    # @classmethod
    # def get_purchases(cls,data):
    #     query =  "SELECT * FROM users JOIN purchases ON users.id = purchases.user_id JOIN cars ON cars.id = purchases.car_id WHERE users.id = %(id)s;"
    #     results = connectToMySQL('cars_db').query_db(query,data)
    #     try:
    #         if cls(results[0]):
    #             cars_purchased = cls(results[0])

    #             for row in results:
    #                 if row['cars.id'] == None:
    #                     break
    #                 data = {
    #                     "id": row['cars.id'],
    #                     "price": row['price'],
    #                     "model": row['model'],
    #                     "make": row['make'],
    #                     "year": row['year'],
    #                     "description": row['description'],
    #                     "seller_name": row['seller_name'],
    #                     "seller_id": row['seller_id'],
    #                     "sold": row['sold'],
    #                     "created_at": row['cars.updated_at'],
    #                     "updated_at": row['cars.updated_at']
    #                 }
    #                 cars_purchased.purchased_cars.append(car.Car(data))
    #             return cars_purchased
    #     except IndexError:
    #         pass