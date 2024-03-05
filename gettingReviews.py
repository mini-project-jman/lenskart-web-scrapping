import pandas as pd
import requests


# Load CSV into DataFrame
df = pd.read_csv("products_data.csv")

# Display the first few rows of the DataFrame to verify it loaded correctly
df.head()

# getting all product ids
products_id = df['id']


reviews_data = []

def scrape_reviews(id):
    # using ids to get the data using api with maximum 10,000 reviews
    reviews_api = f'https://api-gateway.juno.lenskart.com/v2/products/product/{id}/review?count=1000&page=1'
    response = requests.get(reviews_api)
    if response.status_code == 200:
        data = response.json()
        for review in data['result']['review']['reviews']:
            # Fill in missing values with 'NA'
            review_filled = {key: review.get(key, 'NA') for key in ['reviewId', 'reviewTitle', 'reviewDetail', 'reviewee', 'noOfStars', 'reviewDate', 'reviewerType', 'images']}
            review_filled['productId'] = id
            reviews_data.append(review_filled)
    else:
        print(f"Failed to fetch reviews for product ID {id}")

# Scrape reviews for each product id
for id in products_id:
    scrape_reviews(id)

# Creating DataFrame
reviews_df = pd.DataFrame(reviews_data)

# Reordering columns
reviews_df = reviews_df[['productId', 'reviewee', 'noOfStars', 'reviewDetail', 'reviewDate', 'reviewTitle', 'reviewId', 'reviewerType', 'images']]

# Displaying DataFrame
print(reviews_df)

