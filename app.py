import os
from flask import Flask, render_template, redirect, request, url_for, session, flash, send_from_directory
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import json
import bcrypt

app = Flask(__name__)
app.config["MONGO_DBNAME"] = 'recipe-book'
app.config["MONGO_URI"] = 'mongodb+srv://root:r00tUser@myfirstcluster-8j8nw.mongodb.net/recipe-book?retryWrites=true'
app.secret_key = os.getenv("SECRET", "randomsecretstringsosecure123")

mongo = PyMongo(app)


def create_recipe_from_form(form):
    items = form.to_dict().items()
    recipe = {key: value for (key, value) in items if 'ingredients' not in key and 'method' not in key}
    recipe['ingredients'] = [value for (key, value) in items if 'ingredients' in key]
    recipe['method'] = [value for (key, value) in items if 'method' in key]
    recipe['tag_name'] = [item['tag'] for item in json.loads(form['tag_name'])]
    recipe['likes'] = []
    return recipe


def check_add_cuisine():
    cuisine = mongo.db.cuisine
    existing_cuisine = cuisine.find_one({'cuisine_name': request.form['cuisine_name']})

    if existing_cuisine is None:
        cuisine.insert_one({'cuisine_name': request.form['cuisine_name']})


@app.route('/')
@app.route('/get_recipes')
def get_recipes():
    recipe_filter = {}

    cuisine = request.args.get('cuisine_name')
    if cuisine:
        recipe_filter['cuisine_name'] = cuisine

    user = request.args.get('user_name')
    if user:
        recipe_filter['user_name'] = user

    tags = request.args.getlist('tag_name[]')
    if tags:
        recipe_filter['tag_name'] = {"$all": tags}
    return render_template("recipes.html",
                           recipes=mongo.db.recipes.find(recipe_filter),
                           cuisines=mongo.db.cuisine.find(),
                           users=mongo.db.users.find(),
                           tags=mongo.db.tags.find())


@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == 'POST':
        users = mongo.db.users
        login_user = users.find_one({'user_name': request.form['user']})

        if login_user:
            if bcrypt.hashpw(request.form['pass_word'].encode('utf-8'), login_user['password']) == login_user['password']:
                session['username'] = login_user['user_name']
                session['favourites'] = [str(objectId) for objectId in login_user['favourites']]
                return redirect(url_for('get_recipes'))

        flash("Sorry, this username & password combination is invalid. Please try again or register as a new user")

    return render_template('login.html')


@app.route('/register', methods=["POST", "GET"])
def register():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'user_name': request.form['user_name']})

        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
            users.insert({'user_name': request.form['user_name'], 'password': hashpass})
            session['username'] = request.form['user_name']
            session['favourites'] = []
            return redirect(url_for('get_recipes'))

        flash('That username is already in use. Please try another')

    return render_template('register.html')


@app.route('/get_recipes/user/<user_name>')
def user_recipes(user_name):
    return render_template("recipes.html", recipes=mongo.db.recipes.find({"user_name": user_name}))


@app.route('/get_recipes/cuisine/<cuisine_name>')
def cuisine_recipes(cuisine_name):
    return render_template("recipes.html", recipes=mongo.db.recipes.find({"cuisine_name": cuisine_name}))


@app.route('/get_recipes/tag/<tag_name>')
def tag_recipes(tag_name):
    return render_template("recipes.html", recipes=mongo.db.recipes.find({"tag_name": tag_name}))


@app.route('/view_recipe/<recipe_id>')
def view_recipe(recipe_id):
    recipe_object_id = ObjectId(recipe_id)
    the_recipe = mongo.db.recipes.find_one({"_id": recipe_object_id})
    user = mongo.db.users.find_one({"user_name": session['username']})
    return render_template('viewrecipe.html',
                           recipe=the_recipe,
                           is_favourite=recipe_object_id in user['favourites'],
                           is_liked=session['username'] in the_recipe['likes'],
                           likes_count=len(the_recipe['likes']))


@app.route('/set_recipe_favourited/<recipe_id>', methods=["POST"])
def set_recipe_favourited(recipe_id):
    fav_selector = {"favourites": ObjectId(recipe_id)}
    update_params = {'$push': fav_selector} if request.form['favourite'] == 'true' else {'$pull': fav_selector}
    mongo.db.users.update_one({"user_name": session['username']}, update_params)
    return app.response_class(status=200)


@app.route('/set_recipe_liked/<recipe_id>', methods=["POST"])
def set_recipe_liked(recipe_id):
    like_selector = {"likes": session['username']}
    update_params = {'$push': like_selector} if request.form['liked'] == 'true' else {'$pull': like_selector}
    mongo.db.recipes.update_one({"_id": ObjectId(recipe_id)}, update_params)
    return app.response_class(status=200)


@app.route('/user_account')
def user_account():
    recipes = mongo.db.recipes.find({"user_name": session['username']})
    user = mongo.db.users.find_one({"user_name": session['username']}, {"favourites": 1})
    favourites = mongo.db.recipes.find({"_id": {"$in": user['favourites']}})
    return render_template('account.html',
                           favourites=favourites,
                           recipes=recipes)


@app.route('/add_recipe')
def add_recipe():
    return render_template("addrecipe.html", cuisines=mongo.db.cuisine.find())


@app.route('/insert_recipe', methods=["POST"])
def insert_recipe():
    new_recipe = create_recipe_from_form(request.form)
    mongo.db.recipes.insert_one(new_recipe)
    check_add_cuisine()
    return redirect(url_for('get_recipes'))


@app.route('/edit_recipe/<recipe_id>')
def edit_recipe(recipe_id):
    the_recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    return render_template('editrecipe.html', recipe=the_recipe)


@app.route('/update_recipe/<recipe_id>', methods=["POST"])
def update_recipe(recipe_id):
    recipes = mongo.db.recipes
    recipes.update({'_id': ObjectId(recipe_id)},
                   create_recipe_from_form(request.form))
    return redirect(url_for('get_recipes'))


@app.route('/delete_recipe/<recipe_id>')
def delete_recipe(recipe_id):
    mongo.db.recipes.remove({'_id': ObjectId(recipe_id)})
    return redirect(url_for('get_recipes'))


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
