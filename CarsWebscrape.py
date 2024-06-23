import requests
from bs4 import BeautifulSoup
import pandas as pd

baseurl = 'https://www.cars.com/'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 OPR/107.0.0.0'
}

tempproductlinks = []

for x in range(1,100):
    r = requests.get(f'https://www.cars.com/shopping/results/?dealer_id=&include_shippable=false&keyword=&list_price_max=&list_price_min=&makes[]=&maximum_distance=50&mileage_max=&monthly_payment=&no_accidents=true&only_with_photos=true&page={x}&page_size=20&sort=best_match_desc&stock_type=used&year_max=&year_min=&zip=89012')
    soup = BeautifulSoup(r.content, 'lxml')
    productlist = soup.find_all('div', class_='vehicle-card-main js-gallery-click-card')
    for item in productlist:
        for link in item.find_all('a', href=True):
            tempproductlinks.append(baseurl + link['href'])

productlinks = [x for x in tempproductlinks if "vehicledetail" in x]

carinfolist = []

for link in productlinks:
    r = requests.get(link, headers=headers)
    soup = BeautifulSoup(r.content, 'lxml')

    name = soup.find('h1', class_='listing-title').text.strip()
    price = soup.find('span', class_='primary-price').text.strip()
    mileage = soup.find('p', class_='listing-mileage').text.strip()
    
    try:
        exteriorcolor = soup.find('dt', text="Exterior color").findNext('dd').string.strip()
    except AttributeError:
        exteriorcolor = "N/A"
        
    try:
        fueltype = soup.find('dt', text="Fuel type").findNext('dd').string.strip()
    except AttributeError:
        fueltype = "N/A"
    
    try:
        transmission = soup.find('dt', text="Transmission").findNext('dd').string.strip()
    except AttributeError:
        transmission = "N/A"
        
    try:
        drivetrain = soup.find('dt', text="Drivetrain").findNext('dd').string.strip()
    except AttributeError:
        drivetrain = "N/A"
    
    try:
        mpg = soup.find('span', data_qa='mpg').text.strip()
    except AttributeError:
        mpg = "N/A"
    
    try:
        pricedrop = soup.find('span', class_='secondary-price price-drop').text.strip()
    except AttributeError:
        pricedrop = "N/A"

    carinfo = {
        'name': name,
        'price': price,
        'mileage': mileage,
        'exterior color': exteriorcolor,
        'fuel type': fueltype,
        'transmission': transmission,
        'drivetrain': drivetrain,
        'mpg': mpg,
        'price drop': pricedrop
    }    

    carinfolist.append(carinfo)
    print('Saving: ', carinfo['name'])

df = pd.DataFrame(carinfolist)
print(df.head(3))

df.to_csv('carsdata.csv')
