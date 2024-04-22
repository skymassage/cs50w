from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


# print(Service("./chromedriver.exe").path)


driver = webdriver.Chrome()

# s = Service("./chromedriver.exe")
# s = Service("/usr/bin/chromedriver")

# driver = webdriver.Chrome(service=s)
