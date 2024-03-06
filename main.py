from scrapper.scrapper import scrap,scrape_reviews
from utils.transformations import transform
from multiprocessing import Pool, freeze_support

#scrap()
#transform()

if __name__ == '__main__':
    freeze_support()
    scrape_reviews()