import selenium
import pathlib
from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
# waits
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Inputs that require waiting for a dropdown and searching for input
dropdown_inputs = ["s2id_txt_instructor"]

def navigate_to_search(driver: Chrome) -> None:
    """Navigates the driver to the search field"""
    driver.get('https://banssb.coloradomesa.edu/StudentRegistrationSsb/ssb/term/termSelection?mode=search')
    # Find and click on the term section
    driver.find_element(By.ID, "s2id_txt_term").click()
    # Wait for desired section to come up
    selection = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "202104"))
    )
    selection.click()
    driver.find_element(By.ID, "term-go").click()

    # Wait for next page to come up then click advanced search
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "advanced-search-link"))
    ).click()

def input_search_params(driver: Chrome, search_params: dict) -> None:
    """Inputs all valid search params"""
    # Wait for form to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "s2id_txt_subject"))
    )
    for input_id in search_params.keys():
        try:
            input_field = driver.find_element(By.ID, input_id)
            
            # For some inputs we need to wait for drop down w/ class 'select2-result-label' to appear
            if input_id in dropdown_inputs:
                input_field = input_field.find_element(By.TAG_NAME, "input")
                input_field.send_keys(search_params[input_id])
                # Wait for one option to pop up
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "select2-result-label"))
                )
                input_field.send_keys(Keys.ENTER)
            else:
                input_field.send_keys(search_params[input_id])
        except BaseException as err:
            # DEBUG PRINT
            print(f"ERR on {input_id}\n{err}\n")
            continue

def check_classes(search_params: dict) -> list[dict]:
    '''Performs a search with the inputted params

    Parameters:
        search_params (dict): A dictionary with field IDs and values
    
    Returns:
        List of dictionaries with the name, amount of students and the capacity
        of each of the classes that came out of the search, or an empty dictionary if nothing
    '''
    options = Options()
    # options.headless = True

    driver = Chrome(
        executable_path = f'{pathlib.Path(__file__).parent}/../bin/chromedriver.exe',
        options = options
    )
    
    navigate_to_search(driver)
    input_search_params(driver, search_params)
    # Click search button
    driver.find_element(By.ID, "search-go").click()

    driver.close()
