from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import app
from flask_app.models.users import User

class Recipe():
    
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.under_30 = data['under_30']
        self.instructions = data['instructions']
        self.date_made = data['date_made']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.users_id = data['users_id']
        self.user = None

    @classmethod
    def get_all_recipes(cls):
        query = "SELECT * FROM recipes"

        result = connectToMySQL('recipe_schema').query_db(query)

        return result


    @classmethod
    def create_recipe(cls,data):
        query = "INSERT INTO recipes(name, description, instructions, under_30, date_made, users_id) VALUES (%(name)s, %(description)s, %(instructions)s, %(under_30)s, %(date_made)s, %(users_id)s);"

        result = connectToMySQL('recipe_schema').query_db(query, data)

        return result

    
    @classmethod
    def update_recipe(cls,data):
        query = 'UPDATE recipes SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, date_made = %(date_made)s, under_30 = %(under_30)s WHERE id = %(id)s;'

        connectToMySQL('recipe_schema').query_db(query, data)


    @classmethod
    def delete_recipe(cls,data):
        query = 'DELETE FROM recipes WHERE id = %(id)s;'

        connectToMySQL('recipe_schema').query_db(query, data)

    
    @classmethod
    def get_recipes_by_id(cls,data):
        query = "SELECT * FROM recipes WHERE recipes.id = %(id)s"

        result = connectToMySQL('recipe_schema').query_db(query, data)
        #print(result[0])

        return result[0]


    @staticmethod
    def validate_recipe(data):
        is_valid = True

        if len(data['name']) < 3 or len(data['name']) > 100:
            flash("Recipe name should be 1 to 100 characters.")
            is_valid = False

        if len(data['description']) < 3:
            flash("Recipe description should be atleast 3")
            is_valid = False

        if len(data['instructions']) < 3:
            flash("Recipe instructions should be atleast 3")
            is_valid = False

        if len(data['date_made']) == 0:
            flash("Please provide a date.")
            is_valid = False

        if len(data['under_30']) == 0:
            flash("Please click a button")
            is_valid = False

        return is_valid

