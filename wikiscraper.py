import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from urllib.error import URLError
import random
from bs4 import BeautifulSoup
import re
import matplotlib.pyplot as plt
from collections import Counter

dictionary = {}
megastring = ""
def count(element):

    if element[-1] == '.' or element[-1] == ',':
        element = element[0:len(element) - 1]

    if element in dictionary:
        dictionary[element] += 1

    else:
        dictionary.update({element: 1})

def scrape_page(url):
    """
    Scrape the page for words in text and returns a string with all words
    """
    session = requests.Session()
    retry = Retry(connect = 3, backoff_factor = 0.5)
    adapter = HTTPAdapter(max_retries = retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    page = requests.get(url, timeout = 10)

    soup = BeautifulSoup(page.content, "html.parser")
    #dictionary = {}
    text = ""

    # Doesn't find all text with this
    for paragraph in soup.find(id = "bodyContent").find_all('p'):
        text += str(paragraph.text.strip())

    for paragraph in soup.find(id = "bodyContent").find_all('ul'):
        text += str(paragraph.text.strip())

    text = re.sub(r'\[[0-9]*\]',' ', text)
    text = re.sub(r'\s+',' ', text)
    text = text.lower()
    text = re.sub(r'\d',' ', text)
    text = re.sub("[^A-Z]", ' ', text, 0, re.IGNORECASE)

    #print(text)
    lst = text.split()

    all_links = soup.find(id = "bodyContent").find_all('a')
    random.shuffle(all_links)
    new_url = 0

    for link in all_links:
        if link['href'].find("/wiki/") == -1:
            new_url = "https://en.wikipedia.org" + link['href']
            break
    page.close()

    return lst, new_url

def count_words(lst):
    """
    Counts the occurence of all words of input list and adds to the dictionary
    """
    for word in lst:
        count(word)

def find_most_common_words(dictionary):
    """
    Finds the ten most common words in the dictionary and creates a bar plot
    for occurences
    """

    for words in dict(sorted(dictionary.items(), key=lambda item: item[1], reverse = True)):
        print("Frequency {} : {}".format(words, dictionary[words]))

    most_common = dict(sorted(dictionary.items(), key=lambda item: item[1], reverse = True)[:10])

    words = list(most_common.keys())
    occurences = list(most_common.values())

    plt.bar(words, occurences, tick_label=words)
    plt.show()




URL = "https://en.wikipedia.org/wiki/Python_(programming_language)"
list_of_words, new_url = scrape_page(URL)
count_words(list_of_words)
find_most_common_words(dictionary)

def future_work():
    """
    Scrape more than one page
    """
    megastring += str(list_of_words)
    for x in range(0, 2):
        result = scrape_page(new_url)
        megastring += str(result[0])
        new_url = result[1]

    count_words(megastring.split())
    find_most_common_words(dictionary)



def scrape_it_all():
    """
    All the scraping
    """
    all_links = soup.find(id = "bodyContent").find_all("a")
    random.shuffle(all_links)
    link_to_scrape = 0

    for link in all_links:
        if link['href'].find("/wiki/") == -1:
            link_to_scrape = link
            break

