import applicant_scraper
import logging
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import os, time, re

logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filename='selenium_debug3.log')
logger = logging.getLogger(__name__)

def update_grad(driver):
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

            # # For the name (first and last name are in separate text nodes in a div)
            # name_div = row.find_element(By.XPATH, ".//td[2]//div[@class='row'][1]//div")
            # # Get the full text which contains both first and last name
            # full_name_text = name_div.text
            # name = full_name_text.replace('"', '').strip()  # Remove quotes and trim whitespace
            # logger.info(f"Found {name}")
            
            # For the UIN (in the second row div)
            uin_div = row.find_element(By.XPATH, ".//td[2]//div[@class='row'][2]//div")
            uin = uin_div.text.strip()
            logger.info(f"Found {uin}")

            # # For the email (in the third row div)
            # email_div = row.find_element(By.XPATH, ".//td[2]//div[@class='row'][3]//div")
            # email = email_div.text.strip()
            # logger.info(f"Found {email}")

            # # For the score (in the third column)
            # score = row.find_element(By.XPATH, ".//td[3]").text.strip()
            # logger.info(f"Found {score}")
            
            # Find the button in the last td - it's a button, not an anchor!
            app_button = row.find_element(By.XPATH, ".//td[4]/button")
            app_id = app_button.text.strip()
            
            # logger.info(f"Extracted: {name}, {uin}, {email}, Score: {score}, App ID: {app_id}")
            logger.info(f"Extracting uin {uin}")
            
            # # Store basic info before clicking
            applicant_data = {
                "UIN": uin,
                "App ID": app_id,
                "Grad Semester": "",
                "Grad Year": ""
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
                
                #extract grad
                try:
                    grad_question_xpath = "//h5[contains(., 'graduation') or contains(., 'Graduation')]"
                    wait.until(EC.presence_of_element_located((By.XPATH, grad_question_xpath)))
                    
                    # Get the first paragraph after this heading - it should contain the graduation info
                    grad_xpath = "//h5[contains(., 'graduation') or contains(., 'Graduation')]/following-sibling::p[1]"
                    grad_element = wait.until(EC.presence_of_element_located((By.XPATH, grad_xpath)))
                    grad_text = grad_element.text.strip()
                    
                    # Parse the graduation text to extract semester and year
                    semester_keywords = ["spring", "fall", "may", "december", "winter"]
                    grad_sem = "Unknown"
                    grad_year = "Unknown"
                    
                    # Check for semester keywords and numbers
                    words = grad_text.split()
                    for word in words:
                        word = re.sub(r'[^\w\s]', '', word)
                        if word.lower() in semester_keywords:
                            # Found a semester keyword, check if the next word is a year
                            if word.lower() == "spring" or "may":
                                grad_sem = "Spring"
                            else:
                                grad_sem = "Fall"
                        elif "202" in word:
                            grad_year = word[:4]
                    
                    applicant_data["Grad Semester"] = grad_sem
                    applicant_data["Grad Year"] = grad_year
                    logger.info(f"Extracted graduation: {grad_sem} {grad_year}")

                except Exception as e:
                    logger.error(f"Could not extract graduation info: {str(e)}")
                    applicant_data["Grad Semester"] = "Unknown"
                    applicant_data["Grad Year"] = "Unknown"
                
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
            
            # If we got stuck on a details page, try to get back to results
            if "Results!" not in driver.page_source:
                try:
                    driver.back()
                    time.sleep(3)
                except:
                    logger.error("Failed to navigate back after error")
    return applicants_data


def update_applicant_grad_info(app_name, email, password, output_folder="../../data"):
    driver = None

    try:
        driver = applicant_scraper.initialize_driver()
        base_url = "https://members.secsystems.net/"
        login_url = base_url + "login"

        login_successful = applicant_scraper.login(driver, login_url, email, password)

        if not login_successful:
            logger.error("Login failed, aborting")
            return False
        
        target_url = base_url + "applications"
        navigation_successful = applicant_scraper.navigate_to_page(driver, target_url)

        if not navigation_successful:
            logger.error("Navigation failed, aborting")
            return False
        
        view_results_successful = applicant_scraper.view_results_of_application(driver, app_name)

        if not view_results_successful:
            logger.error("Error viewing application results, aborting")
            return False
        
        applicants_data = update_grad(driver)
        
        logger.info(f"Successfully extracted data for {len(applicants_data)} applicants")

        if len(applicants_data) == 0:
            logger.error("Error extracting applicant data")
            return False
        
        json_file = applicant_scraper.export_to_json(applicants_data, app_name+" Grad", output_folder)
        
        if json_file:
            print(f"Data successfully exported to {json_file}")
            return True
        else:
            print("Failed to export data to JSON")
            return False
        
    except Exception as e:
        logger.error(f"Error during scraping: {str(e)}")
        return False
    finally:
        # Always close the driver to free resources
        if driver:
            logger.info("Closing WebDriver")
            driver.quit()

def main():
    email = "eunsooyeo@tamu.edu"
    password = "qlcthrma0530/Tam"
    app_name = "Spring 2023 SEC New Member Application"

    update_applicant_grad_info(app_name, email, password)
    
if __name__ == "__main__":
    print("Starting Selenium-based scraper for SEC Membership Hub...")
    result = main()
    
    if result:
        print("Scraping completed successfully.")
    else:
        print("Scraping encountered errors.")