from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from .forms import InputForm

import threading
from queue import Queue
from .spider import Spider
from .domain import *
from .general import *
from .main import *


HOMEPAGE = ''
DOMAIN_NAME = ''
NUMBER_OF_THREADS = 5
#PROJECT_PATH = 'E:\\Python scrapper\\2 python web crawling\\crawler\\spider'
PROJECT_NAME = 'webcrawler'
QUEUE_FILE = 'queue.txt'
CRAWLED_FILE = 'crawled.txt'
NUMBER_OF_THREADS = 5
queue = Queue()

dictionary = {}


# Create worker threads (will die when main exits)
def create_workers():
    for _ in range(5):
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
    dictionary = crawl()
    return dictionary



# Check if there are items in the queue, if so crawl them
def crawl():
    queued_links = file_to_set(QUEUE_FILE)
    crawled_links = file_to_set(CRAWLED_FILE)
    if len(queued_links) > 0 and len(crawled_links) < 2:
        print(str(len(queued_links)) + ' links in the queue')
        dictionary = create_jobs()
    else:
        return Spider.dictionary
    return Spider.dictionary


"""
def index(request):
   d = {'one':'itemone', 'two':'itemtwo', 'three':'itemthree'}
   return render_to_response('spider/home.html', {'d':d})
"""


def index(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        form = InputForm(request.POST)
        if form.is_valid():
            home_url = form.cleaned_data['home_url']
            number_of_threads = form.data['number_of_threads']
            google_code = form.cleaned_data['google_code']
            broken_links = form.cleaned_data['broken_links']

            print(home_url)
            print(number_of_threads)
            print(google_code)
            print(broken_links)
            print("start crawling....")

            HOMEPAGE = home_url
            DOMAIN_NAME = get_domain_name(HOMEPAGE)
            NUMBER_OF_THREADS = number_of_threads

            print(HOMEPAGE)
            print(DOMAIN_NAME)
            print(NUMBER_OF_THREADS)

            Spider(HOMEPAGE, DOMAIN_NAME) #spider object created
            
            create_workers() # create threads and start them to "functionality = work()"
            dictionary = crawl() #file_to_set, if(len(queue)>0): create jobs

            my_dictionary = {'one': 'itemone', 'two': 'itemtwo', 'three': 'itemthree'}
            
            #print(dictionary)
            # context = {'dictionary': my_dictionary, 'results': result, 'page':page}
            context = {'dictionary': my_dictionary, 'result': dictionary }
            return render(request, 'spider/header.html', context)
    else:
        form = InputForm()

    return render(request, 'spider/header.html', {'form': form } )

