# Procurement scraper

This crawler has been set up to scrape government procurements in China. The spider scrapes data from
[中国政府采购网](http://www.ccgp.gov.cn/). Set parameters for the search and then copy the url to point to the `url` variable. `number_of_pages` also needs to be set. 

### Required packages

* `selenium`
* `scrapy`

### Scraped data

The data scraped from the website includes:

* `title` of the project
* `project` information
* `procurement_unit`
* `region`
* `amount`
* 'announce_date`  
* `link` to documentation
