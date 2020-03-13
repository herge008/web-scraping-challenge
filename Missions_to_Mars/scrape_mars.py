#Scrape Mars Python file

import pandas as pd
import time as time
from splinter import Browser
from bs4 import BeautifulSoup
from pprint import pprint
import requests

executable_path = {"executable_path": "browser_driver/chromedriver.exe"}
browser = Browser("chrome", **executable_path, headless=True)

def scraper():
    #==================================================================================================
    # HEADLINES
    #==================================================================================================

    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)
    page = browser.html
    soup = BeautifulSoup(page, "lxml")

    time.sleep(5)
    for _ in range(10):
        try:
            first_headline = soup.find("div", class_="image_and_description_container")
            first_headline_title = first_headline.find("div", class_="content_title").text
            first_headline_title

            first_headline_teaser = first_headline.find("div", class_="article_teaser_body").text
            first_headline_teaser
        except:
            print("process did not complete successfully")
        else:
            break

    #==================================================================================================
    # FEATURED IMAGE
    #==================================================================================================
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    browser.click_link_by_partial_text('FULL IMAGE')
    browser.click_link_by_partial_text('more info')
    browser.find_by_css('.main_image').click()
    featured_image_url = browser.url
    featured_image_url

    #==================================================================================================
    # WEATHER
    #==================================================================================================
    twitter_url = "https://twitter.com/marswxreport?lang=en"
    response = requests.get(twitter_url)
    twitter_soup = BeautifulSoup(response.text, "lxml")

    for tweet in range(100):
        mars_weather = twitter_soup.find_all('p',class_="js-tweet-text")[tweet].text.split("pic")[0]
        if "InSight sol" in mars_weather:
            break

    mars_weather = mars_weather.split("InSight ")[-1]
    mars_weather

    #==================================================================================================
    # FACTS
    #==================================================================================================

    facts_url = "https://space-facts.com/mars/"
    table = pd.read_html(facts_url)[0]
    table = table.rename(columns={0: "Description", 1: "Value"})
    table.set_index("Description", inplace=True)
    mars_facts_table = table.to_html()

    #==================================================================================================
    # HEMISPHERES
    #==================================================================================================

    hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemispheres_url)

    hemisphere_image_urls = []
    for click_count in range(4):
        page = browser.find_link_by_partial_text('Hemisphere Enhanced')[click_count]
        page.click()
        img_title = browser.find_by_css('.title').first.text
        img_url = browser.find_by_text('Sample').first["href"]
        
        #Store variables in a holding dictionary (need to go back before adding to hemisphere_image_urls)
        holding_dict = {"title": img_title, "img_url": img_url}
        browser.back()
        
        hemisphere_image_urls.append(holding_dict)

    #==================================================================================================
    # VARIABLES RETURNED 
    #==================================================================================================
    return({
        "first_headline_title": first_headline_title,
        "first_headline_teaser": first_headline_teaser,
        "featured_image_url": featured_image_url,
        "mars_weather": mars_weather,
        "mars_facts_table": mars_facts_table,
        "hemisphere_image_urls": hemisphere_image_urls
    })