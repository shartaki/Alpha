from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import wikipedia  # Import Wikipedia API for summary retrieval
import pyttsx3

class WikipediaSearch:
    def __init__(self):
        self.driver = webdriver.Firefox()
        self.wait = WebDriverWait(self.driver, 10) 
        self.engine = pyttsx3.init()

    def get_info(self, query):
        self.driver.get("https://www.wikipedia.org")
        search_input = self.wait.until(EC.presence_of_element_located((By.ID, "searchInput")))
        search_input.send_keys(query)
        search_input.send_keys(Keys.RETURN)  # Press Enter instead of clicking the search button

        # Wait for the page to load
        self.wait.until(EC.presence_of_element_located((By.ID, "content")))
        
        # Get the first five lines of the article using Wikipedia API
        statement = query.replace("wikipedia", "")  # Remove "wikipedia" from query
        results = wikipedia.summary(statement, sentences=5)
        
        # Speak  five  lines
        self.engine.say(results)
        self.engine.runAndWait()
