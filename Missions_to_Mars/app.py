from flask import Flask, render_template
import pymongo
app = Flask(__name__)
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)
db = client.mars_db

@app.route('/')
def index():
	mars_info = list(db.mars_info.find())
	return render_template('index.html', mars_info=mars_info)


@app.route('/scrape')
def scrape():
	import scrape_mars
	mars_dict = scrape_mars.scrape()
	db.mars_info.drop()
	db.mars_info.insert_one(mars_dict)
	return "scraped"


if __name__ == "__main__":
	app.run(debug=True)