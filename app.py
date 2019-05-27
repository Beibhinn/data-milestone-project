import os

import math
from flask import Flask, render_template, redirect, request, url_for, session, flash, Response
from flask_pymongo import PyMongo, DESCENDING, ASCENDING
from bson.objectid import ObjectId
import json
import bcrypt

app = Flask(__name__)
app.config["MONGO_DBNAME"] = os.environ.get('DB_NAME')
app.config["MONGO_URI"] = os.environ.get('MONGO_URI')
app.secret_key = os.environ.get('SECRET')

try:
    mongodb = PyMongo(app).db
except ValueError:
    """We don't provide a URI when running unit tests, so PyMongo will fail to initialize.
    This is okay because we replace it with a version for testing anyway. """
    print('PyMongo not initialized!')
    mongodb = None

RECIPES_PER_PAGE = 12


def create_recipe_from_form(form):
    items = form.to_dict().items()
    recipe = {key: value for (key, value) in items if 'ingredients' not in key and 'method' not in key}
    # The following create arrays to store the items
    recipe['ingredients'] = [value for (key, value) in items if 'ingredients' in key]
    recipe['method'] = [value for (key, value) in items if 'method' in key]
    recipe['tag_name'] = [item['tag'] for item in json.loads(form['tag_name'])]
    recipe['likes'] = []
    recipe['user_name'] = session['username']
    recipe['meal_type'] = form.getlist('meal-type')
    # If no URL for photo given, use the URL for this placeholder image
    if not recipe['photo_src']:
        recipe['photo_src'] = 'https://countrylakesdental.com/wp-content/uploads/2016/10/orionthemes-placeholder' \
                              '-image.jpg '
    return recipe


def create_cuisine_if_not_already():
    """We want to ensure all cuisines entered in the 'cuisine' field on a form are also entered into the cuisine
    collection. First we check if it already exists in the collection, as we don't want duplicates. If it is not
    found in the collection, it is added to it. """
    cuisine = mongodb.cuisine
    existing_cuisine = cuisine.find_one({'cuisine_name': request.form['cuisine_name']})

    if existing_cuisine is None:
        cuisine.insert_one({'cuisine_name': request.form['cuisine_name']})


def create_tag_if_not_already():
    """Ensure all tags entered in the 'tags' field on a form are also entered into the tags collection.
        First check if each tag already exists in the collection, to avoid duplicates.
        If the tag is not found in the collection, it is added to it."""
    tags = mongodb.tags
    recipe_tags = json.loads(request.form['tag_name'])
    if not recipe_tags:
        return

    new_tags = [{'tag_name': tag['tag']}
                for tag in recipe_tags
                if not tags.find_one({'tag_name': tag['tag']})]
    if new_tags:
        tags.insert_many(new_tags)


def find_list_of_recipes(mongo_filter, page):
    if not page:
        page = 1
    # Get one page of recipes matching the filter
    recipes = mongodb.recipes.find(mongo_filter)
    total_recipes = recipes.count()
    return list(recipes
                .skip((int(page) - 1) * RECIPES_PER_PAGE)
                .limit(RECIPES_PER_PAGE)), \
        math.ceil(total_recipes / RECIPES_PER_PAGE), \
        total_recipes


@app.route('/')
@app.route('/get_recipes')
def get_recipes():
    # Queries are used to filter the results
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

    page = request.args.get('page') or 1
    sort_by = request.args.get('sort') or "_id"

    # Aggregation had to be used for 'likes' as it is a list of names and we wanted to sort by length of the list
    recipes = mongodb.recipes.aggregate([
        {
            "$match": recipe_filter,
        },
        {
            "$addFields": {"like_count": {"$size": {"$ifNull": ["$likes", []]}}}
        },
        {
            "$sort": {sort_by: ASCENDING if request.args.get('order') == 'asc' else DESCENDING}
        },
        {
            "$skip": RECIPES_PER_PAGE * (int(page) - 1)
        },
        {
            "$limit": RECIPES_PER_PAGE
        }
    ])

    total_recipes = mongodb.recipes.count(recipe_filter)
    num_pages = math.ceil(total_recipes / RECIPES_PER_PAGE)

    return render_template("recipes.html",
                           recipes=list(recipes),
                           cuisines=mongodb.cuisine.find(),
                           users=mongodb.users.find(),
                           tags=mongodb.tags.find(),
                           num_pages=num_pages,
                           total=total_recipes)


@app.route('/top_recipes')
def top_recipes():
    """Displays up to 12 top recipes, only including recipes where the likes list for that recipe is not empty.
    Ie, for recipes that have 1+ likes"""
    recipes = mongodb.recipes.find({'likes': {'$ne': []}}).sort('likes', ASCENDING).limit(12)
    return render_template("toprecipes.html", recipes=list(recipes))


@app.route('/login', methods=["POST", "GET"])
def login():
    """Checks to see if the user name entered is already in the database.
    If it is, it checks if the password given matches the password in the database when hashed.
    If successful, redirect to homepage. If unsuccessful, show message to user and stay on login page."""
    if request.method == 'POST':
        users = mongodb.users
        login_user = users.find_one({'user_name': request.form['user']})

        if login_user and bcrypt.hashpw(request.form['pass_word'].encode('utf-8'), login_user['password']) == \
                login_user['password']:
            session['username'] = login_user['user_name']
            session['favourites'] = [str(objectId) for objectId in login_user['favourites']]
            return redirect(url_for('get_recipes'))

        flash("Sorry, this username & password combination is invalid. Please try again or register as a new user")

    return render_template('login.html')


@app.route('/register', methods=["POST", "GET"])
def register():
    """"Checks to see if the user name entered is already in the database.
    If it is, a message is shown to the user to inform them the username is already in use, and they stay on the page.
    If it is not already in the database, the password given is hashed, the new user is added to the database and they
    are redirected to the homepage."""
    if request.method == 'POST':
        users = mongodb.users
        existing_user = users.find_one({'user_name': request.form['user_name']})

        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
            users.insert({'user_name': request.form['user_name'], 'password': hashpass, 'favourites': []})
            session['username'] = request.form['user_name']
            session['favourites'] = []
            return redirect(url_for('get_recipes'))

        flash('That username is already in use. Please try another')

    return render_template('register.html')


@app.route('/logout')
def logout():
    # Session will no longer remember the username
    session.pop('username', None)
    flash('You have been successfully signed out')
    return redirect(url_for('get_recipes'))


@app.route('/get_recipes/user/<user_name>')
def user_recipes(user_name):
    # Returns only the recipes of the user selected
    recipes, pages, total = find_list_of_recipes({"user_name": user_name}, request.args.get('page'))
    return render_template("recipes.html", recipes=recipes, num_pages=pages, total=total)


@app.route('/get_recipes/cuisine/<cuisine_name>')
def cuisine_recipes(cuisine_name):
    # Returns only the recipes matching the cuisine type selected
    recipes, pages, total = find_list_of_recipes({"cuisine_name": cuisine_name}, request.args.get('page'))
    return render_template("recipes.html", recipes=recipes, num_pages=pages, total=total)


@app.route('/get_recipes/tag/<tag_name>')
def tag_recipes(tag_name):
    # Returns only the recipes matching the tag selected
    recipes, pages, total = find_list_of_recipes({"tag_name": tag_name}, request.args.get('page'))
    return render_template("recipes.html", recipes=recipes, num_pages=pages, total=total)


@app.route('/view_recipe/<recipe_id>')
def view_recipe(recipe_id):
    # Shows full recipe information for a selected recipe
    recipe_object_id = ObjectId(recipe_id)
    the_recipe = mongodb.recipes.find_one({"_id": recipe_object_id})
    user = mongodb.users.find_one({"user_name": session['username']}) if 'username' in session else None
    return render_template('viewrecipe.html',
                           recipe=the_recipe,
                           is_favourite=recipe_object_id in user['favourites'] if user else False,
                           is_liked=session['username'] in the_recipe['likes'] if user else False,
                           likes_count=len(the_recipe['likes']))


@app.route('/set_recipe_favourited/<recipe_id>', methods=["POST"])
def set_recipe_favourited(recipe_id):
    # Adds or removes the recipe ID to the user's list of favourited recipes
    fav_selector = {"favourites": ObjectId(recipe_id)}
    update_params = {'$push': fav_selector} if request.form['favourite'] == 'true' else {'$pull': fav_selector}
    mongodb.users.update_one({"user_name": session['username']}, update_params)
    return app.response_class(status=200)


@app.route('/set_recipe_liked/<recipe_id>', methods=["POST"])
def set_recipe_liked(recipe_id):
    # Adds or removes the username in session to the list of users who've liked a particular recipe
    like_selector = {"likes": session['username']}
    update_params = {'$push': like_selector} if request.form['liked'] == 'true' else {'$pull': like_selector}
    mongodb.recipes.update_one({"_id": ObjectId(recipe_id)}, update_params)
    return app.response_class(status=200)


@app.route('/user_account')
def user_account():
    # Allows the user in session to view the recipes they've uploaded themselves, and favourited recipes
    recipes = mongodb.recipes.find({"user_name": session['username']})
    user = mongodb.users.find_one({"user_name": session['username']}, {"favourites": 1})
    favourites = mongodb.recipes.find({"_id": {"$in": user['favourites']}})
    return render_template('account.html',
                           favourites=favourites,
                           recipes=recipes)


@app.route('/meal_type')
def meal_type():
    # Displays recipes segregated by meal type
    breakfast = mongodb.recipes.find({"meal_type": "Breakfast"})
    lunch = mongodb.recipes.find({"meal_type": "Lunch"})
    dinner = mongodb.recipes.find({"meal_type": "Dinner"})
    other = mongodb.recipes.find({"meal_type": "Other"})
    return render_template('mealview.html',
                           breakfast=breakfast,
                           lunch=lunch,
                           dinner=dinner,
                           other=other)


@app.route('/add_recipe')
def add_recipe():
    """User must be logged in to add a recipe.
    If user is not logged in, show a message and redirect to login page"""
    if 'username' in session:
        return render_template("addrecipe.html", cuisines=mongodb.cuisine.find(), tags=mongodb.tags.find())
    else:
        flash('Please sign in to add a new recipe')
        return render_template("login.html")


@app.route('/insert_recipe', methods=["POST"])
def insert_recipe():
    new_recipe = create_recipe_from_form(request.form)
    mongodb.recipes.insert_one(new_recipe)
    create_cuisine_if_not_already()
    create_tag_if_not_already()
    return redirect(url_for('get_recipes'))


@app.route('/edit_recipe/<recipe_id>')
def edit_recipe(recipe_id):
    the_recipe = mongodb.recipes.find_one({"_id": ObjectId(recipe_id)})
    return render_template('editrecipe.html', recipe=the_recipe, tags=mongodb.tags.find())


@app.route('/update_recipe/<recipe_id>', methods=["POST"])
def update_recipe(recipe_id):
    # User can only edit/ update their own recipes
    recipes = mongodb.recipes
    result = recipes.update({'_id': ObjectId(recipe_id), "user_name": session['username']},
                            create_recipe_from_form(request.form))
    create_cuisine_if_not_already()
    create_tag_if_not_already()
    return redirect(url_for('get_recipes'), code=302 if result['n'] else 403)


@app.route('/delete_recipe/<recipe_id>', methods=['POST'])
def delete_recipe(recipe_id):
    # USer can only delete their own recipes
    result = mongodb.recipes.remove({'_id': ObjectId(recipe_id), "user_name": session['username']})
    return Response(status=204 if result['n'] else 403)


if __name__ == '__main__':
    if not mongodb:
        print('Cannot run. PyMongo failed to initialize. Double check environment variables.')
        exit(1)

    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=False)
