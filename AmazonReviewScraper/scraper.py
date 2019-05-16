from bs4 import BeautifulSoup
import ssl
import pandas as pd
import requests
import time


class Scrape:

    def __init__(self, amazon_id='B06XCM9LJ4', user_agent='Mozilla/5.0', user_email='president@whitehouse.gov'):
        self.amazon_id = amazon_id
        self.user_agent = user_agent
        self.user_email = user_email

        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

    def get_html(self, page=1):
        url = "https://www.amazon.com/product-reviews/{}/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews&pageNumber={}".format(
            self.amazon_id, page)
        headers = {
            'User-Agent': self.user_agent,
            'From': self.user_email
        }
        page = requests.get(url, headers=headers)
        html = page.text
        return html

    def count_reviews(self, html=None):
        if html is None:
            html = self.get_html(page=1)
        soup = BeautifulSoup(html,"lxml")
        return int(soup.find("span", {"data-hook": "total-review-count"}).text.replace(',', ''))

    def get_pages(self, num_reviews=None):
        import math
        if num_reviews is None:
            num_reviews = self.count_reviews()
        return math.ceil(num_reviews / 10)

    def get_page_reviews(self, html=None):
        if html is None:
            html = self.get_html()
        soup = BeautifulSoup(html,"lxml")
        review_div = "a-section review aok-relative"
        mydivs = soup.findAll("div", {"class": review_div})

        df = pd.DataFrame(columns=['date', 'reviewer', 'badge', 'rating', 'title', 'verified_purchase', 'product_type',
                                   'helpful_votes', 'review'])
        error = 0
        for index in range(len(mydivs)):
            div = mydivs[index]
            try:
                reviewer = div.find("span", {"class": "a-profile-name"}).text
            except:
                reviewer = None
                error += 1
            try:
                date = div.find("span", {"data-hook": "review-date"}).text
                date = pd.to_datetime(date, format="%B %d, %Y")
            except:
                date = None
                error += 1
            try:
                badge = div.find("div", {"class": "badges-genome-widget"}).text[1:]
            except:
                badge = None
            try:
                rating = int(div.find("i", {"data-hook": "review-star-rating"}).text[0])
            except:
                rating = None
                error += 1
            try:
                review_title = div.find("a", {"data-hook": "review-title"}).text[:-1]
            except:
                review_title = None
                error += 1
            try:
                avp_badge = div.find("span", {"data-hook": "avp-badge"}).text
            except:
                avp_badge = None
            try:
                product_type = div.find("a", {"data-hook": "format-strip"}).text
            except:
                product_type = None
            try:
                num_helpful = div.find("span", {"data-hook": "helpful-vote-statement"}).text
                num_helpful = int(''.join(filter(lambda x: x.isdigit(), num_helpful)))
            except:
                num_helpful = None
            try:
                review = div.find("span", {"data-hook": "review-body"}).text[:-1]
            except:
                review = None
                error += 1
            df.loc[index] = [date, reviewer, badge, rating, review_title, avp_badge, product_type, num_helpful, review]
        print("\tRetrieved", len(df), "reviews with", error, "missing values")
        return df

    def get_all_reviews(self, pages=None, wait_time=3):
        if pages is None:
            pages = self.get_pages()
        print("Getting reviews...\nExpect a", pages * wait_time, "second wait to avoid Amazon scraping detection\n")
        df = pd.DataFrame(columns=['date', 'reviewer', 'badge', 'rating', 'title', 'verified_purchase', 'product_type',
                                   'helpful_votes', 'review'])
        for i in range(pages):
            html = self.get_html(i + 1)
            new_df = self.get_page_reviews(html)
            df = df.append(new_df)
            time.sleep(wait_time)
        print("Success!", len(df), "reviews downloaded")
        return df