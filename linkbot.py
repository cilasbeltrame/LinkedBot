from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

import time

# def home(usuario,senha,tag,message):
def home(user,password,tag):
    chrome_options = Options()
    #chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(executable_path="chromedriver", options=chrome_options)
    driver.get("https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin")
    user_element = driver.find_element_by_id("username")
    password_element = driver.find_element_by_id("password")
    user_element.send_keys(user)
    password_element.send_keys(password)
    password_element.send_keys(Keys.RETURN)
    time.sleep(5)
    count = 1
    while count < 3:
        search = "https://www.linkedin.com/search/results/people/?keywords={}&origin=GLOBAL_SEARCH_HEADER&page={}".format(tag, count)
        driver.get(search)
        search_results = driver.find_element_by_class_name('reusable-search__entity-result-list')
        
        items = search_results.find_elements_by_class_name('reusable-search__result-container')
        # Store the ID of the original window
        original_window = driver.current_window_handle
        driver.maximize_window()
        for item in items:
            #print(result.find_element_by_class_name('ember-view').get_attribute("href"))
            button = item.find_element_by_tag_name('button')
            button_span = button.find_element_by_tag_name('span')
            entity_result = item.find_element_by_class_name('entity-result')
            entity = entity_result.find_element_by_class_name('entity-result__content')
            profile_config = entity.find_element_by_class_name('app-aware-link')
            profile_href = profile_config.get_attribute("href")
            profile_span = profile_config.find_element_by_tag_name('span')
            profile_name = profile_span.find_element_by_tag_name('span')
            print("{} - {}".format(profile_name.text, button_span.text))
            if button_span.text == "Connect":
                # button_span.click()
                print("Click!")
            elif button_span.text == "Follow":
                print("Open a tab and Connect")
                driver.execute_script("window.open('{}', 'new_Tab')".format(profile_href))
                time.sleep(6)
                more_button = driver.find_element((By.LINK_TEXT, 'More'))
                print(more_button.text)
                more_button.click()

            else:
                continue        
        count = count + 1
        # driver.switch_to.window(original_window)


user = input("Insira seu email: ")
password = input("Insira sua password: ")
tag = input("Insira a skill do profissional: ")
# message = input("Envie a message de convite: ")


# home(user,password,tag,message)
home(user,password,tag)
