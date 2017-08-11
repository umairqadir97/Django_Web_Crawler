from urllib.request import urlopen
from bs4 import BeautifulSoup
from .link_finder import LinkFinder
from .domain import *
from .general import *


class Spider:
    project_name = ''
    base_url = ''
    domain_name = ''
    queue_file = ''
    crawled_file = ''
    queue = set()
    crawled = set()
    dictionary = {}
    broken_links = []
    no_of_broken_links = 0

    def __init__(self, base_url, domain_name):
        Spider.base_url = base_url
        Spider.domain_name = domain_name
        Spider.queue_file = 'queue.txt'
        Spider.crawled_file = 'crawled.txt'
        self.boot()
        self.crawl_page('First spider', Spider.base_url)

    # Creates directory and files for project on first run and starts the spider
    @staticmethod
    def boot():
        create_data_files( Spider.base_url, Spider.queue_file, Spider.crawled_file)
        Spider.queue = file_to_set(Spider.queue_file)
        Spider.crawled = file_to_set(Spider.crawled_file)

    # Updates user display, fills queue and updates files
    @staticmethod
    def crawl_page(thread_name, page_url):
        if page_url not in Spider.crawled:
            print(thread_name + ' now crawling ' + page_url)
            print('Queue ' + str(len(Spider.queue)) + ' | Crawled  ' + str(len(Spider.crawled)))
            Spider.add_links_to_queue(Spider.gather_links(page_url))
            Spider.queue.remove(page_url)
            Spider.crawled.add(page_url)
            Spider.update_files()

    # Converts raw response data into readable information and checks for proper html formatting
    @staticmethod
    def gather_links(page_url):
        html_string = ''
        status_code = 0
        try:
            response = urlopen(page_url)
            status_code = response.code
            if status_code == 404:
                Spider.broken_links.append(page_url)
                Spider.no_of_broken_links += 1
            
            if 'text/html' in response.getheader('Content-Type'):
                html_bytes = response.read()
                html_string = html_bytes.decode("utf-8")
                Spider.gathering_data(html_bytes, page_url, len(Spider.crawled))

            finder = LinkFinder(Spider.base_url, page_url)
            finder.feed(html_string)
        except Exception as e:
            print(str(e))
            return set()
        return finder.page_links()


    # Saves queue data to project files
    @staticmethod
    def add_links_to_queue(links):
        for url in links:
            if (url in Spider.queue) or (url in Spider.crawled):
                continue
            if Spider.domain_name != get_domain_name(url):
                continue
            Spider.queue.add(url)

    @staticmethod
    def update_files():

        set_to_file(Spider.queue, Spider.queue_file)
        set_to_file(Spider.crawled, Spider.crawled_file)

    # tree = fromstring("<a>Find me!</a>")
    # print tree.xpath("//a/text()")

    @staticmethod
    def gathering_data(html_string, page_url, no_of_url):
        soup = BeautifulSoup(html_string, "lxml")
        images = soup.find_all('img')
        alt_count = 0
        for each in images:
            alt = each['src']
            if(alt):
                continue
            else:
                print(alt)
                alt_count +=1

        # print(soup)
        data_dictionary = {}
        data_dictionary['url_no'] = len(Spider.crawled)
        data_dictionary['url_crawled'] = page_url
        data_dictionary['canonical_url'] = soup.find('link', attrs={'rel': 'canonical'})
        data_dictionary['meta_title'] = soup.find('title')
        if data_dictionary['meta_title']:
            data_dictionary['title_length'] = len(data_dictionary['meta_title'])
        
        output = soup.find('meta', {"name" : "description"})
        if output:
            data_dictionary['meta_description'] = output['content']
        
        if data_dictionary['meta_description']:
            data_dictionary['meta_description_length'] = len(data_dictionary['meta_description'])
        # for tag h1
        t = ''
        string = soup.find_all('h1')
        for each in string:
            t = t + ">" + each.text + '\n'
        data_dictionary['h1'] = t
        
        # for h2 tag
        t = ''
        string = soup.find_all('h2')
        for each in string:
            t = t + ">" + each.text + '\n'
        data_dictionary['h2'] = t

        # for h3 tag
        t = ''
        string = soup.find_all('h3')
        for each in string:
            t = t + ">" + each.text + '\n'
        data_dictionary['h3'] = t

        # for h4 tag
        t = ''
        string = soup.find_all('h4')
        for each in string:
            t = t + ">" + each.text + '\n'
        data_dictionary['h4'] = t

        # for h5 tag
        t = ''
        string = soup.find_all('h5')
        for each in string:
            t = t + ">" + each.text + '\n'
        data_dictionary['h5'] = t

        # Open Graph tags
        # these if statements are implemented tp avoid errors if any element
        #
        data_dictionary['og_title'] = soup.find('meta', {'property': 'og:title'})
        #
        data_dictionary['og_description'] = soup.find('meta', {'property': 'og:description'})
        #
        data_dictionary['og_image'] = soup.find('meta', {'property': 'og:image'})
        #
        data_dictionary['og_type'] = soup.find('meta', {'property': 'og:type'})
        #
        data_dictionary['og_video'] = soup.find('meta', {'property': 'og:video'})
        #
        data_dictionary['og_locale'] = soup.find('meta', {'property': 'og:locale'})
        #
        data_dictionary['og_url'] = soup.find('meta', {'property': 'og:url'})
        #
        data_dictionary['og_site_name'] = soup.find('meta', {'property': 'og:site:name'})
        #
        data_dictionary['og_updated_time'] = soup.find('meta', {'property': 'og:updated:time'})
        #
        data_dictionary['og_audio'] = soup.find('meta', {'property': 'og:audio'})

        # twitter tags
        # ########################
        data_dictionary['twitter_title'] = soup.find(attrs={'name': 'twitter:title'})
        #
        data_dictionary['twitter_description'] = soup.find('meta', {'name': 'twitter:description'})
        #
        data_dictionary['twitter_image'] = soup.find('meta', {'name': 'twitter:image'})
        #
        data_dictionary['twitter_card'] = soup.find('meta', {'name': 'twitter:card'})
        #
        data_dictionary['twitter_site'] = soup.find('meta', {'name': 'twitter:site'})
        #
        data_dictionary['twitter_creator'] = soup.find('meta', {'name': 'twitter:creator'})

        # others
        data_dictionary['missing_alt_tags']  = alt_count
        data_dictionary['no_of_broken_links']  = Spider.no_of_broken_links   
        print("No of broken links:",Spider.no_of_broken_links)    
        
        ga_code = False
        ga = soup.find_all('script')
        for each in ga:
            strr = each.string
            if strr is None:
                continue
            elif 'www.google-analytics.com/analytics.js' in strr:
                ga_code = True
                break

        data_dictionary['google-analytics_code'] = ga_code
        Spider.dictionary[page_url] = data_dictionary

"""
@ will be done later
         - indexing block status 
"""