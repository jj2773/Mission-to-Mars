# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'

# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager

# Set the executable path and initialize Splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# ### Visit the NASA Mars News Site
# Visit the mars nasa news site
url = 'https://redplanetscience.com/'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)

# Convert the browser html to a soup object and then quit the browser
html = browser.html
news_soup = soup(html, 'html.parser')

slide_elem = news_soup.select_one('div.list_text')

slide_elem.find('div', class_='content_title')

# Use the parent element to find the first a tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title

# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p

# ### JPL Space Images Featured Image
# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)

# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()

# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')
img_soup

# find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel

# Use the base url to create an absolute url
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url

# ### Mars Facts
df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.head()

df.columns=['Description', 'Mars', 'Earth']
df.set_index('Description', inplace=True)
df

df.to_html()

# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles
# ### Hemispheres

# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'

browser.visit(url)


# 2. Create a list to hold the images and titles.
image_list=[]
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
        if dictionary not in image_list:
            image_list.append(dictionary)

        #return to the main map to 
        url = 'https://marshemispheres.com/'
        browser.visit(url)
    except:
        print('error')



image_list

# 5. Quit the browser
browser.quit()


