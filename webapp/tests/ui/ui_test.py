from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import unittest

class FlaskAppTest(unittest.TestCase):
    def setUp(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        self.driver.get("http://localhost:5000")

    def test_home_page(self):
        """Test the home page."""
        driver = self.driver
        body = driver.find_element(By.TAG_NAME, 'body')
        self.assertIn('Enter your password', body.text)

    def test_strong_password(self):
        """Test submitting a strong password."""
        driver = self.driver
        driver.find_element(By.NAME, 'password').send_keys('5TrongP@ssw0rd' + Keys.RETURN)
        body = driver.find_element(By.TAG_NAME, 'body')
        self.assertIn('Welcome', body.text)

    def test_weak_password(self):
        """Test submitting a weak password."""
        driver = self.driver
        driver.find_element(By.NAME, 'password').send_keys('password' + Keys.RETURN)
        body = driver.find_element(By.TAG_NAME, 'body')
        self.assertIn('Password not valid', body.text)

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
