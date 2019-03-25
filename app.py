import os
from flask import Flask, render_template, redirect, request, url_for, send_from_directory
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)
app.config["MONGO_DBNAME"] = 'recipe-book'
app.config["MONGO_URI"] = 'mongodb+srv://root:r00tUser@myfirstcluster-8j8nw.mongodb.net/recipe-book?retryWrites=true'

mongo = PyMongo(app)


@app.route('/')
@app.route('/get_recipes')
def get_recipes():
    return render_template("recipes.html",
           recipes = mongo.db.recipes.find())


@app.route('/view_recipe/<recipe_id>')
def view_recipe(recipe_id):
    the_recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    return render_template('viewrecipe.html', recipe=the_recipe)


@app.route('/add_recipe')
def add_recipe():
    return render_template("addrecipe.html")


@app.route('/insert_recipe', methods=["POST"])
def insert_recipe():
    form_data = request.form.to_dict().items()
    new_recipe = {key: value for (key, value) in form_data if 'ingredients' not in key and 'method' not in key}
    new_recipe['ingredients'] = [value for (key, value) in form_data if 'ingredients' in key]
    new_recipe['method'] = [value for (key, value) in form_data if 'method' in key]
    print(new_recipe)
    # mongo.db.recipes.insert_one(new_recipe)
    return redirect(url_for('get_recipes'))


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
