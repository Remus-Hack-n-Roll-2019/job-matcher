import requests
import bs4
from bs4 import BeautifulSoup
import pandas as pd
import time
from gevent.pool import Pool
from gevent import monkey; monkey.patch_all() # patches stdlib
import sys
import logging
from http.client import HTTPSConnection
from timeit import default_timer as timer
from indeed import *
info = logging.getLogger().info

def parallelize_requests(f, listOfRequests):
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
    pool = Pool(20) # limit number of concurrent connections
    start = timer()
    listOfResponses = pool.map(f, listOfRequests)
    info("%d hosts took us %f seconds", len(listOfRequests), timer() - start)
    return listOfResponses

# if __name__=="__main__":
#     strings = [
#         'Deep Learning', 'software engineer', 'test engineer', 'devops engineer', 'mechanical engineer', 'entrepreneur',
#         'Deep Learning', 'software engineer', 'test engineer', 'devops engineer'
#     ]
#     listOfRequests = []
#     for keyword in strings:
#         listOfRequests.append({ "keyword": keyword, "location": "singapore" })
#     listOfResponses = parallelize_requests(listOfRequests)
#     responses = []
#     for response in listOfResponses:
#         responses.extend(response)
#     print(len(responses))
