from flask import Flask, render_template, request, redirect
import requests


app = Flask(__name__)


@app.route("/",methods=["GET"]) #This function will be activated when a user goes to www.your-app.com/
def index():
	#the code in this function is run when the root URL is hit
	print "Hello, I am the index function"
	return render_template("index.html")


#Add in the URL path for your form action
@app.route("YOUR FORM ROUTE HERE",methods=["GET","POST"])
def form_submit():
	#replace 'pass' with the code for your form submission handler
	#check out the 'request' and 'render_template' documentation
	#render the results to the 'form_result.html' template
	pass


if __name__ == "__main__": 
	app.debug = True
	app.run()