import scrapy
import unicodedata
import csv
import os

rating_translate = {
    'width:86.0px': 5,
    'width:68.8px': 4,
    'width:51.6px': 3,
    'width:34.4px': 2,
    'width:17.2px': 1,
    'width:0.0px': 0,
}

class Bank(object):

    bankName = ''
    ticker = ''
    conml = ''
    indeedLinks = []
    BHC_Folder_ID = ''

    def __init__(self, name, ticker, conml, BHC_id):
        self.bankName = name
        self.ticker = ticker
        self.conml = conml
        self.BHC_Folder_ID = BHC_id

    def __repr__(self):
        return 'name: %s, ticker: %s, conml: %s, BHC_Folder_ID: %s.' % (self.bankName, \
            self.ticker, self.conml, self.BHC_Folder_ID)



class IndeedSpider(scrapy.Spider):
    name = "IndeedSpider"
    allowed_domains = ["indeed.com"]

    base_url = 'https://www.indeed.com'
    count = 0
    urls = {}
    company = ''

    def start_requests(self):
        line_count = 0
        with open('../BankList_new.csv', 'r') as bankListFile:
            reader = csv.DictReader(bankListFile)
            for row in reader:
                line_count+=1

                bank = Bank(row['Bank Name'], row['Ticker'], row['conml'],
                    row['BHC_Folder_ID'])
                bank.indeedLinks = row['Indeed Link'].split(';')

                for link in bank.indeedLinks:
                    self.urls[link]= bank


        for url, comp in self.urls.iteritems():
            if url:
                yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):

        self.log('parsing %s, url %s' % (self.company, response.url))

        if not os.path.exists('indeed.csv'):
            with open('indeed.csv', 'a') as csvfile:
                writer = csv.writer(csvfile, dialect='excel')
                writer.writerow(['company name','review title', 'overall rating', 'work/life balance rating',
                    'Comprehension/Benefits rating', 'Security/Advancement rating', 'Management rating',
                    'Job culture rating', 'job title', 'review time', 'reviewer location', 'review content',
                    'pros', 'cons', 'url', 'ticker', 'conml', 'BHC_Folder_ID'])

        next_page = response.css('a.company_reviews_pagination_link_nav[data-tn-element="next-page"]::attr(href)').extract_first()
        current_url = response.url
        page_count = 0
        for review in response.css('div.cmp-review-container'):

            # extract review header
            header = review.css('div.cmp-review-heading')[0]
            title = header.css('div.cmp-review-title span::text').extract_first()
            job_title = header.css('span.cmp-reviewer-job-title span.cmp-reviewer::text').extract_first()
            job_status =  header.css('span.cmp-reviewer-job-title::text').extract_first()
            review_time = header.css('span.cmp-review-date-created::text').extract_first()
            reviewer_location = header.css('span.cmp-reviewer-job-location::text').extract_first()

            #extract rating
            rating_overall = header.css('span.cmp-value-title::attr(title)').extract_first()
            ratings_expanded = header.css('table.cmp-ratings-expanded')[0]
            ratings = [None]*5
            for i in range(5):
                rating_expand = ratings_expanded.css('span.cmp-rating-inner::attr(style)')[i].extract()
                ratings[i] = rating_translate[rating_expand.encode('utf-8')]


            # extract review content
            content = review.css('div.cmp-review-content-container')[0]
            review_text = content.css('span.cmp-review-text::text').extract_first()
            pros = content.css('div.cmp-review-pro-text::text').extract_first()
            cons = content.css('div.cmp-review-con-text::text').extract_first()

            # convert to unicode to ASCII
            title = unicodedata.normalize('NFKD', title).encode('ascii','ignore')
            rating_overall = unicodedata.normalize('NFKD', rating_overall).encode('ascii','ignore')
            if job_title:
                job_title = unicodedata.normalize('NFKD', job_title).encode('ascii','ignore')
                if job_status:
                    job_title += unicodedata.normalize('NFKD', job_status).encode('ascii','ignore')
            if review_text:
                review_text = unicodedata.normalize('NFKD', review_text).encode('ascii','ignore')
            if review_time:
                review_time = unicodedata.normalize('NFKD', review_time).encode('ascii','ignore')
            if reviewer_location:
                reviewer_location = unicodedata.normalize('NFKD', reviewer_location).encode('ascii','ignore')
            if pros:
                pros = unicodedata.normalize('NFKD', pros).encode('ascii','ignore')
            if cons:
                cons = unicodedata.normalize('NFKD', cons).encode('ascii','ignore')

            self.count+=1
            page_count+=1

            parent_url_pos = current_url.find('reviews') + len('reviews')
            parent_url = current_url[:parent_url_pos]
            bank = self.urls[parent_url]

            # write into csv
            with open('indeed.csv', 'a') as csvfile:
                writer = csv.writer(csvfile, dialect='excel')
                writer.writerow([bank.bankName, title, rating_overall]+ratings +
                    [job_title, review_time, reviewer_location, review_text, pros, cons, current_url, \
                    bank.ticker, bank.conml, bank.BHC_Folder_ID])

        # crawl the next page if exist
        if next_page is not None:
            next_page = self.base_url + next_page
            yield scrapy.Request(next_page, callback=self.parse)
