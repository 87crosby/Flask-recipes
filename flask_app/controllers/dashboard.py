import re

from flask.helpers import flash
from flask_app import app
from flask import render_template, redirect, session, request
from flask_bcrypt import Bcrypt
from flask_app.models.users import User
from flask_app.models.recipes import Recipe

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')

    recipes = Recipe.get_all_recipes()

    return render_template('dashboard.html', recipes = recipes)

@app.route('/recipes/new')
def new_recipe():
    if 'user_id' not in session:
        return redirect('/')

    return render_template('new_recipe.html')

@app.route('/recipes/create', methods = ['POST'])
def add_recipe():
    if Recipe.validate_recipe(request.form):
        data = {
            'name' : request.form['name'],
            'description' : request.form['description'],
            'instructions' : request.form['instructions'],
            'date_made' : request.form['date_made'],
            'under_30' : request.form['under_30'],
            'users_id' : session['user_id']
        }
        Recipe.create_recipe(data)
        return redirect('/dashboard')
    return redirect('/recipes/new')

@app.route('/recipes/<int:recipe_id>')
def view_recipe(recipe_id):
    data = {'id': recipe_id}
    recipe_info = Recipe.get_recipes_by_id(data)
    
    return render_template('recipe_info.html', recipe_info = recipe_info)

@app.route('/recipes/edit/<int:recipe_id>')
def edit_recipe(recipe_id):
    data = {'id': recipe_id}
    recipe_info = Recipe.get_recipes_by_id(data)
    if session['user_id'] != recipe_info['users_id']:
        return redirect('/dashboard')
    
    return render_template('recipe_edit.html', recipe_info = recipe_info)

@app.route('/recipes/update/<int:recipe_id>', methods = ['POST'])
def update_recipe(recipe_id):
    if Recipe.validate_recipe(request.form):
        data = {
            'id' : recipe_id,
            'name' : request.form['name'],
            'description' : request.form['description'],
            'instructions' : request.form['instructions'],
            'date_made' : request.form['date_made'],
            'under_30' : request.form['under_30'],
            'users_id' : session['user_id']
        }
        Recipe.update_recipe(data)
        return redirect('/dashboard')
    return redirect(f'/recipes/edit/{recipe_id}')

@app.route('/recipe/delete/<int:recipe_id>')
def delete_recipe(recipe_id):
    data = {'id': recipe_id}
    recipe_info = Recipe.get_recipes_by_id(data)
    if session['user_id'] != recipe_info['users_id']:
        return redirect('/dashboard')
    Recipe.delete_recipe(data)
    return redirect('/dashboard')
