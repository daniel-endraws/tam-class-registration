import selenium
import pathlib
from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

# Inputs that require waiting for a dropdown and searching for input
dropdown_inputs = ["s2id_txt_instructor"]

def navigate_to_search(driver: Chrome) -> None:
    """Navigates the driver to the search field"""
    driver.get('https://banssb.coloradomesa.edu/StudentRegistrationSsb/ssb/term/termSelection?mode=search')
    # Find and click on the term section
    driver.find_element(By.ID, "s2id_txt_term").click()
    driver.find_element(By.ID, "202104").click()
    driver.find_element(By.ID, "term-go").click()

    # Wait for next page to come up then click advanced search
    driver.find_element(By.ID, "advanced-search-link").click()

def input_search_params(driver: Chrome, search_params: dict) -> None:
    """Inputs all valid search params"""
    # Wait for form to load
    for input_id in search_params.keys():
        try:
            input_field = driver.find_element(By.ID, input_id)
            
            # For dropdown inputs we need to get the input and press enter
            if input_id in dropdown_inputs:
                input_field = input_field.find_element(By.TAG_NAME, "input")
                input_field.send_keys(search_params[input_id])
                # Wait for first dropdown option to appear
                driver.find_element(By.CLASS_NAME, "select2-result-label")
                input_field.send_keys(Keys.ENTER)
            else:
                input_field.send_keys(search_params[input_id])
        except BaseException as err:
            # DEBUG PRINT
            print(f"ERR on {input_id}\n{err}\n")
            continue

def scrape_classes(driver: Chrome) -> list[dict]:
    """Iterate through each row to scrape capacity"""
    table = driver.find_element(By.ID, "table1")
    # num_results to be first int in the string
    num_results = driver.find_element(By.CLASS_NAME, "results-out-of").text
    num_results = int(num_results.split(' ')[0])
    results = []
    for i in range(1, min(num_results, 10) + 1):
        # relative x-path //tbody/tr[i]
        row = table.find_element(By.XPATH, f"//tbody/tr[{i}]")
        result = {}
        result["course_name"] = row.find_element(By.XPATH, "//td[@data-property='courseTitle']").text

        status = row.find_element(By.XPATH,  "//td[@data-property='status']").text
        # Parse status text such that first number is seats remaining, and second number is total seats
        status = list(filter(lambda x: x.isdigit(), status.split(' ')))
        result["seats_left"] = status[0]
        result["total_seats"] = status[1]

        results.append(result)

    return results

def check_classes(search_params: dict) -> list[dict]:
    '''Performs a search with the inputted params

    Parameters:
        search_params (dict): A dictionary with field IDs and values
    
    Returns:
        List of dictionaries with "course_name", "seats_left", and "total_seats"
        of each of the classes that came out of the search (max top 10), or an empty list if nothing
    '''
    options = Options()
    # options.headless = True

    driver = Chrome(
        executable_path = f'{pathlib.Path(__file__).parent}/../bin/chromedriver.exe',
        options = options
    )

    driver.implicitly_wait(10)
    navigate_to_search(driver)
    input_search_params(driver, search_params)

    # Move to button (https://www.py4u.net/discuss/19767)
    button = driver.find_element(By.ID, "search-go")
    ActionChains(driver).move_to_element(button).click(button).perform()

    search_results = scrape_classes(driver)   

    driver.close()
    return search_results
