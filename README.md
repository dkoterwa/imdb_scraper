# IMDB Scrapers
Beautiful Soup, Scrapy, and Selenium scrapers for getting information about top 250 IMDB movies.

## How to run Beautiful Soup Scraper
If you don't have BS installed, run '''bash pip install bs4 '''
### 1. Download the scraper_imdb_soup.py file from soup directory.
### 2. Go to the directory with file and run this line of code:

```bash
python scraper_imdb_soup.py
```

## How to run Scrapy Scraper

### 1. Open imdb_spider.py 
### 2. Make sure Scrapy is installed. If it isn't already installed, use the following command: 
```bash pip install scrapy ```
### 3. Install the Scrapy Fake Useragent plugin. Install it by running the following command: 
```bash pip install scrapy-fake-useragent ```
### 4. We may now run the Scrapy spider and extract the data. To start the spider and save the output as a CSV file, use the following command: 
```bash scrapy crawl imdbSpider -o scrapy_scraping_imdb.csv ```

## How to run Selenium Scraper

If you don't have Selenium installed, run '''bash pip install selenium '''
### 1. Download the SeleniumProject.py file from selenium directory.
### 2. Go to the directory with file and run this line of code:

```bash
python SeleniumProject.py
```

