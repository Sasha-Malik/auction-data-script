import requests
from bs4 import BeautifulSoup
import csv

url = 'https://www.kickdown.com/en/brands'
response = requests.get(url)

# Create a BeautifulSoup object from the HTML content
soup = BeautifulSoup(response.content, 'html.parser')

main_div = soup.find('main', class_='container')
pop_div = main_div.select_one('div.row:not(.head-brands.mb-3)')
car_div = soup.find('div', class_='row mt-5 mb-4')


#car names in popular brands
pop_elements = pop_div.find_all('a', class_='text-decoration-none')

# car names in other brands
car_name_elements = car_div.find_all('a', class_='fw-bold')

for e in pop_elements:
    car_name_elements.append(e)

car_data = []
for element in car_name_elements:
    if element.text != "Andere Auktionen":
        name = element.text
        href = "https://www.kickdown.com"+ element['href']
        car_data.append({'Car Name': name, 'Href': href})

# writing hrefs of cars into brands.csv
csv_file = 'brands.csv'
with open(csv_file, 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=['Car Name', 'Href'])
    writer.writeheader()
    writer.writerows(car_data)

# reading from brands.csv
brand_hrefs = []
with open(csv_file, 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        href = row['Href']
        brand_hrefs.append(href)

# getting hrefs for each car
car_hrefs = []
for href in brand_hrefs:
    url = href
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    car_links = soup.find_all('a', class_='btn btn-text text-light')
    if car_links != []:
        car_hrefs.append([ "https://www.kickdown.com" + element['href'] for element in car_links])
   

# wringting car links in carLinks.csv   
car_links_file = 'carLinks.csv'
with open(car_links_file, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(car_hrefs)

car_links = []
with open(car_links_file, 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        for link in row:
            car_links.append(link)

# getting car details for each car
car_details  = []
for link in car_links:
        url = link
        print(link)
        response = requests.get(url)
        if response.status_code != 200:
            continue
        soup = BeautifulSoup(response.content, 'html.parser')
        name_div = soup.find('h1',class_ = "mb-3 fw-bold fs-3")
        name = name_div.get_text(strip=True)

        # table containing car details
        table = soup.find('table', class_='table-borderless')
        data = []

        # Find all rows in the table body
        rows = table.find('tbody').find_all('tr')

        # Loop through the rows
        for row in rows:
            # Find all cells in the row
            cells = row.find_all(['th', 'td'])
            
            # Extract the text from the cells
            row_data = [cell.text.strip() for cell in cells]
            
            # Append the row data to the main data list
            data.append(row_data)

        detail = []
        detail.append({"name",name})
        r = 0 
        while r < len(data):
            c = 0
            while c < len(data[r]):
                detail.append({data[r][c],data[r+1][c]})
                c+=1
            r+=2
        
        # append the details for each car to the list of all cars
        car_details.append(detail)

# writing all details into carDetails.csv
car_details_file = 'carDetails.csv'
with open(car_details_file, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(car_details)