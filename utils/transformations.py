import json
import pandas as pd



def transform():
    csv_file_path = "data/products_data.csv"
    df = pd.read_csv(csv_file_path)
    json_column_name = 'prices'  
 
    def extract_prices(json_str):
        data_list = json.loads(json_str.replace("'", "\""))
        market_price = next((item['price'] for item in data_list if item['name'] == 'Market Price'), None)
        lenskart_price = next((item['price'] for item in data_list if item['name'] == 'Lenskart Price'), None)
        return pd.Series({'Market_Price': market_price, 'Lenskart_Price': lenskart_price})

    df[['Market_Price', 'Lenskart_Price']] = df[json_column_name].apply(extract_prices)
    df = df.drop('prices',axis=1)
    

    json_column_name = 'hashtagList'
    
    def extract_names(json_str):
        data_list = json.loads(json_str.replace("'", "\""))
        name_values = [item.get('name', '') for item in data_list]
        return ",".join(name_values)
    
    df[json_column_name] = df[json_column_name].apply(extract_names)
    
    df['Discount_Percentage'] = round(((df['Market_Price'] - df['Lenskart_Price']) / df['Market_Price']) * 100,0)

    df.to_csv('data/final_data.csv', index=False)