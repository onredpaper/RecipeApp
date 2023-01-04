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
        recipe_id = request.form.get('recipeId')
        if recipe_id:
            # This is a load to edit, load the recipe to fill fields
            recipe = Recipe.query.get(recipe_id)
            flash('Recipe loaded to be editted', category='success')
            return render_template("home.html", user=current_user, edit_recipe=recipe)
        recipe_name = request.form.get('name')
        servings = request.form.get('servings')
        category = request.form.get('category')
        ingredient = request.form.get('ingredient')
        step = request.form.get('step')
        note = request.form.get('note')

        if recipe_name:
            recipe = Recipe.query.filter_by(name=recipe_name).first()
            if recipe:
                # This is an edit
                recipe.name = recipe_name
                recipe.servings = servings
                recipe.category = category
                recipe.ingredient = ingredient
                recipe.step = step
                recipe.note = note
                flash_text = 'Recipe updated!'
            else:
                new_recipe = Recipe(name=recipe_name, user_id=current_user.id, servings=servings, category=category, ingredients=ingredient, instructions=step, notes=note)
                db.session.add(new_recipe)
                flash_text = 'Recipe added!'
            
            db.session.commit()
            flash(flash_text, category='success')

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