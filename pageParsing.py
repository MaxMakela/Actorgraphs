import requests
from bs4 import BeautifulSoup

page = requests.get("https://en.wikipedia.org/wiki/List_of_actors_with_Hollywood_Walk_of_Fame_motion_picture_stars")
soup = BeautifulSoup(page.content, 'html.parser')
print(soup.prettify())