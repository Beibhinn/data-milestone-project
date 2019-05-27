# Data Centric Development Milestone project

## For Cook's Sake

I decided to design my data-centric development milestone project around the suggested brief: an online cookbook.

As a child, I loved to "help" my mother cook and bake, and can clearly remember her tattered notebook where she kept a record of all her recipes. Once I got older and moved away from home, occasionally I would have a craving for one of her recipes and would ask her to send it to me. This meant she would either have to type out the recipe, or take a photo of the page in the book and send that to me. This meant a lot of work for my mother, and also for me if she sent a photo, as faded lettering is not easy to make out.
I also enjoy looking up and trying new recipes on the internet. The only problem is, sometimes it can be difficult to find the same recipe a second time and to remember how you found it originally, or what website it was on. As a result, I have a lot of screenshots of recipes in my phone's photo gallery, in among all the other photos. This doesn't necessarily make it much easier to find the recipe, but at least I can be sure the right one is in there somewhere.

For these reasons, once I saw the example brief for this project, I immediately started thinking of what kind of website I myself would use. In this project I aimed to offer a solution to the issues mentioned above. I wanted a site where I could add and store my own recipes, as well as finding new ones to favourite and save for future reference.

My website can be found at the following URL: http://beibhinn-recipe-book.herokuapp.com/ 

### UX

#### User Stories
- As a cooking/ baking enthusiast, I want to be able to browse and view recipes, so that I can discover new recipes and find ideas and inspiration while planning meals.
- As a cook/ baker, I want to be able to save my own recipes somewhere they can easily be accessed, so I can find them easily when needed in the future.
- As a cook/ baker, I want to be able to store and post my recipes publicly, in order to share my recipes with others.
- As a cook/ baker, I want to be able to edit recipes I've previously posted, so they can evolve and update as I make improvements to the recipes.
- As a cook/ baker, I want to be able to delete old recipes I may not like anymore, so that I can replace it with a new, preferred recipe for the same item.
- As a cooking/ baking enthusiast, I want to be able to save other user's recipes as favourites, so I can easily find them later.
- As a cook/ baker, I want to be able to filter recipes, in order to find something that suits my needs/ cravings.
- As a cook/ baker, I want to be able to vote for and view top rated recipes, so I can take other user's opinions of a recipe into account when deciding whether to try it or not.

#### Wireframes
The wireframes I created for this project can be viewed [here.](https://github.com/Beibhinn/data-milestone-project/blob/master/wireframes.pdf)

### Features

In this section, you should go over the different parts of your project, and describe each in a sentence or so.

#### Existing Features

- **Navbar**: Allows all users to easily navigate to the different sections of the website, regardless of which page they are currently on, by clicking the name of the section they wish to visit in the navbar. 
- **Home Page**: Allows all users to view the current recipes on the site, and to filter down the recipes they wish to see by filling out the form and clicking 'filter'. The user can also sort the order the recipes appear in by clicking one of the four 'sort' buttons. (A-Z Ascending, A-Z Descending, Likes ascending, Likes descending). Viewers can also view a preview of the ingredients for a given recipe by clicking the title.
- **Full Recipe View**: Allows all users to view detailed information for a particular recipe, including author, cuisine, ingredients, method and tags. It also allows signed in users (other than the author of the recipe) to like and favourite the recipe. The owner/ author of the recipe can also edit or delete the recipe from this view, when signed in, by clicking the appropriate floating action button. 
- **Top Recipes Page**: Allows all users to view the 12 recipes with the most likes. 
- **Browse By Meal Page**: Allows all users to browse recipes separated by meal type, by clicking the tab with the name of the meal type they wish to view.
- **Account View**: Allows signed in users to view the recipes they previously uploaded to the site, and recipes they favourited, by clicking the appropriate tab.
- **Add New Recipe Form**: Allows signed in users to add a new recipe to the site, by filling out the form. 
- **Register Form**: Allows new users to create an account, by filling out a form, so that they can add recipes, save recipes as favourites, and like recipes.
- **Sign In Form**: Allows returning users to sign into their account, by filling out a form, so that they can add/ edit recipes, access their account and view favourites.
- **Author View**: Allows all viewers to see all of a particular author’s recipes by simply clicking their name on a given recipe.
- **Cuisine View**: Allows all viewers to see all recipes of a particular cuisine by clicking the cuisine name from the recipe view.
- **Tag View**: Allows all viewers to see all recipes relating to a tag by clicking the tag name from the recipe view.
- **Footer**: Informs the user that the site is hosted by Heroku, and provides as link to where they can view the source code on Github.
    


#### Features Left to Implement

- **Search by ingredient**: A feature where the user would be able to filter by ingredients they have to hand, so that they would not need to manually read through each recipe to see if they have the required ingredients.
- **Checklist of ingredients**: A checkbox beside each ingredient while viewing a recipe, so the user could check off the ingredients they have.
- **Import recipes**: A feature to allow users to import their favourite recipes from other sites directly, to store the all in the one place.
- **Upload own photos to recipe**: A feature to allow the user to upload their own photos to the database, instead of merely providing the URL for a related photo.
- **Make Recipes Public/ Private**: A feature to allow the user to choose whether they want a particular recipe to be visible to other users or just themselves.

### Technologies Used

- **HTML5**: HTML5 was used to create the structure of the website
- [**SCSS**:](https://sass-lang.com/documentation/syntax) SCSS was used to style the website.
- [**JQuery**:](https://jquery.com) : JQuery was used to simplify DOM manipulation.
- [**Font Awesome**:](https://fontawesome.com) : Font Awesome was used to add icons to the site, such as the like and favourite icons.
- [**Materialize 1.0.0**:](https://materializecss.com/getting-started.html) : As Materialize is designed with the Mobile First Approach in mind, this framework was used to help structure the website, ensuring that it would be compatible on mobile devices. Bootstrap would also have served this purpose, however in this case, I chose materialize to force myself to become familiar with working with other frameworks, to ensure I do not become overly reliant on Bootstrap.
- [**Flask 1.0.2**:](http://flask.pocoo.org/docs/1.0/) : Flask was used as it is an easy-to-use and flexible RESTful framework. Its built-in templating engine Jinja allows for rapid prototyping and iterating of pages and endpoints.
- [**MONGODB**:](https://www.mongodb.com/) : MongoDB was used for its flexible JSON-like document data model, making the database scalable and flexible. As MongoDB also has a native Python driver, PyMongo, this seemed like a good choice, as I would be using Python for the backend of this project.
- [**BCrypt**:](http://bcrypt.sourceforge.net/) : BCrypt was used to hash user passwords, for storage in the database. This was to add an element of security to the user accounts.
- [**Pytest**:](https://docs.pytest.org/en/latest/) : Pytest was used to write better tests for the project, ensuring the site works as intended.
- [**Python 3.7**:](https://www.python.org/) : This is the latest, most stable version of Python, and was used to create the backend of the site.
- [**Postman**:](https://www.getpostman.com/) : This program was used to manually test the POST endpoints.
    
### Testing

#### Manual Testing

1. *Navbar* :
    - Click on each of the links within the menu (including the logo), and verify that each one is functioning correctly, and that they take the user to the correct page.

2. *Home page* :
    - Click on the filter button to verify that a form appears. Choose some filters and submit, ensuring that the chosen filters appear as a query string in the URL and that you are redirected to a page with the results. Go back to the home page for further testing.
    - Click each of the sort buttons and verify the order of the recipes changes appropriately.
    - Click the title or three vertical dots and ensure that a preview of the required ingredients is displayed.
    - Click the name of the author for each recipe and verify that you are redirected to a page displaying all recipes posted by that author.
    - Click 'full recipe' and ensure you are redirected to a card showing the full information for the recipe you selected.
    - Click the numbers or chevrons for pagination to ensure a page of different recipes is displayed.
    - Click the floating action button on the bottom right of the screen and ensure you are redirected to a form where you can add a recipe if you are already logged in, otherwise, that you are brought to the login page and prompted to do so before adding a recipe.

3. *Top recipes page* :
    - Click the title or three vertical dots and ensure that a preview of the required ingredients is displayed.
    - Click the name of the author for each recipe and verify that you are redirected to a page displaying all recipes posted by that author.
    - Click 'full recipe' and ensure you are redirected to a card showing the full information for the recipe you selected.
    - Scroll to the bottom of the page to ensure no pagination is displayed, as a limited number of recipes will always appear in the top recipe page.
    - Ensure all recipes displayed have more than 0 likes.
    - Click the floating action button on the bottom right of the screen and ensure you are redirected to a form where you can add a recipe if you are already logged in, otherwise, that you are brought to the login page and prompted to do so before adding a recipe.
    - As an additional test, go back to the home page and choose a recipe with no likes. Click full recipe and click the like button on the bottom right. Return to the 'top recipes' page and verify the recipe you just liked is now displayed here. (This test will only work if the recipe limit for the page has not been reached. Alternatively you can like a recipe which already has likes from other users and verify that the recipe's position in the 'top recipes' page has changed.)

4. *Browse by meal* :
    - Click each of the tabs along the top of the screen and ensure the recipes displayed changes as a different meal type is selected.
    - Click the title or three vertical dots and ensure that a preview of the required ingredients is displayed.
    - Click the name of the author for each recipe and verify that you are redirected to a page displaying all recipes posted by that author.
    - Click 'full recipe' and ensure you are redirected to a card showing the full information for the recipe you selected. Verify that the meal type of the recipe you are viewing matches the tab that you found the recipe in.
    - Click the floating action button on the bottom right of the screen and ensure you are redirected to a form where you can add a recipe if you are already logged in, otherwise, that you are brought to the login page and prompted to do so before adding a recipe.

5. *View full recipe* :
    - Click the name of the author and verify that you are redirected to a page displaying all recipes posted by that author.
    - Click the cuisine name and verify that you are redirected to a page displaying all recipes with that same cuisine type.
    - Click the tags and verify that you are redirected to a page displaying all recipes with the same tag you selected.
    - When logged in and viewing another user's recipe, verify there is a like and favourite button in the bottom right corner (a thumbs up icon and a heart). Click these icons to toggle (a filled- in icons means it is liked/ favourited). If you've selected 'like' for a particular recipe, verify that the number of likes displayed on that recipe's card on the home page has increased by one. If you've selected 'favourite' for a recipe, verify that it is now displaying in your 'favourites' section of your account.
    - When logged in and viewing your own recipe, verify that there are two floating action buttons at the bottom of the photo, on the right hand side: the delete button and the edit button. Click delete and verify a dialogue box pops up confirming the action. Click 'cancel' to exit the dialogue and stop the delete. Click 'ok' to confirm and delete. Click the edit button and verify you are redirected to a form with the recipe's information. Please note at this time a user cannot like or favourite their own recipes, and so the like and favourite buttons will not appear on a user's own recipe. A user's own recipes are stored in their account, and not allowing a user to like their own recipe means other user's can be more confident that likes on a recipe are not biased.

6. *Register form* :
    - Click the 'register' button in the navbar to be brought to the register page
    - Click the 'log in here' link at the bottom of the card and verify you are brought to the login page
    - Try to submit the empty form and verify that required fields are indicated
    - Try to submit the form with invalid login details and verify that a relevant error message appears
    - Try to submit the form with valid inputs and verify that you are redirected to the home page, with your user name displayed on the top right of the navbar (or in the lower section of the sliding navbar on mobile)


7. *Sign in form* :
    - Click the 'sign in' button in the navbar to be brought to the register page
    - Click the 'register here' link at the bottom of the card and verify you are brought to the register page
    - Try to submit the empty form and verify that required fields are indicated
    - Try to submit the form with invalid login details and verify that a relevant error message appears
    - Try to submit the form with valid inputs and verify that you are redirected to the home page, with your user name displayed on the top right of the navbar (or in the lower section of the sliding navbar on mobile)

8. *Account view* :
    - Click the first tab along the top of the screen and ensure the only recipes displayed are those posted by the user you are logged in as.
    - Click the second tab along the top of the screen and verify that recipes you have favourited are displayed.
    - Click the title or three vertical dots and ensure that a preview of the required ingredients is displayed.
    - Click the name of the author for each recipe and verify that you are redirected to a page displaying all recipes posted by that author.
    - Click 'full recipe' and ensure you are redirected to a card showing the full information for the recipe you selected. Verify that the meal type of the recipe you are viewing matches the tab that you found the recipe in.
    - Click the floating action button on the bottom right of the screen and ensure you are redirected to a form where you can add a recipe.

9. *Add recipe form* :
    - Go to the 'add new recipe' page
    - Try to submit the empty form and verify that the required fields are indicated
    - Click the blue '+' buttons to ensure a new input line is added for both ingredients and method, and that a red delete button appears.
    - Click the red 'x' buttons to ensure extra input lines can be deleted if not required, but that the delete button becomes hidden again when there is one input line, to ensure the user can't accidentally remove the option to add an input.
    - Start typing into the 'cuisine type' field, and verify that existing types are auto-completed or prompted.
    - Start typing into the 'cuisine type' field, and verify that existing types are auto-completed or prompted.
    - Start typing into the 'tags' field, and verify that existing tags are auto-completed or prompted. If one is selected, verify it appears in a 'chip' and that the 'x' will remove the chip.
    - Click the 'add recipe' button after inputting all required information, and verify you are redirected to the home page, where your recipe should now be visible.

10. *Add recipe form* :
    - Go to the 'edit recipe' page and verify the information you previously entered in automatically filled in into the form.
    - Click the blue '+' buttons to ensure a new input line is added for both ingredients and method, and that a red delete button appears.
    - Click the red 'x' buttons to ensure extra input lines can be deleted if not required, but that the delete button becomes hidden again when there is one input line, to ensure the user can't accidentally remove the option to add an input.
    - Make whatever changes you wish to your recipe, then click the 'update recipe', and verify you are redirected to the home page. Click to view full recipe and verify that it is showing the updated information.

Postman was also used to manually test the forms and the responses received, to ensure they were as expected. My postman collection can be viewed [here.](https://github.com/Beibhinn/data-milestone-project/blob/master/postman_collection)

####  Automated Testing

While manual testing was done on every feature possible, I also wrote some tests in order to automate the process, and ensure everything was working as it should, to the best of my ability. Unit testing can be found in https://github.com/Beibhinn/data-milestone-project/blob/master/test_app.py. To run the tests simply perform `python3 test_app.py.` These tests focus on the behaviours/ possible actions of the users as they interact with the website, and the expected outcomes of these interactions. The tests verify that all pages and templates are rendered as expected, and also tests CRUD functionality for the database. 

I did have some trouble at the beginning, as I did not want my tests to run and make changes to my live database. For this reason, I mocked the database myself by creating fixtures with mock records, containing the required information for the tests. This means that the tests can be run independently of the live database. 
I also had an issue with the test to check the login feature, where I kept getting the same error repeatedly, even though it seemed to work as expected on the actual site ('TypeError: Unicode-objects must be encoded before hashing'). It turned out that the information in the mock collections, was being loaded as Unicode, which caused the test to fail. To remedy this, I inserted the user and password into the collection within the test. 

This project is fully responsive, and each section adjusts and resizes to fit every screen size. This was tested using devices with various screen sizes, as well as the ‘responsive design mode’ tool in firefox. All features are available on all devices, with easy to use navigation, to help the user get around.


### Deployment

The source code can be viewed on [GitHub](https://github.com/Beibhinn/data-milestone-project).  A live demo has been deployed to [Heroku](http://beibhinn-recipe-book.herokuapp.com/).

In order to deploy to Heroku, a Procfile had to first be created to allow Heroku to identify the type of application that was being handled. The required modules were also exported to a requirements.txt file so that all dependencies could be automatically installed by the host. A Heroku remote was added to the git repository so that the project could be deployed to Heroku via `git push`.

The app relies on the following environment variables, which can be set for Heroku via the web console. If deploying locally, setting these depends on the operating system used.

| Name | Description | Example |
| ------------- |:-------------:|: -----:|
| DB_NAME    | the name of the Mongo database to be used | `recipe-book` |
| IP      | the IP address on which to host the app     |   `0.0.0.0` (to listen on all interfaces) |
| MONGO_URI | the location of the MongoDB instance      |    `mongodb+srv://<USER>:<PASSWORD>@myfirstcluster-8j8nw.mongodb.net/recipe-book?retryWrites=true` |
| PORT | the port to listen on      |   `80` (for default HTTP traffic) |
| SECRET | the key used to encrypt and decrypt the session cookies      |    `ThisCanBeAnythingYouWant` |


To deploy locally:
- Clone repository, open terminal in repository folder
- `pip install -r requirements.txt`
- `python app.py`
- Set the environment variables. Ie. set IP to `127.0.0.1` and the others as normal
- Open `http://localhost:<PORT>`

### Credits

#### Content

The content for the recipes in the database were found on various sites, and used for the purpose of populating my database. The links to where the recipes were originally found are listed below. 
   
-[*Red Velvet Recipe*](https://www.lolascurls.com/blog/recipe-of-the-week-red-velvet)

-[*Rice Krispie Treats*](https://www.twosisterscrafting.com/best-ever-rice-krispie-treat-recipe/)

-[*Chocolate Brownies*](https://www.bbcgoodfood.com/recipes/1223/bestever-brownies)

-[*Strawberry Pavlova*](https://thehappyfoodie.co.uk/recipes/strawberry-pavlova)

-[*Ultimate Spaghetti Carbonara*](https://www.bbcgoodfood.com/recipes/1052/ultimate-spaghetti-carbonara)

-[*Beef Stroganoff*](https://www.bbc.com/food/recipes/beef_stroganoff_16029)

-[*Macaroni Cheese*](https://www.bbcgoodfood.com/recipes/8834/bestever-macaroni-cheese)

-[*Shepherd’s Pie*](https://www.bbcgoodfood.com/recipes/9644/nofuss-shepherds-pie)

-[*Chicken with Sun-dried Tomato Cream Sauce*](https://damndelicious.net/2014/11/22/chicken-sun-dried-tomato-cream-sauce/)

-[*Italian Wonderpot*](https://www.budgetbytes.com/italian-wonderpot/)

-[*Light 'N Fluffy Gluten Free & Keto Waffles*](https://www.gnom-gnom.com/grain-free-keto-waffles/)



#### Media

The photos used in this site were obtained from the respective sites where each of the recipes were found (listed above). Where photos were not available, alternatives were found on google images. 



