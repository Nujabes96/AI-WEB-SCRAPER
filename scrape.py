import selenium.webdriver as webdriver
from selenium.webdriver.edge.service import Service
import time

def steal(website):
    print("Launching browser...")

    browser_path = ('msedgedriver.exe')
    service = Service(browser_path)
    options = webdriver.EdgeOptions()
    driver = webdriver.Edge(service=service, options=options)
    
    try:
        driver.get(website)
        html = driver.page_source
        print("Page loaded...")
        time.sleep(10)
        return html
    finally:
        driver.quit()