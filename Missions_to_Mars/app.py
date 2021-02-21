# Dependencies
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create a Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017")


# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    # Find one record of data from the mongo database
    mars_facts_dict = mongo.db.mars_facts_dict.find_one()

    # Return template and data
    return render_template("index.html", mars=mars_facts_dict)


@app.route("/scrape")
def scrape():
  
    mars_facts_dict = mongo.db.mars_facts_dict
    mars_data = scrape_mars.scrape()
    
    # Update the Mongo database using update and upsert=True
    mars_facts_dict.update({}, mars_data, upsert=True)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)