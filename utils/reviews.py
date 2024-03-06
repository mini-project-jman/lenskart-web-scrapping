import requests
import logging

def fetch_reviews(id):
    logging.info(f"Scrapping reviews for ID {id}")
    reviews_api = f'https://api-gateway.juno.lenskart.com/v2/products/product/{id}/review?count=500&page=1'
    response = requests.get(reviews_api)
    reviews_data = []
    if response.status_code == 200:
        data = response.json()
        for review in data['result']['review']['reviews']:
            review_filled = {key: review.get(key, 'NA') for key in ['reviewId', 'reviewTitle', 'reviewDetail', 'reviewee', 'noOfStars', 'reviewDate', 'reviewerType']}
            review_filled['reviewTitle'] = review_filled['reviewTitle'].replace(","," ")
            review_filled['reviewDetail'] = review_filled['reviewDetail'].replace(","," ")
            review_filled['reviewee'] = review_filled['reviewee'].replace(","," ")
            review_filled['reviewerType'] = review_filled['reviewerType'].replace(","," ")
            review_filled['productId'] = id
            reviews_data.append(review_filled)
    else:
        logging.warning(f"Failed to fetch reviews for product ID {id}")
    return reviews_data