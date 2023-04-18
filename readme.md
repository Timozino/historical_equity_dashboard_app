 
Admin Username = Timson


Admin Password = 123456



Admin email = timson@gmail.com



                                    OVERVIEW
Historical Equity Dashboard App, is a web task that was best unsderstood to automate some processes like:
    - Populate the database with the given demo accounts
    - Initiate login through 3rd-Party API of a Trading app called MT5-Meta Data, every 60 seconds
    - Fetch the data of Equity, balance, and timestamp data from the MT5 trading app, and send them to the database, repeatedly for every 60 seconds.
    - Create a view that Fetches those data, and renders them to the template page that will display them graphically for every 60 seconds.


                                    Technology
The technologies used were:
    - Python -- As the backend Language for Logic
    - Django -- As the backend Framework for Python
    - Django Rest Framework-- As the app Api to automate some process from the frontend, and to perform a GET and POST requests on the App
    - HTML5 -- As the Markup Language to structure the frontend
    - BOOTSTRAP -- As the CSS3 framework to speed-up styling
    - JavaScript -- As the frontend Language to Script and Give functunality to the frontend by adding behavior
    - Jquery-- As the JavaScript Library to reduce Dry-coding within the frontend
    - Chart.JS -- As the Javascript library to create graphical representation
    - Sqlite3 -- The uses SQL RDS to handle Django project database in development stage.


                                    CHALLENGES:
    1. I initially found it difficult to initialize a process and login to MT5 trading website, this really gave me a so much concern, while I was thinking my logic were wrong. Deleted the project and restarted all over. 
                                    FIX
    1. I ran a test module on my app using unittest and pytest system to be sure I was doing the correct thing, and it all came out PASSED. So, It's was definitely not internally, but externally. Nothing wrong with my app.

                                    CHALLENGES:
    1. I decided to login to the MT5 trading site, using the demo accounts provided for this project, and I figured, none of the credentials were valid. So, I registered an account on the site, while trying to initialize a login from my app, I got the same error 500 (server error) both ways, and I then decided to use the login on the same site it was registered from, and I experienced the same error, then further research resulted to the understanding that the website is known for login issues. This was written on their internal community FAQs page. Several complains regarding login, which makes me to conclude that the sites has issues with logging in. 
                                    FIX
        - The fix for it was to wait an hour, after which I was able to login, and tried to log-out again, and I could no longer log in. A community info clears the air that MT-5 Trader disallows connections from less-secure apps. I tried to create a dummy data, and i tried to see of it will render, and it worked, this confirmed my code to be efficient. HTTP ERROR 500 is also another proof that the MT5 trader app is denying access from 3rd party and less-secure apps. 

                                    PROJECT STRUCTURE

1. I created a dashboard_app_task folder, cd into it.
2. I created a Virtual environment to hold my installations (task_view)
3. I installed Django, and started project named (historical_equity_dashboard_app)
4. I installed APP (dashboard), and Registered it in INSTALLED_APPS of settings.py
5. models.py- This is where the database logic codes are contained
6. admin.py This is where the admin dashboard codes are contained
7. views.py- This is where my business logic are handled
8. serializers.py - This serializes my api data from query on the database
9. settings.py - Handles my project installations and connectivity
10. urls.py (Global)- This handles my external routing
11. urls.py(APPS) - This handles my internal routing
12. templates folder- This handles my template files, that renders the logic from views.py


                                    TECHNICAL SUGGESTION
In you could study this app thoroughly, in the AccountDataView, I created an instance of the MT5Trader class for each account ID. However, instead of calling the "get_trading_account_data" method of the MT5Trader instance, I used the "get_account_data_at_interval" method to get the account data at a regular interval. This method uses a generator to yield account data at the specified interval, so we can simply loop through the generator to get account data for all accounts.

I then created an AccountData instance for each account, using the account ID, equity, balance, and market watch time from the account data. I saved this instance to the database using the create method of the AccountData model.

Note that this modified version of AccountDataView uses an infinite loop to continuously get account data at the specified interval. This means that the view will not return a response until it is interrupted, either manually or by an error. In a professional use case, I would not do that, I may want to consider running this view as a background task using a tool like Celery or Django Channels, rather than as a part of a request-response cycle.
I may also decide to use a message broker, like RabbitMQ or Cloud-base Redis to automate the process through a background task. This method ensures speed and accuracy, as well as improves the efficiency of Space and Time complexities.




