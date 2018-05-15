
# coding: utf-8

# # Mission to Mars

# ## Scraping

# In[1]:


# Dependencies
from bs4 import BeautifulSoup
import requests
import pymongo
from splinter import Browser
import pandas as pd
import time


# ### NASA Mars News

# In[2]:


# Get a Chrome browser for the website.
executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=True)


# In[3]:


# URL of page to be scraped
url = 'https://mars.nasa.gov/news/'


# In[4]:


# Open the website with the browser.
browser.visit(url)
time.sleep(5)


# In[5]:


# Retrieve the HTML code for the displayed web page.
html = browser.html


# In[6]:


# Parse the web page.
soup = BeautifulSoup(html, 'html.parser')


# In[7]:


# Get the title of the first news article.
results = soup.find('div', class_='content_title')


# In[8]:


# Store the title of the first news article.
news_title = results.text.strip()


# In[9]:


# Get the teaser text for the first news article.
results = soup.find('div', class_='article_teaser_body')


# In[10]:


# Store the teaser text for the first news article
news_p = results.text.strip()


# In[11]:


# Check the title and text.
print(news_title)
print(news_p)


# ### JPL Mars Space Images - Featured Image

# In[12]:


# Get a Chrome browser for the website.
executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=True)


# In[13]:


# The start page for the featured Mars image at JPL. 
url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'


# In[14]:


# Open the website with the browser.
browser.visit(url)
time.sleep(5)


# In[15]:


browser.click_link_by_partial_text('FULL IMAGE')
time.sleep(5)


# In[16]:


# Retrieve the HTML code for the displayed web page.
html = browser.html


# In[17]:


# Parse the web page.
soup = BeautifulSoup(html, 'html.parser')


# In[18]:


# Get the image on the web page.
results = soup.find('img', class_='fancybox-image')
# results = soup.find('img')


# In[19]:


print(results)


# In[20]:


# Concatenate the website with the src attribute of the img tag.
featured_image_url = 'https://www.jpl.nasa.gov' + results['src']


# In[21]:


# Print featured_image_url.
print(featured_image_url)


# ### Mars Weather

# In[22]:


# Get a Chrome browser for the website.
executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=True)


# In[23]:


# The weather page.
url = 'https://twitter.com/marswxreport?lang=en'


# In[24]:


# Open the website with the browser.
browser.visit(url)
time.sleep(5)


# In[25]:


# Retrieve the HTML code for the displayed web page.
html = browser.html


# In[26]:


# Parse the web page.
soup = BeautifulSoup(html, 'html.parser')


# In[27]:


results = soup.find_all('p')


# In[28]:


for result in results:
    rt = result.text
    if rt.find('Sol') > -1:
        if rt.find('high') > -1:
            if rt.find('low') > -1:
                if rt.find('pressure at') > -1:
                    mars_weather = rt
                    break


# In[29]:


print(mars_weather)


# ### Mars Facts

# In[30]:


# Get a Chrome browser for the website.
executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=True)


# In[31]:


# The facts page.
url = 'https://space-facts.com/mars/'


# In[32]:


dfs = pd.read_html(url)
time.sleep(5)


# In[33]:


df = None
for df_entry in dfs:
    df = df_entry
df = df.rename(columns={0:"Fact", 1:"Value"})
df.set_index('Fact', inplace=True)
print(df)


# In[34]:


fact_table = df.to_html()


# In[35]:


print(fact_table)


# ### Mars Hemispheres

# In[36]:


hemisphere_image_urls = [
    {"title":"Cerberus Hemisphere", 
     "img_url":"https://astrogeology.usgs.gov/cache/images/cfa62af2557222a02478f1fcd781d445_cerberus_enhanced.tif_full.jpg"},
    {"title":"Schiaparelli Hemisphere", 
     "img_url":"https://astrogeology.usgs.gov/cache/images/3cdd1cbf5e0813bba925c9030d13b62e_schiaparelli_enhanced.tif_full.jpg"},
    {"title":"Syrtis Major Hemisphere", 
     "img_url":"https://astrogeology.usgs.gov/cache/images/ae209b4e408bb6c3e67b6af38168cf28_syrtis_major_enhanced.tif_full.jpg"},
    {"title":"Valles Marinefis Hemisphere", 
     "img_url":"https://astrogeology.usgs.gov/cache/images/7cf2da4bf549ed01c17f206327be4db7_valles_marineris_enhanced.tif_full.jpg"}
]


# ## MongoDB

# ### News Title and Paragraph

# In[37]:


# Initialize PyMongo to work with MongoDBs
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)


# In[38]:


client.drop_database('mars_db')


# In[39]:


# Define database and collection
db = client.mars_db
collection = db.items


# In[40]:


martian_datum = {
        "martian_key":"news",
        "martian_data":
        {
            "news_title":news_title, 
            "news_p":news_p
        }
    }

collection.insert_one(martian_datum)


# In[41]:


# Display items in MongoDB collection
martian_news = db.items.find_one({"martian_key":"news"})
print(martian_news['martian_data']['news_title'])
print(martian_news['martian_data']['news_p'])


# ### Featured Image URL

# In[42]:


martian_datum = {
        "martian_key":"featured_image_url",
        "martian_data":
        {
            "featured_image_url":featured_image_url
        }
    }

collection.insert_one(martian_datum)


# In[43]:


# Display items in MongoDB collection
martian_featured_image_url = db.items.find_one({"martian_key":"featured_image_url"})
print(martian_featured_image_url['martian_data']['featured_image_url'])


# ### Mars Weather

# In[44]:


martian_datum = {
        "martian_key":"mars_weather",
        "martian_data":
        {
            "mars_weather":mars_weather
        }
    }

collection.insert_one(martian_datum)


# In[45]:


# Display items in MongoDB collection
martian_mars_weather = db.items.find_one({"martian_key":"mars_weather"})
print(martian_mars_weather['martian_data']['mars_weather'])


# ### Mars Facts

# In[46]:


martian_datum = {
        "martian_key":"mars_facts",
        "martian_data":
        {
            "mars_facts":fact_table
        }
    }

collection.insert_one(martian_datum)


# In[47]:


# Display items in MongoDB collection
martian_mars_facts = db.items.find_one({"martian_key":"mars_facts"})
print(martian_mars_facts['martian_data']['mars_facts'])


# ### Mars Hemispheres

# In[48]:


martian_datum = {
        "martian_key":"hemisphere_image_urls",
        "martian_data":
        {
            "hemisphere_image_urls":hemisphere_image_urls
        }
    }

collection.insert_one(martian_datum)


# In[49]:


# Display items in MongoDB collection
martian_hemispheres = db.items.find_one({"martian_key":"hemisphere_image_urls"})
martian_hemisphere_list = martian_hemispheres['martian_data']['hemisphere_image_urls']
for martian_hemisphere_entry in martian_hemisphere_list:
    print(martian_hemisphere_entry['title'])
    print(martian_hemisphere_entry['img_url'])
    print(" ")


# ## Ready 

# In[50]:


print("****************")
print("* READY")
print("****************")

