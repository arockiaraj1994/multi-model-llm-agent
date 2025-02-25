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
    # Configurable delay times in seconds
    GENERAL_DELAY = 2
    DELAY_AFTER_SAVE = 2
    DELAY_AFTER_PROJECT_CLICK = 2
    DELAY_AFTER_YAML_INPUT = 2
    DELAY_AFTER_ROUTES_TAB = 5
    DELAY_MONACO_EDITOR = 5
    DELAY_AFTER_RUN = 10

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)
    
    def tearDown(self):
        self.driver.quit()

    @parameterized.expand(load_test_cases())
    def test_fill_project_form(self, project_name, yaml_content):
        # Open the localhost page
        self.driver.get("http://localhost:8080")
        
        # Click projects button first
        projects_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "projects"))
        )
        projects_button.click()
        
        time.sleep(self.GENERAL_DELAY)
        # Click create button
        create_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "dev-action-button"))
        )
        create_button.click()
        
        time.sleep(self.GENERAL_DELAY)
        # Wait for the form fields to be visible
        project_id_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "projectId"))
        )
        project_name_input = self.driver.find_element(By.ID, "name")
        
        # Fill in the form fields using the parameter
        project_id_input.send_keys(project_name)
        project_name_input.send_keys(f"{project_name}")
        
        time.sleep(self.GENERAL_DELAY)
        # Find the save button within the modal footer
        save_button = self.driver.find_element(
            By.CSS_SELECTOR, 
            ".pf-v5-c-modal-box__footer .pf-v5-c-button.pf-m-primary"
        )
        
        # Click the save button
        save_button.click()
        
        # Wait after saving
        time.sleep(self.DELAY_AFTER_SAVE)
        
        # Wait for the project link with specific project name to be clickable
        project_link = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((
                By.XPATH,
                f"//table[@aria-label='Projects']//button[contains(@class, 'pf-m-link') and text()='{project_name}']"
            ))
        )
        
        # Get the text of the link to verify later
        link_text = project_link.text
        
        # Verify the link text matches our created project
        self.assertEqual(link_text, project_name)
        
        # Click the project link
        project_link.click()
        
        # Wait for project details to load
        time.sleep(self.DELAY_AFTER_PROJECT_CLICK)
        
        # Verify we're on the correct project page
        project_header = self.driver.find_element(By.CSS_SELECTOR, "div.pf-v5-c-content.title h2")
        self.assertEqual(project_header.text, project_name)

        # Wait for the topology toolbar and Route button with precise path
        toolbar = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "topology-toolbar"))
        )
        
        # Find the second div with class pf-v5-c-toolbar__item pf-m-align-right
        toolbar_items = toolbar.find_elements(By.CLASS_NAME, "pf-v5-c-toolbar__item")
        align_right_div = None
        for item in toolbar_items:
            if "pf-m-align-right" in item.get_attribute("class"):
                align_right_div = item
                break
        
        # Find the Route button within the align-right div
        route_button = align_right_div.find_element(
            By.CSS_SELECTOR,
            "button.pf-v5-c-button.pf-m-primary.pf-m-small.dev-action-button"
        )
        
        # Click the Route button
        route_button.click()
        
        # Wait for the name input field to be visible
        name_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "name"))
        )
        
        # Fill in the name field
        name_input.send_keys(project_name)
        
        # Find and click save button in the modal footer
        modal_footer = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "pf-v5-c-modal-box__footer"))
        )
        
        save_button = modal_footer.find_element(
            By.CSS_SELECTOR,
            "button.pf-v5-c-button.pf-m-primary"
        )
        save_button.click()
        
        # Wait to see the result
        time.sleep(self.DELAY_AFTER_SAVE)
        
        # Wait for the main tabs to be present and find the YAML tab
        main_tabs = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.pf-v5-c-tabs.main-tabs"))
        )
        
        # Find and click the YAML tab (4th tab with text "YAML")
        yaml_tab = main_tabs.find_element(
            By.CSS_SELECTOR,
            "li.pf-v5-c-tabs__item button[aria-controls*='code']"
        )
        yaml_tab.click()
        
        # Wait for the Monaco editor to load
        time.sleep(self.DELAY_MONACO_EDITOR)

        # Use JavaScript to set the editor content with the yaml from CSV
        set_editor_script = """
        const editor = monaco.editor.getModels()[0];
        editor.setValue(arguments[0]);
        """
        self.driver.execute_script(set_editor_script, yaml_content)
        
        # Wait to see the formatted result
        time.sleep(self.DELAY_AFTER_YAML_INPUT)
        
        # Find and click the Routes tab (first tab)
        routes_tab = main_tabs.find_element(
            By.CSS_SELECTOR,
            "li.pf-v5-c-tabs__item button[aria-controls*='routes']"
        )
        routes_tab.click()
        
        # Wait to see the result
        time.sleep(self.DELAY_AFTER_ROUTES_TAB)
        
        # Find and click the Run button
        run_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((
                By.CSS_SELECTOR,
                ".dev-action-button-place button.pf-v5-c-button.pf-m-primary.pf-m-small.dev-action-button"
            ))
        )
        run_button.click()
        
        # Wait to see the result
        time.sleep(self.DELAY_AFTER_RUN)

if __name__ == "__main__":
    unittest.main()
