import threading
from queue import Queue
from .spider import Spider
from .domain import *
from .general import *

HOMEPAGE = 'https://supermonitoring.com/'
DOMAIN_NAME = get_domain_name(HOMEPAGE)
PROJECT_PATH = 'E:\\Python scrapper\\2 python web crawling\\crawler\\spider'
QUEUE_FILE = 'templates\queue.txt'
CRAWLED_FILE = 'templates\crawled.txt'
NUMBER_OF_THREADS = 5
queue = Queue()

#Spider(HOMEPAGE, DOMAIN_NAME)


# Create worker threads (will die when main exits)
def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()


# Do the next job in the queue
def work():
    while True:
        url = queue.get()
        Spider.crawl_page(threading.current_thread().name, url)
        queue.task_done()


# Each queued link is a new job
def create_jobs():
    for link in file_to_set(QUEUE_FILE):
        queue.put(link)
    queue.join()
    crawl()


# Check if there are items in the queue, if so crawl them
def crawl():
    queued_links = file_to_set(QUEUE_FILE)
    if len(queued_links) > 0:
        print(str(len(queued_links)) + ' links in the queue')
        create_jobs()

# these two lines to call all of them and start crawling with threads
page = ''


def compute():
    page = '25 years OLD Trillionaire'
    return page

#create_workers()
#crawl()
