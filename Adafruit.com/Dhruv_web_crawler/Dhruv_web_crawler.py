# -*- coding: utf-8 , Styling: PEP 8 -*-
""" Coding Task
Build a web crawler service (RESTful APIs) to find the best sellers products in 
website https://www.adafruit.com/categories and expose these best sellers data in RESTful APIs. 
It will be better if you can add more useful APIs like the result-filter APIs. You can use any
tech stack you want to make it happen.

    Definitions:-
                * Programmer : Dhruv Patel
                * Email      : 669.294.6970
                * This program serves as the attempt to solve the coding task to scrap and crawl adafruit.com/categories
                  I am a programmer of this code it can be used/evaluated in full or partial without my notice of concern.
    
    Logic Flow:-  
                * The crawler fetches the master url "https://www.adafruit.com/categories" and get 35 links of various
                  categories into list. After completing that step it iterate through the list and scrap the data from 
                  the websites and store into created TABLE SCHEMA in the sqlite3.
                * We will try to explore each and every details in depth scoped into the function.
                * IDE        : IntelliJ IDEA
                * Technology : Flask with Jinja-2 template, Python-3, materialize js, materialize css, 
                               sqlite3(database)
                * Dependency : beautifulsoup4, flask, click, jinja2, pip, urllib3, werkzeug, requests, markupsafe, 
                               itsdangerous, Regular Expression
    """
import re
import sqlite3
import time

import requests as request
from bs4 import BeautifulSoup as soup
from flask import Flask, render_template
from flask import request as flask_request

"""
    The idea of the first parameter is to give Flask an idea of what belongs to your application. 
    This name is used to find resources on the filesystem, can be used by extensions to improve debugging information 
    and a lot more.
    So it’s important what you provide there. 
    If you are using a single module, __name__ is always the correct value. 
"""

app = Flask(__name__)

"""
   This '/' is default route. Flask deals with trailing slashes
   '@' is defined as decorator which map the relationship between front-end actions towards 
   each function body.It also takes parameters of methods names of 'GET' or 'POST'
   Underneath it, there is a definition of a function which returns render_template function which does following :-
        * if no arguments are passed, it creates a new response argument
        * if one argument is passed, flask.Flask.make_response() is invoked with it.
        * if more than one argument is passed, the arguments are passed to the flask.Flask.make_response() 
          function as tuple.
   In our code we have used all flavors mentioned above.     
"""


@app.route('/', methods=['POST', 'GET'])
def out():
    return render_template('index.html')


"""
    Here,we are mapping download button to the fetch_data function.
"""


@app.route('/download', methods=['POST', 'GET'])
def fetch_data():
    """
        :argument
            No parameters it's taking but we can map user's input of master_url with "param(string)"
            As,in our case link is unique and not changing thus we keep initialized after function in invoked
            with variable "master_url"
    
        :return: 
            render_template function with the index.html argument  
    """
    start = time.time()
    connection = sqlite3.connect('product_data.db')
    """
        This API opens a connection to the SQLite database file database. You can use ":memory:" to open a database 
        connection to a database that resides in RAM instead of on disk. If database is opened successfully, it returns 
        a connection object.When a database is accessed by multiple connections, and one of the processes modifies the 
        database, the SQLite database is locked until that transaction is committed. The timeout parameter specifies 
        how long the connection should wait for the lock to go away until raising an exception. The default for the 
        timeout parameter is 5.0 (five seconds).
        If given database name does not exist then this call will create the database. You can specify filename with 
        required path as well if you want to create database anywhere else except in current directory.
        
        :argument
             The file path of a database which in our case :
                "C:\\Users\\print\\PycharmProjects\\Dhruv_web_crawler\\product_data.db"           
    """

    master_url = 'https://www.adafruit.com/categories'

    # Main url to crawl and scrap.

    list_of_urls = []

    # List of 35 urls of various categories fetched from the master_url

    map_of_category_names = {}

    # Dictionary of 35 urls with the url as a KEY and Shopping category as a VALUE.

    cursor_reference = connection.cursor()

    """ 
        This routine creates a cursor which will be used throughout of in database programming with Python. 
        This method accepts a single optional parameter cursorClass. If supplied, this must be a custom cursor class 
        that extends sqlite3.Cursor
        cursor_reference hold the reference of connection.cursor() throughout out the program.
    """

    cursor_reference.execute('''DROP TABLE IF EXISTS ADAFRUIT''')

    """
        We remove the old instance if exist.The reason here to feed updated price and information to the table.
    """

    cursor_reference.execute('''CREATE TABLE ADAFRUIT(product_category TEXT,product_id INTEGER,product_name TEXT,product_price REAL,
    product_qty INTEGER,product_stock TEXT)''')

    """
        It creates schema of the TABLE "ADAFRUIT" with the column names as follows with the data-types:-
        ____________________________________________________________________________________________
       |product_category | product_id | product_name | product_price | product_qty | product_stock | 
        _____TEXT________|__INTEGER___|_____TEXT_____|______REAL_____|___INTEGER___|_____TEXT______|
        
    """
    response = request.get(master_url)

    """
        Requests allows you to send organic, grass-fed HTTP/1.1 requests, without the need for manual labor. 
        There's no need to manually add query strings to your URLs, or to form-encode your POST data. Keep-alive and 
        HTTP connection pooling are 100% automatic, powered by urllib3, which is embedded within Requests.
        Hence,urllib3 code is included into this requests function which turns out to be a little faster than urllib2 
        with a 70% reduced code block in our case.
    """

    page_soup = soup(response.content, "html.parser")
    prefix = "https://www.adafruit.com"

    """
        Beautiful Soup is a Python library for pulling data out of HTML and XML files. It works with your favorite 
        parser to provide idiomatic ways of navigating, searching, and modifying the parse tree. It commonly saves 
        programmers hours or days of work.
        
        :argument
            (:parameter1) - response.content 
            (:parameter2) - parser
        :return
            BeautifulSoup object named page_soup, which represents the document as a nested data structure:  
    """

    for link in page_soup.findAll('a', attrs={'href': re.compile("/category")}):
        category = link.text
        list_of_urls.append(prefix + link.get('href'))
        if category.lower() != "more":
            map_of_category_names[prefix + link.get('href')] = link.text

    """
        :argument
        
            (:parameter1) - name  - Pass in a value for name and you’ll tell Beautiful Soup to only consider tags with 
                                    certain names. Text strings will be ignored, as will tags 
                                    whose names that don’t match.
            (:parameter2) - attrs - HTML tag with re.compile() call to match the precise link also using re.compile() 
                                    and saving the resulting regular expression object for reuse is more efficient when 
                                    the expression will be used several times in a single program.
        
        :returns
             
             url with a call link.get('href) and text linked to it with a call of link.get(text)
             We are storing each into list and dictionary respectively.
         
    """

    for each in list_of_urls:
        response = request.get(each)
        page_soup = soup(response.content, "html.parser")

        """
            Using again beautiful soup4 to iterate through the fetched urls. 
        """
        product_id = 0
        product_name = ""
        product_stock = ""
        product_category = map_of_category_names.get(each)

        """
            ____________________________________________________________________________________________
           |product_category | product_id | product_name | product_price | product_qty | product_stock | 
            _______TEXT______|__INTEGER___|_____TEXT_____|_____REAL______|___INTEGER___|_____TEXT______|
        
            The variables are self explanatory with a reference to the table.We are accessing dictionary to
            fetch product_category mapped to the KEY[each(url)].
            The ordered URL will be picked and this variables are initialized with the default values every
            time and will parse it's bs4 object in the following loop.
        """

        for each_entry in page_soup.findAll("div", {"class": "product-listing-right"}):
            product = each_entry.find("a", {"class": "ec_click_product"})

            """
                :argument .findAll()
                    
                    (:parameter1) - name  - HTML 'div'
                    (:parameter2) - class - which returns only 'div' with class named "product-listing-right" from DOM
                
                :argument .find()
                    
                    (:parameter1) - name  - HTML 'div'
                    (:parameter2) - class - which map 'a' as hyperlink to the class of ec_click_product
                
                :returns
                    
                    Object stored into variable product   
            """
            if product:
                product_id = product.get('data-pid')
                product_name = soup(product.get('data-name'), "html.parser").text

                """
                    We check if the product exist if in case to verify malformed HTML file. In our case it doesnt exist
                    for master_url.
                    
                    :argument .get(attribute)
                    
                        (:parameter) - attribute - DOM attribute to fetch the text associated with it
                    
                    :argument bs4(.get(attribute,parser)).text 
                       
                        (:parameter1) - attribute - DOM attribute named 'data-name'
                        (:parameter2) - parser    - HTML parser
                        
                        The difference between first and second function is only the second one removes the <b><strong> 
                        tags from the text. While parsing records there were some records with such tags so removing 
                        them we have used this utility.
                """

            price = each_entry.find("span", {"class": ["normal-price"]})

            # It will fetch span with a class of normal-price and store into price variable.

            if price is not None:
                price_string = price.getText()  # Will fetch price text
                if "," not in price_string:
                    try:
                        product_price = float(price_string[1:])  # Will fetch the simple format prices removing '$'
                    except Exception:
                        product_price = float(re.findall(r'[-+]?\d*\.\d+|\d+', price_string)[0])
                else:
                    r = re.findall('\d', price_string)  # to handle case as i.e 2,499
                    product_price = float(''.join(r))
            else:
                product_price = 0.00  # If product has no price listed.
            red_price = each_entry.find("span", {"class": ["red-sale-price"]})
            """
                        The red price class is to used to list SALE price and strikethrough the normal price.
                        If such product has sale price than red_price block will be executed.
                        The product_price will be overridden intentionally with a case that if we require the normal 
                        price access.
            """
            if red_price is not None:
                price_string = red_price.getText()
                if "," not in price_string:
                    product_price = float(price_string[1:])
                else:
                    r = re.findall('\d', price_string)
                    product_price = float(''.join(r))

            stock = each_entry.find("div", {"class": "stock"})
            if stock:
                line = stock.getText()
                r = re.findall('\d+', line)
                if r:
                    product_qty = r[0]  # Will fetch the product_qty with regular expression
                else:
                    product_qty = 0

                if "IN STOCK" in line:
                    product_stock = "IN STOCK"
                if "OUT OF STOCK" in line:
                    product_stock = "OUT OF STOCK"
                if "DISCONTINUED" in line:
                    product_stock = "DISCONTINUED"
                if "COMING SOON" in line:
                    product_stock = "COMING SOON"

                """
                            The simple if block to fetch the stock with utility if "string" in line with the various options 
                """
            print(product_category, product_id, product_name, product_price, product_stock, product_qty)
            cursor_reference.execute(
                '''INSERT INTO ADAFRUIT(product_category, product_id, product_name, product_price, product_qty, product_stock)VALUES (?,?,?,?,?,?)''',
                (product_category, product_id, product_name, product_price, product_qty, product_stock))
            """
                        We are inserting the data into the table ADAFRUIT. Initiazlizing the variables to their default 
                        values before going to the next loop iteration.
            """
            product_id = 0
            product_name = ""
            product_price = 0.00
            product_qty = 0
            product_stock = ""
    end = time.time() - start
    print(int(end % 60))  # Total time to crawl and scrap
    connection.commit()  # Committing the changes
    connection.close()  # Closing the database connection
    return render_template('index.html')  # "Data Fetched"


@app.route('/query', methods=['POST', 'GET'])
def query():
    query_request = flask_request.values.get('query_to_fetch')  # Fetching the query request
    print(query_request)
    connection = sqlite3.connect('product_data.db')
    cursor_reference = connection.cursor()
    cursor_reference.execute(query_request)
    query_result = cursor_reference.fetchall()
    print(query_result)
    connection.commit()
    connection.close()
    return render_template('index.html', result=query_result)  # Returning the result of a query


@app.route('/best_seller', methods=['POST', 'GET'])
def best_seller():
    connection = sqlite3.connect('product_data.db')
    cursor_reference = connection.cursor()
    cursor_reference.execute(
        '''SELECT * FROM ADAFRUIT WHERE product_qty <=70 AND product_stock="IN STOCK" ORDER BY product_qty DESC''')
    query_result = cursor_reference.fetchall()
    print(query_result)
    connection.commit()
    connection.close()
    return render_template('index.html', result=query_result)


@app.route('/common_items', methods=['POST', 'GET'])
def common():
    connection = sqlite3.connect('product_data.db')
    cursor_reference = connection.cursor()
    cursor_reference.execute(
        '''SELECT * FROM ADAFRUIT WHERE product_qty>=100 AND product_stock="IN STOCK" ORDER BY product_qty DESC''')
    query_result = cursor_reference.fetchall()
    print(query_result)
    connection.commit()
    connection.close()
    return render_template('index.html', result=query_result)


@app.route('/out_of_stock', methods=['POST', 'GET'])
def out_of_stock():
    connection = sqlite3.connect('product_data.db')
    cursor_reference = connection.cursor()
    cursor_reference.execute('''SELECT * FROM ADAFRUIT  WHERE product_stock="OUT OF STOCK" ORDER BY product_name ASC''')
    query_result = cursor_reference.fetchall()
    print(query_result)
    connection.commit()
    connection.close()
    return render_template('index.html', result=query_result)


@app.route('/coming_soon', methods=['POST', 'GET'])
def coming_soon():
    connection = sqlite3.connect('product_data.db')
    cursor_reference = connection.cursor()
    cursor_reference.execute('''SELECT * FROM ADAFRUIT  WHERE product_stock="COMING SOON" ORDER BY product_name ASC''')
    query_result = cursor_reference.fetchall()
    print(query_result)
    connection.commit()
    connection.close()
    return render_template('index.html', result=query_result)


@app.route('/discontinued', methods=['POST', 'GET'])
def discontinued():
    connection = sqlite3.connect('product_data.db')
    cursor_reference = connection.cursor()
    cursor_reference.execute('''SELECT * FROM ADAFRUIT  WHERE product_stock="DISCONTINUED" ORDER BY product_name ASC''')
    query_result = cursor_reference.fetchall()
    print(query_result)
    connection.commit()
    connection.close()
    return render_template('index.html', result=query_result)


@app.route('/categories', methods=['POST', 'GET'])
def categories():
    connection = sqlite3.connect('product_data.db')
    cursor_reference = connection.cursor()
    cursor_reference.execute('''SELECT DISTINCT (product_category) FROM ADAFRUIT''')
    query_result = cursor_reference.fetchall()
    print(query_result)
    connection.commit()
    connection.close()
    return render_template('index.html', result=query_result)


if __name__ == '__main__':
    app.debug = True  # To oversee debugging
    app.run()  # Run the flask app
    """
        I assume the default port=5000 for a flaks will be same on your machine
        My all routes are mapped in index.html with url : "http://127.0.0.1:5000/ OR default" 
    """
