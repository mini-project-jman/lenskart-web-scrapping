import requests
import json
from pandas import json_normalize

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