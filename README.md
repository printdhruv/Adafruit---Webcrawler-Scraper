### Adafruit.com web_crawling and scraping
#### This app crawl and scrap a website http://www.adafruit.com/categories written in the flask framework with sqlite3 as a database.
#### Front-end has been enhanced with materialize CSS and js library with a few other apis such as Top Seller, Out Of Stock, Common items
#### with a custom SQL query box.
##### The backend logic @('/') default option invoked when download button is clicked. The python 3 code crawl 35 various categories
##### and scrap all links with beautifulsoup4 and requests packages.
##### The data of each product is feed into the following table schema defined in sqlite3.
#####  ______________________________________________________
##### | Category | ID | Name | Price | Quantity | Stock |
##### -------------------------------------------------------
##### There are ~ 4200 accurate records were fetched and stored into product-data.db sqlite3 database.
