import bs4
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup 
import requests
import shutil
import re
import random
base_url = "https://old.reddit.com/"


subreddit = "r/PrincessesOfPower/"

my_url = base_url + subreddit
headers = {'User-Agent': 'Mozilla/5.0'}

def handle_page(page_url): 
    image_page = requests.get(page_url, headers = headers)
    page_html = image_page.text
    page_soup = soup( page_html, "html.parser")
    image_field = page_soup.find("img", {"class" : "preview"})["src"]
    print(image_field)
    image_name = page_url.strip("/").split("/")[-1] +".jpg"
    # image_name = re.match( "\\.[(com)(it)]/.*\\.[(jpg)(png)]", image_field)
    # image_name = str(random.randint(1,1<<200)) +".jpg"
    r = requests.get(image_field,headers=headers, stream=True)
    if r.status_code == 200:
        with open("./images/"+ image_name, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)        


def main_loop(): 

    next_link = my_url # Start link

    for i in range(10**6): # Just an absurdly high number
        print("Scraping page", i)
        request_response = requests.get(next_link, headers = headers)
        page_html = request_response.text
        page_soup = soup( page_html, "html.parser")

        # Handle one page 
        titles = page_soup.find_all( "a", {"class": "title may-blank"})
        for ind,title in enumerate(titles): 
            print("Page", i , "Image", ind,"/", len(titles))
            link = title["href"]
            total_link = base_url + link
            try: 
                handle_page(total_link)
            except Exception as e:
                print("No image Link: ", total_link)
                # raise e
            print("\t", total_link)


        next_link = page_soup.find("span", {"class":"next-button"}).a["href"]

        print(next_link)

main_loop()

# handle_page("https://old.reddit.com/r/PrincessesOfPower/comments/faxpds/hey_adora_my_art/")