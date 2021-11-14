# Mission-to-Mars
Web Scraping Project with Python, MongoDB, Flask, CSS and HTML
This project scrapes another website for information, data tables, and image links.  This scraped data is pushed to a mongo database and then pulled back out for rendering on a local machine hosted flask website.  A button is shown on this locally hosted website which provides an action to refresh the data scrape.

## Three core files are used for this project
* app.py 
* index.html
* scraping.py

### app.py purpose
* sets up flask route such that visitation to the root page pulls mongo db data
* sets up flask route /scrape which kicks off the file scraping.py and updates the mongo database

### index.html purpose
* uses bootstrap for formating and also retrieves data from mongo db in an html format

### scraping.py
* leverages splinter, ChromeDriverManager, beautiful soup, and pandas libraries to navigate the webpages and return a data dictionary


### Operation 
Open an Anaconda prompt for your python environment which has above libraries installed.  Navigate to your project folder containing the above files and then use the command mongod to kickoff the mongo services.  Open another Anaconda prompt and navigate to the folder containing the above files and type python app.py to kickoff flask.  This command window will return the web address to paste into your browswer to see the webpage.  This webpage will contain the scraped data displayed using CSS and html styling by leveraging bootstrap.

![alt text](https://github.com/jj2773/Mission-to-Mars/blob/main/websiteimage1.PNG)



![alt text](https://github.com/jj2773/Mission-to-Mars/blob/main/websiteimage2.PNG)