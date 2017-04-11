# Hello and Welcome to Talk Nerdy to M3

This go round, we’re going to experience the process a developer undertakes to implement and build an app on HubSpot. We’ll work through the HubSpot development portal steps, get Python and Flask up and running, launch a small app on Heroku and then code to initiate oAuth. Once oAuth is granted, we’ll be able to make authenticated requests to any of HubSpot’s APIs in a production environment.
### What is oAuth and how does it work?
At it’s simplest, oAuth is a prescribed method and flow that allows a user to grant access to a platform's data to a third party system. It stands for ‘open authentication’ and allows users to grant this permission for access without directly giving the 3rd party your password. This flow enhances security by authenticating to a single user (instead of using server-side keys), and not having those aforementioned passwords stored in 3rd party databases. The access tokens that are granted to the user allow authenticated requests to the data. 

### General outline of the session:

- Create a HubSpot developer portal and an app in that portal
- Install and run Python, Flask, Requests, Git and Heroku
- Build oAuth Flow in our Python/Flask apps.
-- Create a route/endpoint to handle a front end action and print result/output in backend to terminal
-- Create button with authorize URL (in template)
-- Create route to handle authorize
-- Build authorization code
-- Deploy to Git and Heroku
-- Use the granted token to make an authorized request
-- Party
- Choose: Make authenticated Contacts Call or Implement Timeline API
## First, Knowledge.
Before we dive into our first tasks, let’s understand the way an oAuth flow works. There are 4 main steps to this flow.

1. An app is created in a developer portal, which provides a ‘client id’ and a ‘client secret’. 
    a. The client secret is similar to a HAPI key i.e. it should only be used locally or server side - keep it secret, keep it safe! 
    b. You’ll build an authentication URL for your app that sends the user to HubSpot, where they will grant access using their username and password. 
    c. This is generally just a normal <a> tag or <button> where the ‘href’ points to the service where access will be granted. Note the client_id, scope and redirect (where to go after access is granted)
    d. Example: `<a href="https://app.hubspot.com/oauth/authorize?client_id=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx&scope=contacts%20automation&redirect_uri=http://www.hubspot.com">Authorize me, captain!</a>`
    e. If access granted, the user is redirected to this URL: `http://www.hubspot.com?code=xxxx`
    f. [Read the authentication URL docs](http://developers.hubspot.com/docs/methods/oauth2/initiate-oauth-integration)
2. Upon successful auth, the user is redirected to your app with a `code` appended to the URL. That code is exchanged along with the client secret to get an `access_token` and a `refresh_token`. 
    a. This ‘exchange’ is done via a server-side HTTP call so that you don’t expose your client secret.
    b. The code in the URL is accessible via the request object in Flask
    c. [Read the docs to understand how to do this POST request exchange](http://developers.hubspot.com/docs/methods/oauth2/get-access-and-refresh-tokens)
3. The `access_token` is used to make authenticated API calls. 
    a. An authenticated call using oAuth 2.0 is different than oAuth 1.0. Instead of appending the token to the URL as a query parameter, all HTTP calls carry a header: `Authorization: Bearer CJSP5qf1K-this-is-a-token-qYAGQsF4`
    b. Once that `access_token` expires (after 6 hours), use the `refresh_token` to generate a new `access_token`. The `refresh_token` was obtained in the initial `code` exchange. The refresh token is sent in another HTTP request and a new `access_token` is provided. [Read the docs about using a refresh_token](http://developers.hubspot.com/docs/methods/oauth2/get-refresh-token-information)

## Second, Action.
Let's start by registering an app and installing all the things.
### Step 1 - Create a Developer Portal and App
1. Create a HubSpot Developer portal if you don't already have one. 
    a. [Sign up here](https://app.hubspot.com/developers/signup)
    b. Or, [Login to existing account and select dev portal](https://app.hubspot.com/login/)
2. Create an app in your developer portal
3. Find your `appId`, `client id`, and  `client secret` 
4. Take a deep breath, stuff's about to get real.

### Step 2 - Initiliaze a Flask app
1) Let's make sure we have (most) everything we need installed. 
    a. Open up your terminal app. (OSX: either Terminal or iTerm, Windows: Command Prompt, or download [win-bash](https://sourceforge.net/projects/win-bash/files/shell-complete/latest/)). 
    b. Find your installed version of Python with `python -V`. If 2.7, we should be good to go. Note: Windows users will likely need a fresh install of Python 2.7 from the [Python website](https://www.python.org/).
    b. Install Flask with `pip install flask` - note: if you encounter errors, try a fresh install of Python 2.7 from the [Python website](https://www.python.org/)
    c. Install Requests with `pip install requests`
    d. Install Git with `brew install git`
2) In your terminal, navigate to where you would like to build your project
        _Reminder:_
        `ls` to list files and folders in current location
        `cd {folder_name}` to move into a folder
3) Once you're in the folder you want, clone the starter code with: `git clone https://github.com/jwebgordon/talk_nerdy3.git`. This will create a new directory in your current folder. 
4) Open up Sublime Text and open the directory that you just created (File > Open). Take a look around and explore the code.
5) When you think you understand how it works, run the app from your terminal. Make sure you are in the root of the project folder (`cd talk_nerdy3`), and run the app with `python app.py`
6) Load up the app in your browser at `localhost:5000`

### Step 3 - Make your frontend talk to the backend
1) Head back into the code and add a `<form>` to the index.html template (give it a field or two). Set it up to submit to a specific URL path for your app (choose whatever you want).
2) In app.py, add a new handler for the form submission (use the same URL you added to the form)
3) Retrieve the form fields that were submitted and print them to the console (hint: check out [Flask's `request` module](http://flask.pocoo.org/docs/0.12/quickstart/#accessing-request-data))
4) Have your form handler render a new template (you'll need to create a new HTML file), and display the form field values on the page (check out the documentation for the `render_template` method) hint: you can pass data to the template in this method.

### Step 4 - Installing Heroku Command Line Toolbelt
To properly redirect through our flow, we need a securely hosted app (a requirement of HubSpot's oAuth service and a general all around good idea). This can be done locally, but requires a somewhat esoteric configuration of your local environment. Instead, we'll deploy our app to a securely hosted Heroku app. We'll deploy multiple times throughout the oAuth development flow. Follow the instructions below. You can also find this documentation [ directly on Heroku](https://devcenter.heroku.com/articles/getting-started-with-python)
1. [Sign up for a free Heroku account](https://signup.heroku.com/signup/dc)
2. [Download the Heroku Command Line Tools for OSX](https://devcenter.heroku.com/toolbelt-downloads/osx) or [for Windows](https://devcenter.heroku.com/toolbelt-downloads/windows64)
3. Once installed, you can use the `heroku` command from your command shell. Login w/ username and password (may be prompted at a later step)
4. `cd` back to your local app directory
5. Heroku uses git to determine how to build your app. It also requires 2 configuration files to tell it that it's running a Python app and swap in a production-ready server. Let's create a .gitignore file, Heroku Procfile, and runtime/requirements file. We'll then add and commit any changes to our git repo.
    a. Create a Procfile (required by Heroku to launch a production server): `touch Procfile` and then `open Procfile`
    b. In your Procfile, paste `web: gunicorn -w 4 -b "0.0.0.0:$PORT" app:app` This defines gunicorn as your server, which is production ready, unlike the lightweight server that's included in Flask that you've been running locally
    c. Create a requirements.txt file, letting Heroku's pip instance know how to install your app. `touch requirements.txt` then `open requirements.txt`
    d. Paste the following:
```Flask==0.12.0
Jinja2==2.8.1
Werkzeug==0.8.3
certifi==0.0.8
chardet==1.0.1
gunicorn==19.6.0
requests==2.13.0
wheel==0.24.0
httplib2==0.9.1
```
6. Next, create a .gitignore file to leave git files out of your build process (they're detritus, not worthy of being included): `touch .gitignore` then `open .gitignore`
    a. Copy and save the contents of this [common .gitignore file](https://gist.github.com/octocat/9257657) and save and close
    b. Add/stage all the files in your local repo with `git add *` 
    c. Then commit (i.e. save the version) with `git commit -m "include a short informative message about the commit"`
6. Now we're ready for an initial deployment to Heroku. Create an app on Heroku, which prepares Heroku to receive your source code: `heroku create`
7. Deploy your app to Heroku using  `git push heroku master`
8. The application is now deployed. Your app will have a URL structure like `https://funny-named-number.herokuapp.com`. You will use this as the root of your redirect URL in your oAuth flow.
9. Ensure that at least one instance of the app is running: `heroku ps:scale web=1`
9. Now visit the app at the URL generated by its app name. As a handy shortcut, you can open the website with `heroku open`
10. Congrats, you have now, as they say, "Deployed to Production"

### Step 5 - oAuth Time
1) Create a new route/handler/template in app.py for the `/oauth` URL path (`@app.route("/oauth")`)
2) In the template you create for `/oauth` add a button (`<a>`) and link to the [HubSpot oAuth Authorize URL](http://developers.hubspot.com/docs/methods/oauth2/initiate-oauth-integration). Make sure to add your client ID, scopes, and decide on a callback URL for your app. The base of the callback URL (the domain) should be your Heroku domain (https://funny-name-number.herokuapp.com/{your_path})
3) Once the button is clicked, the user will eventually be redirected to the callback URL you specified. Create a new route/handler in app.py for that path that you chose for your callback URL. 
4) This method for the callback URL will be the meat of the oAuth implementation. Take a read through [this part](http://developers.hubspot.com/docs/methods/oauth2/get-access-and-refresh-tokens) of the documentation. The callback URL of your app will be called, and will include a request parameter for "code=" that you will use in combination with the `client_id` and `client_secret` to get the access token and refresh token.
5) Once you have successfully retrieved the access token and refresh token, render a new template from the callback function, and display the tokens on the page. 
6) When you think you have an `/oauth` route and template, redeploy the app with `git add *`, `git commit -m "message"`, `git push heroku master`
7. Visit your handler/route and attempt to authorize via your button. If you hit errors, view your terminal and figure it out. Re-commit and re-deploy as necessary

## You're a master of karate and friendship for everyone
### Step 6- Choose Your Own Adventure
1. Have the user enter an email address in a custom form and after submission, return the Contacts API data to the front end *easier adventure*
    a. A general outline could include...
    b. Build a new template that has a form
    c. Store the access token as a cookie by using Flasks `session` module (or, just have a form where you can manually enter it, then use it on the backend)
    d. On submission, use the access token in your cookie and email address in form to make a Contacts request
    e. Return the Contacts data to the template as data to render.
2. Create a Timeline API integration.
    a. Create your types
    b. Make a call that tags an event to a contact.

















