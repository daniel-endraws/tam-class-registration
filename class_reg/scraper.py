import selenium
import pathlib
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options

def set_cookies(driver: Chrome) -> None:
    driver.get('https://banssb.coloradomesa.edu/StudentRegistrationSsb/ssb/classSearch/classSearch')

    # Need to add these cookies to get to search screen
    server_id_cookie = driver.get_cookie("CMUSERVERIDPRODSRSSB")
    session_id_cookie = driver.get_cookie("JSESSIONID")
    server_id_cookie["value"] = "banss6"
    session_id_cookie["value"] = "083019972A17668D8752EB1142655DB3"

    driver.delete_cookie("CMUSERVERIDPRODSRSSB")
    driver.delete_cookie("JSESSIONID")
    driver.add_cookie(server_id_cookie)
    driver.add_cookie(session_id_cookie)

    return



def check_classes(search_params: dict) -> None:
    options = Options()
    # options.headless = True

    driver = Chrome(
        executable_path = f'{pathlib.Path(__file__).parent}/../bin/chromedriver.exe',
        options = options
    )
    
    set_cookies(driver)
    driver.get('https://banssb.coloradomesa.edu/StudentRegistrationSsb/ssb/classSearch/classSearch')

    driver.close()
