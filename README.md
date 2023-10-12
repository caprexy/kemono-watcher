# What is kemono-watcher
On Kemono you can see artist's posts, for the sack of archiving some artist are easy as they post directly to the website and thus kemono itself. But others post links to MEGA, google drive, etc. These cannot be automated for archive programs like hyrdrus, so this program creates a manual way to archive artists and view what posts you have not yet seen. 

# Installation

pip install -r requirements.txt

To run, just do python application.py

# How to use
For example, to watch https://www.patreon.com/shencomix you can use https://www.kemono.party/patreon/user/72813 as a proxy. Enter in the ID and select the website(Pateron) in the left panel and add to subscriptions. You will now see Shen or 72813 appear in the known users section at the bottom of the left input panel. Can select them in the list and hit get selected users. By default, all posts will be known but you can move them around by selecting them and moving them around.

On the right, one can hit update unread posts and all currently unknown posts will be displayed there for all users, and the program will attempt to get all new unknown posts. This does not account for the situation where posts may have been updated past the first page but not the first page as this is probably rare and checking all pages would slow down the program. Otherwise once the list is generated, can select one or many posts and open selected post to open in the standard system web browser.


# Tech overview
Uses python's inbuilt tkinter to build the application and GUI. SQlite for storing everything in the database.db. And unittest to implement testing, mocking, etc.

Coverage is used to generate coverage reports and can see the results in here(coverage %) or github actions.

[![Coverage badge](https://raw.githubusercontent.com/caprexy/kemono-watcher/python-coverage-comment-action-data/badge.svg)](https://htmlpreview.github.io/?https://github.com/caprexy/kemono-watcher/blob/python-coverage-comment-action-data/htmlcov/index.html)

Pylint is also the coding style used for linting, there is a pylint github action to check and make sure atleast a score above 9 out of 10. 

Borrows several github actions, see the yamls for relevant actions used
