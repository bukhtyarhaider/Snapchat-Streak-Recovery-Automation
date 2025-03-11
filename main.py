from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

options = webdriver.ChromeOptions()
# Uncomment the next line to run in headless mode:
# options.add_argument("--headless")

# Initialize ChromeDriver automatically
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)


driver.get("https://www.google.com")

# Close the browser
driver.quit()
