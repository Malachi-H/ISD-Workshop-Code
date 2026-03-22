import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoAlertPresentException
from selenium.webdriver.chrome.options import Options

class TestRegister(unittest.TestCase):
    def setUp(self):
        chrome_options = Options()
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.get("http://localhost:8000/register.html")
        self.form = self.driver.find_element(By.ID, "register-form")
    
    def tearDown(self):
        self.driver.quit()
        return super().tearDown()

    def test_name_empty(self):
        # check the tos box if not already checked
        tos_checkbox = self.form.find_element(By.ID, "tos-checkbox")
        if not tos_checkbox.is_selected():
            tos_checkbox.click()

        # no fields are filled, submit the form
        self.form.submit()

        try:
            WebDriverWait(self.driver, 10).until(EC.alert_is_present())
            alert = self.driver.switch_to.alert
            alert_text = alert.text

            if alert_text != "Please enter your name.":
                raise Exception(f'Expected "Please enter your name.", but got "{alert_text}"')

            alert.dismiss()
            print("Passed: shows alert if name is empty")
        except (TimeoutException, NoAlertPresentException):
            raise Exception("Expected alert did not appear")
        
    def test_email_empty(self):        
        tos_checkbox = self.form.find_element(By.ID, "tos-checkbox")
        if not tos_checkbox.is_selected():
            tos_checkbox.click()

        name_input = self.driver.find_element(By.ID, "name")
        name_input.send_keys("Joe")

        self.form.submit()

        try:
            email_error = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.ID, "email-error")))
            email_error_text = email_error.text

            if email_error_text != "Please enter your email.":
                raise Exception(f'Expected "Please enter your email.", but got "{email_error_text}"')

            print("Passed: shows alert if email is empty")
        except (TimeoutException, NoAlertPresentException):
            raise Exception("Expected alert did not appear")

    def test_password_empty(self):
        tos_checkbox = self.form.find_element(By.ID, "tos-checkbox")
        if not tos_checkbox.is_selected():
            tos_checkbox.click()

        name_input = self.driver.find_element(By.ID, "name")
        name_input.send_keys("Joe")
        email_input = self.driver.find_element(By.ID, "email")
        email_input.send_keys("joe.joe@joe.com")

        self.form.submit()

        try:
            password_error = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.ID, "password-error")))
            password_error_text = password_error.text

            if password_error_text != "Please enter your password.":
                raise Exception(f'Expected "Please enter your password.", but got "{password_error_text}"')

            print("Passed: shows alert if password is empty")
        except (TimeoutException, NoAlertPresentException):
            raise Exception("Expected alert did not appear")

    def test_tos_not_ticked(self):
        tos_checkbox = self.form.find_element(By.ID, "tos-checkbox")
        if tos_checkbox.is_selected():
            tos_checkbox.click()
            
        name_input = self.driver.find_element(By.ID, "name")
        name_input.send_keys("Joe")
        email_input = self.driver.find_element(By.ID, "email")
        email_input.send_keys("joe.joe@joe.com")
        password_input = self.driver.find_element(By.ID, "password")
        password_input.send_keys("password123")
        gender_input = self.driver.find_element(By.ID, "gender")
        gender_input.send_keys("m")
        favcol_input = self.driver.find_element(By.ID, "favcol")
        favcol_input.send_keys("red")
        
        self.form.submit()

        try:
            WebDriverWait(self.driver, 10).until(EC.alert_is_present())
            alert = self.driver.switch_to.alert
            alert_text = alert.text

            self.assertEqual(alert_text, "You must agree to the Terms of Service.")
            alert.dismiss()
        except (TimeoutException, NoAlertPresentException):
            self.fail("Expected alert did not appear")

    def test_register_successful(self):
        tos_checkbox = self.form.find_element(By.ID, "tos-checkbox")
        if not tos_checkbox.is_selected():
            tos_checkbox.click()

        name_input = self.driver.find_element(By.ID, "name")
        name_input.send_keys("Joe")
        email_input = self.driver.find_element(By.ID, "email")
        email_input.send_keys("joe.joe@joe.com")
        password_input = self.driver.find_element(By.ID, "password")
        password_input.send_keys("password123")
        gender_input = self.driver.find_element(By.ID, "gender")
        gender_input.send_keys("m")
        favcol_input = self.driver.find_element(By.ID, "favcol")
        favcol_input.send_keys("red")

        self.form.submit()

        try:
            WebDriverWait(self.driver, 10).until(EC.url_contains("welcome.html"))
            current_url = self.driver.current_url

            if "welcome.html" not in current_url:
                raise Exception(f'Expected URL to contain "welcome.html", but got "{current_url}"')

            print("Passed: redirects to welcome page when registration is successful")
        except TimeoutException:
            raise Exception("Expected redirect to welcome page did not occur")

if __name__ == "__main__":
    unittest.main()