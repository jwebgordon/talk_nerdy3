#import everything we need
from flask import Flask, render_template, request, redirect
import requests

#Create the Flask app
app = Flask(__name__)


@app.route("/",methods=["GET"]) #This function will be activated when a user goes to www.your-app.com/
def index():
	#the code in this function is run when the root URL is hit
	print "Hello, I am the index function"
	return render_template("index.html")


#Add in the URL path for your form action
@app.route("/yourFormRouteHere",methods=["GET","POST"])
def form_submit():
	#replace 'pass' with the code for your form submission handler
	#check out the 'request' and 'render_template' documentation
	#render the results to the 'form_result.html' template
	pass


#Start up the app when the app.py file is run
if __name__ == "__main__": 
	app.debug = True
	app.run()