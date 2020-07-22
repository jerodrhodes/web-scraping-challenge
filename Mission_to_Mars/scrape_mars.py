# import dependencies
from bs4 import BeautifulSoup as bs
from splinter import Browser
import os
import pandas as pd
import time
import re

def init_browser():
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()
    mars_data = {}

    # visiting the page
    nasa_url = "https://mars.nasa.gov/news/"
    browser.visit(nasa_url)
    time.sleep(12)

    html = browser.html
    soup = bs(html, 'html.parser')

    #scrape news from nasa
    class_title = soup.find("div",class_="list_text")
    news_title = class_title.find('a').text.strip()
    news_para = soup.find("div", class_="article_teaser_body").text

    mars_data['news_title'] = news_title
    mars_data['news_para'] = news_para

    #featured image from nasa
    image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(image_url)

    html_img = browser.html
    soup_img = bs(html_img, "html.parser")

    # scrape the featured image
    image_url = soup_img.find('div',class_='carousel_container').article.footer.a['data-fancybox-href']
    featured_image_url = f'https://www.jpl.nasa.gov{image_url}'

    mars_data['featured_image'] = featured_image_url

    # Mars weather Tweet
    # visit the Mars weather twitter page
    weather_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(weather_url)

    #get mars weather's latest tweet from the website
    weather_html = browser.html
    weather_soup = bs(weather_html, 'html.parser')
    mars_weather = weather_soup.find('span', text=re.compile("InSight")).text.strip()

    mars_data['mars_weather'] = mars_weather

    # Mars facts table
    facts_url = "https://space-facts.com/mars/"
    browser.visit(facts_url)
    mars_data = pd.read_html(facts_url)
    mars_data = pd.DataFrame(mars_data[0])
    mars_facts = mars_data.to_html(header = False, index = False)

    mars_data['mars_facts_table'] = mars_facts

    # Mars Hemispheres from USGS
    mars_hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    hemi_dicts = []

    for i in range(1,9,2):
        hemi_dict = {}
    
        browser.visit(mars_hemisphere_url)
        time.sleep(1)
        hemispheres_html = browser.html
        hemispheres_soup = bs(hemispheres_html, 'html.parser')
        hemi_name_links = hemispheres_soup.find_all('a', class_='product-item')
        hemi_name = hemi_name_links[i].text.strip('Enhanced')
    
        detail_links = browser.find_by_css('a.product-item')
        detail_links[i].click()
        time.sleep(1)
        browser.find_link_by_text('Sample').first.click()
        time.sleep(1)
        browser.windows.current = browser.windows[-1]
        hemi_img_html = browser.html
        browser.windows.current = browser.windows[0]
        browser.windows[-1].close()
    
        hemi_img_soup = bs(hemi_img_html, 'html.parser')
        hemi_img_path = hemi_img_soup.find('img')['src']

        hemi_dict['title'] = hemi_name.strip()
        hemi_dict['img_url'] = hemi_img_path

        hemi_dicts.append(hemi_dict)
    
    mars_data['hemisphere_imgs'] = hemi_dicts

    browser.quit()

    return mars_data