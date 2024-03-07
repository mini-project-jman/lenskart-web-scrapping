from scrapper.scrapper import scrap,scrape_reviews
from utils.transformations import transform
from multiprocessing import freeze_support
import logging
logging.basicConfig(filename='log.txt',
                    filemode='a',
                    format='%(asctime)s,%(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)

if __name__ == '__main__':
    freeze_support()
    scrap()
    #transform()
    #scrape_reviews()