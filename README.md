# amazon-review-scraper

## Installation

```pip install git+https://github.com/seanmalone3/amazon-review-scraper.git```

## Errors

This package requires ssl, you might have to rebuild Python if you're encountering an error.

## Usage

```
# Import class Scrape
from AmazonReviewScraper import Scrape

# Initialize self with class vars
a = Scrape(amazon_id='B06XCM9LJ4', user_agent='Mozilla/5.0', user_email='president@whitehouse.gov')
```

All functions are designed to run without much user input, but have the ability to take more specific inputs. I recommend starting with a small sample and making sure your `user_agent` and `user_email` are non-descript.

