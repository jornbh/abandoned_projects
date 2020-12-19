import bs4
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup 
my_url = "https://www.newegg.com/global/no-en/Video-Cards-Video-Devices/Category/ID-38"

print(my_url)
uClient = uReq(my_url)
print(uClient)
print("Imported", bs4)

page_html = uClient.read()
uClient.close()

page_soup = soup( page_html, "html.parser")

containers = page_soup.find_all("div", {"class" : "item-container"})

print("Titles \n\n")

container = containers[0]
for container in containers: 
    title = container.a.img["title"]

    title_container = container.find_all("a", {"class": "item-title"})
    product_name = title_container[0].text
    print(title)
    print()