# amazon-review-scraper

## Disclaimer

This is probably against Amazon's terms of service and could potentially result in getting your IP banned, so use at your own risk.

## Installation

```pip install git+https://github.com/seanmalone3/amazon-review-scraper.git```

## Errors

This package requires ssl, you might have to rebuild your Python version if you're encountering an error.

## Usage

You'll need to grab the amazon product id from the product url:
e.g. `B06XCM9LJ4` from https://www.amazon.com/all-new-amazon-echo-speaker-with-wifi-alexa-dark-charcoal/dp/B06XCM9LJ4/

```
# Import class Scrape
from AmazonReviewScraper import Scrape

# Initialize self with class vars (these are the defaults)
a = Scrape(amazon_id='B06XCM9LJ4', user_agent='Mozilla/5.0', user_email='president@whitehouse.gov')
```

All functions are designed to run without much user input, but have the ability to take more specific inputs. I recommend starting with a small sample and making sure your `user_agent` and `user_email` are non-descript.

```
# Count total number of reviews
>>> a.count_reviews()
42980
```

```
# Get first page of reviews
>>> a.get_page_reviews()

# Get all reviews
>>> a.get_all_reviews()
```
|    date    | reviewer            | badge            | rating | title                                             | verified_purchase | product_type                              | helpful_votes | review                                            |
|:----------:|---------------------|------------------|:------:|---------------------------------------------------|-------------------|-------------------------------------------|---------------|---------------------------------------------------|
| 2018-07-20 | Sherry the Dog Lady | None             | 5      | AMAZING SOUND!!                                   | Verified Purchase | Color: Charcoal FabricConfiguration: Echo | 1278          | I got some smart plugs so that I could turn on... |
| 2018-03-01 | Gaylord             | TOP 500 REVIEWER | 5      | Remember GEN 2 is an updated version of the or... | Verified Purchase | Color: Charcoal FabricConfiguration: Echo | 4104          | Let me preface this review by revealing a few ... |

## Updates Planned

1. Current displayed star-rating
2. Getting select reviews (e.g. reviews 100-200)

