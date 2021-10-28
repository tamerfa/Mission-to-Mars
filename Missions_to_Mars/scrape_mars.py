# Importing dependencies
from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd

def scrape():
    # Initiate browser
    executable_path = {'executable_path':ChromeDriverManager().install()}
    browser = Browser('chrome',**executable_path, headless=False)

    # Defining a dictionary to collect all scraped data
    mars_dict = {} 

    # Scraping 'Nasa Mars News' site
    nasa_url = 'https://redplanetscience.com/'
    browser.visit(nasa_url)

    html = browser.html
    soup = bs(html, 'html.parser')

    news_title = soup.find('div', class_= 'content_title').text
    news_p = soup.find('div', class_= 'article_teaser_body').text

    # Adding 'Nasa Mars News' data to mars_dict
    mars_dict['news_title'] = news_title
    mars_dict['news_p'] = news_p


    # Scraping 'JPL Mars Space Images' featured image
    jpl_url = 'https://spaceimages-mars.com/'
    browser.visit(jpl_url)

    html = browser.html
    soup = bs(html, 'html.parser')

    featured_image = soup.find('img', class_= 'headerimage')
    relative_image_url = featured_image['src']
    featured_image_url = jpl_url+relative_image_url

    # Adding JPL's 'featured_image_url' data to mars_dict
    mars_dict['featured_image_url'] = featured_image_url


    # Scraping 'Mars Facts' using pandas
    facts_url = 'https://galaxyfacts-mars.com/'

    tables_list = pd.read_html(facts_url)

    # Required table is the first table in the list
    table_df = tables_list[0]

    table_df.columns = ['Description', 'Mars', 'Earth']
    table_df.set_index('Description', inplace=True)

    # Adding 'Mars facts' dataframe (table_df) to mars_dict
    mars_dict['facts'] = table_df

    # Save the table to an html file
    table_df.to_html('mars_facts.html')


    # Scraping 'Mars Hemispheres'
    hem_url = 'https://marshemispheres.com/'
    browser.visit(hem_url)

    html = browser.html
    soup = bs(html, 'html.parser')

    # Getting a list for the links to be clicked
    clickables = soup.find_all('a', class_='itemLink product-item')

    # clickables contain duplicate links, keep only the ones that contain text
    links = []
    for link in clickables:
        if link.text:
            links.append(link)
        
    # Delete unneeded last element of links
    links.pop()

    # Defining a list to collect data
    hemisphere_image_urls = []

    for link in links:
        hem_dict = {}
        link_text = link.find('h3').text
        hem_dict['title'] = link_text
        #Click to visit the image page
        browser.links.find_by_partial_text(link_text).click()
        time.sleep(1)
        html = browser.html
        soup = bs(html, 'html.parser')
        img_section = soup.find('div', class_='downloads')
        
        # Specify base url to add to each image's relative url
        base_url = "https://marshemispheres.com/"
        hem_dict['img_url'] = base_url+img_section.find('a', text='Original')['href']
        hemisphere_image_urls.append(hem_dict)
        # Going back to the previous page
        browser.back()
        time.sleep(1)

    # Adding 'Mars hemishperes' data to mars_dict
    mars_dict['hemishperes'] = hemisphere_image_urls

    browser.quit()

    return mars_dict