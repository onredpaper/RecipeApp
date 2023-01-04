from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Recipe
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        #note = request.form.get('note')
        recipe_name = request.form.get('name')
        servings = request.form.get('servings')
        category = request.form.get('category')
        ingredient = request.form.get('ingredient')
        step = request.form.get('step')
        note = request.form.get('note')

        if recipe_name:
            new_recipe = Recipe(name=recipe_name, user_id=current_user.id, servings=servings, category=category, ingredients=ingredient, instructions=step, notes=note)
            db.session.add(new_recipe)
            db.session.commit()
            flash('Recipe added!', category='success')

    return render_template("home.html", user=current_user)

@views.route('/main', methods=['GET', 'POST'])
@login_required
def main():
    return render_template("main.html", user=current_user, recipes=Recipe.query.all())

@views.route('/delete-recipe', methods=['POST'])
def delete_recipe():
    recipe = json.loads(request.data)
    recipeId = recipe['recipeId']
    recipe = Recipe.query.get(recipeId)
    if recipe:
        if recipe.user_id == current_user.id:
            db.session.delete(recipe)
            db.session.commit()
    return jsonify({})

@views.route('/recipe', methods=['GET', 'POST'])
def recipe():
    if request.method == 'POST':
        recipe_id = request.form.get('recipeId')
        recipe = Recipe.query.get(recipe_id)
        return render_template("recipe.html", user=current_user, recipe=recipe)
    else:
        flash('Unable to find recipe.', category='error')