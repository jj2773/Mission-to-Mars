from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt


def scrape_all():
    # Set up Splinter
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)
    news_title, news_paragraph = mars_news(browser)
    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemispheres": scrape_hemi(browser)    
    }

    return data


def mars_news(browser):
    # Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)
    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    html = browser.html
    news_soup = soup(html, 'html.parser')
    try:
        slide_elem = news_soup.select_one('div.list_text')
        # Scrape the Title
        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()

        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    except AttributeError:
        return None, None
    
    return news_title, news_p

# ### Featured Images

def featured_image(browser):
    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)


    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()


    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
       
        # Use the base URL to create an absolute URL
        img_url = f'https://spaceimages-mars.com/{img_url_rel}'
               
    except AttributeError:
        return None
    
    return img_url

def mars_facts():
    try: 
    # use read_html to scrape the facts table into a dataframe
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    except BaseException:
        return None
    
    #assign columns and an index to the dataframe
    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)
    
    #conver the dataframe to html format, add bootstrap
    return df.to_html(classes=["table-bordered", "table-striped", "table-hover"])
   

def scrape_hemi(browser):
    # # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles
    # ### Hemispheres

    # 1. Use browser to visit the URL 
    url = 'https://marshemispheres.com/'

    browser.visit(url)


    # 2. Create a list to hold the images and titles.
    hemispheres=[]
    # 3. Write code to retrieve the image urls and titles for each hemisphere.
    html = browser.html
    img_soup = soup(html, 'html.parser')
    #parse html on the images page https://marshemispheres.com/ into img_soup make a list items that has the link URL to the higher res images and titles
    items=img_soup.findAll('a', class_='itemLink product-item')

    dictionary={}

    #loop through this items list to leave the main page go to the high res page get images and titles then back
    for item in items:
        try:  
            #get path to high res photo 
            full_image_page_url =url+ item.get('href')
            
            #browse to the site
            browser.visit(full_image_page_url)
            html = browser.html
            #parse into img_soup to enable finding title and high res link
            img_soup = soup(html, 'html.parser')
            hemisphere_image_url='https://marshemispheres.com/' + img_soup.find('img', class_='wide-image').get('src')
            title=img_soup.find('h2',class_='title').get_text()
            
            #create dictionary 
            dictionary={'img_url':hemisphere_image_url, 'title':title}
            
            #make a list of dictionary URLs and titles found.
            if dictionary not in hemispheres:
                hemispheres.append(dictionary)

            #return to the main map to 
            url = 'https://marshemispheres.com/'
            browser.visit(url)
        except BaseException:
            return hemispheres
    return hemispheres