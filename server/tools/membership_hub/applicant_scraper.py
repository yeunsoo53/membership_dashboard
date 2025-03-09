import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time, csv, traceback

# Set up logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filename='selenium_debug.log')
logger = logging.getLogger(__name__)

def initialize_driver():
    try:
        logger.info("Setting up Chrome options")
        chrome_options = Options()
        chrome_options.add_argument("--window-size=1920,1080")
        # Uncomment to run headless (no browser UI)
        # chrome_options.add_argument("--headless")
        
        logger.info("Initializing WebDriver")
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        return driver
    except Exception as e:
        logger.error(f"Error initializing driver: {str(e)}")
        raise

def login(driver, url, email, password):
    # Navigate to the login page
    driver.get(url)
    
    # Wait for the page to load and the form to be visible
    wait = WebDriverWait(driver, 10)
    email_field = wait.until(EC.presence_of_element_located((By.ID, "email")))
    
    # Fill in the login form
    email_field.send_keys(email)  # Replace with actual email
    
    password_field = driver.find_element(By.ID, "password")
    password_field.send_keys(password)  # Replace with actual password
    
    # Click the login button
    login_button = driver.find_element(By.CSS_SELECTOR, "button.btn.btn-primary")
    login_button.click()

    time.sleep(2)
    try:
        # Using the "Landing" class which appears in the HTML after login
        wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "Landing"))
        )
        logger.info("Dashboard loaded successfully - 'Landing' element found")
        
        # Log the current URL to understand where we are after login
        logger.info(f"Successfully logged in. Current URL: {driver.current_url}")  
        return True

    except Exception as e:
        logger.error(f"Dashboard element not found: {str(e)}")
        # Log the current URL to see where we are
        logger.info(f"Current URL: {driver.current_url}")
        # Take screenshot to see what page looks like
        driver.save_screenshot("error_dashboard.png")
        # Log page source for debugging
        with open("page_source.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        logger.info("Saved page source to page_source.html")
        return False

def navigate_to_page(driver, url):
    try:
        logger.info(f"Navigating to {url}...")
        driver.get(url)

        # Wait for page to load
        time.sleep(3)
        
        # Wait for container to confirm page loaded
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "container")))
        
        logger.info(f"Successfully navigated to {url}")
        return True
    except Exception as e:
        logger.error(f"Error navigating to {url}: {str(e)}")
        return False

def view_results_of_application(driver, app_name):
    wait = WebDriverWait(driver, 10)

    try:
        table_xpath = "//h2[contains(text(), 'Closed Applications')]/following-sibling::table[1]"
        table = wait.until(EC.presence_of_element_located((By.XPATH, table_xpath)))

        logger.info(f"Found following table")

        # Now use the table as the context for finding the row
        app_row = table.find_element(By.XPATH, f".//td[contains(text(), '{app_name}')]/ancestor::tr")

        logger.info(f"Found row containing {app_name}")

        review_button = app_row.find_element(By.XPATH, ".//a[contains(normalize-space(), 'Review Results')]")

        logger.info(f"Found results button for {app_name}")

        # Scroll the button into view
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", review_button)

        time.sleep(0.5)

        try:
            review_button.click()
            # After clicking and waiting a bit
            time.sleep(10)

            wait.until(EC.presence_of_element_located((By.XPATH, "//h2[contains(text(), 'Results!')]")))
            logger.info(f"Results for {app_name} loaded successfully")

            return True
        
        except Exception as e:
            logger.error(f"Error locating results button for {app_name}")
            return False

    except Exception as e:
        logger.error(f"Error locating {app_name}")
        return False

def main():
    driver = None

    try:
        driver = initialize_driver()
        base_url = "https://members.secsystems.net/"
        login_url = base_url + "login"
        email = "eunsooyeo@tamu.edu"
        password = "qlcthrma0530/Tam"

        login_successful = login(driver, login_url, email, password)

        if not login_successful:
            logger.error("Login failed, aborting")
            return False
        
        target_url = base_url + "applications"
        navigation_successful = navigate_to_page(driver, target_url)

        if not navigation_successful:
            logger.error("Navigation failed, aborting")
            return False
        
        app = "Spring 2025 New Member Application"
        view_results_successful = view_results_of_application(driver, app)

        if not view_results_successful:
            logger.error("Error viewing application results, aborting")
            return False

        return True
    except Exception as e:
        logger.error(f"Error during scraping: {str(e)}")
        logger.error(traceback.format_exc())
        return False
    finally:
        # Always close the driver to free resources
        if driver:
            logger.info("Closing WebDriver")
            driver.quit()

if __name__ == "__main__":
    print("Starting Selenium-based scraper for SEC Membership Hub...")
    result = main()
    
    if result:
        print("Scraping completed successfully.")
    else:
        print("Scraping encountered errors.")