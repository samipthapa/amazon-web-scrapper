from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import csv

with open("Amazon_Result.csv", "w", newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["#", "ASINs", "Title", "Price", "Number of Rating", "#Star Rating", "Bullet Point 1", "Bullet Point 2", "Bullet Point 3", "Bullet Point 4", "Bullet Point 5", "Bullet Point 6"])

count = 1

with open("Amazon_Scrape.csv", "r") as csv_file:
    csv_reader = csv.reader(csv_file)
    next(csv_reader)

    for line in csv_reader:
        URL = f"https://www.amazon.com/dp/{line[1]}"

        path = "C:\\Program Files (x86)\\chromedriver.exe"

        service = Service(path)

        options = webdriver.ChromeOptions()
        options.add_argument("--profile-directory=Default")
        options.add_argument("--user-data-dir=C:\\Users\\samip\\AppData\\Local\\Google\\Chrome\\User Data\\")

        driver = webdriver.Chrome(service=service, options=options)
        driver.get(URL)

        page_source = driver.page_source

        driver.quit()

        soup = BeautifulSoup(page_source, "html.parser")

        try:
            parent_tag = soup.find(class_='a-popover-trigger a-declarative')
            rating = parent_tag.find_next(class_='a-size-base a-color-base').get_text().strip()
            
        except AttributeError:
            rating = ""
        
        try:
            title = soup.find(id="productTitle").get_text().strip()
        except AttributeError:
            title = ""

        try:
            reviews = soup.find(id="acrCustomerReviewText").get_text().strip()

        except AttributeError:
            reviews = ""
        
        try:
            price_int = soup.find(class_="a-price-whole").get_text().strip()
            price_fraction = soup.find(class_="a-price-fraction").get_text().strip()
            price = f"${price_int}{price_fraction}"

        except AttributeError:
            price = ""
        
        try:
            about_item = soup.find('div', id='feature-bullets')
            bullet_points = about_item.find_all('span', class_='a-list-item')
            
            bullet_list = [bullet_point.text.strip() for bullet_point in bullet_points]

        except AttributeError:
            bullet_list = []
        
        with open("Amazon_Result.csv", "a", newline='') as file:
            writer = csv.writer(file)

            bullet_points = [bullet_list[i] if i < len(bullet_list) else "" for i in range(6)]

            writer.writerow([count, line[1], title, price, reviews, rating] + bullet_points)
        
        count += 1
