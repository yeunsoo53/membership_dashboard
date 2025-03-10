import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import os, time, traceback, json, datetime

# Set up logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filename='selenium_debug3.log')
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
        driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", review_button)

        time.sleep(1)

        try:
            review_button.click()
            # After clicking and waiting a bit
            time.sleep(3)

            wait.until(EC.presence_of_element_located((By.XPATH, "//h2[contains(text(), 'Results!')]")))
            logger.info(f"Results for {app_name} loaded successfully")

            return True
        
        except Exception as e:
            logger.error(f"Error locating results button for {app_name}")
            return False

    except Exception as e:
        logger.error(f"Error locating {app_name}")
        return False

def extract_question_answers(driver, start_idx=None, end_idx=None):
    try:
        # Find all question headers
        question_headers = driver.find_elements(By.XPATH, "//h5[contains(., 'Question')]")
        qa_pairs = {}
        
        for header in question_headers:
            try:
                # Get the question text
                header_text = header.text.strip()
                
                # Extract the question number
                question_number = None
                if "Question " in header_text:
                    # Extract number after "Question " (split by colon or space)
                    number_part = header_text.split("Question ")[1].split(":")[0].split(" ")[0].strip()
                    if number_part.isdigit():
                        question_number = int(number_part)
                
                # Skip if question number is outside our range
                if question_number is None:
                    continue
                    
                if (start_idx is not None and question_number < start_idx) or \
                   (end_idx is not None and question_number > end_idx):
                    continue
                
                # Create a key for this question
                question_key = f"Question {question_number}"
                
                # Get the question content (after the colon)
                question_content = ""
                if ":" in header_text:
                    question_content = header_text.split(":", 1)[1].strip()
                    
                # Extract answer paragraphs that follow this header
                # First, find this header's ID or create an XPath to uniquely identify it
                answer_paragraphs = []
                
                # This XPath gets all <p> elements that follow this h5 until the next h5
                p_elements = driver.execute_script("""
                    var header = arguments[0];
                    var paragraphs = [];
                    var nextElement = header.nextElementSibling;
                    
                    // Collect paragraphs until we hit the next h5
                    while (nextElement && nextElement.tagName.toLowerCase() !== 'h5') {
                        if (nextElement.tagName.toLowerCase() === 'p') {
                            paragraphs.push(nextElement);
                        }
                        nextElement = nextElement.nextElementSibling;
                    }
                    return paragraphs;
                """, header)
                
                # Extract text from all answer paragraphs
                answer_text = ""
                for p in p_elements:
                    p_text = p.text.strip()
                    if p_text:
                        if answer_text:
                            answer_text += "\n" + p_text
                        else:
                            answer_text = p_text
                
                # Store this Q&A pair
                qa_pairs[question_key] = answer_text
                logger.info(f"Extracted {question_key}: '{answer_text[:30]}...'")
                
            except Exception as e:
                logger.error(f"Error extracting Q&A for header '{header.text[:20]}...': {str(e)}")
                continue
        
        return qa_pairs
        
    except Exception as e:
        logger.error(f"Error extracting Q&As: {str(e)}")
        logger.error(traceback.format_exc())
        return {}

def extract_applicant_data(driver, start_question, end_question):
    wait = WebDriverWait(driver, 10)

    table_xpath = "//h2[contains(text(), 'Results!')]/following-sibling::table[1]"
    table = wait.until(EC.presence_of_element_located((By.XPATH, table_xpath)))

    logger.info("Found applicant table")

    row_count = len(table.find_elements(By.XPATH, ".//tbody/tr"))

    logger.info(f"Found {row_count} applicants to process")

    applicants_data = []
    
    for i in range(row_count):
        try:
            # Refind the table each time to avoid stale element references
            table = wait.until(EC.presence_of_element_located((By.XPATH, table_xpath)))
            
            # Get fresh references to the rows each time
            rows = table.find_elements(By.XPATH, ".//tbody/tr")
            row = rows[i]  # Get the current row

            # For the name (first and last name are in separate text nodes in a div)
            name_div = row.find_element(By.XPATH, ".//td[2]//div[@class='row'][1]//div")
            # Get the full text which contains both first and last name
            full_name_text = name_div.text
            name = full_name_text.replace('"', '').strip()  # Remove quotes and trim whitespace
            logger.info(f"Found {name}")
            
            # For the UIN (in the second row div)
            uin_div = row.find_element(By.XPATH, ".//td[2]//div[@class='row'][2]//div")
            uin = uin_div.text.strip()
            logger.info(f"Found {uin}")

            # For the email (in the third row div)
            email_div = row.find_element(By.XPATH, ".//td[2]//div[@class='row'][3]//div")
            email = email_div.text.strip()
            logger.info(f"Found {email}")

            # For the score (in the third column)
            score = row.find_element(By.XPATH, ".//td[3]").text.strip()
            logger.info(f"Found {score}")
            
            # Find the button in the last td - it's a button, not an anchor!
            app_button = row.find_element(By.XPATH, ".//td[4]/button")
            app_id = app_button.text.strip()
            
            logger.info(f"Extracted: {name}, {uin}, {email}, Score: {score}, App ID: {app_id}")
            
            # Store basic info before clicking
            applicant_data = {
                "Name": name,
                "UIN": uin,
                "Email": email,
                "Score": score,
                "App ID": app_id,
                "Major": "",
                "Grad Semester": "",
                "Grad Year": "",
                "Questions": {}

            }

            driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", app_button)

            time.sleep(1)
            
            # Now click the application ID button to get additional details
            app_button.click()

            try:
                time.sleep(3)

                # Wait for the details page to load by looking for the Tag header
                tag_xpath = "//h4[contains(text(), 'Tag:')]"
                wait.until(EC.presence_of_element_located((By.XPATH, tag_xpath)))

                #extract major
                try:
                    # Find the heading that contains the major question
                    major_question_xpath = "//h5[contains(., 'major') or contains(., 'Major')]"
                    wait.until(EC.presence_of_element_located((By.XPATH, major_question_xpath)))
                    
                    # Get the first paragraph after this heading - it should contain the major
                    major_xpath = "//h5[contains(., 'major') or contains(., 'Major')]/following-sibling::p[1]"
                    major_element = wait.until(EC.presence_of_element_located((By.XPATH, major_xpath)))
                    major = major_element.text.strip()
                    applicant_data["Major"] = major
                    logger.info(f"Extracted major: {major}")
                except Exception as e:
                    logger.error(f"Could not extract major: {str(e)}")
                    applicant_data["Major"] = "Unknown"

                #extract grad
                try:
                    grad_question_xpath = "//h5[contains(., 'graduation') or contains(., 'Graduation')]"
                    wait.until(EC.presence_of_element_located((By.XPATH, grad_question_xpath)))
                    
                    # Get the first paragraph after this heading - it should contain the graduation info
                    grad_xpath = "//h5[contains(., 'graduation') or contains(., 'Graduation')]/following-sibling::p[1]"
                    grad_element = wait.until(EC.presence_of_element_located((By.XPATH, grad_xpath)))
                    grad_text = grad_element.text.strip()
                    
                    # Parse the graduation text to extract semester and year
                    semester_keywords = ["Spring", "Fall"]
                    grad_sem = "Unknown"
                    grad_year = "Unknown"
                    
                    # Check for semester keywords and numbers
                    words = grad_text.split()
                    for i, word in enumerate(words):
                        if word in semester_keywords and i+1 < len(words):
                            # Found a semester keyword, check if the next word is a year
                            grad_sem = word
                            # Check if the next word is a 4-digit number (year)
                            if words[i+1].isdigit() and len(words[i+1]) == 4:
                                grad_year = words[i+1]
                                break
                    
                    applicant_data["Grad Semester"] = grad_sem
                    applicant_data["Grad Year"] = grad_year
                    logger.info(f"Extracted graduation: {grad_sem} {grad_year}")

                except Exception as e:
                    logger.error(f"Could not extract graduation info: {str(e)}")
                    applicant_data["Grad Semester"] = "Unknown"
                    applicant_data["Grad Year"] = "Unknown"
                
                #extract question data
                qa_pairs = extract_question_answers(driver, start_question, end_question)
                applicant_data["Questions"] = qa_pairs

            except Exception as e:
                logger.error(f"Error extracting major, grad:, and question responses: {str(e)}")

            finally:
                # Always go back to results page
                driver.back()
                time.sleep(3)  # Extra time to ensure page is fully loaded
                
                # Make sure we're back on the results page
                wait.until(EC.presence_of_element_located((By.XPATH, "//h2[contains(text(), 'Results!')]")))
                
                # Add this applicant's data to our list
                applicants_data.append(applicant_data)

        except Exception as e:
            logger.error(f"Error processing applicant {i+1}: {str(e)}")
            logger.error(traceback.format_exc())
            
            # If we got stuck on a details page, try to get back to results
            if "Results!" not in driver.page_source:
                try:
                    driver.back()
                    time.sleep(3)
                except:
                    logger.error("Failed to navigate back after error")
    return applicants_data

def export_to_json(data, app_name, folder_path="../../data"):
    # Create a filename with timestamp
    # timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    abs_folder_path = os.path.abspath(folder_path)

    if not os.path.exists(abs_folder_path):
        os.makedirs(abs_folder_path)
        logger.info(f"Created directory {abs_folder_path}")

    # Clean app_name for filename (remove special chars)
    clean_app_name = ''.join(c if c.isalnum() or c in [' ', '_'] else '_' for c in app_name)
    clean_app_name = clean_app_name.replace(' ', '_')
    
    # filename = f"{clean_app_name}_{timestamp}.json"
    filename = f"{clean_app_name}.json"
    fullpath = os.path.join(abs_folder_path, filename)
    
    try:
        with open(fullpath, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, indent=4)
        
        logger.info(f"Successfully exported data to {fullpath}")
        return fullpath
    except Exception as e:
        logger.error(f"Error exporting to JSON: {str(e)}")
        return None

def scrape_application(app_name, email, password, start_idx=None, end_idx=None, output_folder="../../data"):
    driver = None

    try:
        driver = initialize_driver()
        base_url = "https://members.secsystems.net/"
        login_url = base_url + "login"

        login_successful = login(driver, login_url, email, password)

        if not login_successful:
            logger.error("Login failed, aborting")
            return False
        
        target_url = base_url + "applications"
        navigation_successful = navigate_to_page(driver, target_url)

        if not navigation_successful:
            logger.error("Navigation failed, aborting")
            return False
        
        view_results_successful = view_results_of_application(driver, app_name)

        if not view_results_successful:
            logger.error("Error viewing application results, aborting")
            return False
        
        applicants_data = extract_applicant_data(driver, start_idx, end_idx)
        
        logger.info(f"Successfully extracted data for {len(applicants_data)} applicants")

        if len(applicants_data) == 0:
            logger.error("Error extracting applicant data")
            return False
        
        json_file = export_to_json(applicants_data, app_name, output_folder)
        
        if json_file:
            print(f"Data successfully exported to {json_file}")
            return True
        else:
            print("Failed to export data to JSON")
            return False
        
    except Exception as e:
        logger.error(f"Error during scraping: {str(e)}")
        logger.error(traceback.format_exc())
        return False
    finally:
        # Always close the driver to free resources
        if driver:
            logger.info("Closing WebDriver")
            driver.quit()

def main():
    email = "eunsooyeo@tamu.edu"
    password = "qlcthrma0530/Tam"
    app_name = "Spring 2025 New Member Application"

    scrape_application(app_name, email, password, 7, 9)
    
if __name__ == "__main__":
    print("Starting Selenium-based scraper for SEC Membership Hub...")
    result = main()
    
    if result:
        print("Scraping completed successfully.")
    else:
        print("Scraping encountered errors.")