## Introduction
This project is used to scrape job reviews information from Indeed.com. You can also modify the code for other website you want to scrape.

## Requirement
This project is based on Python 3 and Scrapy. Please follow the instruction to install Scrapy: https://doc.scrapy.org/en/latest/intro/install.html.

## Instruction

### How to run the code
You can follow the first part of tutorial here: https://doc.scrapy.org/en/latest/intro/tutorial.html.
To run the code, simply go to the project’s top level directory and run:
```
scrapy crawl IndeedSpider
```

### How it works
The main logic locates in /indeed_scraper/spiders/IndeedSpider.py. The class IndeedSpider is responsible for providing initial urls and call-back function. In start_requests, the spider reads in BankList.csv file and launches a scrapy request for each url.
In parse method, we extract the review information needed based on the CSS structure of the HTML file. Then, we store the information into indeed.csv. You can modify the code to include whatever other information you need.

### The CSV file
BankList.csv:
Contains company's name, ticker in stock market, indeed urls (could be more than one) and its BHC_Folder_ID.

indeed.csv:
Structed as follows:
```
company name, review title, overall rating, work/life balance rating,
Comprehension/Benefits rating, Security/Advancement rating, Management rating,
Job culture rating, job title, review time, reviewer location, review content,
pros, 'cons', 'url', 'ticker', 'conml', 'BHC_Folder_ID'
```
