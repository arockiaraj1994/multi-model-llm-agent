import csv
from parameterized import parameterized
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest
import time

def load_test_cases():
    test_cases = []
    with open('test_cases.csv', 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            test_cases.append((row['project_name'], row['yaml']))
    return test_cases

class IntegrationManagerTest(unittest.TestCase):
    # Wait time configurations
    IMPLICIT_WAIT = 10  # seconds
    EXPLICIT_WAIT = 10  # seconds for explicit waits
    CLICK_DELAY = 2    # seconds delay before clicks
    DELETION_VERIFY_WAIT = 2  # seconds to wait after deletion
    FINAL_WAIT = 10    # seconds to wait at the end

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(self.IMPLICIT_WAIT)
    
    def tearDown(self):
        self.driver.quit()

    @parameterized.expand(load_test_cases())
    def test_fill_project_form(self, project_name, yaml_content):
        # Open the localhost page
        self.driver.get("http://localhost:8080")
        
        # Click projects button first
        projects_button = WebDriverWait(self.driver, self.EXPLICIT_WAIT).until(
            EC.element_to_be_clickable((By.ID, "projects"))
        )
        time.sleep(self.CLICK_DELAY)  # Add delay before click
        projects_button.click()

        # Wait for the projects table to be visible
        table = WebDriverWait(self.driver, self.EXPLICIT_WAIT).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "table[aria-label='Projects']"))
        )

        # Find the row containing the project name
        project_row = table.find_element(
            By.XPATH,
            f"//tbody[@role='rowgroup']//tr[.//button[contains(text(), '{project_name}')]]"
        )

        # Find and click the delete button within that row
        delete_button = project_row.find_element(
            By.CSS_SELECTOR,
            "button.pf-v5-c-button.pf-m-plain.dev-action-button svg[viewBox='0 0 352 512']"
        ).find_element(By.XPATH, "./..")  # Get the parent button of the delete icon SVG
        time.sleep(self.CLICK_DELAY)  # Add delay before click
        delete_button.click()

        # Wait for the confirmation dialog
        WebDriverWait(self.driver, self.EXPLICIT_WAIT).until(
            EC.presence_of_element_located((By.CLASS_NAME, "pf-v5-c-modal-box"))
        )

        # Find and click the switch toggle for "Delete related container and/or deployments"
        switch_toggle = self.driver.find_element(
            By.CSS_SELECTOR,
            "input.pf-v5-c-switch__input[type='checkbox']"
        )
        time.sleep(self.CLICK_DELAY)  # Add delay before click
        switch_toggle.click()

        # Click the delete/confirm button
        confirm_button = WebDriverWait(self.driver, self.EXPLICIT_WAIT).until(
            EC.element_to_be_clickable((
                By.CSS_SELECTOR,
                ".pf-v5-c-modal-box__footer .pf-v5-c-button.pf-m-danger"
            ))
        )
        time.sleep(self.CLICK_DELAY)  # Add delay before click
        confirm_button.click()

        # Wait to ensure deletion is complete
        time.sleep(self.DELETION_VERIFY_WAIT)

        # Verify the project is deleted by checking it's no longer in the table
        try:
            table.find_element(
                By.XPATH,
                f"//button[contains(text(), '{project_name}')]"
            )
            self.fail(f"Project {project_name} was not deleted successfully")
        except:
            pass  # Project not found, which means deletion was successful

        time.sleep(self.FINAL_WAIT)

if __name__ == "__main__":
    unittest.main()
