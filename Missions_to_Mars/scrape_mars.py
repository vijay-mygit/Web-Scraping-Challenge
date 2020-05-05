# Importing all the Dependencies.
from bs4 import BeautifulSoup
import pandas as pd
import requests
from splinter import Browser
import time

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    #executable_path = {'executable_path': 'C:/Users/vijay/OneDrive/Documents/GitHub/Web-Scraping-Challenge/Missions_to_Mars/chromedriver.exe'}
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    browser = init_browser()
    
    # NASA Mars News
    # 
    # Scrape the NASA Mars News Site and collect the latest News Title and Paragraph Text.     
    url_mars_news = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url_mars_news)
    time.sleep(2)
    response = browser.html
    soup = BeautifulSoup(response, 'html.parser')
    # Assign the text to variables that you can reference later.
    news_title = soup.find_all('div',class_="content_title")[1].text
    # Collecting the paragraph text.
    news_p = soup.find('div',class_="article_teaser_body").text

    # JPL Mars Space Images - Featured Image    
    # Visit the url for JPL Featured Space Image.
    image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    # Use splinter to navigate the site and find the image url for the current Featured Mars Image and assign
    # the url string to a variable called featured_image_url.
    browser.visit(image_url)
    time.sleep(2)
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(1)
    browser.click_link_by_partial_text('more info')
    time.sleep(1)
    # Make sure to find the image url to the full size .jpg image.
    browser.click_link_by_partial_href('/spaceimages/images/largesize')
    time.sleep(1)
    # Make sure to save a complete url string for this image.
    featured_image_url = browser.find_by_tag('img')['src']

    # Mars Weather
    # Visit the Mars Weather twitter account and scrape the latest Mars weather tweet from the page. 
    url_twitter = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url_twitter)
    time.sleep(3)
    response_1 = browser.html
    soup = BeautifulSoup(response_1,'html.parser')
    time.sleep(5)
    # Save the tweet text for the weather report as a variable called mars_weather.
    last_tweets = soup.find_all('div', class_="css-901oao r-hkyrab r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0")
    for tweet in last_tweets:
        one_tweet = tweet.find('span').text
        weather_tweet = one_tweet.startswith('InSight')
        if (weather_tweet==True):
            mars_weather = one_tweet
            break
    
    # Mars Facts
    # Visit the Mars Facts webpage and use Pandas to scrape the table containing facts about the planet 
    # including Diameter, Mass, etc. 
    url_facts = 'https://space-facts.com/mars/'
    browser.visit(url_facts)
    time.sleep(1)
    # Use Pandas to convert the data to a HTML table string.
    tables = pd.read_html(url_facts)
    table = tables[0]
    table.columns = ['Parameters','Values']
    mars_table = table.set_index('Parameters',inplace=True)
    mars_table = table.to_html()
    #mars_table.replace('\n', '')
    table.to_html('mars_table.html')

    # Mars Hemispheres
    # Visit the USGS Astrogeology site to obtain high resolution images for each of Mar's hemispheres.
    url_hemi = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url_hemi)
    time.sleep(2)
    response_2 = browser.html
    soup = BeautifulSoup(response_2,'html.parser')
    results = soup.find_all('div',class_='item')
    # Save both the image url string for the full resolution hemisphere image, and the Hemisphere title 
    # containing the hemisphere name. Use a Python dictionary to store the data using the keys img_url and title.
    img_url = []
    title = []
    # You will need to click each of the links to the hemispheres in order to find the image url to the full resolution image.
    for result in results:
        # using splinter to navigate to the full resolution image
        parent_window = browser.driver.current_window_handle
        title.append(result.h3.text)
        browser.click_link_by_partial_text(result.h3.text)
        time.sleep(1)
        browser.click_link_by_partial_text('Sample')
        # Assigning window names parent window is main window and any new tab opened is child window.
        all_windows = browser.driver.window_handles
        time.sleep(1)
        child_window = [window for window in all_windows if window != parent_window][0]
        # Switching the splinter to operate on the child window which contains the link for the image.
        browser.driver.switch_to.window(child_window)
        # Collecting the image url.
        img_url.append(browser.find_by_tag('img')['src'])
        # Closing the child window
        browser.driver.close()
        # Switching the splinter back to operate the parent window.
        browser.driver.switch_to.window(parent_window)
        browser.back()
    hemisphere_image_urls = []
    # Append the dictionary with the image url string and the hemisphere title to a list. 
    # This list will contain one dictionary for each hemisphere.
    for i in range(0,4):
        hemisphere_image_urls.append({"title":title[i],"image_url":img_url[i]})
    
    # One Python dictionary containing all of the scraped data.
    mars_data = {
        "news_title":news_title,
        "news_p" : news_p,
        "featured_image_url" : featured_image_url,
        "mars_weather" : mars_weather,
        "mars_table" : mars_table,
        "hemisphere_image_urls" : hemisphere_image_urls
    }

    # Close the browser after scraping
    browser.quit()
    # Return Results
    return mars_data

