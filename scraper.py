import os
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import json
import itertools

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

path = "/Users/harshverma/Desktop/ pandas/chromedriver"
  
PATH = os.path.relpath(path)


print(PATH)

companies = []

links = []

driver = webdriver.Chrome(PATH)
driver.get("https://www.forbes.com/lists/worlds-best-employers/?sh=27429d461e0c")
print("created ")

try:
    print("started searching...")
    wait = WebDriverWait(driver, 40)
    rank = wait.until(
        lambda driver: driver.find_element(By.CLASS_NAME, "rank"))
    industry = wait.until(
        lambda driver: driver.find_element(By.CLASS_NAME, "industry"))
    name = wait.until(lambda driver: driver.find_element(
        By.CLASS_NAME, "organizationName"))
    country = wait.until(
        lambda driver: driver.find_element(By.CLASS_NAME, "country"))
    employees = wait.until(
        lambda driver: driver.find_element(By.CLASS_NAME, "employees"))
    driver.find_element(By.CLASS_NAME, "toggle-row").click()
    a_tag = driver.find_element(
        By.CLASS_NAME, "ExpandedRow_profileImage__2tl7g")
    link = a_tag.get_attribute("href")
    companies.append({
        "rank": rank.text,
        "name": name.text,
        "industries": industry.text,
        "country": country.text,
        "employees": employees.text,
        "link": link
    })
    links.append(link)
finally:
    driver.quit()


req = requests.get(
    "https://www.forbes.com/lists/worlds-best-employers/?sh=27429d461e0c")

soup = BeautifulSoup(req.content, "html.parser")

div = soup.find('section', class_="csf-row et-rows row_633eeebb2fd89")

for a in div.find_all("a", attrs={"class": "table-row"}, href=True):
    # print(a.contents)
    Rank, Name, Industries, Country, Employees = a.contents
    
    fixed_rank = (Rank.text)
    fixed_Name = (Name.text)
    fixed_industries = (Industries.text)
    fixed_country = (Country.text)
    fixed_employees = (Employees.text)
    href = (a['href'])
    links.append(href)
    company = {
        "rank": fixed_rank,
        "name": fixed_Name,
        "industries": fixed_industries,
        "country": fixed_country,
        "employees": fixed_employees,
        "link": href
    }
    companies.append(company)

n=20
Info =[]

for link in itertools.islice(links,n):
    req = requests.get(link)
    soup = BeautifulSoup(req.content, "html.parser")
    company_name=soup.find('h1', class_='listuser-header__name').text
    company_revenue=soup.find('div',class_="listuser-financial-item__value")
    if (company_revenue):
        company_Revenue=company_revenue.text
    company_industry = soup.find('span',class_="profile-stats__text").text
    company_details={
        "name": company_name,
        "revenue": company_Revenue,
        "industry":company_industry
    }

    Info.append(company_details)

with open("websites_details.json","w") as f:
    json.dump(Info,f,indent=3)

with open("companies.json", "w") as f:
    json.dump(companies, f, indent=6)
