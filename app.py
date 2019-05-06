import os

import math
from flask import Flask, render_template, redirect, request, url_for, session, flash, Response
from flask_pymongo import PyMongo, DESCENDING, ASCENDING
from bson.objectid import ObjectId
import json
import bcrypt

app = Flask(__name__)
app.config["MONGO_DBNAME"] = 'recipe-book'
app.config["MONGO_URI"] = 'mongodb+srv://root:r00tUser@myfirstcluster-8j8nw.mongodb.net/recipe-book?retryWrites=true'
app.secret_key = os.getenv("SECRET", "randomsecretstringsosecure123")

mongo = PyMongo(app)

RECIPES_PER_PAGE = 12


def create_recipe_from_form(form):
    items = form.to_dict().items()
    recipe = {key: value for (key, value) in items}
    recipe['ingredients'] = [value for (key, value) in items if 'ingredients' in key]
    recipe['method'] = [value for (key, value) in items if 'method' in key]
    recipe['tag_name'] = [item['tag'] for item in json.loads(form['tag_name'])]
    recipe['likes'] = []
    recipe['meal_type'] = form.getlist('meal-type')
    if not recipe['photo_src']:
        recipe['photo_src'] = 'https://countrylakesdental.com/wp-content/uploads/2016/10/orionthemes-placeholder-image.jpg'
    return recipe


def create_cuisine_if_not_already():
    cuisine = mongo.db.cuisine
    existing_cuisine = cuisine.find_one({'cuisine_name': request.form['cuisine_name']})

    if existing_cuisine is None:
        cuisine.insert_one({'cuisine_name': request.form['cuisine_name']})


def create_tag_if_not_already():
    tags = mongo.db.tags

    # new_tags = []
    # for tag_dict in json.loads(request.form['tag_name']):
    #     tag = {'tag_name': tag_dict['tag']}
    #     if not tags.find_one(tag):
    #         new_tags.append(tag)
    # tags.insert_many(new_tags)

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
    recipes = mongo.db.recipes.find(mongo_filter)
    total_recipes = recipes.count()
    return list(recipes
                .skip((int(page) - 1) * RECIPES_PER_PAGE)
                .limit(RECIPES_PER_PAGE)), \
            math.ceil(total_recipes / RECIPES_PER_PAGE), \
            total_recipes


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

    page = request.args.get('page') or 1
    sort_by = request.args.get('sort') or "_id"
    recipes = mongo.db.recipes.aggregate([
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

    total_recipes = mongo.db.recipes.count(recipe_filter)
    num_pages = math.ceil(total_recipes / RECIPES_PER_PAGE)

    return render_template("recipes.html",
                           recipes=list(recipes),
                           cuisines=mongo.db.cuisine.find(),
                           users=mongo.db.users.find(),
                           tags=mongo.db.tags.find(),
                           num_pages=num_pages,
                           total=total_recipes)


@app.route('/top_recipes')
def top_recipes():
    recipes = mongo.db.recipes.find({'likes': {'$ne': []}}).sort('likes', DESCENDING).limit(10)
    return render_template("toprecipes.html", recipes=list(recipes))


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


@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been successfully signed out')
    return redirect(url_for('get_recipes'))


@app.route('/get_recipes/user/<user_name>')
def user_recipes(user_name):
    recipes, pages, total = find_list_of_recipes({"user_name": user_name}, request.args.get('page'))
    return render_template("recipes.html", recipes=recipes, num_pages=pages, total=total)


@app.route('/get_recipes/cuisine/<cuisine_name>')
def cuisine_recipes(cuisine_name):
    recipes, pages, total = find_list_of_recipes({"cuisine_name": cuisine_name}, request.args.get('page'))
    return render_template("recipes.html", recipes=recipes, num_pages=pages, total=total)


@app.route('/get_recipes/tag/<tag_name>')
def tag_recipes(tag_name):
    recipes, pages, total = find_list_of_recipes({"tag_name": tag_name}, request.args.get('page'))
    return render_template("recipes.html", recipes=recipes, num_pages=pages, total=total)


@app.route('/view_recipe/<recipe_id>')
def view_recipe(recipe_id):
    recipe_object_id = ObjectId(recipe_id)
    the_recipe = mongo.db.recipes.find_one({"_id": recipe_object_id})
    user = mongo.db.users.find_one({"user_name": session['username']}) if 'username' in session else None
    return render_template('viewrecipe.html',
                           recipe=the_recipe,
                           is_favourite=recipe_object_id in user['favourites'] if user else False,
                           is_liked=session['username'] in the_recipe['likes'] if user else False,
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


@app.route('/meal_type')
def meal_type():
    breakfast = mongo.db.recipes.find({"meal_type": "Breakfast"})
    lunch = mongo.db.recipes.find({"meal_type": "Lunch"})
    dinner = mongo.db.recipes.find({"meal_type": "Dinner"})
    other = mongo.db.recipes.find({"meal_type": "Other"})
    return render_template('mealview.html',
                           breakfast=breakfast,
                           lunch=lunch,
                           dinner=dinner,
                           other=other)


@app.route('/add_recipe')
def add_recipe():
    return render_template("addrecipe.html", cuisines=mongo.db.cuisine.find(), tags=mongo.db.tags.find())


@app.route('/insert_recipe', methods=["POST"])
def insert_recipe():
    new_recipe = create_recipe_from_form(request.form)
    mongo.db.recipes.insert_one(new_recipe)
    create_cuisine_if_not_already()
    create_tag_if_not_already()
    return redirect(url_for('get_recipes'))


@app.route('/edit_recipe/<recipe_id>')
def edit_recipe(recipe_id):
    the_recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    return render_template('editrecipe.html', recipe=the_recipe, tags=mongo.db.tags.find())


@app.route('/update_recipe/<recipe_id>', methods=["POST"])
def update_recipe(recipe_id):
    recipes = mongo.db.recipes
    result = recipes.update({'_id': ObjectId(recipe_id), "user_name": session['username']},
                            create_recipe_from_form(request.form))
    return redirect(url_for('get_recipes'), code=302 if result['n'] else 403)


@app.route('/delete_recipe/<recipe_id>', methods=['POST'])
def delete_recipe(recipe_id):
    result = mongo.db.recipes.remove({'_id': ObjectId(recipe_id), "user_name": session['username']})
    return Response(status=204 if result['n'] else 403)


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
