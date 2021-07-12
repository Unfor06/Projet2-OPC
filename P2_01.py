from requests import Session
from bs4 import BeautifulSoup as bs
from typing import Tuple, List, Dict
import pandas as pd
 
ROOT_URL = "http://books.toscrape.com/"
SESSION = Session() 
def get_page(url: str) -> Tuple[bs, int]:
    
    assert isinstance(url, str), f"url doit être un str correspondant à une page du site. url était: {str(url)}, de type: {type(url)}"
    assert url.startswith(ROOT_URL), f"Cette fonction ne fonctionne que sur le site web {ROOT_URL}. \n L'URL donnée était: {url}"

    response = SESSION.get(url)
    status = response.status_code
    if not response.ok:
        print(f"L'URL {url} n'est pas ok \n Code d'erreur: {status}")
        return None, status
    else:
        soup = bs(response.content.decode("utf-8"), "lxml")
        return soup, status

def get_nb_pages(url="http://books.toscrape.com/catalogue/category/books_1/index.html"):
    """
    Renvoie le nombre total de pages dans le catalogue
    """
    soup, _ = get_page(url)
     
    return int(soup.find("li", class_= "current")
                   .get_text()
                   .strip()[-2:])

def get_links(soup: bs) -> List[str]:
    """
     La fonction get_links permet de extraire toutes les url présentes sur 1 page du catalogue et renvoie toutes les url sous forme de liste
    """
    links = []
    
    listings = soup.findAll("article", class_= "product_pod")
    base_url: str = f"{ROOT_URL}catalogue/"

    for listing in listings:
        book_link = (listing.find("h3")
                            .find('a')
                            .attrs["href"]
                            .replace('../../', base_url))
        links.append(book_link)
    return links

def get_all_links(url="http://books.toscrape.com/catalogue/category/books_1/index.html",
                  url_fmt="http://books.toscrape.com/catalogue/category/books_1/page-{}.html"):
    links = []
                
    for i in range(1, get_nb_pages(url) + 1):
        url = url_fmt.format(i)
        links.extend(get_links(get_page(url)[0]))
    return links


def extract_book_data(url: str="http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html",
                      table_fields: List[str]=["upc", "product_type", "price_ex_tax", "price_in_tax", "tax", "available", "nb_reviews"]) -> Dict[str, str]:
    
    soup, code = get_page(url)
    book_data = {}
    
    trs = soup.findAll('tr')
    book_data["title"] = soup.find('title').get_text()
    if soup.find('div', id='product_description') is not None: # test pour vérifier si soup.find est None/vide
        book_data["product_description"] = soup.find('div', id='product_description').find_next("p").get_text()
    # https://docs.python.org/fr/3/library/functions.html#zip
    for name_field, tr in zip(table_fields, trs):
        book_data[name_field] = tr.find('td').get_text()

    book_data["category"] = (soup.find('ul' , class_= 'breadcrumb')
                                 .findAll('li')[-2]
                                 .find('a')
                                 .get_text())
    book_data["rating"] = soup.find(class_='star-rating').attrs["class"][-1]
    book_data["image"] = (soup.find('div', id="product_gallery")
                              .find('img')
                              .attrs["src"]
                              .replace('../../', ROOT_URL))

    return book_data
url = f"{ROOT_URL}catalogue/category/books_1/index.html"
all_books = []
all_urls = get_all_links()
nb_urls = len(all_urls)
print(all_urls)
i = 1
for url in all_urls:
    print(f"Scraping de l'url {i}/1000 du catalogue")
    i += 1
    soup, status = get_page(url)
    if status == 200:   
        all_books.append(extract_book_data(url))
    else:
        print("The End")

df = pd.DataFrame(all_books)
df.to_csv("scraped_data.csv")
