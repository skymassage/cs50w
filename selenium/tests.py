'''
URL (Uniform Resource Locator):
URL specifies how the resource can be accessed (protocol) and includes the location of the resource (like a web address). 
For example, "https://www.example.com".

URN (Uniform Resource Name):
URN provides a unique and persistent identifier, but it does not specify a location or method to access the resource.
For example, "urn:isbn:0451450523" uniquely identifies a book using its ISBN, irrespective of where it exists.

URI (Uniform Resource Identifier):
URI is a generic term used to identify a resource either by location, name, or both. 
It serves as a universal identifier for resources on the internet. 
All URLs and URNs are URIs, but not all URIs are URLs or URNs.

Summary of Differences:
URL: Specifies both the identity and the location of a resource (How and Where).
URI: A more comprehensive term covering both URLs (identifying and locating) and URNs (just identifying).
URN: Focuses only on uniquely identifying a resource, not on where it is located or how to access it.
In practical terms, when you're browsing the internet, you're mostly dealing with URLs. 
URIs and URNs come more into play in specific contexts like software development, digital libraries, 
and systems where unique and persistent identification of a resource is crucial.
'''
# So far, we've been able to test out the server-side code we've written using Python and Django, 
# but as we're building up our applications we'll want the ability to create tests for our client-side code as well.

# Selenium allows us to define a testing file in Python where we can simulate a user opening a web browser, 
# navigating to our page, and interacting with it. Our main tool when doing this is known as a Web Driver, 
# which will open up a web browser on your computer. 
# And ChromeDriver is a separate executable that Selenium WebDriver uses to control Chrome. 
# So we need to run "pip3 install selenium" and "pip3 install chromedriver-py" to use them. 

import os
import pathlib
import unittest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

# In order to target a specific page, we need the file's URI which is a unique string that represents that resource.
# "file_uri" takes a file and get its URI, and we need the URI to be able to open it up.
def file_uri(filename):         
    # Path classes are divided between pure paths, which provide purely computational operations without I/O; 
    # and concrete paths, which inherit from pure paths but also provide I/O operations.
    # A subclass of PurePath, this class represents concrete paths of the system's path flavour 
    # (instantiating it creates either a PosixPath or a WindowsPath).
    # PosixPath represents a Unix-style path object and WindowsPath represents Windows-style one.

    # "os.path.abspath" returns a normalized absolutized version of the pathname path.
    # "as_uri" represents the path as a file URI. ValueError is raised if the path isn't absolute.
    return pathlib.Path(os.path.abspath(filename)).as_uri() 

driver = webdriver.Chrome()  # Use "webdriver.Chrome" to create a Chrome browser object

uri = file_uri("counter.html") # Find the URI of counter.html
driver.get(uri)                # Use the URI by ".get" to open the web page.
driver.title                   # Use ".title" to access the title of the current page
driver.page_source             # Use ".page_source" to access the source code of the page

# find_element_by_tag_name: Select by tag element.
# find_element_by_class_name: Select by class.
# find_element_by_id: Selectid by id.
# There is only one letter ('s') difference between find_element_by_<element_type> and find_elements_by_<element>. 
# The former will only return the first element that meets the <element_type> condition. 
# The latter returns all elements that meet the <element_type> condition in the form of a list.
increase = driver.find_element_by_id("increase") # Find and store the increase buttons.
decrease = driver.find_element_by_id("decrease")

increase.click() # Use ".click" to simulate user click operations.
increase.click()
decrease.click()

for i in range(25): # We can even include clicks within other Python constructs:
    increase.click()


# Standard outline of testing class
class WebpageTests(unittest.TestCase):

    def test_title(self):
        """Make sure title is correct"""
        driver.get(file_uri("counter.html")) 
        self.assertEqual(driver.title, "Counter")

    def test_increase(self):
        """Make sure header updated to 1 after 1 click of increase button"""
        driver.get(file_uri("counter.html"))
        increase = driver.find_element_by_id("increase")
        increase.click()
        self.assertEqual(driver.find_element_by_tag_name("h1").text, "1")

    def test_decrease(self):
        """Make sure header updated to -1 after 1 click of decrease button"""
        driver.get(file_uri("counter.html"))
        decrease = driver.find_element_by_id("decrease")
        decrease.click()
        self.assertEqual(driver.find_element_by_tag_name("h1").text, "-1")

    def test_multiple_increase(self):
        """Make sure header updated to 3 after 3 clicks of increase button"""
        driver.get(file_uri("counter.html"))
        increase = driver.find_element_by_id("increase")
        for i in range(3):
            increase.click()
        self.assertEqual(driver.find_element_by_tag_name("h1").text, "3")

if __name__ == "__main__":
    unittest.main()