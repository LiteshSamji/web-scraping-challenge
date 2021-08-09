#Import Dependancies 
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import time
from webdriver_manager.chrome import ChromeDriverManager
 





def scrape():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # URL of page to be scraped
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    time.sleep(1)

    #using bs to write it into html
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    news_title = soup.find("div",class_="content_title").text
    news_p = soup.find("div", class_="article_teaser_body").text
    print(f"Title: {news_title}")
    print(f"Paragraph: {news_p}")

    # # Mars Space Images

    # URL of page to be scraped
    fullimage_url = 'https://spaceimages-mars.com/'
    browser.visit(fullimage_url)

    #using bs to write it into html
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    button = browser.links.find_by_partial_text('FULL IMAGE')
    button.click()

    link=soup.find('img', class_='headerimage fade-in')['src']
    featured_image_url=fullimage_url+link
    print(featured_image_url)
                                                 
    # # Mars Facts

    # URL of page to be scraped
    marsfacts_url = 'https://galaxyfacts-mars.com/'
    browser.visit(marsfacts_url)

    tables = pd.read_html(marsfacts_url)
    tables

    marsdf = tables[0]
    marsdf.columns = ["Description", "Mars", "Earth"]
    marsdf.set_index('Description', inplace=True)
    marsdf.head()

    #Remove the the first line 
    marsdf[1:].reset_index()

    #Generate HTML tables from df
    html_table = marsdf.to_html()
    html_table

    #Save as html file
    marsdf.to_html('mars_table.html')

    # # Mars Hemispheres

    # URL of page to be scraped
    mars_hemisphere_url = 'https://marshemispheres.com/'
    browser.visit(mars_hemisphere_url)


    hemisphere_image_urls = []

    # Get a List of All the Hemispheres
    links = browser.find_by_css("a.product-item img")

    for item in range(len(links)):
        hemisphere = {}
    
        # Find Element on Each Loop to Avoid a Stale Element Exception
        browser.find_by_css('a.product-item img')[item].click()
        
        # Find Sample Image Anchor Tag & Extract <href>
        sample_element = browser.find_link_by_text("Sample").first
        hemisphere["img_url"] = sample_element["href"]
        
        # Get Hemisphere Title
        hemisphere["title"] = browser.find_by_css("h2.title").text
        
        # Append Hemisphere Object to List
        hemisphere_image_urls.append(hemisphere)
        
        # Navigate Backwards
        browser.back()
        hemisphere_image_urls

    #Create dictionary for all the information scraped from the sources
    mars_dict = {
        "news_title":news_title,
        "news_p":news_p,
        "featured_image_url":featured_image_url,
        "html_table":html_table,
       "image_urls":hemisphere_image_urls
    }
    # Close the browser after scraping
    browser.quit()
    # Return results
    return mars_dict    




