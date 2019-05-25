import bcrypt
import pytest
from bson.objectid import ObjectId
import app


@pytest.fixture
def client():
    app.app.config['TESTING'] = True
    app.app.config['SECRET_KEY'] = 'sekrit!'
    # app.app.secret_key = 'Test'
    client = app.app.test_client()
    return client


def test_mongo_test_data_set_up_properly(mongodb):
    collections = mongodb.list_collection_names()
    assert 'recipes' in collections
    assert 'users' in collections


def test_new_recipe_submission_creates_new_db_entry(client, mongodb):
    app.mongodb = mongodb
    # Provide form with dummy information to be added as a recipe to database
    form = {
        '_id': '2c951aa01c9d230000c6c7b4',
        'title': 'Test',
        'cuisine_name': 'Example',
        'ingredients[0]': 'Milk',
        'ingredients[1]': 'Cheese',
        'ingredients[2]': 'Eggs',
        'method[0]': 'Whisk',
        'method[1]': 'Stir',
        'method[2]': 'Pour',
        'tag_name': '[{"tag":"Milky"},{"tag":"Cheesy"},{"tag":"Eggcellent"}]',
        'meal_type[0]': 'Breakfast',
        'photo_src': 'http://place/holder.png'
    }
    with client.session_transaction() as session:
        session['username'] = 'TestUser'
    result = client.post('/insert_recipe', data=form)
    # Expect status code 302 to indicate successfully redirected to home page
    assert result.status_code == 302
    assert "/get_recipes" in result.location
    # Verify form info has been added as a new recipe, and that new tags/ cuisines added to their respective databases
    assert mongodb.recipes.find_one({"title": "Test"})
    assert mongodb.tags.find_one({"tag_name": "Eggcellent"})
    assert mongodb.cuisine.find_one({"cuisine_name": "Example"})


def test_new_information_updates_to_recipe_record_in_db(client, mongodb):
    app.mongodb = mongodb
    form = {
        'title': 'EditedTest Recipe One',
        'cuisine_name': 'Update Test',
        'user_name': 'TestUser',
        'ingredients[0]': 'Ingredient Four',
        'ingredients[1]': 'Ingredient Five',
        'ingredients[2]': 'Ingredient Six',
        'method[0]': 'Step Four',
        'method[1]': 'Step Five',
        'method[2]': 'Step Six',
        'tag_name': '[{"tag":"Comfort-food"},{"tag":"Traditional"},{"tag":"Eggcellent"}]',
        'meal_type[0]': 'Breakfast',
        'photo_src': 'http://place/holder.png'
    }
    with client.session_transaction() as session:
        session['username'] = 'TestUser'
    result = client.post('/update_recipe/5c951aa01c9d440000c6c7a7', data=form)
    # Verify successful redirect
    assert result.status_code == 302
    assert "/get_recipes" in result.location
    recipe = mongodb.recipes.find_one({"_id": ObjectId("5c951aa01c9d440000c6c7a7")})
    # Verify changed info has been updated
    assert recipe['title'] == "EditedTest Recipe One"


def test_delete_recipe_record_from_db(client, mongodb):
    app.mongodb = mongodb
    with client.session_transaction() as session:
        session['username'] = 'TestUser'
    result = client.post('/delete_recipe/5c951aa01c9d440000c6c7a7')
    # Expect status code 204 to indicate request successfully fulfilled &  no content
    assert result.status_code == 204
    # Verify recipe is no longer in the database
    recipe = mongodb.recipes.find_one({"_id": ObjectId("5c951aa01c9d440000c6c7a7")})
    assert not recipe


def test_set_recipe_favourited_by_user_in_session(client, mongodb):
    app.mongodb = mongodb
    form = {
        'favourite': 'true',
    }
    with client.session_transaction() as session:
        session['username'] = 'TestUser'
    result = client.post('/set_recipe_favourited/5c951aa01c9d440000c6c7a7', data=form)
    # Expect status code 200 to indicate request success
    assert result.status_code == 200
    # Verify the recipe ID is now in the user's favourite list
    user = mongodb.users.find_one({"user_name": session['username']})
    assert ObjectId('5c951aa01c9d440000c6c7a7') in user['favourites']


def test_unfavourite_recipe_by_user_in_session(client, mongodb):
    app.mongodb = mongodb
    form = {
        'favourite': 'false',
    }
    with client.session_transaction() as session:
        session['username'] = 'TestUser'
    result = client.post('/set_recipe_favourited/5c951aa01c9d440000c6c7a7', data=form)
    # Expect status code 200 to indicate request success
    assert result.status_code == 200
    # Verify the recipe ID is now not in the user's favourite list
    user = mongodb.users.find_one({"user_name": session['username']})
    assert ObjectId('5c951aa01c9d440000c6c7a7') not in user['favourites']


def test_set_recipe_liked_by_user_in_session(client, mongodb):
    app.mongodb = mongodb
    form = {
        'liked': 'true',
    }
    with client.session_transaction() as session:
        session['username'] = 'TestUser'
    result = client.post('/set_recipe_liked/5c951aa01c9d440000c6c7a7', data=form)
    # Expect status code 200 to indicate request success
    assert result.status_code == 200
    # Verify the user name in session is now in the 'likes' list for that recipe
    recipe = mongodb.recipes.find_one({"_id": ObjectId("5c951aa01c9d440000c6c7a7")})
    assert session['username'] in recipe['likes']


def test_unlike_recipe_by_user_in_session(client, mongodb):
    app.mongodb = mongodb
    form = {
        'liked': 'false',
    }
    with client.session_transaction() as session:
        session['username'] = 'TestUser'
    result = client.post('/set_recipe_liked/5c951aa01c9d440000c6c7a7', data=form)
    # Expect status code 200 to indicate request success
    assert result.status_code == 200
    # Verify the user name in session is now not in the 'likes' list for that recipe
    recipe = mongodb.recipes.find_one({"_id": ObjectId("5c951aa01c9d440000c6c7a7")})
    assert session['username'] not in recipe['likes']


def test_login(client, mongodb):
    app.mongodb = mongodb
    # We have to set the password here because the fixture loads it in as a unicode string (and causes hard-to-debug bcrypt issues)
    mongodb.users.update({'user_name': 'TestUser'}, {
        'user_name': 'TestUser',
        'password': bcrypt.hashpw('MyPassword'.encode('utf-8'), bcrypt.gensalt()),
        'favourites': [ObjectId('6c951aa01c9d440000c6c7a8')]
    })
    form = {
        'user': 'TestUser',
        'pass_word': 'MyPassword'
    }
    result = client.post('/login', data=form)
    with client.session_transaction() as session:
        # Verify  the user is now in session
        assert 'username' in session
        assert session['username'] == 'TestUser'
        assert "6c951aa01c9d440000c6c7a8" in session['favourites']
    # Expect status code 302 to indicate successfully redirected
    assert result.status_code == 302
    assert "/get_recipes" in result.location


def test_login_fail(client, mongodb):
    app.mongodb = mongodb
    not_existing_user_form = {
        'user': 'Frank',
        'pass_word': 'HelloThere'
    }
    result = client.post('/login', data=not_existing_user_form)
    # Expect status code 200 as renders the template but does not redirect
    assert result.status_code == 200
    with client.session_transaction() as session:
        # Verify  the user is not in session
        assert 'username' not in session


def test_register(client, mongodb):
    app.mongodb = mongodb
    form = {
        'user_name': 'Paul',
        'password': 'NewPassword'
    }
    result = client.post('/register', data=form)
    # Expect status code 302 to indicate successfully redirected to home page
    assert result.status_code == 302
    assert "/get_recipes" in result.location
    # Verify user in session has been added to the users database
    assert mongodb.users.find_one({"user_name": "Paul"})
    # Verify the password of that user has been hashed
    password = mongodb.users.find_one({"password": "NewPassword"})
    assert not password
    with client.session_transaction() as session:
        # Verify the new user is now the username in session
        assert 'username' in session
        assert session['username'] == "Paul"


def test_register_fail(client, mongodb):
    app.mongodb = mongodb
    existing_user_form = {
        'user_name': 'TestUser',
        'password': 'Chocolate'
    }
    fail_result = client.post('/register', data=existing_user_form)
    with client.session_transaction() as session:
        # Verify the username given is not the username in session
        assert 'username' not in session
    # Expect status code 200 as renders the template but does not redirect
    assert fail_result.status_code == 200
