from flask import Flask, render_template
import pymongo
import json
import imp

app = Flask(__name__)

conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)
db = client.mars_db
items = db.items
import mission_to_mars



@app.route("/")
def index():

    martian_news = db.items.find_one({"martian_key":"news"})
    martian_featured_image_url = db.items.find_one({"martian_key":"featured_image_url"})
    martian_mars_weather = db.items.find_one({"martian_key":"mars_weather"})
    martian_mars_facts = db.items.find_one({"martian_key":"mars_facts"})

    martian_hemispheres = db.items.find_one({"martian_key":"hemisphere_image_urls"})
    martian_hemisphere_list = martian_hemispheres['martian_data']['hemisphere_image_urls']



    return render_template("index.html", \
        news_title = martian_news['martian_data']['news_title'],
        news_p = martian_news['martian_data']['news_p'],
        featured_image_url = martian_featured_image_url['martian_data']['featured_image_url'],
        mars_weather = martian_mars_weather['martian_data']['mars_weather'],
        mars_facts = martian_mars_facts['martian_data']['mars_facts'],    
        title_0 = martian_hemisphere_list[0]['title'],
        img_url_0 = martian_hemisphere_list[0]['img_url'],
        title_1 = martian_hemisphere_list[1]['title'],
        img_url_1 = martian_hemisphere_list[1]['img_url'],
        title_2 = martian_hemisphere_list[2]['title'],
        img_url_2 = martian_hemisphere_list[2]['img_url'],
        title_3 = martian_hemisphere_list[3]['title'],
        img_url_3 = martian_hemisphere_list[3]['img_url'])

@app.route("/update")
def update():
    print("Calling mission_to_mars")
    imp.reload(mission_to_mars)
    print("Callend mission to mars")

    martian_news = db.items.find_one({"martian_key":"news"})
    martian_featured_image_url = db.items.find_one({"martian_key":"featured_image_url"})
    martian_mars_weather = db.items.find_one({"martian_key":"mars_weather"})
    martian_mars_facts = db.items.find_one({"martian_key":"mars_facts"})

    martian_hemispheres = db.items.find_one({"martian_key":"hemisphere_image_urls"})
    martian_hemisphere_list = martian_hemispheres['martian_data']['hemisphere_image_urls']
    return render_template("index.html", \
        news_title = martian_news['martian_data']['news_title'],
        news_p = martian_news['martian_data']['news_p'],
        featured_image_url = martian_featured_image_url['martian_data']['featured_image_url'],
        mars_weather = martian_mars_weather['martian_data']['mars_weather'],
        mars_facts = martian_mars_facts['martian_data']['mars_facts'],    
        title_0 = martian_hemisphere_list[0]['title'],
        img_url_0 = martian_hemisphere_list[0]['img_url'],
        title_1 = martian_hemisphere_list[1]['title'],
        img_url_1 = martian_hemisphere_list[1]['img_url'],
        title_2 = martian_hemisphere_list[2]['title'],
        img_url_2 = martian_hemisphere_list[2]['img_url'],
        title_3 = martian_hemisphere_list[3]['title'],
        img_url_3 = martian_hemisphere_list[3]['img_url'])


if __name__ == "__main__":
    app.run(debug=True)
