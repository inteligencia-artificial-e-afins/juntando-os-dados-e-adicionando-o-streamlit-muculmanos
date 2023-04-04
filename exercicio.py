from bs4 import BeautifulSoup
import requests


url = "https://imobiliariaperez.com.br/alugar" # site para extrair
response = requests.get(url) #request html


soup = BeautifulSoup(response.content, 'html.parser') #configurao beautifulsoup

myInfoArray = []

links = soup.find_all('a',class_="slide-home-btn")

for link in links:
    pushHref = link['href']
    newResponse = requests.get(pushHref)
    newSoup = BeautifulSoup(newResponse.content, 'html.parser') #configurao beautifulsoup
    title = newSoup.find('h1', class_= "elementor-heading-title").get_text()
    value = newSoup.find('h2', class_= "elementor-heading-title").get_text()
    area =  newSoup.find('div', class_= "col-6").get_text()
    description = newSoup.find_all('p')[3].get_text()
    address = "londrina-PR"
    aux = [title, value, area, description, address ]
    myInfoArray.append(aux)
print(myInfoArray)