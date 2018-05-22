from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import time

###initiate browser so that it can be used 
def init_browser():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser('chrome', **executable_path, headless=False)




def scrape():
    browser = init_browser()
    ####final form going to mongo db
    mars_data={}
    #########################################get featured image    
    #  # Visit NSA image site
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    time.sleep(2)

    # Find and click the full image button
    full_image_elem = browser.find_by_id('full_image')
    full_image_elem.click()
    time.sleep(2)
    # Find the more info button and click that
    more_info_elem = browser.find_link_by_partial_text('more info')
    more_info_elem.click()
    time.sleep(2)
    # Parse the resulting html with soup
    html = browser.html
    img_soup = BeautifulSoup(html, 'html.parser')
     # find the relative image url
    img_link = img_soup.find('figure', class_='lede').find('img')['src']
    #total link not partial so html can point to it in template code
    #this code contains the proper link for image url
    img_url = f'https://www.jpl.nasa.gov{img_link}'

    #put into database
    mars_data["featured_image"] = img_url
    ######################################################################
    # get most recent weather data 
    url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url)
    html = browser.html
    #get the data using beautiful soup
    weather_soup = BeautifulSoup(html, 'html.parser')
    #grab the appropriate weather data from container within container 
    #weather_find contains most recent weather data
    weather_find=weather_soup.find("div", class_="js-tweet-text-container").find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").get_text()
    #put into database
    mars_data["weather"]= weather_find
    
    ##################################################################
    #get hemisphere data 
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    #make a list for the image links to use later
    hemisphere_image_links = []
    # all links lie in h3 of css
    links = browser.find_by_css("h3")
    #loop through all the links 
    for i in range(len(links)):
        hemispheres = {}
    
      # get overall string
        browser.find_by_css("h3")[i].click()
    
    #rip out the and make the link for dictionary
        sample_elem = browser.find_link_by_text('Sample').first
        hemispheres['img_link'] = sample_elem['href']
    
    #get titles and apply to dictionary
        hemispheres['title'] = browser.find_by_css("h2.title").text
    
    # throw the dictionary into the hemesphere image links list 
        hemisphere_image_links.append(hemispheres)
        print(hemispheres)
    # browser has to go to previous page
        browser.back()
    
    mars_data["hemispheres"]= hemisphere_image_links
    # rip out table facts_df has been changed to html 
    facts_df = pd.read_html('http://space-facts.com/mars/')[0]
    facts_df.columns=['description', 'value']
    facts_df.set_index('description', inplace=True)
    facts_table=facts_df.to_html()
    table = facts_table.replace('\n', '')
    #put facts table into database
    mars_data['facts'] = table
#turn off browser
    browser.quit()
#return the data 
    return mars_data




