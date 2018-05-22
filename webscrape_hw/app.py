#put dependancies in and initiate flask
from flask import Flask, render_template, jsonify, redirect
from flask_pymongo import PyMongo
import scrape_mars


#initiate flask app and name app variable
app = Flask(__name__)
#have mongo going for data base mars is the database
mongo = PyMongo(app)


#first route
@app.route('/')
def index():
    mars = mongo.db.mars.find_one()
    return render_template('index.html', mars=mars)

#use your scrapper app
@app.route('/scrape')
def scrape():
    mars_data = mongo.db.mars
    mars_data_scrape = scrape_mars.scrape()
    mars_data.update(
        {},
        mars_data_scrape,
        upsert=True
    )
    return redirect("http://127.0.0.1:5000/", code=302)


if __name__ == "__main__":
    app.run(debug=True)