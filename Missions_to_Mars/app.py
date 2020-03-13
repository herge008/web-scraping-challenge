from flask import Flask, jsonify, render_template, redirect
from flask_pymongo import PyMongo
import flask
import scrape_mars

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars"
mongo = PyMongo(app)

@app.route("/")
def home():
    data = mongo.db.mars_data.find_one()
    return render_template("index.html", mars=data)

@app.route("/scraper")
def scraper():
    mongo.db.mars_data.drop()
    data_scraped = scrape_mars.scraper()
    mongo.db.mars_data.insert_one(data_scraped)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)