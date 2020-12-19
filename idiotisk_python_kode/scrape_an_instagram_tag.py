import requests
from bs4 import BeautifulSoup as soup 
headers = {'User-Agent': 'Mozilla/5.0'}

url = "https://www.instagram.com/explore/tags/steming/"

response = requests.get(url, headers)

insta_soup = soup(response.text, "html.parser")

print(insta_soup)