from selenium import webdriver
from selenium.webdriver.chrome.service import Service

# print(Service("./chromedriver.exe").path)


driver = webdriver.Chrome()

# s = Service("./chromedriver.exe")
# driver = webdriver.Chrome(service=s)
