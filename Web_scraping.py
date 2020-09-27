from bs4 import BeautifulSoup
import requests

page = 'http://www.allocine.fr/film/fichefilm_gen_cfilm=61.html'

resp = requests.get(page).text

soup = BeautifulSoup(resp, 'html.parser')

title = soup.find_all("div", {"class":"titlebar-title titlebar-title-lg"})
synopsis = soup.find_all("div", {"class":"content-txt"})
genres = soup.find_all("span", {"class" : lambda value: value and value.startswith("ACrL2ZACrpbG1zL2")})

