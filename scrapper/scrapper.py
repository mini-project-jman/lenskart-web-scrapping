import requests
import json
import pandas as pd
from pandas import json_normalize
from multiprocessing import Pool

def scrap():
    # Initialize an empty list to store all product details
    all_data = []
    for i in range(4):
        eyeglasses_api = f'https://api-gateway.juno.lenskart.com/v2/products/category/3363?page-size=1400&page={i}'
        response = requests.get(eyeglasses_api)

        if response.status_code == 200:
            data = response.json()
            # Append the data to the list
            all_data.extend(data['result']['product_list'])

    # Flatten the list of dictionaries
    flattened_data = json_normalize(all_data)
    # Save the DataFrame to a CSV file
    flattened_data.to_csv('data/products_data.csv', index=False)

    print("Data saved to 'products_data.csv'")

def fetch_reviews(id):
    print(f"Scrapping reviews for ID {id}")
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
        print(f"Failed to fetch reviews for product ID {id}")
    return reviews_data

def scrape_reviews():
    df = pd.read_csv("data/products_data.csv")
    products_id = df['id'].tolist()

    # Initialize pool of workers
    with Pool(processes=8) as pool:
        results = pool.map(fetch_reviews, products_id)

    # Flatten the list of lists into a single list
   
    all_reviews = [review for sublist in results for review in sublist]
    reviews_df = pd.DataFrame(all_reviews)
    reviews_df = reviews_df[['productId', 'reviewee', 'noOfStars', 'reviewDetail', 'reviewDate', 'reviewTitle', 'reviewId', 'reviewerType']]
    print(reviews_df)

    reviews_df.to_csv('data/reviews_data.csv', index=False)
    print("Data saved to 'reviews_data.csv'")

