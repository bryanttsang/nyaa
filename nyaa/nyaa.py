from selenium import webdriver
from selenium.webdriver.chrome.options import Options

f = open("omit.txt", "r")
omit = f.read().split("\n") # separate titles by a newline
f.close()

lst = []

options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)
driver.get("https://nyaa.si/user/subsplease?f=0&c=0_0&q=SubsPlease+1080p")

for x in range(1, 76):
    date = driver.find_element_by_xpath("/html/body/div/div/div[1]/table/tbody/tr[%d]/td[5]" %x).get_attribute("title")
    if "week" in date:
        break
    title = driver.find_element_by_xpath("/html/body/div/div/div[1]/table/tbody/tr[%d]/td[2]/a" %x).text
    if title.isnumeric():
        title = driver.find_element_by_xpath("/html/body/div/div/div[1]/table/tbody/tr[%d]/td[2]/a[2]" %x).text
    if not "Batch" in title and not any(x in title for x in omit):
        magnet = driver.find_element_by_xpath("/html/body/div/div/div[1]/table/tbody/tr[%d]/td[3]/a[2]" %x).get_attribute("href")
        lst.append(tuple((title[13:-23], magnet)))

driver.quit()

for t, m in lst:
    print("\n%s\n%s" %(t.center(80, '='), m))
