from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping

#setup flask
app = Flask(__name__)

# tell python how to connect to Mongo using PyMongo
# Use flask_pymongo to set up mongo connection
# the 'MONGO_URI' is a uniform resource identifier similar to a URL
#'mongodb://localhost:27017/mars_app' is the URI we'll be using to connect to Mongo
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)


#flask routes find the URL to a function following the route call @app.route
# line mars= mongo..... is using PyMongo to find the mars collection
# the mars database will be created by our scraping script
# the return statement says to use the index.html and the mars collection

@app.route("/")
def index():
   mars = mongo.db.mars.find_one()
   return render_template("index.html", mars=mars)


@app.route("/scrape")
def scrape():
   mars = mongo.db.mars
   mars_data = scraping.scrape_all()
   mars.update({}, mars_data, upsert=True)
   return redirect('/', code=302)

#tells flask to run
if __name__ == "__main__":
   app.run()