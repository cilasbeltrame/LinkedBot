from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains

import time

def home(user, password, tag='it recruiter', pages=1):
    chrome_options = Options()

    driver = webdriver.Chrome(options=chrome_options)

    driver.get("https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin")

    user_element = driver.find_element(By.ID, "username")
    password_element = driver.find_element(By.ID, "password")

    user_element.send_keys(user)
    password_element.send_keys(password)
    
    password_element.send_keys(Keys.RETURN)

    time.sleep(5)

    for idx in range(pages):
        # idx + 1 because range starts at zero
        search = f"https://www.linkedin.com/search/results/people/?keywords={tag}&origin=GLOBAL_SEARCH_HEADER&page={idx+1}"
        
        driver.get(search)
        
        profile_list_container = driver.find_element(By.CLASS_NAME, 'reusable-search__entity-result-list')
        
        profile_list = profile_list_container.find_elements(By.CLASS_NAME, 'reusable-search__result-container')
        
        driver.maximize_window()

        for profile in profile_list:
            # scroll to view better
            ActionChains(driver)\
                .scroll_to_element(profile)\
                .perform()
             
            name_container = profile.find_element(By.CLASS_NAME, 'entity-result__title-text')\
                .find_element(By.TAG_NAME, 'a')
            
            link = name_container.get_attribute('href')

            name = name_container.find_element(By.TAG_NAME, 'span')\
                .find_element(By.TAG_NAME, 'span')\
                .text
            
            button = profile.find_element(By.TAG_NAME, 'button')
            button_span = button.find_element(By.TAG_NAME, 'span')

            if button_span.text == "Connect":
                print(f"{name} - {link}\n")
                # button.click()
            elif button_span.text == "Follow": # open tab and connect
                driver.execute_script(f"window.open('{link}', 'new_Tab')") # open new tab
                driver.switch_to.window(driver.window_handles[-1]) # switch to new tab

                time.sleep(6)

                more_button = driver.find_element(By.CSS_SELECTOR, ".pvs-profile-actions [aria-label='More actions']")
                
                more_button.click()

                time.sleep(1)
                
                more_button_parent = more_button.find_element(By.XPATH, '..')

                option_more_button = more_button_parent.find_element(By.CSS_SELECTOR, f"[aria-label='Invite {name} to connect']")
                text_option_more_button = option_more_button.find_element(By.TAG_NAME, 'span').text

                time.sleep(1)

                if text_option_more_button == "Connect":
                    print(f"{name} - {link}\n")
                    # option_more_button.click()
                
                driver.close() # close current focused tab
                driver.switch_to.window(driver.window_handles[0]) # switch back to main tab
            else:
                continue      

            time.sleep(1) # wait 1s for the next iteration  

user = input("Insert your email: ")
password = input("Insert your password: ")
tag = input("Insert the tag to search people for: ")
pages = input("Insert how many pages do you want: ")
parsed_pages = int(pages)
# message = input("Envie a message de convite: ")

home(user, password, tag, parsed_pages)