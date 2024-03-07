import requests
import json
import pandas as pd
from pandas import json_normalize
from multiprocessing import Pool
from utils.reviews import fetch_reviews
from utils.upload import upload_to_blob
import logging

def scrap():

    logging.info("scrapping  started")
    all_data = []
    for i in range(4):
        logging.info(f"scrapping page no {i}")
        eyeglasses_api = f'https://api-gateway.juno.lenskart.com/v2/products/category/3363?page-size=1400&page={i}'
        response = requests.get(eyeglasses_api)

        if response.status_code == 200:
            data = response.json()

            all_data.extend(data['result']['product_list'])


    flattened_data = json_normalize(all_data)

    flattened_data.to_csv('data/products_data.csv', index=False)

    logging.info("Data saved to 'products_data.csv'")

    #upload_to_blob('data/products_data.csv')
    #upload_to_blob('data/customers.csv')
    #upload_to_blob('data/transactions.csv')

def scrape_reviews():
    df = pd.read_csv("data/products_data.csv")
    products_id = df['id'].tolist()

    with Pool(processes=8) as pool:
        results = pool.map(fetch_reviews, products_id)
   
    all_reviews = [review for sublist in results for review in sublist]
    reviews_df = pd.DataFrame(all_reviews)
    reviews_df = reviews_df[['productId', 'reviewee', 'noOfStars', 'reviewDetail', 'reviewDate', 'reviewTitle', 'reviewId', 'reviewerType']]
    print(reviews_df)

    reviews_df.to_csv('data/reviews_data.csv', index=False)
    logging.info("Data saved to 'reviews_data.csv'")
    #upload_to_blob('data/reviews_data.csv')

