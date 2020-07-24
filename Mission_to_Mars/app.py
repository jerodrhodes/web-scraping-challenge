from flask import Flask, render_template, jsonify, redirect
import pymongo
import scrape_mars
from flask_pymongo import PyMongo

app = Flask(__name__)

# # Use flask_pymongo to set up mongo connection
# app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
# mongo = PyMongo(app)


# @app.route("/")
# def index():
#     mars_data = mongo.db.mars.find_one()
#     return render_template("index.html", mars_data=mars_data)

# @app.route('/scrape')
# def scraper():
#     mars_data = mongo.db.mars
#     mars_data = scrape_mars.scrape()
#     mars_data.insert_one({}, mars_data)
#     return redirect("/", code=302)

# create mongo connection
client = pymongo.MongoClient()
db = client.mars_db
collection = db.mars_data_entries

@app.route("/")
def home():
    mars_data = db.collection.find_one()
    return  render_template('index.html', mars_data=mars_data)

@app.route("/scrape")
def scraper():
    db.collection.remove({})
    mars_data = scrape_mars.scrape()
    db.collection.replace_one({}, mars_data, upsert=True)
    return redirect('/', code=302)

if __name__ == "__main__":
    app.run(debug=True)
