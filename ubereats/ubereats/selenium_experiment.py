import time
from selenium.webdriver import Chrome, ChromeOptions

options = ChromeOptions()

# options.add_argument("--headless")

options.add_argument("start-maximized")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")
options.add_argument("--disable-gpu")

driver = Chrome(options=options)

driver.get('https://www.google.com/')
time.sleep(5)

search_box = driver.find_element_by_name("q")
search_box.send_keys('ChromeDriver')
search_box.submit()
time.sleep(5)

driver.quit()
