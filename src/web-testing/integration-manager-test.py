from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest
import time

class IntegrationManagerTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)
    
    def tearDown(self):
        self.driver.quit()
    
    
    '''def test_click_projects_button(self):
        # Open the localhost page
        self.driver.get("http://localhost:8080")
        
        # Wait for 2 seconds to see the page clearly
        time.sleep(2)
        
        # Wait for the projects button to be clickable
        projects_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "projects"))
        )
        
        # Pause briefly before clicking
        time.sleep(1)
        
        # Click the button
        projects_button.click()
        
        # Wait after clicking to see the result
        time.sleep(2)
        
        # Verify the button was clicked (you can add specific assertions here)
        self.assertTrue(projects_button.is_displayed())
    
    def test_click_create_button(self):
        # Open the localhost page
        self.driver.get("http://localhost:8080")
        
        # Click projects button first
        projects_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "projects"))
        )
        projects_button.click()
        
        # Wait for the create button to be clickable
        create_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "dev-action-button"))
        )
        
        # Pause briefly before clicking
        time.sleep(1)
        
        # Click the create button
        create_button.click()
        
        # Wait after clicking to see the result
        time.sleep(2)
        
        # Verify the button was clicked
        self.assertTrue(create_button.is_displayed())'''

    def test_fill_project_form(self):
        # Open the localhost page
        self.driver.get("http://localhost:8080")
        
        # Click projects button first
        projects_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "projects"))
        )
        projects_button.click()
        
        # Click create button
        create_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "dev-action-button"))
        )
        create_button.click()
        
        # Wait for the form fields to be visible
        project_id_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "projectId"))
        )
        project_name_input = self.driver.find_element(By.ID, "name")
        
        # Fill in the form fields
        project_id_input.send_keys("test-project-001")
        project_name_input.send_keys("Test Project")
        
        # Find the save button within the modal footer
        save_button = self.driver.find_element(
            By.CSS_SELECTOR, 
            ".pf-v5-c-modal-box__footer .pf-v5-c-button.pf-m-primary"
        )
        
        # Click the save button
        save_button.click()
        
        # Wait for 10 seconds after saving
        time.sleep(2)
        
        # Wait for the project link to be clickable within the table structure
        project_link = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((
                By.CSS_SELECTOR, 
                'table[aria-label="Projects"] tbody.pf-v5-c-table__tbody button.pf-v5-c-button.pf-m-link'
            ))
        )
        
        # Get the text of the link to verify later
        project_name = project_link.text
        
        # Verify the link text matches our created project
        self.assertEqual(project_name, "test-project-001")
        
        # Click the project link
        project_link.click()
        
        # Wait for project details to load
        time.sleep(2)
        
        # Verify we're on the correct project page
        project_header = self.driver.find_element(By.CSS_SELECTOR, "div.pf-v5-c-content.title h2")
        self.assertEqual(project_header.text, "test-project-001")

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
        name_input.send_keys("test-route-001")
        
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
        time.sleep(2)
        
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
        time.sleep(5)

        # Prepare the YAML content with proper formatting
        yaml_content = """- route:
    id: timer-route-cron
    from:
      uri: timer:mytimer?cron=0+*+*+*+*
      steps:
        - setBody:
            simple: "Timer triggered at ${header.firedTime}"
        - log: "${body}"
"""

        # Use JavaScript to properly set the editor content
        set_editor_script = """
        const editor = monaco.editor.getModels()[0];
        editor.setValue(arguments[0]);
        """
        self.driver.execute_script(set_editor_script, yaml_content)
        
        # Wait to see the formatted result
        time.sleep(2)
        
        # Find and click the Routes tab (first tab)
        routes_tab = main_tabs.find_element(
            By.CSS_SELECTOR,
            "li.pf-v5-c-tabs__item button[aria-controls*='routes']"
        )
        routes_tab.click()
        
        # Wait to see the result
        time.sleep(5)
        
        # Find and click the Run button
        run_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((
                By.CSS_SELECTOR,
                ".dev-action-button-place button.pf-v5-c-button.pf-m-primary.pf-m-small.dev-action-button"
            ))
        )
        run_button.click()
        
        # Wait to see the result
        time.sleep(10)

if __name__ == "__main__":
    unittest.main()
