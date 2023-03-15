import requests
from bs4 import BeautifulSoup
import re
import matplotlib.pyplot as plt

def count(element):

    if element[-1] == '.' or element[-1] == ',':
        element = element[0:len(element) - 1]

    if element in dictionary:
        dictionary[element] += 1

    else:
        dictionary.update({element: 1})

URL = "https://en.wikipedia.org/wiki/Python_(programming_language)"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")
dictionary = {}
text = ""

# Doesn't find all text with this
for paragraph in soup.find(id = "bodyContent").find_all('p'):
    text += str(paragraph.text.strip())

text = re.sub(r'\[[0-9]*\]',' ', text)
text = re.sub(r'\s+',' ', text)
text = text.lower()
text = re.sub(r'\d',' ', text)

lst = text.split()

for word in lst:
    count(word)

for words in dict(sorted(dictionary.items(), key=lambda item: item[1], reverse = True)):
    print("Frequency", words, end = " ")
    print(":", end = " ")
    print(dictionary[words], end = " ")
    print()

words = list(dictionary.keys())
occurences = list(dictionary.values())

plt.bar(range(len(dictionary)), values, tick_label=words)
plt.show()
#print(text)
