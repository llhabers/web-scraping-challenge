# Dependencies
from bs4 import BeautifulSoup
import requests
import pymongo
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
from flask import Flask, render_template, redirect
import pandas as pd

# Define Internet Browser and Scrape functions
def internet_browser():
    executable_path = {'executable_path': 'chromedriver'}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    browser = internet_browser()
    mars_facts_dict = {}
    
    ## NASA Mars News

    # URL of page to be scraped
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html,'html.parser')

    # Retrieve the latest news title
    news_title = soup.find_all('div', class_='content_title')[0].text

    # Retrieve the latest news paragraph
    news_paragraph = soup.find_all('div', class_='rollover_description_inner')[0].text

    print(f"The latest News Title and Paragraph Text from Nasa's Mars Exploration website is {news_title} {news_paragraph}")
        
    ## JPL Mars Space Images - Featured Image

    jpl_url = 'https://www.jpl.nasa.gov/images?search=&category=Mars'
    browser.visit(jpl_url)

    for x in range(1, 2):
    
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        imgs = soup.find_all('div', class_='SearchResultCard')[0]

    # Use Beautiful Soup's find() method to navigate and retrieve attributes
        for img in imgs:
            link = imgs.find('a')
            href = link['href']
            print('-----------')
            print(img.text)
            print('https://www.jpl.nasa.gov' + href)    
    
    featured_image_url = 'https://www.jpl.nasa.gov/images/great-anticipation-as-perseverance-lands'
    
    ## Mars Fact

    # Scrape Mars facts from https://space-facts.com/mars/
    mars_facts_url = 'https://space-facts.com/mars/'
    browser.visit(mars_facts_url)
    
    mars_fact = pd.read_html(mars_facts_url)
    
    #Find Mars Facts DataFrame in the lists of DataFrames
    mars_facts = mars_fact[0]
    # mars_facts

    #Assign the columns
    mars_facts.columns = ['Description', 'Value']
    # mars_facts

    print(mars_facts)
    
    ## Mars Hemispheres

    # Scrape Mars hemisphere title and image
    # Scrape Mars hemispheres titles and images
    mh_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    mh_img_url = 'https://astrogeology.usgs.gov'

    browser.visit(mh_url)

    # Extract hemispheres item elements. This will help with scraping the correct items you need.
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    mars_hemis = soup.find('div',class_='collapsible results')
    mars_items = mars_hemis.find_all('div',class_='item')

    #EXTRACTION
    mars_hemi_img_url = []

    for items in mars_items:
        # Extract title
        hemi = items.find('div',class_='description')
        title = hemi.h3.text
        
        # Extract image url
        hemi_url = hemi.a['href']
        browser.visit(mh_img_url + hemi_url)
        html = browser.html
        soup = BeautifulSoup(html,'html.parser')
        image_src = soup.find('li').a['href']
        
        if (title and image_src):
            # Print results
            print('-'*50)
            print(title)
            print(image_src)
        # Create dictionary for title and url
        hemi_dict={
            'title':title,
            'image_url':image_src
        }
        mars_hemi_img_url.append(hemi_dict)

    # Create dictionary for all info scraped from sources above to support your data in Mongo
    mars_facts_dict = {
        "news_title":news_title,
        "news_paragraph":news_paragraph,
        "featured_image_url":featured_image_url,
        "mars_fact_table":mars_facts,
        "hemisphere_images":mars_hemi_img_url
    }
    # Close the browser after scraping
    browser.quit()
    return mars_facts_dict